from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class EpisodeEventsAndNotesPage(BasePage):
    """Episode Events and Notes Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # List of episode events and notes - page locators

    def expected_episode_event_is_displayed(self, event_description: str) -> None:
        """Check if the expected episode event is displayed on the page."""
        expect(
            self.page.get_by_role("cell", name=event_description, exact=True)
        ).to_be_visible()
