from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class KitServiceManagement(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # KIT Service Management - page locators
        self.kit_service_management_title = self.page.locator("#page-title")

    def verify_kit_service_management_title(self) -> None:
        expect(self.kit_service_management_title).to_contain_text(
            "Kit Service Management"
        )
