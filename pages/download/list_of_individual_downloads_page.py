from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ListOfIndividualDownloadsPage(BasePage):
    """List of Individual Downloads Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # List Of Individual Downloads - page locators, methods

    def verify_list_of_individual_downloads_title(self) -> None:
        """Verifies that the List of Individual Downloads page title is displayed correctly."""
        self.bowel_cancer_screening_page_title_contains_text(
            "List of Individual Downloads"
        )
