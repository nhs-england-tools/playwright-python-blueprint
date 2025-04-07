from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class MaintainContacts(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Maintain Contacts - page locators
        self.maintain_contacts_title = self.page.locator("#ntshPageTitle")

    def verify_maintain_contacts_title(self) -> None:
        expect(self.maintain_contacts_title).to_contain_text("Maintain Contacts")
