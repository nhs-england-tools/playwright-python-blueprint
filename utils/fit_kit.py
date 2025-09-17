from utils.oracle.oracle_specific_functions.kit_management import (
    get_kit_id_from_db,
    get_kit_id_logged_from_db,
    execute_fit_kit_stored_procedures,
)
from pages.base_page import BasePage
from pages.fit_test_kits.log_devices_page import LogDevicesPage
from pages.fit_test_kits.fit_test_kits_page import FITTestKitsPage
from datetime import datetime
import logging
import pandas as pd
import pytest
from utils.oracle.oracle import OracleDB
from decimal import Decimal
from classes.user.user_role_type import UserRoleType
from classes.repositories.analyser_repository import AnalyserRepository
from classes.repositories.user_repository import UserRepository
from classes.repositories.kit_service_management_repository import (
    KitServiceManagementRepository,
)
from classes.kits.kit_status import KitStatus


class FitKitGeneration:
    """
    This class is responsible for generating FIT Device IDs from test kit data.
    It is also used to retrieve a kit belonging to a subject
    """

    def create_fit_id_df(
        self,
        tk_type_id: int,
        hub_id: int,
        no_of_kits_to_retrieve: int,
    ) -> pd.DataFrame:
        """
        This function retrieves test kit data from the database for the specified compartment (using the 'get_kit_id_from_db' function from 'oracle_specific_functions.py').
        It then calculates a check digit for each retrieved kit ID and appends it to the kit ID.
        Finally, it generates a FIT Device ID by appending an expiry date and a fixed suffix to the kit ID.

        For example:
            Given the following inputs:
                tk_type_id = 1, hub_id = 101, no_of_kits_to_retrieve = 2
            The function retrieves two kit IDs from the database, e.g., ["ABC123", "DEF456"].
            It calculates the check digit for each kit ID, resulting in ["ABC123-K", "DEF456-M"].
            Then, it generates the FIT Device IDs, e.g., ["ABC123-K122512345/KD00001", "DEF456-M122512345/KD00001"].

        Args:
            tk_type_id (int): The type ID of the test kit.
            hub_id (int): The ID of the hub from which to retrieve the kits.
            no_of_kits_to_retrieve (int): The number of kits to retrieve from the database.

        Returns:
            pd.DataFrame: A DataFrame containing the processed kit IDs, including the calculated check digit
            and the final formatted FIT Device ID.
        """
        df = get_kit_id_from_db(tk_type_id, hub_id, no_of_kits_to_retrieve)
        df["fit_device_id"] = df["kitid"].apply(self.calculate_check_digit)
        df["fit_device_id"] = df["fit_device_id"].apply(
            self.convert_kit_id_to_fit_device_id
        )
        return df

    def calculate_check_digit(self, kit_id: str) -> str:
        """
        Calculates the check digit for a given kit ID.

        The check digit is determined by summing the positions of each character in the kit ID
        within a predefined character set. The remainder of the sum divided by 43 is used to
        find the corresponding character in the character set, which becomes the check digit.

        For example:
            Given the kit ID "ABC123", the positions of the characters in the predefined
            character set are summed. If the total is 123, the remainder when divided by 43
            is 37. The character at position 37 in the character set is "K". The resulting
            kit ID with the check digit appended would be "ABC123-K".

        Args:
            kit_id (str): The kit ID to calculate the check digit for.

        Returns:
            str: The kit ID with the calculated check digit appended.
        """
        logging.info(f"Calculating check digit for kit id: {kit_id}")
        total = 0
        char_string = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. $/+%"
        for i in range(len(kit_id)):
            total += char_string.index(kit_id[i - 1])
        check_digit = char_string[total % 43]
        return f"{kit_id}-{check_digit}"

    def convert_kit_id_to_fit_device_id(self, kit_id: str) -> str:
        """
        Converts a Kit ID into a FIT Device ID by appending an expiry date and a fixed suffix.

        The expiry date is calculated by setting the month to December and the year to one year
        in the future based on the current date. For example, if the current date is June 2024,
        the expiry date will be set to December 2025.

        Args:
            kit_id (str): The Kit ID to be converted.

        Returns:
            str: The generated FIT Device ID in the format "{kit_id}12{next_year}12345/KD00001".
        """
        logging.info(f"Generating FIT Device ID from: {kit_id}")
        today = datetime.now()
        year = today.strftime("%y")  # Get the year from todays date in YY format
        return f"{kit_id}12{int(year) + 1}12345/KD00001"

    def get_fit_kit_for_subject_sql(self, nhs_no: str, logged: bool, read: bool) -> str:
        """
        Constructs SQL for requesting the kit ID of the latest FIT kit for a subject.
        This then gets the subject's subject id from the DB and runs the query to return their FIT kit
        It then calculates the check digit and extra info to append at the end of the FIT Kit

        Args:
            nhs_no (str): The subject's NHS number.
            logged (bool): Whether to look for logged kits.
            read (bool): Whether to look for read kits.

        Returns:
            str: The FIT KIT belonging to the subject
        """

        sql_query = []
        sql_query.append(
            """
            SELECT kitid
            FROM tk_items_t
            WHERE tk_type_id > 1
            AND kitid = (
                SELECT MAX(tkx.kitid)
                FROM tk_items_t tkx
                LEFT OUTER JOIN kit_queue kq ON kq.device_id = tkx.device_id
                WHERE tkx.tk_type_id > 1
                AND tkx.screening_subject_id = :subject_id
            """
        )
        if logged:
            sql_query.append("    AND tkx.logged_in_flag = 'Y' ")
            if not read:
                sql_query.append("    AND kq.device_id IS NOT NULL ")
        else:
            sql_query.append(
                """
                AND tkx.logged_in_flag = 'N'
                AND kq.device_id IS NULL """
            )
        if read:
            sql_query.append("    AND tkx.reading_flag = 'Y' ")
        else:
            sql_query.append("    AND tkx.reading_flag = 'N' ")
        sql_query.append("    ) ")

        query = "\n".join(sql_query)
        subject_id = OracleDB().get_subject_id_from_nhs_number(nhs_no)
        params = {"subject_id": subject_id}
        fit_kits_df = OracleDB().execute_query(query, params)
        fit_kits_df["fit_device_id"] = fit_kits_df["kitid"].apply(
            self.calculate_check_digit
        )
        fit_kits_df["fit_device_id"] = fit_kits_df["fit_device_id"].apply(
            self.convert_kit_id_to_fit_device_id
        )
        return fit_kits_df["fit_device_id"].iloc[0]


