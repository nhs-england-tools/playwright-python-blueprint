from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ViewContacts(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # View Contacts - page locators
        self.view_contacts_title = self.page.locator("#ntshPageTitle")

    def verify_view_contacts_title(self) -> None:
        expect(self.view_contacts_title).to_contain_text("View Contacts")
