from playwright.sync_api import Page
from pages.base_page import BasePage
from datetime import datetime
from utils.calendar_picker import CalendarPicker


class ReferToMdtPage(BasePage):
    """Refer to MDT Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # Refer MDT page - page locators
        self.mdt_discussion_date_field = self.page.locator("#UI_MDT_DATE_LinkOrButton")
        self.mdt_location = self.page.locator("#UI_NS_SITE_SELECT_LINK")
        self.visible_ui_results_string = 'select[id^="UI_RESULTS_"]:visible'
        self.record_MDT_appointment_button = self.page.locator(
            '[name="UI_BUTTON_SAVE"]'
        )

    def enter_date_in_Mdt_discussion_date_field(self, date: datetime) -> None:
        """
        Enters a date in the MDT discussion date field.
        Args:
            date (datetime): The date to enter in the field.
        """
        self.click(self.mdt_discussion_date_field)
        CalendarPicker(self.page).v2_calendar_picker(date)
        self.mdt_discussion_date_field.press("Tab")

    def select_mdt_location_lookup(self, option: int) -> None:
        """
        This method is designed to select an option from the MDT location lookup dropdown.
        Args:
            option (int): The index of the option to select (0-based).
        """
        self.click(self.mdt_location)
        select_locator = self.page.locator(self.visible_ui_results_string)
        select_locator.first.wait_for(state="visible")
        # Find all option elements inside the select and click the one at the given index
        option_elements = select_locator.first.locator("option")
        option_elements.nth(option).wait_for(state="visible")
        self.click(option_elements.nth(option))

    def click_record_MDT_appointment_button(self) -> None:
        """Clicks the record MDT appointment button."""
        self.click(self.record_MDT_appointment_button)
