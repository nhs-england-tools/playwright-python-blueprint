from datetime import datetime
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.calendar_picker import CalendarPicker


class NonNeoplasticResultFromSymptomaticProcedurePage(BasePage):
    """Non Neoplastic Result From Symptomatic Procedure Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        # Non Neoplastic Result From Symptomatic Procedure - page locators
        self.date_of_symptomatic_procedure_calendar_button = self.page.locator(
            "#UI_SURGERY_DATE__LinkOrButton"
        )
        self.alert_textbox = self.page.locator("#UI_SPAN_RECALL_TEXT")
        self.all_tests = self.page.locator("#UI_ID_RECALL_ANCHOR_DATE_EXT_TEST_ID")
        self.save_button = self.page.get_by_role("button", name="Save")

    def click_date_of_symptomatic_procedure_calendar_button(self) -> None:
        """Click the date of symptomatic procedure calendar button."""
        self.click(self.date_of_symptomatic_procedure_calendar_button)

    def enter_date_of_symptomatic_procedure(self, date: datetime) -> None:
        """
        Enter the date of the symptomatic procedure.
        Args:
            date (datetime): The date to be entered in the date of symptomatic procedure field. Example: datetime(2023, 10, 25)
        """
        self.click_date_of_symptomatic_procedure_calendar_button()
        CalendarPicker(self.page).v1_calender_picker(date)

    def assert_text_in_alert_textbox(self, expected_text: str) -> None:
        """
        Assert that the expected text is present in the alert textbox.
        Args:
            expected_text (str): The text expected to be found in the alert textbox. Example: "This is a test alert"
        """
        actual_text = self.alert_textbox.inner_text()
        assert (
            expected_text in actual_text
        ), f"Expected text '{expected_text}' not found in alert textbox. Actual text: '{actual_text}'"

    def select_test_number(self, test_number: int) -> None:
        """
        Select a test from the all tests dropdown by its index.
        Args:
            test_number (int): The index of the test to select (1-based index). Example: if you want to select the 1st test pass in 1
        """
        self.click(self.all_tests.nth(test_number - 1))

    def click_save_button(self) -> None:
        """Click the 'Save' button."""
        self.click(self.save_button)
