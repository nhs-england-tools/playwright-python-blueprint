import oracledb
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import logging


class OracleDB:
    def __init__(self):
        load_dotenv()
        self.user = os.getenv("ORACLE_USERNAME")
        self.dns = os.getenv("ORACLE_DB")
        self.password = os.getenv("ORACLE_PASS")

    def connect_to_db(self) -> oracledb.Connection:
        """
        This function is used to connect to the Oracle DB. All the credentials are retrieved from a .env file
        """
        try:
            logging.info("Attempting DB connection...")
            conn = oracledb.connect(
                user=self.user, password=self.password, dsn=self.dns
            )
            logging.info("DB connection successful!")
            return conn
        except Exception as queryExecutionError:
            logging.error(
                f"Failed to to extract subject ID with error: {queryExecutionError}"
            )

    def disconnect_from_db(self, conn) -> None:
        conn.close()
        logging.info("Connection Closed")

    def exec_bcss_timed_events(
        self, nhs_number_df
    ) -> None:  # Executes bcss_timed_events when given NHS numbers
        """
        this function is used to execute bcss_timed_events against NHS Numbers.
        It expects the nhs_numbers to be in a dataframe, and runs a for loop to get the subject_screening_id for each nhs number
        Once a subject_screening_id is retrieved, it will then run the command: exec bcss_timed_events [<subject_id>,'Y']
        """
        conn = self.connect_to_db()
        try:
            for index, row in nhs_number_df.iterrows():
                subject_id = self.get_subject_id_from_nhs_number(
                    row["subject_nhs_number"]
                )
                try:
                    logging.info(
                        f"Attempting to execute stored procedure: {f"'bcss_timed_events', [{subject_id},'Y']"}"
                    )
                    cursor = conn.cursor()
                    cursor.callproc("bcss_timed_events", [subject_id, "Y"])
                    logging.info("Stored procedure execution successful!")
                except Exception as spExecutionError:
                    logging.error(
                        f"Failed to execute stored procedure with execution error: {spExecutionError}"
                    )
        except Exception as queryExecutionError:
            logging.error(
                f"Failed to to extract subject ID with error: {queryExecutionError}"
            )
        finally:
            if conn is not None:
                self.disconnect_from_db(conn)

    def get_subject_id_from_nhs_number(self, nhs_number) -> str:
        """
        This function is used to obtain the subject_screening_id of a subject when given an nhs number
        """
        conn = self.connect_to_db()
        logging.info(f"Attempting to get subject_id from nhs number: {nhs_number}")
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT SCREENING_SUBJECT_ID FROM SCREENING_SUBJECT_T WHERE SUBJECT_NHS_NUMBER = {int(nhs_number)}"
        )
        result = cursor.fetchall()
        subject_id = result[0][0]
        logging.info(f"Able to extract subject ID: {subject_id}")
        return subject_id

    def populate_ui_approved_users_table(
        self, user: str
    ) -> None:  # To add users to the UI_APPROVED_USERS table
        """
        This function is used to add a user to the UI_APPROVED_USERS table
        """
        conn = self.connect_to_db()
        try:
            logging.info("Attempting to write to the db...")
            cursor = conn.cursor()
            cursor.execute(
                f"INSERT INTO UI_APPROVED_USERS (OE_USER_CODE) VALUES ('{user}')"
            )
            conn.commit()
            logging.info("DB write successful!")
        except Exception as dbWriteError:
            logging.error(f"Failed to write to the DB! with write error {dbWriteError}")
        finally:
            if conn is not None:
                self.disconnect_from_db(conn)

    def delete_all_users_from_approved_users_table(
        self,
    ) -> None:  # To remove all users from the UI_APPROVED_USERS table
        """
        This function is used to remove users from the UI_APPROVED_USERS table where OE_USER_CODE is not null
        """
        conn = self.connect_to_db()
        try:
            logging.info("Attempting to delete users from DB table...")
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM UI_APPROVED_USERS WHERE OE_USER_CODE is not null"
            )
            conn.commit()
            logging.info("DB table values successfully deleted!")
        except Exception as dbValuesDeleteError:
            logging.error(
                f"Failed to delete values from the DB table! with data deletion error {dbValuesDeleteError}"
            )
        finally:
            if conn is not None:
                self.disconnect_from_db(conn)

    def execute_query(
        self, query: str, parameters: list | None = None
    ) -> pd.DataFrame:  # To use when "select xxxx" (stored procedures)
        """
        This is used to execute any sql queries.
        A query is provided and then the result is returned as a pandas dataframe
        """
        conn = self.connect_to_db()
        engine = create_engine("oracle+oracledb://", creator=lambda: conn)
        try:
            df = pd.read_sql(query, engine) if parameters == None else pd.read_sql(query, engine, params = parameters)
        except Exception as executionError:
            logging.error(
                f"Failed to execute query with execution error {executionError}"
            )
        finally:
            if conn is not None:
                self.disconnect_from_db(conn)
        return df

    def execute_stored_procedure(
        self, procedure: str
    ) -> None:  # To use when "exec xxxx" (stored procedures)
        """
        This is to be used whenever we need to execute a stored procedure.
        It is provided with the stored procedure name and then executes it
        """
        conn = self.connect_to_db()
        try:
            logging.info(f"Attempting to execute stored procedure: {procedure}")
            cursor = conn.cursor()
            cursor.callproc(procedure)
            conn.commit()
            logging.info("stored procedure execution successful!")
        except Exception as executionError:
            logging.error(
                f"Failed to execute stored procedure with execution error: {executionError}"
            )
        finally:
            if conn is not None:
                self.disconnect_from_db(conn)

    def update_or_insert_data_to_table(
        self, statement, params
    ) -> None:  # To update or insert data into a table
        """
        This is used to update or insert data into a table.
        It is provided with the SQL statement along with the arguments
        """
        conn = self.connect_to_db()
        try:
            logging.info("Attempting to insert/update table")
            cursor = conn.cursor()
            cursor.execute(statement, params)
            conn.commit()
            logging.info("DB table successfully updated!")
        except Exception as dbUpdateInsertError:
            logging.error(
                f"Failed to insert/update values from the DB table! with error {dbUpdateInsertError}"
            )
        finally:
            if conn is not None:
                self.disconnect_from_db(conn)
