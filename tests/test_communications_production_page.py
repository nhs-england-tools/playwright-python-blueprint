import pytest
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.communications_production_page import CommunicationsProduction
from pages.batch_list_page import ActiveBatchList,ArchivedBatchList
from pages.letter_library_index_page import LetterLibraryIndex
from pages.letter_signatory_page import LetterSignatory
from pages.electronic_communications_management import ElectronicCommunicationManagement
from utils.user_tools import UserTools


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as a test user and navigates to the communications
    production page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager State Registered")

    # Go to communications production page
    BasePage(page).go_to_communications_production_page()


@pytest.mark.smoke
def test_communications_production_page_navigation(page: Page) -> None:
    """
    Confirms all menu items are displayed on the communications production page, and that the relevant pages
    are loaded when the links are clicked
    """
    # Active batch list page loads as expected
    CommunicationsProduction(page).go_to_active_batch_list_page()
    ActiveBatchList(page).verify_batch_list_page_title("Active Batch List")
    BasePage(page).click_back_button()

    # Archived batch list page loads as expected
    CommunicationsProduction(page).go_to_archived_batch_list_page()
    ArchivedBatchList(page).verify_batch_list_page_title("Archived Batch List")
    BasePage(page).click_back_button()

    # Letter library index page loads as expected
    CommunicationsProduction(page).go_to_letter_library_index_page()
    LetterLibraryIndex(page).verify_letter_library_index_title()
    BasePage(page).click_back_button()

    # Manage individual letter link is visible (not clickable due to user role permissions)
    CommunicationsProduction(page).verify_manage_individual_letter_page_visible()

    # Letter signatory page loads as expected
    CommunicationsProduction(page).go_to_letter_signatory_page()
    LetterSignatory(page).verify_letter_signatory_title()
    BasePage(page).click_back_button()

    # Electronic communication management page loads as expected
    CommunicationsProduction(page).go_to_electronic_communication_management_page()
    ElectronicCommunicationManagement(page).verify_electronic_communication_management_title()

    # Return to main menu
    # main_menu_link = page.get_by_role("link", name="Main Menu")
    BasePage(page).click_main_menu_link()
    BasePage(page).main_menu_header_is_displayed()
