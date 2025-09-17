import pytest
import logging
import pandas as pd
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.oracle.subject_selector import SubjectSelector
from utils.oracle.oracle import OracleDB
from pages.base_page import BasePage
from pages.manual_cease.manual_cease_page import ManualCeasePage
from utils import screening_subject_page_searcher
from utils.user_tools import UserTools
from utils.manual_cease import EXPECT
from utils.manual_cease import (
    ScreeningStatus,
    ScreeningStatusReason,
    ScreeningDueDateReason,
    SurveillanceDueDateReason,
)
from utils.manual_cease import ManualCeaseTools
from datetime import datetime
from typing import Any


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as a test user and navigates to the active batch list page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager at BCS01")

    # Go to screening subject search page
    base_page = BasePage(page)
    base_page.click_main_menu_link()
    base_page.go_to_screening_subject_search_page()


@pytest.fixture
def base_expected_db() -> dict[str, Any]:
    return {
        "Screening Status": ScreeningStatus.CEASED,
        "Screening Due Date": EXPECT.NULL,
        "Ceased Confirmation Details": "AUTO TEST: notes",
        "Clinical Reason for Cease": EXPECT.NULL,
        "Calculated FOBT Due Date": EXPECT.UNCHANGED,
        "Calculated Surveillance Due Date": EXPECT.UNCHANGED,
    }


# Feature: Manually cease a subject


# These scenarios just check that manually ceasing a subject (either immediately or via a disclaimer letter) from different statuses correctly sets their screening status and status reason.
# Screening due date reason is always set to "Ceased" during a manual cease, even if the SDD is not changing.
@pytest.mark.vpn_required
@pytest.mark.manual_cease_tests
@pytest.mark.regression
def test_manual_cease_from_inactive_subject_for_informed_dissent(
    page: Page, base_expected_db
) -> None:
    """
    Scenario: Subject is at status Inactive, cease for Informed Dissent

        Given I log in to BCSS "England" as user role "Hub Manager"
        And there is a subject who meets the following criteria:
            | Screening status | Inactive |
        When I view the subject
        And I manually cease the subject with reason "Informed Dissent"
        And I pause for "5" seconds to let the process complete
        Then my subject has been updated as follows:
            | Screening Status                 | Ceased                                           |
            | Screening Status Reason          | Informed Dissent                                 |
            | Screening Status Date of Change  | Today                                            |
            | Screening Due Date Reason        | Ceased                                           |
            | Screening Due Date               | Null (unchanged)                                 |
            | Ceased Confirmation Details      | AUTO TESTING: confirm not-immediate manual cease |
            | Ceased Confirmation User ID      | User's ID                                        |
            | Lynch / Surveillance Due Dates   | Unchanged or Null                                |
            | Clinical Reason for Cease        | Null                                             |
    """
    logging.info("[TEST START] Manual cease from Inactive subject for Informed Dissent")

    # Convert user details dictionary into User object for fallback logic
    user_details = UserTools.retrieve_user("Hub Manager at BCS02")

    try:
        # Try retrieving existing subject via updated selector method
        criteria = {
            "screening status": "Inactive",
            "screening due date": "Null",
            "manual cease requested": "No",
            "subject hub code": user_details["hub_code"],
        }
        nhs_number = SubjectSelector.get_subject_for_manual_cease(criteria)
        logging.info(f"[SUBJECT FOUND] Retrieved NHS number: {nhs_number}")

        nhs_df = pd.DataFrame({"subject_nhs_number": [nhs_number]})
        OracleDB().exec_bcss_timed_events(nhs_df)
        logging.info("[TIMED EVENTS] Executed for existing subject")

    except ValueError:
        # Fallback: Create a new subject using manual cease creation utility
        logging.warning(
            "[SUBJECT NOT FOUND] Creating fallback subject for manual cease"
        )

        nhs_number = ManualCeaseTools.create_manual_cease_ready_subject(
            screening_centre=user_details["hub_code"], base_age=75
        )

        logging.info(f"[SUBJECT CREATED] Fallback NHS number: {nhs_number}")

    # Navigate to subject profile in UI
    screening_subject_page_searcher.search_subject_by_nhs_number(page, nhs_number)
    logging.info("[SUBJECT VIEW] Subject loaded in UI")

    # Manually cease subject with specified reason
    manual_cease_page = ManualCeasePage(page)
    ManualCeaseTools.process_manual_cease_with_disclaimer(
        manual_cease_page, reason="Informed Dissent"
    )
    logging.info("[CEASE ACTION] Manual cease triggered")

    # Perform UI field assertions
    today = datetime.today().strftime("%d/%m/%Y")  # Get today's date in required format

    # Define the shared locator
    manual_cease_page = ManualCeasePage(page)

    # UI Assertions
    expect(manual_cease_page.summary_table).to_contain_text("Ceased")
    expect(manual_cease_page.summary_table).to_contain_text("Informed Dissent")
    expect(manual_cease_page.summary_table).to_contain_text(today)

    # DB assertions
    expected_db = {
        **base_expected_db,
        "Screening Status Reason": ScreeningStatusReason.INFORMED_DISSENT,
        "Screening Status Date of Change": EXPECT.TODAY,
        "Screening Due Date Reason": ScreeningDueDateReason.CEASED,
        "Calculated Lynch Due Date": EXPECT.UNCHANGED,
    }

    # Fire off the DB asserts
    ManualCeaseTools.verify_manual_cease_db_fields_dynamic(nhs_number, expected_db)
    logging.info("[ASSERTIONS COMPLETE] Manual cease scenario validated successfully")


