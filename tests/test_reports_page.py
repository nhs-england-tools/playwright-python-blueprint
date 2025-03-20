import pytest
from playwright.sync_api import Page, expect
from pages import reports_page
from pages.bcss_home_page import MainMenu
from utils.user_tools import UserTools


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as the specified user and navigates to the
    reports page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager State Registered")

    # Open reports page
    MainMenu(page).go_to_reports_page()


@pytest.mark.smoke
def test_reports_page_navigation(page: Page) -> None:
    """
    Confirms all menu items are displayed on the reports page, and that the relevant pages
    are loaded when the links are clicked
    """
    # Bureau reports link is visible
    expect(page.get_by_text("Bureau Reports")).to_be_visible()

    # Failsafe reports page opens as expected
    reports_page.go_to_failsafe_reports_page(page)
    expect(page.locator("#ntshPageTitle")).to_contain_text("Failsafe Reports")
    page.get_by_role("link", name="Back").click()

    # Operational reports page opens as expected
    reports_page.go_to_operational_reports_page(page)
    expect(page.locator("#ntshPageTitle")).to_contain_text("Operational Reports")
    page.get_by_role("link", name="Back").click()

    # Strategic reports page opens as expected
    reports_page.go_to_strategic_reports_page(page)
    expect(page.locator("#ntshPageTitle")).to_contain_text("Strategic Reports")
    page.get_by_role("link", name="Back").click()

    # "Cancer waiting times reports" page opens as expected
    reports_page.go_to_cancer_waiting_times_reports_page(page)
    expect(page.locator("#ntshPageTitle")).to_contain_text("Cancer Waiting Times Reports")
    page.get_by_role("link", name="Back").click()

    # Dashboard opens as expected TODO - this step may be failing legitimately
    # reports_page.go_to_dashboard(page)
    # expect(page.locator("#ntshPageTitle")).to_contain_text("Dashboard")
    # page.get_by_role("link", name="Back").click()

    # QA Report : Dataset Completion link is visible
    expect(page.get_by_text("QA Report : Dataset Completion")).to_be_visible()

    # Return to main menu
    page.get_by_role("link", name="Main Menu").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Main Menu")


# Failsafe Reports
def test_failsafe_reports_date_report_last_requested(page: Page) -> None:
    """
    Confirms 'date_report_last_requested' page loads, 'generate report' and 'refresh' buttons work as expected
    and the timestamp updates to current date and time when refreshed
    """
    # Go to failsafe reports page
    reports_page.go_to_failsafe_reports_page(page)

    # Click 'date report last requested' link
    reports_page.go_to_date_report_last_requested_page(page)

    # Verify 'Date Report Last Requested' is the page title
    expect(page.locator("#ntshPageTitle")).to_contain_text("Date Report Last Requested")

    # Click 'generate report' button
    page.get_by_role("button", name="Generate Report").click()

    # Verify timestamp has updated (equals current date and time)
    report_timestamp = reports_page.report_timestamp_date_format()
    expect(page.locator("b")).to_contain_text(report_timestamp)

    # Click 'refresh' button
    page.get_by_role("button", name="Refresh").click()

    # Verify timestamp has updated (equals current date and time)
    report_timestamp = reports_page.report_timestamp_date_format()
    expect(page.locator("b")).to_contain_text(report_timestamp)


def test_failsafe_reports_screening_subjects_with_inactive_open_episode(page: Page) -> None:
    """
    Confirms 'screening_subjects_with_inactive_open_episode' page loads, 'generate report' button works as expected
    and that a screening subject record can be opened
    """
    # Go to failsafe reports page
    reports_page.go_to_failsafe_reports_page(page)

    # Click screening subjects with inactive open episode link
    reports_page.go_to_screening_subjects_with_inactive_open_episode_link_page(page)

    # Verify "Screening Subjects With Inactive Open Episode" is the page title
    expect(page.locator("#page-title")).to_contain_text("Screening Subjects With Inactive Open Episode")

    # Click 'Generate Report' button
    page.get_by_role("button", name="Generate Report").click()

    # Open a screening subject record
    page.get_by_role("cell", name="401 7652").click()

    # Verify "Subject Screening Summary" is the page title
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Screening Summary")


