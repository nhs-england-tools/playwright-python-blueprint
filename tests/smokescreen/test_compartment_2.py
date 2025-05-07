import logging
from datetime import datetime
import pytest
from playwright.sync_api import Page
from pages.fit_test_kits.fit_test_kits_page import FITTestKitsPage
from pages.base_page import BasePage
from pages.logout.log_out_page import LogoutPage
from pages.fit_test_kits.log_devices_page import LogDevicesPage
from utils.batch_processing import batch_processing
from utils.fit_kit_generation import create_fit_id_df
from utils.screening_subject_page_searcher import verify_subject_event_status_by_nhs_no
from utils.user_tools import UserTools


@pytest.mark.vpn_required
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
    FITTestKitsPage(page).go_to_log_devices_page()

    tk_type_id = smokescreen_properties["c2_fit_kit_tk_type_id"]
    hub_id = smokescreen_properties["c2_fit_kit_logging_test_org_id"]
    no_of_kits_to_retrieve = smokescreen_properties["c2_total_fit_kits_to_retieve"]
    subjectdf = create_fit_id_df(tk_type_id, hub_id, no_of_kits_to_retrieve)

    for subject in range(int(smokescreen_properties["c2_normal_kits_to_log"])):
        fit_device_id = subjectdf["fit_device_id"].iloc[subject]
        logging.info(f"Logging FIT Device ID: {fit_device_id}")
        LogDevicesPage(page).fill_fit_device_id_field(fit_device_id)
        sample_date = datetime.now()
        logging.info("Setting sample date to today's date")
        LogDevicesPage(page).fill_sample_date_field(sample_date)
        LogDevicesPage(page).log_devices_title.get_by_text("Scan Device").wait_for()
        try:
            LogDevicesPage(page).verify_successfully_logged_device_text()
            logging.info(f"{fit_device_id} Successfully logged")
        except Exception as e:
            pytest.fail(f"{fit_device_id} unsuccessfully logged: {str(e)}")

    nhs_no = subjectdf["subject_nhs_number"].iloc[0]
    verify_subject_event_status_by_nhs_no(
        page, nhs_no, "S43 - Kit Returned and Logged (Initial Test)"
    )

    BasePage(page).click_main_menu_link()
    BasePage(page).go_to_fit_test_kits_page()
    FITTestKitsPage(page).go_to_log_devices_page()
    spoilt_fit_device_id = subjectdf["fit_device_id"].iloc[-1]
    logging.info(f"Logging Spoilt FIT Device ID: {spoilt_fit_device_id}")
    LogDevicesPage(page).fill_fit_device_id_field(spoilt_fit_device_id)
    LogDevicesPage(page).click_device_spoilt_button()
    LogDevicesPage(page).select_spoilt_device_dropdown_option()
    LogDevicesPage(page).click_log_as_spoilt_button()
    try:
        LogDevicesPage(page).verify_successfully_logged_device_text()
        logging.info(f"{spoilt_fit_device_id} Successfully logged")
    except Exception as e:
        pytest.fail(f"{spoilt_fit_device_id} Unsuccessfully logged: {str(e)}")

    batch_processing(
        page, "S3", "Retest (Spoilt) (FIT)", "S11 - Retest Kit Sent (Spoilt)"
    )

    # Log out
    LogoutPage(page).log_out()
