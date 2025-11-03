import logging
from click import option
from playwright.sync_api import Page, expect, Locator
from pages.base_page import BasePage
from enum import StrEnum


class ReferralProcedureType(StrEnum):
    ENDOSCOPIC = "20356"
    RADIOLOGICAL = "20357"


class ReasonForOnwardReferral(StrEnum):
    CURRENTLY_UNSUITABLE_FOR_ENDOSCOPIC_REFERRAL = "20358"
    FURTHER_CLINICAL_ASSESSMENT = "20359"
    INCOMPLETE_COLONIC_VISUALISATION = "20481"
    POLYP_EXCISION = "203011"
    CORRECTIVE_SURGERY = "203012"
    SUSPECTED_CANCER_SURGERY = "203013"


class DiagnosticTestOutcomePage(BasePage):
    """Diagnostic Test Outcome Page locators and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Diagnostic Test Outcome- page locators
        self.test_outcome_dropdown = self.page.get_by_label(
            "Outcome of Diagnostic Test"
        )
        self.reason_for_sympptomatic_referral_dropdown = self.page.get_by_label(
            "Reason for Symptomatic Referral"
        )
        self.save_button = self.page.get_by_role("button", name="Save")
        self.referral_procedure_dropdown = self.page.locator(
            "#UI_REFERRAL_PROCEDURE_TYPE"
        )
        self.reason_for_onward_referral_dropdown = self.page.locator("#UI_COMPLETE_ID")
        self.visible_ui_results_string = 'select[id^="UI_RESULTS_"]:visible'
        self.onward_referring_clinician_lookup_link = self.page.locator(
            "#UI_CONSULTANT_PIO_SELECT_LINK"
        )

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

    def verify_reason_for_symptomatic_referral(self, symptomatic_reason: str) -> None:
        """
        Verify reason for symptomatic referral is visible.

        Args:
            symptomatic_reason(str): The accessible name or visible text of the symptomatic reason cell to verify.
        """
        expect(
            self.page.get_by_role("cell", name=symptomatic_reason).nth(1)
        ).to_be_visible()

    def select_reason_for_symptomatic_referral_option(self, option: str) -> None:
        """Select an option from the reason for symptomatic referral dropdown.

        Args:
            option (str): option (str): The option to select from the Reason For Symptomatic Referral options.
        """
        self.reason_for_sympptomatic_referral_dropdown.select_option(option)

    def click_save_button(self) -> None:
        """Click the 'Save' button."""
        self.click(self.save_button)

    def select_referral_procedure_type(self, value: ReferralProcedureType) -> None:
        """Select Radiological or Endoscopic Referral value."""
        self.referral_procedure_dropdown.wait_for(state="visible")
        self.referral_procedure_dropdown.select_option(value=value)

    def select_reason_for_onward_referral(self, value: ReasonForOnwardReferral) -> None:
        """Select Reason for Onward Referral value."""
        self.reason_for_onward_referral_dropdown.wait_for(state="visible")
        self.reason_for_onward_referral_dropdown.select_option(value=value)

    def select_valid_onward_referral_consultant_index(self, option: int) -> None:
        """Selects the first valid consultant from the lookup dropdown inside the iframe."""
        self.click(self.onward_referring_clinician_lookup_link)
        select_locator = self.page.locator(self.visible_ui_results_string)
        select_locator.first.wait_for(state="visible")
        # Find all option elements inside the select and click the one at the given index
        option_elements = select_locator.first.locator("option")
        option_elements.nth(option).wait_for(state="visible")
        self.click(option_elements.nth(option))


class OutcomeOfDiagnosticTest(StrEnum):
    """Enum for outcome of diagnostic test options."""

    FAILED_TEST_REFER_ANOTHER = "20363"
    REFER_SYMPTOMATIC = "20366"
    REFER_SURVEILLANCE = "20365"
    INVESTIGATION_COMPLETE = "20360"
    REFER_ANOTHER_DIAGNOSTIC_TEST = "20364"


class ReasonForSymptomaticReferral(StrEnum):
    """Enum for Symptomatic Referral reason options."""

    POLYP_EXCISION = "203011"
    CORRECTIVE_SURGERY = "203012"
    SUSPECTED_CANCER_SURGERY = "203013"
