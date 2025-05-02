from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class KitServiceManagementPage(BasePage):
    """Kit Service Management Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # KIT Service Management - page locators
        self.kit_service_management_title = self.page.locator("#page-title")

    def verify_kit_service_management_title(self) -> None:
        """Verifies that the Kit Service Management page title is displayed correctly."""
        expect(self.kit_service_management_title).to_contain_text(
            "Kit Service Management"
        )
