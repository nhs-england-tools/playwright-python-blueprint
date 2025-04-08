from oracle.oracle import OracleDB
from oracle.oracle_specific_functions import get_kit_id_logged_from_db
import pandas as pd
import logging
import pytest


def process_kit_data(smokescreen_properties: dict) -> list:
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
    normal_fit_kit_df, abnormal_fit_kit_df = split_fit_kits(
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
            device_ids.append((device_id, False))  # Add to the list with abnormal flag
    else:
        pytest.fail("No abnormal kits found for processing.")

    return device_ids


def split_fit_kits(kit_id_df: pd.DataFrame, smokescreen_properties: dict) -> pd.DataFrame:
    """
    This method splits the dataframe into two, 1 normal and 1 abnormal
    """
    number_of_normal = int(smokescreen_properties["c3_eng_number_of_normal_fit_kits"])
    number_of_abnormal = int(
        smokescreen_properties["c3_eng_number_of_abnormal_fit_kits"]
    )

    # Split dataframe into two dataframes
    normal_fit_kit_df = kit_id_df.iloc[:number_of_normal]
    abnormal_fit_kit_df = kit_id_df.iloc[
        number_of_normal : number_of_normal + number_of_abnormal
    ]
    return normal_fit_kit_df, abnormal_fit_kit_df
