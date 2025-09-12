import logging
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class CreateSite(BasePage):
    """Create Site Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # Create Site links
        self.site_code = self.page.get_by_label("Site Code*")
        self.site_name = self.page.get_by_label("Site Name*")
        self.start_date_calendar = self.page.locator("#START_DATE_LinkOrButton")
        self.audit_reason = self.page.get_by_label("Audit Reason*")
        self.save_button = self.page.get_by_role("button", name="Save")

    def fill_site_code(self, text: str) -> None:
        """
        This method is designed to fill in the site Code field on the Create site page.
        Args:
            text (str): The site code to be entered. Example: "Z9Z1X"
        """
        logging.info("Filling Site Code on Create site page")
        self.site_code.fill(text)

    def fill_site_name(self, text: str) -> None:
        """
        This method is designed to fill in the Site Name field on the Create Site page.
        Args:
            text (str): The site name to be entered. Example: "TEST ANANA NHS TRUST SITE"
        """
        logging.info("Filling Site Name on Create Site page")
        self.site_name.fill(text)

    def click_start_date_calendar(self) -> None:
        """
        This method is designed to click the Start Date Calendar button on the Create Site page.
        """
        logging.info("Clicking Start Date Calendar on Create Site page")
        self.click(self.start_date_calendar)

    def fill_audit_reason(self, text: str) -> None:
        """
        This method is designed to fill in the Audit Reason field on the Create Site page.
        Args:
            text (str): The audit reason to be entered. Example: "Automated ANANA Test"
        """
        logging.info("Filling Audit Reason on Create Site page")
        self.audit_reason.fill(text)

    def click_save_button(self) -> None:
        """
        This method is designed to click the Save button on the Create Site page.

        """
        logging.info("Clicking Save button on Create Site page")
        self.click(self.save_button)

    def verify_success_message(self) -> None:
        """Verifies that the success message is displayed after saving the Site."""
        logging.info("Verifying success message on Create Site page")
        expect(self.page.locator("th")).to_contain_text(
            "The action was performed successfully"
        )
