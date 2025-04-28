from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class GFOBTTestKitLogging(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.test_kit_logging_title = self.page.locator("#ntshPageTitle")

    def verify_test_kit_logging_title(self) -> None:
        expect(self.test_kit_logging_title).to_contain_text("Test Kit Logging")
