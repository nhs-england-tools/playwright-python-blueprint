from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.table_util import TableUtils
from datetime import datetime
from utils.calendar_picker import CalendarPicker
from typing import Optional


class BookAppointmentPage(BasePage):
    """Book Appointment Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Book Appointment - page locators
        self.screening_center_dropdown = self.page.locator("#UI_NEW_SCREENING_CENTRE")
        self.site_dropdown = self.page.locator("#UI_NEW_SITE")
        self.appointment_time_radio_button = self.page.get_by_role(
            "radio", name="UI_NEW_SLOT_SELECTION_ID"
        )
        self.save_button = self.page.get_by_role("button", name="Save")
        self.appointments_table = TableUtils(self.page, "#displayRS")
        self.current_month_displayed = self.page.locator("#MONTH_AND_YEAR")
        self.screening_practitioner_dropdown = self.page.locator("#UI_NEW_PRACTITIONER")

        self.appointment_cell_locators = self.page.locator("input.twoColumnCalendar")
        self.appointment_fully_available_colour = "rgb(102, 255, 153)"  # Mint Green
        self.appointment_partially_available_colour = (
            "rgb(255, 220, 144)"  # Peach Orange
        )
        self.appointment_date_input = self.page.locator("#UI_NEW_APPT_DATE")
        self.appointment_time_start_time_input = self.page.locator(
            "#UI_NEW_APPT_TIME_FROM"
        )

    def select_screening_centre_dropdown_option(self, screening_centre: str) -> None:
        """Selects the screening centre from the dropdown."""
        self.screening_center_dropdown.select_option(label=screening_centre)

    def select_site_dropdown_option(self, screening_site: str | list) -> None:
        """Selects the screening site from the dropdown and presses Enter."""
        self.site_dropdown.select_option(label=screening_site)
        self.site_dropdown.press("Enter")

    def choose_appointment_time(self) -> None:
        """Checks the appointment time radio button."""
        self.appointment_time_radio_button.check()

    def click_save_button(self) -> None:
        """Clicks the save button."""
        self.safe_accept_dialog(self.save_button)

    def click_save_button_and_return_message(self) -> Optional[str]:
        """
        Clicks the save button and returns the dialog message if a dialog appears.
        Returns None if no dialog appears.
        """
        dialog_message = None

        def handle_dialog(dialog):
            nonlocal dialog_message
            dialog_message = dialog.message
            dialog.accept()

        self.page.once("dialog", handle_dialog)
        self.click(self.save_button)
        return dialog_message

    def appointment_booked_confirmation_is_displayed(self, message: str) -> None:
        """Checks if the appointment booked confirmation message is displayed."""
        expect(self.page.get_by_text(message)).to_be_visible(timeout=10000)

    def get_current_month_displayed(self) -> str:
        """Returns the current month displayed in the calendar."""
        current_month_displayed_content = self.current_month_displayed.text_content()
        if current_month_displayed_content is None:
            raise ValueError("Current month displayed is 'None'")
        return current_month_displayed_content

    def select_screening_practitioner_dropdown_option(self, index: int) -> None:
        """Selects the screening practitioner from the dropdown by index."""
        self.screening_practitioner_dropdown.select_option(index=index)

    def enter_appointment_date(self, date: datetime) -> None:
        """
        Enters the appointment date in the date input field and clicks 'Enter'.
        Args:
            date (datetime): The date to enter.
        """
        CalendarPicker(self.page).calendar_picker_ddmmyyyy(
            date, self.appointment_date_input
        )
        self.appointment_date_input.press("Enter")

    def enter_appointment_start_time(self, time: str) -> None:
        """
        Enters the appointment start time in the time input field and clicks 'Enter'.
        Args:
            time (str): The time to enter in the format 'HH:MM'.
        """
        self.appointment_time_start_time_input.fill(time)
        self.appointment_time_start_time_input.press("Enter")
