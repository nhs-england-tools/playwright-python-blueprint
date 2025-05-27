from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class BatchDownloadRequestAndRetrievalPage(BasePage):
    """Batch Download Request and Retrieval Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Batch Download Request And Retrieval - page locators
        self.page_form = self.page.locator('form[name="frm"]')

    def expect_form_to_have_warning(self) -> None:
        """Checks if the form contains a warning message about FS Screening data not being downloaded."""
        expect(self.page_form).to_contain_text(
            "Warning - FS Screening data will not be downloaded"
        )

    def verify_batch_download_request_and_retrieval_title(self) -> None:
        """Verifies that the Batch Download Request and Retrieval page title is displayed correctly."""
        self.bowel_cancer_screening_page_title_contains_text(
            "Batch Download Request and Retrieval"
        )
