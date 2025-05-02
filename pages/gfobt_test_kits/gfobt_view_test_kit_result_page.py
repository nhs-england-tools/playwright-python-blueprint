from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ViewTestKitResultPage(BasePage):
    """View Test Kit Result Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.view_test_kit_result_title = self.page.locator("#ntshPageTitle")

    def verify_view_test_kit_result_title(self) -> None:
        """Verify the title of the View Test Kit Result page."""
        expect(self.view_test_kit_result_title).to_contain_text("View Test Kit Result")
