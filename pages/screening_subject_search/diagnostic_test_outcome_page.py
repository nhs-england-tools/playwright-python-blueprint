from playwright.sync_api import Page, expect, Locator
from pages.base_page import BasePage
from enum import StrEnum


class DiagnosticTestOutcomePage(BasePage):
    """Diagnostic Test Outcome Page locators and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Diagnostic Test Outcome- page locators
        self.test_outcome_dropdown = self.page.get_by_label(
            "Outcome of Diagnostic Test"
        )
        self.save_button = self.page.get_by_role("button", name="Save")

    def verify_diagnostic_test_outcome(self, outcome_name: str) -> None:
        """
        Verify that the diagnostic test outcome is visible.

        Args:
            outcome_name (str): The accessible name or visible text of the test outcome cell to verify.
        """
        expect(self.page.get_by_role("cell", name=outcome_name).nth(1)).to_be_visible()

    def select_test_outcome_option(self, option: str) -> None:
        """Select an option from the Outcome of Diagnostic Test dropdown.

        Args:
            option (str): option (str): The option to select from the Outcome Of Diagnostic Test options.
        """
        self.test_outcome_dropdown.select_option(option)

    def click_save_button(self) -> None:
        """Click the 'Save' button."""
        self.click(self.save_button)


class OutcomeOfDiagnosticTest(StrEnum):
    """Enum for outcome of diagnostic test options."""

    FAILED_TEST_REFER_ANOTHER = "20363"
    REFER_SYMPTOMATIC = "20366"
    REFER_SURVEILLANCE = "20365"
    INVESTIGATION_COMPLETE = "20360"
