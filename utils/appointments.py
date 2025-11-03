import logging
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.logout.log_out_page import LogoutPage
from pages.screening_practitioner_appointments.practitioner_availability_page import (
    PractitionerAvailabilityPage,
)
from pages.screening_practitioner_appointments.screening_practitioner_appointments_page import (
    ScreeningPractitionerAppointmentsPage,
)
from pages.screening_practitioner_appointments.set_availability_page import (
    SetAvailabilityPage,
)
from pages.screening_practitioner_appointments.book_appointment_page import (
    BookAppointmentPage,
)
from utils.calendar_picker import CalendarPicker
from utils.user_tools import UserTools
from datetime import datetime, timedelta
from pages.screening_practitioner_appointments.appointment_detail_page import (
    AppointmentDetailPage,
)
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from pages.screening_subject_search.episode_events_and_notes_page import (
    EpisodeEventsAndNotesPage,
)


def setup_appointments(page: Page, no_of_practitioners: int, max: bool = False) -> None:
    """
    Set up appointments for multiple practitioners at a screening centre.
    This function logs in as a Screening Centre Manager, sets availability for
    practitioners, and creates appointments for the next 10 practitioners.

    Args:
        no_of_practitioners (int): The number of practitioners to set up appointments for.
        max (bool): If True, sets up appointments for all practitioners. Defaults to False.
    """
    UserTools.user_login(page, "Screening Centre Manager at BCS001")

    if max:
        go_to_appointments_page_and_select_site(page)
        total_practitioners = (
            PractitionerAvailabilityPage(page)
            .screening_practitioner_dropdown.locator("option")
            .count()
        )
        no_of_practitioners = total_practitioners - 1  # Exclude the first option
        BasePage(page).click_main_menu_link()

    logging.info(f"Setting up appointments for {no_of_practitioners} practitioners")
    for index in range(no_of_practitioners):
        logging.info(f"Setting up appointments for practitioner {index + 1}")
        go_to_appointments_page_and_select_site(page)
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
        logging.info(f"Appointments set for practitioner {index + 1} at BCS001")
        BasePage(page).click_main_menu_link()
    LogoutPage(page).log_out(close_page=False)


def go_to_appointments_page_and_select_site(page: Page) -> None:
    """
    Navigate to the Screening Practitioner Appointments page.

    Args:
        page (Page): The Playwright page object.
    """
    BasePage(page).go_to_screening_practitioner_appointments_page()
    ScreeningPractitionerAppointmentsPage(page).go_to_set_availability_page()
    SetAvailabilityPage(page).go_to_practitioner_availability_page()
    PractitionerAvailabilityPage(page).select_site_dropdown_option(
        "THE ROYAL HOSPITAL (WOLVERHAMPTON)"
    )
    page.wait_for_timeout(1000)  # Wait for the practitioners to load


def book_appointments(page: Page, screening_centre: str, site: str) -> None:
    """
    Book appointments for the selected practitioner.

    Args:
        page (Page): The Playwright page object.
        screening_centre (str): The name of the screening centre.
        site (str): The name of the site.
    Raises:
        RuntimeError: If the appointment booking confirmation is not displayed.
    """
    book_appointments_page = BookAppointmentPage(page)
    book_appointments_page.select_screening_centre_dropdown_option(screening_centre)
    book_appointments_page.select_site_dropdown_option(
        [
            f"{site} (? km)",
            f"{site} (? km) (attended)",
        ]
    )

    # And I book the "earliest" available practitioner appointment on this date
    current_month_displayed = book_appointments_page.get_current_month_displayed()
    CalendarPicker(page).book_first_eligible_appointment(
        current_month_displayed,
        book_appointments_page.appointment_cell_locators,
        [
            book_appointments_page.appointment_fully_available_colour,
            book_appointments_page.appointment_partially_available_colour,
        ],
    )
    page.wait_for_timeout(500)  # Wait for the appointments to load
    book_appointments_page.appointments_table.click_first_input_in_column(
        "Appt/Slot Time"
    )
    BasePage(page).safe_accept_dialog(book_appointments_page.save_button)
    try:
        book_appointments_page.appointment_booked_confirmation_is_displayed(
            "Appointment booked"
        )
        logging.info("[BOOK APPOINTMENTS] Appointment successfully booked")
    except Exception as e:
        raise RuntimeError(
            f"[BOOK APPOINTMENTS] Appointment not booked successfully: {e}"
        )


