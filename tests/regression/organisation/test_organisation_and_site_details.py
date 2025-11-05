import pytest
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.organisations import organisations_and_site_details_page
from pages.organisations.organisations_page import OrganisationsPage
from pages.organisations.organisations_and_site_details_page import (
    OrganisationsAndSiteDetailsPage,
)
from pages.organisations.list_all_organisations_page import (
    ListAllOrganisationsPage,
    OrganisationType,
)
from pages.organisations.create_organisation_page import CreateOrganisationPage
from pages.organisations.view_organisation_page import ViewOrganisationPage
from pages.organisations.list_all_sites_page import ListAllSitesPage, SiteType
from pages.organisations.create_site_page import CreateSitePage
from utils.user_tools import UserTools
from utils.table_util import TableUtils
from utils.calendar_picker import CalendarPicker
from utils.oracle.oracle_specific_functions.organisation import (
    delete_organisations_created_for_test,
    delete_sites_created_for_test,
)
from datetime import datetime


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as a test user and navigates to the call and recall page
    """
    # Log in to BCSS
    UserTools.user_login(page, "BCSS Bureau Staff")

    # Go to call and recall page
    BasePage(page).go_to_organisations_page()


# Define constants for repeated values
ICB_ORGANISATION_CODE = "Z9Z1S"
NHS_TRUST_SITE_CODE = "Z9Z1X"


@pytest.mark.regression
@pytest.mark.organisations_users_and_contacts_tests
@pytest.mark.organisations_and_contacts_build_level_tests
def test_check_list_all_organisations_page(page) -> None:
    """
    Verifies that the 'List All Organisations' page displays correctly and contains expected elements.
    """
    OrganisationsPage(page).go_to_organisations_and_site_details_page()
    OrganisationsAndSiteDetailsPage(page).go_to_list_all_organisations()
    ListAllOrganisationsPage(page).select_organisation_type_option(OrganisationType.ICB)
    ListAllOrganisationsPage(page).click_first_link_in_table()
    ViewOrganisationPage(page).verify_page_title()


@pytest.mark.regression
@pytest.mark.organisations_users_and_contacts_tests
@pytest.mark.organisations_and_contacts_develop_level_tests
def test_create_new_icb_z9z1s_using_create_new_org(page) -> None:
    """
    Verifies that the 'Create New Organisation' functionality works correctly for creating a new ICB organisation.
    """
    OrganisationsPage(page).go_to_organisations_and_site_details_page()
    OrganisationsAndSiteDetailsPage(page).go_to_list_all_organisations()
    ListAllOrganisationsPage(page).select_organisation_type_option(OrganisationType.ICB)
    ListAllOrganisationsPage(page).click_create_new_org()
    CreateOrganisationPage(page).organisation_code.fill(ICB_ORGANISATION_CODE)
    CreateOrganisationPage(page).organisation_name.fill("Test ANANA ICB")
    CreateOrganisationPage(page).click_start_date_calendar()
    CalendarPicker(page).select_day(datetime.today())
    CreateOrganisationPage(page).audit_reason.fill("Automated ANANA Test ")
    CreateOrganisationPage(page).click_save_button()
    CreateOrganisationPage(page).verify_success_message()


@pytest.mark.regression
@pytest.mark.organisations_users_and_contacts_tests
@pytest.mark.organisations_and_contacts_develop_level_tests
def test_create_new_nhs_trust_site_z9z1x_using_create_site(page) -> None:
    """
    Verifies that the 'Create New Site' functionality works correctly for creating a new NHS Trust site.
    """
    OrganisationsPage(page).go_to_organisations_and_site_details_page()
    OrganisationsAndSiteDetailsPage(page).go_to_list_all_sites()
    ListAllSitesPage(page).select_site_type_option(SiteType.NHS_TRUST_SITE)
    ListAllSitesPage(page).click_create_new_site()
    CreateSitePage(page).fill_site_code(NHS_TRUST_SITE_CODE)
    CreateSitePage(page).fill_site_name("TEST ANANA NHS TRUST SITE")
    CreateSitePage(page).click_start_date_calendar()
    CalendarPicker(page).select_day(datetime.today())
    CreateSitePage(page).fill_audit_reason("Automated ANANA Test")
    CreateSitePage(page).click_save_button()
    CreateSitePage(page).verify_success_message()


@pytest.mark.regression
@pytest.mark.organisations_users_and_contacts_tests
@pytest.mark.organisations_and_contacts_develop_level_tests
def test_view_and_edit_organisation_values_z9z1s(page) -> None:
    """
    Verifies that the 'View and Edit Organisation' functionality works correctly for an existing ICB organisation.
    """
    OrganisationsPage(page).go_to_organisations_and_site_details_page()
    OrganisationsAndSiteDetailsPage(page).go_to_list_all_organisations()
    ListAllOrganisationsPage(page).select_organisation_type_option(OrganisationType.ICB)
    ListAllOrganisationsPage(page).search_organisation_code(ICB_ORGANISATION_CODE)
    ListAllOrganisationsPage(page).click_first_link_in_table()
    ViewOrganisationPage(page).verify_organisation_type_details(ICB_ORGANISATION_CODE)
    ViewOrganisationPage(page).verify_organisation_code_details("ICB")
    ViewOrganisationPage(page).click_edit_button()
    ViewOrganisationPage(page).verify_organisation_type_details(ICB_ORGANISATION_CODE)
    ViewOrganisationPage(page).verify_organisation_code_details("ICB")


@pytest.mark.regression
@pytest.mark.organisations_users_and_contacts_tests
@pytest.mark.organisations_and_contacts_develop_level_tests
def test_remove_all_created_organisation(page) -> None:
    """
    Verifies that the 'Remove All Created Organisation' functionality works correctly
    """
    OrganisationsPage(page).go_to_organisations_and_site_details_page()
    delete_organisations_created_for_test([ICB_ORGANISATION_CODE])
    OrganisationsAndSiteDetailsPage(page).go_to_list_all_organisations()
    ListAllOrganisationsPage(page).select_organisation_type_option(OrganisationType.CCG)
    ListAllOrganisationsPage(page).search_organisation_code(NHS_TRUST_SITE_CODE)
    ListAllOrganisationsPage(page).verify_no_organisation_record_found(
        "Sorry, no records match your search criteria. Please refine your search and try again."
    )


@pytest.mark.regression
@pytest.mark.organisations_users_and_contacts_tests
@pytest.mark.organisations_and_contacts_develop_level_tests
def test_remove_all_created_sites(page) -> None:
    """
    Verifies that the 'Remove All Created Sites' functionality works correctly
    """
    OrganisationsPage(page).go_to_organisations_and_site_details_page()
    delete_sites_created_for_test([NHS_TRUST_SITE_CODE])
    OrganisationsAndSiteDetailsPage(page).go_to_list_all_sites()
    ListAllSitesPage(page).select_site_type_option(SiteType.NHS_TRUST_SITE)
    ListAllSitesPage(page).search_site_code(NHS_TRUST_SITE_CODE)
    ListAllSitesPage(page).verify_no_site_record_found(
        "Sorry, no records match your search criteria. Please refine your search and try again."
    )
