from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class EditMyContactDetails(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Edit My Contact Details - page locators
        self.edit_my_contact_details_title = self.page.locator("#ntshPageTitle")

    def verify_edit_my_contact_details_title(self) -> None:
        expect(self.edit_my_contact_details_title).to_contain_text(
            "Edit My Contact Details"
        )
