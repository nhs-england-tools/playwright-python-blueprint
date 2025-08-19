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
    LogoutPage(page).log_out()


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
