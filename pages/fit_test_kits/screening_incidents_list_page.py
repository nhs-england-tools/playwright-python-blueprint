from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ScreeningIncidentsListPage(BasePage):
    """Screening Incidents List page locators and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Screening Incidents List - page locators
        self.screening_incidents_list_title = self.page.locator("#page-title")

    def verify_screening_incidents_list_title(self) -> None:
        """Verify the Screening Incidents List page title is displayed correctly."""
        expect(self.screening_incidents_list_title).to_contain_text(
            "Screening Incidents List"
        )
