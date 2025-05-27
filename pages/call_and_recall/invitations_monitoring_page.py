from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class InvitationsMonitoringPage(BasePage):
    """Invitations Monitoring page locators, and methods to interact with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    def go_to_invitation_plan_page(self, sc_id) -> None:
        self.click(self.page.get_by_role("link", name=sc_id))

    def verify_invitations_monitoring_title(self) -> None:
        self.bowel_cancer_screening_page_title_contains_text(
            "Invitations Monitoring - Screening Centre"
        )
