import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Optional, Dict
from classes.date.date_description import DateDescription
from classes.date.date_description_utils import DateDescriptionUtils
from classes.person.person import Person
from classes.person.person_accreditation_status import PersonAccreditationStatus
from classes.person.person_role_status import PersonRoleStatus
from classes.person.person_selection_criteria_key import PersonSelectionCriteriaKey
from classes.role.role_type import RoleType
from classes.subject.subject import Subject
from classes.subject_selection_query_builder.selection_builder_exception import (
    SelectionBuilderException,
)
from classes.user.user import User
from utils.oracle.oracle import OracleDB

RESECT_AND_DISCARD_ACCREDITATION = 305730


class PersonRepository:
    """
    Repository class for building and executing person selection queries.
    """

    def __init__(self):
        self.oracle_db = OracleDB()
        self.sql_select = []
        self.sql_from = []
        self.sql_where = []
        self.sql_from_person_in_org = []
        self.sql_from_person_accreditation = []
        self.sql_order_by = []
        self.sql_query_end = []

        self.pio = ""

    def build_select_query_root(self) -> None:
        """
        Initializes the base SQL query components.
        """
        # Reset buffers
        self.sql_select = []
        self.sql_from = []
        self.sql_where = []
        self.sql_from_person_in_org = []
        self.sql_from_person_accreditation = []
        self.sql_order_by = []
        self.sql_query_end = []
        self.pio = ""
        self.sql_select.append(
            """
        SELECT
        prs.prs_id,
        prs.person_family_name,
        prs.person_given_name,
        prs.gmc_code,
        """
        )
        self.sql_from.append(" FROM person prs ")
        self.sql_where.append(" WHERE 1=1 ")

    def build_person_selection_query(
        self,
        criteria: Optional[Dict[str, str]] = None,
        person: Optional[Person] = None,
        required_person_count: Optional[int] = None,
        user: Optional[User] = None,
        subject: Optional[Subject] = None,
    ) -> str:
        """
        Builds a SQL query string to select persons based on the provided criteria.
        Args:
            criteria (Optional[Dict[str, str]]): A dictionary of selection criteria.
            person (Optional[Person]): A Person object for specific person-based criteria.
            required_person_count (Optional[int]): The required number of persons to select.
            user (Optional[User]): The user performing the selection, for context.
            subject (Optional[Subject]): The subject related to the selection, if applicable.
        Returns:
            str: The constructed SQL query string.
        """
        self.build_select_query_root()
        if criteria is not None:
            self.add_variable_selection_criteria(criteria, person, user, subject)

        if ".pio_id IS NOT NULL" not in "".join(self.sql_where):
            select_str = "".join(self.sql_select).rstrip()
            if not select_str.endswith(","):
                self.sql_select.append(",")
            self.sql_select.append(" NULL AS pio_id")
        if required_person_count is None:
            required_person_count = 1
        self.add_query_end(required_person_count)

        query = " ".join(
            str(part)
            for part in (
                self.sql_select
                + self.sql_from
                + self.sql_from_person_in_org
                + self.sql_from_person_accreditation
                + self.sql_where
                + self.sql_order_by
                + self.sql_query_end
            )
        )

        return query

    def add_variable_selection_criteria(
        self,
        criteria: Dict[str, str],
        person: Optional[Person],
        user: Optional[User],
        subject: Optional[Subject],
    ) -> None:
        """
        Adds variable selection criteria to the SQL query based on the provided criteria dictionary.
        Args:
            criteria (Dict[str, str]): A dictionary of selection criteria.
            person (Optional[Person]): A Person object for specific person-based criteria.
            user (Optional[User]): The user performing the selection, for context.
            subject (Optional[Subject]): The subject related to the selection, if applicable.
        """
        if person is not None:
            self.add_criteria_person_id(str(person.person_id))
        for criterium_key, criterium_value in criteria.items():
            self.criteria_comparator = "="
            self.criteria_value = criterium_value
            self.criteria_key_name = criterium_key
            if criterium_value.startswith("#"):
                criterium_value = ""

            if len(criterium_value) > 0:
                criteria_key = (
                    PersonSelectionCriteriaKey.by_description_case_insensitive(
                        criterium_key
                    )
                )
                match criteria_key:
                    case PersonSelectionCriteriaKey.FORENAMES:
                        self.add_criteria_person_forenames()
                    case (
                        PersonSelectionCriteriaKey.LATEST_RESECT_AND_DISCARD_ACCREDITATION_START_DATE
                    ):
                        self.add_criteria_latest_accreditation_start_date(
                            RESECT_AND_DISCARD_ACCREDITATION
                        )
                    case (
                        PersonSelectionCriteriaKey.LATEST_RESECT_AND_DISCARD_ACCREDITATION_CREATED_DATE
                    ):
                        self.add_criteria_latest_accreditation_created_date(
                            RESECT_AND_DISCARD_ACCREDITATION
                        )
                    case PersonSelectionCriteriaKey.PERSON_ID:
                        if person is None:
                            raise ValueError(
                                "Cannot select by PERSON_ID: 'person' is None."
                            )
                        self.add_criteria_person_id(str(person.person_id))
                    case PersonSelectionCriteriaKey.PERSON_HAS_CURRENT_ROLE:
                        self.add_criteria_person_has_role("current")
                    case PersonSelectionCriteriaKey.PERSON_HAS_ENDED_ROLE:
                        self.add_criteria_person_has_role("ended")
                    case PersonSelectionCriteriaKey.PERSON_HAS_NEVER_HAD_ROLE:
                        self.add_criteria_person_has_role("none")
                    case (
                        PersonSelectionCriteriaKey.PERSON_HAS_CURRENT_ROLE_IN_ORGANISATION
                        | PersonSelectionCriteriaKey.PERSON_HAS_ENDED_ROLE_IN_ORGANISATION
                        | PersonSelectionCriteriaKey.PERSON_HAS_NEVER_HAD_ROLE_IN_ORGANISATION
                    ):
                        self.add_criteria_person_has_role_organisation(user)
                    case (
                        PersonSelectionCriteriaKey.RESECT_AND_DISCARD_ACCREDITATION_STATUS
                    ):
                        self.add_criteria_person_accreditation(
                            RESECT_AND_DISCARD_ACCREDITATION, subject
                        )
                    case PersonSelectionCriteriaKey.ROLE_START_DATE:
                        self.add_criteria_role_start_date()
                    case PersonSelectionCriteriaKey.SURNAME:
                        self.add_criteria_person_surname()
                    case _:
                        raise ValueError(
                            f"Invalid person selection criteria key: {criterium_key}"
                        )

    def add_criteria_person_forenames(self) -> None:
        """
        Adds a criteria to filter a person by their forenames.
        """
        self.sql_where.append(
            f" AND LOWER(prs.person_given_name) = LOWER(TRIM('{self.criteria_value}')) "
        )

    def add_criteria_person_surname(self) -> None:
        """
        Adds a criteria to filter a person by their surname.
        """
        self.sql_where.append(
            f" AND LOWER(prs.person_family_name) = LOWER(TRIM('{self.criteria_value}')) "
        )

    def add_criteria_person_id(self, person_id: str) -> None:
        """
        Adds a criteria to filter a person by their unique identifier.
        Args:
            person_id (str): The unique identifier of the person.
        """
        self.sql_where.append(f" AND prs.prs_id = {person_id} ")

    def add_join_to_person_in_org(self, role: RoleType, role_exists: bool) -> None:
        """
        Adds a join to the person_in_org table for role-based criteria.
        Args:
            role (RoleType): The role type to filter by.
            role_exists (bool): Whether the role should exist for the person.
        """
        try:
            self.pio = "pio" + str(role.valid_value_id)
            sql_from_person_in_org_str = "".join(self.sql_from_person_in_org)
            pio_position = sql_from_person_in_org_str.rfind("person_in_org " + self.pio)
            if pio_position < 0:
                self.sql_from_person_in_org.append(
                    f" LEFT OUTER JOIN person_in_org {self.pio} ON {self.pio}.prs_id = prs.prs_id "
                )
                if role_exists:
                    pio2 = self.pio + "_2"
                    self.sql_from_person_in_org.append(
                        f""" AND NOT EXISTS (
                        SELECT 1
                        FROM person_in_org {pio2}
                        WHERE {self.pio}.prs_id = {pio2}.prs_id
                        AND {self.pio}.role_id = {pio2}.role_id
                        AND {self.pio}.pio_id != {pio2}.pio_id)
                        """
                    )
                    sql_order_by_str = "".join(self.sql_order_by)
                    if not sql_order_by_str.startswith(" ORDER BY "):
                        self.sql_order_by.append(" ORDER BY ")
                    else:
                        self.sql_order_by.append(", ")
                    self.sql_order_by.append(f" {self.pio}.start_date ASC ")
            else:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value + " (SECOND COPY!)"
                )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def add_criteria_person_has_role(self, role_state: str) -> None:
        """
        Adds criteria to filter people based on their role status.
        Args:
            role_state (str): The state of the role to filter by (e.g., "current", "ended", "none").
        """
        try:
            role_type = RoleType.by_description_case_insensitive(self.criteria_value)
            if role_type is None:
                raise ValueError(
                    f"Invalid role type description: {self.criteria_value}"
                )
            person_role_status = PersonRoleStatus.by_description_case_insensitive(
                role_state
            )
            self.add_join_to_person_in_org(
                role_type, role_exists=(person_role_status != PersonRoleStatus.NONE)
            )
            self.sql_from_person_in_org.append(
                f""" AND {self.pio}.role_id =
            {str(role_type.valid_value_id)} """
            )

            match person_role_status:
                case PersonRoleStatus.CURRENT:
                    self.sql_from_person_in_org.append(
                        f""" AND TRUNC(SYSDATE) BETWEEN
                    {self.pio}.start_date AND NVL({self.pio}.end_date, TO_DATE('31/12/3999','DD/MM/YYYY')) """
                    )
                case PersonRoleStatus.FUTURE:
                    self.sql_from_person_in_org.append(
                        f" AND {self.pio}.start_date > TRUNC(SYSDATE) "
                    )
                case PersonRoleStatus.ENDED:
                    self.sql_from_person_in_org.append(
                        f" AND {self.pio}.end_date < TRUNC(SYSDATE) "
                    )
            if person_role_status == PersonRoleStatus.NONE:
                self.sql_where.append(f" AND {self.pio}.pio_id IS NULL ")
            else:
                self.sql_where.append(f" AND {self.pio}.pio_id IS NOT NULL ")
                sql_select_str = "".join(self.sql_select)
                if ".pio_id" not in sql_select_str:
                    self.sql_select.append(f" {self.pio}.pio_id ")
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def add_criteria_person_has_role_organisation(self, user: Optional[User]) -> None:
        """
        Adds criteria to filter people based on their role status within a specific organisation.
        Args:
            user (Optional[User]): The user performing the selection, for context.
        """
        opio = "o" + self.pio
        org_code = self.criteria_value
        if self.criteria_value.lower().startswith("user's"):
            if user is None or user.organisation is None:
                raise ValueError("User has no organisation assigned.")
            org_code = user.organisation.code
        self.sql_from_person_in_org.append(
            f""" AND {self.pio}.org_id IN (
            SELECT {opio}.org_id FROM org {opio} WHERE
            {opio}.org_code = '{org_code}')
            """
        )

    def add_criteria_role_start_date(self) -> None:
        """
        Adds criteria to filter people based on the start date of their role.
        """
        self.sql_from_person_in_org.append(
            f" AND {self.pio}.start_date {self.date_comparison_clause()}"
        )

    def date_comparison_clause(self) -> str:
        """
        Constructs a SQL date comparison clause based on the criteria value.
        Returns:
            str: The SQL date comparison clause.
        Raises:
            SelectionBuilderException: If the criteria value is invalid.
        """
        try:
            if self.criteria_value.lower().startswith(
                "more than"
            ) and self.criteria_value.lower().endswith("ago"):
                comparator = " < "
            elif self.criteria_value.lower().startswith(
                "less than"
            ) and self.criteria_value.lower().endswith("ago"):
                comparator = " > "
            elif self.criteria_value.lower().startswith("within the last"):
                comparator = " >= "
            elif self.criteria_value.lower().startswith("before"):
                comparator = " < "
            elif self.criteria_value.lower().startswith("after"):
                comparator = " > "
            else:
                comparator = " = "
                date_to_compare = self.criteria_value

            if comparator != " = ":
                date_desc = DateDescription.by_description_case_insensitive(
                    self.criteria_value
                )
                if date_desc is None:
                    raise ValueError(f"Invalid date description: {self.criteria_value}")
                number_of_months = date_desc.number_of_months
                date_to_compare = (
                    datetime.today() - relativedelta(months=number_of_months)
                ).strftime("%d/%m/%Y")
            date_to_compare = DateDescriptionUtils.convert_description_to_sql_date(
                self.criteria_key_name, date_to_compare
            )
        except Exception:
            logging.debug(f"comparator: {comparator}")
            logging.debug(f"date_to_compare: {date_to_compare}")
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)
        return f" {comparator} {date_to_compare}"

    def add_join_to_latest_person_accreditation(
        self, accreditation_type_id: int, join_type: str
    ) -> None:
        """
        Adds a join to the latest person accreditation of a specific type.
        Args:
            accreditation_type_id (int): The ID of the accreditation type.
            join_type (str): The type of join to use (e.g., " INNER ", " LEFT OUTER ").
        Raises:
            SelectionBuilderException: If there is an error adding the join.
        """
        if not self.sql_from_person_accreditation:
            self.sql_from_person_accreditation.append(
                f""" {join_type} JOIN person_accreditation pa
                ON pa.prs_id = prs.prs_id
                AND pa.accreditation_id = (
                SELECT pax.accreditation_id
                FROM person_accreditation pax
                WHERE pax.prs_id = prs.prs_id
                AND pax.accreditation_type_id = {accreditation_type_id}
                ORDER BY pax.start_date DESC
                FETCH FIRST 1 ROW ONLY) """
            )

    def add_criteria_person_accreditation(
        self, accreditation_type_id: int, subject: Optional[Subject]
    ) -> None:
        """
        Adds criteria to filter people based on their accreditation status.
        Args:
            accreditation_type_id (int): The ID of the accreditation type.
            subject (Optional[Subject]): The subject related to the accreditation, if applicable.
        Raises:
            SelectionBuilderException: If there is an error adding the criteria.
        """
        try:
            person_accreditation_status = (
                PersonAccreditationStatus.by_description_case_insensitive(
                    self.criteria_value
                )
            )
            join_type = " INNER "
            if (
                person_accreditation_status == PersonAccreditationStatus.NONE
                or person_accreditation_status
                == PersonAccreditationStatus.NOT_ACCREDITED_AT_SUBJECTS_LATEST_DIAGNOSTIC_TEST
            ):
                join_type = " LEFT OUTER "
            self.add_join_to_latest_person_accreditation(
                accreditation_type_id, join_type
            )
            self.sql_from_person_accreditation.append(
                f" AND pa.accreditation_type_id = {accreditation_type_id}"
            )
            match person_accreditation_status:
                case PersonAccreditationStatus.CURRENT:
                    self.sql_from_person_accreditation.append(
                        """ AND pa.start_date <= TRUNC(SYSDATE)
                        AND pa.end_date > ADD_MONTHS(TRUNC(SYSDATE), 5)"""
                    )
                case PersonAccreditationStatus.EXPIRES_SOON:
                    self.sql_from_person_accreditation.append(
                        """ AND pa.start_date < TRUNC(SYSDATE)
                        AND pa.end_date BETWEEN TRUNC(SYSDATE)
                        AND ADD_MONTHS(TRUNC(SYSDATE), 5)"""
                    )
                case PersonAccreditationStatus.EXPIRED:
                    self.sql_from_person_accreditation.append(
                        """ AND pa.end_date < TRUNC(SYSDATE)"""
                    )
                case (
                    PersonAccreditationStatus.NOT_ACCREDITED_AT_SUBJECTS_LATEST_DIAGNOSTIC_TEST
                    | PersonAccreditationStatus.ACCREDITED_AT_SUBJECTS_LATEST_DIAGNOSTIC_TEST
                ):
                    if subject is None:
                        raise ValueError(
                            "Subject must be provided for this accreditation status criterium."
                        )
                    else:
                        self.sql_from_person_accreditation.append(
                            f""" AND (SELECT MAX(xt.confirmed_date) FROM
                            external_tests_t xt
                            WHERE xt.void = 'N'
                            AND xt.screening_subject_id = {str(subject.screening_subject_id)})
                            BETWEEN pa.start_date AND pa.end_date """
                        )
            if join_type == " LEFT OUTER ":
                self.sql_where.append(" AND pa.accreditation_id IS NULL ")
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def add_criteria_latest_accreditation_start_date(
        self, accreditation_type_id: int
    ) -> None:
        """
        Adds criteria to filter people based on the start date of their latest accreditation.
        Args:
            accreditation_type_id (int): The ID of the accreditation type.
        """
        self.add_criteria_latest_accreditation_date(
            accreditation_type_id, "pa.start_date"
        )

    def add_criteria_latest_accreditation_created_date(
        self, accreditation_type_id: int
    ) -> None:
        """
        Adds criteria to filter people based on the created date of their latest accreditation.
        Args:
            accreditation_type_id (int): The ID of the accreditation type.
        """
        self.add_criteria_latest_accreditation_date(
            accreditation_type_id, "TRUNC(pa.created_datestamp)"
        )

    def add_criteria_latest_accreditation_date(
        self, accreditation_type_id: int, sql_date_expression: str
    ) -> None:
        """
        Adds criteria to filter people based on a date attribute of their latest accreditation.
        Args:
            accreditation_type_id (int): The ID of the accreditation type.
            sql_date_expression (str): The SQL expression representing the date attribute to filter by.
        """
        self.add_join_to_latest_person_accreditation(accreditation_type_id, " INNER ")
        self.sql_from_person_accreditation.append(
            f""" AND {sql_date_expression} {self.date_comparison_clause()}"""
        )

    def add_query_end(self, required_person_count: int) -> None:
        """
        Adds the query end clause to limit the number of returned rows.
        Args:
            required_person_count (int): The required number of people to select.
        """
        self.sql_query_end.append(
            f" FETCH FIRST {str(required_person_count)} ROWS ONLY "
        )
