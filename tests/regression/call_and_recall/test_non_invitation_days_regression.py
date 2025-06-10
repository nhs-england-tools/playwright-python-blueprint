import pytest
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.call_and_recall.call_and_recall_page import CallAndRecallPage
from pages.call_and_recall.non_invitations_days_page import NonInvitationDaysPage
from utils.user_tools import UserTools


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as a test user and navigates to the call and recall page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager at BCS02")

    # Go to call and recall page
    BasePage(page).go_to_call_and_recall_page()


@pytest.mark.regression
@pytest.mark.call_and_recall
def test_add_then_delete_non_invitation_day(page: Page) -> None:
    """
    Verifies that a user can add and delete a non-invitation day.
    """
    # Scenario: Add then delete a non invitation day
    # And I go to "Non-Invitation Days"
    CallAndRecallPage(page).go_to_non_invitation_days_page()

    # # The date entered should be a week day, otherwise a warning message will pop up
    # When I enter "14/11/2030" in the input box with id "date"
    NonInvitationDaysPage(page).enter_date("14/11/2030")
    # # Add a new non invitation day
    # And I enter "Add a non invitation day for automated test" in the input box with id "note"
    NonInvitationDaysPage(page).enter_note(
        "Add a non-invitation day for automated test"
    )

    # And I click the "Add Non-Invitation Day" button
    NonInvitationDaysPage(page).click_add_non_invitation_day_button()
    # Then todays date is visible in the non-invitation days table
    NonInvitationDaysPage(page).verify_date_is_visible()
    # When I click the delete button for the non-invitation day
    # NonInvitationDaysPage(page).click_delete_button() TODO: this step should be executed as part of the next step (delete this step once confirmed working)
    # And I press OK on my confirmation prompt
    BasePage(page).safe_accept_dialog(page.get_by_role("button", name="Delete"))
    # Then todays date is not visible in the non-invitation days table
    NonInvitationDaysPage(page).verify_date_is_not_visible()


@pytest.mark.regression
@pytest.mark.call_and_recall
def test_non_invitation_day_note_is_mandatory(page: Page) -> None:
    """
    Verifies that a note is required when adding a non-invitation day.
    """
    # And I go to "Non-Invitation Days"
    CallAndRecallPage(page).go_to_non_invitation_days_page()
    # When I enter "14/11/2030" in the input box with id "date"
    NonInvitationDaysPage(page).enter_date("14/11/2030")
    # And I click the "Add Non-Invitation Day" button
    NonInvitationDaysPage(page).click_add_non_invitation_day_button()
    # Then I get an alert message that "contains" "The Note field is mandatory"
    BasePage(page).assert_dialog_text("The Note field is mandatory")
