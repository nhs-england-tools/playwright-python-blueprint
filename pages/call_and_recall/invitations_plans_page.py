from playwright.sync_api import Page
from pages.base_page import BasePage


class InvitationsPlansPage(BasePage):
    """Invitations Plans page locators, and methods to interact with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Call and Recall - page links
        self.create_a_plan = self.page.get_by_role("button", name="Create a Plan")
        self.invitations_plans_title = self.page.locator(
            '#page-title:has-text("Invitation Plans")'
        )
        self.first_available_plan = (
            self.page.get_by_role("row").nth(1).get_by_role("link")
        )

    def go_to_create_a_plan_page(self) -> None:
        """Clicks the Create a Plan button to navigate to the Create a Plan page"""
        self.click(self.create_a_plan)

    def go_to_first_available_plan(self) -> None:
        """Clicks the first available plan to navigate to the Create a Plan page"""
        self.click(self.first_available_plan)
