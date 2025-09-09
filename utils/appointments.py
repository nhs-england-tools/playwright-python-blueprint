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
from datetime import datetime


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
            book_appointments_page.available_background_colour,
            book_appointments_page.some_available_background_colour,
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
