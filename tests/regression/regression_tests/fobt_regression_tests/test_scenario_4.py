import pytest
import logging
from datetime import datetime
from playwright.sync_api import Page
from utils.oracle.subject_creation_util import CreateSubjectSteps
from utils.sspi_change_steps import SSPIChangeSteps
from utils.user_tools import UserTools
from utils.subject_assertion import subject_assertion
from utils.call_and_recall_utils import CallAndRecallUtils
from utils import screening_subject_page_searcher
from utils.batch_processing import batch_processing
from utils.fit_kit import FitKitLogged, FitKitGeneration
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from pages.screening_subject_search.close_fobt_screening_episode_page import (
    CloseFobtScreeningEpisodePage,
)
from utils.appointments import book_appointments
from pages.logout.log_out_page import LogoutPage
from pages.base_page import BasePage
from pages.screening_subject_search.episode_events_and_notes_page import (
    EpisodeEventsAndNotesPage,
)
from pages.screening_practitioner_appointments.appointment_detail_page import (
    AppointmentDetailPage,
    ReasonForCancellationOptions,
)
from pages.screening_subject_search.advance_fobt_screening_episode_page import (
    AdvanceFOBTScreeningEpisodePage,
)
from pages.screening_subject_search.record_diagnosis_date_page import (
    RecordDiagnosisDatePage,
)


