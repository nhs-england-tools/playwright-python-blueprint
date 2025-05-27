from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ScreeningIncidentsListPage(BasePage):
    """Screening Incidents List page locators and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Screening Incidents List - page locators, methods

    def verify_screening_incidents_list_title(self) -> None:
        """Verify the Screening Incidents List page title is displayed correctly."""
        self.bowel_cancer_screening_page_title_contains_text(
            "Screening Incidents List"
        )