def book_post_investigation_appointment(
    page: Page,
    site: str,
    screening_practitioner_index: int,
    appointment_start_time: str = "08:00",
) -> None:
    """
    Book a post-investigation appointment for a subject.
    Sets the appointment date to today and the start time to '08:00'.
    If a dialog about overlapping appointments is triggered, increases the start time by 15 minutes and retries.
    Loops until a successful booking or until 17:00.
    Args:
        page (Page): The Playwright page object.
        site (str): The name of the site.
        screening_practitioner_index (int): The index of the screening practitioner to select.
        appointment_start_time (str): The start time for the appointment.
    """
    book_appointments_page = BookAppointmentPage(page)
    book_appointments_page.select_site_dropdown_option(
        [
            f"{site} (? km)",
            f"{site} (? km) (attended)",
        ]
    )
    book_appointments_page.select_screening_practitioner_dropdown_option(
        screening_practitioner_index
    )
    book_appointments_page.enter_appointment_date(datetime.today())

    overlap_message = "Overlaps a Post Investigation, Surveillance appointment or Colonoscopy Assessment appointment"
    hour, minute = map(int, appointment_start_time.split(":"))

    while True:
        current_time = f"{hour:02d}:{minute:02d}"
        book_appointments_page.enter_appointment_start_time(current_time)
        dialog_message = book_appointments_page.click_save_button_and_return_message()
        if dialog_message is None or overlap_message not in dialog_message:
            # Success or no overlap dialog
            break
        # Increase time by 15 minutes
        minute += 15
        if minute >= 60:
            hour += 1
            minute -= 60
        if hour >= 17:
            raise ValueError("Could not book appointment before 17:00 due to overlaps.")


def book_practitioner_appointment(
    page: Page,
    site: str,
    screening_practitioner_index: int,
    appointment_start_time: str = "08:00",
) -> None:
    """
    Book a practitioner appointment for a subject.
    Sets the appointment date to today and the start time to '08:00'.
    If a dialog about overlapping appointments is triggered, increases the start time by 15 minutes and retries.
    Loops until a successful booking or until 17:00.
    Args:
        page (Page): The Playwright page object.
        site (str): The name of the site.
        screening_practitioner_index (int): The index of the screening practitioner to select.
        appointment_start_time (str): The start time for the appointment.
    """
    book_post_investigation_appointment(
        page, site, screening_practitioner_index, appointment_start_time
    )


