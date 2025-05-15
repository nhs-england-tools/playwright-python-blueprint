from playwright.sync_api import Page
from pages.base_page import BasePage


class ContactWithPatientPage(BasePage):
    """
    ContactWithPatientPage class for interacting with 'Contact With Patient' page elements.
    """

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # Contact With Patient - Page Locators
        self.contact_direction_dropdown = self.page.locator("#UI_DIRECTION")
        self.contact_made_between_patient_and_dropdown = self.page.locator(
            "#UI_CALLER_ID"
        )
        self.calendar_button = self.page.get_by_role("button", name="Calendar")
        self.start_time_field = self.page.locator("#UI_START_TIME")
        self.end_time_field = self.page.locator("#UI_END_TIME")
        self.discussion_record_text_field = self.page.locator("#UI_COMMENT_ID")
        self.outcome_dropdown = self.page.locator("#UI_OUTCOME")
        self.save_button = self.page.get_by_role("button", name="Save")

    def select_direction_dropdown_option(self, direction: str) -> None:
        """
        Select an option from the 'Direction' dropdown by its label.

        Args:
        direction (str): The label of the direction option to select.
        """
        self.contact_direction_dropdown.select_option(label=direction)

    def select_caller_id_dropdown_index_option(self, index_value: int) -> None:
        """
        Select an option from the 'Caller ID' dropdown by its index.

        Args:
        index_value (int): The index of the caller ID option to select.
        """
        self.contact_made_between_patient_and_dropdown.select_option(index=index_value)

    def click_calendar_button(self) -> None:
        """Click the 'Calendar' button to open the calendar picker."""
        self.click(self.calendar_button)

    def enter_start_time(self, start_time: str) -> None:
        """
        Enter a value into the 'Start Time' field.

        Args:
        start_time (str): The start time to enter into the field.
        """
        self.start_time_field.fill(start_time)

    def enter_end_time(self, end_time: str) -> None:
        """
        Enter a value into the 'End Time' field.

        Args:
        end_time (str): The end time to enter into the field.
        """
        self.end_time_field.fill(end_time)

    def enter_discussion_record_text(self, value: str) -> None:
        """
        Enter text into the 'Discussion Record' field.

        Args:
        value (str): The text to enter into the discussion record field.
        """
        self.discussion_record_text_field.fill(value)

    def select_outcome_dropdown_option(self, outcome: str) -> None:
        """
        Select an option from the 'Outcome' dropdown by its label.

        Args:
        outcome (str): The label of the outcome option to select.
        """
        self.outcome_dropdown.select_option(label=outcome)

    def click_save_button(self) -> None:
        """Click the 'Save' button to save the contact with patient form."""
        self.click(self.save_button)
