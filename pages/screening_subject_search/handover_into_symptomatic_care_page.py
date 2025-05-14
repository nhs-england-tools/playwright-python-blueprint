from playwright.sync_api import Page
from pages.base_page import BasePage
from datetime import datetime

class HandoverIntoSymptomaticCarePage(BasePage):
    """
    HandoverIntoSymptomaticCarePage class for interacting with the 'Handover Into Symptomatic Care' page elements.
    """
    def __init__(self, page: Page):
        self.page = page
        self.referral_dropdown = self.page.get_by_label("Referral")
        self.calendar_button = self.page.get_by_role("button", name="Calendar")
        self.consultant_link = self.page.locator("#UI_NS_CONSULTANT_PIO_SELECT_LINK")
        self.notes_textbox = self.page.get_by_role("textbox", name="Notes")
        self.save_button = self.page.get_by_role("button", name="Save")

    def select_referral_dropdown_option(self, value: str) -> None:
        """
        Select a given option from the Referral dropdown.

        Args:
            value (str): The value of the option you want to select
        """
        self.referral_dropdown.select_option(value)

    def click_calendar_button(self) -> None:
        """Click the calendar button to open the calendar picker."""
        self.click(self.calendar_button)

    def select_consultant(self, value: str) -> None:
        """
        Select a consultant from the consultant dropdown using the given value.

        Args:
        value (str): The value attribute of the consultant option to select.
        """
        self.consultant_link.click()
        option_locator = self.page.locator(f'[value="{value}"]:visible')
        option_locator.wait_for(state="visible")
        self.click(option_locator)

    def fill_notes(self, notes: str) -> None:
        """
        Fill the 'Notes' textbox with the provided text.

        Args:
        notes (str): The text to enter into the notes textbox.
        """
        self.notes_textbox.click()
        self.notes_textbox.fill(notes)

    def click_save_button(self) -> None:
        """Click the save button to save the changes."""
        self.safe_accept_dialog(self.save_button)
