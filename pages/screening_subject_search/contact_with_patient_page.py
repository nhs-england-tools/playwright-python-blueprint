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
        self.contact_direction_dropdown.select_option(label=direction)

    def select_caller_id_dropdown_index_option(self, index_value: int) -> None:
        self.contact_made_between_patient_and_dropdown.select_option(index=index_value)

    def click_calendar_button(self) -> None:
        self.click(self.calendar_button)

    def enter_start_time(self, start_time: str) -> None:
        self.start_time_field.fill(start_time)

    def enter_end_time(self, end_time: str) -> None:
        self.end_time_field.fill(end_time)

    def enter_discussion_record_text(self, value: str) -> None:
        self.discussion_record_text_field.fill(value)

    def select_outcome_dropdown_option(self, outcome: str) -> None:
        self.outcome_dropdown.select_option(label=outcome)

    def click_save_button(self) -> None:
        self.click(self.save_button)
