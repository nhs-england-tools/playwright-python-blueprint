from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class TestKitQualityControlReading(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.test_kit_quality_control_reading_title = self.page.locator(
            "#ntshPageTitle"
        )

    def verify_test_kit_logging_tile(self) -> None:
        expect(self.test_kit_quality_control_reading_title).to_contain_text(
            "Test Kit Quality Control Reading"
        )
