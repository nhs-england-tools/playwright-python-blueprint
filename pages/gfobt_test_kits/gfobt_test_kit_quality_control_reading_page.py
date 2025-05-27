from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class GFOBTTestKitQualityControlReadingPage(BasePage):
    """GFOBT Test Kit Quality Control Reading Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    def verify_test_kit_logging_tile(self) -> None:
        """Verify the title of the GFOBT Test Kit Quality Control Reading page."""
        self.bowel_cancer_screening_page_title_contains_text(
            "Test Kit Quality Control Reading"
        )
