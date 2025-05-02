from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ViewFITKitResultPage(BasePage):
    """View FIT Kit Result page locators and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # View FIT Kit Result - page locators
        self.view_fit_kit_result_body = self.page.locator("body")

    def verify_view_fit_kit_result_body(self) -> None:
        """Verify the View FIT Kit Result page body contains text "View FIT Kit Result"."""
        expect(self.view_fit_kit_result_body).to_contain_text("View FIT Kit Result")
