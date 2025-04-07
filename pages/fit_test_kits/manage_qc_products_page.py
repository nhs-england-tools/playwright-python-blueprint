from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ManageQCProducts(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Manage QC Products - page locators
        self.manage_qc_products_title = self.page.locator("#page-title")

    def verify_manage_qc_products_title(self) -> None:
        expect(self.manage_qc_products_title).to_contain_text("FIT QC Products")
