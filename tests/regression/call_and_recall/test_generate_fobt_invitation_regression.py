import pytest
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.call_and_recall.call_and_recall_page import CallAndRecallPage
from pages.call_and_recall.invitations_monitoring_page import InvitationsMonitoringPage
from pages.call_and_recall.generate_invitations_page import GenerateInvitationsPage
from pages.call_and_recall.non_invitations_days_page import NonInvitationDaysPage
from pages.call_and_recall.invitations_plans_page import InvitationsPlansPage
from pages.call_and_recall.create_a_plan_page import CreateAPlanPage
from utils.user_tools import UserTools


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as a test user and navigates to the call and recall page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager at BCS01")

    # Go to call and recall page
    BasePage(page).go_to_call_and_recall_page()


# Scenario: Run FOBT invitations and process the S1 letter batch
# Many feature scenarios need a subject at S9.
#     When I generate invitations
#     And I view the active batch list
#     And I view the "Original" type "Open" status active letter batch for "S1" "Pre-invitation (FIT)"
#     And I prepare the letter batch
#     And I retrieve and confirm the letters
#     Then there is a subject who meets the following criteria:
#         | Latest episode kit class  | FIT   |
#         | Latest event status       | S9    |
#         | Latest episode type       | FOBT  |
#         | Subject hub code          | BCS01 |

# Scenario: User generates invitations for screening episodes (#3)
# # Version copied from now-deleted UserPathway.feature - duplicate steps etc need to be sorted out
#     Given I log in to BCSS "England" as user role "Hub Manager - State Registered"
#     When I navigate to the Call and Recall > Generate Invitations Page
#     And I press the Generate Invitations button and generate invitations
#     Then Invitations are successfully generated


@pytest.mark.regression
@pytest.mark.call_and_recall
def test_generate_fobt_invitations(page: Page) -> None:
    """
    Verifies that a user can generate FOBT invitations and process the S1 letter batch.
    """
    CallAndRecallPage(page).go_to_generate_invitations_page()
    GenerateInvitationsPage(page).click_generate_invitations_button()

    GenerateInvitationsPage(page).view_active_batch_list()
    GenerateInvitationsPage(page).view_original_open_status_batch(
        "S1", "Pre-invitation (FIT)"
    )
    GenerateInvitationsPage(page).prepare_letter_batch()
    GenerateInvitationsPage(page).retrieve_and_confirm_letters()

    GenerateInvitationsPage(page).verify_subject_meets_criteria(
        kit_class="FIT", event_status="S9", episode_type="FOBT", hub_code="BCS01"
    )
