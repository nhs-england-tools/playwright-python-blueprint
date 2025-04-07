import pytest
from sys import platform
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.call_and_recall.call_and_recall_page import CallAndRecall
from pages.call_and_recall.invitations_monitoring_page import InvitationsMonitoring
from pages.call_and_recall.generate_invitations_page import GenerateInvitations
from pages.call_and_recall.non_invitations_days_page import NonInvitationDays
from pages.call_and_recall.age_extension_rollout_plans_page import AgeExtensionRolloutPlans
from pages.call_and_recall.invitations_plans_page import InvitationsPlans
from pages.call_and_recall.create_a_plan_page import CreateAPlan
from utils.user_tools import UserTools
from jproperties import Properties


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
    Before every test is executed, this fixture logs in to BCSS as a test user and navigates to the call and recall page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager State Registered")

    # Go to call and recall page
    BasePage(page).go_to_call_and_recall_page()


@pytest.mark.smoke
def test_call_and_recall_page_navigation(page: Page) -> None:
    """
    Confirms that the Call and Recall menu displays all menu options and confirms they load the correct pages
    """
    # Planning and monitoring page loads as expected
    CallAndRecall(page).go_to_planning_and_monitoring_page()
    InvitationsMonitoring(page).verify_invitations_monitoring_title()
    BasePage(page).click_back_button()

    # Generate invitations page loads as expected
    CallAndRecall(page).go_to_generate_invitations_page()
    GenerateInvitations(page).verify_generate_invitations_title()
    BasePage(page).click_back_button()

    # Invitation generation progress page loads as expected
    CallAndRecall(page).go_to_invitation_generation_progress_page()
    GenerateInvitations(page).verify_invitation_generation_progress_title()
    BasePage(page).click_back_button()

    # Non invitation days page loads as expected
    CallAndRecall(page).go_to_non_invitation_days_page()
    NonInvitationDays(page).verify_non_invitation_days_tile()
    BasePage(page).click_back_button()

    # Age extension rollout page loads as expected
    CallAndRecall(page).go_to_age_extension_rollout_plans_page()
    AgeExtensionRolloutPlans(page).verify_age_extension_rollout_plans_title()
    BasePage(page).click_back_button()

    # Return to main menu
    BasePage(page).click_main_menu_link()
    BasePage(page).main_menu_header_is_displayed()


def test_view_an_invitation_plan(page: Page, tests_properties: dict) -> None:
    """
    Confirms that an invitation plan can be viewed via a screening centre from the planning ad monitoring page
    """
    # Go to planning and monitoring page
    CallAndRecall(page).go_to_planning_and_monitoring_page()

    # Select a screening centre
    InvitationsMonitoring(page).go_to_invitation_plan_page(
        tests_properties["screening_centre_code"]
    )

    # Select an invitation plan
    InvitationsPlans(page).go_to_first_available_plan()

    # Verify invitation page is displayed
    CreateAPlan(page).verify_create_a_plan_title()
