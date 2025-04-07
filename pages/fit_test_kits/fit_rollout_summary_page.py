from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class FITRolloutSummary(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # FIT Rollout Summary - page locators
        self.fit_rollout_summary_body = self.page.locator("body")

    def verify_fit_rollout_summary_body(self) -> None:
        expect(self.fit_rollout_summary_body).to_contain_text("FIT Rollout Summary")
