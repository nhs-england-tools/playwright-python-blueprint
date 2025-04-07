import pytest
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.bowel_scope.bowel_scope_page import BowelScope
from pages.bowel_scope.bowel_scope_appointments_page import BowelScopeAppointments
from utils.user_tools import UserTools


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as a test user and navigates to the bowel scope page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager State Registered")

    # Go to bowel scope page
    BasePage(page).go_to_bowel_scope_page()


@pytest.mark.smoke
def test_bowel_scope_page_navigation(page: Page) -> None:
    """
    Confirms that the bowel scope appointments page loads, the appointments calendar is displayed and the
    main menu button returns the user to the main menu
    """
    # Bowel scope appointments page loads as expected
    BowelScope(page).go_to_bowel_scope_page()
    BowelScopeAppointments(page).verify_page_title()

    # Return to main menu
    BasePage(page).click_main_menu_link()
    BasePage(page).main_menu_header_is_displayed()