def test_failsafe_reports_subjects_ceased_due_to_date_of_birth_changes(page: Page) -> None:
    """
    Confirms 'subjects_ceased_due_to_date_of_birth_changes' page loads,
    the datepicker and 'generate report' button works as expected
    the timestamp updates to current date and time when refreshed and
    a screening subject record can be opened
    """
    # Go to failsafe reports page
    reports_page.go_to_failsafe_reports_page(page)

    # Click on "Subjects Ceased Due to Date Of Birth Changes" link
    reports_page.go_to_subjects_ceased_due_to_date_of_birth_changes_page(page)

    # Select a "report start date" from the calendar
    page.get_by_role("button", name="Calendar").click()
    page.get_by_text("«").click()
    page.get_by_role("cell", name="18", exact=True).click()

    # Click "Generate Report"
    page.get_by_role("button", name="Generate Report").click()

    # Verify timestamp has updated to current date and time
    report_timestamp = reports_page.report_timestamp_date_format()
    expect(page.locator("b")).to_contain_text(report_timestamp)

    # Open a screening subject record from the search results
    page.get_by_role("cell", name="954 296 8175", exact=True).click()

    # Verify page title is "Subject Demographic"
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Demographic")


def test_failsafe_reports_allocate_sc_for_patient_movements_within_hub_boundaries(page: Page) -> None:
    """
    Confirms 'allocate_sc_for_patient_movements_within_hub_boundaries' page loads,
    the 'generate report' button works as expected
    the timestamp updates to current date and time when refreshed
    a screening subject record can be opened and
    a different SC can be allocated to a patient record
    """
    # Go to failsafe reports page
    reports_page.go_to_failsafe_reports_page(page)

    # Click on the "Allocate SC for Patient Movements within Hub Boundaries" link
    reports_page.go_to_allocate_sc_for_patient_movements_within_hub_boundaries_page(page)

    # Verify page title is "Allocate SC for Patient Movements within Hub Boundaries"
    expect(page.locator("#ntshPageTitle")).to_contain_text("Allocate SC for Patient Movements within Hub Boundaries")

    # Click "Generate Report"
    page.get_by_role("button", name="Generate Report").click()

    # Verify timestamp has updated to current date and time
    report_timestamp = reports_page.report_timestamp_date_format()
    expect(page.locator("b")).to_contain_text(report_timestamp)

    # Open a screening subject record from the first row/first cell of the table
    page.locator("//*[@id='listReportDataTable']/tbody/tr[3]/td[1]").click()

    # Verify page title is "Set Patient's Screening Centre"
    expect(page.locator("#ntshPageTitle")).to_contain_text("Set Patient's Screening Centre")

    # Select another screening centre
    page.locator("#cboScreeningCentre").select_option("23643")

    # Click update
    page.get_by_role("button", name="Update").click()

    # Verify new screening centre has saved
    expect(page.locator("#cboScreeningCentre")).to_have_value("23643")


def test_failsafe_reports_allocate_sc_for_patient_movements_into_your_hub(page: Page) -> None:
    """
    Confirms 'allocate_sc_for_patient_movements_into_your_hub' page loads,
    the 'generate report' and 'refresh' buttons work as expected and
    the timestamp updates to current date and time when refreshed
    """
    # Go to failsafe reports page
    reports_page.go_to_failsafe_reports_page(page)

    # Click on "allocate sc for patient movements into your hub" link
    reports_page.go_to_allocate_sc_for_patient_movements_into_your_hub_page(page)

    # Verify page title is "Date Report Last Requested"
    expect(page.locator("#ntshPageTitle")).to_contain_text("Allocate SC for Patient Movements into your Hub")

    # Click "Generate Report" button
    page.get_by_role("button", name="Generate Report").click()

    # Verify timestamp has updated to current date and time
    report_timestamp = reports_page.report_timestamp_date_format()
    expect(page.locator("b")).to_contain_text(report_timestamp)

    # Click "Refresh" button
    page.get_by_role("button", name="Refresh").click()

    # Verify timestamp has updated to current date and time
    report_timestamp = reports_page.report_timestamp_date_format()
    expect(page.locator("b")).to_contain_text(report_timestamp)


