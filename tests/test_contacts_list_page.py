import pytest
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.contacts_list.contacts_list_page import ContactsListPage
from pages.contacts_list.view_contacts_page import ViewContacts
from pages.contacts_list.edit_my_contact_details_page import EditMyContactDetails
from pages.contacts_list.maintain_contacts_page import MaintainContacts
from pages.contacts_list.my_preference_settings_page import MyPreferenceSettings
from utils.user_tools import UserTools


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as a test user and navigates to the contacts list page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    # Go to contacts list page
    BasePage(page).go_to_contacts_list_page()


@pytest.mark.smoke
def test_contacts_list_page_navigation(page: Page) -> None:
    """
    Confirms all menu items are displayed on the contacts list page, and that the relevant pages
    are loaded when the links are clicked
    """
    # View contacts page loads as expected
    ContactsListPage(page).go_to_view_contacts_page()
    ViewContacts(page).verify_view_contacts_title()
    BasePage(page).click_back_button()

    # Edit my contact details page loads as expected
    ContactsListPage(page).go_to_edit_my_contact_details_page()
    EditMyContactDetails(page).verify_edit_my_contact_details_title()
    BasePage(page).click_back_button()

    # Maintain contacts page loads as expected
    ContactsListPage(page).go_to_maintain_contacts_page()
    MaintainContacts(page).verify_maintain_contacts_title()
    BasePage(page).click_back_button()

    # My preference settings page loads as expected
    ContactsListPage(page).go_to_my_preference_settings_page()
    MyPreferenceSettings(page).verify_my_preference_settings_title()
    BasePage(page).click_back_button()

    # Other links are visible (Not clickable due to user role permissions)
    ContactsListPage(page).verify_extract_contact_details_page_visible()
    ContactsListPage(page).verify_resect_and_discard_accredited_page_visible()

    # Return to main menu
    BasePage(page).click_main_menu_link()
    BasePage(page).main_menu_header_is_displayed()
