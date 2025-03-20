import pytest
from playwright.sync_api import Page, expect
from pages.bcss_home_page import MainMenu
from utils.user_tools import UserTools


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as the specified user and navigates to the bowel scope page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager State Registered")

    # Go to bowel scope page
    MainMenu(page).go_to_bowel_scope_page()


@pytest.mark.smoke
def test_bowel_scope_page_navigation(page: Page) -> None:
    """
    Confirms that the bowel scope appointments page loads, the appointments calendar is displayed and the
    main menu button returns the user to the main menu
    """
    # Bowel scope appointments page loads as expected
    page.get_by_role("link", name="View Bowel Scope Appointments").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Appointment Calendar")

    # Return to main menu
    page.get_by_role("link", name="Main Menu").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Main Menu")