@pytest.mark.vpn_required
@pytest.mark.manual_cease_tests
@pytest.mark.regression
def test_manual_cease_from_call_subject_for_informed_dissent_verbal_only(
    page: Page, base_expected_db
) -> None:
    """
    Scenario: Subject is at status Call, cease for Informed Dissent, verbal only

        Given I log in to BCSS "England" as user role "Hub Manager"
        And there is a subject who meets the following criteria:
            | Screening status                         | Call |
            | Subject has episodes                     | No   |
        When Comment: NHS number
        When I view the subject
        And I manually cease the subject with reason "Informed Dissent (verbal only)"
        And I pause for "5" seconds to let the process complete
        Then my subject has been updated as follows:
            | Calculated FOBT due date                 | Unchanged                                        |
            | Calculated lynch due date                | Null                                             |
            | Calculated surveillance due date         | Unchanged                                        |
            | Ceased confirmation date                 | Today                                            |
            | Ceased confirmation details              | AUTO TESTING: confirm immediate manual cease     |
            | Ceased confirmation user ID              | User's ID                                        |
            | Clinical reason for cease                | Null                                             |
            | Lynch due date                           | Null                                             |
            | Lynch due date reason                    | Unchanged                                        |
            | Lynch due date date of change            | Unchanged                                        |
            | Screening due date                       | Null                                             |
            | Screening due date date of change        | Today                                            |
            | Screening due date reason                | Ceased                                           |
            | Screening status                         | Ceased                                           |
            | Screening status reason                  | Informed Dissent (verbal only)                   |
            | Screening status date of change          | Today                                            |
            | Surveillance due date                    | Null                                             |
            | Surveillance due date reason             | Unchanged                                        |
            | Surveillance due date date of change     | Unchanged                                        |
    """
    logging.info(
        "[TEST START] Manual cease from Call subject for Informed Dissent (verbal only)"
    )

    # Convert user details dictionary into User object for fallback logic
    user_details = UserTools.retrieve_user("Hub Manager at BCS02")

    try:
        # Try retrieving existing subject via updated selector method
        criteria = {
            "screening status": "Call",
            "screening due date": "Null",
            "manual cease requested": "No",
            "subject hub code": user_details["hub_code"],
            "subject has episodes": "No",
        }
        nhs_number = SubjectSelector.get_subject_for_manual_cease(criteria)
        logging.info(f"[SUBJECT FOUND] Retrieved NHS number: {nhs_number}")
    except ValueError:
        # Fallback: Create a new subject using manual cease creation utility
        logging.warning(
            "[SUBJECT NOT FOUND] Creating fallback subject for manual cease"
        )
        nhs_number = ManualCeaseTools.create_manual_cease_ready_subject(
            screening_centre=user_details["hub_code"], base_age=75
        )

        logging.info(f"[SUBJECT CREATED] Fallback NHS number: {nhs_number}")

    # Navigate to subject profile in UI
    screening_subject_page_searcher.search_subject_by_nhs_number(page, nhs_number)
    logging.info("[SUBJECT VIEW] Subject loaded in UI")

    # Manually cease subject with specified reason
    manual_cease_page = ManualCeasePage(page)
    ManualCeaseTools.process_manual_cease_immediate(
        manual_cease_page, reason="Informed Dissent (verbal only)"
    )
    logging.info("[CEASE ACTION] Manual cease triggered")

    # Define the shared locator and today's date
    today = datetime.today().strftime("%d/%m/%Y")  # Get today's date in required format
    manual_cease_page = ManualCeasePage(page)

    # UI Assertions
    expect(manual_cease_page.summary_table).to_contain_text("Ceased")
    expect(manual_cease_page.summary_table).to_contain_text(
        "Informed Dissent (verbal only)"
    )
    expect(manual_cease_page.summary_table).to_contain_text(today)

    # DB assertions
    expected_db = {
        **base_expected_db,
        "Screening Status": ScreeningStatus.CEASED,
        "Screening Status Reason": ScreeningStatusReason.INFORMED_DISSENT_VERBAL,
        "Screening Status Date of Change": EXPECT.TODAY,
        "Screening Due Date Reason": ScreeningDueDateReason.CEASED,
        "Screening Due Date": EXPECT.NULL,
        "Ceased Confirmation Details": "AUTO TEST: notes",
        "Clinical Reason for Cease": EXPECT.NULL,
        "Calculated Lynch Due Date": EXPECT.NULL,
        "Lynch due date": EXPECT.NULL,
        "Screening due date date of change": EXPECT.TODAY,
        "Surveillance due date": EXPECT.NULL,
    }

    # Fire off the DB asserts
    ManualCeaseTools.verify_manual_cease_db_fields_dynamic(nhs_number, expected_db)
    logging.info("[ASSERTIONS COMPLETE] Manual cease scenario validated successfully")


