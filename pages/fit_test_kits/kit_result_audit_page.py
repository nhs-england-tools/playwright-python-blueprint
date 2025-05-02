from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class KitResultAuditPage(BasePage):
    """Kit Results Audit Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Kit Result Audit - page locators
        self.kit_result_audit_title = self.page.locator("#page-title")

    def verify_kit_result_audit_title(self) -> None:
        """Verifies that the Kit Result Audit page title is displayed correctly."""
        expect(self.kit_result_audit_title).to_contain_text("Kit Result Audit")
