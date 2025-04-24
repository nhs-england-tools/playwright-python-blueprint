from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ViewScreeningCentreFITConfiguration(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # View Screening Centre FIT Configuration - page locators
        self.view_screening_centre_body = self.page.locator("body")
        self.screening_centre_fit_title = self.page.get_by_role(
            "heading", name="View Screening Centre FIT"
        )

    def verify_view_screening_centre_body(self) -> None:
        expect(self.view_screening_centre_body).to_contain_text("Maintain Analysers")

    def verify_view_screening_centre_fit_title(self) -> None:
        expect(self.screening_centre_fit_title).to_contain_text(
            "View Screening Centre FIT Configuration"
        )
