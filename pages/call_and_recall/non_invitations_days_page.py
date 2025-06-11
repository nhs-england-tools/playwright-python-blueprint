from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.date_time_utils import DateTimeUtils


class NonInvitationDaysPage(BasePage):
    """Non Invitation Days page locators, and methods to interact with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Non Invitation Days - page locators, methods
        self.enter_note_field = self.page.locator("#note")
        self.enter_date_field = self.page.get_by_role("textbox", name="date")
        self.add_non_invitation_day_button = self.page.get_by_role(
            "button", name="Add Non-Invitation Day"
        )
        self.non_invitation_day_delete_button = self.page.get_by_role(
            "button", name="Delete"
        )
        self.created_on_date_locator = self.page.locator(
            "tr.oddTableRow td:nth-child(4)"
        )

    def verify_non_invitation_days_tile(self) -> None:
        """Verifies the page title of the Non Invitation Days page"""
        self.bowel_cancer_screening_page_title_contains_text("Non-Invitation Days")

    def enter_date(self, date: str) -> None:
        """Enters a date in the date input field
        Args:
            date (str): The date to enter in the field, formatted as 'dd/mm/yyyy'.
        """
        self.enter_date_field.fill(date)

    def enter_note(self, note: str) -> None:
        """Enters a note in the note input field
        Args:
            note (str): The note to enter in the field.
        """
        self.enter_note_field.fill(note)

    def click_add_non_invitation_day_button(self) -> None:
        """Clicks the Add Non-Invitation Day button"""
        self.click(self.add_non_invitation_day_button)

    def click_delete_button(self) -> None:
        """Clicks the Delete button for a non-invitation day"""
        self.click(self.non_invitation_day_delete_button)

    def verify_created_on_date_is_visible(self) -> None:
        """Verifies that the specified date is visible on the page
        Args:
            date (str): The date to verify, formatted as 'dd/mm/yyyy'.
        """
        today = DateTimeUtils.current_datetime("%d/%m/%Y")
        expect(self.created_on_date_locator).to_have_text(today)

    def verify_created_on_date_is_not_visible(self) -> None:
        """Verifies that the 'created on' date element is not visible on the page.
        This is used to confirm that the non-invitation day has been successfully deleted.
        """
        expect(self.created_on_date_locator).not_to_be_visible
