from playwright.sync_api import Page
from pages.base_page import BasePage


class SurveillanceSummaryPage(BasePage):
    """Page object for navigating to and interacting with the Surveillance Review Summary section."""

    def __init__(self, page: Page):
        super().__init__(page)

        # Locators
        self.org_and_site_details_link = self.page.get_by_role(
            "link", name="Organisation and Site Details"
        )
        self.list_all_orgs_link = self.page.get_by_role(
            "link", name="List All Organisations"
        )
        self.list_all_sites_link = self.page.get_by_role("link", name="List All Sites")
        self.surveillance_link = self.page.get_by_role(
            "link", name="Surveillance", exact=True
        )
        self.manage_surveillance_review_link = self.page.get_by_role(
            "link", name="Manage Surveillance Review"
        )
        self.surveillance_review_summary_header = self.page.get_by_text(
            "Surveillance Review Summary"
        )
        self.back_link = self.page.get_by_role("link", name="Back", exact=True)

    def navigate_to_surveillance_review_summary(self):
        """Navigates through multiple UI steps to reach the Surveillance Review Summary section."""
        self.click(self.org_and_site_details_link)
        self.click(self.list_all_orgs_link)
        self.click(self.back_link)
        self.click(self.list_all_sites_link)
        for _ in range(3):
            self.click(self.back_link)
        self.click(self.surveillance_link)
        self.click(self.manage_surveillance_review_link)
