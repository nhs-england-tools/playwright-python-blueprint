from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class EpisodeEventsAndNotesPage(BasePage):
    """Episode Events and Notes Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # List of episode events and notes - page locators
        self.view_appointment_link = self.page.get_by_role(
            "link", name="View Appointment"
        )

    def expected_episode_event_is_displayed(self, event_description: str) -> None:
        """Check if the expected episode event is displayed on the page."""
        expect(
            self.page.get_by_role("cell", name=event_description, exact=True)
        ).to_be_visible()

    def click_view_appointment_link(self) -> None:
        """Click the 'View Appointment' link"""
        self.click(self.view_appointment_link)
