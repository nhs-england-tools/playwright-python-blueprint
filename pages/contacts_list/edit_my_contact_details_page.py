from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class EditMyContactDetailsPage(BasePage):
    """Edit My Contact Details Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Edit My Contact Details - page locators
        self.edit_my_contact_details_title = self.page.locator("#ntshPageTitle")

    def verify_edit_my_contact_details_title(self) -> None:
        """Verify the Edit My Contact Details page title is displayed correctly"""
        expect(self.edit_my_contact_details_title).to_contain_text(
            "Edit My Contact Details"
        )