@pytest.mark.usefixtures("setup_org_and_appointments")
@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.fobt_regression_tests
def test_scenario_4(page: Page) -> None:
    """
    Scenario: 4: Screening Centre discharges patient prior to colonoscopy assessment

    S1-S9-S10-S43-A8-S92-C203 [SSCL35b] A8-A183-A25-(A167)-J4-J22-J20-A25-J24-J25-J26-P202-J26-C203 [SSCL6a(J26)]

    This scenario tests where the screening centre discharges the patient before the colonoscopy assessment appointment takes place. It also tests a mid-episode manual close and reopen, and the diagnosis date spur event.

    Scenario summary:

    > Create a new subject in the FOBT age range > Inactive
    > Run the FOBT failsafe trawl > Call
    > Run the database transition to invite them for FOBT screening > S1(1.1)
    > Process S1 letter batch > S9 (1.1)
    > SSPI update changes subject to below-age
    > Run timed events > creates S9 letter (1.1)
    > Process S9 letter batch > S10 (1.1)
    > Log kit > S43 (1.2)
    > Read kit with ABNORMAL result > A8 (1.3)
    > Manually close episode on interrupt > S92 > C203
    > Check recall [SSCL35b]
    > Reopen episode for correction > A8 (1.3)
    > Invite for colonoscopy assessment > A183 (1.11)
    > Process A183 appointment letter > A25 (1.11)
    > Process A183 result letter (A167) (1.11)
    > Patient cancels to consider > J4 (1.11)
    > Process J4 letter batch > J22 (1.11)
    > Rebook colonoscopy assessment > J20 (1.11)
    > Process J20 letter batch > A25 (1.11)
    > SC cancels appointment “Patient unsuitable – recently screened” > J24 (1.11)
    > Process J24 letter batch > J25 (1.11)
    > Process J25 letter batch > J26 (1.11) > P202
    > Record diagnosis date reason (A52) > J26 (1.11) > C203 (1.13)
    > Check recall [SSCL6a(J26)]
    """

    summary_page = SubjectScreeningSummaryPage(page)
    logging.info(
        "[TEST START] Regression - Scenario: 4: Screening Centre discharges patient prior to colonoscopy assessment"
    )

    # Given I log in to BCSS "England" as user role "Hub Manager"
    user_role = UserTools.user_login(
        page, "Hub Manager State Registered at BCS01", return_role_type=True
    )
    if user_role is None:
        raise ValueError("User cannot be assigned to a UserRoleType")

    # And I create a subject that meets the following criteria:
    requirements = {
        "age (y/d)": "62/45",
        "active gp practice in hub/sc": "BCS01/BCS001",
    }
    nhs_no = CreateSubjectSteps().create_custom_subject(requirements)
    if nhs_no is None:
        pytest.fail("Failed to create subject: NHS number not returned.")

    # Then Comment: NHS number
    logging.info(f"[SUBJECT CREATED] NHS number: {nhs_no}")

    # And my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "subject age": "62",
            "subject has episodes": "No",
            "screening status": "Inactive",
        },
    )
    # Assert subject details in the UI
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    summary_page.assert_subject_age(62)
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

    # Assert subject details in the UI
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
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
    # Then my subject has been updated as follows:
    batch_processing(
        page,
        "S1",
        "Pre-invitation (FIT)",
        "S9 - Pre-invitation Sent",
        True,
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I receive an SSPI update to change their date of birth to "45" years old
    SSPIChangeSteps().sspi_update_to_change_dob_received(nhs_no, 45)

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
    subject_assertion(
        nhs_no,
        {
            "latest event status": "S43 Kit Returned and Logged (Initial Test)",
        },
    )

    # # When I read my subject's latest logged FIT kit as "ABNORMAL"
    FitKitLogged().read_latest_logged_kit(user_role, 2, fit_kit, "ABNORMAL")

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A8 Abnormal",
        },
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I close the subject's episode for "Opt out of current episode"
    CloseFobtScreeningEpisodePage(page).close_fobt_screening_episode(
        "Opt out of current episode"
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "calculated FOBT due date": "2 years from episode end",
            "calculated lynch due date": "Null",
            "calculated surveillance due date": "Null",
            "ceased confirmation date": "Null",
            "ceased confirmation details": "Null",
            "ceased confirmation user ID": "Null",
            "clinical reason for cease": "Null",
            "latest episode accumulated result": "Definitive abnormal FOBT outcome",
            "latest episode recall calculation method": "S92 Interrupt Close Date",
            "latest episode recall episode type": "FOBT Screening",
            "latest episode recall surveillance type": "Null",
            "latest episode status": "Closed",
            "latest episode status reason": "Opt out of current episode",
            "latest event status": "S92 Close Screening Episode via Interrupt",
            "lynch due date": "Null",
            "lynch due date date of change": "Unchanged",
            "lynch due date reason": "Unchanged",
            "screening due date": "Null",
            "screening due date date of change": "Today",
            "screening due date reason": "Awaiting failsafe",
            "screening status": "Recall",
            "screening status reason": "Recall",
            "surveillance due date": "Null",
            "surveillance due date date of change": "Unchanged",
            "surveillance due date reason": "Unchanged",
        },
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I reopen the subject's episode for "Reopen episode for correction"
    SubjectScreeningSummaryPage(page).reopen_fobt_screening_episode()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "calculated FOBT due date": "As at episode start",
            "calculated lynch due date": "Null",
            "calculated surveillance due date": "Null",
            "ceased confirmation date": "Null",
            "ceased confirmation details": "Null",
            "ceased confirmation user ID": "Null",
            "clinical reason for cease": "Null",
            "latest episode accumulated result": "Null",
            "latest episode includes event code": "E63 Reopen episode for correction",
            "latest episode recall calculation method": "S92 Interrupt Close Date",
            "latest episode recall episode type": "Null",
            "latest episode recall surveillance type": "Null",
            "latest episode status": "Open",
            "latest episode status reason": "Null",
            "latest event status": "A8 Abnormal",
            "lynch due date": "Null",
            "lynch due date date of change": "Unchanged",
            "lynch due date reason": "Unchanged",
            "screening due date": "Calculated FOBT due date",
            "screening due date date of change": "Today",
            "screening due date reason": "Reopened episode",
            "surveillance due date": "Null",
            "surveillance due date date of change": "Unchanged",
            "surveillance due date reason": "Unchanged",
        },
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I choose to book a practitioner clinic for my subject
    SubjectScreeningSummaryPage(page).click_book_practitioner_clinic_button()

    # And I select "BCS001" as the screening centre where the practitioner appointment will be held
    # And I set the practitioner appointment date to "tomorrow"
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

    # And there is a "A183" letter batch for my subject with the exact title "GP Result (Abnormal)"
    # When I process the open "A183 - GP Result (Abnormal)" letter batch for my subject
    # Then my subject has been updated as follows:
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
    SubjectScreeningSummaryPage(page).expand_episodes_list()
    SubjectScreeningSummaryPage(page).click_first_fobt_episode_link()

    # And I view the latest practitioner appointment in the subject's episode
    EpisodeEventsAndNotesPage(page).click_most_recent_view_appointment_link()

    # And the subject cancels the practitioner appointment with reason "Patient Cancelled to Consider"
    AppointmentDetailPage(page).check_cancel_radio()
    AppointmentDetailPage(page).select_reason_for_cancellation_option(
        ReasonForCancellationOptions.PATIENT_CANCELLED_TO_CONSIDER
    )

    # And I press OK on my confirmation prompt
    AppointmentDetailPage(page).click_save_button(accept_dialog=True)

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "J4 Appointment Cancellation (Patient to Consider)",
        },
    )

    # When I process the open "J4" letter batch for my subject
    # # Then my subject has been updated as follows:
    batch_processing(
        page,
        "J4",
        "Practitioner Clinic 1st Appt Cancelled (Patient To Consider)",
        "J22 - Appointment Cancellation letter sent (Patient to Consider)",
        True,
    )

    # When I switch users to BCSS "England" as user role "Hub Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    # And I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I choose to book a practitioner clinic for my subject
    SubjectScreeningSummaryPage(page).click_book_practitioner_clinic_button()

    # And I select "BCS001" as the screening centre where the practitioner appointment will be held
    # And I set the practitioner appointment date to "tomorrow"
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
            "latest event status": "J20 Appointment Requested (Patient to Reschedule Letter)",
        },
    )

    # And there is a "J20" letter batch for my subject with the exact title "Practitioner Clinic 1st Appt Cancelled (Patient To Reschedule)"
    # When I process the open "J20" letter batch for my subject
    # Then my subject has been updated as follows:
    batch_processing(
        page,
        "J20",
        "Practitioner Clinic 1st Appt Cancelled (Patient To Reschedule)",
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

    # And the subject cancels the practitioner appointment with reason "Patient Unsuitable - Recently Screened"
    AppointmentDetailPage(page).check_cancel_radio()
    AppointmentDetailPage(page).select_reason_for_cancellation_option(
        ReasonForCancellationOptions.PATIENT_UNSUITABLE_RECENTLY_SCREENED
    )

    # And I press OK on my confirmation prompt
    AppointmentDetailPage(page).click_save_button(accept_dialog=True)

    # Then my subject has been updated as follows:
    # And there is a "J24" letter batch for my subject with the exact title "Subject Discharge (Screening Centre)"
    # When I process the open "J24 - Subject Discharge (Screening Centre)" letter batch for my subject
    # Then my subject has been updated as follows:
    batch_processing(
        page,
        "J24",
        "Subject Discharge (Screening Centre)",
        "J25 - Patient discharge sent (Screening Centre discharge patient)",
    )

    # When I switch users to BCSS "England" as user role "Hub Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    # And there is a "J25" letter batch for my subject with the exact title "GP Discharge (Discharged By Screening Centre)"
    # And I process the open "J25" letter batch for my subject
    # Then my subject has been updated as follows:
    batch_processing(
        page,
        "J25",
        "GP Discharge (Discharged By Screening Centre)",
        "P202 - Waiting Completion of Outstanding Events",
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the advance episode options
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # And I select the advance episode option for "Record Diagnosis Date"
    AdvanceFOBTScreeningEpisodePage(page).click_record_diagnosis_date_button()

    # And I select Diagnosis Date Reason "Patient choice"
    RecordDiagnosisDatePage(page).record_diagnosis_reason(reason_text="Patient choice")

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "calculated FOBT due date": "2 years from latest J25 event",
            "calculated lynch due date": "Unchanged",
            "calculated surveillance due date": "Unchanged",
            "ceased confirmation date": "Null",
            "ceased confirmation details": "Null",
            "ceased confirmation user ID": "Null",
            "clinical reason for cease": "Null",
            "latest episode accumulated result": "Definitive abnormal FOBT outcome",
            "latest episode diagnosis date reason": "Patient choice",
            "latest episode has diagnosis date": "No",
            "latest episode includes event status": "A52 No diagnosis date recorded",
            "latest episode recall calculation method": "Date of last patient letter",
            "latest episode recall episode type": "FOBT Screening",
            "latest episode recall surveillance type": "Null",
            "latest episode status": "Closed",
            "latest episode status reason": "Discharged",
            "latest event status": "J26 GP Discharge letter sent (Discharge by Screening centre)",
            "lynch due date": "Null",
            "lynch due date date of change": "Unchanged",
            "lynch due date reason": "Unchanged",
            "screening due date": "Null",
            "screening due date date of change": "Today",
            "screening due date reason": "Awaiting failsafe",
            "screening status": "Recall",
            "screening status reason": "Recall",
            "surveillance due date": "Null",
            "surveillance due date reason": "Unchanged",
            "surveillance due date date of change": "Unchanged",
        },
    )

    logging.info("[TEST COMPLETE] Scenario 4 passed all assertions")
    LogoutPage(page).log_out()
