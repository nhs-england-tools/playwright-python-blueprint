from playwright.sync_api import Page, expect, Locator
from pages.base_page import BasePage
import logging
import pytest


class AdvanceFOBTScreeningEpisodePage(BasePage):
    """Advance FOBT Screening Episode Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Advance FOBT Screening Episode - page locators
        self.suitable_for_endoscopic_test_button = self.page.get_by_role(
            "button", name="Suitable for Endoscopic Test"
        )
        self.calendar_button = self.page.get_by_role("button", name="Calendar")
        self.test_type_dropdown = self.page.locator("#UI_EXT_TEST_TYPE_2233")
        self.test_type_dropdown_2 = self.page.locator("#UI_EXT_TEST_TYPE_4325")
        self.advance_checkbox = self.page.get_by_label(
            "There are some events available which should only be used in exceptional circumstances. If you wish to see them, check this box"
        )
        self.invite_for_diagnostic_test_button = self.page.get_by_role(
            "button", name="Invite for Diagnostic Test >>"
        )
        self.attend_diagnostic_test_button = self.page.get_by_role(
            "button", name="Attend Diagnostic Test"
        )
        self.other_post_investigation_button = self.page.get_by_role(
            "button", name="Other Post-investigation"
        )
        self.record_other_post_investigation_contact_button = self.page.get_by_role(
            "button", name="Record other post-"
        )
        self.enter_diagnostic_test_outcome_button = self.page.get_by_role(
            "button", name="Enter Diagnostic Test Outcome"
        )
        self.handover_into_symptomatic_care_button = self.page.get_by_role(
            "button", name="Handover into Symptomatic Care"
        )
        self.record_diagnosis_date_button = self.page.get_by_role(
            "button", name="Record Diagnosis Date"
        )
        self.record_contact_with_patient_button = self.page.get_by_role(
            "button", name="Record Contact with Patient"
        )
        self.amend_diagnosis_date_button = self.page.get_by_role(
            "button", name="Amend Diagnosis Date"
        )
        self.advance_checkbox_v2 = self.page.get_by_role("checkbox")
        self.subsequent_assessment_appointment_required_dropdown = (
            self.page.get_by_role("combobox")
        )
        self.subsequent_assessment_appointment_required_button = self.page.get_by_role(
            "button", name="Subsequent Assessment Appointment Required"
        )
        self.suitable_for_radiological_test_button = self.page.get_by_role(
            "button", name="Suitable for Radiological Test"
        )
        self.decision_not_to_continue_with_diagnostic_test_button = (
            self.page.get_by_role(
                "button", name="Decision not to Continue with Diagnostic Test"
            )
        )
        self.waiting_decision_to_proceed_with_diagnostic_test_button = (
            self.page.get_by_role(
                "button", name="Waiting Decision to Proceed with Diagnostic Test"
            )
        )
        self.not_suitable_for_diagnostic_tests_button = self.page.get_by_role(
            "button", name="Not Suitable for Diagnostic Tests"
        )

    def click_suitable_for_endoscopic_test_button(self) -> None:
        """Click the 'Suitable for Endoscopic Test' button."""
        self.safe_accept_dialog(self.suitable_for_endoscopic_test_button)

    def click_calendar_button(self) -> None:
        """Click the calendar button to open the calendar picker."""
        self.click(self.calendar_button)

    def select_test_type_dropdown_option(self, text: str) -> None:
        """Select the test type from the dropdown."""
        self.test_type_dropdown.select_option(label=text)

    def select_test_type_dropdown_option_2(self, text: str) -> None:
        """Select the test type from the dropdown."""
        self.test_type_dropdown_2.select_option(label=text)

    def click_invite_for_diagnostic_test_button(self) -> None:
        """Click the 'Invite for Diagnostic Test' button."""
        self.safe_accept_dialog(self.invite_for_diagnostic_test_button)

    def click_attend_diagnostic_test_button(self) -> None:
        """Click the 'Attend Diagnostic Test' button."""
        self.click(self.attend_diagnostic_test_button)

    def click_other_post_investigation_button(self) -> None:
        """Click the 'Other Post-investigation' button."""
        self.safe_accept_dialog(self.other_post_investigation_button)

    def get_latest_event_status_cell(self, latest_event_status: str) -> Locator:
        """Get the cell containing the latest event status."""
        return self.page.get_by_role("cell", name=latest_event_status, exact=True)

    def verify_latest_event_status_value(self, latest_event_status: str) -> None:
        """Verify that the latest event status value is visible."""
        logging.info(f"Verifying subject has the status: {latest_event_status}")
        latest_event_status_cell = self.get_latest_event_status_cell(
            latest_event_status
        )
        try:
            expect(latest_event_status_cell).to_be_visible()
            logging.info(f"Subject has the status: {latest_event_status}")
        except Exception:
            pytest.fail(f"Subject does not have the status: {latest_event_status}")

    def click_record_other_post_investigation_contact_button(self) -> None:
        """Click the 'Record other post-investigation contact' button."""
        self.click(self.record_other_post_investigation_contact_button)

    def click_enter_diagnostic_test_outcome_button(self) -> None:
        """Click the 'Enter Diagnostic Test Outcome' button."""
        self.click(self.enter_diagnostic_test_outcome_button)

    def click_handover_into_symptomatic_care_button(self) -> None:
        """Click the 'Handover Into Symptomatic Care' button."""
        self.click(self.handover_into_symptomatic_care_button)

    def click_record_diagnosis_date_button(self) -> None:
        """Click the 'Record Diagnosis Date' button."""
        self.click(self.record_diagnosis_date_button)

    def click_record_contact_with_patient_button(self) -> None:
        """Click the 'Record Contact with Patient' button."""
        self.click(self.record_contact_with_patient_button)

    def check_advance_checkbox(self) -> None:
        """Selects the 'Advance FOBT' checkbox"""
        self.advance_checkbox.check()

    def click_amend_diagnosis_date_button(self) -> None:
        """Checks the 'Advance FOBT' checkbox and clicks the 'Amend Diagnosis Date' button."""
        self.advance_checkbox_v2.check()
        self.click(self.amend_diagnosis_date_button)

    def click_and_select_subsequent_assessment_appointment_required(
        self, option: str
    ) -> None:
        """
        Click the 'Subsequent Assessment Appointment Required' button and select an option from the dropdown.
        Args:
            option (str): The option to select from the dropdown.
            Must be one of:
                - 'Previous attendance, further assessment required'
                - 'Interpreter requirement not identified'
                - 'SC interpreter DNA'
        """
        self.subsequent_assessment_appointment_required_dropdown.select_option(
            label=option
        )
        self.safe_accept_dialog(self.subsequent_assessment_appointment_required_button)

    def click_suitable_for_radiological_test_button(self) -> None:
        """Click the 'Suitable for Radiological Test' button."""
        self.safe_accept_dialog(self.suitable_for_radiological_test_button)

    def click_decision_not_to_continue_with_diagnostic_test(self) -> None:
        """Click the 'Decision not to Continue with Diagnostic Test' button."""
        self.safe_accept_dialog(
            self.decision_not_to_continue_with_diagnostic_test_button
        )

    def click_waiting_decision_to_proceed_with_diagnostic_test(self) -> None:
        """Click the 'Waiting Decision to Proceed with Diagnostic Test' button."""
        self.safe_accept_dialog(
            self.waiting_decision_to_proceed_with_diagnostic_test_button
        )

    def click_not_suitable_for_diagnostic_tests_button(self) -> None:
        """Click the 'Not Suitable for Diagnostic Tests' button."""
        self.safe_accept_dialog(self.not_suitable_for_diagnostic_tests_button)
