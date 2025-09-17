import pytest
import logging
import pandas as pd
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.call_and_recall.call_and_recall_page import CallAndRecallPage
from pages.call_and_recall.generate_invitations_page import GenerateInvitationsPage
from utils.user_tools import UserTools
from pages.screening_subject_search.subject_screening_search_page import (
    SubjectScreeningPage,
)
from utils.oracle.oracle import OracleDB, OracleSubjectTools
from classes.subject.subject import Subject
from utils.oracle.oracle import OracleSubjectTools
from pages.communication_production.communications_production_page import (
    CommunicationsProductionPage,
)
from pages.communication_production.batch_list_page import (
    ActiveBatchListPage,
    LetterBatchDetailsPage,
)
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from utils.table_util import TableUtils
from utils.oracle.oracle_specific_functions.subject_batch import (
    get_nhs_no_from_batch_id,
)
from utils import batch_processing
from utils import screening_subject_page_searcher


# Feature: FIT Self Refer - letter processing

# Narrative Description: When a self-referral subject is invited for FOBT screening, they are entered into
# an S83f letter batch.  This batch comprises the S83f and S83f-ATT letters, and the S83f-CSV (test kit) file.
# When the batch is prepared and confirmed, the subject is progressed to status S84, and links to both the S83f
# and S83f-ATT letters are displayed in their event history, in the S84 event.


