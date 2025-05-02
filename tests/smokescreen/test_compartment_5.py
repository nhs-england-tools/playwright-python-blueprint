import pytest
from playwright.sync_api import Page
from pages.logout.log_out_page import LogoutPage
from pages.base_page import BasePage
from pages.screening_practitioner_appointments.appointment_calendar_page import (
    AppointmentCalendarPage,
)
from pages.screening_practitioner_appointments.appointment_detail_page import (
    AppointmentDetailPage,
)
from pages.screening_practitioner_appointments.screening_practitioner_appointments_page import (
    ScreeningPractitionerAppointmentsPage,
)
from pages.screening_practitioner_appointments.screening_practitioner_day_view_page import (
    ScreeningPractitionerDayViewPage,
)
from pages.datasets.subject_datasets_page import (
    SubjectDatasetsPage,
)
from pages.datasets.colonoscopy_dataset_page import (
    ColonoscopyDatasetsPage,
    FitForColonoscopySspOptions,
    AsaGradeOptions,
)
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from pages.screening_subject_search.advance_fobt_screening_episode_page import (
    AdvanceFOBTScreeningEpisodePage,
)
from pages.screening_practitioner_appointments.screening_practitioner_day_view_page import (
    ScreeningPractitionerDayViewPage,
)
from pages.screening_practitioner_appointments.appointment_detail_page import (
    AppointmentDetailPage,
)
from pages.screening_practitioner_appointments.appointment_calendar_page import (
    AppointmentCalendarPage,
)
from pages.screening_subject_search.attend_diagnostic_test_page import (
    AttendDiagnosticTestPage,
)
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)

from pages.screening_subject_search.contact_with_patient_page import (
    ContactWithPatientPage,
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
    AppointmentCalendarPage(page).select_appointment_type_dropdown(
        smokescreen_properties["c5_eng_appointment_type"]
    )
    AppointmentCalendarPage(page).select_screening_centre_dropdown(
        smokescreen_properties["c5_eng_screening_centre"]
    )
    AppointmentCalendarPage(page).select_site_dropdown(
        smokescreen_properties["c5_eng_site"]
    )
    # page.get_by_role("link", name="Screening Practitioner").select_option("")

    AppointmentCalendarPage(page).click_view_appointments_on_this_day_button()
    ScreeningPractitionerDayViewPage(page).click_calendar_button()
    date_from_util = datetime(2025, 4, 30)
    CalendarPicker(page).v1_calender_picker(date_from_util)
    # page.locator("#UI_PRACTITIONER_NDV").select_option("")

    # Select subject from inital test data util
    ScreeningPractitionerDayViewPage(page).click_patient_link("DIVIDEND MUZZLE")

    # Select Attendance radio button, tick Attended checkbox, set Attended Date to yesterday's (system) date and then press Save
    AppointmentDetailPage(page).check_attendance_radio()
    AppointmentDetailPage(page).check_attended_check_box()
    AppointmentDetailPage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today() - timedelta(1))
    AppointmentDetailPage(page).click_save_button()
    AppointmentDetailPage(page).verify_text_visible("Record updated")

    # Repeat for x Abnormal  patients

    # Navigate to the 'Subject Screening Summary' screen for the 1st Abnormal patient
    nhs_no = "9645516129"  # Test NHS NO for DIVIDEND MUZZLE
    verify_subject_event_status_by_nhs_no(
        page, nhs_no, "J10 - Attended Colonoscopy Assessment Appointment"
    )

    # Click on 'Datasets' link
    SubjectScreeningSummaryPage(page).click_datasets_link()

    # Click on 'Show Dataset' next to the Colonoscopy Assessment
    SubjectDatasetsPage(page).click_colonoscopy_show_datasets()

    # Populate Colonoscopy Assessment Details fields

    # ASA Grade  - I - Fit
    ColonoscopyDatasetsPage(page).select_asa_grade_option(AsaGradeOptions.FIT.value)

    # Fit for Colonoscopy (SSP) - Yes
    ColonoscopyDatasetsPage(page).select_fit_for_colonoscopy_option(
        FitForColonoscopySspOptions.YES.value
    )

    # Click 'Yes' for Dataset Complete?
    ColonoscopyDatasetsPage(page).click_dataset_complete_radio_button_yes()

    # Click Save Dataset button
    ColonoscopyDatasetsPage(page).save_dataset()

    # Click Back
    BasePage(page).click_back_button()
    BasePage(page).click_back_button()
    # This brings you back to the subject screening summary page

    # On the Subject Screening Summary click on the 'Advance FOBT Screening Episode' button and then click on the 'Suitable for Endoscopic Test' button
    # Click OK after message
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_suitable_for_endoscopic_test_button()

    # Enter a 'First Offered Appointment Date' (enter a date after the attended appt)
    AdvanceFOBTScreeningEpisodePage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())

    # Select 'Colonoscopy' from the 'Type of Test' from the drop down list
    AdvanceFOBTScreeningEpisodePage(page).select_test_type_dropdown_option(
        "Colonoscopy"
    )

    # Click the 'Invite for Diagnostic Test >>' button
    # Click 'OK'
    AdvanceFOBTScreeningEpisodePage(page).click_invite_for_diagnostic_test_button()
    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A59 - Invited for Diagnostic Test"
    )

    # Click 'Attend Diagnostic Test' button
    AdvanceFOBTScreeningEpisodePage(page).click_attend_diagnostic_test_button()

    # Select Colonoscopy from drop down list. Enter the actual appointment date as today's date and select 'Save'
    AttendDiagnosticTestPage.select_actual_type_of_test_dropdown_option("Colonoscopy")
    AttendDiagnosticTestPage.click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())
    AttendDiagnosticTestPage.click_save_button()
    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A259 - Attended Diagnostic Test"
    )
    # Repeat above for x number of subjects

    # Click on 'Advance FOBT Screening Episode' button for the 1st Abnormal patient
    verify_subject_event_status_by_nhs_no(
        page, nhs_no, "A259 - Attended Diagnostic Test"
    )
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # Click 'Other Post-investigation Contact Required' button
    # Click 'OK'
    AdvanceFOBTScreeningEpisodePage(page).click_other_post_investigation_button()
    AdvanceFOBTScreeningEpisodePage(page).verify_latest_event_status_value(
        "A361 - Other Post-investigation Contact Required"
    )

    # Select 'Record other post-investigation contact' button
    AdvanceFOBTScreeningEpisodePage(
        page
    ).click_record_other_post_investigation_contact_button()

    ContactWithPatientPage(page).select_direction_dropdown_option("To patient")
    ContactWithPatientPage(page).select_caller_id_dropdown_index_option(1)
    ContactWithPatientPage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())
    ContactWithPatientPage(page).enter_start_time("11:00")
    ContactWithPatientPage(page).enter_end_time("12:00")
    ContactWithPatientPage(page).enter_discussion_record_text("Test Automation")
    ContactWithPatientPage(page).select_outcome_dropdown_option(
        "Post-investigation Appointment Not Required"
    )
    ContactWithPatientPage(page).click_save_button()

    verify_subject_event_status_by_nhs_no(
        page, nhs_no, "A323 - Post-investigation Appointment NOT Required"
    )

    # Repeat above for x subjects

    LogoutPage(page).log_out()
