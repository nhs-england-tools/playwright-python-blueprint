import logging
from datetime import datetime
import pytest
from playwright.sync_api import Page
from pages.fit_test_kits.fit_test_kits_page import FITTestKits
from pages.base_page import BasePage
from pages.logout.log_out_page import Logout
from pages.fit_test_kits.log_devices_page import LogDevices
from utils.batch_processing import batch_processing
from utils.fit_kit_generation import create_fit_id_df
from utils.screening_subject_page_searcher import verify_subject_event_status_by_nhs_no
from utils.user_tools import UserTools
from utils.load_properties_file import PropertiesFile


@pytest.fixture
def smokescreen_properties() -> dict:
    return PropertiesFile().get_smokescreen_properties()


@pytest.mark.smoke
@pytest.mark.smokescreen
@pytest.mark.compartment2
def test_compartment_2(page: Page, smokescreen_properties: dict) -> None:
    """
    This is the main compartment 2 function. It covers the following:
    - Obtaining test data from the DB
    - Creating FIT Device IDs from the obtained test data
    - Logging FIT Devices
    - Logging FIT Devices as Spoilt
    - Processing the generated S3 batch
    """
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    BasePage(page).go_to_fit_test_kits_page()
    FITTestKits(page).go_to_log_devices_page()
    subjectdf = create_fit_id_df()

    for subject in range(int(smokescreen_properties["c2_normal_kits_to_log"])):
        fit_device_id = subjectdf["fit_device_id"].iloc[subject]
        logging.info(f"Logging FIT Device ID: {fit_device_id}")
        LogDevices(page).fill_fit_device_id_field(fit_device_id)
        sample_date = datetime.now().strftime("%#d %b %Y")
        logging.info("Setting sample date to today's date")
        LogDevices(page).fill_sample_date_field(sample_date)
        LogDevices(page).log_devices_title.get_by_text("Scan Device").wait_for()
        try:
            LogDevices(page).verify_successfully_logged_device_text()
            logging.info(f"{fit_device_id} Successfully logged")
        except Exception as e:
            pytest.fail(f"{fit_device_id} unsuccessfully logged: {str(e)}")

    nhs_no = subjectdf["subject_nhs_number"].iloc[0]
    try:
        verify_subject_event_status_by_nhs_no(
            page, nhs_no, "S43 - Kit Returned and Logged (Initial Test)"
        )
        logging.info(
            f"Successfully verified NHS number {nhs_no} with status S43 - Kit Returned and Logged (Initial Test)"
        )
    except Exception as e:
        pytest.fail(f"Verification failed for NHS number {nhs_no}: {str(e)}")

    BasePage(page).click_main_menu_link()
    BasePage(page).go_to_fit_test_kits_page()
    FITTestKits(page).go_to_log_devices_page()
    spoilt_fit_device_id = subjectdf["fit_device_id"].iloc[-1]
    logging.info(f"Logging Spoilt FIT Device ID: {spoilt_fit_device_id}")
    LogDevices(page).fill_fit_device_id_field(spoilt_fit_device_id)
    LogDevices(page).click_device_spoilt_button()
    LogDevices(page).select_spoilt_device_dropdown_option()
    LogDevices(page).click_log_as_spoilt_button()
    try:
        LogDevices(page).verify_successfully_logged_device_text()
        logging.info(f"{spoilt_fit_device_id} Successfully logged")
    except Exception as e:
        pytest.fail(f"{spoilt_fit_device_id} Unsuccessfully logged: {str(e)}")

    batch_processing(
        page, "S3", "Retest (Spoilt) (FIT)", "S11 - Retest Kit Sent (Spoilt)"
    )

    # Log out
    Logout(page).log_out()
