from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class MyPreferenceSettingsPage(BasePage):
    """My Preference Settings Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # My Preference Settings - page locators, methods

    def verify_my_preference_settings_title(self) -> None:
        """Verify the My Preference Settings page title is displayed correctly"""
        self.bowel_cancer_screening_page_title_contains_text(
            "My Preference Settings"
        )
