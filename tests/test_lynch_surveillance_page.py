import pytest
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.lynch_surveillance.lynch_invitation_page import LynchInvitationPage
from pages.lynch_surveillance.set_lynch_invitation_rates_page import SetLynchInvitationRatesPage
from utils.user_tools import UserTools


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as a test user and navigates to the
    lynch surveillance page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    # Go to Lynch Surveillance page
    BasePage(page).go_to_lynch_surveillance_page()


@pytest.mark.smoke
def test_lynch_surveillance_page_navigation(page: Page) -> None:
    """
    Confirms that the 'set lynch invitation rates' link is visible and clickable, and navigates to the
    expected page when clicked
    """
    # 'Set lynch invitation rates' page loads as expected
    LynchInvitationPage(page).click_set_lynch_invitation_rates_link()
    SetLynchInvitationRatesPage(page).verify_set_lynch_invitation_rates_title()

    # Return to main menu
    BasePage(page).click_main_menu_link()
    BasePage(page).main_menu_header_is_displayed()
