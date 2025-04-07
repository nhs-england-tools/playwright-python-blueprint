from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class KitResultAudit(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Kit Result Audit - page locators
        self.kit_result_audit_title = self.page.locator("#page-title")

    def verify_kit_result_audit_title(self) -> None:
        expect(self.kit_result_audit_title).to_contain_text("Kit Result Audit")
