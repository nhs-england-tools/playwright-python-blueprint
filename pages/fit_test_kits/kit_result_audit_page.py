from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class KitResultAuditPage(BasePage):
    """Kit Results Audit Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Kit Result Audit - page locators, methods

    def verify_kit_result_audit_title(self) -> None:
        """Verifies that the Kit Result Audit page title is displayed correctly."""
        self.bowel_cancer_screening_page_title_contains_text(
            "Kit Result Audit"
        )
