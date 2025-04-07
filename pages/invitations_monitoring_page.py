from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class InvitationsMonitoring(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.invitations_monitoring_title = self.page.locator("#page-title")

    def go_to_invitation_plan_page(self, sc_id) -> None:
        self.click(self.page.get_by_role("link", name=sc_id))

    def verify_invitations_monitoring_title(self) -> None:
        expect(self.invitations_monitoring_title).to_contain_text(
            "Invitations Monitoring - Screening Centre"
        )
