import pytest
from playwright.sync_api import Page, expect
from pages.logout.log_out_page import Logout
from pages.base_page import BasePage
from pages.screening_practitioner_appointments.screening_practitioner_appointments import (
    ScreeningPractitionerAppointmentsPage,
)
from pages.screening_subject_search.subject_screening_summary import (
    SubjectScreeningSummary,
)
from pages.screening_practitioner_appointments.screening_practitioner_day_view import (
    ScreeningPractitionerDayView,
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
    page.locator("#UI_APPOINTMENT_TYPE").select_option(label="Colonoscopy Assessment")
    page.locator("#UI_SCREENING_CENTRE").select_option(
        label="BCS001 - Wolverhampton Bowel Cancer Screening Centre"
    )
    page.locator("#UI_SITE").select_option(label="The Royal Hospital (Wolverhampton)")

    page.get_by_role("button", name="View appointments on this day").click()
    ScreeningPractitionerDayView(page).click_calendar_button()
    date_from_util = datetime(2025, 4, 29)
    CalendarPicker(page).v1_calender_picker(date_from_util)

    # Select subject from inital test data util
    ScreeningPractitionerDayView(page).click_patient_link("STARLESS BLUSH")

    # Select Attendance radio button, tick Attended checkbox, set Attended Date to yesterday's (system) date and then press Save
    page.get_by_role("radio", name="Attendance").check()
    page.locator("#UI_ATTENDED").check()
    page.get_by_role("button", name="Calendar").click()
    CalendarPicker(page).v1_calender_picker(datetime.today() - timedelta(1))
    page.get_by_role("button", name="Save").click()
    expect(page.get_by_text("Record updated")).to_be_visible()

    # Repeat for x Abnormal  patients

    # Navigate to the 'Subject Screening Summary' screen for the 1st Abnormal patient
    nhs_no = "9937265193"  # Test NHS NO for Scaliding Cod
    verify_subject_event_status_by_nhs_no(
        page, nhs_no, "J10 - Attended Colonoscopy Assessment Appointment"
    )

    # Click on 'Datasets' link
    SubjectScreeningSummary(page).click_datasets_link()

    # Click on 'Show Dataset' next to the Colonoscopy Assessment

    # Populate Colonoscopy Assessment Details fields

    # ASA Grade  - I - Fit
    # Fit for Colonoscopy (SSP) - Yes

    # Click 'Yes' for Dataset Complete?
    # Click Save Dataset button
    # Click Back
    page.get_by_role("link", name="Show Dataset").click()
    page.get_by_label("ASA Grade").select_option("17009")
    page.get_by_label("Fit for Colonoscopy (SSP)").select_option("17058")
    page.get_by_role("radio", name="Yes").check()
    page.locator("#UI_DIV_BUTTON_SAVE1").get_by_role(
        "button", name="Save Dataset"
    ).click()
    BasePage(page).click_back_button()
    BasePage(page).click_back_button()
    # This brings you back to the subject screening summary page

    # On the Subject Screening Summary click on the 'Advance FOBT Screening Episode' button and then click on the 'Suitable for Endoscopic Test' button
    # Click OK after message
    SubjectScreeningSummary(page).click_advance_fobt_screening_episode_button()
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Suitable for Endoscopic Test").click()

    # Enter a 'First Offered Appointment Date' (enter a date after the attended appt)
    page.get_by_role("button", name="Calendar").click()
    CalendarPicker(page).v1_calender_picker(datetime.today())

    # Select 'Colonoscopy' from the 'Type of Test' from the drop down list
    page.locator("#UI_EXT_TEST_TYPE_2233").select_option(label="Colonoscopy")

    # Click the 'Invite for Diagnostic Test >>' button
    # Click 'OK'
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Invite for Diagnostic Test >>").click()
    SubjectScreeningSummary(page).verify_latest_event_status_value(
        "A59 - Invited for Diagnostic Test"
    )

    # Click 'Attend Diagnostic Test' button
    page.get_by_role("button", name="Attend Diagnostic Test").click()

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
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Other Post-investigation").click()
    expect(
        page.get_by_role(
            "cell", name="A361 - Other Post-investigation Contact Required", exact=True
        )
    ).to_be_visible()

    # Select 'Record other post-investigation contact' button
    page.get_by_role("button", name="Record other post-").click()

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
