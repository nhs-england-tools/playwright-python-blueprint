import pytest
from playwright.sync_api import Page, expect
from pages.logout.log_out_page import Logout
from pages.base_page import BasePage
from pages.screening_practitioner_appointments.screening_practitioner_appointments import (
    ScreeningPractitionerAppointmentsPage,
)
from pages.screening_practitioner_appointments.subject_datasets import (
    SubjectDatasets,
    FitForColonoscopySspOptions,
    AsaGradeOptions,
)
from pages.screening_subject_search.subject_screening_summary import (
    SubjectScreeningSummary,
)
from pages.screening_subject_search.advance_fobt_screening_episode_page import (
    AdvanceFOBTScreeningEpisode,
)
from pages.screening_practitioner_appointments.screening_practitioner_day_view import (
    ScreeningPractitionerDayView,
)
from pages.screening_practitioner_appointments.appointment_detail_page import (
    AppointmentDetail,
)
from pages.screening_practitioner_appointments.appointment_calendar_page import (
    AppointmentCalendar,
)
from utils.user_tools import UserTools
from utils.load_properties_file import PropertiesFile
from utils.screening_subject_page_searcher import verify_subject_event_status_by_nhs_no
from utils.calendar_picker import CalendarPicker
from datetime import datetime, timedelta


@pytest.fixture
def smokescreen_properties() -> dict:
    return PropertiesFile().get_smokescreen_properties()


