from playwright.sync_api import Page
from pages.base_page import BasePage


class AppointmentCalendarPage(BasePage):
    """Appointment Calendar Page locators, and methods for interacting with the Appointment Calendar."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Appointment Calendar - page filters
        self.appointment_type_drowdown = self.page.locator("#UI_APPOINTMENT_TYPE")
        self.screening_centre_dropdown = self.page.locator("#UI_SCREENING_CENTRE")
        self.site_dropdown = self.page.locator("#UI_SITE")
        self.view_appointments_on_this_day_button = self.page.get_by_role(
            "button", name="View appointments on this day"
        )

    def select_appointment_type_dropdown(self, type: str) -> None:
        """Selects the appointment type from the dropdown."""
        self.appointment_type_drowdown.select_option(label=type)

    def select_screening_centre_dropdown(self, screening_centre: str) -> None:
        """Selects the screening centre from the dropdown."""
        self.screening_centre_dropdown.select_option(label=screening_centre)

    def select_site_dropdown(self, site: str) -> None:
        """Selects the site from the dropdown."""
        self.site_dropdown.select_option(label=site)

    def click_view_appointments_on_this_day_button(self) -> None:
        """Clicks the 'View appointments on this day' button."""
        self.click(self.view_appointments_on_this_day_button)
