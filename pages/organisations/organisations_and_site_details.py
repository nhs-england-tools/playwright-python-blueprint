import logging
from playwright.sync_api import Page
from pages.base_page import BasePage


class OrganisationsAndSiteDetails(BasePage):
    """Organisations And Site Details Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # Organisations And Site Details Page links
        self.my_organisation = self.page.get_by_role("link", name="My Organisation")
        self.list_all_organisations = self.page.get_by_role(
            "link", name="List All Organisations"
        )
        self.list_all_sites = self.page.get_by_role("link", name="List All Sites")

    def go_to_my_organisation(self) -> None:
        """Clicks the 'my organisation' link"""
        logging.info("Navigating to My Organisation page")
        self.click(self.my_organisation)

    def go_to_list_all_organisations(self) -> None:
        """Clicks the 'list all organisations' link"""
        logging.info("Navigating to List All Organisations page")
        self.click(self.list_all_organisations)

    def go_to_list_all_sites(self) -> None:
        """Clicks the 'go to list all sites' link."""
        logging.info("Navigating to List All Sites page")
        self.click(self.list_all_sites)
