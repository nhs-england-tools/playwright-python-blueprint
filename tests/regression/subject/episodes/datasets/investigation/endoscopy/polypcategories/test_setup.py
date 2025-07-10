from datetime import datetime, timedelta
import pandas as pd
import pytest
from _pytest.fixtures import FixtureRequest
import logging
from playwright.sync_api import Page
from classes.subject import Subject
from classes.user import User
from pages.base_page import BasePage
from pages.datasets.colonoscopy_dataset_page import (
    ColonoscopyDatasetsPage,
    FitForColonoscopySspOptions,
)
from pages.datasets.subject_datasets_page import (
    SubjectDatasetsPage,
)
from pages.fit_test_kits.fit_test_kits_page import FITTestKitsPage
from pages.fit_test_kits.log_devices_page import LogDevicesPage
from pages.logout.log_out_page import LogoutPage
from pages.screening_practitioner_appointments.appointment_detail_page import (
    AppointmentDetailPage,
)
from pages.screening_practitioner_appointments.book_appointment_page import (
    BookAppointmentPage,
)
from pages.screening_practitioner_appointments.practitioner_availability_page import (
    PractitionerAvailabilityPage,
)
from pages.screening_practitioner_appointments.screening_practitioner_appointments_page import (
    ScreeningPractitionerAppointmentsPage,
)
from pages.screening_practitioner_appointments.set_availability_page import (
    SetAvailabilityPage,
)
from pages.screening_subject_search.advance_fobt_screening_episode_page import (
    AdvanceFOBTScreeningEpisodePage,
)
from pages.screening_subject_search.attend_diagnostic_test_page import (
    AttendDiagnosticTestPage,
)
from pages.screening_subject_search.episode_events_and_notes_page import (
    EpisodeEventsAndNotesPage,
)
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from utils.batch_processing import batch_processing
from utils.calendar_picker import CalendarPicker
from utils.fit_kit import FitKitGeneration
from utils.last_test_run import has_test_run_today
from utils.oracle.oracle import OracleDB
from utils.oracle.oracle_specific_functions import (
    update_kit_service_management_entity,
    execute_fit_kit_stored_procedures,
    set_org_parameter_value,
    get_org_parameter_value,
)
from utils.oracle.subject_selection_query_builder import SubjectSelectionQueryBuilder
from utils.screening_subject_page_searcher import (
    search_subject_episode_by_nhs_number,
    verify_subject_event_status_by_nhs_no,
)
from utils.user_tools import UserTools


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page, request: FixtureRequest) -> None:
    """
    Checks that the required organization parameters are set correctly before each test.
    If not, it sets them to the expected values.
    Also sets up appointments if the test has not been run today.
    """
    param_12_set_correctly = check_parameter(12, "23162", "10")
    param_28_set_correctly = check_parameter(28, "23162", "07:00")
    param_29_set_correctly = check_parameter(29, "23162", "20:00")
    if not param_12_set_correctly:
        set_org_parameter_value(12, "10", "23162")
    if not param_28_set_correctly:
        set_org_parameter_value(28, "07:00", "23162")
    if not param_29_set_correctly:
        set_org_parameter_value(29, "20:00", "23162")

    base_url = request.config.getoption("--base-url")
    if not has_test_run_today(
        "subject/episodes/datasets/investigation/endoscopy/polypcategories/test_setup", base_url  # type: ignore
    ):
        setup_appointments(page)


def test_setup_subjects_as_a99(page: Page, subjects_to_run_for: int) -> None:
    """
    Scenario Outline: Set up 10 subjects to be at status A99
    """
    page = page.context.new_page()
    page.goto("/")
    criteria = {
        "latest event status": "S9",
        "latest episode type": "FOBT",
        "subject has unprocessed sspi updates": "no",
        "subject has user dob updates": "no",
    }
    user = User()
    subject = Subject()

    builder = SubjectSelectionQueryBuilder()

    query, bind_vars = builder.build_subject_selection_query(
        criteria=criteria,
        user=user,
        subject=subject,
        subjects_to_retrieve=subjects_to_run_for,
    )

    df = OracleDB().execute_query(query, bind_vars)
    setup_a99_status(page, df)
    LogoutPage(page).log_out()


