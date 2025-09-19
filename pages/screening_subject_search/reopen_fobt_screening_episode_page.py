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
