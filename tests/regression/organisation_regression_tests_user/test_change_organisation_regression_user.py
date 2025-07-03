import pytest
import logging
from utils.user_tools import UserTools
from playwright.sync_api import Page
from pages.organisations.organisations_page import OrganisationSwitchPage


@pytest.mark.regression
def test_user_can_switch_between_organisations(page: Page) -> None:
    """
    Feature: Change Organisation
    Scenario: Check that an English user with multiple organisations is able to switch between them
    Given I log in to BCSS "England" as user role "MultiOrgUser"
    When I change organisation
    Then I will be logged in as the alternative organisation.
    """

    # Log in as a user with multiple organisations
    UserTools.user_login(page, "Specialist Screening Practitioner at BCS009 & BCS001")
    org_switch_page = OrganisationSwitchPage(page)

    # Get the list of available organisation IDs
    org_ids = org_switch_page.get_available_organisation_ids()

    # Select available organisations in turn and verify the switch
    for org_id in org_ids:
        # Select the organisation
        org_switch_page.select_organisation_by_id(org_id)

        # Click continue
        org_switch_page.click_continue()

        # Assert logged-in org matches expected
        login_text = org_switch_page.get_logged_in_text()
        logging.info(f"The user's current organisation is: {login_text}")
        assert (
            org_id in login_text
        ), f"Expected to be logged in as '{org_id}', but got: {login_text}"

        # Return to selection screen
        org_switch_page.click_select_org_link()
