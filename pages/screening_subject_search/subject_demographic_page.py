from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from datetime import datetime
from utils.calendar_picker import CalendarPicker
import logging

class SubjectDemographicPage(BasePage):
    """Subject Demographic Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self.title = "Subject Demographic";

        # Subject Demographic - page filters
        self.forename_field = self.page.get_by_role("textbox", name="Forename")
        self.surname_field = self.page.get_by_role("textbox", name="Surname")
        self.postcode_field = self.page.get_by_role("textbox", name="Postcode")
        self.dob_field = self.page.get_by_role("textbox", name="Date of Birth")
        self.update_subject_data_button = self.page.get_by_role(
            "button", name="Update Subject Data"
        )
        self.temporary_address_show_link = (
            self.page.locator("font")
            .filter(has_text="Temporary Address show")
            .get_by_role("link")
        )
        self.temporary_address_valid_from_calendar_button = self.page.locator(
            "#UI_SUBJECT_ALT_FROM_0_LinkOrButton"
        )
        self.temporary_address_valid_to_calendar_button = self.page.locator(
            "#UI_SUBJECT_ALT_TO_0_LinkOrButton"
        )
        self.temporary_address_valid_from_text_box = self.page.get_by_role(
            "textbox", name="Valid from"
        )
        self.temporary_address_valid_to_text_box = self.page.get_by_role(
            "textbox", name="Valid to"
        )
        self.temporary_address_address_line_1 = self.page.locator(
            "#UI_SUBJECT_ALT_ADDR1_0"
        )
        self.temporary_address_address_line_2 = self.page.locator(
            "#UI_SUBJECT_ALT_ADDR2_0"
        )
        self.temporary_address_address_line_3 = self.page.locator(
            "#UI_SUBJECT_ALT_ADDR3_0"
        )
        self.temporary_address_address_line_4 = self.page.locator(
            "#UI_SUBJECT_ALT_ADDR4_0"
        )
        self.temporary_address_address_line_5 = self.page.locator(
            "#UI_SUBJECT_ALT_ADDR5_0"
        )
        self.temporary_address_postcode = self.page.locator(
            "#UI_SUBJECT_ALT_POSTCODE_0"
        )

    def verify_page_title(self) -> None:
        logging.info(f"Verify title as '{self.title}'")
        ""f"Verifies that the {self.title} page title is displayed correctly."""
        self.page_title_contains_text(self.title)

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

    def update_temporary_address(self, dict: dict) -> None:
        """
        Updates the temporary address fields with the provided dictionary values.
        Args:
            dict (dict): A dictionary containing the temporary address details.
                Expected keys: 'valid_from', 'valid_to', 'address_line_1',
                'address_line_2', 'address_line_3', 'address_line_4', 'address_line_5'.
        """
        # Click the link to show the temporary address fields
        if self.temporary_address_show_link.is_visible():
            # If the link is visible, click it to show the temporary address fields
            self.click(self.temporary_address_show_link)

        # Update the valid from date
        if "valid_from" in dict:
            if dict["valid_from"] is None:
                self.temporary_address_valid_from_text_box.fill("")
            else:
                CalendarPicker(self.page).calendar_picker_ddmmyyyy(
                    dict["valid_from"], self.temporary_address_valid_from_text_box
                )

        # Update the valid to date
        if "valid_to" in dict:
            if dict["valid_to"] is None:
                self.temporary_address_valid_to_text_box.fill("")
            else:
                CalendarPicker(self.page).calendar_picker_ddmmyyyy(
                    dict["valid_to"], self.temporary_address_valid_to_text_box
                )

        # Fill in the address lines
        if "address_line_1" in dict:
            self.temporary_address_address_line_1.fill(dict["address_line_1"])
        if "address_line_2" in dict:
            self.temporary_address_address_line_2.fill(dict["address_line_2"])
        if "address_line_3" in dict:
            self.temporary_address_address_line_3.fill(dict["address_line_3"])
        if "address_line_4" in dict:
            self.temporary_address_address_line_4.fill(dict["address_line_4"])
        if "address_line_5" in dict:
            self.temporary_address_address_line_5.fill(dict["address_line_5"])

        # Fill in the postcode
        if "postcode" in dict:
            self.temporary_address_postcode.fill(dict["postcode"])

        # Click the update subject data button to save changes
        self.update_subject_data_button.click()
