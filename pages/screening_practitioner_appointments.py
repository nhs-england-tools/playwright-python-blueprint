from playwright.sync_api import Page
from pages.base_page import BasePage


class ScreeningPractitionerAppointmentsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # ScreeningPractitionerAppointments Page
        self.log_in_page = self.page.get_by_role("button", name="Log in")
        self.view_appointments_page = self.page.get_by_role(
            "link", name="View appointments"
        )
        self.patients_that_require_page = self.page.get_by_role(
            "link", name="Patients that Require"
        )
        # Greyed out links (not clickable due to user role permissions)
        self.patients_that_require_colonoscopy_assessment_appointments_bowel_scope_link = self.page.get_by_text(
            "Patients that Require Colonoscopy Assessment Appointments - Bowel Scope"
        )
        self.patients_that_require_surveillance_appointment_link = page.get_by_text(
            "Patients that Require Surveillance Appointments"
        )
        self.patients_that_require_post = page.get_by_text(
            "Patients that Require Post-"
        )
        self.set_availability_link = page.get_by_text("Set Availability")

    def go_to_log_in_page(self) -> None:
        self.click(self.log_in_page)

    def go_to_view_appointments_page(self) -> None:
        self.click(self.view_appointments_page)

    def go_to_patients_that_require_page(self) -> None:
        self.click(self.patients_that_require_page)