@pytest.mark.vpn_required
@pytest.mark.manual_cease_tests
@pytest.mark.regression
def test_manual_cease_from_recall_subject_for_no_colon_subject_request(
    page: Page, base_expected_db
) -> None:
    """
    Scenario: Subject is at status Recall, cease for No Colon, subject request

        Look for subject's with a not-null due date so the check for the SDD change is not tripped up by dodgy test data.

        Given I log in to BCSS "England" as user role "Hub Manager"
        And there is a subject who meets the following criteria:
            | Screening status                         | Recall   |
            | Screening due date                       | Not null |
            | Latest episode status                    | Closed   |
        When Comment: NHS number
        When I view the subject
        And I manually cease the subject with reason "No Colon (subject request)"
        And I pause for "5" seconds to let the process complete
        Then my subject has been updated as follows:
            | Calculated FOBT due date                 | Unchanged                                        |
            | Calculated lynch due date                | Null                                             |
            | Calculated surveillance due date         | Unchanged                                        |
            | Ceased confirmation date                 | Today                                            |
            | Ceased confirmation details              | AUTO TESTING: confirm not-immediate manual cease |
            | Ceased confirmation user ID              | User's ID                                        |
            | Clinical reason for cease                | Null                                             |
            | Lynch due date                           | Null                                             |
            | Lynch due date reason                    | Unchanged                                        |
            | Lynch due date date of change            | Unchanged                                        |
            | Screening due date                       | Null                                             |
            | Screening due date date of change        | Today                                            |
            | Screening due date reason                | Ceased                                           |
            | Screening status                         | Ceased                                           |
            | Screening status reason                  | No Colon (subject request)                       |
            | Screening status date of change          | Today                                            |
            | Surveillance due date                    | Null                                             |
            | Surveillance due date reason             | Unchanged                                        |
            | Surveillance due date date of change     | Unchanged                                        |
    """
    logging.info(
        "[TEST START] Manual cease from Recall subject for No Colon (subject request)"
    )

    # Convert user details dictionary into User object for fallback logic
    user_details = UserTools.retrieve_user("Hub Manager at BCS02")

    try:
        # Try retrieving existing subject via updated selector method
        criteria = {
            "screening status": "Recall",
            "screening due date": "Not null",
            "latest episode status": "Closed",
            "subject hub code": user_details["hub_code"],
        }
        nhs_number = SubjectSelector.get_subject_for_manual_cease(criteria)
        logging.info(f"[SUBJECT FOUND] Retrieved NHS number: {nhs_number}")
    except ValueError:
        # Fallback: Create a subject with post-scheduled timeline events
        logging.warning(
            "[SUBJECT NOT FOUND] Creating fallback subject for manual cease"
        )
        nhs_number = ManualCeaseTools.create_manual_cease_ready_subject(
            screening_centre=user_details["hub_code"], base_age=75
        )
        logging.info(f"[SUBJECT CREATED] Fallback NHS number: {nhs_number}")

    # View the subject profile in UI
    screening_subject_page_searcher.search_subject_by_nhs_number(page, nhs_number)
    logging.info("[SUBJECT VIEW] Subject loaded in UI")

    # Perform manual cease with specified reason
    manual_cease_page = ManualCeasePage(page)
    ManualCeaseTools.process_manual_cease_with_disclaimer(
        manual_cease_page, reason="No Colon (subject request)"
    )
    logging.info("[CEASE ACTION] Manual cease triggered")

    # Define the shared locator and today's date
    today = datetime.today().strftime("%d/%m/%Y")
    manual_cease_page = ManualCeasePage(page)

    # UI assertions
    expect(manual_cease_page.summary_table).to_contain_text("Ceased")
    expect(manual_cease_page.summary_table).to_contain_text(
        "No Colon (subject request)"
    )
    expect(manual_cease_page.summary_table).to_contain_text(today)

    # DB field assertions
    expected_db = {
        **base_expected_db,
        "Screening Status": ScreeningStatus.CEASED,
        "Screening Status Reason": ScreeningStatusReason.NO_COLON_SUBJECT_REQUEST,
        "Screening Status Date of Change": EXPECT.TODAY,
        "Screening Due Date": EXPECT.NULL,
        "Screening Due Date Reason": ScreeningDueDateReason.CEASED,
        "Screening due date date of change": EXPECT.TODAY,
        "Ceased Confirmation Details": "AUTO TEST: notes",
        "Clinical Reason for Cease": EXPECT.NULL,
    }

    # Fire off the DB assertions
    ManualCeaseTools.verify_manual_cease_db_fields_dynamic(nhs_number, expected_db)
    logging.info("[ASSERTIONS COMPLETE] Manual cease scenario validated successfully")


