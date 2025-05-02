from playwright.sync_api import Page
from pages.base_page import BasePage


class ScreeningPractitionerDayViewPage(BasePage):
    """Screening Practitioner Day View Page locators and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Screening Practitioner Day View   - page locators
        self.calendar_button = page.get_by_role("button", name="Calendar")

    def click_calendar_button(self) -> None:
        """Click on the Calendar button to open the calendar picker."""
        self.click(self.calendar_button)

    def click_patient_link(self, patient_name: str) -> None:
        """Click on the patient link to navigate to the patient's details page."""
        self.click(self.page.get_by_role("link", name=patient_name))
