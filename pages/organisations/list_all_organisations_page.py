import logging
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from enum import StrEnum
from utils.table_util import TableUtils


class ListAllOrganisationsPage(BasePage):
    """Organisations And Site Details Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        # Initialize TableUtils for the table with id="displayRS"
        self.list_all_org_table = TableUtils(page, "#listAllOrgsTable")

        # List All Organisations links
        self.select_organisation_type = self.page.locator("#organisationType")
        self.create_new_org = self.page.get_by_role("button", name="Create New Org")
        self.search_org_code = self.page.locator('input[name="ORG_CODE"]')

    def select_organisation_type_option(self, option: str) -> None:
        """
        This method is designed to select a specific organisation type from the List All Organisations page.
        Args:
            option (str): The organisation type option to be selected. This should be a string that matches one of the available options in the dropdown menu.
        """
        logging.info(f"Selecting Organisation Type: {option}")
        self.select_organisation_type.select_option(option)

    def click_first_link_in_table(self) -> None:
        """Clicks the first Org Code link from the List All Orgs table."""
        logging.info(
            "Clicking the first Org Code link in the List All Organisations table"
        )
        self.list_all_org_table.click_first_link_in_column("Org Code↑")

    def click_create_new_org(self) -> None:
        """Clicks the 'Create New Org' button."""
        logging.info("Clicking the 'Create New Org' button")
        self.click(self.create_new_org)

    def search_organisation_code(self, org_code: str) -> None:
        """
        This method is designed to search for an organisation by its code.
        Args:
            org_code (str): The organisation code to search for.
        """
        logging.info(f"Searching for Organisation with code: {org_code}")
        self.search_org_code.fill(org_code)
        self.search_org_code.press("Enter")

    def verify_no_organisation_record_found(self, text: str) -> None:
        """Verifies that no organisation record is found.
        Args:
            text (str): The text to verify is present indicating no records found. Example: "No organisation record found"
        """
        logging.info("Verifying that no organisation record is found")
        expect(self.page.locator('form[name="frm"]')).to_contain_text(text)


class OrganisationType(StrEnum):
    BCS_PROGRAMME_HUB = "1002"
    BCS_QA_TEAM = "202189"
    BCS_SCREENING_CENTRE = "1003"
    BCSS_SERVICE_MANAGER = "1036"
    CCG = "1006"
    CARE_TRUST = "1007"
    GP_PRACTICE = "1009"
    ICB = "1004"
    IT_CLUSTER = "1001"
    NHS_BOWEL_CANCER_SCREENING_PROGRAMME = "1000"
    NHS_TRUST = "1005"
    PUBLIC_HEALTH_ENGLAND = "202130"
