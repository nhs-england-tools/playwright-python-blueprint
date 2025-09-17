from classes.database.database_transition_parameters import (
    DatabaseTransitionParameters,
)
import logging
from utils.oracle.oracle import OracleDB
import oracledb


class GeneralRepository:
    """
    Repository for general database operations.
    """

    def __init__(self):
        self.oracle_db = OracleDB()

    def run_database_transition(
        self, database_transition_parameters: DatabaseTransitionParameters
    ) -> None:
        """
        Executes the PKG_EPISODE.p_set_episode_next_status stored procedure with the provided parameters.
        Args:
            database_transition_parameters (DatabaseTransitionParameters): The parameters for the database transition.
        Raises:
            oracledb.DatabaseError: If there is an error executing the database transition.
        """
        logging.debug(
            f"Running database transition with transition_id = {database_transition_parameters.transition_id}"
        )
        conn = self.oracle_db.connect_to_db()
        try:
            cursor = conn.cursor()
            procedure_name = "PKG_EPISODE.p_set_episode_next_status"
            params = database_transition_parameters.to_params_list()
            params[-2] = cursor.var(oracledb.CURSOR)  # po_error_cur
            params[-1] = cursor.var(oracledb.CURSOR)  # po_data_cur

            cursor.callproc(procedure_name, params)

            # Fetch output from the cursors
            error_cursor = params[-2].getvalue()
            error_rows = error_cursor.fetchall() if error_cursor is not None else []

            success = any(
                "The action was performed successfully" in str(row)
                for row in error_rows
            )

            assert success, f"Error when executing database transition: {error_rows}"

            conn.commit()
            logging.debug("Database transition executed successfully.")
        except Exception as e:
            logging.error("Database transition failed", exc_info=True)
            raise oracledb.DatabaseError(f"Error executing database transition: {e}")
        finally:
            self.oracle_db.disconnect_from_db(conn)
