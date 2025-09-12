import pytest
import logging
from datetime import datetime
from playwright.sync_api import Page
from utils.oracle.subject_creation_util import CreateSubjectSteps
from utils.user_tools import UserTools
from utils.subject_assertion import subject_assertion
from utils.call_and_recall_utils import CallAndRecallUtils
from utils import screening_subject_page_searcher
from utils.batch_processing import batch_processing
from utils.fit_kit import FitKitLogged, FitKitGeneration
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from pages.logout.log_out_page import LogoutPage


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.fobt_regression_tests
def test_scenario_2(page: Page) -> None:
    """
    Scenario: 2: Normal kit reading

    S1-S9-S10-S43-S2-S158-S159-C203 [SSCL4a]

    This scenario tests the basic scenario where a subject returns their initial test kit which gives a normal result.

    Scenario summary:
    > Create a new subject in the FOBT age range > Inactive
    > Run the FOBT failsafe trawl > Call
    > Run the database transition to invite them for FOBT screening > S1(1.1)
    > Process S1 letter batch > S9 (1.1)
    > Run timed events > creates S9 letter (1.1)
    > Process S9 letter batch > S10 (1.1)
    > Log kit > S43 (1.2)
    > Read kit with NORMAL result > S2 (1.3)
    > Process S2 letter batch > S158 (1.3)
    > Process S158 letter batch > S159 (1.3) > C203 (1.13)
    > Check recall [SSCL4a]
    """
    summary_page = SubjectScreeningSummaryPage(page)
    logging.info("[TEST START] Regression - fobt normal kit reading")

    # Given I log in to BCSS "England" as user role "Hub Manager"
    user_role = UserTools.user_login(
        page, "Hub Manager State Registered at BCS01", return_role_type=True
    )
    if user_role is None:
        raise ValueError("User cannot be assigned to a UserRoleType")

    # And I create a subject that meets the following criteria:
    requirements = {
        "age (y/d)": "66/130",
        "active gp practice in hub/sc": "BCS01/BCS001",
    }
    nhs_no = CreateSubjectSteps().create_custom_subject(requirements)
    if nhs_no is None:
        pytest.fail("Failed to create subject: NHS number not returned.")

    # Then Comment: NHS number
    logging.info(f"[SUBJECT CREATED] Created subject's NHS number: {nhs_no}")

    # And my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "subject age": "66",
            "subject has episodes": "No",
            "screening status": "Inactive",
        },
    )

    # Navigate to subject summary page in UI
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # Assert subject details in the UI
    summary_page.assert_subject_age(66)
    summary_page.assert_screening_status("Inactive")

    # When I run the FOBT failsafe trawl for my subject
    CallAndRecallUtils().run_failsafe(nhs_no)

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "subject has episodes": "No",
            "Screening Due Date": "Last Birthday",
            "Screening due date date of change": "Today",
            "Screening Due Date Reason": "Failsafe Trawl",
            "screening status": "Call",
            "Screening Status Date of Change": "Today",
            "Screening Status Reason": "Failsafe Trawl",
        },
    )

    # Navigate to subject summary page in UI
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # Assert subject details in the UI
    summary_page.assert_screening_status("Call")

    # When I invite my subject for FOBT screening
    CallAndRecallUtils().invite_subject_for_fobt_screening(nhs_no, user_role)

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "S1 Selected for Screening",
            "latest episode kit class": "FIT",
            "latest episode type": "FOBT",
        },
    )

    # Then there is a "S1" letter batch for my subject with the exact title "Pre-invitation (FIT)"
    # When I process the open "S1" letter batch for my subject
    # Then there is a "S9" letter batch for my subject with the exact title "Invitation & Test Kit (FIT)"
    batch_processing(
        page, "S1", "Pre-invitation (FIT)", "S9 - Pre-invitation Sent", True
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "S9 - Pre-invitation Sent",
        },
    )

    # When I process the open "S9" letter batch for my subject
    batch_processing(
        page,
        "S9",
        "Invitation & Test Kit (FIT)",
        "S10 - Invitation & Test Kit Sent",
        True,
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "S10 - Invitation & Test Kit Sent",
        },
    )

    # When I log my subject's latest unlogged FIT kit
    fit_kit = FitKitGeneration().get_fit_kit_for_subject_sql(nhs_no, False, False)
    sample_date = datetime.now()
    FitKitLogged().log_fit_kits(page, fit_kit, sample_date)

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "S43 Kit Returned and Logged (Initial Test)",
        },
    )

    # Navigate to subject summary page in UI
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # Assert subject details in the UI
    summary_page.assert_latest_event_status(
        "S43 - Kit Returned and Logged (Initial Test)"
    )

    # When I read my subject's latest logged FIT kit as "NORMAL"
    FitKitLogged().read_latest_logged_kit(user_role, 2, fit_kit, "NORMAL")

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "S2 Normal",
        },
    )

    # Navigate to subject summary page in UI
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # Assert subject details in the UI
    summary_page.assert_latest_event_status("S2 - Normal")

    # And there is a "S2" letter batch for my subject with the exact title "Subject Result (Normal)"
    # When I process the open "S2" letter batch for my subject
    batch_processing(
        page,
        "S2",
        "Subject Result (Normal)",
        "S158 - Subject Discharge Sent (Normal)",
        True,
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "S158 Subject Discharge Sent (Normal)",
        },
    )

    # And there is a "S158" letter batch for my subject with the exact title "GP Result (Normal)"
    # When I process the open "S158" letter batch for my subject
    batch_processing(
        page,
        "S158",
        "GP Result (Normal)",
        "S159 - GP Discharge Sent (Normal)",
        True,
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "calculated screening due date": "2 years from latest S158 event",
            "calculated lynch due date": "Null",
            "calculated surveillance due date": "Null",
            "ceased confirmation date": "Null",
            "ceased confirmation details": "Null",
            "ceased confirmation user ID": "Null",
            "clinical reason for cease": "Null",
            "latest episode accumulated result": "Definitive normal FOBt outcome",
            "latest episode recall calculation method": "Date of last patient letter",
            "latest episode recall episode type": "FOBT screening",
            "latest episode recall surveillance type": "Null",
            "latest episode status": "Closed",
            "latest episode status reason": "Episode Complete",
            "lynch due date": "Null",
            "lynch due date date of change": "Null",
            "lynch due date reason": "Null",
            "screening status": "Recall",
            # 'Screening status date of change' intentionally omitted as status may or may not have changed
            "screening status reason": "Recall",
            "screening due date": "Calculated screening due date",
            "screening due date date of change": "Today",
            "screening due date reason": "Recall",
            "surveillance due date": "Null",
            "surveillance due date date of change": "Unchanged",
            "surveillance due date reason": "Unchanged",
        },
    )

    logging.info("[TEST COMPLETE] Scenario 2 passed all assertions")
    LogoutPage(page).log_out()
