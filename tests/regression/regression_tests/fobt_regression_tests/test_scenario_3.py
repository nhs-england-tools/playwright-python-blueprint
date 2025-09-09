import pytest
from playwright.sync_api import Page
from utils.user_tools import UserTools
from utils.oracle.subject_creation_util import CreateSubjectSteps
from utils.subject_assertion import subject_assertion
from utils.call_and_recall_utils import CallAndRecallUtils
import logging
from utils.batch_processing import batch_processing
from utils.fit_kit import FitKitGeneration, FitKitLogged
from utils import screening_subject_page_searcher
from utils.calendar_picker import CalendarPicker
from utils.sspi_change_steps import SSPIChangeSteps
from utils.appointments import book_appointments
from pages.base_page import BasePage
from pages.logout.log_out_page import LogoutPage
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from pages.screening_subject_search.reopen_fobt_screening_episode_page import (
    ReopenFOBTScreeningEpisodePage,
)
from pages.screening_subject_search.advance_fobt_screening_episode_page import (
    AdvanceFOBTScreeningEpisodePage,
)
from pages.screening_practitioner_appointments.book_appointment_page import (
    BookAppointmentPage,
)
from pages.screening_subject_search.record_diagnosis_date_page import (
    RecordDiagnosisDatePage,
)
from pages.screening_subject_search.episode_events_and_notes_page import (
    EpisodeEventsAndNotesPage,
)
from pages.screening_practitioner_appointments.appointment_detail_page import (
    AppointmentDetailPage,
    ReasonForCancellationOptions,
)
from datetime import datetime


