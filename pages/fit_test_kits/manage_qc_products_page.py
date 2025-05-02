from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ManageQCProductsPage(BasePage):
    """Manage QC Products page locators and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Manage QC Products - page locators
        self.manage_qc_products_title = self.page.locator("#page-title")

    def verify_manage_qc_products_title(self) -> None:
        """Verify the Manage QC Products page title is displayed correctly."""
        expect(self.manage_qc_products_title).to_contain_text("FIT QC Products")
