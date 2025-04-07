from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ViewAlgorithms(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # View Algorithms - page locators
        self.view_algorithms_body = self.page.locator("body")

    def verify_view_algorithms_body(self) -> None:
        expect(self.view_algorithms_body).to_contain_text("Select Algorithm")
