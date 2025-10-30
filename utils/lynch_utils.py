import logging
import random
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from typing import Optional

from classes.date.date_description_utils import DateDescriptionUtils
from classes.repositories.general_repository import GeneralRepository
from classes.screening.region_type import RegionType
from classes.data.data_creation import DataCreation
from classes.repositories.word_repository import WordRepository
from classes.repositories.subject_repository import SubjectRepository
from classes.user.user import User
from classes.user.user_role_type import UserRoleType
from classes.subject.gender_type import GenderType
from classes.subject_selection_query_builder.selection_builder_exception import (
    SelectionBuilderException,
)

from utils import nhs_number_tools
from utils.oracle.oracle import OracleDB

DATE_FORMAT_DD_MM_YYYY = "%d/%m/%Y"
DATE_OF_BIRTH_DESCRIPTION = "Date of birth description"
DIAGNOSIS_DATE_DESCRIPTION = "Diagnosis date description"
LAST_COLONOSCOPY_DATE_DESCRIPTION = "Last colonoscopy date description"


class LynchUtils:
    @staticmethod
    def insert_validated_lynch_patient_from_new_subject_with_age(
        age: str,
        gene: str,
        when_diagnosis_took_place: str,
        when_last_colonoscopy_took_place: str,
        user_role: UserRoleType,
    ) -> str:
        """
        Inserts a validated Lynch patient into the database with the specified age and other details.
        Args:
            age (str): The age of the patient.
            gene (str): The gene associated with the patient's Lynch syndrome.
            when_diagnosis_took_place (str): The date when the diagnosis took place.
            when_last_colonoscopy_took_place (str): The date when the last colonoscopy took place.
            user_role (UserRoleType): The role of the user performing the action.
        Returns:
            str: The NHS number of the newly created Lynch patient.
        """
        logging.debug(
            f"[START] insert_validated_lynch_patient_from_new_subject_with_age({age}, {gene}, {when_diagnosis_took_place}, {when_last_colonoscopy_took_place})"
        )

        PLUS = "+"
        MINUS = "-"
        LESS = "less"

        try:
            if age.endswith(" days") or age.endswith(" day"):
                parts = age.split(" ")
                if len(parts) != 4:
                    raise SelectionBuilderException("Invalid age format", age)
                years = int(parts[0])
                plus_or_minus = parts[1]
                days = int(parts[2])
            else:
                years = int(age)
                days = random.randint(0, 363)
                plus_or_minus = PLUS
        except Exception:
            raise SelectionBuilderException("Invalid age format", age)

        date_of_birth = datetime.today().date().replace(
            day=15, month=10
        ) - relativedelta(years=years)
        if plus_or_minus in [MINUS, LESS]:
            date_of_birth += timedelta(days=days)
        else:
            date_of_birth -= timedelta(days=days)

        nhs_number = LynchUtils.insert_validated_lynch_patient_from_new_subject(
            date_of_birth,
            gene,
            when_diagnosis_took_place,
            when_last_colonoscopy_took_place,
            user_role,
        )

        logging.debug("[END] insert_validated_lynch_patient_from_new_subject_with_age")
        return nhs_number

    @staticmethod
    def insert_validated_lynch_patient_from_new_subject(
        date_of_birth: Optional[date],
        gene: str,
        when_diagnosis_took_place: str,
        when_last_colonoscopy_took_place: str,
        user_role: UserRoleType,
    ) -> str:
        """
        Inserts a validated Lynch patient into the database.
        Args:
            date_of_birth (Optional[date]): The date of birth of the patient.
            gene (str): The gene associated with the patient's Lynch syndrome.
            when_diagnosis_took_place (str): The date when the diagnosis took place.
            when_last_colonoscopy_took_place (str): The date when the last colonoscopy took place.
            user_role (UserRoleType): The role of the user performing the action.
        Returns:
            str: The NHS number of the newly created Lynch patient.
        """
        logging.debug(
            f"[START] insert_validated_lynch_patient_from_new_subject({date_of_birth}, {gene}, {when_diagnosis_took_place}, {when_last_colonoscopy_took_place})"
        )

        # Random subject creation
        data_creation = DataCreation()
        word_repo = WordRepository()
        subject_repo = SubjectRepository()
        pi_subject = data_creation.generate_random_subject(
            word_repo.get_random_subject_details(),
            "NEW LYNCH TEST SUBJECT",
            region=RegionType.get_region("England"),
        )

        # Ensure NHS number uniqueness
        attempts = 1
        max_attempts = 100
        while True:
            if pi_subject.nhs_number is None:
                raise SelectionBuilderException(
                    "Generated subject has no NHS number", None
                )
            if (
                subject_repo.find_by_nhs_number(pi_subject.nhs_number) is None
                or attempts > max_attempts
            ):
                break
            pi_subject.nhs_number = (
                nhs_number_tools.NHSNumberTools.generate_random_nhs_number()
            )
            attempts += 1

        if attempts > max_attempts:
            raise SelectionBuilderException(
                "Could not generate unique NHS number", None
            )

        LynchUtils.delete_validated_lynch_patient(pi_subject.nhs_number)

        # Parse and convert dates properly
        diagnosis_date = DateDescriptionUtils.convert_description_to_python_date(
            DIAGNOSIS_DATE_DESCRIPTION, when_diagnosis_took_place
        )
        last_colonoscopy_date = DateDescriptionUtils.convert_description_to_python_date(
            LAST_COLONOSCOPY_DATE_DESCRIPTION, when_last_colonoscopy_took_place
        )

        # Gender mapping
        gender_code = (
            pi_subject.gender_code if pi_subject.gender_code is not None else 0
        )
        gender_type = GenderType.by_redefined_value(gender_code)
        gender_value = gender_type.allowed_value if gender_type else "Unknown"

        # User/org
        user = User.from_user_role_type(user_role)
        org_code = (
            user.organisation.code
            if user.organisation and user.organisation.code
            else "Unknown"
        )

        # Prepare SQL
        sql_query = """
        INSERT INTO validated_lynch_patients (
            gene, diagnosis_date, last_colonoscopy_date, genetics_team, processing_status,
            created_datestamp, updated_datestamp, audit_reason, consultant, registry_id, file_name,
            nhs_number, title, family_name, given_name, other_names, date_of_birth, gender,
            address_line_1, address_line_2, address_line_3, address_line_4, address_line_5, postcode,
            gp_practice_code, validation_error, updated_user_code, date_of_death
        )
        SELECT
            :gene AS gene,
            :diagnosis_date AS diagnosis_date,
            :last_colonoscopy_date AS last_colonoscopy_date,
            (SELECT site_code FROM sites WHERE site_type_id = 306448 AND end_date IS NULL
            ORDER BY DBMS_RANDOM.random FETCH FIRST 1 ROW ONLY) AS genetics_team,
            'BCSS_READY' AS processing_status,
            SYSDATE AS created_datestamp,
            SYSDATE AS updated_datestamp,
            'AUTO TESTING' AS audit_reason,
            'PROFESSOR AUTO TESTING' AS consultant,
            1234 AS registry_id,
            'AUTO_TESTING.csv' AS file_name,
            :nhs_number AS nhs_number,
            :title AS title,
            :family_name AS family_name,
            :given_name AS given_name,
            :other_names AS other_names,
            :date_of_birth AS date_of_birth,
            :gender AS gender,
            :address_line_1 AS address_line_1,
            :address_line_2 AS address_line_2,
            :address_line_3 AS address_line_3,
            :address_line_4 AS address_line_4,
            :address_line_5 AS address_line_5,
            :postcode AS postcode,
            (SELECT gp.org_code
            FROM gp_practice_current_links gpl
            INNER JOIN org gp ON gp.org_id = gpl.gp_practice_id
            INNER JOIN org hub ON hub.org_id = gpl.hub_id
            WHERE hub.org_code = :org_code
            ORDER BY DBMS_RANDOM.random FETCH FIRST 1 ROW ONLY) AS gp_practice_code,
            NULL AS validation_error,
            NULL AS updated_user_code,
            NULL AS date_of_death
        FROM dual
        """

        params = {
            "gene": gene,
            "diagnosis_date": diagnosis_date,
            "last_colonoscopy_date": last_colonoscopy_date,
            "nhs_number": pi_subject.nhs_number,
            "title": pi_subject.name_prefix,
            "family_name": pi_subject.family_name,
            "given_name": pi_subject.first_given_names,
            "other_names": pi_subject.other_given_names,
            "date_of_birth": date_of_birth,
            "gender": gender_value,
            "address_line_1": pi_subject.address_line_1,
            "address_line_2": pi_subject.address_line_2,
            "address_line_3": pi_subject.address_line_3,
            "address_line_4": pi_subject.address_line_4,
            "address_line_5": pi_subject.address_line_5,
            "postcode": pi_subject.postcode,
            "org_code": org_code,
        }

        db_query = OracleDB()
        logging.info(f"Executing query with parameters: {params}")
        rows_affected = db_query.update_or_insert_data_to_table(sql_query, params)
        logging.info(f"Rows affected = {rows_affected}")

        LynchUtils.process_new_lynch_patients()

        logging.debug("[END] insert_validated_lynch_patient_from_new_subject")
        return pi_subject.nhs_number

    @staticmethod
    def delete_validated_lynch_patient(nhs_number: str) -> None:
        """
        Deletes a validated Lynch patient from the database based on NHS number.
        Args:
            nhs_number (str): The NHS number of the patient to delete.
        """
        db_query = OracleDB()
        sql = "DELETE FROM validated_lynch_patients WHERE nhs_number = :nhs_number"
        db_query.update_or_insert_data_to_table(sql, {"nhs_number": nhs_number})

    @staticmethod
    def process_new_lynch_patients() -> None:
        """
        Processes new Lynch patients in the system.
        """
        general_repository = GeneralRepository()
        general_repository.process_new_lynch_patients()
