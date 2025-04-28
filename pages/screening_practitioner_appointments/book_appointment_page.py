from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.table_util import TableUtils


class BookAppointmentPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Book Appointment - page locators
        self.screening_center_dropdown = page.locator("#UI_NEW_SCREENING_CENTRE")
        self.site_dropdown = page.locator("#UI_NEW_SITE")
        self.appointment_time_radio_button = page.locator(
            page.get_by_role("radio", name="UI_NEW_SLOT_SELECTION_ID")
        )
        self.save_button = page.get_by_role("button", name="Save")
        self.appointments_table = TableUtils(self.page, "#displayRS")
        self.current_month_displayed = self.page.locator("#MONTH_AND_YEAR")

        self.appointment_cell_locators = self.page.locator("input.twoColumnCalendar")
        self.available_background_colour = "rgb(102, 255, 153)"
        self.some_available_background_colour = "rgb(255, 220, 144)"

    def select_screening_centre_dropdown_option(self, screening_centre: str) -> None:
        self.screening_center_dropdown.select_option(label=screening_centre)

    def select_site_dropdown_option(self, screening_site: str | list) -> None:
        self.site_dropdown.select_option(label=screening_site)
        self.site_dropdown.press("Enter")

    def choose_appointment_time(self) -> None:
        self.appointment_time_radio_button.check()

    def click_save_button(self) -> None:
        self.click(self.save_button)

    def appointment_booked_confirmation_is_displayed(self, message: str) -> None:
        expect(self.page.get_by_text(message)).to_be_visible()

    def get_current_month_displayed(self) -> str:
        return self.current_month_displayed.text_content()
