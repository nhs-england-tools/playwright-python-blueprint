import pytest
from playwright.sync_api import Page, expect
from pages.bcss_home_page import MainMenu
from utils.user_tools import UserTools


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as the specified user and navigates to the
    organisations page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager State Registered")

    # Go to organisations page
    MainMenu(page).go_to_organisations_page()


@pytest.mark.smoke
def test_organisations_page_navigation(page: Page) -> None:
    """
    Confirms all menu items are displayed on the organisations page, and that the relevant pages
    are loaded when the links are clicked
    """
    # Screening centre parameters page loads as expected
    page.get_by_role("link", name="Screening Centre Parameters").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Screening Centre Parameters")
    page.get_by_role("link", name="Back", exact=True).click()

    # Organisation parameters page loads as expected
    page.get_by_role("link", name="Organisation Parameters").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("System Parameters")
    page.get_by_role("link", name="Back", exact=True).click()

    # Organisation and site details page loads as expected
    page.get_by_role("link", name="Organisation and Site Details").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Organisation and Site Details")
    page.get_by_role("link", name="Back").click()

    # The links below are visible (not clickable due to user role permissions)
    expect(page.get_by_text("Upload NACS data (Bureau)")).to_be_visible()
    expect(page.get_by_text("Bureau", exact=True)).to_be_visible()

    # GP practice endorsement page loads as expected
    page.get_by_role("link", name="GP Practice Endorsement").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("GP Practice Endorsement")

    # Return to main menu
    page.get_by_role("link", name="Main Menu").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Main Menu")


def test_view_an_organisations_system_parameters(page: Page) -> None:
    """
    Confirms that an organisation's system parameters can be accessed and viewed
    """
    # Go to screening centre parameters page
    page.get_by_role("link", name="Screening Centre Parameters").click()

    # View an Organisation
    page.get_by_role("link", name="BCS001").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("System Parameters")
