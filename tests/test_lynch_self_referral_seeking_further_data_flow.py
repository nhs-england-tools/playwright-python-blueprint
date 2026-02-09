import pytest
import logging
from playwright.sync_api import Page
from pages.logout.log_out_page import LogoutPage
from utils.oracle.oracle import OracleDB
from utils.user_tools import UserTools
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
    ChangeScreeningStatusOptions,
    ReasonOptions,
)
from utils.subject_assertion import subject_assertion
from utils import screening_subject_page_searcher
from utils.lynch_utils import LynchUtils


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.lynch_self_referral_tests
def test_lynch_self_referral_seeking_further_data_flow(page: Page) -> None:
    """
    Scenario: [BCSS-20606] Verify that a Lynch self-referred subject can be moved to 'Seeking Further Data' (due to uncertified death) and then reverted back to 'Lynch Self-referral' status.

    Steps:
    Log in as Hub Manager
    Receive Lynch diagnosis
    Self-refer subject
    Assert updates
    Set to Seeking Further Data
    Revert to Lynch Self-referral
    """
    logging.info("[TEST START] test_lynch_self_referral_seeking_further_data_flow")

    # Given I log in to BCSS "England" as user role "Hub Manager"
    login_role = "Hub Manager at BCS01"
    user_role = UserTools.user_login(page, login_role, True)
    if user_role is None:
        raise ValueError(
            f"User role '{login_role}' could not be determined after login."
        )

    # When I receive Lynch diagnosis "EPCAM" for a new subject in my hub aged "75" with diagnosis date "3 years ago" and last colonoscopy date "2 years ago"
    # Get or create a subject suitable for Lynch self-referral
    nhs_no = LynchUtils(page).insert_validated_lynch_patient_from_new_subject_with_age(
        "75", "EPCAM", "3 years ago", "2 years ago", user_role
    )

    OracleDB().exec_bcss_timed_events(nhs_number=nhs_no)

    logging.info(
        "[SUBJECT CREATED IN DB] created subject in the database with no screening history who is eligible to self refer"
    )

    # Then Comment: NHS number
    logging.info(f"[SUBJECT CREATION] Created subject's NHS number: {nhs_no}")

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    logging.info(f"[UI ACTION] Navigated to subject summary page for {nhs_no}")

    # When I self refer the subject
    SubjectScreeningSummaryPage(page).click_self_refer_lynch_surveillance_button()

    # Then my subject has been updated as follows:
    self_referral_criteria = {
        "calculated fobt due date": "Null",
        "calculated lynch due date": "Today",
        "calculated surveillance due date": "Null",
        "lynch due date": "Today",
        "lynch due date date of change": "Null",
        "lynch due date reason": "Self-referral",
        "previous screening status": "Lynch Surveillance",
        "screening due date": "Null",
        "screening due date date of change": "Null",
        "screening due date reason": "null",
        "screening status": "Lynch Self-referral",
        "screening status date of change": "Today",
        "screening status reason": "Self-Referral",
        "subject has lynch diagnosis": "Yes",
        "subject lower fobt age": "Default",
        "subject lower lynch age": "25",
        "surveillance due date date of change": "Null",
        "surveillance due date reason": "null",
        "surveillance due date": "Null",
    }

    subject_assertion(nhs_no, self_referral_criteria)
    logging.info(
        "[ASSERTION PASSED] Subject details after self-referral are as expected"
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I set the subject to Seeking Further Data
    SubjectScreeningSummaryPage(page).change_screening_status(
        ChangeScreeningStatusOptions.SEEKING_FURTHER_DATA,
        ReasonOptions.UNCERTIFIED_DEATH,
    )

    # Then my subject has been updated as follows:
    seeking_further_data_criteria = {
        "calculated fobt due date": "Null",
        "calculated lynch due date": "today",
        "calculated surveillance due date": "Null",
        "lynch due date": "today",
        "lynch due date date of change": "Null",
        "lynch due date reason": "Self-referral",
        "previous screening status": "Lynch Self-referral",
        "screening due date": "Null",
        "screening due date date of change": "Null",
        "screening due date reason": "Null",
        "subject has lynch diagnosis": "Yes",
        "subject lower fobt age": "Default",
        "subject lower lynch age": "25",
        "screening status": "Seeking Further Data",
        "screening status date of change": "Today",
        "screening status reason": "Uncertified Death",
        "surveillance due date": "Null",
        "surveillance due date date of change": "Null",
        "surveillance due date reason": "Null",
    }

    subject_assertion(nhs_no, seeking_further_data_criteria)

    # When I set the subject from Seeking Further Data back to "Lynch Self-referral"
    SubjectScreeningSummaryPage(page).change_screening_status(
        ChangeScreeningStatusOptions.LYNCH_SELF_REFERRAL,
        ReasonOptions.RESET_SEEKING_FURTHER_DATA_TO_LYNCH_SELF_REFERRAL,
    )

    # Then my subject has been updated as follows:
    reverted_criteria = {
        "calculated fobt due date": "Null",
        "calculated lynch due date": "today",
        "calculated surveillance due date": "Null",
        "lynch due date": "today",
        "lynch due date date of change": "Null",
        "lynch due date reason": "Self-referral",
        "previous screening status": "Lynch Self-referral",
        "screening due date": "Null",
        "screening due date date of change": "Null",
        "screening due date reason": "Null",
        "subject has lynch diagnosis": "Yes",
        "subject lower fobt age": "Default",
        "subject lower lynch age": "25",
        "screening status": "Lynch Self-referral",
        "screening status date of change": "Today",
        "screening status reason": "Reset seeking further data to Lynch Self-referral",
        "surveillance due date": "Null",
        "surveillance due date date of change": "Null",
        "surveillance due date reason": "Null",
    }

    subject_assertion(nhs_no, reverted_criteria)

    LogoutPage(page).log_out()
    logging.info("[TEST END] test_lynch_self_referral_seeking_further_data_flow")
