import pytest
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.call_and_recall.call_and_recall_page import CallAndRecallPage
from pages.call_and_recall.invitations_monitoring_page import InvitationsMonitoringPage
from pages.call_and_recall.invitations_plans_page import InvitationsPlansPage
from pages.call_and_recall.create_a_plan_page import CreateAPlanPage
from utils.user_tools import UserTools


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as a test user and navigates to the call and recall page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    # Go to call and recall page
    BasePage(page).go_to_call_and_recall_page()


@pytest.mark.regression
@pytest.mark.call_and_recall
def test_create_a_plan_set_daily_rate(page: Page, general_properties: dict) -> None:
    """
    Verifies that a user is able to click on the Set all button and enter a daily rate.
    """
    # When I go to "Invitations Monitoring - Screening Centre"
    CallAndRecallPage(page).go_to_planning_and_monitoring_page()

    # And I click the link text "BCS001"
    InvitationsMonitoringPage(page).go_to_invitation_plan_page(
        general_properties["screening_centre_code"]
    )
    # And I click the "Create a Plan" button
    InvitationsPlansPage(page).go_to_create_a_plan_page()

    # And I click the set all button
    CreateAPlanPage(page).click_set_all_button()

    # And I enter "28" in the input box with id "dailyRate"
    CreateAPlanPage(page).fill_daily_invitation_rate_field(
        general_properties["daily_invitation_rate"]
    )

    # And I click the "Update" button
    CreateAPlanPage(page).click_update_button()

    # Then the Weekly Invitation Rate for weeks 1 to 50 is set correctly
    # based on a set all daily rate of 28
    CreateAPlanPage(page).verify_weekly_invitation_rate_for_weeks(1, 50, "140")


@pytest.mark.regression
@pytest.mark.call_and_recall
def test_create_a_plan_weekly_rate(page: Page, general_properties: dict) -> None:
    """
    Verifies that a user can set a weekly invitation rate in Create a Plan.
    """

    # When I go to "Invitations Monitoring - Screening Centre"
    CallAndRecallPage(page).go_to_planning_and_monitoring_page()

    # And I click the link text "BCS001"
    InvitationsMonitoringPage(page).go_to_invitation_plan_page(
        general_properties["screening_centre_code"]
    )
    # And I click the "Create a Plan" button
    InvitationsPlansPage(page).go_to_create_a_plan_page()

    # And I click the set all button
    CreateAPlanPage(page).click_set_all_button()

    # And I enter "130" in the input box with id "weeklyRate"
    CreateAPlanPage(page).fill_weekly_invitation_rate_field(
        general_properties["weekly_invitation_rate"]
    )

    # And I click the "Update" button
    CreateAPlanPage(page).click_update_button()

    # And the Weekly Invitation Rate for weeks 1 to 50 is set to the set all weekly rate of 130
    CreateAPlanPage(page).verify_weekly_invitation_rate_for_weeks(1, 50, "130")


@pytest.mark.regression
@pytest.mark.call_and_recall
def test_update_invitation_rate_weekly(page: Page, general_properties: dict) -> None:
    """
    Verifies that a Hub Manager State Registered is able to update a weekly Invitation rate
    and the Cumulative 'Invitations sent' and 'Resulting Position' values are updated.
    """

    # When I go to "Invitations Monitoring - Screening Centre"
    CallAndRecallPage(page).go_to_planning_and_monitoring_page()

    # And I click the link text "BCS001"
    InvitationsMonitoringPage(page).go_to_invitation_plan_page(
        general_properties["screening_centre_code"]
    )

    # And I click the "Create a Plan" button
    InvitationsPlansPage(page).go_to_create_a_plan_page()

    # When I increase the Weekly Invitation Rate for week 1 by 1 and tab out of the cell
    # Then the Cumulative Invitations Sent is incremented by 1 for week 1
    # And the Cumulative Resulting Position is incremented by 1 for week 1
    CreateAPlanPage(page).increment_invitation_rate_and_verify_changes()
