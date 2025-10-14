from playwright.sync_api import Page
from pages.base_page import BasePage


class GFOBTTestKitsPage(BasePage):
    """GFOBT Test Kits Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.test_kits_header = self.page.get_by_text("gFOBT Test Kits")
        self.test_kit_logging_page = self.page.get_by_role(
            "link", name="Test Kit Logging"
        )
        self.test_kit_reading_page = self.page.get_by_role(
            "link", name="Test Kit Reading"
        )
        self.test_kit_result_page = self.page.get_by_role(
            "link", name="View Test Kit Result"
        )
        self.create_qc_kit_page = self.page.get_by_role("link", name="Create QC Kit")

    def go_to_test_kit_logging_page(self) -> None:
        """Navigate to the Test Kit Logging page."""
        self.click(self.test_kit_logging_page)

    def go_to_test_kit_reading_page(self) -> None:
        """Navigate to the Test Kit Reading page."""
        self.click(self.test_kit_reading_page)

    def go_to_test_kit_result_page(self) -> None:
        """Navigate to the View Test Kit Result page."""
        self.click(self.test_kit_result_page)

    def go_to_create_qc_kit_page(self) -> None:
        """Navigate to the Create QC Kit page."""
        self.click(self.create_qc_kit_page)

    def open_test_kits_report(self) -> None:
        """Clicks the 'Test Kits' header to open the corresponding report section."""
        self.click(self.test_kits_header)


