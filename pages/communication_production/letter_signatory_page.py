from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LetterSignatoryPage(BasePage):
    """Letter Signatory Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Letter Signatory - page locators, methods

    def verify_letter_signatory_title(self) -> None:
        """Verify the Letter Signatory page title is displayed as expected"""
        self.bowel_cancer_screening_page_title_contains_text(
            "Letter Signatory"
        )
