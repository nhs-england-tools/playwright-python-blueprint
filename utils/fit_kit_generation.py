from utils.oracle.oracle_specific_functions import get_kit_id_from_db
import pandas as pd
from datetime import datetime
import logging


def create_fit_id_df(
    tk_type_id: int, hub_id: int, no_of_kits_to_retrieve: int
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
    df["fit_device_id"] = df["kitid"].apply(calculate_check_digit)
    df["fit_device_id"] = df["fit_device_id"].apply(convert_kit_id_to_fit_device_id)
    return df


def calculate_check_digit(kit_id: str) -> str:
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


def convert_kit_id_to_fit_device_id(kit_id: str) -> str:
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
