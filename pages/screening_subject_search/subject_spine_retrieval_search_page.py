from datetime import datetime
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from typing import Dict
from utils.calendar_picker import CalendarPicker

class SpineSearchPage(BasePage):
    """
    Page object for the Spine Search screen, enabling demographic searches
    and data retrieval from the Spine system.
    """
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # Define locators
        self.demographics_radio = self.page.get_by_role("radio", name="Demographics")
        self.date_of_birth_field = self.page.locator("#dateOfBirth")
        self.surname_field = self.page.locator("#surname")
        self.forename_field = self.page.locator("#forename")
        self.gender_dropdown = self.page.locator("#gender")
        self.postcode_field = self.page.locator("#postcode")
        self.search_button = self.page.get_by_role("button", name="Search")
        self.alert_locator= self.page.locator(".spine-alert")

        # CalendarPicker utility instance
        self.calendar_picker = CalendarPicker(self.page)

    def select_demographic_search(self) -> None:
        """
        Selects the 'Demographics' radio button to enable demographic search mode.
        """
        self.demographics_radio.check()

    def enter_search_criteria(
        self, dob: str, surname: str, forename: str, gender: str, postcode: str
    ) -> None:
        """
        Fills in the demographic search fields with the provided values.

        Args:
            dob (str): Date of birth in string format (e.g., "06 May 1940").
            surname (str): Subject's surname.
            forename (str): Subject's forename.
            gender (str): Gender value ("Male" or "Female").
            postcode (str): Subject's postcode.
        """

        # Convert dob string to datetime object
        dob_dt = datetime.strptime(dob, "%d %b %Y")  # Adjust format if needed
        self.click(self.date_of_birth_field)
        self.calendar_picker.v2_calendar_picker(dob_dt)  # dob should be in a supported format, e.g. "YYYY-MM-DD"
        self.surname_field.fill(surname)
        self.forename_field.fill(forename)
        gender_option = {"Male": "1", "Female": "2"}.get(gender, "1")
        self.gender_dropdown.select_option(gender_option)
        self.postcode_field.fill(postcode)

    def perform_search(self) -> None:
        """
        Clicks the 'Search' button to initiate the Spine demographic search.
        """
        self.click(self.search_button)

    def get_spine_alert_message(self) -> str:
        """
        Retrieves the text content of a visible spine alert message from the page.

        This method waits for the alert element with the CSS class `.spine-alert` to become visible
        within a 5-second timeout. If the alert appears, its inner text is returned after stripping
        leading and trailing whitespace. If the alert does not appear within the timeout or an unexpected
        error occurs, an empty string is returned and the error is logged to the console.

        Returns:
            str: The stripped text of the alert message if visible, otherwise an empty string.
        """
        alert_locator = self.page.locator(".spine-alert")
        try:
            alert_locator.wait_for(state="visible", timeout=5000)
            return alert_locator.inner_text().strip()
        except TimeoutError:
            print("Alert message not visible within timeout.")
            return ""
        except Exception as e:
            print(f"Unexpected error while fetching alert: {e}")
            return ""
