from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class GFOBTTestKitLoggingPage(BasePage):
    """GFOBT Test Kit Logging Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    def verify_test_kit_logging_title(self) -> None:
        """Verify the title of the GFOBT Test Kit Logging page."""
        self.bowel_cancer_screening_page_title_contains_text("Test Kit Logging")
