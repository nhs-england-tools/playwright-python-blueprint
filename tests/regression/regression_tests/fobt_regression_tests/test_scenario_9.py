import pytest
import logging
from datetime import datetime, timedelta
from playwright.sync_api import Page
from classes.subject.subject import Subject
from classes.user.user import User
from utils.calendar_picker import CalendarPicker
from utils.user_tools import UserTools
from utils.subject_assertion import subject_assertion
from utils import screening_subject_page_searcher
from utils.batch_processing import batch_processing
from utils.fit_kit import FitKitLogged, FitKitGeneration
from utils.oracle.subject_selection_query_builder import SubjectSelectionQueryBuilder
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from utils.appointments import book_appointments
from utils.oracle.oracle import OracleDB
from pages.logout.log_out_page import LogoutPage
from pages.base_page import BasePage
from pages.screening_subject_search.episode_events_and_notes_page import (
    EpisodeEventsAndNotesPage,
)
from pages.screening_practitioner_appointments.appointment_detail_page import (
    AppointmentDetailPage,
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
from pages.screening_subject_search.contact_with_patient_page import (
    ContactWithPatientPage,
)


@pytest.mark.usefixtures("setup_org_and_appointments")
@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.fobt_regression_tests
def test_scenario_9(page: Page) -> None:
    """
    Scenario: 9: Discharge in-age FOBT subject for patient choice, cancelled diagnostic test so "No result"

    S9-S10-S43-A8-A183-A25-J10-(A167)-A99-A59-A306-A396-(A52)-A392-A350-C203 [SSCL13a(A350)]

    This scenario tests where the subject is invited for a diagnostic test, but cancels the test (giving an episode result of "No result") and decides not to continue.

    Scenario summary:

    > Find an in-age subject at S9 whose episode started recently before today (1.1)
    > Run timed events > creates S9 letter (1.1)
    > Process S9 letter batch > S10 (1.1)
    > Log kit > S43 (1.2)
    > Read kit with ABNORMAL result > A8 (1.3)
    > Invite for colonoscopy assessment > A183 (1.11)
    > Process A183 appointment letter > A25 (1.11)
    > Attend assessment appointment > J10 (1.11)
    > Process A183 result letter (A167) (1.11)
    > Suitable for colonoscopy > A99 (1.12)
    > Invite for diagnostic test > A59 (2.1)
    > Cancel diagnostic test > A306 (2.1)
    > Record patient contact – contacted, close on patient choice > A396 (2.3)
    > Record diagnosis date reason (A52)
    > Process A396 letter batch > A392 (2.3)
    > Process A391 letter batch > A350 (2.3) > C203 (1.13)
    > Check recall [SSCL13a(A350)]
    """
    # Given I log in to BCSS "England" as user role "Hub Manager"
    user_role = UserTools.user_login(
        page, "Hub Manager State Registered at BCS01", return_role_type=True
    )
    if user_role is None:
        raise ValueError("User cannot be assigned to a UserRoleType")

    # And there is a subject who meets the following criteria:
    criteria = {
        "latest event status": "S9 Pre-Invitation Sent",
        "latest episode kit class": "FIT",
        "latest episode started": "Within the last 6 months",
        "latest episode type": "FOBT",
        "subject age": "Between 60 and 72",
        "subject has unprocessed sspi updates": "No",
        "subject has user dob updates": "No",
    }
    subject = Subject()
    user = User()
    builder = SubjectSelectionQueryBuilder()

    query, bind_vars = builder.build_subject_selection_query(
        criteria=criteria,
        user=user,
        subject=subject,
        subjects_to_retrieve=1,
    )

    nhs_no_df = OracleDB().execute_query(query, bind_vars)
    nhs_no = nhs_no_df["subject_nhs_number"].iloc[0]

    # Then Comment: NHS number
    logging.info(f"[SUBJECT CREATION] Created subject's NHS number: {nhs_no}")

    # When I run Timed Events for my subject
    OracleDB().exec_bcss_timed_events(nhs_number=nhs_no)

    # Then there is a "S9" letter batch for my subject with the exact title "Invitation & Test Kit (FIT)"
    # When I process the open "S9" letter batch for my subject
    batch_processing(
        page, "S9", "Invitation & Test Kit (FIT)", "S10 - Invitation & Test Kit Sent"
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
        criteria={
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
        criteria={
            "latest event status": "J10 Attended Colonoscopy Assessment Appointment",
        },
    )

    # When I switch users to BCSS "England" as user role "Hub Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    # And there is a "A183" letter batch for my subject with the exact title "GP Result (Abnormal)"
    # And I process the open "A183 - GP Result (Abnormal)" letter batch for my subject
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

    # And I edit the Colonoscopy Assessment Dataset for this subject
    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_colonoscopy_show_datasets()

    # And I update the Colonoscopy Assessment Dataset with the following values:
    ColonoscopyDatasetsPage(page).select_fit_for_colonoscopy_option(
        FitForColonoscopySspOptions.YES
    )
    ColonoscopyDatasetsPage(page).click_dataset_complete_radio_button_yes()
    ColonoscopyDatasetsPage(page).save_dataset()

    # And I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I advance the subject's episode for "Suitable for Endoscopic Test"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_suitable_for_endoscopic_test_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no, {"latest event status": "A99 Suitable for Endoscopic Test"}
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the advance episode options
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # And I enter a Diagnostic Test First Offered Appointment Date of "today"
    AdvanceFOBTScreeningEpisodePage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())

    # And I select Diagnostic Test Type "Colonoscopy"
    AdvanceFOBTScreeningEpisodePage(page).select_test_type_dropdown_option(
        "Colonoscopy"
    )

    # And I advance the subject's episode for "Invite for Diagnostic Test >>"
    AdvanceFOBTScreeningEpisodePage(page).click_invite_for_diagnostic_test_button()

    # Then my subject has been updated as follows:
    AdvanceFOBTScreeningEpisodePage(page).verify_latest_event_status_value(
        "A59 - Invited for Diagnostic Test"
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I advance the subject's episode for "Cancel Diagnostic Test"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_cancel_diagnostic_test_button()

    # Then my subject has been updated as follows:
    AdvanceFOBTScreeningEpisodePage(page).verify_latest_event_status_value(
        "A306 - Cancel Diagnostic Test"
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I select the advance episode option for "Record Contact with Patient"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_record_contact_with_patient_button()

    # And I record contact with the subject with outcome "Close Episode - Patient Choice"
    ContactWithPatientPage(page).record_contact("Close Episode - Patient Choice")

    # Then my subject has been updated as follows:
    AdvanceFOBTScreeningEpisodePage(page).verify_latest_event_status_value(
        "A396 - Discharged from Screening Round - Patient Choice"
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I select the advance episode option for "Record Diagnosis Date"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_record_diagnosis_date_button()

    # And I select Diagnosis Date Reason "Patient choice"
    PatientAdvisedOfDiagnosisPage(page).select_diagnosis_reason("Patient choice")

    # Then my subject has been updated as follows:
    criteria = {
        "latest episode diagnosis date reason": "Patient choice",
        "latest episode has diagnosis date": "No",
        "latest episode includes event status": "A52 No diagnosis date recorded",
    }
    subject_assertion(nhs_no, criteria)

    # And there is a "A396" letter batch for my subject with the exact title "Discharge from screening round - patient decision (letter to patient)"
    # When I process the open "A396" letter batch for my subject
    batch_processing(
        page,
        "A396",
        "Discharge from screening round - patient decision (letter to patient)",
        "A392 - Patient Discharge Letter Printed - Patient Choice",
    )

    # And there is a "A392" letter batch for my subject with the exact title "Discharge from screening round - patient decision (letter to GP)"
    # When I process the open "A392" letter batch for my subject
    batch_processing(
        page,
        "A392",
        "Discharge from screening round - patient decision (letter to GP)",
        "A350 - Letter of Non-agreement to Continue with Investigation sent to GP",
    )

    # Then my subject has been updated as follows:
    criteria = {
        "calculated fobt due date": "2 years from episode end",
        "calculated lynch due date": "Unchanged",
        "calculated surveillance due date": "Unchanged",
        "ceased confirmation date": "Null",
        "ceased confirmation details": "Null",
        "ceased confirmation user ID": "Null",
        "clinical reason for cease": "Null",
        "latest episode accumulated result": "No result",
        "latest episode recall calculation method": "Episode end date",
        "latest episode recall episode type": "FOBT Screening",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Closed",
        "latest episode status reason": "Informed Dissent",
        "latest event status": "A350 Letter of Non-agreement to Continue with Investigation sent to GP",
        "lynch due date": "Null",
        "lynch due date date of change": "Unchanged",
        "lynch due date reason": "Unchanged",
        "screening due date": "Calculated FOBT Due Date",
        "screening due date reason": "Recall",
        "screening due date date of change": "Today",
        "screening status": "Recall",
        "screening status reason": "Recall",
        "surveillance due date": "Null",
        "surveillance due date date of change": "Unchanged",
        "surveillance due date reason": "Unchanged",
    }
    subject_assertion(nhs_no, criteria)
    LogoutPage(page).log_out()
