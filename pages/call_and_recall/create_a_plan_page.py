from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class CreateAPlanPage(BasePage):
    """Create a Plan page locators and methods to interact with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Call and Recall - page links
        self.set_all_button = self.page.get_by_role("link", name="Set all")
        self.daily_invitation_rate_field = self.page.get_by_placeholder(
            "Enter daily invitation rate"
        )
        self.weekly_invitation_rate_field = self.page.get_by_placeholder(
            "Enter weekly invitation rate"
        )
        self.update_button = self.page.get_by_role("button", name="Update")
        self.confirm_button = self.page.get_by_role("button", name="Confirm")
        self.save_button = self.page.get_by_role("button", name="Save")
        self.note_field = self.page.get_by_placeholder("Enter note")
        self.save_note_button = self.page.locator("#saveNote").get_by_role(
            "button", name="Save"
        )
        self.create_a_plan_title = self.page.locator("#page-title")

    def click_set_all_button(self) -> None:
        """Clicks the Set all button to set all values"""
        self.click(self.set_all_button)

    def fill_daily_invitation_rate_field(self, value: str) -> None:
        """Fills the daily invitation rate field with the given value"""
        self.daily_invitation_rate_field.fill(value)

    def fill_weekly_invitation_rate_field(self, value) -> None:
        """Fills the weekly invitation rate field with the given value"""
        self.weekly_invitation_rate_field.fill(value)

    def click_update_button(self) -> None:
        """Clicks the Update button to save any changes"""
        self.click(self.update_button)

    def click_confirm_button(self) -> None:
        """Clicks the Confirm button"""
        self.click(self.confirm_button)

    def click_save_button(self) -> None:
        """Clicks the Save button"""
        self.click(self.save_button)

    def fill_note_field(self, value) -> None:
        """Fills the note field with the given value"""
        self.note_field.fill(value)

    def click_save_note_button(self) -> None:
        """Clicks the Save note button"""
        self.click(self.save_note_button)

    def verify_create_a_plan_title(self) -> None:
        """Verifies the Create a Plan page title"""
        expect(self.create_a_plan_title).to_contain_text("View a plan")