@pytest.mark.usefixtures("setup_org_and_appointments")
@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.fobt_regression_tests
def test_scenario_3(page: Page) -> None:
    """
    Scenario: 3: Patient refuses colonoscopy assessment appointment

    S1-S9-S10-S43-A8-A183-(A50)-A25-(A167)-J2-J18-A25-J4-J22-J8-J9-C203 [SSCL4a(J9)] J32-J33-A25-J4-J22-J8-J9-C203 [SSCL5a(J9)]

    This scenario tests where an initial colonoscopy assessment appointment does not take place, because the subject cancels to consider and then does not book a new appointment within the time limit so is deemed to have refused the assessment.

    Scenario summary:

    > Create a new subject in the FOBT age range > Inactive
    > Run the FOBT failsafe trawl > Call
    > Run the database transition to invite them for FOBT screening > S1(1.1)
    > Process S1 letter batch > S9 (1.1)
    > Run timed events > creates S9 letter (1.1)
    > Process S9 letter batch > S10 (1.1)
    > Log kit > S43 (1.2)
    > Read kit with ABNORMAL result > S2 (1.3)
    > Invite for colonoscopy assessment > A183 (1.11)
    > Record diagnosis date (A50)
    > Process A183 appointment letter > A25 (1.11)
    > Process A183 result letter (A167) (1.11)
    > SC cancels > J2 (1.11)
    > Rebook colonoscopy assessment > J18 (1.11)
    > Process J18 letter > A25 (1.11)
    > Patient cancels to consider > J4 (1.11)
    > Process J4 letter batch > J22 (1.11)
    > Run timed events > J22 (1.11)
    > Process J22 letter batch > J8 (1.11)
    > Process J8 letter batch > J9 (1.11) > C203 (1.13)
    > Check recall [SSCL4a(J9)]
    > SSPI update changes subject to over-age
    > Reopen to book an assessment appointment > J32 (1.11)
    > Book colonoscopy assessment > J33 (1.11)
    > Process J33 letter batch > A25 (1.11)
    > Patient cancels to consider > J4 (1.11)
    > Process J4 letter batch > J22 (1.11)
    > Run timed events > J22 (1.11)
    > Process J22 letter batch > J8 (1.11)
    > Process J8 letter batch > J9 (1.11) > C203 (1.13)
    > Check recall [SSCL5a(J9)]
    """
    # Given I log in to BCSS "England" as user role "Hub Manager"
    user_role = UserTools.user_login(
        page, "Hub Manager State Registered at BCS01", return_role_type=True
    )
    if user_role is None:
        raise ValueError("User cannot be assigned to a UserRoleType")

    # And I create a subject that meets the following criteria:
    requirements = {
        "age (y/d)": "67/320",
        "active gp practice in hub/sc": "BCS01/BCS001",
    }
    nhs_no = CreateSubjectSteps().create_custom_subject(requirements)
    if nhs_no is None:
        raise ValueError("NHS No is 'None'")

    # Then Comment: NHS number
    logging.info(f"[SUBJECT CREATION] Created subject's NHS number: {nhs_no}")

    # Then my subject has been updated as follows:
    criteria = {
        "subject age": "67",
        "subject has episodes": "no",
        "screening status": "Inactive",
    }
    subject_assertion(nhs_no, criteria)

    # When I run the FOBT failsafe trawl for my subject
    CallAndRecallUtils().run_failsafe(nhs_no)

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
    criteria = {
        "latest event status": "S43 Kit Returned and Logged (Initial Test)",
    }
    subject_assertion(nhs_no, criteria)

    # When I read my subject's latest logged FIT kit as "ABNORMAL"
    FitKitLogged().read_latest_logged_kit(user_role, 2, fit_kit, "ABNORMAL")

    # Then my subject has been updated as follows:
    criteria = {"latest event status": "A8 Abnormal"}
    subject_assertion(nhs_no, criteria)

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I choose to book a practitioner clinic for my subject
    SubjectScreeningSummaryPage(page).click_book_practitioner_clinic_button()

    # And I select "BCS001" as the screening centre where the practitioner appointment will be held
    # And I book the "earliest" available practitioner appointment on this date
    book_appointments(
        page,
        "BCS001 - Wolverhampton Bowel Cancer Screening Centre",
        "The Royal Hospital (Wolverhampton)",
    )

    # Then my subject has been updated as follows:
    criteria = {
        "latest event status": "A183 1st Colonoscopy Assessment Appointment Requested"
    }
    subject_assertion(nhs_no, criteria)

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the advance episode options
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # And I select the advance episode option for "Record Diagnosis Date"
    AdvanceFOBTScreeningEpisodePage(page).click_record_diagnosis_date_button()

    # And I enter a Diagnosis Date of "today"
    RecordDiagnosisDatePage(page).enter_date_in_diagnosis_date_field(datetime.today())

    # And I save Diagnosis Date Information
    RecordDiagnosisDatePage(page).click_save_button()

    # Then my subject has been updated as follows:
    criteria = {
        "latest episode diagnosis date reason": "Null",
        "latest episode has diagnosis date": "Yes",
        "latest episode includes event status": "A50 Diagnosis date recorded",
        "latest event status": "A183 1st Colonoscopy Assessment Appointment Requested",
    }
    subject_assertion(nhs_no, criteria)

    # When I process the open "A183 - Practitioner Clinic 1st Appointment" letter batch for my subject
    batch_processing(
        page,
        "A183",
        "Practitioner Clinic 1st Appointment",
        "A25 - 1st Colonoscopy Assessment Appointment Booked, letter sent",
    )

    # When I process the open "A183 - GP Result (Abnormal)" letter batch for my subject
    batch_processing(
        page,
        "A183",
        "GP Result (Abnormal)",
        "A25 - 1st Colonoscopy Assessment Appointment Booked, letter sent",
    )

    # Then my subject has been updated as follows:
    SubjectScreeningSummaryPage(page).expand_episodes_list()
    SubjectScreeningSummaryPage(page).click_first_fobt_episode_link()
    EpisodeEventsAndNotesPage(page).expected_episode_event_is_displayed(
        "A167 - GP Abnormal FOBT Result Sent"
    )

    # When I switch users to BCSS "England" as user role "Screening Centre Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Screening Centre Manager at BCS001")

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the event history for the subject's latest episode
    SubjectScreeningSummaryPage(page).expand_episodes_list()
    SubjectScreeningSummaryPage(page).click_first_fobt_episode_link()

    # And I view the latest practitioner appointment in the subject's episode
    EpisodeEventsAndNotesPage(page).click_view_appointment_link()

    # And The Screening Centre cancels the practitioner appointment with reason "Screening Centre Cancelled - Other Reason"
    AppointmentDetailPage(page).check_cancel_radio()
    AppointmentDetailPage(page).select_reason_for_cancellation_option(
        ReasonForCancellationOptions.SCREENING_CENTRE_CANCELLED_OTHER_REASON
    )

    # And I press OK on my confirmation prompt
    AppointmentDetailPage(page).click_save_button(accept_dialog=True)

    # Then my subject has been updated as follows:
    criteria = {"latest event status": "J2 Appointment Cancellation (Screening Centre)"}
    subject_assertion(nhs_no, criteria)

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I choose to book a practitioner clinic for my subject
    SubjectScreeningSummaryPage(page).click_book_practitioner_clinic_button()

    # And I select "BCS001" as the screening centre where the practitioner appointment will be held
    # And I book the "earliest" available practitioner appointment on this date
    book_appointments(
        page,
        "BCS001 - Wolverhampton Bowel Cancer Screening Centre",
        "The Royal Hospital (Wolverhampton)",
    )

    # Then my subject has been updated as follows:
    criteria = {
        "latest event status": "J18 Appointment Requested (Screening Centre Cancellation Letter)"
    }
    subject_assertion(nhs_no, criteria)

    # And there is a "J18" letter batch for my subject with the exact title "Practitioner Clinic 1st Appt Cancelled (Screening Centre)"
    # When I process the open "J18" letter batch for my subject
    batch_processing(
        page,
        "J18",
        "Practitioner Clinic 1st Appt Cancelled (Screening Centre)",
        "A25 - 1st Colonoscopy Assessment Appointment Booked, letter sent",
    )

    cancel_appointment_and_processes_batches(page, nhs_no)

    # When I switch users to BCSS "England" as user role "Hub Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    # And there is a "J8" letter batch for my subject with the exact title "GP Discharge (Refusal of Practitioner Clinic Appointment)"
    # And I process the open "J8" letter batch for my subject
    batch_processing(
        page,
        "J8",
        "GP Discharge (Refusal of Practitioner Clinic Appointment)",
        "J9 - GP discharge letter sent (refusal of colonoscopy assessment appointment)",
    )

    # Then my subject has been updated as follows:
    criteria = {
        "calculated fobt due date": "2 years from latest J8 event",
        "calculated lynch due date": "Null",
        "calculated surveillance due date": "Null",
        "ceased confirmation date": "Null",
        "ceased confirmation details": "Null",
        "ceased confirmation user id": "Null",
        "clinical reason for cease": "Null",
        "latest episode accumulated result": "Definitive abnormal FOBT outcome",
        "latest episode recall calculation method": "Date of last patient letter",
        "latest episode recall episode type": "FOBT Screening",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Closed",
        "latest episode status reason": "Informed Dissent",
        "latest event status": "J9 GP discharge letter sent (refusal of colonoscopy assessment appointment)",
        "lynch due date": "Null",
        "lynch due date date of change": "Unchanged",
        "lynch due date reason": "Unchanged",
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

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I reopen the subject's episode for "Reopen to book an assessment appointment"
    SubjectScreeningSummaryPage(page).click_reopen_fobt_screening_episode_button()
    ReopenFOBTScreeningEpisodePage(page).click_reopen_to_book_an_assessment_button()

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
        "latest episode includes event code": "E204 Reopen to book an assessment appointment",
        "latest episode recall calculation method": "Date of last patient letter",
        "latest episode recall episode type": "Null",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Open",
        "latest episode status reason": "Null",
        "latest event status": "J32 Colonoscopy Assessment Appointment Request (Redirected)",
        "lynch due date": "Null",
        "lynch due date date of change": "Unchanged",
        "lynch due date reason": "Unchanged",
        "screening due date": "Calculated FOBT due date",
        "screening due date date of change": "Today",
        "screening due date reason": "Reopened episode",
        "surveillance due date": "Null",
        "surveillance due date date of change": "Unchanged",
        "surveillance due date reason": "Unchanged",
    }
    subject_assertion(nhs_no, criteria)

    # When I receive an SSPI update to change their date of birth to "75" years old
    SSPIChangeSteps().sspi_update_to_change_dob_received(nhs_no, 75)

    # Then my subject has been updated as follows:
    criteria = {"subject age": "75"}
    subject_assertion(nhs_no, criteria)

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I choose to book a practitioner clinic for my subject
    SubjectScreeningSummaryPage(page).click_book_practitioner_clinic_button()

    # And I select "BCS001" as the screening centre where the practitioner appointment will be held
    # And I book the "earliest" available practitioner appointment on this date
    book_appointments(
        page,
        "BCS001 - Wolverhampton Bowel Cancer Screening Centre",
        "The Royal Hospital (Wolverhampton)",
    )

    # Then my subject has been updated as follows:
    criteria = {
        "latest event status": "J33 Colonoscopy Assessment Appointment Requested (Redirected)"
    }
    subject_assertion(nhs_no, criteria)

    # And there is a "J33" letter batch for my subject with the exact title "Redirected Assessment Appointment"
    # When I process the open "J33" letter batch for my subject
    batch_processing(
        page,
        "J33",
        "Redirected Assessment Appointment",
        "A25 - 1st Colonoscopy Assessment Appointment Booked, letter sent",
    )

    cancel_appointment_and_processes_batches(page, nhs_no)

    # When I switch users to BCSS "England" as user role "Hub Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    user_role = UserTools.user_login(
        page, "Hub Manager State Registered at BCS01", True
    )

    # And there is a "J8" letter batch for my subject with the exact title "GP Discharge (Refusal of Practitioner Clinic Appointment)"
    # And I process the open "J8" letter batch for my subject
    batch_processing(
        page,
        "J8",
        "GP Discharge (Refusal of Practitioner Clinic Appointment)",
        "J9 - GP discharge letter sent (refusal of colonoscopy assessment appointment)",
    )

    # Then my subject has been updated as follows:
    criteria = {
        "calculated fobt due date": "2 years from latest J8 event",
        "calculated lynch due date": "Null",
        "calculated surveillance due date": "Null",
        "ceased confirmation date": "Today",
        "ceased confirmation details": "Outside screening population at recall.",
        "ceased confirmation user id": "User's ID",
        "clinical reason for cease": "Null",
        "latest episode accumulated result": "Definitive abnormal FOBT outcome",
        "latest episode recall calculation method": "Date of last patient letter",
        "latest episode recall episode type": "FOBT Screening",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Closed",
        "latest episode status reason": "Informed Dissent",
        "latest event status": "J9 GP discharge letter sent (refusal of colonoscopy assessment appointment)",
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

    LogoutPage(page).log_out()


def cancel_appointment_and_processes_batches(page: Page, nhs_no: str) -> None:
    """
    This function is used to reduce duplicate code in the test.
    It navigates to the subject summary page and cancels an appointment for the subject.
    Once the appointment is cancelled it processes the relevant batches
    """
    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the event history for the subject's latest episode
    SubjectScreeningSummaryPage(page).expand_episodes_list()
    SubjectScreeningSummaryPage(page).click_first_fobt_episode_link()

    # And I view the latest practitioner appointment in the subject's episode
    EpisodeEventsAndNotesPage(page).click_view_appointment_link()

    # And The subject cancels the practitioner appointment with reason "Patient Cancelled to Consider"
    AppointmentDetailPage(page).check_cancel_radio()
    AppointmentDetailPage(page).select_reason_for_cancellation_option(
        ReasonForCancellationOptions.PATIENT_CANCELLED_TO_CONSIDER
    )

    # And I press OK on my confirmation prompt
    AppointmentDetailPage(page).click_save_button(accept_dialog=True)

    # Then my subject has been updated as follows:
    criteria = {
        "latest event status": "J4 Appointment Cancellation (Patient to Consider)"
    }
    subject_assertion(nhs_no, criteria)

    # And there is a "J4" letter batch for my subject with the exact title "Practitioner Clinic 1st Appt Cancelled (Patient To Consider)"
    # When I process the open "J4" letter batch for my subject
    batch_processing(
        page,
        "J4",
        "Practitioner Clinic 1st Appt Cancelled (Patient To Consider)",
        "J22 - Appointment Cancellation letter sent (Patient to Consider)",
        True,
    )

    # Then there is a "J22" letter batch for my subject with the exact title "Subject Discharge (Refused Appointment)"
    # When I process the open "J22" letter batch for my subject
    batch_processing(
        page,
        "J22",
        "Subject Discharge (Refused Appointment)",
        "J8 - Patient discharge sent (refused colonoscopy assessment appointment)",
    )
