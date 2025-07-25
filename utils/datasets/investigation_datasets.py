import pandas as pd
from classes.user import User
from classes.subject import Subject
from datetime import datetime
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.screening_subject_search.attend_diagnostic_test_page import (
    AttendDiagnosticTestPage,
)
from pages.screening_subject_search.contact_with_patient_page import (
    ContactWithPatientPage,
)
from pages.screening_subject_search.diagnostic_test_outcome_page import (
    DiagnosticTestOutcomePage,
    OutcomeOfDiagnosticTest,
)
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from pages.screening_subject_search.advance_fobt_screening_episode_page import (
    AdvanceFOBTScreeningEpisodePage,
)
from utils.batch_processing import batch_processing
from utils.calendar_picker import CalendarPicker
from utils.oracle.oracle import OracleDB
from utils.oracle.subject_selection_query_builder import SubjectSelectionQueryBuilder
from utils.screening_subject_page_searcher import (
    search_subject_episode_by_nhs_number,
)
from pages.datasets.investigation_dataset_page import (
    DrugTypeOptions,
    BowelPreparationQualityOptions,
    ComfortOptions,
    EndoscopyLocationOptions,
    YesNoOptions,
    InsufflationOptions,
    OutcomeAtTimeOfProcedureOptions,
    LateOutcomeOptions,
    InvestigationDatasetsPage,
)
from typing import Optional
from utils.investigation_dataset import (
    InvestigationDatasetCompletion,
)
import logging
from pages.logout.log_out_page import LogoutPage


def get_subject_with_investigation_dataset_ready() -> pd.DataFrame:
    """
    This functions obtains 1 subject who is ready to have their investigation dataset complete
    """
    criteria = {
        "latest episode status": "open",
        "latest episode latest investigation dataset": "colonoscopy_new",
        "latest episode started": "less than 4 years ago",
    }
    user = User()
    subject = Subject()

    builder = SubjectSelectionQueryBuilder()

    query, bind_vars = builder.build_subject_selection_query(
        criteria=criteria,
        user=user,
        subject=subject,
        subjects_to_retrieve=1,
    )

    df = OracleDB().execute_query(query, bind_vars)
    return df


def get_subject_with_a99_status() -> pd.DataFrame:
    """
    This functions obtains 1 subject who has the latest episode status A99 - Suitable for Endoscopic Test
    """
    criteria = {
        "latest episode has colonoscopy assessment dataset": "yes_complete",
        "latest episode has diagnostic test": "no",
        "latest event status": "A99",
        "latest episode type": "FOBT",
        "latest episode started": "less than 4 years ago",
    }
    user = User()
    subject = Subject()

    builder = SubjectSelectionQueryBuilder()

    query, bind_vars = builder.build_subject_selection_query(
        criteria=criteria,
        user=user,
        subject=subject,
        subjects_to_retrieve=1,
    )

    df = OracleDB().execute_query(query, bind_vars)
    return df


def go_from_a99_status_to_a259_status(page: Page, nhs_no: str) -> None:
    """
    Takes a subject who has the latest episode status A99 - Suitable for Endoscopic Test
    and takes them to A259 - Attended Diagnostic Test.

    Args:
        nhs_no (str): The NHS number of the subject.
    """
    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    AdvanceFOBTScreeningEpisodePage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())

    AdvanceFOBTScreeningEpisodePage(page).select_test_type_dropdown_option(
        "Colonoscopy"
    )

    AdvanceFOBTScreeningEpisodePage(page).click_invite_for_diagnostic_test_button()
    AdvanceFOBTScreeningEpisodePage(page).verify_latest_event_status_value(
        "A59 - Invited for Diagnostic Test"
    )

    AdvanceFOBTScreeningEpisodePage(page).click_attend_diagnostic_test_button()

    AttendDiagnosticTestPage(page).select_actual_type_of_test_dropdown_option(
        "Colonoscopy"
    )
    AttendDiagnosticTestPage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())
    AttendDiagnosticTestPage(page).click_save_button()
    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A259 - Attended Diagnostic Test"
    )


