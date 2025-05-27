from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class MaintainContactsPage(BasePage):
    """Maintain Contacts Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Maintain Contacts - page locators, methods

    def verify_maintain_contacts_title(self) -> None:
        """Verify the Maintain Contacts page title is displayed correctly"""
        self.bowel_cancer_screening_page_title_contains_text("Maintain Contacts")
