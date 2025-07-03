from playwright.sync_api import Page
from pages.base_page import BasePage
from typing import List

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

class OrganisationSwitchPage:
    """Page Object Model for interacting with the Organisation Switch page."""

    def __init__(self, page: Page):
        """
        Initializes the OrganisationSwitchPage with locators for key elements.

        Args:
            page (Page): The Playwright Page object representing the browser page.
        """
        self.page = page
        self.radio_buttons = self.page.locator("input[type='radio']")
        self.selected_radio = self.page.locator("input[name='organisation']:checked")
        self.continue_button = self.page.get_by_role("button", name="Continue")
        self.select_org_link = self.page.get_by_role("link", name="Select Org")
        self.login_info = self.page.locator("td.loginInfo")

    def click(self, locator) -> None:
        """
        Clicks the given locator element.

        Args:
            locator: A Playwright Locator object to be clicked.
        """
        locator.click()

    def get_available_organisation_ids(self) -> List[str]:
        """
        Retrieves the list of available organisation IDs from the radio button on the page.

        Returns:
            List[str]: A list of organisation ID strings.
        """
        org_ids = []
        count = self.radio_buttons.count()
        for element in range(count):
            org_id = self.radio_buttons.nth(element).get_attribute("id")
            if org_id:
                org_ids.append(org_id)
        return org_ids

    def select_organisation_by_id(self, org_id: str) -> None:
        """
        Selects an organisation radio button by its ID.

        Args:
            org_id (str): The ID of the organisation to select.
        """
        self.click(self.page.locator(f"#{org_id}"))

    def click_continue(self) -> None:
        """
        Clicks the 'Continue' button on the page.
        """
        self.click(self.continue_button)

    def click_select_org_link(self) -> None:
        """
        Clicks the 'Select Org' link to return to the organisation selection page.
        """
        self.click(self.select_org_link)

    def get_logged_in_text(self) -> str:
        """
        Retrieves the logged-in user information from the login info section.

        Returns:
            str: The text indicating the logged-in user's role or name.
        """
        return self.login_info.inner_text()


