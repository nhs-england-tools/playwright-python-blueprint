from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class MaintainAnalysersPage(BasePage):
    """Maintain Analysers page locators and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Maintain Analysers - page locators, methods

    def verify_maintain_analysers_title(self) -> None:
        """Verify the Maintain Analysers page title is displayed correctly."""
        self.bowel_cancer_screening_page_title_contains_text("Maintain Analysers")
