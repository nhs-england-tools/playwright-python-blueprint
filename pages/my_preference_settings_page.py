from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class MyPreferenceSettings(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        #My Preference Settings - page locators
        self.my_preference_settings_title = self.page.locator("#ntshPageTitle")

    def verify_my_preference_settings_title(self) -> None:
        expect(self.my_preference_settings_title).to_contain_text("My Preference Settings")