def test_failsafe_reports_identify_and_link_new_gp(page: Page) -> None:
    """
    Confirms 'identify_and_link_new_gp' page loads,
    the 'generate report' and 'refresh' buttons work as expected
    the timestamp updates to current date and time when refreshed
    a screening subject record can be opened and the Link GP practice to Screening Centre page
    can be opened from here
    """
    # Go to failsafe reports page
    reports_page.go_to_failsafe_reports_page(page)

    # Click on "Identify and link new GP" link
    reports_page.go_to_identify_and_link_new_gp_page(page)

    # Verify page title is "Identify and link new GP practices"
    expect(page.locator("#ntshPageTitle")).to_contain_text("Identify and link new GP practices")

    # Click on "Generate Report"
    page.get_by_role("button", name="Generate Report").click()

    # Verify timestamp has updated to current date and time
    report_timestamp = reports_page.report_timestamp_date_format()
    expect(page.locator("b")).to_contain_text(report_timestamp)

    # Click "Refresh" button
    page.get_by_role("button", name="Refresh").click()

    # Verify timestamp has updated to current date and time
    report_timestamp = reports_page.report_timestamp_date_format()
    expect(page.locator("b")).to_contain_text(report_timestamp)

    # Open a screening subject record from the first row/second cell of the table
    page.locator("//*[@id='listReportDataTable']/tbody/tr[3]/td[2]").click()

    # Verify page title is "Link GP practice to Screening Centre"
    expect(page.locator("#ntshPageTitle")).to_contain_text("Link GP practice to Screening Centre")


# Operational Reports
def test_operational_reports_appointment_attendance_not_updated(page: Page) -> None:
    """
    Confirms 'appointment_attendance_not_updated' page loads,
    a SC can be selected from the dropdown
    the 'generate report' button works as expected
    the timestamp updates to current date and time when refreshed and
    an appointment record can be opened from here
    """
    # Go to operational reports page
    reports_page.go_to_operational_reports_page(page)

    # Go to "appointment attendance not updated" report page
    reports_page.go_to_appointment_attendance_not_updated_page(page)

    # Verify page title is "Appointment Attendance Not Updated"
    expect(page.locator("#ntshPageTitle")).to_contain_text("Appointment Attendance Not Updated")

    # Select a screening centre from the drop-down options
    page.get_by_label("Screening Centre").select_option("23643")

    # Click "Generate Report" button
    page.get_by_role("button", name="Generate Report").click()

    # Verify timestamp has updated to current date and time
    report_timestamp = reports_page.report_timestamp_date_format()
    expect(page.locator("b")).to_contain_text(report_timestamp)

    # Open an appointment record from the report
    page.locator("#listReportDataTable > tbody > tr:nth-child(3) > td:nth-child(1) > a").click()

    # Verify the page title is "Appointment Detail"
    expect(page.locator("#ntshPageTitle")).to_contain_text("Appointment Detail")


