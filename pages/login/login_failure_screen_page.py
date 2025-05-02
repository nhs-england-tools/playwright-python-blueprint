from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoginFailureScreenPage(BasePage):
    """Login Failure Screen Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Login failure message
        self.login_failure_msg = self.page.get_by_role(
            "heading", name="Sorry, BCSS is unavailable"
        )

    def verify_login_failure_screen_is_displayed(self) -> None:
        """Verifies that the login failure screen is displayed."""
        expect(self.login_failure_msg).to_be_visible()
