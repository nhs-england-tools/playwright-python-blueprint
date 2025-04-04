from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class LynchInvitationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Lynch Invitation Page - Links
        self.set_lynch_invitation_rates_link = self.page.get_by_role("link", name="Set Lynch Invitation Rates")

    def click_set_lynch_invitation_rates_link(self)->None:
        self.click(self.set_lynch_invitation_rates_link)
