from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class SetLynchInvitationRatesPage(BasePage):
    """Set Lynch Invitation Rates Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Lynch Invitation Page - Links, methods

    def verify_set_lynch_invitation_rates_title(self) -> None:
        """Verifies that the Set Lynch Invitation Rates title is displayed."""
        self.bowel_cancer_screening_page_title_contains_text(
            "Set Lynch Surveillance Invitation Rates"
        )
