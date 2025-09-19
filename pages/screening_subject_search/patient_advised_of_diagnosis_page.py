from playwright.sync_api import Page
from pages.base_page import BasePage
from datetime import datetime
from utils.calendar_picker import CalendarPicker


class PatientAdvisedOfDiagnosisPage(BasePage):
    """Advance FOBT Screening Episode Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Patient Advised Of Diagnosis - page locators
        self.diagnosis_date_calendar_icon = self.page.locator("#diagnosisAdvice span")
        self.reason_dropdown = self.page.locator("#reason")
        self.save_button = self.page.get_by_role("button", name="Save")

    def select_diagnosis_date_and_reason(self, date: datetime, reason: str) -> None:
        """
        Selects the diagnosis date and reason, then saves the form.
        Args:
            date (datetime): The diagnosis date to select.
            reason (str): The reason for the diagnosis.
        """
        self.click(self.diagnosis_date_calendar_icon)
        CalendarPicker(self.page).v2_calendar_picker(date)
        self.reason_dropdown.select_option(label=reason)
        self.click(self.save_button)
