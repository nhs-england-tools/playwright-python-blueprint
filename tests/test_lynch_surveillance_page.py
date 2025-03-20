import pytest
from playwright.sync_api import Page, expect
from pages.bcss_home_page import MainMenu
from utils.user_tools import UserTools


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as the specified user and navigates to the
    lynch surveillance page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager State Registered")

    # Go to Lynch Surveillance page
    MainMenu(page).go_to_lynch_surveillance_page()


@pytest.mark.smoke
def test_lynch_surveillance_page_navigation(page: Page) -> None:
    """
    Confirms that the 'set lynch invitation rates' link is visible and clickable, and navigates to the
    expected page when clicked
    """
    # 'Set lynch invitation rates' page loads as expected
    page.get_by_role("link", name="Set Lynch Invitation Rates").click()
    expect(page.locator("#page-title")).to_contain_text("Set Lynch Surveillance Invitation Rates")

    # Return to main menu
    page.get_by_role("link", name="Main Menu").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Main Menu")
