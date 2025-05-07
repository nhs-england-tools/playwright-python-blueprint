import pytest
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.fit_test_kits.fit_test_kits_page import FITTestKitsPage
from pages.fit_test_kits.fit_rollout_summary_page import FITRolloutSummaryPage
from pages.fit_test_kits.log_devices_page import LogDevicesPage
from pages.fit_test_kits.view_fit_kit_result_page import ViewFITKitResultPage
from pages.fit_test_kits.kit_service_management_page import KitServiceManagementPage
from pages.fit_test_kits.kit_result_audit_page import KitResultAuditPage
from pages.fit_test_kits.view_algorithms_page import ViewAlgorithmsPage
from pages.fit_test_kits.view_screening_centre_fit_configuration_page import (
    ViewScreeningCentreFITConfigurationPage,
)
from pages.fit_test_kits.screening_incidents_list_page import ScreeningIncidentsListPage
from pages.fit_test_kits.manage_qc_products_page import ManageQCProductsPage
from pages.fit_test_kits.maintain_analysers_page import MaintainAnalysersPage
from utils.user_tools import UserTools


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as a test user and navigates to the
    fit test kits page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    # Go to fit test kits page
    BasePage(page).go_to_fit_test_kits_page()


@pytest.mark.smoke
def test_fit_test_kits_page_navigation(page: Page, general_properties: dict) -> None:
    """
    Confirms all menu items are displayed on the fit test kits page, and that the relevant pages
    are loaded when the links are clicked
    """
    # Verify FIT rollout summary page opens as expected
    FITTestKitsPage(page).go_to_fit_rollout_summary_page()
    FITRolloutSummaryPage(page).verify_fit_rollout_summary_body()
    BasePage(page).click_back_button()

    # Verify Log Devices page opens as expected
    FITTestKitsPage(page).go_to_log_devices_page()
    LogDevicesPage(page).verify_log_devices_title()
    BasePage(page).click_back_button()

    # Verify View FIT Kit Result page opens as expected
    FITTestKitsPage(page).go_to_view_fit_kit_result()
    ViewFITKitResultPage(page).verify_view_fit_kit_result_body()
    BasePage(page).click_back_button()

    # Verify Kit Service Management page opens as expected
    FITTestKitsPage(page).go_to_kit_service_management()
    KitServiceManagementPage(page).verify_kit_service_management_title()
    BasePage(page).click_back_button()

    # Verify Kit Result Audit page opens as expected
    FITTestKitsPage(page).go_to_kit_result_audit()
    KitResultAuditPage(page).verify_kit_result_audit_title()
    BasePage(page).click_back_button()

    # Verify View Algorithm page opens as expected
    FITTestKitsPage(page).go_to_view_algorithm()
    ViewAlgorithmsPage(page).verify_view_algorithms_body()
    BasePage(page).click_back_button()

    # Verify View Screening Centre FIT page opens as expected
    FITTestKitsPage(page).go_to_view_screening_centre_fit()
    FITTestKitsPage(
        page
    ).sc_fit_configuration_page_screening_centre_dropdown.select_option(
        general_properties["coventry_and_warwickshire_bcs_centre"]
    )
    ViewScreeningCentreFITConfigurationPage(
        page
    ).verify_view_screening_centre_fit_title()
    BasePage(page).click_back_button()  # Go back to the Select Screening Centre page
    BasePage(page).click_back_button()  # Go back to the FIT Test Kits page

    # Verify Screening Incidents List page opens as expected
    FITTestKitsPage(page).go_to_screening_incidents_list()
    ScreeningIncidentsListPage(page).verify_screening_incidents_list_title()
    BasePage(page).click_back_button()

    # Verify FIT QC Products page opens as expected
    FITTestKitsPage(page).go_to_manage_qc_products()
    ManageQCProductsPage(page).verify_manage_qc_products_title()
    BasePage(page).click_back_button()

    # Verify Maintain Analysers page opens as expected
    FITTestKitsPage(page).go_to_maintain_analysers()
    MaintainAnalysersPage(page).verify_maintain_analysers_title()
    BasePage(page).click_back_button()
    FITTestKitsPage(page).verify_fit_test_kits_title()

    # Return to main menu
    BasePage(page).click_main_menu_link()
    BasePage(page).main_menu_header_is_displayed()