@pytest.mark.vpn_required
@pytest.mark.manual_cease_tests
@pytest.mark.regression
def test_manual_cease_from_surveillance_subject_for_no_colon_programme_assessed(
    page: Page, base_expected_db
) -> None:
    """
    Scenario: Subject is at status Surveillance, cease for No Colon, programme assessed

        Given I log in to BCSS "England" as user role "Hub Manager"
        And there is a subject who meets the following criteria:
            | Screening status                         | Surveillance |
            | Latest episode status                    | Closed       |

        When Comment: NHS number
        When I view the subject
        And I manually cease the subject with reason "No Colon (programme assessed)"
        And I pause for "5" seconds to let the process complete
        Then my subject has been updated as follows:
            | Calculated FOBT due date                 | Unchanged                                        |
            | Calculated lynch due date                | Null                                             |
            | Calculated surveillance due date         | Unchanged                                        |
            | Ceased confirmation date                 | Today                                            |
            | Ceased confirmation details              | AUTO TESTING: confirm immediate manual cease     |
            | Ceased confirmation user ID              | User's ID                                        |
            | Clinical reason for cease                | Null                                             |
            | Lynch due date                           | Null                                             |
            | Lynch due date reason                    | Unchanged                                        |
            | Lynch due date date of change            | Unchanged                                        |
            | Screening due date                       | Null                                             |
            | Screening due date date of change        | Unchanged                                        |
            | Screening due date reason                | Ceased                                           |
            | Screening status                         | Ceased                                           |
            | Screening status reason                  | No Colon (programme assessed)                    |
            | Screening status date of change          | Today                                            |
            | Surveillance due date                    | Null                                             |
            | Surveillance due date reason             | Ceased                                           |
            | Surveillance due date date of change     | Today                                            |
    """
    logging.info(
        "[TEST START] Manual cease from Surveillance subject for No Colon (programme assessed)"
    )

    user_details = UserTools.retrieve_user("Hub Manager at BCS02")

    try:
        criteria = {
            "screening status": "Surveillance",
            "latest episode status": "Closed",
            "subject hub code": user_details["hub_code"],
        }
        nhs_number = SubjectSelector.get_subject_for_manual_cease(criteria)
        logging.info(f"[SUBJECT FOUND] Retrieved NHS number: {nhs_number}")
    except ValueError:
        logging.warning("[SUBJECT NOT FOUND] Creating fallback subject")

        nhs_number = ManualCeaseTools.create_manual_cease_ready_subject(
            screening_centre=user_details["hub_code"],
            base_age=76,
        )
        logging.info(f"[SUBJECT CREATED] Fallback NHS number: {nhs_number}")

    screening_subject_page_searcher.search_subject_by_nhs_number(page, nhs_number)
    logging.info("[SUBJECT VIEW] Subject loaded in UI")

    manual_cease_page = ManualCeasePage(page)
    ManualCeaseTools.process_manual_cease_immediate(
        manual_cease_page, reason="No Colon (programme assessed)"
    )
    logging.info("[CEASE ACTION] Manual cease triggered")

    # Define the shared locator and today's date
    today = datetime.today().strftime("%d/%m/%Y")
    manual_cease_page = ManualCeasePage(page)

    # UI Assertions
    expect(manual_cease_page.summary_table).to_contain_text("Ceased")
    expect(manual_cease_page.summary_table).to_contain_text(
        "No Colon (programme assessed)"
    )
    expect(manual_cease_page.summary_table).to_contain_text(today)

    expected_db = {
        **base_expected_db,
        "Screening Status": ScreeningStatus.CEASED,
        "Screening Status Reason": ScreeningStatusReason.NO_COLON_PROGRAMME_ASSESSED,
        "Screening Status Date of Change": EXPECT.TODAY,
        "Screening Due Date": EXPECT.NULL,
        "Screening Due Date Reason": ScreeningDueDateReason.CEASED,
        "Screening due date date of change": EXPECT.UNCHANGED,
        "Ceased Confirmation Details": "AUTO TEST: notes",
        "Clinical Reason for Cease": EXPECT.NULL,
        "Surveillance due date": EXPECT.NULL,
        "Surveillance due date reason": SurveillanceDueDateReason.CEASED,
        "Surveillance due date date of change": EXPECT.TODAY,
    }

    ManualCeaseTools.verify_manual_cease_db_fields_dynamic(nhs_number, expected_db)
    logging.info(
        "[ASSERTIONS COMPLETE] Surveillance cease scenario validated successfully"
    )


