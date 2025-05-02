from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class MaintainContactsPage(BasePage):
    """Maintain Contacts Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Maintain Contacts - page locators
        self.maintain_contacts_title = self.page.locator("#ntshPageTitle")

    def verify_maintain_contacts_title(self) -> None:
        """Verify the Maintain Contacts page title is displayed correctly"""
        expect(self.maintain_contacts_title).to_contain_text("Maintain Contacts")
