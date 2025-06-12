import pytest
from playwright.sync_api import Page
import logging
from pages.base_page import BasePage
from pages.call_and_recall.call_and_recall_page import CallAndRecallPage
from pages.call_and_recall.generate_invitations_page import GenerateInvitationsPage
from pages.communication_production.batch_list_page import BatchListPage
from pages.communication_production.communications_production_page import (
    CommunicationsProductionPage,
)
from pages.communication_production.manage_active_batch_page import (
    ManageActiveBatchPage,
)
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


@pytest.mark.regression
@pytest.mark.call_and_recall
def test_run_fobt_invitations_and_process_s1_batch(
    page: Page, general_properties: dict
):
    """
    Run FOBT invitations, open the S1 batch, prepare, retrieve and confirm.
    """
    # Navigate to generate invitations
    CallAndRecallPage(page).go_to_generate_invitations_page()

    # When I generate invitations
    logging.info("Generating invitations based on the invitation plan")
    GenerateInvitationsPage(page).click_generate_invitations_button()
    GenerateInvitationsPage(page).wait_for_invitation_generation_complete(
        int(general_properties["daily_invitation_rate"])
    )
    logging.info("Invitations generated successfully")

    # And I view the active batch list
    BasePage(page).click_main_menu_link()
    BasePage(page).go_to_communications_production_page()
    CommunicationsProductionPage(page).go_to_active_batch_list_page()

    # And I open the "Original" / "Open" / "S1" / "Pre-invitation (FIT)" batch
    BatchListPage(page).open_letter_batch(
        batch_type="Original",
        status="Open",
        level="S1",
        description="Pre-invitation (FIT)",
    )

    # Then I retrieve and confirm the letters
    ManageActiveBatchPage(page).click_prepare_button()
    ManageActiveBatchPage(page).click_retrieve_button()
    BasePage(page).safe_accept_dialog(
        page.get_by_role("button", name="Confirm Printed")
    )  # Click the confirm button and accept the confirmation dialog
