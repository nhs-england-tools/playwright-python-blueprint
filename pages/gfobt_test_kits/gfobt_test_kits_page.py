from playwright.sync_api import Page
from pages.base_page import BasePage


class GFOBTTestKits(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

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
        self.click(self.test_kit_logging_page)

    def go_to_test_kit_reading_page(self) -> None:
        self.click(self.test_kit_reading_page)

    def go_to_test_kit_result_page(self) -> None:
        self.click(self.test_kit_reading_page)

    def go_to_create_qc_kit_page(self) -> None:
        self.click(self.create_qc_kit_page)
