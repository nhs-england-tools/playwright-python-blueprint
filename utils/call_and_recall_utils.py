import logging
import oracledb
from utils.oracle.oracle import OracleDB
from classes.repositories.general_repository import GeneralRepository
from classes.repositories.database_transition_parameters import (
    DatabaseTransitionParameters,
)
from classes.user_role_type import UserRoleType
from classes.repositories.user_repository import UserRepository


class CallAndRecallUtils:
    """
    This contains utility methods to do with Call and Recall
    """

    def __init__(self):
        self.oracledb = OracleDB()

    def run_failsafe(self, nhs_no: str) -> None:
        """
        Run the failsafe trawl for the given NHS number.
        Args:
            nhs_no: The NHS number of the subject
        """
        subject_id = int(self.oracledb.get_subject_id_from_nhs_number(nhs_no))
        conn = self.oracledb.connect_to_db()
        conn.callTimeout = 30000  # Setting call timeout to 30 seconds
        cur = conn.cursor()

        pi = cur.var(oracledb.NUMBER)
        pi.setvalue(0, subject_id)

        out_cursor = cur.var(oracledb.CURSOR)

        cur.execute(
            """
            BEGIN
                pkg_fobt_call.p_failsafe_trawl(
                    pi_subject_id => :pi,
                    po_cur_error  => :po
                );
            END;""",
            {"pi": str(subject_id), "po": out_cursor},
        )

        result_cursor = out_cursor.getvalue()
        row = result_cursor.fetchone()
        conn.commit()
        assert (
            "The action was performed successfully" in row
        ), f"Error when executing failsafe for {nhs_no}: {row}"

        # Clean up
        result_cursor.close()
        cur.close()
        conn.close()
        logging.info(f"[FAILSAFE TRAWL RUN] FOBT failsafe trawl run for subject {nhs_no}")

    def invite_subject_for_fobt_screening(
        self, nhs_no: str, user_role: UserRoleType
    ) -> None:
        """
        Runs the database transition to 'invite' the subject for FOBT screening and create an FOBT episode.
        Uses OracleDB to execute the stored procedure.
        Args:
            nhs_no (str): The NHS number of the subject
            user_role (UserRoleType): UserRoleType object for the user you are logged in as
        Raises:
            oracledb.DatabaseError: If there is an error in the execution of the stored procedure
        """
        logging.debug(f"START: invite_subject_for_fobt_screening for NHS No: {nhs_no}")

        try:
            # Prepare parameters for the stored procedure
            user_repository = UserRepository()
            general_repository = GeneralRepository()
            pio_id = user_repository.get_pio_id_for_role(user_role)
            database_transition_parameters = DatabaseTransitionParameters(
                transition_id=58,
                subject_id=int(self.oracledb.get_subject_id_from_nhs_number(nhs_no)),
                user_id=pio_id,
                rollback_on_failure="Y",
            )
            general_repository.run_database_transition(database_transition_parameters)
        except Exception as e:
            logging.error("Failsafe execution failed", exc_info=True)
            raise oracledb.DatabaseError(
                f"Error in invite_subject_for_fobt_screening for NHS No {nhs_no}: {e}"
            )
        logging.debug(f"END: invite_subject_for_fobt_screening for NHS No: {nhs_no}")
