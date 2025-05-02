from playwright.sync_api import Page
from pages.base_page import BasePage


class OrganisationsPage(BasePage):
    """Organisations Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # Organisations page links
        self.screening_centre_parameters_page = self.page.get_by_role(
            "link", name="Screening Centre Parameters"
        )
        self.organisation_parameters_page = self.page.get_by_role(
            "link", name="Organisation Parameters"
        )
        self.organisations_and_site_details_page = self.page.get_by_role(
            "link", name="Organisation and Site Details"
        )
        self.gp_practice_endorsement_page = self.page.get_by_role(
            "link", name="GP Practice Endorsement"
        )
        self.upload_nacs_data_bureau_page = self.page.get_by_role(
            "link", name="Upload NACS data (Bureau)"
        )
        self.bureau_page = self.page.get_by_role("link", name="Bureau")

    def go_to_screening_centre_parameters_page(self) -> None:
        """Clicks the 'Screening Centre Parameters' link."""
        self.click(self.screening_centre_parameters_page)

    def go_to_organisation_parameters_page(self) -> None:
        """Clicks the 'Organisation Parameters' link."""
        self.click(self.organisation_parameters_page)

    def go_to_organisations_and_site_details_page(self) -> None:
        """Clicks the 'Organisation and Site Details' link."""
        self.click(self.organisations_and_site_details_page)

    def go_to_gp_practice_endorsement_page(self) -> None:
        """Clicks the 'GP Practice Endorsement' link."""
        self.click(self.gp_practice_endorsement_page)

    def go_to_upload_nacs_data_bureau_page(self) -> None:
        """Clicks the 'Upload NACS data (Bureau)' link."""
        self.click(self.upload_nacs_data_bureau_page)

    def go_to_bureau_page(self) -> None:
        """Clicks the 'Bureau' link."""
        self.click(self.bureau_page)
