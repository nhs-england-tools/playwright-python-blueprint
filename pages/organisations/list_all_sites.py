import logging
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from enum import StrEnum
from utils.table_util import TableUtils


class ListAllSites(BasePage):
    """List All Sites Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        # Initialize TableUtils for the table with id="listAllOrgsTable"
        self.list_all_org_table = TableUtils(page, "#listAllOrgsTable")

        # List All Site links
        self.select_site_type = self.page.locator("#siteTypeId")
        self.create_new_site = self.page.get_by_role("button", name="Create New Site")
        self.site_code = self.page.locator('input[name="SITE_CODE"]')

    def select_site_type_option(self, option: str) -> None:
        """
        This method is designed to select a specific site type from the List All Sites page.
        """
        self.select_site_type.select_option(option)

    def click_create_new_site(self) -> None:
        """Clicks the 'Create New Site' button."""
        self.click(self.create_new_site)

    def search_site_code(self, site_code: str) -> None:
        """
        This method is designed to search for an site by its code.
        Args:
            site_code (str): The site code to search for.
        """
        logging.info(f"Searching for Site with code: {site_code}")
        self.site_code.fill(site_code)
        self.site_code.press("Enter")

    def verify_no_site_record_found(self, text: str) -> None:
        """Verifies that no site record is found."""
        logging.info("Verifying that no site record is found")
        expect(self.page.locator('form[name="frm"]')).to_contain_text(text)


class SiteType(StrEnum):
    CARE_TRUST_SITE = "1020"
    NHS_TRUST_SITE = "1018"
    PCT_SITE = "1019"
    PATHOLOGY_LABORATORY_SITE = "306448"
