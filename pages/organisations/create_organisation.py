import logging
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class CreateOrganisation(BasePage):
    """Create Organisation Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # Create Organisation links
        self.organisation_code = self.page.get_by_label("Organisation Code*")
        self.organisation_name = self.page.get_by_label("Organisation Name*")
        self.start_date_calendar = self.page.locator("#UI_START_DATE_LinkOrButton")
        self.audit_reason = self.page.get_by_label("Audit Reason*")
        self.date_of_diagnosis_textbox = self.page.get_by_role(
            "textbox", name="Date of Diagnosis"
        )
        self.save_button = self.page.get_by_role("button", name="Save")

    def fill_organisation_code(self, text: str) -> None:
        """
        This method is designed to fill in the Organisation Code field on the Create Organisation page.
        Args:
        text (str): The organisation code to be entered. Example: "Z9Z1S"
        """
        logging.info("Filling Organisation Code on Create Organisation page")
        self.organisation_code.fill(text)

    def fill_organisation_name(self, text: str) -> None:
        """
        This method is designed to fill in the Organisation Name field on the Create Organisation page.
        Args:
        text (str): The organisation name to be entered. Example: "Test ANANA ICB"
        """
        logging.info("Filling Organisation Name on Create Organisation page")
        self.organisation_name.fill(text)

    def click_start_date_calendar(self) -> None:
        """
        This method is designed to click the Start Date Calendar button on the Create Organisation page.
        """
        logging.info("Clicking Start Date Calendar on Create Organisation page")
        self.click(self.start_date_calendar)

    def fill_audit_reason(self, text: str) -> None:
        """
        This method is designed to fill in the Audit Reason field on the Create Organisation page.
        Args:
        text (str): The audit reason to be entered. Example: "Automated ANANA Test"
        """
        logging.info("Filling Audit Reason on Create Organisation page")
        self.audit_reason.fill(text)

    def click_save_button(self) -> None:
        """
        This method is designed to click the Save button on the Create Organisation page.
        """
        logging.info("Clicking Save button on Create Organisation page")
        self.click(self.save_button)

    def verify_success_message(self) -> None:
        """Verifies that the success message is displayed after saving the organisation."""
        logging.info("Verifying success message on Create Organisation page")
        expect(self.page.locator("th")).to_contain_text(
            "The action was performed successfully"
        )