class AppointmentAttendance(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # Page object dependencies
        self.appointment_detail_page = AppointmentDetailPage(page)
        self.subject_screening_summary_page = SubjectScreeningSummaryPage(page)
        self.episode_events_and_notes_page = EpisodeEventsAndNotesPage(page)

        # Locators
        self.attended_checkbox = self.page.locator("#UI_ATTENDED")
        self.attended_date_field = self.page.locator("#UI_ATTENDED_DATE")
        self.attended_time_from_field = self.page.locator("#UI_ATTENDED_TIME_FROM")
        self.attended_time_to_field = self.page.locator("#UI_ATTENDED_TIME_TO")
        self.meeting_mode_field = self.page.locator("#UI_NEW_MEETING_MODE")
        self.non_attendance_reason_dropdown = self.page.locator(
            "#UI_NON_ATTENDANCE_REASON"
        )
        self.dna_diagnostic_test_date_field = self.page.locator("#UI_APPT_DATE_1210")
        self.dna_diagnostic_test_button = self.page.get_by_role(
            "button", name="DNA Diagnostic Test >>"
        )

    def mark_as_dna(self, non_attendance_reason: str) -> None:
        """
        Marks an appointment as DNA (Did Not Attend).
        Navigates through the subject's episode and appointment pages,
        selects the 'Attendance' radio option, and sets the given DNA reason.
        """
        logging.info(
            f"[APPOINTMENT DNA] Starting DNA flow with reason: {non_attendance_reason}"
        )
        self.subject_screening_summary_page.click_list_episodes()
        self.subject_screening_summary_page.click_view_events_link()
        self.episode_events_and_notes_page.click_most_recent_view_appointment_link()
        self.appointment_detail_page.check_attendance_radio()
        self.non_attendance_reason_dropdown.select_option(label=non_attendance_reason)
        self.appointment_detail_page.click_save_button(accept_dialog=True)
        logging.info("[APPOINTMENT DNA] DNA flow completed successfully")

    def mark_as_attended_today(self) -> None:
        """
        Marks an appointment as attended and logs the auto-filled attendance details.
        """
        logging.info("[APPOINTMENT ATTENDED] Starting attended flow")
        self.subject_screening_summary_page.click_list_episodes()
        self.subject_screening_summary_page.click_view_events_link()
        self.episode_events_and_notes_page.click_most_recent_view_appointment_link()
        self.appointment_detail_page.check_attendance_radio()

        self.attended_checkbox.check()

        attended_date = self.attended_date_field.input_value()
        time_from = self.attended_time_from_field.input_value()
        time_to = self.attended_time_to_field.input_value()
        meeting_mode = self.meeting_mode_field.input_value()

        logging.info(
            f"[APPOINTMENT ATTENDED] How Attended: {meeting_mode}, Date: {attended_date}, Time From: {time_from}, Time To: {time_to}"
        )

        self.appointment_detail_page.click_save_button(accept_dialog=True)
        logging.info("[APPOINTMENT ATTENDED] Attended flow completed successfully")

    def mark_as_attended_yesterday(self) -> None:
        """
        Marks an appointment as attended with the attendance date set to yesterday.
        """
        logging.info("[APPOINTMENT ATTENDED] Starting attended-yesterday flow")
        self.subject_screening_summary_page.click_list_episodes()
        self.subject_screening_summary_page.click_view_events_link()
        self.episode_events_and_notes_page.click_most_recent_view_appointment_link()
        self.appointment_detail_page.check_attendance_radio()

        self.attended_checkbox.check()

        yesterday = (datetime.today() - timedelta(days=1)).strftime("%d/%m/%Y")
        self.attended_date_field.fill(yesterday)

        attended_date = self.attended_date_field.input_value()
        time_from = self.attended_time_from_field.input_value()
        time_to = self.attended_time_to_field.input_value()
        meeting_mode = self.meeting_mode_field.input_value()

        logging.info(
            f"[APPOINTMENT ATTENDED] How Attended: {meeting_mode}, Date: {attended_date}, Time From: {time_from}, Time To: {time_to}"
        )

        self.appointment_detail_page.click_save_button(accept_dialog=True)
        logging.info(
            "[APPOINTMENT ATTENDED] Attended-yesterday flow completed successfully"
        )

    def mark_diagnostic_test_as_dna(self) -> None:
        """
        Marks a subject's diagnostic test appointment as DNA (Did Not Attend).
        Fills today's date and triggers the DNA Diagnostic Test action.
        """
        logging.info(
            "[APPOINTMENT DNA] Starting DNA flow with reason: Did not attend - Diagnostic Test"
        )
        today = datetime.today().strftime("%d/%m/%Y")
        self.dna_diagnostic_test_date_field.fill(today)

        self.safe_accept_dialog(self.dna_diagnostic_test_button)
        logging.info(
            "[APPOINTMENT DNA] DNA diagnostic test flow completed successfully"
        )
