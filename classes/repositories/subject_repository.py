import logging
from typing import Optional
from classes.pi_subject import PISubject
from utils.oracle.oracle import OracleDB


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

    def update_pi_subject(self, pi_subject: PISubject) -> None:
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
        procedure = "PKG_SSPI.p_process_pi_subject"
        params = [pi_subject, None, None, None, None]
        self.oracle_db.execute_stored_procedure(procedure, params)

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
        return df.iloc[0]["gp_code"]

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
        return df.iloc[0]["gp_code"]

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
        return df.iloc[0]["gp_code"]
