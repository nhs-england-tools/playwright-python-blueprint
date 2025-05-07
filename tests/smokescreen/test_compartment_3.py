import logging
import pytest
from playwright.sync_api import Page
from pages.logout.log_out_page import LogoutPage
from utils.batch_processing import batch_processing
from utils.fit_kit_logged import process_kit_data
from utils.screening_subject_page_searcher import verify_subject_event_status_by_nhs_no
from utils.oracle.oracle_specific_functions import (
    update_kit_service_management_entity,
    execute_fit_kit_stored_procedures,
)
from utils.user_tools import UserTools
from utils.load_properties_file import PropertiesFile


@pytest.fixture
def smokescreen_properties() -> dict:
    return PropertiesFile().get_smokescreen_properties()


@pytest.mark.vpn_required
@pytest.mark.smokescreen
@pytest.mark.compartment3
def test_compartment_3(page: Page, smokescreen_properties: dict) -> None:
    """
    This is the main compartment 3 method
    First it finds any relevant test data from the DB and stores it in a pandas dataframe
    Then it separates it out into normal and abnormal results
    Once that is done it updates a table on the DB and runs two stored procedures so that these subjects will not have normal/abnormal results on BCSS
    It then checks that the status of the subject is as expected using the subject screening summary page
    Then it process two batches performing checks on the subjects to ensure they always have the correct event status
    """
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    # Find data , separate it into normal and abnormal, Add results to the test records in the KIT_QUEUE table (i.e. mimic receiving results from the middleware)
    # and get device IDs and their flags
    device_ids = process_kit_data(smokescreen_properties)
    # Retrieve NHS numbers for each device_id and determine normal/abnormal status
    nhs_numbers = []
    normal_flags = []

    for device_id, is_normal in device_ids:
        nhs_number = update_kit_service_management_entity(
            device_id, is_normal, smokescreen_properties
        )
        nhs_numbers.append(nhs_number)
        normal_flags.append(
            is_normal
        )  # Store the flag (True for normal, False for abnormal)

    # Run two stored procedures to process any kit queue records at status BCSS_READY
    try:
        execute_fit_kit_stored_procedures()
        logging.info("Stored procedures executed successfully.")
    except Exception as e:
        logging.error(f"Error executing stored procedures: {str(e)}")
        raise

    # Check the results of the processed FIT kits have correctly updated the status of the associated subjects
    # Verify subject event status based on normal or abnormal classification
    for nhs_number, is_normal in zip(nhs_numbers, normal_flags):
        expected_status = (
            "S2 - Normal" if is_normal else "A8 - Abnormal"
        )  # S2 for normal, A8 for abnormal
        logging.info(
            f"Verifying NHS number: {nhs_number} with expected status: {expected_status}"
        )

        verify_subject_event_status_by_nhs_no(page, nhs_number, expected_status)

    # Process S2 batch
    batch_processing(
        page,
        "S2",
        "Subject Result (Normal)",
        "S158 - Subject Discharge Sent (Normal)",
        True,
    )

    # Process S158 batch
    batch_processing(
        page,
        "S158",
        "GP Result (Normal)",
        "S159 - GP Discharge Sent (Normal)",
    )

    # Log out
    LogoutPage(page).log_out()
