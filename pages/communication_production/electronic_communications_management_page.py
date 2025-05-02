from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ElectronicCommunicationManagementPage(BasePage):
    """Electronic Communication Management Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Electronic Communication Management - page locators
        self.electronic_communication_management_title = self.page.locator(
            "#page-title"
        )

    def verify_electronic_communication_management_title(self) -> None:
        """Verify the Electronic Communication Management page title is displayed as expected"""
        expect(self.electronic_communication_management_title).to_contain_text(
            "Electronic Communication Management"
        )
