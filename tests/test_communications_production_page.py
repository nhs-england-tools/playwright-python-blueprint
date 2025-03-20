import pytest
from playwright.sync_api import Page, expect
from utils.user_tools import UserTools
from pages.bcss_home_page import MainMenu


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as the specified user and navigates to the communications
    production page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager State Registered")

    # Go to communications production page
    MainMenu(page).go_to_communications_production_page()


@pytest.mark.smoke
def test_communications_production_page_navigation(page: Page) -> None:
    """
    Confirms all menu items are displayed on the communications production page, and that the relevant pages
    are loaded when the links are clicked
    """
    # Active batch list page loads as expected
    page.get_by_role("link", name="Active Batch List").click()
    expect(page.locator("#page-title")).to_contain_text("Active Batch List")
    page.get_by_role("link", name="Back").click()

    # Archived batch list page loads as expected
    page.get_by_role("link", name="Archived Batch List").click()
    expect(page.locator("#page-title")).to_contain_text("Archived Batch List")
    page.get_by_role("link", name="Back").click()

    # Letter library index page loads as expected
    page.get_by_role("link", name="Letter Library Index").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Letter Library Index")
    page.get_by_role("link", name="Back", exact=True).click()

    # Manage individual letter link is visible (not clickable due to user role permissions)
    expect(page.get_by_text("Manage Individual Letter")).to_be_visible()

    # Letter signatory page loads as expected
    page.get_by_role("link", name="Letter Signatory").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Letter Signatory")
    page.get_by_role("link", name="Back").click()

    # Electronic communication management page loads as expected
    page.get_by_role("link", name="Electronic Communication").click()
    expect(page.locator("#page-title")).to_contain_text("Electronic Communication Management")

    # Return to main menu
    page.get_by_role("link", name="Main Menu").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Main Menu")
