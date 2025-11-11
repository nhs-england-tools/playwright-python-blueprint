import logging
from typing import Optional
from classes.subject.pi_subject import PISubject
from classes.subject.subject import Subject
from classes.user.user import User
from utils.oracle.oracle import OracleDB
from utils.oracle.subject_selection_query_builder import SubjectSelectionQueryBuilder


class SubjectRepository:
    """
    Repository class handling database access for subjects / patients.
    """

    def __init__(self):
        """
        Args:
            oracle_db: OracleDB instance for executing SQL queries.
        """
        self.oracle_db = OracleDB()

    def find_by_nhs_number(self, nhs_number: str) -> Optional[bool]:
        """
        Finds a subject by NHS number.
        """
        query = (
            "SELECT * FROM screening_subject_t WHERE subject_nhs_number = :nhs_number"
        )
        df = self.oracle_db.execute_query(query, {"nhs_number": nhs_number})
        if df.empty:
            return None
        return True

    def create_pi_subject(self, pio_id: int, pi_subject: PISubject) -> Optional[int]:
        """
        Creates a new screening subject, returning the contact id.

        Args:
            pio_id (int): The practitioner-in-organisation ID.
            pi_subject (PISubject): The subject to create.

        Returns:
            int: The new contact id.
        """
        logging.debug(f"Creating PI subject: {pi_subject}")
        nhs_number = pi_subject.nhs_number
        if nhs_number is None:
            raise ValueError("NHS Number must be specified when creating a new subject")
        if self.find_by_nhs_number(nhs_number) is not None:
            raise ValueError(
                f"Cannot create new subject with NHS Number {nhs_number} because it is already in use"
            )
        if pi_subject.pi_reference is None:
            raise ValueError(
                "A PI Reference must be specified when creating a new subject, for example 'SELF REFERRAL' or 'AUTOMATED TEST'"
            )

        return self.process_pi_subject(pio_id, pi_subject)

    def process_pi_subject(self, pio_id: int, pi_subject: PISubject) -> Optional[int]:
        """
        Processes a PI subject using the PKG_SSPI.p_process_pi_subject stored procedure.

        Args:
            pio_id (int): The practitioner-in-organisation ID.
            pi_subject (PISubject): The PI subject to process.

        Returns:
            Optional[int]: The new contact ID if successful, None otherwise.

        Raises:
            SubjectRepositoryException: If the stored procedure returns an error.
        """
        logging.debug(
            f"Processing PI subject: pio_id={pio_id}, pi_subject={pi_subject}"
        )

        procedure = "PKG_SSPI.p_process_pi_subject"
        conn = self.oracle_db.connect_to_db()
        obj_pi_subject_type = conn.gettype("MPI.OBJ_PI_SUBJECT")
        pi_struct = obj_pi_subject_type.newobject()
        for attr in obj_pi_subject_type.attributes:
            value = getattr(pi_subject, attr.name.lower())
            setattr(pi_struct, attr.name, value)

        in_params = [pi_struct, pio_id]
        out_params = [int, int, str]  # contact_id, error_id, error_text

        result = self.oracle_db.execute_stored_procedure(
            procedure,
            in_params=in_params,
            out_params=out_params,
            conn=conn,
        )

        new_contact_id = result.get(3)
        error_id = result.get(4)
        error_text = result.get(5)

        logging.debug(
            f"Stored procedure outputs: new_contact_id={new_contact_id}, error_id={error_id}, error_text={error_text}"
        )

        if error_id != 0:
            raise ValueError(f"Database error processing PI subject: {error_text}")

        return new_contact_id

    def update_pi_subject(self, pio_id: int, pi_subject: PISubject) -> None:
        """
        Updates an existing screening subject.

        Args:
            pi_subject (PISubject): The subject to update.
        """
        logging.debug(f"Updating PI subject: {pi_subject}")
        nhs_number = pi_subject.nhs_number
        if nhs_number is None:
            raise ValueError("NHS Number must be specified when creating a new subject")
        if self.find_by_nhs_number(nhs_number) is None:
            raise ValueError(
                f"Cannot find existing subject to update with NHS Number {nhs_number}"
            )
        if getattr(pi_subject, "pi_reference", None) is None:
            raise ValueError(
                "A PI Reference must be specified when updating an existing subject, for example 'SELF REFERRAL' or 'AUTOMATED TEST'"
            )
        self.process_pi_subject(pio_id, pi_subject)

    def get_active_gp_practice_in_hub_and_sc(
        self, hub_code: str, screening_centre_code: str
    ) -> Optional[str]:
        """
        Finds the org code of any active GP practice linked to both hub and screening centre.

        Args:
            hub_code (str): Hub code.
            screening_centre_code (str): Screening centre code.

        Returns:
            Optional[str]: GP practice org code.
        """
        query = """
        SELECT gp.org_code AS gp_code
        FROM org gp
        INNER JOIN gp_practice_current_links gpl ON gpl.gp_practice_id = gp.org_id
        INNER JOIN org hub ON hub.org_id = gpl.hub_id
        INNER JOIN org sc ON sc.org_id = gpl.sc_id
        WHERE hub.org_code = :hub_code AND sc.org_code = :sc_code
        """
        df = self.oracle_db.execute_query(
            query, {"hub_code": hub_code, "sc_code": screening_centre_code}
        )
        if df.empty:
            return None
        return df["gp_code"].iloc[0]

    def get_inactive_gp_practice(self) -> Optional[str]:
        """
        Finds the org code of any inactive GP practice (not linked to both hub and SC).

        Returns:
            Optional[str]: GP practice org code.
        """
        query = """
        SELECT gp.org_code AS gp_code
        FROM org gp
        LEFT OUTER JOIN gp_practice_current_links gpl ON gpl.gp_practice_id = gp.org_id
        WHERE gp.org_type_id = 1009 AND gpl.gp_practice_id IS NULL
        """
        df = self.oracle_db.execute_query(query)
        if df.empty:
            return None
        return df["gp_code"].iloc[0]

    def get_latest_gp_practice_for_subject(self, nhs_number: str) -> Optional[str]:
        """
        Finds the org code of the latest GP practice for a subject.

        Args:
            nhs_number (str): NHS number.

        Returns:
            Optional[str]: GP practice org code.
        """
        query = """
        SELECT gp.org_code AS gp_code
        FROM sd_contact_t c
        INNER JOIN subject_in_org sio ON sio.contact_id = c.contact_id
        INNER JOIN org gp ON gp.org_id = sio.org_id
        WHERE c.nhs_number = :nhs_number
        AND sio.org_type_id = 1009
        AND sio.sio_id = (SELECT MAX(siox.sio_id) FROM subject_in_org siox WHERE siox.contact_id = c.contact_id AND siox.org_type_id = 1009)
        """
        df = self.oracle_db.execute_query(query, {"nhs_number": nhs_number})
        if df.empty:
            return None
        return df["gp_code"].iloc[0]

    def get_matching_subject(
        self, criteria: dict, subject: Subject, user: User
    ) -> Subject:
        """
        Finds a subject in the DB matching the given criteria.
        Args:
            criteria (dict): The criteria you want the subject to match
            subject (Subject): The subject class object. Can be populated or not, depends on the criteria
            user (User): The user class object. Can be populated or not, depends on the criteria
        Returns:
            Subject: A populated Subject object with a subject that matches the provided criteria
        Raises:
            ValueError: If no subject matching the criteria was found.
        """
        builder = SubjectSelectionQueryBuilder()
        query, bind_vars = builder.build_subject_selection_query(
            criteria=criteria,
            user=user,
            subject=subject,
            subjects_to_retrieve=1,
        )
        df = OracleDB().execute_query(query, bind_vars)
        try:
            df_row = df.iloc[0]
            subject = Subject().from_dataframe_row(df_row)
        except Exception:
            raise ValueError("No subject found matching the given criteria")
        return subject

    def there_is_letter_batch_for_subject(
        self,
        nhs_no: str,
        letter_batch_code: str,
        letter_batch_title: str,
        assertion: bool = True,
    ) -> None:
        """
        Checks if the subject under test has a specific letter batch assosiated with them.
        Args:
            nhs_no (str): The subject's NHS number.
            letter_batch_code (str): The letter batch code.
            letter_batch_title (str): The letter batch title.
            assertion (bool): If the subject should have this batch (True), or should not have this batch (False).
        """
        sql_query = """ SELECT lb.batch_id
        FROM lett_batch_records lbr
        INNER JOIN lett_batch lb
        ON lb.batch_id = lbr.batch_id
        INNER JOIN valid_values ld
        ON ld.valid_value_id = lb.description_id
        INNER JOIN valid_values lbs
        ON lbs.valid_value_id = lb.status_id
        WHERE lb.batch_state_id = 12018
        AND lbr.screening_subject_id = :subject_id
        AND lbs.allowed_value = :batch_code
        AND LOWER(ld.description) = LOWER(:batch_title)
        AND lbr.non_inclusion_id IS NULL
        AND lbr.key_id != 11539
        """

        subject_id = self.oracle_db.get_subject_id_from_nhs_number(nhs_no)

        params = {
            "subject_id": subject_id,
            "batch_code": letter_batch_code,
            "batch_title": letter_batch_title,
        }

        batch_df = self.oracle_db.execute_query(sql_query, params)
        if assertion:
            assert (
                not batch_df.empty
            ), f"[DB ASSERTION FAILED] Subject {nhs_no} does not have a {letter_batch_code} - {letter_batch_title} batch when they are expected to"
            logging.info(
                f"[DB ASSERTION Passed] Subject {nhs_no} has a {letter_batch_code} - {letter_batch_title} batch"
            )
        else:
            assert (
                batch_df.empty
            ), f"[DB ASSERTION FAILED] Subject {nhs_no} has a {letter_batch_code} - {letter_batch_title} batch when they are expected not to"
            logging.info(
                f"[DB ASSERTION Passed] Subject {nhs_no} does not have a {letter_batch_code} - {letter_batch_title} batch"
            )
