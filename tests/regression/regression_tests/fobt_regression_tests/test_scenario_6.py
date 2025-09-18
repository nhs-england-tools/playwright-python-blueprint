import pytest
import logging
from datetime import datetime
from playwright.sync_api import Page
from pages.datasets.subject_datasets_page import SubjectDatasetsPage
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
from utils.appointments import book_appointments
from pages.logout.log_out_page import LogoutPage
from pages.base_page import BasePage
from pages.screening_subject_search.advance_fobt_screening_episode_page import (
    AdvanceFOBTScreeningEpisodePage,
)
from pages.screening_subject_search.record_diagnosis_date_page import (
    RecordDiagnosisDatePage,
)
from utils.appointments import AppointmentAttendance
from pages.datasets.colonoscopy_dataset_page import (
    ColonoscopyDatasetsPage,
    FitForColonoscopySspOptions,
)
from utils.sspi_change_steps import SSPIChangeSteps
from pages.screening_subject_search.reopen_fobt_screening_episode_page import (
    ReopenFOBTScreeningEpisodePage,
)
from utils.oracle.oracle import OracleDB


@pytest.mark.usefixtures("setup_org_and_appointments")
@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.fobt_regression_tests
def test_scenario_6(page: Page) -> None:
    """
    Scenario: 6: Non-agreement to diagnostic tests

    S1-S9-S10-S43-A8-A183-A25-J28-J30-A25-(A50)-J10-A100-(A167)-A38-A168-C203 [SSCL7a] J10-A99-A165-A168-C203 [SSCL8a]

    This scenario tests where a subject is suitable but refuses to have a diagnostic test.  This tests both routes to this discharge - one where the patient makes an immediate decision (A38 route) and one where the subject asks for time to consider but does not make a decision within the time limit (A165 route).  It also tests both in-age and over-age closures, and the "further review" functionality of a colonoscopy assessment dataset, where the suitability chosen from the Advance Episode screen does not match with the suitability stored in the dataset.

    Scenario summary:

    > Create a new subject in the FOBT age range > Inactive
    > Run the FOBT failsafe trawl > Call
    > Run the database transition to invite them for FOBT screening > S1(1.1)
    > Process S1 letter batch > S9 (1.1)
    > Run timed events > creates S9 letter (1.1)
    > Process S9 letter batch > S10 (1.1)
    > Log kit > S43 (1.2)
    > Read kit with ABNORMAL result > A8 (1.3)
    > Invite for colonoscopy assessment > A183 (1.11)
    > Process A183 appointment letter > A25 (1.11)
    > SC DNA appointment > J28
    > Rebook colonoscopy assessment > J30 (1.11)
    > Process J30 letter > A25 (1.11)
    > Record diagnosis date (A50)
    > Attend assessment appointment > J10 (1.11)
    > Suitable for radiology > A100 (1.12)
    > Process A183 result letter (A167)
    > Decision not to proceed > A38 (1.12)
    > Process A38 letter batch > A168 (1.12) > C203 (1.13)
    > Check recall [SSCL7a]
    > Reopen following non-response > J10 (1.11)
    > SSPI update changes subject to over-age
    > Suitable for colonoscopy > A99 (1.12)
    > Awaiting decision to proceed > A165 (1.12)
    > Run timed events > creates A165 letter (1.12)
    > Process A165 letter batch > A168 (1.12) > C203 (1.13)
    > Check recall [SSCL8a]
    """

    summary_page = SubjectScreeningSummaryPage(page)
    attendance = AppointmentAttendance(page)
    dataset = ColonoscopyDatasetsPage(page)
    ssp_options = FitForColonoscopySspOptions
    advance_fobt_episode = AdvanceFOBTScreeningEpisodePage(page)

    logging.info(
        "[TEST START] Regression - Scenario: 6: Non-agreement to diagnostic tests"
    )

    # Given I log in to BCSS "England" as user role "Hub Manager"
    user_role = UserTools.user_login(
        page, "Hub Manager at BCS01", return_role_type=True
    )
    if user_role is None:
        raise ValueError("User cannot be assigned to a UserRoleType")

    # And I create a subject that meets the following criteria:
    requirements = {
        "age (y/d)": "68/301",
        "active gp practice in hub/sc": "BCS01/BCS001",
    }
    nhs_no = CreateSubjectSteps().create_custom_subject(requirements)
    if nhs_no is None:
        pytest.fail("Failed to create subject: NHS number not returned.")

    # Then Comment: NHS number
    logging.info(f"[SUBJECT CREATED] NHS number: {nhs_no}")

    # And my subject has been updated as follows:
    criteria = {
        "subject age": "68",
        "subject has episodes": "No",
        "screening status": "Inactive",
    }
    subject_assertion(nhs_no, criteria)

    # Assert subject details in the UI
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    summary_page.assert_subject_age(68)
    summary_page.assert_screening_status("Inactive")

    # When I run the FOBT failsafe trawl for my subject
    CallAndRecallUtils().run_failsafe(nhs_no)

    # Then my subject has been updated as follows:
    criteria = {
        "subject has episodes": "No",
        "Screening Due Date": "Last Birthday",
        "Screening due date date of change": "Today",
        "Screening Due Date Reason": "Failsafe Trawl",
        "screening status": "Call",
        "Screening Status Date of Change": "Today",
        "Screening Status Reason": "Failsafe Trawl",
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
    batch_processing(
        page,
        "S1",
        "Pre-invitation (FIT)",
        "S9 - Pre-invitation Sent",
        True,
    )

    # When I run Timed Events for my subject
    # Then there is a "S9" letter batch for my subject with the exact title "Invitation & Test Kit (FIT)"
    # When I process the open "S9" letter batch for my subject
    # # Then my subject has been updated as follows:
    batch_processing(
        page,
        "S9",
        "Invitation & Test Kit (FIT)",
        "S10 - Invitation & Test Kit Sent",
        True,
    )

    # When I log my subject's latest unlogged FIT kit
    fit_kit = FitKitGeneration().get_fit_kit_for_subject_sql(nhs_no, False, False)
    sample_date = datetime.now()
    FitKitLogged().log_fit_kits(page, fit_kit, sample_date)

    # Then my subject has been updated as follows:
    criteria = {
        "latest event status": "S43 Kit Returned and Logged (Initial Test)",
    }
    subject_assertion(nhs_no, criteria)

    # When I read my subject's latest logged FIT kit as "ABNORMAL"
    FitKitLogged().read_latest_logged_kit(user_role, 2, fit_kit, "ABNORMAL")

    # Then my subject has been updated as follows:
    criteria = {
        "latest event status": "A8 Abnormal",
    }
    subject_assertion(nhs_no, criteria)

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I choose to book a practitioner clinic for my subject
    SubjectScreeningSummaryPage(page).click_book_practitioner_clinic_button()

    # And I select "BCS001" as the screening centre where the practitioner appointment will be held
    # And I set the practitioner appointment date to "today"
    # And I book the "earliest" available practitioner appointment on this date
    book_appointments(
        page,
        "BCS001 - Wolverhampton Bowel Cancer Screening Centre",
        "The Royal Hospital (Wolverhampton)",
    )

    # Then my subject has been updated as follows:
    criteria = {
        "latest event status": "A183 1st Colonoscopy Assessment Appointment Requested",
    }
    subject_assertion(nhs_no, criteria)

    # And there is a "A183" letter batch for my subject with the exact title "Practitioner Clinic 1st Appointment"
    # When I process the open "A183 - Practitioner Clinic 1st Appointment" letter batch for my subject
    # Then my subject has been updated as follows:
    batch_processing(
        page,
        "A183",
        "Practitioner Clinic 1st Appointment",
        "A25 - 1st Colonoscopy Assessment Appointment Booked, letter sent",
    )

    # And there is a "A183" letter batch for my subject with the exact title "GP Result (Abnormal)"
    batch_processing(
        page,
        "A183",
        "GP Result (Abnormal)",
        "A25 - 1st Colonoscopy Assessment Appointment Booked, letter sent",
    )

    # When I switch users to BCSS "England" as user role "Screening Centre Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Screening Centre Manager at BCS001")

    # And I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the event history for the subject's latest episode
    # And I view the latest practitioner appointment in the subject's episode
    # And The Screening Centre DNAs the practitioner appointment
    attendance.mark_as_dna("Screening Centre did not attend")

    # Then my subject has been updated as follows:
    criteria = {
        "latest event status": "J28 Appointment Non-attendance (Screening Centre)",
    }
    subject_assertion(nhs_no, criteria)

    # And I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I choose to book a practitioner clinic for my subject
    SubjectScreeningSummaryPage(page).click_book_practitioner_clinic_button()

    # And I select "BCS001" as the screening centre where the practitioner appointment will be held
    # And I set the practitioner appointment date to "today"
    # And I book the "earliest" available practitioner appointment on this date
    book_appointments(
        page,
        "BCS001 - Wolverhampton Bowel Cancer Screening Centre",
        "The Royal Hospital (Wolverhampton)",
    )

    # Then my subject has been updated as follows:
    criteria = {
        "latest event status": "J30 Appointment Requested (SC Non-attendance Letter)",
    }
    subject_assertion(nhs_no, criteria)

    # And there is a "J30" letter batch for my subject with the exact title "Practitioner Clinic 1st Appointment Non Attendance (Screening Centre)"
    # When I process the open "J30" letter batch for my subject
    # Then my subject has been updated as follows:
    batch_processing(
        page,
        "J30",
        "Practitioner Clinic 1st Appointment Non Attendance (Screening Centre)",
        "A25 - 1st Colonoscopy Assessment Appointment Booked, letter sent",
    )

    # When I switch users to BCSS "England" as user role "Hub Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the advance episode options
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # And I select the advance episode option for "Record Diagnosis Date"
    AdvanceFOBTScreeningEpisodePage(page).click_record_diagnosis_date_button()

    # And I enter a Diagnosis Date of "today"
    RecordDiagnosisDatePage(page).enter_date_in_diagnosis_date_field(datetime.now())

    # And I save Diagnosis Date Information
    RecordDiagnosisDatePage(page).click_save_button()

    # Then my subject has been updated as follows:
    criteria = {
        "latest episode diagnosis date reason": "Null",
        "latest episode has diagnosis date": "Yes",
        "latest episode includes event status": "A50 Diagnosis date recorded",
        "latest event status": "A25 1st Colonoscopy Assessment Appointment Booked",
    }
    subject_assertion(nhs_no, criteria)

    # When I switch users to BCSS "England" as user role "Screening Centre Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Screening Centre Manager at BCS001")

    # And I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the event history for the subject's latest episode
    # And I view the latest practitioner appointment in the subject's episode
    # And I attend the subject's practitioner appointment "today"
    attendance.mark_as_attended()

    # Then my subject has been updated as follows:
    criteria = {
        "latest event status": "J10 Attended Colonoscopy Assessment Appointment",
    }
    subject_assertion(nhs_no, criteria)

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I edit the Colonoscopy Assessment Dataset for this subject
    # And I update the Colonoscopy Assessment Dataset with the following values:
    # 	| Fit for Colonoscopy (SSP) | Unable to assess |
    # 	| Dataset complete?         | Yes              |
    # And I save the Colonoscopy Assessment Dataset
    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_colonoscopy_show_datasets()
    dataset.select_fit_for_colonoscopy_option(ssp_options.UNABLE_TO_ASSESS)
    dataset.click_dataset_complete_radio_button_yes()
    dataset.save_dataset()

    # And I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I advance the subject's episode for "Suitable for Radiological Test"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    advance_fobt_episode.click_suitable_for_radiological_test_button()

    # Then my subject has been updated as follows:
    criteria = {
        "latest event status": "A100 Suitable for Radiological Test",
    }
    subject_assertion(nhs_no, criteria)

    # When I switch users to BCSS "England" as user role "Hub Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Hub Manager at BCS01")

    # Then my subject has been updated as follows:
    criteria = {
        "latest episode includes event status": "A167 GP Abnormal FOBT Result Sent",
        "latest event status": "A100 Suitable for Radiological Test",
    }
    subject_assertion(nhs_no, criteria)

    # When I switch users to BCSS "England" as user role "Screening Centre Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    user_role = UserTools.user_login(page, "Screening Centre Manager at BCS001", True)

    # And I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # 	And I advance the subject's episode for "Decision not to Continue with Diagnostic Test"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    advance_fobt_episode.click_decision_not_to_continue_with_diagnostic_test()

    # Then my subject has been updated as follows:
    # 	| Latest event status | A38 Decision not to Continue with Diagnostic Test |
    criteria = {
        "latest event status": "A38 Decision not to Continue with Diagnostic Test",
    }
    subject_assertion(nhs_no, criteria)

    # And there is a "A38" letter batch for my subject with the exact title "Discharge (No Agreement To Proceed With Diagnostic Tests) - Patient letter"
    # When I process the open "A38" letter batch for my subject
    # Then my subject has been updated as follows:
    batch_processing(
        page,
        "A38",
        "Discharge (No Agreement To Proceed With Diagnostic Tests) - Patient letter",
        "A168 - GP Discharge Sent (No Agreement to Proceed with Diagnostic Tests)",
    )
    criteria = {
        "calculated FOBT due date": "2 years from episode end",
        "calculated lynch due date": "Unchanged",
        "calculated surveillance due date": "Unchanged",
        "ceased confirmation date": "Null",
        "ceased confirmation details": "Null",
        "ceased confirmation user ID": "Null",
        "clinical reason for cease": "Null",
        "latest episode accumulated result": "Definitive abnormal FOBT outcome",
        "latest episode recall calculation method": "Episode end date",
        "latest episode recall episode type": "FOBT Screening",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Closed",
        "latest episode status reason": "Informed Dissent",
        "lynch due date": "Null",
        "lynch due date date of change": "Unchanged",
        "lynch due date reason": "Unchanged",
        "screening due date": "Calculated FOBT due date",
        "screening due date date of change": "Today",
        "screening due date reason": "Recall",
        "screening status": "Recall",
        "screening status date of change": "# Not checking as status may or may not have changed",
        "screening status reason": "Recall",
        "surveillance due date": "Null",
        "surveillance due date date of change": "Unchanged",
        "surveillance due date reason": "Unchanged",
    }
    subject_assertion(nhs_no, criteria)

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I reopen the subject's episode for "Reopen following Non-Response"
    SubjectScreeningSummaryPage(page).click_reopen_fobt_screening_episode_button()
    ReopenFOBTScreeningEpisodePage(page).click_reopen_following_non_response_button()

    # Then my subject has been updated as follows:
    criteria = {
        "calculated FOBT due date": "As at episode start",
        "calculated lynch due date": "Null",
        "calculated surveillance due date": "Null",
        "ceased confirmation date": "Null",
        "ceased confirmation details": "Null",
        "ceased confirmation user ID": "Null",
        "clinical reason for cease": "Null",
        "latest episode accumulated result": "Null",
        "latest episode includes event code": "E62 Reopen following Non-Response",
        "latest episode recall calculation method": "Episode end date",
        "latest episode recall episode type": "Null",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Open",
        "latest episode status reason": "Null",
        "latest event status": "J10 Attended Colonoscopy Assessment Appointment",
        "lynch due date": "Null",
        "lynch due date date of change": "Unchanged",
        "lynch due date reason": "Unchanged",
        "screening due date": "Calculated FOBT due date",
        "screening due date date of change": "Today",
        "screening due date reason": "Reopened episode",
        "screening status": "# Not checking as status may or may not have changed",
        "screening status date of change": "# Not checking as status may or may not have changed",
        "screening status reason": "# Not checking as status may or may not have changed",
        "surveillance due date": "Null",
        "surveillance due date date of change": "Unchanged",
        "surveillance due date reason": "Unchanged",
    }
    subject_assertion(nhs_no, criteria, user_role)

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I receive an SSPI update to change their date of birth to "75" years old
    SSPIChangeSteps().sspi_update_to_change_dob_received(nhs_no, 75)

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the advance episode options
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # And I select the advance episode option for "Suitable for Endoscopic Test"
    AdvanceFOBTScreeningEpisodePage(page).click_suitable_for_endoscopic_test_button()

    # Then I get a confirmation prompt that "contains" "If there has been further discussion regarding the patient's suitability for a colonoscopy then the colonoscopy assessment dataset will be updated with this further review"
    # When I press OK on my confirmation prompt
    # Then my subject has been updated as follows:
    criteria = {
        "latest event status": "A99 Suitable for Endoscopic Test",
    }
    subject_assertion(nhs_no, criteria)

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # When I advance the subject's episode for "Waiting Decision to Proceed with Diagnostic Test"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    advance_fobt_episode.click_waiting_decision_to_proceed_with_diagnostic_test()

    # Then my subject has been updated as follows:
    criteria = {
        "latest event status": "A165 Waiting Decision to Proceed with Diagnostic Test",
    }
    subject_assertion(nhs_no, criteria)

    # When I run Timed Events for my subject
    OracleDB().exec_bcss_timed_events(nhs_number=nhs_no)

    # Then there is a "A165" letter batch for my subject with the exact title "Patient Discharge (No Agreement To Proceed With Diagnostic Tests) - Patient Letter"
    # When I process the open "A165" letter batch for my subject
    # Then my subject has been updated as follows:
    batch_processing(
        page,
        "A165",
        "Patient Discharge (No Agreement To Proceed With Diagnostic Tests) - Patient Letter",
        "A168 - GP Discharge Sent (No Agreement to Proceed with Diagnostic Tests)",
    )
    criteria = {
        "calculated fobt due date": "2 years from episode end",
        "calculated surveillance due date": "Unchanged",
        "ceased confirmation date": "Today",
        "ceased confirmation details": "Outside screening population at recall.",
        "ceased confirmation user id": "User's ID",
        "clinical reason for cease": "Null",
        "latest episode accumulated result": "Definitive abnormal FOBT outcome",
        "latest episode recall calculation method": "Episode end date",
        "latest episode recall episode type": "FOBT Screening",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Closed",
        "latest episode status reason": "Informed Dissent",
        "lynch due date": "Null",
        "lynch due date date of change": "Unchanged",
        "lynch due date reason": "Unchanged",
        "screening due date": "Null",
        "screening due date date of change": "Today",
        "screening due date reason": "Ceased",
        "screening status": "Ceased",
        "screening status date of change": "Today",
        "screening status reason": "Outside screening population",
        "surveillance due date": "Null",
        "surveillance due date date of change": "Unchanged",
        "surveillance due date reason": "Unchanged",
    }
    subject_assertion(nhs_no, criteria, user_role)

    logging.info("[TEST COMPLETE] Scenario 6 passed all assertions")
    LogoutPage(page).log_out()
