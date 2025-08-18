from playwright.sync_api import Page, expect
from datetime import datetime
from pages.base_page import BasePage
from utils.calendar_picker import CalendarPicker


class ResectAndDiscardAccreditationHistoryPage(BasePage):
    """Resect And Discard Accreditation History Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Resect And Discard Accreditation History - page locators, methods
        self.heading = self.page.get_by_role("heading", name="Resect and Discard")
        self.add_accreditation_button = self.page.get_by_role(
            "button", name="+ Add Accreditation"
        )
        self.save_button = self.page.get_by_role("button", name="Save")
        self.changes_saved_text = self.page.get_by_text("×Saved Changes")

    def verify_heading_is_correct(self) -> None:
        """Verifies the heading is visible and contains 'View Resect and Discard'"""
        expect(self.heading).to_be_visible()

    def verify_add_accreditation_button_exists(self) -> None:
        """Verifies that the 'Add Accreditation' button exists"""
        expect(self.add_accreditation_button).to_be_visible()

    def click_add_accreditation_button(self) -> None:
        """Clicks the 'Add Accreditation' button"""
        self.click(self.add_accreditation_button)

    def click_save_button(self) -> None:
        """Clicks the 'Save' button"""
        self.click(self.save_button)

    def verify_changes_saved(self) -> None:
        """Verifies the new period added has been saved"""
        expect(self.changes_saved_text).to_be_visible()

    def add_new_period_of_resect_and_discard_accerditation(
        self, date: datetime
    ) -> None:
        """
        Adds a new period of resect and discard accreditation
        Args:
            date (datetime): The date the period starts
        """
        self.click_add_accreditation_button()
        CalendarPicker(self.page).v2_calendar_picker(date)
        self.click_save_button()
        self.verify_changes_saved()
