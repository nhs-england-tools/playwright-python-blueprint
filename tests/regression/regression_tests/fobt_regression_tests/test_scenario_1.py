import pytest
from playwright.sync_api import Page
from utils.user_tools import UserTools
from utils.oracle.subject_creation_util import CreateSubjectSteps
from utils.subject_assertion import subject_assertion
from utils.call_and_recall_utils import CallAndRecallUtils
import logging
from utils.batch_processing import batch_processing
from utils.fit_kit import FitKitGeneration, FitKitLogged
from pages.logout.log_out_page import LogoutPage
from datetime import datetime


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.fobt_regression_tests
def test_scenario_1(page: Page) -> None:
    """
    Scenario: 1: Non-response to test kits

    S1-S9-S10-S19-S44-C203 [SSCL1] S43-S3-S11-S20-S47-C203 [SSCL1]

    This scenario tests two of the episode closures for non-response to test kits: from the initial kit and from a retest kit.  It includes an episode reopen.

    Scenario summary:
    > Create a new subject in the FOBT age range > Inactive
    > Run the FOBT failsafe trawl > Call
    > Run the database transition to invite them for FOBT screening > S1(1.1)
    > Process S1 letter batch > S9 (1.1)
    > Run timed events > creates S9 letter (1.1)
    > Process S9 letter batch > S10 (1.1)
    > Run timed events > S19 (1.2)
    > Process S19 letter batch > S44 > C203 (1.2)
    > Check recall [SSCL1]
    > Reopen to log a kit > S10 (1.1) > S43 (1.2)
    > Read kit with SPOILT result > S3 (1.4)
    > Process S3 letter batch > S11 (1.4)
    > Run timed events > creates S11 letter batch (1.4)
    > Process S11 letter batch > S20 (1.4)
    > Run timed events > creates S20 letter batch (1.4)
    > Process S20 letter batch > S47 (1.4) > C203 (1.13)
    > Check recall [SSCL1]
    """
    # Given I log in to BCSS "England" as user role "Hub Manager"
    user_role = UserTools.user_login(
        page, "Hub Manager State Registered at BCS01", return_role_type=True
    )
    if user_role is None:
        raise ValueError("User cannot be assigned to a UserRoleType")

    requirements = {
        "age (y/d)": "65/25",
        "active gp practice in hub/sc": "BCS01/BCS001",
    }
    nhs_no = CreateSubjectSteps().create_custom_subject(requirements)
    if nhs_no is None:
        raise ValueError("NHS No is 'None'")

    # Then Comment: NHS number
    logging.info(f"[SUBJECT CREATION] Created subject's NHS number: {nhs_no}")

    # Then my subject has been updated as follows:
    criteria = {
        "subject age": "65",
        "subject has episodes": "No",
        "screening status": "Inactive",
    }
    subject_assertion(nhs_no, criteria)

    # When I run the FOBT failsafe trawl for my subject
    CallAndRecallUtils().run_failsafe(nhs_no)

    page.wait_for_timeout(2000)  # Wait for 2 seconds to allow DB to update

    # Then my subject has been updated as follows:
    criteria = {
        "subject has episodes": "No",
        "screening due date": "Last birthday",
        "screening due date date of change": "Today",
        "screening due date reason": "Failsafe Trawl",
        "screening status": "Call",
        "screening status date of change": "Today",
        "screening status reason": "Failsafe Trawl",
    }
    subject_assertion(nhs_no, criteria)

    # When I invite my subject for FOBT screening
    CallAndRecallUtils().invite_subject_for_fobt_screening(nhs_no, user_role)

    # Then my subject has been updated as follows:
    criteria = {
        "latest event status": "S1 Selected for Screening",
        "latest episode kit class": "FIT",
        "latest episode type": "FOBT",
    }

    subject_assertion(nhs_no, criteria)

    # Then there is a "S1" letter batch for my subject with the exact title "Pre-invitation (FIT)"
    # When I process the open "S1" letter batch for my subject
    # Then my subject has been updated as follows:
    # When I run Timed Events for my subject
    batch_processing(
        page, "S1", "Pre-invitation (FIT)", "S9 - Pre-invitation Sent", True
    )

    # Then there is a "S9" letter batch for my subject with the exact title "Invitation & Test Kit (FIT)"
    # When I process the open "S9" letter batch for my subject
    # Then my subject has been updated as follows:
    # When I run Timed Events for my subject
    batch_processing(
        page,
        "S9",
        "Invitation & Test Kit (FIT)",
        "S10 - Invitation & Test Kit Sent",
        True,
    )

    # Then there is a "S10" letter batch for my subject with the exact title "Test Kit Reminder"
    # When I process the open "S10" letter batch for my subject
    # Then my subject has been updated as follows:
    # When I run Timed Events for my subject
    batch_processing(
        page, "S10", "Test Kit Reminder", "S19 - Reminder of Initial Test Sent", True
    )

    # Then there is a "S19" letter batch for my subject with the exact title "GP Discharge (Initial Test)"
    # When I process the open "S19" letter batch for my subject
    batch_processing(
        page,
        "S19",
        "GP Discharge (Initial Test)",
        "S44 - GP Discharge for Non-response Sent (Initial Test)",
    )

    # Then my subject has been updated as follows:
    criteria = {
        "calculated fobt due date": "2 years from earliest S10 event",
        "calculated lynch due date": "Null",
        "calculated surveillance due date": "Unchanged",
        "ceased confirmation date": "Null",
        "ceased confirmation details": "Null",
        "ceased confirmation user id": "Null",
        "clinical reason for cease": "Null",
        "latest episode accumulated result": "FOBt inadequate participation",
        "latest episode recall calculation method": "Invitation Kit Date",
        "latest episode recall episode type": "FOBT screening",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Closed",
        "latest episode status reason": "Non Response",
        "latest event status": "S44 GP Discharge for Non-response Sent (Initial Test)",
        "lynch due date": "Null",
        "lynch due date date of change": "Null",
        "lynch due date reason": "Null",
        "screening due date": "Calculated FOBT due date",
        "screening due date date of change": "Today",
        "screening due date reason": "Recall",
        "screening status": "Recall",
        "screening status reason": "Recall",
        "surveillance due date": "Null",
        "surveillance due date date of change": "Unchanged",
        "surveillance due date reason": "Unchanged",
    }

    subject_assertion(nhs_no, criteria)

    # When I log my subject's latest unlogged FIT kit
    fit_kit = FitKitGeneration().get_fit_kit_for_subject_sql(nhs_no, False, False)
    sample_date = datetime.now()
    FitKitLogged().log_fit_kits(page, fit_kit, sample_date)

    # Then my subject has been updated as follows:
    criteria = {
        "latest episode accumulated result": "Null",
        "latest episode includes event code": "E55 Reopen to Log a kit",
        "latest episode recall calculation method": "Invitation Kit Date",
        "latest episode recall episode type": "Null",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Open",
        "latest episode status reason": "Null",
        "latest event status": "S43 Kit Returned and Logged (Initial Test)",
        "screening due date": "As at episode start",
        "screening due date date of change": "Today",
        "screening due date reason": "Reopened episode",
    }
    subject_assertion(nhs_no, criteria)

    # When I read my subject's latest logged FIT kit as "SPOILT"
    FitKitLogged().read_latest_logged_kit(user_role, 2, fit_kit, "SPOILT")

    # Then my subject has been updated as follows:
    criteria = {"latest event status": "S3 Test Spoilt"}
    subject_assertion(nhs_no, criteria)

    # And there is a "S3" letter batch for my subject with the exact title "Retest (Spoilt) (FIT)"
    # When I process the open "S3" letter batch for my subject
    # Then my subject has been updated as follows:
    # When I run Timed Events for my subject
    batch_processing(
        page, "S3", "Retest (Spoilt) (FIT)", "S11 - Retest Kit Sent (Spoilt)", True
    )

    # Then there is a "S11" letter batch for my subject with the exact title "Reminder of Retest (Spoilt)"
    # When I process the open "S11" letter batch for my subject
    # Then my subject has been updated as follows:
    # When I run Timed Events for my subject
    batch_processing(
        page,
        "S11",
        "Reminder of Retest (Spoilt)",
        "S20 - Reminder of Retest Kit Sent (Spoilt)",
        True,
    )

    # Then there is a "S20" letter batch for my subject with the exact title "GP Discharge Non Response (Spoilt)"
    # When I process the open "S20" letter batch for my subject
    batch_processing(
        page,
        "S20",
        "GP Discharge Non Response (Spoilt)",
        "S47 - GP Discharge for Non-response Sent (Spoilt Retest Kit)",
    )

    # Then my subject has been updated as follows:
    criteria = {
        "calculated fobt due date": "2 years from earliest S10 event",
        "calculated lynch due date": "Null",
        "calculated surveillance due date": "Null",
        "ceased confirmation date": "Null",
        "ceased confirmation details": "Null",
        "ceased confirmation user id": "Null",
        "clinical reason for cease": "Null",
        "latest episode accumulated result": "FOBt inadequate participation",
        "latest episode recall calculation method": "Invitation Kit Date",
        "latest episode recall episode type": "FOBT screening",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Closed",
        "latest episode status reason": "Non Response",
        "latest event status": "S47 GP Discharge for Non-response Sent (Spoilt Retest Kit)",
        "lynch due date": "Null",
        "lynch due date date of change": "Null",
        "lynch due date reason": "Null",
        "screening due date": "Calculated FOBT due date",
        "screening due date date of change": "Today",
        "screening due date reason": "Recall",
        "screening status": "Recall",
        "screening status reason": "Recall",
        "surveillance due date": "Null",
        "surveillance due date date of change": "Unchanged",
        "surveillance due date reason": "Unchanged",
    }
    subject_assertion(nhs_no, criteria)

    LogoutPage(page).log_out()
