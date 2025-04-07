from playwright.sync_api import Page, expect, Locator
from pages.base_page import BasePage

class BowelScope(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        #Bowel Scope - page locators
        self.view_bowel_scope_appointments_page = self.page.get_by_role("link", name="View Bowel Scope Appointments")

    def go_to_view_bowel_scope_appointments_page(self) -> None:
        self.click(self.view_bowel_scope_appointments_page)
