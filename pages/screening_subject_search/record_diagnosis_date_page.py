from playwright.sync_api import Page
from pages.base_page import BasePage
from datetime import datetime
from utils.calendar_picker import CalendarPicker


class RecordDiagnosisDatePage(BasePage):
    """Record Diagnosis Date Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Record Diagnosis Date - page locators
        self.diagnosis_date_field = self.page.locator("#diagnosisDate")
        self.save_button = self.page.get_by_role("button", name="Save")

    def enter_date_in_diagnosis_date_field(self, date: datetime) -> None:
        """
        Enters a date in the diagnosis date field.
        Args:
            date (datetime): The date to enter in the field.
        """
        self.click(self.diagnosis_date_field)
        CalendarPicker(self.page).v2_calendar_picker(date)
        self.diagnosis_date_field.press("Enter")

    def click_save_button(self) -> None:
        """Clicks the save button."""
        self.click(self.save_button)
