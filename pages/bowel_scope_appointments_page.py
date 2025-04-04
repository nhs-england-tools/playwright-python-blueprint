from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class BowelScopeAppointments(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        #Bowel Scope Appointments - page locators
        self.page_title = self.page.locator("#ntshPageTitle")

    def verify_page_title(self) -> None:
        expect(self.page_title).to_contain_text("Appointment Calendar")
