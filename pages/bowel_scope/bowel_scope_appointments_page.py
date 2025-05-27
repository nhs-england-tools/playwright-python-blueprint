from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class BowelScopeAppointmentsPage(BasePage):
    """Bowel Scope Appointments page locators, and methods to interact with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Bowel Scope Appointments - page locators, methods

    def verify_page_title(self) -> None:
        """Verifies the page title of the Bowel Scope Appointments page"""
        self.bowel_cancer_screening_page_title_contains_text(
            "Appointment Calendar"
        )
