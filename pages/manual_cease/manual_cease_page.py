from playwright.sync_api import Page
import logging
from datetime import datetime
from pages.base_page import BasePage


class ManualCeasePage(BasePage):
    """This class contains locators to interact with the manual cease page."""

    def __init__(self, page: Page):
        self.page = page
        self.request_cease_button = page.locator("input[name='BTN_REQUEST_CEASE']")
        self.cease_reason_dropdown = page.locator("#A_C_RequestCeaseReason")
        self.notes_textbox = page.get_by_role("textbox", name="Notes (up to 500 char)")
        self.date_confirmed_field = page.get_by_label("Date Confirmed")
        self.confirm_cease_button = page.get_by_role("button", name="Confirm Cease")
        self.save_request_cease_button = page.locator(
            "input[name='BTN_SAVE'][value='Save Request Cease']"
        )
        self.summary_table = page.locator("#screeningSummaryTable")
        self.record_disclaimer_sent_button = page.get_by_role(
            "button", name="Record Disclaimer Letter Sent"
        )
        self.confirm_disclaimer_sent_button = page.get_by_role("button", name="Confirm")
        self.record_return_disclaimer_button = page.get_by_role(
            "button", name="Record Return of Disclaimer Letter"
        )
        self.notes_field = page.get_by_label("Notes")

    def click_request_cease(self) -> None:
        """Clicks the 'Request Cease' button."""
        self.click(self.request_cease_button)

    def select_cease_reason(self, reason: str) -> None:
        """Selects a given cease reason from the dropdown.
        Args:
            reason (str): The reason to select from the dropdown.
        """
        self.cease_reason_dropdown.select_option(label=reason)

    def click_save_request_cease(self) -> None:
        """Clicks the 'Save Request Cease' button."""
        self.click(self.save_request_cease_button)

    def record_disclaimer_sent(self) -> None:
        """Clicks the 'Record the disclaimer letter has been sent' button."""
        self.click(self.record_disclaimer_sent_button)

    def confirm_disclaimer_sent(self) -> None:
        """Clicks the 'Confirm disclaimer letter has been sent' button."""
        self.click(self.confirm_disclaimer_sent_button)

    def record_return_of_disclaimer(self) -> None:
        """Clicks the 'Record the return of the disclaimer letter' button."""
        self.click(self.record_return_disclaimer_button)

    def fill_notes_and_date(self, notes: str = "AUTO TEST: notes") -> None:
        """Fills in notes and today's date in the form.
        Args:
            notes (str): Notes to fill in the text box.
        """
        self.notes_field.fill(notes)
        today_str = datetime.today().strftime("%d/%m/%Y")
        self.date_confirmed_field.fill(today_str)

    def confirm_cease(self) -> None:
        """Clicks the 'Confirm cease' button and accepts dialog."""
        self.safe_accept_dialog(self.confirm_cease_button)

    def fill_notes_if_visible(self, notes: str = "AUTO TEST: notes") -> None:
        """Fills in notes if the notes textbox is visible.
        Args:
            notes (str): Notes to fill in the text box.
        """
        if self.notes_textbox.is_visible():
            self.notes_textbox.fill(notes)

    def fill_date_if_visible(self, date_str: str) -> None:
        """Fills in today's date if the date confirmed field is visible.
        Args:
            date_str (str): Date to fill in the date confirmed field.
        """
        if self.date_confirmed_field.is_visible():
            self.date_confirmed_field.fill(date_str)

    def confirm_or_save_cease(self) -> None:
        """Confirms the cease action via either 'Confirm Cease' or 'Save Request Cease' button."""
        if self.confirm_cease_button.is_visible():
            BasePage(self.page).safe_accept_dialog(self.confirm_cease_button)

        elif self.save_request_cease_button.is_visible():
            self.click(self.save_request_cease_button)
        else:
            logging.error("No cease confirmation button found!")
            raise RuntimeError("Cease button not found on the page")
