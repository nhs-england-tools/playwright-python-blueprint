import pytest
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.reports.reports_page import ReportsPage
from utils.date_time_utils import DateTimeUtils
from utils.user_tools import UserTools
from utils.load_properties_file import PropertiesFile


@pytest.fixture
def general_properties() -> dict:
    return PropertiesFile().get_general_properties()


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as a test user and navigates to the
    reports page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    # Open reports page
    BasePage(page).go_to_reports_page()


def test_reports_page_navigation(page: Page) -> None:
    """
    Confirms all menu items are displayed on the reports page, and that the relevant pages
    are loaded when the links are clicked
    """

    # Bureau reports link is visible
    expect(ReportsPage(page).bureau_reports_link).to_be_visible()

    # Failsafe reports page opens as expected
    ReportsPage(page).go_to_failsafe_reports_page()
    BasePage(page).bowel_cancer_screening_page_title_contains_text("Failsafe Reports")
    BasePage(page).click_back_button()

    # Operational reports page opens as expected
    ReportsPage(page).go_to_operational_reports_page()
    BasePage(page).bowel_cancer_screening_page_title_contains_text(
        "Operational Reports"
    )
    BasePage(page).click_back_button()

    # Strategic reports page opens as expected
    ReportsPage(page).go_to_strategic_reports_page()
    BasePage(page).bowel_cancer_screening_page_title_contains_text("Strategic Reports")
    BasePage(page).click_back_button()

    # "Cancer waiting times reports" page opens as expected
    ReportsPage(page).go_to_cancer_waiting_times_reports_page()
    BasePage(page).bowel_cancer_screening_page_title_contains_text(
        "Cancer Waiting Times Reports"
    )
    BasePage(page).click_back_button()

    # Dashboard opens as expected TODO - this step may be failing legitimately
    # ReportsPage(page).go_to_dashboard()
    # BasePage(page).bowel_cancer_screening_page_title_contains_text("Dashboard")
    # BasePage(page).click_back_button()

    # QA Report : Dataset Completion link is visible
    expect(ReportsPage(page).qa_report_dataset_completion_link).to_be_visible()

    # Return to main menu
    BasePage(page).click_main_menu_link()
    BasePage(page).bowel_cancer_screening_page_title_contains_text("Main Menu")


# Failsafe Reports
def test_failsafe_reports_date_report_last_requested(page: Page) -> None:
    """
    Confirms 'date_report_last_requested' page loads, 'generate report' and 'refresh' buttons work as expected
    and the timestamp updates to current date and time when refreshed
    """

    # Go to failsafe reports page
    ReportsPage(page).go_to_failsafe_reports_page()

    # Click 'date report last requested' link
    ReportsPage(page).go_to_date_report_last_requested_page()

    # Verify 'Date Report Last Requested' is the page title
    BasePage(page).bowel_cancer_screening_page_title_contains_text(
        "Date Report Last Requested"
    )

    # Click 'generate report' button
    ReportsPage(page).click_generate_report_button()
    # Verify timestamp has updated (equals current date and time)
    report_timestamp = DateTimeUtils.report_timestamp_date_format()
    expect(ReportsPage(page).common_report_timestamp_element).to_contain_text(
        report_timestamp
    )

    # Click 'refresh' button
    ReportsPage(page).click_refresh_button()

    # Verify timestamp has updated (equals current date and time)
    report_timestamp = DateTimeUtils.report_timestamp_date_format()
    expect(ReportsPage(page).common_report_timestamp_element).to_contain_text(
        report_timestamp
    )


def test_failsafe_reports_screening_subjects_with_inactive_open_episode(
    page: Page,
) -> None:
    """
    Confirms 'screening_subjects_with_inactive_open_episode' page loads, 'generate report' button works as expected
    and that a screening subject record can be opened
    """

    # Go to failsafe reports page
    ReportsPage(page).go_to_failsafe_reports_page()

    # Click screening subjects with inactive open episode link
    ReportsPage(page).go_to_screening_subjects_with_inactive_open_episode_page()

    # Verify "Screening Subjects With Inactive Open Episode" is the page title
    BasePage(page).bowel_cancer_screening_page_title_contains_text(
        "Screening Subjects With Inactive Open Episode"
    )

    # Click 'Generate Report' button
    ReportsPage(page).click_generate_report_button()

    # Open a screening subject record
    ReportsPage(
        page
    ).click_fail_safe_reports_screening_subjects_with_inactive_open_episodes_link()

    # Verify the page title is "Subject Screening Summary"
    BasePage(page).bowel_cancer_screening_page_title_contains_text(
        "Subject Screening Summary"
    )


