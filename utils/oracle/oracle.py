from tkinter import N
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

        Returns:
            conn (oracledb.Connection): The Oracle DB connection object
        """
        try:
            logging.info("Attempting DB connection...")
            conn = oracledb.connect(
                user=self.user, password=self.password, dsn=self.dns
            )
            logging.info("DB connection successful!")
            return conn
        except Exception as queryExecutionError:
            raise RuntimeError(f"Database connection failed: {queryExecutionError}")

    def disconnect_from_db(self, conn: oracledb.Connection) -> None:
        """
        Disconnects from the DB

        Args:
            conn (oracledb.Connection): The Oracle DB connection object
        """
        conn.close()
        logging.info("Connection Closed")

    def exec_bcss_timed_events(
        self, nhs_number_df: pd.DataFrame
    ) -> None:  # Executes bcss_timed_events when given NHS numbers
        """
        This function is used to execute bcss_timed_events against NHS Numbers.
        It expects the nhs_numbers to be in a dataframe, and runs a for loop to get the subject_screening_id for each nhs number
        Once a subject_screening_id is retrieved, it will then run the command: exec bcss_timed_events [<subject_id>,'Y']

        Args:
            nhs_number_df (pd.DataFrame): A dataframe containing all of the NHS numbers as separate rows
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

    def get_subject_id_from_nhs_number(self, nhs_number: str) -> str:
        """
        This function is used to obtain the subject_screening_id of a subject when given an nhs number

        Args:
            nhs_number (str): The NHS number of the subject

        Returns:
            subject_id (str): The subject id for the provided nhs number
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

        Args:
            user (str): The user you want to add to the table
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
        self, query: str, parameters: dict | None = None
    ) -> pd.DataFrame:  # To use when "select xxxx" (stored procedures)
        """
        This is used to execute any sql queries.
        A query is provided and then the result is returned as a pandas dataframe

        Args:
            query (str): The SQL query you wish to run
            parameters (dict | None): Optional - Any parameters you want to pass on in a dictionary

        Returns:
            df (pd.DataFrame): A pandas dataframe of the result of the query
        """
        conn = self.connect_to_db()
        engine = create_engine("oracle+oracledb://", creator=lambda: conn)
        df = pd.DataFrame()

        try:
            df = (
                pd.read_sql(query, engine)
                if parameters == None
                else pd.read_sql(query, engine, params=parameters)
            )
        except Exception as executionError:
            logging.error(
                f"Failed to execute query with execution error {executionError}"
            )
        finally:
            if conn is not None:
                self.disconnect_from_db(conn)
        return df

    def execute_stored_procedure(
        self, procedure: str, params: list = [None]
    ) -> None:  # To use when "exec xxxx" (stored procedures)
        """
        This is to be used whenever we need to execute a stored procedure.
        It is provided with the stored procedure name and then executes it

        Args:
            procedure (str): The stored procedure you want to run
        """
        conn = self.connect_to_db()
        try:
            logging.info(f"Attempting to execute stored procedure: {procedure}")
            cursor = conn.cursor()
            if params is not None:
                cursor.callproc(procedure, params)
            else:
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
        self, statement: str, params: dict
    ) -> None:  # To update or insert data into a table
        """
        This is used to update or insert data into a table.
        It is provided with the SQL statement along with the arguments

        Args:
            statement (str): The SQL query you wish to run
            params (list | None): Any parameters you want to pass on in a list
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


class OracleSubjectTools(OracleDB):
    def __init__(self):
        super().__init__()

    def create_subjects_via_sspi(
        self,
        count: int,
        screening_centre: str,
        base_age: int,
        start_offset: int = -2,
        end_offset: int = 4,
        nhs_start: int = 9200000000,
    ) -> None:
        """
        Creates a batch of test screening subjects using the SSPI stored procedure.

        This method invokes `PKG_SSPI.p_process_pi_subject` in the database, which generates
        synthetic subjects with varying dates of birth and NHS numbers starting from a given base.

        Args:
            count (int): Number of subjects to create.
            screening_centre (str): Code for the target screening centre (e.g., 'BCS01').
            base_age (int): Age around which the subjects are distributed.
            start_offset (int, optional): Days before today for earliest DOB (default -2).
            end_offset (int, optional): Days after today for latest DOB (default 4).
            nhs_start (int, optional): Starting NHS number for generated subjects (default 9200000000).

        Logs:
            Error message if subject generation fails.

        Side Effects:
            Commits to the database; subjects are available for further test flows.
        """
        conn = self.connect_to_db()
        try:
            cursor = conn.cursor()
            cursor.callproc(
                "PKG_SSPI.p_process_pi_subject",
                [
                    count,
                    screening_centre,
                    base_age,
                    start_offset,
                    end_offset,
                    nhs_start,
                ],
            )
            conn.commit()
        except Exception as e:
            logging.error(f"Failed to generate subjects: {e}")
        finally:
            self.disconnect_from_db(conn)

    def create_self_referral_ready_subject(
        self, screening_centre: str = "BCS002", base_age: int = 75
    ) -> str:
        """
        Creates a subject in the database with no screening history who is eligible to self refer.
        Uses PKG_SSPI.p_process_pi_subject to insert the subject,
        then retrieves the NHS number based on age and applies bcss_timed_events.

        Args:
            screening_centre (str): The screening centre code to associate the subject with.
            base_age (int): The minimum age threshold for subject date of birth.

        Returns:
            str: The NHS number of the created subject.
        """
        # Step 1: Generate subject via stored procedure
        self.create_subjects_via_sspi(
            count=1,
            screening_centre=screening_centre,
            base_age=base_age,
            start_offset=-2,
            end_offset=4,
            nhs_start=9200000000,
        )

        # Step 1a: Retrieve NHS number by joining SCREENING_SUBJECT_T and SD_CONTACT_T
        # - Ensures subject exists in both tables
        # - Filters by minimum age using DATE_OF_BIRTH
        # - Sorted by NHS number descending to get most recent insert

        query = """
            SELECT s.SUBJECT_NHS_NUMBER
            FROM SCREENING_SUBJECT_T s
            JOIN SD_CONTACT_T c ON s.SUBJECT_NHS_NUMBER = c.NHS_NUMBER
            WHERE c.DATE_OF_BIRTH <= ADD_MONTHS(TRUNC(SYSDATE), -12 * :min_age)
            ORDER BY s.SUBJECT_NHS_NUMBER DESC
            FETCH FIRST 1 ROWS ONLY
        """
        df = self.execute_query(query, {"min_age": base_age})

        if df.empty:
            raise RuntimeError(f"No subjects found aged {base_age}+ in both tables.")

        nhs_number = df.iloc[0]["subject_nhs_number"]
        logging.info(f"[SUBJECT CREATED WITH AGE {base_age}+] NHS number: {nhs_number}")

        # Step 2: Progress timeline
        nhs_df = pd.DataFrame({"subject_nhs_number": [nhs_number]})
        self.exec_bcss_timed_events(nhs_df)

        logging.info(f"[SUBJECT READY FOR SELF REFERRAL] NHS number: {nhs_number}")
        return nhs_number

    def open_subject_by_nhs(self, nhs_number: str) -> "OracleSubjectTools":
        """
        Placeholder for accessing a subject by NHS number.
        While no front-end page exists for subject viewing, this method preserves test readability
        and signals that the subject record is now active within the test context.

        Args:
            nhs_number (str): The NHS number of the subject you want to access.

        Returns:
            OracleSubjectTools: Returns self for method chaining.
        """
        logging.info(f"[SUBJECT ACCESS] NHS number: {nhs_number} loaded into test flow")
        return self
