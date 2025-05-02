from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ColonoscopyAssessmentAppointmentsPage(BasePage):
    """Colonoscopy Assessment Appointments Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Colonoscopy Assessment Appointments - page locators
        self.page_header = self.page.locator("#page-title")
        self.page_header_with_title = self.page.locator(
            "#page-title",
            has_text="Patients that Require Colonoscopy Assessment Appointments",
        )
        self.nhs_number_filter_text_field = self.page.locator("#nhsNumberFilter")

    def verify_page_header(self) -> None:
        """Verifies the Colonoscopy Assessment Appointments page header is displayed correctly."""
        expect(self.page_header).to_contain_text(
            "Patients that Require Colonoscopy Assessment Appointments"
        )

    def wait_for_page_header(self) -> None:
        """Waits for the Colonoscopy Assessment Appointments page header to be displayed."""
        self.page_header_with_title.wait_for()

    def filter_by_nhs_number(self, nhs_number: str) -> None:
        """Filters the Colonoscopy Assessment Appointments page by NHS number."""
        self.click(self.nhs_number_filter_text_field)
        self.nhs_number_filter_text_field.fill(nhs_number)
        self.nhs_number_filter_text_field.press("Enter")

    def click_nhs_number_link(self, nhs_number: str) -> None:
        """Clicks the NHS number link on the Colonoscopy Assessment Appointments page."""
        self.click(self.page.get_by_role("link", name=nhs_number))
