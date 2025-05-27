from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from enum import Enum
from datetime import datetime
from utils.calendar_picker import CalendarPicker


class LogDevicesPage(BasePage):
    """Log Devices Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Log Devices - page links
        self.fit_device_id_field = self.page.get_by_role(
            "textbox", name="FIT Device ID"
        )
        self.save_and_log_device_button = self.page.get_by_role(
            "button", name="Save and Log Device"
        )
        self.device_spoilt_button = self.page.get_by_role(
            "button", name="Device Spoilt"
        )
        self.sample_date_field = self.page.locator("#sampleDate")
        self.successfully_logged_device_text = self.page.get_by_text(
            "×Successfully logged device"
        )
        self.spoilt_device_dropdown = self.page.get_by_label("Spoil reason drop down")
        self.log_as_spoilt_button = self.page.get_by_role(
            "button", name="Log as Spoilt"
        )
        self.log_devices_title = self.page.locator("#page-title")

    def verify_log_devices_title(self) -> None:
        """Verifies that the Log Devices page title is displayed correctly."""
        self.bowel_cancer_screening_page_title_contains_text(
            "Scan Device"
        )

    def fill_fit_device_id_field(self, value) -> None:
        """Fills the FIT Device ID field with the provided value and presses Enter."""
        self.fit_device_id_field.fill(value)
        self.fit_device_id_field.press("Enter")

    def click_save_and_log_device_button(self) -> None:
        """Clicks the 'Save and Log Device' button."""
        self.click(self.save_and_log_device_button)

    def click_device_spoilt_button(self) -> None:
        """Clicks the 'Device Spoilt' button."""
        self.click(self.device_spoilt_button)

    def fill_sample_date_field(self, date: datetime) -> None:
        """Fills the sample date field with the provided date."""
        CalendarPicker(self.page).calendar_picker_ddmonyy(date, self.sample_date_field)

    def verify_successfully_logged_device_text(self) -> None:
        """Verifies that the 'Successfully logged device' text is displayed."""
        expect(self.successfully_logged_device_text).to_be_visible()

    def select_spoilt_device_dropdown_option(self) -> None:
        """Selects the 'Broken in transit' option from the spoilt device dropdown."""
        self.spoilt_device_dropdown.select_option(
            SpoiltDeviceOptions.BROKEN_IN_TRANSIT.value
        )

    def click_log_as_spoilt_button(self) -> None:
        """Clicks the 'Log as Spoilt' button."""
        self.click(self.log_as_spoilt_button)


class SpoiltDeviceOptions(Enum):
    """Enumeration for the options available in the spoilt device dropdown."""

    BROKEN_IN_TRANSIT = "205156"
    DEVICE_MISUSE = "205157"
    NOT_USED = "205159"
    SAMPLE_BUFFER_LOST = "205158"
    TOO_MUCH_SAMPLE = "306397"
    OTHER = "205161"
