from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from datetime import datetime
from utils.calendar_picker import CalendarPicker


class SubjectDemographicPage(BasePage):
    """Subject Demographic Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Subject Demographic - page filters
        self.forename_field = self.page.get_by_role("textbox", name="Forename")
        self.surname_field = self.page.get_by_role("textbox", name="Surname")
        self.postcode_field = self.page.get_by_role("textbox", name="Postcode")
        self.dob_field = self.page.get_by_role("textbox", name="Date of Birth")
        self.update_subject_data_button = self.page.get_by_role(
            "button", name="Update Subject Data"
        )

    def is_forename_filled(self) -> bool:
        """
        Checks if the forename textbox contains a value.

        Returns:
            True if the textbox has a non-empty value, False otherwise
        """
        forename_value = self.forename_field.input_value()
        return bool(forename_value.strip())

    def is_surname_filled(self) -> bool:
        """
        Checks if the surname textbox contains a value.

        Returns:
            True if the textbox has a non-empty value, False otherwise
        """
        surname_value = self.surname_field.input_value()
        return bool(surname_value.strip())

    def is_postcode_filled(self) -> bool:
        """
        Checks if the postcode textbox contains a value.

        Returns:
            True if the textbox has a non-empty value, False otherwise
        """
        postcode_value = self.postcode_field.input_value()
        return bool(postcode_value.strip())

    def fill_forename_input(self, name: str) -> None:
        """
        Enters a value into the forename input textbox

        Args:
            name (str): The name you want to enter
        """
        self.forename_field.fill(name)

    def fill_surname_input(self, name: str) -> None:
        """
        Enters a value into the surname input textbox

        Args:
            name (str): The name you want to enter
        """
        self.surname_field.fill(name)

    def fill_dob_input(self, date: datetime) -> None:
        """
        Enters a value into the date of birth input textbox

        Args:
            date (datetime): The date you want to enter
        """
        if date is None:
            raise ValueError("The 'date' argument cannot be None")
        CalendarPicker(self.page).calendar_picker_ddmmyyyy(date, self.dob_field)

    def fill_postcode_input(self, postcode: str) -> None:
        """
        Enters a value into the postcode input textbox

        Args:
            postcode (str): The postcode you want to enter
        """
        self.postcode_field.fill(postcode)

    def click_update_subject_data_button(self) -> None:
        """Clicks on the 'Update Subject Data' button"""
        self.click(self.update_subject_data_button)

    def get_dob_field_value(self) -> str:
        """
        Returns the value in the date of birth input textbox

        Returns:
            str: The subject's date of birth as a string
        """
        return self.dob_field.input_value()
