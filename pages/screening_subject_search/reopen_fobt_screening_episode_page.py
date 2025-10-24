from playwright.sync_api import Page
from pages.base_page import BasePage


class ReopenFOBTScreeningEpisodePage(BasePage):
    """Reopen FOBT Screening Episode Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self.reopen_to_book_an_assessment_button = self.page.get_by_role(
            "button", name="Reopen to book an assessment"
        )
        self.reopen_episode_for_correction_button = self.page.get_by_role(
            "button", name="Reopen episode for correction"
        )
        self.reopen_due_to_subject_or_patient_decision = self.page.get_by_role(
            "button", name="Reopen due to subject or patient decision"
        )
        self.reopen_following_non_response_button = self.page.get_by_role(
            "button", name="Reopen following Non-Response"
        )
        self.reopen_to_confirm_diagnostic_test_result_and_outcome_button = (
            self.page.get_by_role(
                "button", name="Reopen to Confirm Diagnostic Test Result and Outcome"
            )
        )
        self.reopen_to_reschedule_diagnostic_test_button = self.page.get_by_role(
            "button", name="Reopen to Reschedule Diagnostic Test"
        )
        self.reopen_to_rerecord_outcome_from_symptomatic_referral_button = (
            self.page.get_by_role(
                "button", name="Reopen to Re-record Outcome from Symptomatic Referral"
            )
        )

    def click_reopen_to_book_an_assessment_button(self) -> None:
        """Click the 'Reopen to book an assessment' button."""
        self.safe_accept_dialog(self.reopen_to_book_an_assessment_button)

    def click_reopen_episode_for_correction_button(self) -> None:
        """Click the 'Reopen episode for correction' button."""
        self.safe_accept_dialog(self.reopen_episode_for_correction_button)

    def click_reopen_due_to_subject_or_patient_decision(self) -> None:
        """Click the 'Reopen due to subject or patient decision' button."""
        self.safe_accept_dialog(self.reopen_due_to_subject_or_patient_decision)

    def click_reopen_following_non_response_button(self) -> None:
        """Click the 'Reopen following Non-Response' button."""
        self.safe_accept_dialog(self.reopen_following_non_response_button)

    def click_reopen_to_confirm_diagnostic_test_result_and_outcome_button(self) -> None:
        """Click the 'Reopen to Confirm Diagnostic Test Result and Outcome' button."""
        self.safe_accept_dialog(
            self.reopen_to_confirm_diagnostic_test_result_and_outcome_button
        )

    def click_reopen_to_reschedule_diagnostic_test_button(self) -> None:
        """Click the 'Reopen to Reschedule Diagnostic Test' button."""
        self.safe_accept_dialog(self.reopen_to_reschedule_diagnostic_test_button)

    def click_reopen_to_rerecord_outcome_from_symptomatic_referral_button(self) -> None:
        """Click the 'Reopen to Re-record Outcome from Symptomatic Referral' button."""
        self.safe_accept_dialog(
            self.reopen_to_rerecord_outcome_from_symptomatic_referral_button
        )
