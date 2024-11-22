import pytest
from playwright.sync_api import Page, expect

from pages.bcss_home_page import MainMenu
from pages.login_page import BcssLoginPage


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    # Log in to BCSS
    BcssLoginPage(page).login_as_user_bcss401()

    # Go to contacts list page
    MainMenu(page).go_to_contacts_list_page()


@pytest.mark.smoke
def test_contacts_list_page_navigation(page: Page) -> None:
    # View contacts page loads as expected
    page.get_by_role("link", name="View Contacts").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("View Contacts")
    page.get_by_role("link", name="Back", exact=True).click()

    # Edit my contact details page loads as expected
    page.get_by_role("link", name="Edit My Contact Details").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Edit My Contact Details")
    page.get_by_role("link", name="Back").click()

    # Maintain contacts page loads as expected
    page.get_by_role("link", name="Maintain Contacts").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Maintain Contacts")
    page.get_by_role("link", name="Back").click()

    # My preference settings page loads as expected
    page.get_by_role("link", name="My Preference Settings").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("My Preference Settings")
    page.get_by_role("link", name="Back").click()

    # Other links are visible (Not clickable due to user role permissions)
    expect(page.get_by_text("Extract Contact Details")).to_be_visible()
    expect(page.get_by_text("Resect and Discard Accredited")).to_be_visible()

    # Return to main menu
    page.get_by_role("link", name="Main Menu").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Main Menu")