def test_setup_subjects_as_a259(page: Page, subjects_to_run_for: int) -> None:
    """
    Set up 10 subjects to have new Colonoscopy datasets in episodes started within in the last 4 years
    """
    page = page.context.new_page()
    page.goto("/")
    criteria = {
        "latest episode status": "open",
        "latest episode latest investigation dataset": "colonoscopy_new",
        "latest episode started": "less than 4 years ago",
    }
    user = User()
    subject = Subject()

    builder = SubjectSelectionQueryBuilder()

    query, bind_vars = builder.build_subject_selection_query(
        criteria=criteria,
        user=user,
        subject=subject,
        subjects_to_retrieve=subjects_to_run_for,
    )

    df = OracleDB().execute_query(query, bind_vars)

    if df.shape[0] == subjects_to_run_for:
        pytest.skip("Enough subjects found, no need to run test setup")

    criteria = {
        "latest event status": "S9",
        "latest episode type": "FOBT",
        "subject has unprocessed sspi updates": "no",
        "subject has user dob updates": "no",
    }
    user = User()
    subject = Subject()

    builder = SubjectSelectionQueryBuilder()

    query, bind_vars = builder.build_subject_selection_query(
        criteria=criteria,
        user=user,
        subject=subject,
        subjects_to_retrieve=subjects_to_run_for,
    )

    df = OracleDB().execute_query(query, bind_vars)
    df = setup_a99_status(page, df)

    for _, row in df.iterrows():
        nhs_no = row["nhs_number"]

        verify_subject_event_status_by_nhs_no(
            page, nhs_no, "A99 - Suitable for Endoscopic Test"
        )

        SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

        AdvanceFOBTScreeningEpisodePage(page).click_calendar_button()
        CalendarPicker(page).v1_calender_picker(datetime.today())

        AdvanceFOBTScreeningEpisodePage(page).select_test_type_dropdown_option(
            "Colonoscopy"
        )

        AdvanceFOBTScreeningEpisodePage(page).click_invite_for_diagnostic_test_button()
        AdvanceFOBTScreeningEpisodePage(page).verify_latest_event_status_value(
            "A59 - Invited for Diagnostic Test"
        )

        AdvanceFOBTScreeningEpisodePage(page).click_attend_diagnostic_test_button()

        AttendDiagnosticTestPage(page).select_actual_type_of_test_dropdown_option(
            "Colonoscopy"
        )
        AttendDiagnosticTestPage(page).click_calendar_button()
        CalendarPicker(page).v1_calender_picker(datetime.today())
        AttendDiagnosticTestPage(page).click_save_button()
        SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
            "A259 - Attended Diagnostic Test"
        )

    LogoutPage(page).log_out()


def check_parameter(param_id: int, org_id: str, expected_param_value: str) -> bool:
    """
    Check if the organization parameter is set correctly.
    Args:
        param_id (int): The ID of the parameter to check.
        org_id (str): The ID of the organization.
        expected_param_value (str): The expected value of the parameter.

    Returns:
        bool: True if the parameter is set correctly, False otherwise.
    """
    df = get_org_parameter_value(param_id, org_id)
    for _, row in df.iterrows():
        val_matches = str(row["val"]) == expected_param_value
        audit_reason_matches = row["audit_reason"] == "AUTOMATED TESTING - ADD"

        if val_matches and audit_reason_matches:
            logging.info(f"Parameter {param_id} is set correctly: {row['val']}")
            return True

    logging.warning(f"Parameter {param_id} is not set correctly, updating parameter.")
    return False


