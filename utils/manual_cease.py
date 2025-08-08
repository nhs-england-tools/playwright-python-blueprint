import logging
import pandas as pd
from utils.oracle.oracle import OracleDB
from datetime import datetime, date
from enum import IntEnum
from pages.manual_cease.manual_cease_page import ManualCeasePage
from playwright.sync_api import TimeoutError


class ManualCeaseTools:
    """
    This class provides utility functions for handling manual ceases in the BCSS system.
    It includes methods to create subjects ready for manual cease and to process manual ceases.
    """

    # Map readable labels to real DB columns
    _DYNAMIC_COLUMN_MAP = {
        "Screening Status": "screening_status_id",
        "Screening Status Reason": "ss_reason_for_change_id",
        "Screening Status Date of Change": "screening_status_change_date",
        "Screening Due Date Reason": "sdd_reason_for_change_id",
        "Screening Due Date": "screening_due_date",
        "Ceased Confirmation Details": "ceased_confirmation_details",
        "Ceased Confirmation Date": "ceased_confirmation_recd_date",
        "Clinical Reason for Cease": "lynch_sdd_reason_for_change_id",
        "Calculated FOBT Due Date": "calculated_sdd",
        "Calculated Lynch Due Date": "lynch_calculated_sdd",
        "Calculated Surveillance Due Date": "calculated_sdd",
        "Lynch due date": "lynch_screening_due_date",
        "Lynch due date reason": "lynch_sdd_reason_for_change_id",
        "Lynch due date date of change": "lynch_sdd_change_date",
        "Screening due date date of change": "screening_status_change_date",
        "Surveillance due date": "surveillance_screen_due_date",
        "Surveillance due date reason": "sdd_reason_for_change_id",
        "Surveillance due date date of change": "surveillance_sdd_change_date",
    }

    @staticmethod
    def create_manual_cease_ready_subject(
        screening_centre: str = "BCS002", base_age: int = 75
    ) -> str:
        """
        Creates a subject with 'Inactive' screening status suitable for manual cease.
        Executes timeline progression to match expected system behavior.

        Args:
            screening_centre (str): Screening centre code for subject association.
            base_age (int): Minimum age to filter subject candidates.

        Returns:
            str: NHS number of the created subject.
        """
        from utils.oracle.oracle import (
            OracleSubjectTools,
        )  # import here to avoid circulars

        oracle_subject = OracleSubjectTools()
        oracle_subject.create_subjects_via_sspi(
            count=1,
            screening_centre=screening_centre,
            base_age=base_age,
            start_offset=-2,
            end_offset=3,
            nhs_start=9300000000,
        )

        query = """
            SELECT s.SUBJECT_NHS_NUMBER
            FROM SCREENING_SUBJECT_T s
            WHERE s.SCREENING_STATUS_ID = 4002
            ORDER BY s.SUBJECT_NHS_NUMBER DESC
            FETCH FIRST 1 ROWS ONLY
        """
        df = OracleDB().execute_query(query)

        if df.empty:
            raise RuntimeError("No Inactive subject found post creation")

        nhs_number = df.iloc[0]["subject_nhs_number"]
        logging.info(f"[SUBJECT CREATED - INACTIVE] NHS number: {nhs_number}")

        nhs_df = pd.DataFrame({"subject_nhs_number": [nhs_number]})
        OracleDB().exec_bcss_timed_events(nhs_df)

        logging.info(
            f"[TIMED EVENTS COMPLETE] Subject ready for manual cease: {nhs_number}"
        )
        return nhs_number

    @staticmethod
    def process_manual_cease_with_disclaimer(
        manual_cease_page: ManualCeasePage, reason: str = "Informed Dissent"
    ) -> None:
        """
        Executes the full (non-immediate) manual cease workflow via UI, including:
        - Optional steps: Requesting cease, selecting reason, saving
        - Required steps: Sending disclaimer letter, recording return, finalizing cease

        Args:
            page (Page): Playwright page object representing the browser session.
            reason (str): Cease reason to select from the dropdown.
        """
        logging.info("[MANUAL CEASE] Starting full cease workflow")

        try:
            # Check if Request Cease button is visible (if not, move to step 4)
            manual_cease_page.request_cease_button.wait_for(timeout=3000)
            logging.info(
                "[CHECK] 'Request Cease' button is present — proceeding with steps 1-3"
            )

            # Step 1: Click "Request Cease"
            manual_cease_page.click_request_cease()
            logging.info("[STEP 1] Clicked 'Request Cease'")

            # Step 2: Select reason
            manual_cease_page.select_cease_reason(reason)
            logging.info(f"[STEP 2] Selected cease reason: {reason}")

            # Step 3: Save cease request
            manual_cease_page.click_save_request_cease()
            logging.info("[STEP 3] Clicked 'Save Request Cease'")

        except TimeoutError:
            logging.info(
                "[CHECK] 'Request Cease' button not found — skipping steps 1-3"
            )

        # Step 4: Record Disclaimer Letter Sent
        manual_cease_page.record_disclaimer_sent()
        logging.info("[STEP 4] Clicked 'Record Disclaimer Letter Sent'")

        # Step 5: Confirm manual sending of disclaimer letter
        manual_cease_page.confirm_disclaimer_sent()
        logging.info("[STEP 5] Confirmed disclaimer letter sent")

        # Step 6: Record Return of Disclaimer letter
        manual_cease_page.record_return_of_disclaimer()
        logging.info("[STEP 6] Clicked 'Record Return of Disclaimer Letter'")

        # Step 7: Final confirmation (Record Informed Dissent screen)
        manual_cease_page.fill_notes_and_date()
        logging.info("[STEP 7] Entered note and today's date")

        # Step 8: Confirm cease
        manual_cease_page.confirm_cease()
        logging.info("[STEP 8] Clicked 'Confirm Cease'")

    @staticmethod
    def process_manual_cease_immediate(
        manual_cease_page: ManualCeasePage, reason: str = "Informed Dissent"
    ) -> None:
        """
        Executes the manual cease workflow via UI. Handles both standard and simplified cease paths:
        - Clicks 'Request Cease'
        - Selects cease reason from dropdown
        - Conditionally enters notes and date if visible
        - Clicks either 'Confirm Cease' or 'Save Request Cease'

        Args:
            page (Page): Playwright page object representing the browser session.
            reason (str): Cease reason to select from the dropdown.
        """
        logging.info("[MANUAL CEASE] Starting full cease workflow")

        # Step 1: Click "Request Cease"
        manual_cease_page.click_request_cease()
        logging.info("[STEP 1] Clicked 'Request Cease'")

        # Step 2: Select reason from dropdown
        manual_cease_page.select_cease_reason(reason)
        logging.info(f"[STEP 2] Selected cease reason: {reason}")

        # Step 3: Conditionally enter notes and today's date
        today_str = datetime.today().strftime("%d/%m/%Y")
        manual_cease_page.fill_notes_if_visible()
        manual_cease_page.fill_date_if_visible(today_str)
        logging.info("[STEP 3] Entered note and today's date: {date_str}")

        # Step 4: Confirm cease via available button
        manual_cease_page.confirm_or_save_cease()
        logging.info("[STEP 4] Clicked 'Confirm Cease' or 'Save Request Cease'")

    @staticmethod
    def verify_manual_cease_db_fields_dynamic(
        nhs_number: str, expected: dict[str, object]
    ) -> None:
        """
        Dynamically builds SELECT query based on only expected fields.
        Prevents breakage when invalid columns are present in static map.
        """
        cols_sql = ",\n    ".join(
            f'{ManualCeaseTools._DYNAMIC_COLUMN_MAP[label]} AS "{label}"'
            for label in expected
            if label in ManualCeaseTools._DYNAMIC_COLUMN_MAP
        )

        query = f"""
            SELECT
                {cols_sql}
            FROM SCREENING_SUBJECT_T
            WHERE SUBJECT_NHS_NUMBER = :nhs_number
        """

        df = OracleDB().execute_query(query, {"nhs_number": nhs_number})
        if df.empty:
            raise AssertionError(f"No DB record for NHS {nhs_number}")

        row = df.iloc[0]

        for label, exp in expected.items():
            actual = row[label]

            if exp is EXPECT.TODAY:
                today_str = date.today().isoformat()
                assert str(actual).startswith(today_str), f"{label}: expected today"

            elif exp is EXPECT.NULL:
                assert pd.isna(actual), f"{label}: expected NULL"

            elif exp is EXPECT.UNCHANGED:
                _ = actual  # pass if exists

            else:
                assert actual == exp, f"{label}: expected {exp!r}, got {actual!r}"


# Markers for special assertions
class EXPECT:
    TODAY = object()  # Date must be today
    NULL = object()  # DB value must be NULL
    UNCHANGED = object()  # Column must exist (no change)
    MATCH_USER_ID = object()  # Must be an integer user ID


class ScreeningStatus(IntEnum):
    ACTIVE = 4001
    INACTIVE = 4002
    SUSPENDED = 4003
    CEASED = 4008


class ScreeningStatusReason(IntEnum):
    INFORMED_DISSENT = 43
    INFORMED_DISSENT_VERBAL = 44
    MOVED_AWAY = 44
    DECEASED = 45
    OTHER = 46
    NO_COLON_SUBJECT_REQUEST = 45
    NO_COLON_PROGRAMME_ASSESSED = 46
    INFORMAL_DEATH = 47


class ScreeningDueDateReason(IntEnum):
    CEASED = 11329
    POSTPONED = 11330
    RESCHEDULED = 11331


class SurveillanceDueDateReason(IntEnum):
    CEASED = 11329