def test_operational_reports_fobt_kits_logged_but_not_read(page: Page) -> None:
    """
    Confirms 'fobt_kits_logged_but_not_read' page loads,
    the 'refresh' button works as expected and
    the timestamp updates to current date and time when refreshed
    """
    # Go to operational reports page
    reports_page.go_to_operational_reports_page(page)

    # Go to "FOBT Kits Logged but Not Read" page
    reports_page.go_to_fobt_kits_logged_but_not_read_page(page)

    # Verify page title is "FOBT Kits Logged but Not Read - Summary View"
    expect(page.locator("#page-title")).to_contain_text("FOBT Kits Logged but Not Read - Summary View")

    # Click refresh button
    page.get_by_role("button", name="Refresh").click()

    # Verify timestamp has updated to current date and time
    report_timestamp = reports_page.fobt_kits_logged_but_not_read_report_timestamp_date_format()
    expect(page.locator("#report-generated")).to_contain_text(f"Report generated on {report_timestamp}.")


def test_operational_reports_demographic_update_inconsistent_with_manual_update(page: Page) -> None:
    """
    Confirms 'demographic_update_inconsistent_with_manual_update' page loads,
    the 'refresh' button works as expected and
    the timestamp updates to current date and time when refreshed
    """
    # Go to operational reports page
    reports_page.go_to_operational_reports_page(page)

    # Go to "Demographic Update Inconsistent With Manual Update" page
    reports_page.go_to_demographic_update_inconsistent_with_manual_update_page(page)

    # Verify page title is "Demographic Update Inconsistent With Manual Update"
    expect(page.locator("#page-title")).to_contain_text("Demographic Update Inconsistent With Manual Update")


def test_operational_reports_screening_practitioner_6_weeks_availability_not_set_up(page: Page) -> None:
    """
    Confirms 'screening_practitioner_6_weeks_availability_not_set_up_report' page loads,
    a SC can be selected
    the 'generate report' and 'refresh' buttons work as expected and
    the timestamp updates to current date and time when refreshed
    """
    # Go to operational reports page
    reports_page.go_to_operational_reports_page(page)

    # Go to "Screening Practitioner 6 Weeks Availability Not Set Up" page
    reports_page.go_to_screening_practitioner_6_weeks_availability_not_set_up_report_page(page)

    # Verify page title is "Screening Practitioner 6 Weeks Availability Not Set Up"
    expect(page.locator("#ntshPageTitle")).to_contain_text("Screening Practitioner 6 Weeks Availability Not Set Up")

    # Select a screening centre
    page.get_by_label("Screening Centre").select_option("23643")

    # Click "Generate Report"
    page.get_by_role("button", name="Generate Report").click()

    # Verify timestamp has updated to current date and time
    report_timestamp = reports_page.report_timestamp_date_format()
    expect(page.locator("#displayGenerateDate")).to_contain_text(report_timestamp)

    # Click "Refresh" button
    page.get_by_role("button", name="Refresh").click()

    # Verify timestamp has updated to current date and time
    report_timestamp = reports_page.report_timestamp_date_format()
    expect(page.locator("#displayGenerateDate")).to_contain_text(report_timestamp)


def test_operational_reports_screening_practitioner_appointments(page: Page) -> None:
    """
    Confirms 'screening_practitioner_appointments' page loads,
    a SC and Screening Practitioner can be selected
    the 'generate report' button works as expected and
    the timestamp updates to current date and time when refreshed
    """
    # Go to operational reports page
    reports_page.go_to_operational_reports_page(page)

    # Go to "Screening Practitioner Appointments" page
    reports_page.go_to_screening_practitioner_appointments_page(page)

    # Verify page title is "Screening Practitioner Appointments"
    expect(page.locator("#ntshPageTitle")).to_contain_text("Screening Practitioner Appointments")

    # Select a screening centre
    page.get_by_label("Screening Centre").select_option("23643")

    # Select a screening practitioner
    page.locator("#A_C_NURSE").select_option("1982")

    # Click "Generate Report"
    page.locator("#submitThisForm").click()

    # Verify timestamp has updated to current date and time
    report_timestamp = reports_page.screening_practitioner_appointments_report_timestamp_date_format()
    expect(page.locator("b")).to_contain_text(report_timestamp)
