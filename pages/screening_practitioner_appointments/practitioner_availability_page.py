from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class PractitionerAvailabilityPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Practitioner Availability - page locators
        self.site_id_dropdown = page.locator("#UI_SITE_ID")
        self.screening_practitioner_dropdown = page.locator("#UI_PRACTITIONER_ID")
        self.calendar_button = page.get_by_role("button", name="Calendar")
        self.show_button = page.get_by_role("button", name="Show")
        self.time_from_text_field = page.get_by_role("textbox", name="From:")
        self.time_to_text_field = page.get_by_role("textbox", name="To:")
        self.calculate_slots_button = page.get_by_role("button", name="Calculate Slots")
        self.number_of_weeks_text_field = page.locator("#FOR_WEEKS")
        self.save_button = page.get_by_role("button", name="Save")

    def select_site_dropdown_option(self, site_to_use: str) -> None:
        self.site_id_dropdown.select_option(label=site_to_use)

    def select_practitioner_dropdown_option(self, practitioner: str) -> None:
        self.screening_practitioner_dropdown.select_option(label=practitioner)

    def click_calendar_button(self) -> None:
        self.click(self.calendar_button)

    def click_show_button(self) -> None:
        self.click(self.show_button)

    def enter_start_time(self, start_time: str) -> None:
        self.time_from_text_field.fill(start_time)

    def enter_end_time(self, end_time: str) -> None:
        self.time_to_text_field.fill(end_time)

    def click_calculate_slots_button(self) -> None:
        self.click(self.calculate_slots_button)

    def enter_number_of_weeks(self, weeks: str) -> None:
        self.number_of_weeks_text_field.fill(weeks)

    def click_save_button(self) -> None:
        self.click(self.save_button)

    def slots_updated_message_is_displayed(self, message: str) -> None:
        expect(self.page.get_by_text(message)).to_be_visible()
