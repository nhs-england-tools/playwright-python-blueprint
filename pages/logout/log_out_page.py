from playwright.sync_api import Page, expect
import logging
from pages.base_page import BasePage


class Logout(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Call and Recall - page links
        self.log_out_msg = self.page.get_by_role("heading", name="You have logged out")

    def verify_log_out_page(self) -> None:
        expect(self.log_out_msg).to_be_visible()

    def log_out(self) -> None:
        logging.info("Test Complete - Logging Out")
        self.click_log_out_link()
        expect(self.log_out_msg).to_be_visible()
        self.page.close()
