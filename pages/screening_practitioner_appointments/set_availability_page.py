from playwright.sync_api import Page
from pages.base_page import BasePage


class SetAvailabilityPage(BasePage):
    """Set Availability Page locators and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Set Availability - page locators
        self.practitioner_availability_link = page.get_by_role(
            "link", name="Practitioner Availability -"
        )

    def go_to_practitioner_availability_page(self) -> None:
        """Navigate to the Practitioner Availability page."""
        self.click(self.practitioner_availability_link)
