from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ElectronicCommunicationManagement(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Electronic Communication Management - page locators
        self.electronic_communication_management_title = self.page.locator(
            "#page-title"
        )

    def verify_electronic_communication_management_title(self) -> None:
        expect(self.electronic_communication_management_title).to_contain_text(
            "Electronic Communication Management"
        )