@pytest.mark.vpn_required
@pytest.mark.manual_cease_tests
@pytest.mark.regression
def test_manual_cease_from_already_ceased_subject_for_informal_death(
    page: Page, base_expected_db
) -> None:
    """
    Scenario: Subject is at status Ceased, outside screening population, cease for Informal Death

        Screening status reason is set, but because the status itself is not changing
        the status date of change is not changed.

        Given I log in to BCSS "England" as user role "Hub Manager"
        And there is a subject who meets the following criteria:
            | Screening status                         | Ceased                       |
            | Screening status reason                  | Outside screening population |

        When Comment: NHS number
        When I view the subject
        And I manually cease the subject with reason "Informal Death"
        And I pause for "5" seconds to let the process complete
        Then my subject has been updated as follows:
            | Calculated FOBT due date                 | Unchanged                                        |
            | Calculated lynch due date                | Null                                             |
            | Calculated surveillance due date         | Unchanged                                        |
            | Ceased confirmation date                 | Today                                            |
            | Ceased confirmation details              | AUTO TESTING: confirm immediate manual cease     |
            | Ceased confirmation user ID              | User's ID                                        |
            | Clinical reason for cease                | Null                                             |
            | Lynch due date                           | Null                                             |
            | Lynch due date reason                    | Unchanged                                        |
            | Lynch due date date of change            | Unchanged                                        |
            | Screening due date                       | Null                                             |
            | Screening due date date of change        | Unchanged                                        |
            | Screening due date reason                | Unchanged                                        |
            | Screening status                         | Ceased                                           |
            | Screening status reason                  | Informal Death                                   |
            | Screening status date of change          | Unchanged                                        |
            | Surveillance due date                    | Null                                             |
            | Surveillance due date reason             | Unchanged                                        |
            | Surveillance due date date of change     | Unchanged                                        |
    """
    logging.info(
        "[TEST START] Manual cease from already ceased subject for Informal Death"
    )

    user_details = UserTools.retrieve_user("Hub Manager at BCS02")

    try:
        criteria = {
            "screening status": "Ceased",
            "screening status reason": "Outside screening population",
            "subject hub code": user_details["hub_code"],
        }
        nhs_number = SubjectSelector.get_subject_for_manual_cease(criteria)
        logging.info(f"[SUBJECT FOUND] Retrieved NHS number: {nhs_number}")
    except ValueError:
        logging.warning("[SUBJECT NOT FOUND] Creating fallback ceased subject")

        nhs_number = ManualCeaseTools.create_manual_cease_ready_subject(
            screening_centre=user_details["hub_code"],
            base_age=77,
        )
        logging.info(f"[SUBJECT CREATED] Fallback NHS number: {nhs_number}")

    screening_subject_page_searcher.search_subject_by_nhs_number(page, nhs_number)
    logging.info("[SUBJECT VIEW] Subject loaded in UI")

    manual_cease_page = ManualCeasePage(page)
    ManualCeaseTools.process_manual_cease_immediate(
        manual_cease_page, reason="Informal Death"
    )
    logging.info("[CEASE ACTION] Manual cease triggered")

    # Define the shared locator and today's date
    today = datetime.today().strftime("%d/%m/%Y")
    manual_cease_page = ManualCeasePage(page)

    # UI Assertions
    expect(manual_cease_page.summary_table).to_contain_text("Ceased")
    expect(manual_cease_page.summary_table).to_contain_text("Informal Death")
    expect(manual_cease_page.summary_table).to_contain_text(today)

    expected_db = {
        **base_expected_db,
        "Screening Status Reason": ScreeningStatusReason.INFORMAL_DEATH,
        "Screening Status Date of Change": EXPECT.UNCHANGED,
        "Screening Due Date Reason": EXPECT.UNCHANGED,
        "Screening due date date of change": EXPECT.UNCHANGED,
        "Ceased Confirmation Date": EXPECT.TODAY,
        "Calculated Lynch Due Date": EXPECT.NULL,
        "Lynch due date": EXPECT.NULL,
        "Lynch due date reason": EXPECT.UNCHANGED,
        "Lynch due date date of change": EXPECT.UNCHANGED,
        "Surveillance due date": EXPECT.NULL,
        "Surveillance due date reason": EXPECT.UNCHANGED,
        "Surveillance due date date of change": EXPECT.UNCHANGED,
    }

    ManualCeaseTools.verify_manual_cease_db_fields_dynamic(nhs_number, expected_db)
    logging.info(
        "[ASSERTIONS COMPLETE] Informal Death cease scenario validated successfully"
    )