class FitKitLogged:
    """This class is responsible for processing FIT Device IDs and logging them as normal or abnormal."""

    def process_kit_data(self, smokescreen_properties: dict) -> list:
        """
        This method retrieved the test data needed for compartment 3 and then splits it into two data frames:
        - 1 normal
        - 1 abnormal
        Once the dataframe is split in two it then creates two lists, one for normal and one for abnormal
        Each list will either have true or false appended depending on if it is normal or abnormal
        """
        # Get test data for compartment 3
        kit_id_df = get_kit_id_logged_from_db(smokescreen_properties)

        # Split dataframe into two different dataframes, normal and abnormal
        normal_fit_kit_df, abnormal_fit_kit_df = self.split_fit_kits(
            kit_id_df, smokescreen_properties
        )

        # Prepare a list to store device IDs and their respective flags
        device_ids = []

        # Process normal kits (only 1)
        if not normal_fit_kit_df.empty:
            device_id = normal_fit_kit_df["device_id"].iloc[0]
            logging.info(
                f"Processing normal kit with Device ID: {device_id}"
            )  # Logging normal device_id
            device_ids.append((device_id, True))  # Add to the list with normal flag
        else:
            pytest.fail("No normal kits found for processing.")

            # Process abnormal kits (multiple, loop through)
        if not abnormal_fit_kit_df.empty:
            for index, row in abnormal_fit_kit_df.iterrows():
                device_id = row["device_id"]
                logging.info(
                    f"Processing abnormal kit with Device ID: {device_id}"
                )  # Logging abnormal device_id
                device_ids.append(
                    (device_id, False)
                )  # Add to the list with abnormal flag
        else:
            pytest.fail("No abnormal kits found for processing.")

        return device_ids

    def split_fit_kits(
        self, kit_id_df: pd.DataFrame, smokescreen_properties: dict
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        This method splits the dataframe into two, 1 normal and 1 abnormal
        """
        number_of_normal = int(
            smokescreen_properties["c3_eng_number_of_normal_fit_kits"]
        )
        number_of_abnormal = int(
            smokescreen_properties["c3_eng_number_of_abnormal_fit_kits"]
        )

        # Split dataframe into two dataframes
        normal_fit_kit_df = kit_id_df.iloc[:number_of_normal]
        abnormal_fit_kit_df = kit_id_df.iloc[
            number_of_normal : number_of_normal + number_of_abnormal
        ]
        return normal_fit_kit_df, abnormal_fit_kit_df

    def read_latest_logged_kit(
        self, user: UserRoleType, kit_type: int, kit: str, kit_result: str
    ) -> None:
        """
        Reads the subject's latest logged FIT kit and updates its status/result.
        Args:
            user (UserRoleType): The user role type of the user making the request
            kit_type (int): The type of the kit being processed
            kit (str): The ID of the kit being processed
            kit_result (str): The result of the kit processing
        Raises:
            RuntimeError: If there is an error while reading the latest logged kit
        """
        logging.info("start: read_latest_logged_kit")

        try:
            user_repo = UserRepository()
            org_id = user_repo.get_org_id_for_role(user)
            analyser_repo = AnalyserRepository()
            analyser = analyser_repo.get_active_analyser_for_hub_and_kit_type(
                org_id, kit_type
            )
            assert (
                analyser is not None
            ), f"Can't find an active analyser for user's hub: {org_id}"

            # Set up kit result reading or code according to the input parameter
            result_reading = None
            result_code = None
            match kit_result:
                case "NORMAL":
                    result_reading = Decimal("7.5")
                case "ABNORMAL":
                    result_reading = Decimal("876.42")
                case "SPOILT":
                    if analyser.analyser_type_id is None:
                        raise RuntimeError(
                            "Analyser type ID is missing for SPOILT kit result."
                        )
                    result_code = analyser_repo.get_spoilt_result_code(
                        analyser.analyser_type_id
                    )
                case "TECHNICAL_FAILURE":
                    if analyser.analyser_type_id is None:
                        raise RuntimeError(
                            "Analyser type ID is missing for TECHNICAL_FAILURE kit result."
                        )
                    result_code = analyser_repo.get_technical_fail_result_code(
                        analyser.analyser_type_id
                    )
                case _:
                    logging.error("Error reading latest logged kit", exc_info=True)
                    raise RuntimeError(f"Invalid kit result value '{kit_result}'")

            kit_queue_repo = KitServiceManagementRepository()
            kit_queue_record = kit_queue_repo.get_service_management_by_device_id(kit)
            kit_queue_record.test_kit_status = KitStatus.BCSS_READY.value
            kit_queue_record.analyser_code = analyser.analyser_code
            kit_queue_record.date_time_authorised = datetime.now()
            kit_queue_record.authoriser_user_code = "AUTOTEST"
            kit_queue_record.test_result = result_reading
            kit_queue_record.error_code = result_code
            logging.debug(f"kit queue record: {kit_queue_record.__str__()}")
            kit_queue_repo.update_kit_service_management_record(kit_queue_record)

            # Immediately process the kit queue (don't wait for the scheduled DB job to kick in)
            execute_fit_kit_stored_procedures()

        except Exception as e:
            raise RuntimeError(f"Error occurred while reading latest logged kit: {e}")

        logging.info("exit: read_latest_logged_kit")

    def log_fit_kits(self, page, fit_kit: str, sample_date: datetime) -> None:
        """
        Navigates to the log devices page and logs FIT kits
        Args:
            fit_kit (str): The device id of the FIT kit
            sample_date (datetime): The date you want to select for the sample date field
        """
        BasePage(page).click_main_menu_link()
        BasePage(page).go_to_fit_test_kits_page()
        FITTestKitsPage(page).go_to_log_devices_page()
        logging.info(f"[FIT KITS] Logging FIT Device ID: {fit_kit}")
        LogDevicesPage(page).fill_fit_device_id_field(fit_kit)
        LogDevicesPage(page).fill_sample_date_field(sample_date)
        LogDevicesPage(page).log_devices_title.get_by_text("Scan Device").wait_for()
        try:
            LogDevicesPage(page).verify_successfully_logged_device_text()
            logging.info(f"[UI ASSERTIONS COMPLETE] {fit_kit} Successfully logged")
        except Exception as e:
            pytest.fail(
                f"[UI ASSERTIONS FAILED] {fit_kit} unsuccessfully logged: {str(e)}"
            )
