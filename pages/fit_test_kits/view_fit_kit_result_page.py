from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ViewFITKitResult(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # View FIT Kit Result - page locators
        self.view_fit_kit_result_body = self.page.locator("body")

    def verify_view_fit_kit_result_body(self) -> None:
        expect(self.view_fit_kit_result_body).to_contain_text("View FIT Kit Result")