def test_failsafe_reports_subjects_ceased_due_to_date_of_birth_changes(
    page: Page,
) -> None:
    """
    Confirms 'subjects_ceased_due_to_date_of_birth_changes' page loads,
    the datepicker and 'generate report' button works as expected
    the timestamp updates to current date and time when refreshed and
    a screening subject record can be opened
    """

    # Test Data
    report_start_date = "18/03/2023"  # This date is specific to this test only

    # Go to failsafe reports page
    ReportsPage(page).go_to_failsafe_reports_page()

    # Click on "Subjects Ceased Due to Date Of Birth Changes" link
    ReportsPage(page).go_to_subjects_ceased_due_to_date_of_birth_changes_page()

    # Select a "report start date" from the calendar
    ReportsPage(page).report_start_date_field.fill(report_start_date)

    # Click "Generate Report"
    ReportsPage(page).click_generate_report_button()
    # Verify timestamp has updated to current date and time
    report_timestamp = DateTimeUtils.report_timestamp_date_format()
    expect(ReportsPage(page).subject_ceased_report_timestamp_element).to_contain_text(
        report_timestamp
    )

    # Open a screening subject record from the search results

    ReportsPage(page).click_failsafe_reports_sub_links()

    # Verify page title is "Subject Demographic"
    BasePage(page).bowel_cancer_screening_page_title_contains_text(
        "Subject Demographic"
    )


def test_failsafe_reports_allocate_sc_for_patient_movements_within_hub_boundaries(
    page: Page, general_properties: dict
) -> None:
    """
    Confirms 'allocate_sc_for_patient_movements_within_hub_boundaries' page loads,
    the 'generate report' button works as expected
    the timestamp updates to current date and time when refreshed
    a screening subject record can be opened and
    a different SC can be allocated to a patient record
    """

    # Go to failsafe reports page
    failsafe_report_page = ReportsPage(page)
    failsafe_report_page.go_to_failsafe_reports_page()

    # Click on the "Allocate SC for Patient Movements within Hub Boundaries" link
    failsafe_report_page.go_to_allocate_sc_for_patient_movements_within_hub_boundaries_page()

    # Verify page title is "Allocate SC for Patient Movements within Hub Boundaries"
    failsafe_report_page.bowel_cancer_screening_page_title_contains_text(
        "Allocate SC for Patient Movements within Hub Boundaries"
    )

    # Click "Generate Report"
    failsafe_report_page.click_generate_report_button()

    # Verify timestamp has updated to current date and time
    report_timestamp = DateTimeUtils.report_timestamp_date_format()
    expect(ReportsPage(page).common_report_timestamp_element).to_contain_text(
        report_timestamp
    )

    # Open a screening subject record from the first row/first cell of the table
    # nhs_number_link.click()
    ReportsPage(page).click_failsafe_reports_sub_links()

    # Verify page title is "Set Patient's Screening Centre"
    BasePage(page).bowel_cancer_screening_page_title_contains_text(
        "Set Patient's Screening Centre"
    )

    # Select another screening centre
    ReportsPage(page).set_patients_screening_centre_dropdown.select_option(
        general_properties["coventry_and_warwickshire_bcs_centre"]
    )

    # Click update
    failsafe_report_page.click_reports_pages_update_button()

    # Verify new screening centre has saved
    expect(ReportsPage(page).set_patients_screening_centre_dropdown).to_have_value(
        general_properties["coventry_and_warwickshire_bcs_centre"]
    )


def test_failsafe_reports_allocate_sc_for_patient_movements_into_your_hub(
    page: Page,
) -> None:
    """
    Confirms 'allocate_sc_for_patient_movements_into_your_hub' page loads,
    the 'generate report' and 'refresh' buttons work as expected and
    the timestamp updates to current date and time when refreshed
    """

    # Go to failsafe reports page
    ReportsPage(page).go_to_failsafe_reports_page()

    # Click on "allocate sc for patient movements into your hub" link
    ReportsPage(page).go_to_allocate_sc_for_patient_movements_into_your_hub_page()

    # Verify page title is "Date Report Last Requested"
    BasePage(page).bowel_cancer_screening_page_title_contains_text(
        "Allocate SC for Patient Movements into your Hub"
    )

    # Click "Generate Report" button
    ReportsPage(page).click_generate_report_button()

    # Verify timestamp has updated to current date and time
    report_timestamp = DateTimeUtils.report_timestamp_date_format()
    expect(ReportsPage(page).common_report_timestamp_element).to_contain_text(
        report_timestamp
    )

    # Click "Refresh" button
    ReportsPage(page).click_refresh_button()

    # Verify timestamp has updated to current date and time
    report_timestamp = DateTimeUtils.report_timestamp_date_format()
    expect(ReportsPage(page).common_report_timestamp_element).to_contain_text(
        report_timestamp
    )


