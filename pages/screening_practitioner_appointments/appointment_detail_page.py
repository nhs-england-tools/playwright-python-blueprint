from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class AppointmentDetail(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Appointment Detail - page filters
        self.attendance_radio = self.page.get_by_role("radio", name="Attendance")
        self.attendented_check_box = self.page.locator("#UI_ATTENDED")
        self.calendar_button = self.page.get_by_role("button", name="Calendar")
        self.save_button = self.page.get_by_role("button", name="Save").click()

    def check_attendance_radio(self) -> None:
        self.attendance_radio.check()

    def check_attendented_check_box(self) -> None:
        self.attendented_check_box.check()

    def click_calendar_button(self) -> None:
        self.click(self.calendar_button)

    def click_save_button(self) -> None:
        self.click(self.save_button)

    def verify_text_visible(self, text: str) -> None:
        expect(self.page.get_by_text(text)).to_be_visible()
