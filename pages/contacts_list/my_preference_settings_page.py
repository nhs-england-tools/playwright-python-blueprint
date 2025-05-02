from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class MyPreferenceSettingsPage(BasePage):
    """My Preference Settings Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # My Preference Settings - page locators
        self.my_preference_settings_title = self.page.locator("#ntshPageTitle")

    def verify_my_preference_settings_title(self) -> None:
        """Verify the My Preference Settings page title is displayed correctly"""
        expect(self.my_preference_settings_title).to_contain_text(
            "My Preference Settings"
        )
