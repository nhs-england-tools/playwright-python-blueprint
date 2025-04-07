from sys import platform
import pytest
from jproperties import Properties
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.organisations.organisations_page import OrganisationsPage
from utils.user_tools import UserTools


@pytest.fixture
def tests_properties() -> dict:
    """
    Reads the 'bcss_tests.properties' file and populates a 'Properties' object.
    Returns a dictionary of properties for use in tests.

    Returns:
        dict: A dictionary containing the values loaded from the 'bcss_tests.properties' file.
    """
    configs = Properties()
    if platform == "win32":  # File path from content root is required on Windows OS
        with open("tests/bcss_tests.properties", "rb") as read_prop:
            configs.load(read_prop)
    elif platform == "darwin":  # Only the filename is required on macOS
        with open("bcss_tests.properties", "rb") as read_prop:
            configs.load(read_prop)
    return configs.properties


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as a test user and navigates to the
    organisations page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager State Registered")

    # Go to organisations page
    BasePage(page).go_to_organisations_page()


@pytest.mark.smoke
def test_organisations_page_navigation(page: Page) -> None:
    upload_nacs_data_bureau_link = page.get_by_text(
        "Upload NACS data (Bureau)", exact=True
    )
    bureau_page_link = page.get_by_text("Bureau", exact=True)
    """
    Confirms all menu items are displayed on the organisations page, and that the relevant pages
    are loaded when the links are clicked
    """
    # Screening centre parameters page loads as expected
    OrganisationsPage(page).go_to_screening_centre_parameters_page()
    BasePage(page).bowel_cancer_screening_ntsh_page_title_contains_text(
        "Screening Centre Parameters"
    )
    BasePage(page).click_back_button()

    # Organisation parameters page loads as expected
    OrganisationsPage(page).go_to_organisation_parameters_page()
    BasePage(page).bowel_cancer_screening_ntsh_page_title_contains_text(
        "System Parameters"
    )
    BasePage(page).click_back_button()

    # Organisation and site details page loads as expected
    OrganisationsPage(page).go_to_organisations_and_site_details_page()
    BasePage(page).bowel_cancer_screening_ntsh_page_title_contains_text(
        "Organisation and Site Details"
    )
    BasePage(page).click_back_button()

    # The links below are visible (not clickable due to user role permissions)
    expect(upload_nacs_data_bureau_link).to_be_visible()
    expect(bureau_page_link).to_be_visible()

    # GP practice endorsement page loads as expected
    OrganisationsPage(page).go_to_gp_practice_endorsement_page()
    BasePage(page).bowel_cancer_screening_ntsh_page_title_contains_text(
        "GP Practice Endorsement"
    )

    # Return to main menu
    BasePage(page).click_main_menu_link()
    BasePage(page).bowel_cancer_screening_ntsh_page_title_contains_text("Main Menu")


def test_view_an_organisations_system_parameters(
    page: Page, tests_properties: dict
) -> None:
    """
    Confirms that an organisation's system parameters can be accessed and viewed
    """
    # Go to screening centre parameters page
    OrganisationsPage(page).go_to_screening_centre_parameters_page()

    # View an Organisation
    page.get_by_role("link", name=tests_properties["screening_centre_code"]).click()
    BasePage(page).bowel_cancer_screening_ntsh_page_title_contains_text(
        "System Parameters"
    )
