from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ManageQCProductsPage(BasePage):
    """Manage QC Products page locators and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Manage QC Products - page locators, methods

    def verify_manage_qc_products_title(self) -> None:
        """Verify the Manage QC Products page title is displayed correctly."""
        self.bowel_cancer_screening_page_title_contains_text(
            "FIT QC Products"
        )