def setup_appointments(page: Page) -> None:
    """
    Set up appointments for multiple practitioners at a screening centre.
    This function logs in as a Screening Centre Manager, sets availability for
    practitioners, and creates appointments for the next 10 practitioners.
    """
    UserTools.user_login(page, "Screening Centre Manager at BCS001")
    for index in range(10):
        BasePage(page).go_to_screening_practitioner_appointments_page()
        ScreeningPractitionerAppointmentsPage(page).go_to_set_availability_page()
        SetAvailabilityPage(page).go_to_practitioner_availability_page()
        PractitionerAvailabilityPage(page).select_site_dropdown_option(
            "THE ROYAL HOSPITAL (WOLVERHAMPTON)"
        )
        PractitionerAvailabilityPage(
            page
        ).select_practitioner_dropdown_option_from_index(index + 1)
        PractitionerAvailabilityPage(page).click_calendar_button()
        CalendarPicker(page).select_day(datetime.today())
        PractitionerAvailabilityPage(page).click_show_button()
        PractitionerAvailabilityPage(page).enter_start_time("07:00")
        PractitionerAvailabilityPage(page).enter_end_time("20:00")
        PractitionerAvailabilityPage(page).click_calculate_slots_button()
        PractitionerAvailabilityPage(page).enter_number_of_weeks("1")
        PractitionerAvailabilityPage(page).click_save_button()
        BasePage(page).click_main_menu_link()
    LogoutPage(page).log_out()


