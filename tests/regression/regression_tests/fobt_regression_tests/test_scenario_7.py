import pytest
import logging
from datetime import datetime, timedelta
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
from utils.appointments import book_appointments
from utils.sspi_change_steps import SSPIChangeSteps
from pages.logout.log_out_page import LogoutPage
from pages.base_page import BasePage
from pages.screening_subject_search.episode_events_and_notes_page import (
    EpisodeEventsAndNotesPage,
)
from pages.screening_practitioner_appointments.appointment_detail_page import (
    AppointmentDetailPage,
)
from pages.screening_subject_search.reopen_fobt_screening_episode_page import (
    ReopenFOBTScreeningEpisodePage,
)
from pages.screening_subject_search.advance_fobt_screening_episode_page import (
    AdvanceFOBTScreeningEpisodePage,
)
from pages.screening_subject_search.patient_advised_of_diagnosis_page import (
    PatientAdvisedOfDiagnosisPage,
)
from pages.datasets.subject_datasets_page import SubjectDatasetsPage
from pages.datasets.colonoscopy_dataset_page import (
    ColonoscopyDatasetsPage,
    FitForColonoscopySspOptions,
)


@pytest.mark.usefixtures("setup_org_and_appointments")
@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.fobt_regression_tests
def test_scenario_7(page: Page) -> None:
    """
    Scenario: 7: Patient is unsuitable for diagnostic tests

    S9-S10-S43-A8-A183-A25-J10-S92-C203 [SSCL33d] J10-(A51)-(A167)-J1-J34-J35-J10-J15-J16-J17-C203 [SSCL4a(J17)]

    This scenario tests where a patient is discharged as unsuitable for diagnostic tests, following attendance at a colonoscopy assessment appointment.  It also tests booking and attending a subsequent colonoscopy assessment appointment, after attending the initial assessment appointment, and a mid-episode SSPI cease and uncease then reopen.  Note that although the subject has had an FOBT episode, the uncease puts them back to their previous screening status, Call, rather than Recall.

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
    > Attend assessment appointment > J10 (1.11)
    > SSPI update ceases subject for death > S92 > C203 (1.13)
    > Check recall [SSCL33d]
    > SSPI update unceases subject [SSUN4]
    > Reopen episode for correction > J10 (1.11)
    > Amend diagnosis date (A51)
    > Process A183 result letter (A167) (1.11)
    > Another assessment required > J1 (1.12)
    > Invite for colonoscopy assessment > J34 (1.11)
    > Process J34 letter > J35 (1.11)
    > Attend assessment appointment > J10 (1.11)
    > Unsuitable for diagnostic tests > J15 (1.12)
    > Process J15 letter batch > J16 (1.12)
    > Process J16 letter batch > J17 (1.12) > C203 (1.13)
    > Check recall [SSCL4a(J17)]


    Note: A latest episode diagnosis date reason of "SSPI update - patient deceased" is not cleared down as part of this reopen, even though it probably should be as it was added by the SSPI automated process. Because it is not, in order to set the diagnosis date after the reopen the Amend Diagnosis Date (interrupt) option must be used.
    """
    # Given I log in to BCSS "England" as user role "Hub Manager"
    user_role = UserTools.user_login(
        page, "Hub Manager State Registered at BCS01", return_role_type=True
    )
    if user_role is None:
        raise ValueError("User cannot be assigned to a UserRoleType")

    requirements = {
        "age (y/d)": "61/3",
        "active gp practice in hub/sc": "BCS01/BCS001",
    }
    nhs_no = CreateSubjectSteps().create_custom_subject(requirements)
    if nhs_no is None:
        raise ValueError("NHS No is 'None'")

    # Then Comment: NHS number
    logging.info(f"[SUBJECT CREATION] Created subject's NHS number: {nhs_no}")

    # Then my subject has been updated as follows:
    criteria = {
        "subject age": "61",
        "subject has episodes": "No",
        "screening status": "Inactive",
    }
    subject_assertion(nhs_no, criteria)

    # Navigate to subject summary page in UI
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # Assert subject details in the UI
    SubjectScreeningSummaryPage(page).assert_subject_age(61)
    SubjectScreeningSummaryPage(page).assert_screening_status("Inactive")

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

    # Navigate to subject summary page in UI
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # Assert subject details in the UI
    SubjectScreeningSummaryPage(page).assert_screening_status("Call")

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
    # Then my subject has been updated as follows:
    # When I run Timed Events for my subject
    batch_processing(
        page, "S1", "Pre-invitation (FIT)", "S9 - Pre-invitation Sent", True
    )

    # Then there is a "S9" letter batch for my subject with the exact title "Invitation & Test Kit (FIT)"
    # When I process the open "S9" letter batch for my subject
    # Then my subject has been updated as follows:
    batch_processing(
        page,
        "S9",
        "Invitation & Test Kit (FIT)",
        "S10 - Invitation & Test Kit Sent",
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

    # When I read my subject's latest logged FIT kit as "SPOILT"
    FitKitLogged().read_latest_logged_kit(user_role, 2, fit_kit, "ABNORMAL")

    # Then my subject has been updated as follows:
    subject_assertion(nhs_no, {"latest event status": "A8 Abnormal"})

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
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A183 1st Colonoscopy Assessment Appointment Requested",
        },
    )

    # And there is a "A183" letter batch for my subject with the exact title "Practitioner Clinic 1st Appointment"
    # When I process the open "A183 - Practitioner Clinic 1st Appointment" letter batch for my subject
    # Then my subject has been updated as follows:
    batch_processing(
        page,
        "A183",
        "Practitioner Clinic 1st Appointment",
        "A25 - 1st Colonoscopy Assessment Appointment Booked, letter sent",
    )

    # When I switch users to BCSS "England" as user role "Screening Centre Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Screening Centre Manager at BCS001")

    # And I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the event history for the subject's latest episode
    SubjectScreeningSummaryPage(page).expand_episodes_list()
    SubjectScreeningSummaryPage(page).click_first_fobt_episode_link()

    # And I view the latest practitioner appointment in the subject's episode
    EpisodeEventsAndNotesPage(page).click_most_recent_view_appointment_link()

    # And I attend the subject's practitioner appointment "yesterday"
    AppointmentDetailPage(page).mark_appointment_as_attended(
        datetime.today() - timedelta(1)
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "J10 Attended Colonoscopy Assessment Appointment",
        },
    )

    # When I process an SSPI update for deduction code "DEA"
    SSPIChangeSteps().process_sspi_deduction_by_code(nhs_no, "DEA")

    # Then my subject has been updated as follows:
    criteria = {
        "calculated fobt due date": "2 years from episode end",
        "calculated lynch due date": "Null",
        "calculated surveillance due date": "Null",
        "ceased confirmation date": "Today",
        "ceased confirmation details": "SSPI deduction for death received.",
        "ceased confirmation user id": "automated process id",
        "clinical reason for cease": "Null",
        "latest episode accumulated result": "Definitive abnormal FOBt outcome",
        "latest episode has diagnosis date": "No",
        "latest episode includes event status": "A52",
        "latest episode recall calculation method": "S92 Interrupt Close Date",
        "latest episode recall episode type": "FOBT Screening",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Closed",
        "latest episode status reason": "Deceased",
        "latest event status": "S92",
        "lynch due date": "Null",
        "lynch due date date of change": "Unchanged",
        "lynch due date reason": "unchanged",
        "pre-interrupt event status": "J10",
        "previous screening status": "Call",
        "screening due date": "Null",
        "screening due date date of change": "Today",
        "screening due date reason": "Ceased",
        "screening status": "Ceased",
        "screening status date of change": "Today",
        "screening status reason": "Deceased",
        "surveillance due date date of change": "Unchanged",
        "surveillance due date reason": "unchanged",
        "surveillance due date": "Null",
    }
    subject_assertion(nhs_no, criteria)

    # When I process an SSPI update to re-register my subject with their latest GP practice
    SSPIChangeSteps().reregister_subject_with_latest_gp_practice(nhs_no)

    # Then my subject has been updated as follows:
    criteria = {
        "calculated fobt due date": "Unchanged",
        "calculated lynch due date": "Null",
        "calculated surveillance due date": "Null",
        "ceased confirmation date": "Null",
        "ceased confirmation details": "Null",
        "ceased confirmation user id": "Null",
        "clinical reason for cease": "Null",
        "latest episode accumulated result": "Definitive abnormal FOBt outcome",
        "latest episode diagnosis date reason": "SSPI update - patient deceased",
        "latest episode has diagnosis date": "No",
        "latest episode recall calculation method": "S92 Interrupt Close Date",
        "latest episode recall episode type": "FOBT Screening",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Closed",
        "latest episode status reason": "Deceased",
        "latest event status": "S92",
        "lynch due date": "Null",
        "lynch due date date of change": "Unchanged",
        "lynch due date reason": "unchanged",
        "screening due date": "Calculated FOBT due date",
        "screening due date date of change": "Today",
        "screening due date reason": "Reversal of Death Notification",
        "screening status": "Call",
        "screening status date of change": "Today",
        "screening status reason": "Reversal of Death Notification",
        "surveillance due date date of change": "Unchanged",
        "surveillance due date reason": "unchanged",
        "surveillance due date": "Null",
    }
    subject_assertion(nhs_no, criteria)

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I reopen the subject's episode for "Reopen episode for correction"
    SubjectScreeningSummaryPage(page).click_reopen_fobt_screening_episode_button()
    ReopenFOBTScreeningEpisodePage(page).click_reopen_episode_for_correction_button()

    # Then my subject has been updated as follows:
    criteria = {
        "calculated fobt due date": "As at episode start",
        "calculated lynch due date": "Null",
        "calculated surveillance due date": "Null",
        "ceased confirmation date": "Null",
        "ceased confirmation details": "Null",
        "ceased confirmation user id": "Null",
        "clinical reason for cease": "Null",
        "latest episode accumulated result": "Null",
        "latest episode diagnosis date reason": "SSPI update - patient deceased",
        "latest episode has diagnosis date": "No",
        "latest episode includes event code": "E63 Reopen episode for correction",
        "latest episode recall calculation method": "S92 Interrupt Close Date",
        "latest episode recall episode type": "Null",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Open",
        "latest episode status reason": "Null",
        "latest event status": "J10 Attended Colonoscopy Assessment Appointment",
        "lynch due date": "Null",
        "lynch due date date of change": "Unchanged",
        "lynch due date reason": "unchanged",
        "screening due date": "Calculated FOBT due date",
        "screening due date date of change": "Today",
        "screening due date reason": "Reopened episode",
        "screening status": "Unchanged",
        "screening status date of change": "Unchanged",
        "screening status reason": "Unchanged",
        "surveillance due date date of change": "Unchanged",
        "surveillance due date reason": "unchanged",
        "surveillance due date": "Null",
    }
    subject_assertion(nhs_no, criteria)

    # When I switch users to BCSS "England" as user role "Hub Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    # And I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the advance episode options
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # And I select the interrupt episode option for "Amend Diagnosis Date"
    AdvanceFOBTScreeningEpisodePage(page).click_amend_diagnosis_date_button()

    # And I enter a Diagnosis Date of "today"
    # And I select Diagnosis Date Reason "Incorrect information previously entered"
    # And I save Diagnosis Date Information
    PatientAdvisedOfDiagnosisPage(page).select_diagnosis_date_and_reason(
        datetime.today(), "Incorrect information previously entered"
    )

    # When I process the open "A183 - GP Result (Abnormal)" letter batch for my subject
    batch_processing(
        page,
        "A183",
        "GP Result (Abnormal)",
        "J10 - Attended Colonoscopy Assessment Appointment",
    )

    # Then my subject has been updated as follows:
    criteria = {
        "latest episode includes event status": "A167 GP Abnormal FOBT Result Sent",
        "latest event status": "J10 Attended Colonoscopy Assessment Appointment",
    }
    subject_assertion(nhs_no, criteria)

    # When I switch users to BCSS "England" as user role "Screening Centre Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Screening Centre Manager at BCS001")

    # And I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the advance episode options
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # And I select Subsequent Assessment Appointment Required reason "Previous attendance, further assessment required"
    AdvanceFOBTScreeningEpisodePage(
        page
    ).click_and_select_subsequent_assessment_appointment_required(
        "Previous attendance, further assessment required"
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no, {"latest event status": "J1 Subsequent Assessment Appointment Required"}
    )

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
    subject_assertion(
        nhs_no,
        {
            "latest event status": "J34 Subsequent Appointment Requested",
        },
    )

    # And there is a "J34" letter batch for my subject with the exact title "Practitioner Clinic 1st Subsequent Appointment"
    # When I process the open "J34" letter batch for my subject
    batch_processing(
        page,
        "J34",
        "Practitioner Clinic 1st Subsequent Appointment",
        "J35 - Subsequent Appointment Booked, letter sent",
    )

    # When I view the event history for the subject's latest episode
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    SubjectScreeningSummaryPage(page).expand_episodes_list()
    SubjectScreeningSummaryPage(page).click_first_fobt_episode_link()

    # And I view the latest practitioner appointment in the subject's episode
    EpisodeEventsAndNotesPage(page).click_most_recent_view_appointment_link()

    # And I attend the subject's practitioner appointment "today"
    AppointmentDetailPage(page).mark_appointment_as_attended(datetime.today())

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "J10 Attended Colonoscopy Assessment Appointment",
        },
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I edit the Colonoscopy Assessment Dataset for this subject
    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_colonoscopy_show_datasets()

    # And I update the Colonoscopy Assessment Dataset with the following values:
    ColonoscopyDatasetsPage(page).select_fit_for_colonoscopy_option(
        FitForColonoscopySspOptions.NO
    )
    ColonoscopyDatasetsPage(page).click_dataset_complete_radio_button_yes()
    ColonoscopyDatasetsPage(page).save_dataset()

    # And I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I advance the subject's episode for "Not Suitable for Diagnostic Tests"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(
        page
    ).click_not_suitable_for_diagnostic_tests_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no, {"latest event status": "J15 Not Suitable for Diagnostic Tests"}
    )

    # And there is a "J15" letter batch for my subject with the exact title "Subject Discharge (Unsuitable For Further Diagnostic Tests)"
    # When I process the open "J15" letter batch for my subject
    batch_processing(
        page,
        "J15",
        "Subject Discharge (Unsuitable For Further Diagnostic Tests)",
        "J16 - Patient Discharge Sent (Unsuitable for Diagnostic Tests)",
    )

    # When I switch users to BCSS "England" as user role "Hub Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    # And there is a "J16" letter batch for my subject with the exact title "GP Discharge (Not Suitable For Diagnostic Tests)"
    # And I process the open "J16" letter batch for my subject

    batch_processing(
        page,
        "J16",
        "GP Discharge (Not Suitable For Diagnostic Tests)",
        "J17 - GP Discharge Sent (Unsuitable for Diagnostic Tests)",
    )

    # Then my subject has been updated as follows:
    criteria = {
        "calculated fobt due date": "2 years from latest J16 event",
        "calculated lynch due date": "Unchanged",
        "calculated surveillance due date": "Unchanged",
        "ceased confirmation date": "Null",
        "ceased confirmation details": "Null",
        "ceased confirmation user id": "Null",
        "clinical reason for cease": "Null",
        "latest episode accumulated result": "Definitive abnormal FOBT outcome",
        "latest episode recall calculation method": "Date of last patient letter",
        "latest episode recall episode type": "FOBT Screening",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Closed",
        "latest episode status reason": "Clinical Reason",
        "latest event status": "J17 GP Discharge Sent (Unsuitable for Diagnostic Tests)",
        "lynch due date": "Null",
        "lynch due date date of change": "Unchanged",
        "lynch due date reason": "unchanged",
        "screening due date": "Calculated FOBT due date",
        "screening due date date of change": "Today",
        "screening due date reason": "Recall",
        "screening status": "Recall",
        "screening status date of change": "Today",
        "screening status reason": "Recall",
        "surveillance due date date of change": "Unchanged",
        "surveillance due date reason": "unchanged",
        "surveillance due date": "Null",
    }
    subject_assertion(nhs_no, criteria)
    LogoutPage(page).log_out()
