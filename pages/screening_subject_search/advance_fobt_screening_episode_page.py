from datetime import date, datetime
from playwright.sync_api import Page, expect, Locator, Dialog
from pages.base_page import BasePage
import logging
from typing import List
from utils.calendar_picker import CalendarPicker
from enum import Enum


class ContactDirection(Enum):
    TO_PATIENT = "20159"
    FROM_PATIENT = "20160"


class ContactMethod(Enum):
    IN_PERSON = "16028"
    TELEPHONE = "16029"
    VISIT = "16030"
    LETTER = "20012"


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
        self.test_type_dropdown = self.page.locator("[id^='UI_EXT_TEST_TYPE_']")
        self.advance_checkbox_label = self.page.get_by_label(
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
        self.advance_checkbox_label_v2 = self.page.get_by_role("checkbox")
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
        self.cancel_diagnostic_test_button = self.page.get_by_role(
            "button", name="Cancel Diagnostic Test"
        )
        self.post_investigation_appointment_required_button = self.page.get_by_role(
            "button", name="Post-investigation Appointment Required"
        )
        self.redirect_to_delete_the_latest_diagnostic_test_result_button = (
            self.page.get_by_role("button", name="Redirect to DELETE the Latest")
        )
        self.redirect_to_reestablish_suitability_for_diagnostic_test_repatient_contact = self.page.get_by_role(
            "button", name="Redirect to re-establish"
        )
        # Contact recording locators
        self.contact_direction_dropdown = self.page.get_by_label("Contact Direction")
        self.contact_made_between_dropdown = self.page.get_by_label(
            "Contact made between patient and"
        )
        self.contact_method_dropdown = self.page.get_by_label("Contact Method")
        self.call_date_input = self.page.locator("#UI_CALL_DATE")
        self.start_time_input = self.page.locator("#UI_START_TIME")
        self.end_time_input = self.page.locator("#UI_END_TIME")
        self.duration_input = self.page.locator("#UI_DURATION")
        self.note_input = self.page.get_by_text("(up to 500 char)")
        self.patient_contacted_dropdown = self.page.get_by_label("Patient Contacted")
        self.outcome_dropdown = self.page.get_by_label("Outcome")
        self.save_button = self.page.locator("input[name='UI_BUTTON_SAVE']")
        # CT Colonography invitation locators
        self.ct_colonography_appointment_date_input = self.page.locator(
            "#UI_APPT_DATE_38"
        )
        self.ct_colonography_test_type_dropdown = self.page.locator(
            "#UI_EXT_TEST_TYPE_38"
        )
        self.invite_for_diagnostic_test_button = self.page.get_by_role(
            "button", name="Invite for Diagnostic Test >>"
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
        logging.info(
            f"[UI ASSERTION] Verifying subject has the status: {latest_event_status}"
        )
        latest_event_status_cell = self.get_latest_event_status_cell(
            latest_event_status
        )
        try:
            expect(latest_event_status_cell).to_be_visible()
            logging.info(
                f"[UI ASSERTION COMPLETE] Subject has the status: {latest_event_status}"
            )
        except Exception:
            raise AssertionError(
                f"[UI ASSERTION FAILED] Subject does not have the status: {latest_event_status}"
            )

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
        self.advance_checkbox_label.check()

    def click_amend_diagnosis_date_button(self) -> None:
        """Checks the 'Advance FOBT' checkbox and clicks the 'Amend Diagnosis Date' button."""
        self.advance_checkbox_label_v2.check()
        self.click(self.amend_diagnosis_date_button)

    def check_exception_circumstances_checkbox(self) -> None:
        """Checks the 'Exceptional circumstances' checkbox"""
        self.advance_checkbox_label_v2.check()

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

    def select_ct_colonography_and_invite(self) -> None:
        """
        Enters today's date, selects 'CT Colonography' as the diagnostic test type,
        and clicks the 'Invite for Diagnostic Test' button.
        """
        logging.info(
            "[ADVANCE EPISODE] Selecting CT Colonography and inviting for diagnostic test"
        )

        # Step 1: Enter today's date
        today = date.today().strftime("%d/%m/%Y")
        self.ct_colonography_appointment_date_input.fill(today)
        logging.info(f"[ADVANCE EPISODE] Entered appointment date: {today}")

        # Step 2: Select 'CT Colonography' from dropdown
        self.ct_colonography_test_type_dropdown.select_option(label="CT Colonography")
        logging.info("[ADVANCE EPISODE] Selected test type: CT Colonography")

        # Step 3: Click 'Invite for Diagnostic Test'
        self.safe_accept_dialog(self.invite_for_diagnostic_test_button)
        logging.info("[ADVANCE EPISODE] Invite for diagnostic test completed")

    def record_contact_close_episode_no_contact(self) -> None:
        """
        Records contact with the subject and sets the outcome to 'Close Episode - No Contact'.

        Steps:
            - Clicks the 'Record Contact with Patient' button
            - Selects direction and contact type
            - Picks a calendar date
            - Fills start time, end time, and duration
            - Enters a note
            - Selects 'Patient Contacted' as 'No'
            - Selects the outcome 'Close Episode - No Contact'
            - Clicks the save button
        """
        logging.info(
            "[CONTACT RECORD] Starting contact recording flow with outcome: Close Episode - No Contact"
        )

        # Step 1: Select direction and contact method and practitioner
        self.contact_direction_dropdown.select_option(ContactDirection.TO_PATIENT.value)
        self.contact_method_dropdown.select_option(ContactMethod.TELEPHONE.value)
        self.select_any_practitioner()
        logging.info(
            "[CONTACT RECORD] Selected direction, contact method, and practitioner"
        )

        # Step 2: Pick calendar date using V1 calendar picker
        calendar_picker = CalendarPicker(self.page)
        today = datetime.today()
        calendar_picker.calendar_picker_ddmmyyyy(today, self.call_date_input)
        logging.info(
            f"[CONTACT RECORD] Selected calendar date: {today.strftime('%d/%m/%Y')}"
        )

        # Step 3: Enter time details
        self.start_time_input.fill("08:00")
        self.end_time_input.fill("08:10")
        self.duration_input.fill("10")
        logging.info("[CONTACT RECORD] Entered time details: 08:00–08:10")

        # Step 4: Enter note
        self.note_input.fill("Automation test record")
        logging.info("[CONTACT RECORD] Entered note: Automation test record")

        # Step 5: Select 'Patient Contacted' as 'No'
        self.patient_contacted_dropdown.select_option("N")
        logging.info("[CONTACT RECORD] Selected 'Patient Contacted': No")

        # Step 6: Select outcome
        self.outcome_dropdown.select_option("20202")
        logging.info("[CONTACT RECORD] Selected outcome: Close Episode - No Contact")

        # Step 7: Click save
        self.click(self.save_button)
        logging.info("[CONTACT RECORD] Contact recording flow completed successfully")

    def click_not_suitable_for_diagnostic_tests_button(self) -> None:
        """Click the 'Not Suitable for Diagnostic Tests' button."""
        self.safe_accept_dialog(self.not_suitable_for_diagnostic_tests_button)

    def click_cancel_diagnostic_test_button(self) -> None:
        """Click the 'Cancel Diagnostic Test' button."""
        self.safe_accept_dialog(self.cancel_diagnostic_test_button)

    def click_post_investigation_appointment_required_button(self) -> None:
        """Click the 'Post-investigation Appointment Required' button."""
        self.safe_accept_dialog(self.post_investigation_appointment_required_button)

    def click_redirect_to_delete_the_latest_diagnostic_test_result_button(
        self, messages_to_assert: List[str]
    ) -> None:
        """
        Click the 'Redirect to DELETE the Latest Diagnostic Test Result' button, handle both dialogs.
        Args:
            messages_to_assert (List[str]): List of messages to assert in the second dialog.
        """

        # Handler for the first dialog: accept it
        def handle_first_dialog(dialog: Dialog) -> None:
            """Handle the first dialog by accepting it."""
            logging.info(f"[DIALOG 1] Message: {dialog.message}")
            dialog.accept()
            logging.info("[DIALOG 1] First dialog accepted.")

            # Handler for the second dialog: assert text and accept/dismiss as needed
            def handle_second_dialog(dialog: Dialog) -> None:
                """
                Handle the second dialog by asserting its text and accepting it.
                Checks for specific warning messages passed in through messages_to_assert.
                Raises:
                    AssertionError: If the dialog text does not contain expected messages.
                """
                logging.info(f"[DIALOG 2] Message: {dialog.message}")
                actual_text = dialog.message
                for message in messages_to_assert:
                    logging.info(
                        f"[UI ASSERTION] Verifying dialog contains: '{message}'"
                    )
                    assert (
                        message in actual_text
                    ), f"Expected dialog to contain '{message}', but got '{actual_text}'"
                    logging.info(
                        f"[UI ASSERTIONS COMPLETE]: '{message}' found in dialog text."
                    )
                dialog.accept()
                logging.info("[DIALOG 2] Second dialog asserted and accepted.")

            self.page.once("dialog", handle_second_dialog)

        self.page.once("dialog", handle_first_dialog)

        # Click the button to trigger dialogs
        self.click(self.redirect_to_delete_the_latest_diagnostic_test_result_button)

    def click_redirect_to_reestablish_suitability_for_diagnostic_test_repatient_contact(
        self,
    ) -> None:
        """Click the 'Redirect to re-establish suitability for diagnostic test - repatient contact' button."""
        self.safe_accept_dialog(
            self.redirect_to_reestablish_suitability_for_diagnostic_test_repatient_contact
        )

    def select_any_practitioner(self) -> None:
        """
        Selects any practitioner from the 'Contact made between patient and' dropdown.
        Skips the empty default option and selects the first available practitioner.
        """
        logging.info("[CONTACT RECORD] Selecting any practitioner from dropdown")

        # Get all available options
        options = self.contact_made_between_dropdown.locator("option").all()
        for option in options:
            value = option.get_attribute("value")
            if value and value.strip():
                self.contact_made_between_dropdown.select_option(value)
                logging.info(
                    f"[CONTACT RECORD] Selected practitioner with value: {value}"
                )
                return

        logging.warning("[CONTACT RECORD] No valid practitioner found to select")
