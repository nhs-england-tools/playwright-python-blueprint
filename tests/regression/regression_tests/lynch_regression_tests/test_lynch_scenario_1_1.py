import logging
import pytest
from datetime import datetime
from playwright.sync_api import Page
from classes.repositories.general_repository import GeneralRepository
from pages.base_page import BasePage
from pages.logout.log_out_page import LogoutPage
from pages.screening_practitioner_appointments.appointment_detail_page import (
    AppointmentDetailPage,
    ReasonForCancellationOptions,
)
from pages.screening_subject_search.advance_lynch_surveillance_episode_page import (
    AdvanceLynchSurveillanceEpisodePage,
)
from pages.screening_subject_search.episode_events_and_notes_page import (
    EpisodeEventsAndNotesPage,
)
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from utils import screening_subject_page_searcher
from utils.appointments import AppointmentAttendance, book_appointments
from utils.batch_processing import batch_processing
from utils.lynch_utils import LynchUtils
from utils.oracle.oracle import OracleDB
from utils.subject_assertion import subject_assertion
from utils.user_tools import UserTools


@pytest.mark.usefixtures("setup_org_and_appointments")
@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.lynch_regression_tests
def test_lynch_scenario_1_1(page: Page) -> None:
    """
    Scenario: 1.1 - Patient refuses colonoscopy assessment appointment - self referral

    G4-G2-G3-A183-A25-J10-J1-J34-J35-J36-J27-J37-J38-J14-J22-J8-J9-C203 over age range [SSCL5b(J9)]

    This scenario tests where a subject attends a colonoscopy assessment appointment, but is then referred for a subsequent assessment appointment which does not take place because the subject first DNAs the appointment then cancels to consider.  As the subject then does not book a new appointment within the time limit so is deemed to have refused the assessment and the episode is closed.

    Subject summary:

    > Process Lynch diagnosis for a new over-age subject suitable for immediate self-referral
    > Self refer the subject
    > Run Lynch invitations > G4 (5.1)
    > Process G4 letter batch > G2 (5.1)
    > Run timed events > G3 (5.1)
    > Book appointment > A183 (1.11)
    > Process A183 letter batch > A25 (1.11)
    > Attend appointment > J10 (1.11)
    > Advance for "Subsequent Assessment Appointment Required" > J1 (1.11)
    > Book appointment > J34 (1.11)
    > Process J34 letter batch > J35 (1.11)
    > Subject DNA > J36 (1.11)
    > Process J36 letter batch > J27 (1.11)
    > Book appointment > J37 (1.11)
    > Process J37 letter batch > J38 (1.11)
    > Patient cancels to consider > J14 (1.11)
    > Process J14 letter batch > J22 (1.11)
    > Run timed events > J22 (1.11)
    > Process J22 letter batch > J8 (1.11)
    > Process J8 letter batch > J9 (1.11) > C203 (1.13)
    > Check recall [SSCL5b(J9)]
    """
    # Given I log in to BCSS "England" as user role "Hub Manager"
    user_role = UserTools.user_login(
        page, "Hub Manager State Registered at BCS01", return_role_type=True
    )
    if user_role is None:
        raise ValueError("User cannot be assigned to a UserRoleType")

    # When I receive Lynch diagnosis "EPCAM" for a new subject in my hub aged "75" with diagnosis date "3 years ago" and last colonoscopy date "2 years ago"
    nhs_no = LynchUtils(page).insert_validated_lynch_patient_from_new_subject_with_age(
        age="75",
        gene="EPCAM",
        when_diagnosis_took_place="3 years ago",
        when_last_colonoscopy_took_place="2 years ago",
        user_role=user_role,
    )

    # Then Comment: NHS number
    assert nhs_no is not None
    logging.info(f"[SUBJECT CREATION] Created Lynch subject with NHS number: {nhs_no}")

    # When I self refer the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    SubjectScreeningSummaryPage(page).click_self_refer_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "Calculated FOBT due date": "Null",
            "Calculated lynch due date": "Today",
            "Calculated surveillance due date": "Null",
            "Lynch due date": "Today",
            "Lynch due date date of change": "Null",
            "Lynch due date reason": "Self-referral",
            "Previous screening status": "Lynch Surveillance",
            "Screening due date": "Null",
            "Screening due date date of change": "Null",
            "Screening due date reason": "Null",
            "Subject has lynch diagnosis": "Yes",
            "Subject lower FOBT age": "Default",
            "Subject lower lynch age": "25",
            "Screening status": "Lynch Self-referral",
            "Screening status date of change": "Today",
            "Screening status reason": "Self-referral",
            "Subject age": "75",
            "Surveillance due date": "Null",
            "Surveillance due date date of change": "Null",
            "Surveillance due date reason": "Null",
        },
    )

    # When I set the Lynch invitation rate for all screening centres to 50
    LynchUtils(page).set_lynch_invitation_rate(rate=50)

    # And I run the Lynch invitations process
    GeneralRepository().run_lynch_invitations()

    # And my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest episode type": "Lynch Surveillance",
            "latest episode sub-type": "Over Age",
            "latest event status": "G4 Selected for Lynch Surveillance (Self-referral)",
            "calculated fobt due date": "Null",
            "calculated lynch due date": "Today",
            "calculated surveillance due date": "Null",
            "lynch due date": "Today",
            "lynch due date date of change": "Null",
            "lynch due date reason": "Self-referral",
            "previous screening status": "Lynch Surveillance",
            "screening due date": "Null",
            "screening due date date of change": "Null",
            "screening due date reason": "Null",
            "subject has lynch diagnosis": "Yes",
            "subject lower fobt age": "Default",
            "subject lower lynch age": "25",
            "screening status": "Lynch Self-referral",
            "screening status date of change": "Today",
            "screening status reason": "Self-referral",
            "subject age": "75",
            "surveillance due date": "Null",
            "surveillance due date date of change": "Null",
            "surveillance due date reason": "Null",
        },
    )

    # And there is a "G4" letter batch for my subject with the exact title "Lynch Surveillance Invitation (Self-referral)"
    # When I process the open "G4" letter batch for my subject
    batch_processing(
        page,
        "G4",
        "Lynch Surveillance Invitation (Self-referral)",
    )

    # Then my subject has been updated as follows:
    subject_assertion(nhs_no, {"latest event status": "G2 Lynch Pre-invitation Sent"})

    # When I run Timed Events for my subject
    OracleDB().exec_bcss_timed_events(nhs_number=nhs_no)

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "G3 Lynch Surveillance Colonoscopy Assessment Appointment Required"
        },
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the practitioner appointment booking screen
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

    # And there is a "A183" letter batch for my subject with the exact title "Practitioner Clinic 1st Appointment (Lynch)"
    # When I process the open "A183" letter batch for my subject
    batch_processing(page, "A183", "Practitioner Clinic 1st Appointment (Lynch)")

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A25 1st Colonoscopy Assessment Appointment Booked, letter sent",
        },
    )

    # When I switch users to BCSS "England" as user role "Screening Centre Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    user_role = UserTools.user_login(page, "Screening Centre Manager at BCS001", True)
    if user_role is None:
        raise ValueError("User cannot be assigned to a UserRoleType")

    # And I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the event history for the subject's latest episode
    SubjectScreeningSummaryPage(page).expand_episodes_list()
    SubjectScreeningSummaryPage(page).click_first_lynch_surveillance_episode_link()

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

    # And I view the advance episode options
    SubjectScreeningSummaryPage(page).click_advance_lynch_surveillance_episode_button()

    # And I select Subsequent Assessment Appointment Required reason "SC interpreter DNA"
    # And I advance the subject's episode for "Subsequent Assessment Appointment Required"
    AdvanceLynchSurveillanceEpisodePage(
        page
    ).click_and_select_subsequent_assessment_appointment_required("SC interpreter DNA")

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "J1 Subsequent Assessment Appointment Required",
        },
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the practitioner appointment booking screen
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

    # And there is a "J34" letter batch for my subject with the exact title "Practitioner Clinic 1st Subsequent Appointment (Lynch)"
    # When I process the open "J34" letter batch for my subject
    batch_processing(
        page,
        "J34",
        "Practitioner Clinic 1st Subsequent Appointment (Lynch)",
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "J35 Subsequent Appointment Booked, letter sent",
        },
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the event history for the subject's latest episode
    # And I view the latest practitioner appointment in the subject's episode
    # And The subject DNAs the practitioner appointment
    AppointmentAttendance(page).mark_as_dna("Patient did not attend")

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "J36 Subsequent Appointment Non-attendance (Patient)",
        },
    )

    # And there is a "J36" letter batch for my subject with the exact title "Practitioner Clinic 1st Subsequent Appointment Non Attendance (Patient) (Lynch)"
    # When I process the open "J36" letter batch for my subject
    batch_processing(
        page,
        "J36",
        "Practitioner Clinic 1st Subsequent Appointment Non Attendance (Patient) (Lynch)",
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "J27 Appointment Non-attendance Letter Sent (Patient)",
        },
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the practitioner appointment booking screen
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
            "latest event status": "J37 Subsequent Appointment Requested following a DNA",
        },
    )

    # And there is a "J37" letter batch for my subject with the exact title "Practitioner Clinic 2nd Subsequent Appointment (Lynch)"
    # When I process the open "J37" letter batch for my subject
    batch_processing(
        page,
        "J37",
        "Practitioner Clinic 2nd Subsequent Appointment (Lynch)",
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "J38 Subsequent Appointment Booked, letter sent following a DNA",
        },
    )

    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the event history for the subject's latest episode
    SubjectScreeningSummaryPage(page).expand_episodes_list()
    SubjectScreeningSummaryPage(page).click_first_lynch_surveillance_episode_link()

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
            "latest event status": "J14 Appointment Cancelled following a DNA (Patient to Consider)",
        },
    )

    # And there is a "J14" letter batch for my subject with the exact title "Practitioner Clinic 2nd Appt Cancelled (Patient To Consider) (Lynch)"
    # When I process the open "J14" letter batch for my subject
    batch_processing(
        page,
        "J14",
        "Practitioner Clinic 2nd Appt Cancelled (Patient To Consider) (Lynch)",
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "J23 Appointment Cancellation letter sent following a DNA (Patient to Consider)",
        },
    )

    # When I run Timed Events for my subject
    OracleDB().exec_bcss_timed_events(nhs_number=nhs_no)

    # Then there is a "J23" letter batch for my subject with the exact title "Subject Discharge (Refused Appointment) (Lynch)"
    # When I process the open "J23" letter batch for my subject
    batch_processing(
        page,
        "J23",
        "Subject Discharge (Refused Appointment) (Lynch)",
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "J8 Patient discharge sent (refused colonoscopy assessment appointment)",
        },
    )

    logging.info("Check subject details against closure scenario SSCL5b (J9)")

    # When I switch users to BCSS "England" as user role "Hub Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    user_role = UserTools.user_login(
        page, "Hub Manager State Registered at BCS01", True
    )
    if user_role is None:
        raise ValueError("User cannot be assigned to a UserRoleType")

    # And there is a "J8" letter batch for my subject with the exact title "GP Discharge (Refusal of Practitioner Clinic Appointment) (Lynch)"
    # When I process the open "J8" letter batch for my subject
    batch_processing(
        page,
        "J8",
        "GP Discharge (Refusal of Practitioner Clinic Appointment) (Lynch)",
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "Calculated FOBT due date": "Null",
            "Calculated lynch due date": "2 years from latest J8 event",
            "Calculated surveillance due date": "Null",
            "Ceased confirmation date": "Today",
            "Ceased confirmation details": "Outside screening population at recall.",
            "Ceased confirmation user ID": "User's ID",
            "Clinical reason for cease": "Null",
            "Latest episode accumulated result": "Lynch non-participation",
            "Latest episode recall calculation method": "Date of last patient letter",
            "Latest episode recall episode type": "Lynch Surveillance",
            "Latest episode recall surveillance type": "Null",
            "Latest episode status": "Closed",
            "Latest episode status reason": "Informed Dissent",
            "Latest event status": "J9 GP discharge letter sent (refusal of colonoscopy assessment appointment)",
            "Lynch due date": "Null",
            "Lynch due date date of change": "Today",
            "Lynch due date reason": "Ceased",
            "Lynch incident episode": "Null",
            "Screening due date": "Null",
            "Screening due date date of change": "Null",
            "Screening due date reason": "Null",
            "Screening status": "Ceased",
            "Screening status date of change": "Today",
            "Screening status reason": "Outside Screening Population",
            "Surveillance due date": "Null",
            "Surveillance due date date of change": "Unchanged",
            "Surveillance due date reason": "Unchanged",
        },
        user_role,
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # Then I "can" see a button with value of "Self-refer Lynch Surveillance"
    SubjectScreeningSummaryPage(page).button_with_value_present(
        "Self-refer Lynch Surveillance", True
    )

    LogoutPage(page).log_out()
