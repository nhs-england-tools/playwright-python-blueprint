from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class AgeExtensionRolloutPlansPage(BasePage):
    """Age Extension Rollout Plans page locators, and methods to interact with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Age Extension Rollout Plans - page locators
        self.age_extension_rollout_plans_title = self.page.locator("#page-title")

    def verify_age_extension_rollout_plans_title(self) -> None:
        """Verifies the page title of the Age Extension Rollout Plans page"""
        expect(self.age_extension_rollout_plans_title).to_contain_text(
            "Age Extension Rollout Plans"
        )
