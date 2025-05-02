from playwright.sync_api import Page, expect
import logging
from pages.base_page import BasePage


class LogoutPage(BasePage):
    """Logout locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Logout page locators
        self.log_out_msg = self.page.get_by_role("heading", name="You have logged out")

    def verify_log_out_page(self) -> None:
        """Verifies that the logout message is displayed."""
        expect(self.log_out_msg).to_be_visible()

    def log_out(self, close_page: bool = True) -> None:
        """Logs out of the application and verifies the logout message is displayed."""
        logging.info("Logging Out")
        self.click_log_out_link()
        expect(self.log_out_msg).to_be_visible()
        if close_page:
            self.page.close()