@pytest.mark.vpn_required
@pytest.mark.manual_cease_tests
@pytest.mark.regression
def test_manual_cease_from_already_ceased_subject_for_no_colon_subject_request(
    page: Page, base_expected_db
) -> None:
    """
    Scenario: Subject is at status Ceased, outside screening population, cease for No Colon (subject request)

        Screening status reason is set, but because the status itself is not changing
        the status date of change is not changed.

        Given I log in to BCSS "England" as user role "Hub Manager"
        And there is a subject who meets the following criteria:
            | Screening status                         | Ceased                       |
            | Screening status reason                  | Outside screening population |

        When I view the subject
        And I manually cease the subject with reason "No Colon (subject request)"
        And I pause for "5" seconds to let the process complete
        Then my subject has been updated as follows:
            | Screening Status                         | Ceased                                 |
            | Screening Status Reason                  | No Colon (subject request)             |
            | Screening Status Date of Change          | Unchanged                              |
            | Screening Due Date                       | NULL                                   |
            | Screening Due Date Reason                | Unchanged                              |
            | Screening Due Date Date of Change        | Unchanged                              |
            | Ceased Confirmation Details              | AUTO TEST: notes                       |
            | Ceased Confirmation Date                 | Today's date                           |
            | Clinical Reason for Cease                | NULL                                   |
            | Calculated FOBT Due Date                 | Unchanged                              |
            | Calculated Lynch Due Date                | NULL                                   |
            | Calculated Surveillance Due Date         | Unchanged                              |
            | Lynch due date                           | NULL                                   |
            | Lynch due date reason                    | Unchanged                              |
            | Lynch due date date of change            | Unchanged                              |
            | Surveillance due date                    | NULL                                   |
            | Surveillance due date reason             | Unchanged                              |
            | Surveillance due date date of change     | Unchanged                              |
    """
    # Start test log
    logging.info(
        "[TEST START] Manual cease from already ceased subject for No Colon (subject request)"
    )

    # Retrieve user details for the test role
    user_details = UserTools.retrieve_user("Hub Manager at BCS02")

    try:
        # Try to find a subject that already meets the required ceased criteria
        criteria = {
            "screening status": "Ceased",
            "screening status reason": "Outside screening population",
            "subject has episodes": "No",
        }
        nhs_number = SubjectSelector.get_subject_for_manual_cease(criteria)
        logging.info(f"[SUBJECT FOUND] Retrieved NHS number: {nhs_number}")
    except ValueError:
        # If no matching subject exists, create a fallback one
        logging.warning("[SUBJECT NOT FOUND] Creating fallback ceased subject")

        nhs_number = ManualCeaseTools.create_manual_cease_ready_subject(
            screening_centre=user_details["hub_code"],
            base_age=75,
        )
        logging.info(f"[SUBJECT CREATED] Fallback NHS number: {nhs_number}")

    # Search for the subject in UI
    screening_subject_page_searcher.search_subject_by_nhs_number(page, nhs_number)
    logging.info("[SUBJECT VIEW] Subject loaded in UI")

    # Manually cease the subject with the specified reason
    manual_cease_page = ManualCeasePage(page)
    ManualCeaseTools.process_manual_cease_with_disclaimer(
        manual_cease_page, reason="No Colon (subject request)"
    )
    logging.info("[CEASE ACTION] Manual cease triggered")

    # Define shared locator
    manual_cease_page = ManualCeasePage(page)

    # UI Assertions
    expect(manual_cease_page.summary_table).to_contain_text("Ceased")
    expect(manual_cease_page.summary_table).to_contain_text(
        "No Colon (subject request)"
    )

    # Define expected database values post-cease
    expected_db = {
        **base_expected_db,
        "Screening Status Reason": ScreeningStatusReason.NO_COLON_SUBJECT_REQUEST,
        "Screening Status Date of Change": EXPECT.UNCHANGED,
        "Screening Due Date Reason": EXPECT.UNCHANGED,
        "Screening due date date of change": EXPECT.UNCHANGED,
        "Ceased Confirmation Date": EXPECT.TODAY,
        "Calculated Lynch Due Date": EXPECT.NULL,
        "Lynch due date": EXPECT.NULL,
        "Lynch due date reason": EXPECT.UNCHANGED,
        "Lynch due date date of change": EXPECT.UNCHANGED,
        "Surveillance due date": EXPECT.NULL,
        "Surveillance due date reason": EXPECT.UNCHANGED,
        "Surveillance due date date of change": EXPECT.UNCHANGED,
    }

    # Verify database updates match expected values
    ManualCeaseTools.verify_manual_cease_db_fields_dynamic(nhs_number, expected_db)
    logging.info("[ASSERTIONS COMPLETE] No Colon cease scenario validated successfully")
