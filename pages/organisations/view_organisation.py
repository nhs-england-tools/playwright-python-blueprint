import logging
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ViewOrganisation(BasePage):
    """View Organisation Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        # View Organisation links
        self.edit_button = self.page.get_by_role("button", name="Edit")

    def verify_page_title(self) -> None:
        """Verifies that the page title contains 'View Organisation'."""
        logging.info("Verifying page title for View Organisation")
        expect(self.page.locator("#ntshPageTitle")).to_contain_text("View Organisation")

    def verify_organisation_code_details(self,text:str) -> None:
        """Verifies that the organisation code details are displayed correctly."""
        logging.info("Verifying organisation code details on View Organisation page")
        expect(self.page.locator('form[name="frm"]')).to_contain_text(text)

    def verify_organisation_type_details(self,text:str) -> None:
        """Verifies that the organisation type details are displayed correctly."""
        logging.info("Verifying organisation type details on View Organisation page")
        expect(self.page.locator('form[name="frm"]')).to_contain_text(text)

    def click_edit_button(self) -> None:
        """Clicks the Edit button on the View Organisation page."""
        logging.info("Clicking Edit button on View Organisation page")
        self.click(self.edit_button)