@pytest.mark.vpn_required
@pytest.mark.smokescreen
@pytest.mark.compartment5
def test_compartment_5(page: Page, smokescreen_properties: dict) -> None:
    """
    This is the main compartment 5 method
    It involves marking the attendance of subjects to their screening practitioner appointments
    Then it invites them for colonoscopy
    Then it marks post investigation appointment as not required
    """

    # --------------
    # Attendance of Screening
    # Practitioner Clinic Appointment
    # --------------

    # Log in as a Screening Centre user
    UserTools.user_login(page, "Screening Centre Manager at BCS001")

    # From the Main Menu, choose the 'Screening Practitioner Appointments' and then 'View Appointments' option
    BasePage(page).go_to_screening_practitioner_appointments_page()
    ScreeningPractitionerAppointmentsPage(page).go_to_view_appointments_page()

    # Select the Appointment Type, Site, Screening Practitioner and required date of the appointment and click 'View appointments on this day' button
    AppointmentCalendar(page).select_appointment_type_dropdown(
        smokescreen_properties["c5_eng_appointment_type"]
    )
    AppointmentCalendar(page).select_screening_centre_dropdown(
        smokescreen_properties["c5_eng_screening_centre"]
    )
    AppointmentCalendar(page).select_site_dropdown(
        smokescreen_properties["c5_eng_site"]
    )

    AppointmentCalendar(page).click_view_appointments_on_this_day_button()
    ScreeningPractitionerDayView(page).click_calendar_button()
    date_from_util = datetime(2025, 4, 29)
    CalendarPicker(page).v1_calender_picker(date_from_util)

    # Select subject from inital test data util
    ScreeningPractitionerDayView(page).click_patient_link("STARLESS BLUSH")

    # Select Attendance radio button, tick Attended checkbox, set Attended Date to yesterday's (system) date and then press Save
    AppointmentDetail(page).check_attendance_radio()
    AppointmentDetail(page).check_attendented_check_box()
    AppointmentDetail(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today() - timedelta(1))
    AppointmentDetail(page).click_save_button()
    AppointmentDetail(page).verify_text_visible("Record updated")

    # Repeat for x Abnormal  patients

    # Navigate to the 'Subject Screening Summary' screen for the 1st Abnormal patient
    nhs_no = "9937265193"  # Test NHS NO for Scaliding Cod
    verify_subject_event_status_by_nhs_no(
        page, nhs_no, "J10 - Attended Colonoscopy Assessment Appointment"
    )

    # Click on 'Datasets' link
    SubjectScreeningSummary(page).click_datasets_link()

    # Click on 'Show Dataset' next to the Colonoscopy Assessment
    SubjectDatasets(page).click_show_datasets()

    # Populate Colonoscopy Assessment Details fields

    # ASA Grade  - I - Fit
    SubjectDatasets(page).select_asa_grade_option(AsaGradeOptions.FIT.value)

    # Fit for Colonoscopy (SSP) - Yes
    SubjectDatasets(page).select_fit_for_colonoscopy_option(
        FitForColonoscopySspOptions.YES.value
    )

    # Click 'Yes' for Dataset Complete?
    SubjectDatasets(page).click_dataset_complete_radio_button_yes()

    # Click Save Dataset button
    SubjectDatasets(page).save_dataset()

    # Click Back
    BasePage(page).click_back_button()
    BasePage(page).click_back_button()
    # This brings you back to the subject screening summary page

    # On the Subject Screening Summary click on the 'Advance FOBT Screening Episode' button and then click on the 'Suitable for Endoscopic Test' button
    # Click OK after message
    SubjectScreeningSummary(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisode(page).click_suitable_for_endoscopic_test_button()

    # Enter a 'First Offered Appointment Date' (enter a date after the attended appt)
    AdvanceFOBTScreeningEpisode(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())

    # Select 'Colonoscopy' from the 'Type of Test' from the drop down list
    AdvanceFOBTScreeningEpisode(page).select_test_type_dropdown_option("Colonoscopy")

    # Click the 'Invite for Diagnostic Test >>' button
    # Click 'OK'
    AdvanceFOBTScreeningEpisode(page).click_invite_for_diagnostic_test_button()
    SubjectScreeningSummary(page).verify_latest_event_status_value(
        "A59 - Invited for Diagnostic Test"
    )

    # Click 'Attend Diagnostic Test' button
    AdvanceFOBTScreeningEpisode(page).click_attend_diagnostic_test_button()

    # Select Colonoscopy from drop down list. Enter the actual appointment date as today's date and select 'Save'
    page.locator("#UI_CONFIRMED_TYPE_OF_TEST").select_option(label="Colonoscopy")
    page.get_by_role("button", name="Calendar").click()
    CalendarPicker(page).v1_calender_picker(datetime.today())
    page.get_by_role("button", name="Save").click()
    SubjectScreeningSummary(page).verify_latest_event_status_value(
        "A259 - Attended Diagnostic Test"
    )
    # Repeat above for x number of subjects

    # Click on 'Advance FOBT Screening Episode' button for the 1st Abnormal patient
    verify_subject_event_status_by_nhs_no(
        page, nhs_no, "A259 - Attended Diagnostic Test"
    )
    SubjectScreeningSummary(page).click_advance_fobt_screening_episode_button()

    # Click 'Other Post-investigation Contact Required' button
    # Click 'OK'
    AdvanceFOBTScreeningEpisode(page).click_other_post_investigation_button()
    AdvanceFOBTScreeningEpisode(page).verify_latest_event_status_value(
        "A361 - Other Post-investigation Contact Required"
    )

    # Select 'Record other post-investigation contact' button
    AdvanceFOBTScreeningEpisode(
        page
    ).click_record_other_post_investigation_contact_button()

    # Complete 'Contact Direction',   To patient
    # 'Contact made between patient and',  Selects the top option in the dropdown
    # 'Date of Patient Contact',  Today
    # 'Duration',  01:00
    # 'Start Time',  11:00
    # 'End Time',  12:00
    # 'Discussion Record'   TEST AUTOMATION
    # select 'Outcome' - 'Post-investigation Appointment Not Required' and click 'Save'
    page.locator("#UI_DIRECTION").select_option(label="To patient")
    page.locator("#UI_CALLER_ID").select_option(index=0)
    page.get_by_role("button", name="Calendar").click()
    CalendarPicker(page).v1_calender_picker(datetime.today())
    page.locator("#UI_START_TIME").click()
    page.locator("#UI_START_TIME").fill("11:00")
    page.locator("#UI_END_TIME").click()
    page.locator("#UI_END_TIME").fill("12:00")
    page.locator("#UI_COMMENT_ID").click()
    page.locator("#UI_COMMENT_ID").fill("Test Automation")
    page.locator("#UI_OUTCOME").select_option(
        label="Post-investigation Appointment Not Required"
    )
    page.get_by_role("button", name="Save").click()

    verify_subject_event_status_by_nhs_no(
        page, nhs_no, "A361 - Other Post-investigation Contact Required"
    )

    # Repeat above for x subjects

    Logout(page).log_out()