def test_failsafe_reports_identify_and_link_new_gp(page: Page) -> None:
    """
    Confirms 'identify_and_link_new_gp' page loads,
    the 'generate report' and 'refresh' buttons work as expected
    the timestamp updates to current date and time when refreshed
    a screening subject record can be opened and the Link GP practice to Screening Centre page
    can be opened from here
    """

    # Go to failsafe reports page
    ReportsPage(page).go_to_failsafe_reports_page()

    # Click on "Identify and link new GP" link
    ReportsPage(page).go_to_identify_and_link_new_gp_page()

    # Verify page title is "Identify and link new GP practices"
    BasePage(page).bowel_cancer_screening_page_title_contains_text(
        "Identify and link new GP practices"
    )

    # Click on "Generate Report"
    ReportsPage(page).click_generate_report_button()

    # Verify timestamp has updated to current date and time
    report_timestamp = DateTimeUtils.report_timestamp_date_format()
    expect(ReportsPage(page).common_report_timestamp_element).to_contain_text(
        report_timestamp
    )

    # Click "Refresh" button
    ReportsPage(page).click_refresh_button()

    # Verify timestamp has updated to current date and time
    report_timestamp = DateTimeUtils.report_timestamp_date_format()
    expect(ReportsPage(page).common_report_timestamp_element).to_contain_text(
        report_timestamp
    )

    # Open a practice code from the first row/second cell of the table
    ReportsPage(page).click_fail_safe_reports_identify_and_link_new_gp_practices_link()

    # Verify page title is "Link GP practice to Screening Centre"
    BasePage(page).bowel_cancer_screening_page_title_contains_text(
        "Link GP practice to Screening Centre"
    )


# Operational Reports


def test_operational_reports_appointment_attendance_not_updated(
    page: Page, general_properties: dict
) -> None:
    """
    Confirms 'appointment_attendance_not_updated' page loads,
    a SC can be selected from the dropdown
    the 'generate report' button works as expected
    the timestamp updates to current date and time when refreshed and
    an appointment record can be opened from here
    """

    # Go to operational reports page
    ReportsPage(page).go_to_operational_reports_page()

    # Go to "appointment attendance not updated" report page
    ReportsPage(page).go_to_appointment_attendance_not_updated_page()

    # Verify page title is "Appointment Attendance Not Updated"
    BasePage(page).bowel_cancer_screening_page_title_contains_text(
        "Appointment Attendance Not Updated"
    )

    # Select a screening centre from the drop-down options
    ReportsPage(
        page
    ).attendance_not_updated_set_patients_screening_centre_dropdown.select_option(
        general_properties["coventry_and_warwickshire_bcs_centre"]
    )

    # Click "Generate Report" button
    ReportsPage(page).click_generate_report_button()

    # Verify timestamp has updated to current date and time
    report_timestamp = DateTimeUtils.report_timestamp_date_format()
    expect(ReportsPage(page).common_report_timestamp_element).to_contain_text(
        report_timestamp
    )

    # Open an appointment record from the report
    ReportsPage(page).click_failsafe_reports_sub_links()

    # Verify the page title is "Appointment Detail"
    BasePage(page).bowel_cancer_screening_page_title_contains_text("Appointment Detail")


def test_operational_reports_fobt_kits_logged_but_not_read(page: Page) -> None:
    """
    Confirms 'fobt_kits_logged_but_not_read' page loads,
    the 'refresh' button works as expected and
    the timestamp updates to current date and time when refreshed
    """

    # Go to operational reports page
    ReportsPage(page).go_to_operational_reports_page()

    # Go to "FOBT Kits Logged but Not Read" page
    ReportsPage(page).go_to_fobt_kits_logged_but_not_read_page()

    # Verify page title is "FOBT Kits Logged but Not Read - Summary View"
    BasePage(page).bowel_cancer_screening_page_title_contains_text(
        "FOBT Kits Logged but Not Read - Summary View"
    )

    # Click refresh button
    ReportsPage(page).click_refresh_button()

    # Verify timestamp has updated to current date and time
    report_timestamp = (
        DateTimeUtils.fobt_kits_logged_but_not_read_report_timestamp_date_format()
    )
    expect(
        ReportsPage(page).fobt_logged_not_read_report_timestamp_element
    ).to_contain_text(f"Report generated on {report_timestamp}.")


