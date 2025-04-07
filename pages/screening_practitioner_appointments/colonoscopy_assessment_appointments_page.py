from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ColonoscopyAssessmentAppointments(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Colonoscopy Assessment Appointments - page locators
        self.page_header = self.page.locator("#page-title")

    def verify_page_header(self) -> None:
        expect(self.page_header).to_contain_text(
            "Patients that Require Colonoscopy Assessment Appointments"
        )