def go_from_investigation_dataset_complete_to_a259_status(page: Page) -> None:
    """
    Takes a subject who has just had thier investigation dataset compelted to having the event status A259 - Attended Diagnostic Test.
    """
    BasePage(page).click_back_button()
    BasePage(page).click_back_button()
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_enter_diagnostic_test_outcome_button()
    DiagnosticTestOutcomePage(page).select_test_outcome_option(
        OutcomeOfDiagnosticTest.FAILED_TEST_REFER_ANOTHER
    )
    DiagnosticTestOutcomePage(page).click_save_button()
    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A315 - Diagnostic Test Outcome Entered"
    )

    # Make post investigation contact > A361
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_other_post_investigation_button()
    AdvanceFOBTScreeningEpisodePage(page).verify_latest_event_status_value(
        "A361 - Other Post-investigation Contact Required"
    )

    AdvanceFOBTScreeningEpisodePage(
        page
    ).click_record_other_post_investigation_contact_button()
    ContactWithPatientPage(page).record_post_investigation_appointment_not_required()
    BasePage(page).click_back_button()
    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A318 - Post-investigation Appointment NOT Required - Result Letter Created"
    )

    # Process the A318 letters > A380
    batch_processing(
        page,
        "A318",
        "Result Letters - No Post-investigation Appointment",
        "A380 - Failed Diagnostic Test - Refer Another",
    )

    # Another contact to bring the subject back to A99
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_record_contact_with_patient_button()
    ContactWithPatientPage(page).select_direction_dropdown_option("To patient")
    ContactWithPatientPage(page).select_caller_id_dropdown_index_option(1)
    ContactWithPatientPage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())
    ContactWithPatientPage(page).enter_start_time("11:00")
    ContactWithPatientPage(page).enter_end_time("12:00")
    ContactWithPatientPage(page).enter_discussion_record_text("Test Automation")
    ContactWithPatientPage(page).select_outcome_dropdown_option(
        "Suitable for Endoscopic Test"
    )
    ContactWithPatientPage(page).click_save_button()
    AdvanceFOBTScreeningEpisodePage(page).verify_latest_event_status_value(
        "A99 - Suitable for Endoscopic Test"
    )

    # Invite for 2nd diagnostic test > A59 - check options
    AdvanceFOBTScreeningEpisodePage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())
    AdvanceFOBTScreeningEpisodePage(page).select_test_type_dropdown_option_2(
        "Colonoscopy"
    )
    AdvanceFOBTScreeningEpisodePage(page).click_invite_for_diagnostic_test_button()
    AdvanceFOBTScreeningEpisodePage(page).click_attend_diagnostic_test_button()
    AttendDiagnosticTestPage(page).select_actual_type_of_test_dropdown_option(
        "Colonoscopy"
    )
    AttendDiagnosticTestPage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())
    AttendDiagnosticTestPage(page).click_save_button()
    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A259 - Attended Diagnostic Test"
    )


def get_default_general_information() -> dict:
    """Return default general information for investigation dataset tests."""
    return {
        "site": -1,
        "practitioner": -1,
        "testing clinician": -1,
        "aspirant endoscopist": None,
    }


def get_default_drug_information() -> dict:
    """Return default drug information for investigation dataset tests."""
    return {
        "drug_type1": DrugTypeOptions.MANNITOL,
        "drug_dose1": "3",
    }


def get_default_endoscopy_information() -> dict:
    """Return default endoscopy information for investigation dataset tests."""
    return {
        "endoscope inserted": "yes",
        "procedure type": "therapeutic",
        "bowel preparation quality": BowelPreparationQualityOptions.GOOD,
        "comfort during examination": ComfortOptions.NO_DISCOMFORT,
        "comfort during recovery": ComfortOptions.NO_DISCOMFORT,
        "endoscopist defined extent": EndoscopyLocationOptions.DESCENDING_COLON,
        "scope imager used": YesNoOptions.YES,
        "retroverted view": YesNoOptions.NO,
        "start of intubation time": "09:00",
        "start of extubation time": "09:30",
        "end time of procedure": "10:00",
        "scope id": "Autotest",
        "insufflation": InsufflationOptions.AIR,
        "outcome at time of procedure": OutcomeAtTimeOfProcedureOptions.LEAVE_DEPARTMENT,
        "late outcome": LateOutcomeOptions.NO_COMPLICATIONS,
    }


def complete_and_assert_investigation(
    page: Page,
    general_information: dict,
    drug_information: dict,
    endoscopy_information: dict,
    failure_information: dict,
    polyp_1_information: dict,
    polyp_1_intervention: dict,
    polyp_1_histology: dict,
    expected_category: str,
    expected_size: str,
    completion_information: Optional[dict] = None,
) -> None:
    """
    Fills the investigation dataset, asserts results, and marks dataset not complete.
    """
    polyp_information = [polyp_1_information]
    polyp_intervention = [polyp_1_intervention]
    polyp_histology = [polyp_1_histology]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        polyp_information=polyp_information,
        polyp_intervention=polyp_intervention,
        polyp_histology=polyp_histology,
        completion_information=completion_information,
    )

    InvestigationDatasetsPage(page).assert_polyp_algorithm_size(1, expected_size)
    InvestigationDatasetsPage(page).assert_polyp_category(1, expected_category)

    mark_dataset_not_complete_and_assert(page)


def mark_dataset_not_complete_and_assert(page: Page) -> None:
    """
    Marks the investigation dataset as not complete and asserts that the polyp size and category are None.
    """
    logging.info("Marking investigation dataset not complete")
    InvestigationDatasetsPage(page).click_edit_dataset_button()
    InvestigationDatasetsPage(page).check_dataset_incomplete_checkbox()
    InvestigationDatasetsPage(page).click_save_dataset_button()
    InvestigationDatasetsPage(page).assert_polyp_algorithm_size(1, None)
    InvestigationDatasetsPage(page).assert_polyp_category(1, None)
    LogoutPage(page).log_out()
