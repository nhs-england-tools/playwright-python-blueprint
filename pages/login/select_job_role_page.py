from playwright.sync_api import Page
from pages.base_page import BasePage


class SelectJobRolePage(BasePage):
    """Select Job Role Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.select_job_dropdown = self.page.locator("#selRole")
        self.continue_button = self.page.locator("#SelectButton")

    def select_option_for_job_role(self, job_role: str) -> None:
        """
        Selects a job from the job role dropdown
        Args:
            job_role (str): This is the text of the role you want to select (e.g. Screening Practitioner)
        """
        self.select_job_dropdown.select_option(label=job_role)

    def click_continue_button(self) -> None:
        """Clicks on the 'Continue' button"""
        self.click(self.continue_button)