def setup_a99_status(page: Page, df: pd.DataFrame) -> pd.DataFrame:
    """
    Set up subjects to have status A99 - Suitable for Endoscopic Test.

    Args:
        page (Page): The Playwright page object.
        df (pd.DataFrame): DataFrame containing subjects to set up.

    Returns:
        pd.DataFrame: DataFrame with updated subjects.
    """
    OracleDB().exec_bcss_timed_events(df)
    page.wait_for_timeout(5000)
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")
    csv_df = batch_processing(
        page,
        "S9",
        "Invitation & Test Kit (FIT)",
        "S10 - Invitation & Test Kit Sent",
        save_csv_as_df=True,
    )
    if csv_df is None:
        raise ValueError(
            "CSV DataFrame is None. Batch processing failed or returned no data."
        )
    kit_df = csv_df.iloc[:, [1, -2]].copy()
    kit_df.columns = ["nhs_number", "device_id"]
    kit_df["device_id"] = kit_df["device_id"].apply(
        FitKitGeneration().convert_kit_id_to_fit_device_id
    )

    for _, row in kit_df.iterrows():
        BasePage(page).click_main_menu_link()
        BasePage(page).go_to_fit_test_kits_page()
        FITTestKitsPage(page).go_to_log_devices_page()
        fit_device_id = row["device_id"]
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
        verify_subject_event_status_by_nhs_no(
            page,
            kit_df["nhs_number"].iloc[0],
            "S43 - Kit Returned and Logged (Initial Test)",
        )
    device_ids = []
    for _, row in kit_df.iterrows():
        device_id = row["device_id"]
        logging.info(f"Processing abnormal kit with Device ID: {device_id}")
        device_ids.append((device_id, False))

    nhs_nos = []
    normal_flags = []

    smokescreen_properties = {
        "c3_fit_kit_analyser_code": "UU2_tdH3",
        "c3_fit_kit_authorised_user": "AUTO1",
        "c3_fit_kit_normal_result": "75",
        "c3_fit_kit_abnormal_result": "150",
    }

    for device_id, is_normal in device_ids:
        nhs_no = update_kit_service_management_entity(
            device_id, is_normal, smokescreen_properties
        )
        nhs_nos.append(nhs_no)
        normal_flags.append(is_normal)

    try:
        execute_fit_kit_stored_procedures()
        logging.info("Stored procedures executed successfully.")
    except Exception as e:
        logging.error(f"Error executing stored procedures: {str(e)}")
        raise

    for nhs_no, is_normal in zip(nhs_nos, normal_flags):
        expected_status = (
            "S2 - Normal" if is_normal else "A8 - Abnormal"
        )  # S2 for normal, A8 for abnormal
        logging.info(
            f"Verifying NHS number: {nhs_no} with expected status: {expected_status}"
        )

        verify_subject_event_status_by_nhs_no(page, nhs_no, expected_status)

    for _, row in kit_df.iterrows():
        nhs_no = row["nhs_number"]
        BasePage(page).click_main_menu_link()
        BasePage(page).go_to_screening_subject_search_page()
        search_subject_episode_by_nhs_number(page, nhs_no)
        SubjectScreeningSummaryPage(page).click_book_practitioner_clinic_button()

        BookAppointmentPage(page).select_screening_centre_dropdown_option(
            "BCS001 - Wolverhampton Bowel Cancer Screening Centre"
        )
        BookAppointmentPage(page).select_site_dropdown_option(
            [
                "The Royal Hospital (Wolverhampton) (? km)",
                "The Royal Hospital (Wolverhampton) (? km) (attended)",
            ]
        )

        current_month_displayed = BookAppointmentPage(
            page
        ).get_current_month_displayed()
        CalendarPicker(page).book_first_eligible_appointment(
            current_month_displayed,
            BookAppointmentPage(page).appointment_cell_locators,
            [
                BookAppointmentPage(page).available_background_colour,
                BookAppointmentPage(page).some_available_background_colour,
            ],
        )
        BookAppointmentPage(page).appointments_table.click_first_input_in_column(
            "Appt/Slot Time"
        )
        BasePage(page).safe_accept_dialog(BookAppointmentPage(page).save_button)
        BookAppointmentPage(page).appointment_booked_confirmation_is_displayed(
            "Appointment booked"
        )

        verify_subject_event_status_by_nhs_no(
            page, nhs_no, "	A183 - 1st Colonoscopy Assessment Appointment Requested"
        )

    batch_processing(
        page,
        "A183",
        "Practitioner Clinic 1st Appointment",
        "A25 - 1st Colonoscopy Assessment Appointment Booked, letter sent",
    )

    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Screening Centre Manager at BCS001")

    for _, row in kit_df.iterrows():
        BasePage(page).click_main_menu_link()
        BasePage(page).go_to_screening_subject_search_page()
        nhs_no = row["nhs_number"]
        search_subject_episode_by_nhs_number(page, nhs_no)
        SubjectScreeningSummaryPage(page).expand_episodes_list()
        SubjectScreeningSummaryPage(page).click_first_fobt_episode_link()
        EpisodeEventsAndNotesPage(page).click_view_appointment_link()
        AppointmentDetailPage(page).wait_for_attendance_radio(
            600000
        )  # Max of 10 minute wait as appointments need to be set for future times and they are in 10 minute intervals
        AppointmentDetailPage(page).check_attendance_radio()
        AppointmentDetailPage(page).check_attended_check_box()
        AppointmentDetailPage(page).click_calendar_button()
        CalendarPicker(page).v1_calender_picker(datetime.today() - timedelta(1))
        AppointmentDetailPage(page).click_save_button()
        AppointmentDetailPage(page).verify_text_visible("Record updated")
        logging.info(
            f"Subject attended appointment - Record successfully updated for: {nhs_no}"
        )
        BasePage(page).click_back_button()
        BasePage(page).click_back_button()
        SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
            "J10 - Attended Colonoscopy Assessment Appointment"
        )

    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    batch_processing(
        page,
        "A183",
        "GP Result (Abnormal)",
        "J10 - Attended Colonoscopy Assessment Appointment",
    )
    SubjectScreeningSummaryPage(page).expand_episodes_list()
    SubjectScreeningSummaryPage(page).click_first_fobt_episode_link()
    EpisodeEventsAndNotesPage(page).expected_episode_event_is_displayed(
        "A167 - GP Abnormal FOBT Result Sent"
    )

    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Screening Centre Manager at BCS001")

    for _, row in kit_df.iterrows():
        nhs_no = row["nhs_number"]

        verify_subject_event_status_by_nhs_no(
            page, nhs_no, "J10 - Attended Colonoscopy Assessment Appointment"
        )

        SubjectScreeningSummaryPage(page).click_datasets_link()
        SubjectDatasetsPage(page).click_colonoscopy_show_datasets()

        ColonoscopyDatasetsPage(page).select_fit_for_colonoscopy_option(
            FitForColonoscopySspOptions.YES.value
        )
        ColonoscopyDatasetsPage(page).click_dataset_complete_radio_button_yes()
        ColonoscopyDatasetsPage(page).save_dataset()
        BasePage(page).click_back_button()
        BasePage(page).click_back_button()

        SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
        AdvanceFOBTScreeningEpisodePage(
            page
        ).click_suitable_for_endoscopic_test_button()

        AdvanceFOBTScreeningEpisodePage(page).verify_latest_event_status_value(
            "A99 - Suitable for Endoscopic Test"
        )
    return kit_df
