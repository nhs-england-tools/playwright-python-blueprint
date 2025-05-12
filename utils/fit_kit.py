from oracle.oracle_specific_functions import get_kit_id_logged_from_db
from utils.oracle.oracle_specific_functions import get_kit_id_from_db
from pages.base_page import BasePage
from datetime import datetime
import logging
import pandas as pd
import pytest


class FitKitGeneration:
    """This class is responsible for generating FIT Device IDs from test kit data."""

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
    ) -> pd.DataFrame:
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
