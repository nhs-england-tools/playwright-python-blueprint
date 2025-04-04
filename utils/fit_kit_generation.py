from utils.oracle.oracle_specific_functions import get_kit_id_from_db
import pandas as pd
from datetime import datetime
import logging


def create_fit_id_df() -> pd.DataFrame:
    """
    The first step here is to get the relevant test data for compartment 2
    Then it calculates the check digit for each kit id retrieved
    Finally it adds the final part on the end (expiry date + random characters)
    """
    df = get_kit_id_from_db()
    df["fit_device_id"] = df["kitid"].apply(calculate_check_digit)
    df["fit_device_id"] = df["fit_device_id"].apply(convert_kit_id_to_fit_device_id)
    return df

def calculate_check_digit(kit_id: str) -> str:
    """
    This function used used to calculate the check digit of a kit ID
    It calculates the check digit by getting the sum of the location of each character in the kit id
    Then it divides the sum by 43 and gets the remainder from this
    It then searches the string "char_string" to find the index of the remainder
    The character found is then the check digit
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
    This is used to add the expiry date to the end of the Kit ID
    This by setting the month to december
    And the year is set to 1 year in the future.
    E.g. if the current date is 06/24 the expiry date will be set to 12/25
    """
    logging.info(f"Generating FIT Device ID from: {kit_id}")
    today = datetime.now()
    year = today.strftime("%y")  # Get the year from todays date in YY format
    return f"{kit_id}12{int(year) + 1}12345/KD00001"