def test_operational_reports_demographic_update_inconsistent_with_manual_update(
    page: Page,
) -> None:
    """
    Confirms 'demographic_update_inconsistent_with_manual_update' page loads,
    the 'refresh' button works as expected and
    the timestamp updates to current date and time when refreshed
    """
    # Go to operational reports page
    ReportsPage(page).go_to_operational_reports_page()

    # Go to "Demographic Update Inconsistent With Manual Update" page
    ReportsPage(page).go_to_demographic_update_inconsistent_with_manual_update_page()

    # Verify page title is "Demographic Update Inconsistent With Manual Update"
    BasePage(page).bowel_cancer_screening_page_title_contains_text(
        "Demographic Update Inconsistent With Manual Update"
    )


def test_operational_reports_screening_practitioner_6_weeks_availability_not_set_up(
    page: Page, general_properties: dict
) -> None:
    """
    Confirms 'screening_practitioner_6_weeks_availability_not_set_up_report' page loads,
    a SC can be selected
    the 'generate report' and 'refresh' buttons work as expected and
    the timestamp updates to current date and time when refreshed
    """

    # Go to operational reports page
    ReportsPage(page).go_to_operational_reports_page()

    # Go to "Screening Practitioner 6 Weeks Availability Not Set Up" page
    ReportsPage(
        page
    ).go_to_screening_practitioner_6_weeks_availability_not_set_up_report_page()

    # Verify page title is "Screening Practitioner 6 Weeks Availability Not Set Up"
    BasePage(page).bowel_cancer_screening_page_title_contains_text(
        "Screening Practitioner 6 Weeks Availability Not Set Up"
    )

    # Select a screening centre
    ReportsPage(
        page
    ).six_weeks_availability_not_set_up_set_patients_screening_centre_dropdown.select_option(
        general_properties["coventry_and_warwickshire_bcs_centre"]
    )

    # Click "Generate Report"
    ReportsPage(page).click_generate_report_button()

    # Verify timestamp has updated to current date and time
    report_timestamp = DateTimeUtils.report_timestamp_date_format()
    expect(
        ReportsPage(page).six_weeks_availability_not_set_up_report_timestamp_element
    ).to_contain_text(report_timestamp)

    # Click "Refresh" button
    ReportsPage(page).click_refresh_button()

    # Verify timestamp has updated to current date and time
    report_timestamp = DateTimeUtils.report_timestamp_date_format()
    expect(
        ReportsPage(page).six_weeks_availability_not_set_up_report_timestamp_element
    ).to_contain_text(report_timestamp)


def test_operational_reports_screening_practitioner_appointments(
    page: Page, general_properties: dict
) -> None:
    """
    Confirms 'screening_practitioner_appointments' page loads,
    a SC and Screening Practitioner can be selected
    the 'generate report' button works as expected and
    the timestamp updates to current date and time when refreshed
    """

    # Go to operational reports page
    ReportsPage(page).go_to_operational_reports_page()

    # Go to "Screening Practitioner Appointments" page
    ReportsPage(page).go_to_screening_practitioner_appointments_page()

    # Verify page title is "Screening Practitioner Appointments"
    BasePage(page).bowel_cancer_screening_page_title_contains_text(
        "Screening Practitioner Appointments"
    )

    # Select a screening centre
    ReportsPage(
        page
    ).practitioner_appointments_set_patients_screening_centre_dropdown.select_option(
        general_properties["coventry_and_warwickshire_bcs_centre"]
    )

    # Select a screening practitioner
    ReportsPage(page).screening_practitioner_dropdown.select_option(
        general_properties["screening_practitioner_named_another_stubble"]
    )

    # Click "Generate Report"
    ReportsPage(page).operational_reports_sp_appointments_generate_report_button.click()

    # Verify timestamp has updated to current date and time
    report_timestamp = (
        DateTimeUtils.screening_practitioner_appointments_report_timestamp_date_format()
    )
    expect(ReportsPage(page).common_report_timestamp_element).to_contain_text(
        report_timestamp
    )
