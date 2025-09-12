from pages.base_page import BasePage
from playwright.sync_api import Page


class CloseFobtScreeningEpisodePage(BasePage):
    """Close FOBT Screening Episode Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.close_fobt_screening_episode_button = self.page.get_by_role(
            "button", name="Close FOBT Screening Episode"
        )
        self.reason_dropdown = self.page.locator("#CLOSE_REASON")
        self.notes_textarea = self.page.locator("#UI_NOTES_TEXT")
        self.final_close_button = self.page.locator("#UI_BUTTON_CLOSE")

    def close_fobt_screening_episode(self, reason_text: str) -> None:
        """
        Complete the process of closing a FOBT screening episode.
        Args:
            reason_text (str): The visible text of the reason to select from the dropdown.
        """
        # Step 1: Trigger the dialog and accept it
        self.safe_accept_dialog(self.close_fobt_screening_episode_button)

        # Step 2: Select reason from dropdown
        self.reason_dropdown.select_option(label=reason_text)

        # Step 3: Enter note
        self.notes_textarea.fill("automation test note")

        # Step 4: Click final 'Close Episode' button
        self.safe_accept_dialog(self.final_close_button)
