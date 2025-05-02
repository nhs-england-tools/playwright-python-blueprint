from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class FITRolloutSummaryPage(BasePage):
    """FIT Rollout Summary Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # FIT Rollout Summary - page locators
        self.fit_rollout_summary_body = self.page.locator("body")

    def verify_fit_rollout_summary_body(self) -> None:
        """Verifies that the FIT Rollout Summary page body is displayed correctly."""
        expect(self.fit_rollout_summary_body).to_contain_text("FIT Rollout Summary")
