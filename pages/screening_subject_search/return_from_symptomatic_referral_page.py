from playwright.sync_api import Page
from pages.base_page import BasePage


class ReturnFromSymptomaticReferralPage(BasePage):
    """Return From Symptomatic Referral Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        # Return From Symptomatic Referral - page locators
        self.radiological_or_endoscopic_referral_dropdown = self.page.locator(
            "#referralTypeId"
        )
        self.reason_for_onward_referral_dropdown = self.page.locator(
            "#referralReasonId"
        )
        self.save_button = self.page.get_by_role("button", name="Save")

    def select_radiological_or_endoscopic_referral_option(
        self, referral_type: str
    ) -> None:
        """
        Select a radiological or endoscopic referral from the dropdown.
        Args:
            referral_type (str): The referral type to be selected in the dropdown. Example: "Colonoscopy"
        """
        self.radiological_or_endoscopic_referral_dropdown.select_option(
            label=referral_type
        )

    def select_reason_for_onward_referral_option(
        self, reason_for_referral: str
    ) -> None:
        """
        Select a reason for onward referral from the dropdown.
        Args:
            reason_for_referral (str): The reason for onward referral to be selected in the dropdown. Example: "Further Clinical Assessment"
        """
        self.reason_for_onward_referral_dropdown.select_option(
            label=reason_for_referral
        )

    def click_save_button(self) -> None:
        """Click the 'Save' button."""
        self.click(self.save_button)
