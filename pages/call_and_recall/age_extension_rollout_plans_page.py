from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class AgeExtensionRolloutPlansPage(BasePage):
    """Age Extension Rollout Plans page locators, and methods to interact with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Age Extension Rollout Plans - page locators, methods

    def verify_age_extension_rollout_plans_title(self) -> None:
        """Verifies the page title of the Age Extension Rollout Plans page"""
        self.bowel_cancer_screening_page_title_contains_text(
            "Age Extension Rollout Plans"
        )
