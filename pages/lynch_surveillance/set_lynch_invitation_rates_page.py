from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class SetLynchInvitationRatesPage(BasePage):
    """Set Lynch Invitation Rates Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Lynch Invitation Page - Links
        self.set_lynch_invitation_rates_title = self.page.locator("#page-title")

    def verify_set_lynch_invitation_rates_title(self) -> None:
        """Verifies that the Set Lynch Invitation Rates title is displayed."""
        expect(self.set_lynch_invitation_rates_title).to_contain_text(
            "Set Lynch Surveillance Invitation Rates"
        )
