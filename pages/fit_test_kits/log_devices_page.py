from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from enum import Enum


class LogDevices(BasePage):

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
        expect(self.log_devices_title).to_contain_text("Scan Device")

    def fill_fit_device_id_field(self, value) -> None:
        self.fit_device_id_field.fill(value)
        self.fit_device_id_field.press("Enter")

    def click_save_and_log_device_button(self) -> None:
        self.click(self.save_and_log_device_button)

    def click_device_spoilt_button(self) -> None:
        self.click(self.device_spoilt_button)

    def fill_sample_date_field(self, value) -> None:
        self.sample_date_field.fill(value)
        self.sample_date_field.press("Enter")

    def verify_successfully_logged_device_text(self) -> None:
        expect(self.successfully_logged_device_text).to_be_visible()

    def select_spoilt_device_dropdown_option(self) -> None:
        self.spoilt_device_dropdown.select_option(
            SpoiltDeviceOptions.BROKEN_IN_TRANSIT.value
        )

    def click_log_as_spoilt_button(self) -> None:
        self.click(self.log_as_spoilt_button)


class SpoiltDeviceOptions(Enum):
    BROKEN_IN_TRANSIT = "205156"
    DEVICE_MISUSE = "205157"
    NOT_USED = "205159"
    SAMPLE_BUFFER_LOST = "205158"
    TOO_MUCH_SAMPLE = "306397"
    OTHER = "205161"
