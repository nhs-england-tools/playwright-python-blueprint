from playwright.sync_api import Page
from pages.base_page import BasePage


class AttendDiagnosticTest(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Advance Diagnostic Test - page locators
        self.actual_type_of_test_dropdown = self.page.locator("#UI_CONFIRMED_TYPE_OF_TEST")
        self.calendar_button = self.page.get_by_role("button", name="Calendar")
        self.save_button =self.page.get_by_role("button", name="Save")

    def select_actual_type_of_test_dropdown_option(self, text: str) -> None:
        self.actual_type_of_test_dropdown.select_option(label=text)

    def click_calendar_button(self) -> None:
        self.click(self.calendar_button)

    def click_save_button(self) -> None:
        self.click(self.save_button)
