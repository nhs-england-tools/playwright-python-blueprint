from datetime import datetime
import logging
import pytest
from playwright.sync_api import Page
from classes.repositories.general_repository import GeneralRepository
from pages.base_page import BasePage
from pages.datasets.colonoscopy_dataset_page import (
    ColonoscopyDatasetsPage,
    FitForColonoscopySspOptions,
)
from pages.datasets.subject_datasets_page import SubjectDatasetsPage
from pages.logout.log_out_page import LogoutPage

from pages.screening_practitioner_appointments.appointment_detail_page import AppointmentDetailPage
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
def test_lynch_scenario_4_1(page: Page) -> None:
    """
    Scenario: 4.1 - Non-agreement for diagnostic tests - self referral

    G4-G2-G3-A183-A25-J28-J30-A25-J10-A99-A165-A38-A168-C203 above age range [SSCL8c]

    This scenario tests where a subject is suitable but refuses to have a diagnostic test.  There are two routes to this closure; this scenario tests where the subject makes an immediate decision not to proceed.

    Subject summary:

    > Process Lynch diagnosis for a new over-age subject suitable for immediate invitation
    > Self refer the subject
    > Run Lynch invitations > G4 (5.1)
    > Process G4 letter batch > G2 (5.1)
    > Run timed events > G3 (5.1)
    > Book appointment > A183 (1.11)
    > Process A183 letter batch > A25 (1.11)
    > Screening Centre DNA > J28 (1.11)
    > Book appointment > J30 (1.11)
    > Process J30 letter batch > A25 (1.11)
    > Attend appointment > J10 (1.11)
    > Suitable for Endoscopic Test > A99 (1.12)
    > Waiting Decision to Proceed with Diagnostic Test > A165 (1.12)
    > Decision not to Continue with Diagnostic Test > A38 (1.12)
    > Process A38 letter batch > A168 (1.12)
    > Check recall [SSCL8c]
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

    # When Comment:
    logging.info("Progress the episode through the required pathway")

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
    # And I view the latest practitioner appointment in the subject's episode
    # And The Screening Centre DNAs the practitioner appointment
    AppointmentAttendance(page).mark_as_dna("Screening Centre did not attend")

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "J28 Appointment Non-attendance (Screening Centre)",
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
            "latest event status": "J30 Appointment Requested (SC Non-attendance Letter)",
        },
    )

    # And there is a "J30" letter batch for my subject with the exact title "Practitioner Clinic 1st Appointment Non Attendance (Screening Centre) (Lynch)"
    # When I process the open "J30" letter batch for my subject
    batch_processing(
        page,
        "J30",
        "Practitioner Clinic 1st Appointment Non Attendance (Screening Centre) (Lynch)",
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A25 1st Colonoscopy Assessment Appointment Booked, letter sent",
        },
    )

    # When I view the subject
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

    # And I edit the Colonoscopy Assessment Dataset for this subject
    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_colonoscopy_show_datasets()

    # And I update the Colonoscopy Assessment Dataset with the following values:
    ColonoscopyDatasetsPage(page).select_fit_for_colonoscopy_option(
        FitForColonoscopySspOptions.YES
    )
    ColonoscopyDatasetsPage(page).click_dataset_complete_radio_button_yes()

    # And I save the Colonoscopy Assessment Dataset
    ColonoscopyDatasetsPage(page).save_dataset()

    # And I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I advance the subject's episode for "Suitable for Endoscopic Test"
    SubjectScreeningSummaryPage(page).click_advance_lynch_surveillance_episode_button()
    AdvanceLynchSurveillanceEpisodePage(
        page
    ).click_suitable_for_endoscopic_test_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A99 Suitable for Endoscopic Test",
        },
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I advance the subject's episode for "Waiting Decision to Proceed with Diagnostic Test"
    SubjectScreeningSummaryPage(page).click_advance_lynch_surveillance_episode_button()
    AdvanceLynchSurveillanceEpisodePage(
        page
    ).click_waiting_decision_to_proceed_with_diagnostic_test()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A165 Waiting Decision to Proceed with Diagnostic Test",
        },
    )

    # And I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I advance the subject's episode for "Decision not to Continue with Diagnostic Test"
    SubjectScreeningSummaryPage(page).click_advance_lynch_surveillance_episode_button()
    AdvanceLynchSurveillanceEpisodePage(
        page
    ).click_decision_not_to_continue_with_diagnostic_test()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A38 Decision not to Continue with Diagnostic Test",
        },
    )

    # And there is a "A38" letter batch for my subject with the exact title "Discharge (No Agreement To Proceed With Diagnostic Tests) (Lynch) - Patient Letter"
    # When I process the open "A38" letter batch for my subject
    batch_processing(
        page,
        "A38",
        "Discharge (No Agreement To Proceed With Diagnostic Tests) (Lynch) - Patient Letter",
    )

    logging.info("Check subject details against closure scenario SSCL8c")

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "Calculated FOBT due date": "Null",
            "Calculated lynch due date": "2 years from episode end",
            "Calculated surveillance due date": "Null",
            "Ceased confirmation date": "Today",
            "Ceased confirmation details": "Outside screening population at recall.",
            "Ceased confirmation user ID": "User's ID",
            "Clinical reason for cease": "Null",
            "Latest episode accumulated result": "Lynch non-participation",
            "Latest episode recall calculation method": "Episode end date",
            "Latest episode recall episode type": "Lynch Surveillance",
            "Latest episode recall surveillance type": "Null",
            "Latest episode status": "Closed",
            "Latest episode status reason": "Informed Dissent",
            "Latest event status": "A168 GP Discharge Sent (No Agreement to Proceed with Diagnostic Tests)",
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
