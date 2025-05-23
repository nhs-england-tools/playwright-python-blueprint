import pytest
from playwright.sync_api import Page
from utils.user_tools import UserTools
from utils.screening_subject_page_searcher import verify_subject_event_status_by_nhs_no
from utils.batch_processing import batch_processing
from pages.logout.log_out_page import LogoutPage
from utils.oracle.oracle_specific_functions import (
    get_subjects_for_investigation_dataset_updates,
)
from utils.subject_demographics import SubjectDemographicUtil
from utils.investigation_dataset import (
    InvestigationDatasetCompletion,
    InvestigationDatasetResults,
    AfterInvestigationDatasetComplete,
)
import logging


@pytest.mark.vpn_required
@pytest.mark.smokescreen
@pytest.mark.compartment6
def test_compartment_6(page: Page, smokescreen_properties: dict) -> None:
    """
    This is the main compartment 6 method
    This test fills out the investigation datasets for different subjects to get different outcomes for a diagnostic test
    based on the test results and the subject's age, then prints the diagnostic test result letters.
    If the subject is old enough and they get a high-risk or LNPCP result, then they are handed over
    into symptomatic care, and the relevant letters are printed.
    Here old refers to if a subject is over 75 at recall
    """

    # For the following tests 'old' refers to if a subject is over 75 at recall
    # The recall period is 2 years from the last diagnostic test for a Normal or Abnormal diagnostic test result
    # or 3 years for someone who is going in to Surveillance (High-risk findings or LNPCP)

    UserTools.user_login(page, "Screening Centre Manager at BCS001")

    # Older patient - High Risk Result
    logging.info("High-risk result for an older subject")
    subjects_df = get_subjects_for_investigation_dataset_updates(
        smokescreen_properties["c6_eng_number_of_subjects_to_record"],
        smokescreen_properties["c6_eng_org_id"],
    )
    logging.info("Fetched subjects for investigation dataset updates.")
    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    logging.info(f"Selected NHS number for older subject: {nhs_no}")
    SubjectDemographicUtil(page).update_subject_dob(nhs_no, False)
    logging.info(
        f"Updated date of birth for NHS number {nhs_no} to indicate an older subject."
    )
    InvestigationDatasetCompletion(page).complete_with_result(
        nhs_no, InvestigationDatasetResults.HIGH_RISK
    )
    logging.info(
        f"Completed investigation dataset for NHS number {nhs_no} with result: HIGH_RISK."
    )
    AfterInvestigationDatasetComplete(page).progress_episode_based_on_result(
        InvestigationDatasetResults.HIGH_RISK, False
    )
    logging.info(
        f"Progressed episode for NHS number {nhs_no} based on result: HIGH_RISK."
    )

    # Younger patient - High Risk Result
    logging.info("High-risk result for a younger subject")
    nhs_no = subjects_df["subject_nhs_number"].iloc[1]
    logging.info(f"Selected NHS number for younger subject: {nhs_no}")
    SubjectDemographicUtil(page).update_subject_dob(nhs_no, True)
    logging.info(
        f"Updated date of birth for NHS number {nhs_no} to indicate a younger subject."
    )
    InvestigationDatasetCompletion(page).complete_with_result(
        nhs_no, InvestigationDatasetResults.HIGH_RISK
    )
    logging.info(
        f"Completed investigation dataset for NHS number {nhs_no} with result: HIGH_RISK."
    )
    AfterInvestigationDatasetComplete(page).progress_episode_based_on_result(
        InvestigationDatasetResults.HIGH_RISK, True
    )
    logging.info(
        f"Progressed episode for NHS number {nhs_no} based on result: HIGH_RISK."
    )

    # Older patient - LNPCP Result
    logging.info("LNPCP result for an older subject")
    nhs_no = subjects_df["subject_nhs_number"].iloc[2]
    logging.info(f"Selected NHS number for older subject: {nhs_no}")
    SubjectDemographicUtil(page).update_subject_dob(nhs_no, False)
    logging.info(
        f"Updated date of birth for NHS number {nhs_no} to indicate an older subject."
    )
    InvestigationDatasetCompletion(page).complete_with_result(
        nhs_no, InvestigationDatasetResults.LNPCP
    )
    logging.info(
        f"Completed investigation dataset for NHS number {nhs_no} with result: LNPCP."
    )
    AfterInvestigationDatasetComplete(page).progress_episode_based_on_result(
        InvestigationDatasetResults.LNPCP, False
    )
    logging.info(f"Progressed episode for NHS number {nhs_no} based on result: LNPCP.")

    # Younger patient - LNPCP Result
    logging.info("LNPCP result for a younger subject")
    nhs_no = subjects_df["subject_nhs_number"].iloc[3]
    logging.info(f"Selected NHS number for younger subject: {nhs_no}")
    SubjectDemographicUtil(page).update_subject_dob(nhs_no, True)
    logging.info(f"Updated date of birth for NHS number {nhs_no} to indicate a younger subject.")
    InvestigationDatasetCompletion(page).complete_with_result(
        nhs_no, InvestigationDatasetResults.LNPCP
    )
    logging.info(f"Completed investigation dataset for NHS number {nhs_no} with result: LNPCP.")
    AfterInvestigationDatasetComplete(page).progress_episode_based_on_result(
        InvestigationDatasetResults.LNPCP, True
    )
    logging.info(f"Progressed episode for NHS number {nhs_no} based on result: LNPCP.")

    # Any patient -  Normal Result
    logging.info("Normal result for any age subject")
    nhs_no_normal = subjects_df["subject_nhs_number"].iloc[4]
    logging.info(f"Selected NHS number for normal result: {nhs_no_normal}")
    InvestigationDatasetCompletion(page).complete_with_result(
        nhs_no_normal, InvestigationDatasetResults.NORMAL
    )
    logging.info(
        f"Completed investigation dataset for NHS number {nhs_no_normal} with result: NORMAL."
    )
    AfterInvestigationDatasetComplete(page).progress_episode_based_on_result(
        InvestigationDatasetResults.NORMAL, True
    )
    logging.info(f"Progressed episode for NHS number {nhs_no_normal} based on result: NORMAL.")
    # Batch processing for result letters
    logging.info("Starting batch processing for result letters.")
    batch_processing(
        page,
        "A318",
        "Result Letters - No Post-investigation Appointment",
        [
            "S61 - Normal (No Abnormalities Found)",
            "A158 - High-risk findings",
            "A157 - LNPCP",
        ],
    )

    # This is to check for the status of a normal subject as this NHS Number cannot be retrieved from the DB
    verify_subject_event_status_by_nhs_no(
        page, nhs_no_normal, "S61 - Normal (No Abnormalities Found)"
    )

    batch_processing(
        page,
        "A385",
        "Handover into Symptomatic Care Adenoma Surveillance, Age - GP Letter",
        "A382 - Handover into Symptomatic Care - GP Letter Printed",
    )

    batch_processing(
        page,
        "A382",
        "Handover into Symptomatic Care Adenoma Surveillance - Patient Letter",
        "P202 - Waiting Completion of Outstanding Events",
    )

    LogoutPage(page).log_out()
