from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class NonInvitationDaysPage(BasePage):
    """Non Invitation Days page locators, and methods to interact with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Non Invitation Days - page locators, methods

    def verify_non_invitation_days_tile(self) -> None:
        """Verifies the page title of the Non Invitation Days page"""
        self.bowel_cancer_screening_page_title_contains_text("Non-Invitation Days")
