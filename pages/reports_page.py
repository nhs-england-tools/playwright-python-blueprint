from datetime import datetime
from utils import date_time_utils
from playwright.sync_api import Page


class ReportsPageUtils:
    def __init__(self):
        pass


# Timestamp Date Formatting
def report_timestamp_date_format() -> str:
    """Gets the current date time and converts it to the timestamp format used on the report pages

    Returns:
        date report last requested (str): The current datetime in the "date report last requested" timestamp format.

    """
    dtu = date_time_utils.DateTimeUtils
    return dtu.format_date(datetime.now(), "%d/%m/%Y" + " at " + "%H:%M:%S")


def fobt_kits_logged_but_not_read_report_timestamp_date_format() -> str:
    """Gets the current date time and converts it to the timestamp format used on the fobt_kits_logged_but_not_read report page

    Returns:
        fobt_kits_logged_but_not_read timestamp (str): The current datetime in the "fobt_kits_logged_but_not_read report" timestamp format.

    """
    dtu = date_time_utils.DateTimeUtils
    return dtu.format_date(datetime.now(), "%d %b %Y %H:%M:%S")


def screening_practitioner_appointments_report_timestamp_date_format() -> str:
    """Gets the current date time and converts it to the timestamp format used on the screening practitioner appointments report page

    Returns:
        screening practitioner appointments timestamp (str): The current datetime in the "screening practitioner appointments report" timestamp format.

    """
    dtu = date_time_utils.DateTimeUtils
    return dtu.format_date(datetime.now(), "%d.%m.%Y" + " at " + "%H:%M:%S")


# Reports page main menu links
def go_to_failsafe_reports_page(page: Page) -> None:
    page.get_by_role("link", name="Failsafe Reports").click()


def go_to_operational_reports_page(page: Page) -> None:
    page.get_by_role("link", name="Operational Reports").click()


def go_to_strategic_reports_page(page: Page) -> None:
    page.get_by_role("link", name="Strategic Reports").click()


def go_to_cancer_waiting_times_reports_page(page: Page) -> None:
    page.get_by_role("link", name="Cancer Waiting Times Reports").click()


def go_to_dashboard(page: Page) -> None:
    page.get_by_role("link", name="Dashboard").click()


# Failsafe Reports menu links
def go_to_date_report_last_requested_page(page: Page) -> None:
    page.get_by_role("link", name="Date Report Last Requested").click()


def go_to_screening_subjects_with_inactive_open_episode_link_page(page: Page) -> None:
    page.get_by_role("link", name="Screening Subjects With").click()


def go_to_subjects_ceased_due_to_date_of_birth_changes_page(page: Page) -> None:
    page.get_by_role("link", name="Subjects Ceased Due to Date").click()


def go_to_allocate_sc_for_patient_movements_within_hub_boundaries_page(page: Page) -> None:
    page.get_by_role("link", name="Allocate SC for Patient Movements within Hub Boundaries").click()


def go_to_allocate_sc_for_patient_movements_into_your_hub_page(page: Page) -> None:
    page.get_by_role("link", name="Allocate SC for Patient Movements into your Hub").click()


def go_to_identify_and_link_new_gp_page(page: Page) -> None:
    page.get_by_role("link", name="Identify and link new GP").click()


# Operational Reports menu links
def go_to_appointment_attendance_not_updated_page(page: Page) -> None:
    page.get_by_role("link", name="Appointment Attendance Not").click()


def go_to_fobt_kits_logged_but_not_read_page(page: Page) -> None:
    page.get_by_role("link", name="FOBT Kits Logged but Not Read").click()


def go_to_demographic_update_inconsistent_with_manual_update_page(page: Page) -> None:
    page.get_by_role("link", name="Demographic Update").click()


def go_to_screening_practitioner_6_weeks_availability_not_set_up_report_page(page: Page) -> None:
    page.get_by_role("link", name="Screening Practitioner 6").click()


def go_to_screening_practitioner_appointments_page(page: Page) -> None:
    page.get_by_role("link", name="Screening Practitioner Appointments").click()