# # NOTES (from the selenium tests):
# # This feature file assumes that the default kit type for all SC invitations is FIT, so all self-referrals will be sent a FIT kit.
# # Because the smokescreen tests also generate invitations, this feature file was consistently failing due to the invitations for
# # hub BCS01 being right up to date, i.e. no more invitations were allowed to be generated.  To fix this, this feature file has
# # been changed to use hub BCS02 instead.


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page) -> None:
    """
    Before every test is executed, this fixture logs in to BCSS as a test user and navigates to the call and recall page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager at BCS02")

    # Go to call and recall page
    BasePage(page).go_to_call_and_recall_page()


@pytest.mark.regression
@pytest.mark.letters_tests
def test_self_refer_subject_in_my_hub_for_fit(page: Page) -> None:
    """
    Scenario: Self-refer a subject in my hub for FIT
    Given I log in to BCSS "England" as user role "Hub Manager at BCS02"
    And there are "currently" "no" self-refer subjects ready to invite
    And I have a subject with no screening history who is eligible to self refer
    When I view the subject
    And I self refer the subject
    And I send a new kit to the subject
    And the FOBT invitations shortlist is refreshed
    Then there are "now" "some" self-refer subjects ready to invite
    """
    logging.info("[TEST START] Self-refer subject in my hub for FIT")
    user_role = "Hub Manager at BCS02"

    # Navigate to Generate Invitations page
    CallAndRecallPage(page).go_to_generate_invitations_page()
    logging.info("[NAVIGATION] Navigated to Generate Invitations page")

    # Retrieve hub info from users.json
    user_details = UserTools.retrieve_user(user_role)

    # Confirm no subjects ready to invite
    generate_invitations_page = GenerateInvitationsPage(page)
    generate_invitations_page.check_self_referral_subjects_ready("currently", "no")
    logging.info("[ASSERTION] Confirmed no self-referral subjects are ready")

    # Try to retrieve eligible subject from DB, fallback to create if none found
    # Convert user details dictionary into User object for easier handling
    user = UserTools.get_user_object(user_details)
    # Create empty Subject object to store subject details
    subject = Subject()

    try:
        # Attempt to find an existing eligible subject from the database
        nhs_number = generate_invitations_page.get_self_referral_eligible_subject(
            user, subject
        )
        logging.info(
            f"[SUBJECT FOUND] Retrieved eligible subject NHS number: {nhs_number}"
        )
        # Create DataFrame with NHS number to pass to timed events procedure
        nhs_df = pd.DataFrame({"subject_nhs_number": [nhs_number]})
        # Execute timed events procedure to process the subject
        OracleDB().exec_bcss_timed_events(nhs_df)
        logging.info("[TIMED EVENTS] Executed for existing subject")
    except RuntimeError:
        # If no eligible subject found, create a new one
        logging.warning("[SUBJECT NOT FOUND] Creating fallback subject")
        oracle_subject = OracleSubjectTools()
        # Create new subject in database with specified screening centre and age
        nhs_number = oracle_subject.create_self_referral_ready_subject(
            screening_centre=user_details["hub_code"], base_age=75
        )
        logging.info(f"[SUBJECT CREATED] Fallback subject NHS number: {nhs_number}")
        # Open the newly created subject record
        oracle_subject.open_subject_by_nhs(nhs_number)

    # Run stored procedure to include subject in invitation shortlist
    OracleDB().execute_stored_procedure("pkg_fobt_call.p_find_next_subjects_to_invite")
    logging.info(
        "[STORED PROCEDURE] Executed: pkg_fobt_call.p_find_next_subjects_to_invite"
    )

    # View subject
    base_page = BasePage(page)
    subject_screening_page = SubjectScreeningPage(page)
    base_page.click_main_menu_link()
    base_page.go_to_screening_subject_search_page()
    screening_subject_page_searcher.search_subject_by_nhs_number(page, nhs_number)
    logging.info("[SUBJECT VIEW] Subject loaded in UI")

    # Send new kit
    subject_screening_page.click_send_kit_button()
    subject_screening_page.complete_send_kit_form(
        request_from="Subject", previous_kit_status="Lost", note_text="Test"
    )
    logging.info("[KIT SENT] New kit dispatched")

    # Rebuild invitation shortlist to include self-referral subject
    # Arguments:
    # - pi_number_of_weeks: how far ahead to look for subjects (e.g. 20)
    # - pi_max_number_of_subjects: how many subjects to shortlist (e.g. 100)
    # - pi_hub_id and pi_sc_id: optional, but must be either both provided or both NULL
    OracleDB().execute_stored_procedure(
        "pkg_fobt_call.p_find_next_subjects_to_invite", [20, 100, None, None]
    )
    logging.info(
        "[STORED PROCEDURE] Executed: pkg_fobt_call.p_find_next_subjects_to_invite (20, 100, NULL, NULL)"
    )

    base_page.click_main_menu_link()
    base_page.go_to_call_and_recall_page()
    CallAndRecallPage(page).go_to_generate_invitations_page()

    # Use TableUtils to get the correct value dynamically
    table_utils = TableUtils(page, "#displayRS")

    try:
        self_referral_count_text = table_utils.get_footer_value_by_header(
            "Self Referrals"
        )
        self_referral_count = int(self_referral_count_text.strip())
        assert (
            self_referral_count > 0
        ), f"Expected self-referral count > 0 for BCS002, but got {self_referral_count}"
        logging.info(
            f"[ASSERTION PASSED] Self-referral count for BCS002 is now {self_referral_count}"
        )
    except Exception as e:
        pytest.fail(
            f"[ERROR] Unable to retrieve or assert Self Referrals count: {str(e)}"
        )


@pytest.mark.regression
@pytest.mark.letters_tests
def test_invite_self_referral_creates_s83f_batch(page: Page) -> None:
    """
    Scenario: Invite a self-refer subject for FIT creates or updates an S83f letter batch
    Given I log in to BCSS "England" as user role "HubManagerAtBCS02"
    And there are "currently" "some" self-refer subjects ready to invite
    When I generate invitations
    And I view the active batch list
    And I filter the active batch list to view only "Original" type batches
    And I filter the active batch list to view only "Open" status batches
    Then There is "now" a letter batch for "S83" "Invitation & Test Kit (Self-referral) (FIT)"
    """
    logging.info(
        "[TEST START] Invite self-referral creates or updates an S83f letter batch"
    )

    # Navigate to Generate Invitations page
    CallAndRecallPage(page).go_to_generate_invitations_page()
    logging.info("[NAVIGATION] Navigated to Generate Invitations page")

    # Confirm self-referral subjects are ready
    generate_invitations_page = GenerateInvitationsPage(page)
    generate_invitations_page.check_self_referral_subjects_ready("currently", "some")
    logging.info("[ASSERTION] Confirmed self-referral subjects are ready")

    # Generate invitations
    generate_invitations_page.click_generate_invitations_button()
    logging.info("[ACTION] Clicked Generate Invitations button")
    generate_invitations_page.wait_for_self_referral_invitation_generation_complete()
    logging.info("[WAIT] Invitation generation completed")

    # Navigate to Active Batch List
    base_page = BasePage(page)
    active_batch_page = ActiveBatchListPage(page)
    base_page.click_main_menu_link()
    base_page.go_to_communications_production_page()
    CommunicationsProductionPage(page).go_to_active_batch_list_page()
    logging.info("[NAVIGATION] Navigated to Active Batch List page")

    # Filter by "Original" type and "Open" status
    active_batch_page.enter_type_filter("Original")
    active_batch_page.enter_event_code_filter("S83")
    logging.info("[FILTER] Applied filters: Type='Original', Event Code='S83'")

    # Assert S83f batch is present
    active_batch_page.assert_s83f_batch_present()
    logging.info("[ASSERTION PASSED] S83f batch is present in Active Batch List")


# # Note that this "When I view ..." includes 3 steps from above (view active batch list, and filter by type and status), and clicks the batch ID link
@pytest.mark.regression
@pytest.mark.letters_tests
def test_s83f_letter_batch_has_three_components(page: Page) -> None:
    """
    Scenario: There are 3 components in the S83f letter batch
    Given I log in to BCSS "England" as user role "HubManagerAtBCS02"
    When I view the active batch list
    And I view the "Original" type "Open" status active letter batch for "S83" "Invitation & Test Kit (Self-referral) (FIT)"
    Then letter type "Invitation & Test Kit (Self-referral) (FIT)" with file format "PDF-A4-V03" is listed
    And letter type "Pre-invitation (Self-referral) (FIT)" with file format "PDF-A4-V03" is listed
    And letter type "Invitation & Test Kit (Self-referral) (FIT)" with file format "FIT-KIT-CSV" is listed
    """
    logging.info("[TEST START] S83f letter batch has three components")

    # Navigate to Active Batch List and filter
    base_page = BasePage(page)
    active_batch_page = ActiveBatchListPage(page)
    base_page.click_main_menu_link()
    base_page.go_to_communications_production_page()
    CommunicationsProductionPage(page).go_to_active_batch_list_page()

    # Filter by "Original" type, "S83" event code, and description
    logging.info("[NAVIGATION] Navigated to Active Batch List page")
    active_batch_page.enter_type_filter("Original")
    active_batch_page.enter_event_code_filter("S83")
    active_batch_page.enter_description_filter(
        "Invitation & Test Kit (Self-referral) (FIT)"
    )
    logging.info(
        "[FILTER] Applied filters: Type='Original', Event Code='S83', Description='Invitation & Test Kit (Self-referral) (FIT)'"
    )

    # Open the matching batch
    active_batch_page.open_letter_batch(
        batch_type="Original",
        status="Open",
        description="Invitation & Test Kit (Self-referral) (FIT)",
    )
    logging.info("[ACTION] Opened S83f batch")

    # Assert letter components
    letter_batch_page = LetterBatchDetailsPage(page)
    letter_batch_page.assert_letter_component_present(
        "Invitation & Test Kit (Self-referral) (FIT)", "PDF-A4-V03"
    )
    logging.info(
        "[ASSERTION PASSED] Component: Invitation & Test Kit (Self-referral) (FIT) | Format: PDF-A4-V03"
    )

    letter_batch_page.assert_letter_component_present(
        "Pre-invitation (Self-referral) (FIT)", "PDF-A4-V03"
    )
    logging.info(
        "[ASSERTION PASSED] Component: Pre-invitation (Self-referral) (FIT) | Format: PDF-A4-V03"
    )

    letter_batch_page.assert_letter_component_present(
        "Invitation & Test Kit (Self-referral) (FIT)", "FIT-KIT-CSV"
    )
    logging.info(
        "[ASSERTION PASSED] Component: Invitation & Test Kit (Self-referral) (FIT) | Format: FIT-KIT-CSV"
    )


@pytest.mark.regression
@pytest.mark.letters_tests
def test_before_confirming_s83f_batch_subject_status_is_s83(page: Page) -> None:
    """
    Scenario: Before confirming the S83f letter batch the self-referred subject's latest event status is S83
    Given I log in to BCSS "England" as user role "HubManagerAtBCS02"
    When I view the active batch list
    And I view the "Original" type "Open" status active letter batch for "S83" "Invitation & Test Kit (Self-referral) (FIT)"
    And I identify a subject who is in the letter batch
    And I view the subject
    Then the subject is at latest event status "S83 - Selected for Screening (Self-referral)"
    """
    logging.info("[TEST START] Before confirming S83f batch, subject status is S83")

    # Navigate to Active Batch List and filter
    base_page = BasePage(page)
    active_batch_page = ActiveBatchListPage(page)
    base_page.click_main_menu_link()
    base_page.go_to_communications_production_page()
    CommunicationsProductionPage(page).go_to_active_batch_list_page()
    logging.info("[NAVIGATION] Navigated to Active Batch List page")

    # Filter by "Original" type, "S83" event code, and description
    active_batch_page.enter_type_filter("Original")
    active_batch_page.enter_event_code_filter("S83")
    active_batch_page.enter_description_filter(
        "Invitation & Test Kit (Self-referral) (FIT)"
    )
    logging.info(
        "[FILTER] Applied filters: Type='Original', Event Code='S83', Description='Invitation & Test Kit (Self-referral) (FIT)'"
    )
    # Identify the S83f batch ID
    batch_id_link = page.locator("a[href*='/letters/activebatch/']").first
    batch_id = batch_id_link.inner_text().strip()
    logging.info(f"[BATCH IDENTIFIED] Batch ID: {batch_id}")

    # Query DB for subjects in the batch
    nhs_df = get_nhs_no_from_batch_id(batch_id)
    nhs_number = nhs_df.iloc[0]["subject_nhs_number"]
    logging.info(f"[SUBJECT IDENTIFIED] NHS number: {nhs_number}")

    # View the subject
    base_page.click_main_menu_link()
    base_page.go_to_screening_subject_search_page()
    screening_subject_page_searcher.search_subject_by_nhs_number(page, nhs_number)
    logging.info("[SUBJECT VIEW] Subject loaded in UI")

    # Assert latest event status is S83
    summary_page = SubjectScreeningSummaryPage(page)
    summary_page.verify_latest_event_status_value(
        "S83 - Selected for Screening (Self-referral)"
    )
    logging.info(
        "[ASSERTION PASSED] Subject is at status: S83 - Selected for Screening (Self-referral)"
    )


@pytest.mark.regression
@pytest.mark.letters_tests
def test_confirm_s83f_batch_subject_has_s84_event_and_letters(page: Page) -> None:
    """
    Scenario: When the S83f batch has been confirmed the self-referred subject has a self-referral invitation and test kit sent
    Given I log in to BCSS "England" as user role "HubManagerAtBCS02"
    When I view the active batch list
    And I view the "Original" type "Open" status active letter batch for "S83" "Invitation & Test Kit (Self-referral) (FIT)"
    And I identify a subject who is in the letter batch
    And I prepare the letter batch
    And I retrieve and confirm the letters
    And I view the subject
    Then the subject is at latest event status "S84 - Invitation and Test Kit Sent (Self-referral)"
    And the latest "S84 - Invitation and Test Kit Sent (Self-referral)" event shows "2" "View Letter" links
    """
    logging.info("[TEST START] Confirm S83f batch: subject has S84 event and letters")

    # Navigate to Active Batch List and filter
    base_page = BasePage(page)
    active_batch_page = ActiveBatchListPage(page)
    base_page.click_main_menu_link()
    base_page.go_to_communications_production_page()
    CommunicationsProductionPage(page).go_to_active_batch_list_page()
    logging.info("[NAVIGATION] Navigated to Active Batch List page")

    # Filter by "Original" type, "S83" event code, and description
    active_batch_page.enter_type_filter("Original")
    active_batch_page.enter_event_code_filter("S83")
    active_batch_page.enter_description_filter(
        "Invitation & Test Kit (Self-referral) (FIT)"
    )
    logging.info(
        "[FILTER] Applied filters: Type='Original', Event Code='S83', Description='Invitation & Test Kit (Self-referral) (FIT)'"
    )

    # Identify a subject in the batch using DB query
    batch_id_link = page.locator("a[href*='/letters/activebatch/']").first
    batch_id = batch_id_link.inner_text().strip()
    logging.info(f"[BATCH IDENTIFIED] Batch ID: {batch_id}")

    nhs_df = get_nhs_no_from_batch_id(batch_id)
    nhs_number = nhs_df.iloc[0]["subject_nhs_number"]
    logging.info(f"[SUBJECT IDENTIFIED] NHS number: {nhs_number}")

    # Open the matching batch
    active_batch_page.open_letter_batch(
        batch_type="Original",
        description="Invitation & Test Kit (Self-referral) (FIT)",
    )
    logging.info("[ACTION] Opened S83f batch")

    # Prepare the batch
    batch_processing.prepare_and_print_batch(page, link_text=batch_id)

    # View the subject
    base_page.click_main_menu_link()
    base_page.go_to_screening_subject_search_page()
    screening_subject_page_searcher.search_subject_by_nhs_number(page, nhs_number)
    logging.info("[SUBJECT VIEW] Subject loaded in UI")

    # Assert latest event status is S84
    summary_page = SubjectScreeningSummaryPage(page)
    summary_page.verify_latest_event_status_value(
        "S84 - Invitation and Test Kit Sent (Self-referral)"
    )
    logging.info(
        "[ASSERTION PASSED] Subject is at status: S84 - Invitation and Test Kit Sent (Self-referral)"
    )

    # Assert 2 "View Letter" links for S84
    summary_page.click_list_episodes()
    summary_page.click_view_events_link()
    summary_page.assert_view_letter_links_for_event(
        "S84 - Invitation and Test Kit Sent (Self-referral)", expected_count=2
    )
    logging.info("[ASSERTION PASSED] Found 2 'View Letter' links for S84 event")
