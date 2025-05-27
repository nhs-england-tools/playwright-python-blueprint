from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class KitServiceManagementPage(BasePage):
    """Kit Service Management Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # KIT Service Management - page locators, methods

    def verify_kit_service_management_title(self) -> None:
        """Verifies that the Kit Service Management page title is displayed correctly."""
        self.bowel_cancer_screening_page_title_contains_text("Kit Service Management")
