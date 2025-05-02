from playwright.sync_api import Page
from pages.base_page import BasePage


class BowelScopePage(BasePage):
    """Bowel Scope page locators, and methods to interact with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Bowel Scope - page locators
        self.view_bowel_scope_appointments_page = self.page.get_by_role(
            "link", name="View Bowel Scope Appointments"
        )

    def go_to_view_bowel_scope_appointments_page(self) -> None:
        """Clicks the link to navigate to the Bowel Scope Appointments page"""
        self.click(self.view_bowel_scope_appointments_page)
