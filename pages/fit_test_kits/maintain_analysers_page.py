from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class MaintainAnalysers(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Maintain Analysers - page locators
        self.maintain_analysers_title = self.page.locator("#ntshPageTitle")

    def verify_maintain_analysers_title(self) -> None:
        expect(self.maintain_analysers_title).to_contain_text("Maintain Analysers")
