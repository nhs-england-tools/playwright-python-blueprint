from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ScreeningIncidentsList(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Screening Incidents List - page locators
        self.screening_incidents_list_title = self.page.locator("#page-title")

    def verify_screening_incidents_list_title(self) -> None:
        expect(self.screening_incidents_list_title).to_contain_text(
            "Screening Incidents List"
        )
