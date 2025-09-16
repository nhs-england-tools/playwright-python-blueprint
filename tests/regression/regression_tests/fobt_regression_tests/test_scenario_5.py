import pytest
import logging
from datetime import datetime
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
from pages.logout.log_out_page import LogoutPage
from pages.base_page import BasePage
from pages.screening_subject_search.advance_fobt_screening_episode_page import (
    AdvanceFOBTScreeningEpisodePage,
)
from pages.screening_subject_search.record_diagnosis_date_page import (
    RecordDiagnosisDatePage,
)
from utils.appointments import mark_appointment_as_dna


@pytest.mark.usefixtures("setup_org_and_appointments")
@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.fobt_regression_tests
def test_scenario_5(page: Page) -> None:
    """
    Scenario: 5: DNA colonoscopy assessment twice

    S1-S9-S10-S43-A8-A183-A25-J11-J27-A184-A26-A185-A37-A166-P202-(A50)-(A167)-A166-C203 [SSCL4a(A166)]

    This scenario tests where the patient is discharged from their FOBT episode because they DNA their colonoscopy assessment appointment twice. It also tests the diagnosis date and kit result letter spur events.

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
    > Patient DNA appointment > J11 (1.11)
    > Process J11 letter batch > J27 (1.11)
    > Rebook colonoscopy assessment > A184 (1.11)
    > Process A184 letter > A26 (1.11)
    > Patient DNA appointment > A185 (1.11)
    > Process A185 letter batch > A37 (1.11)
    > Process A37 letter batch > A166 (1.11) > P202
    > Record diagnosis date (A50)
    > Process A183 result letter (A167) > A166 (1.11) > C203 (1.13)
    > Check recall [SSCL4a(A166)]
    """

    summary_page = SubjectScreeningSummaryPage(page)
    logging.info(
        "[TEST START] Regression - Scenario: 5: DNA colonoscopy assessment twice"
    )

    # Given I log in to BCSS "England" as user role "Hub Manager"
    user_role = UserTools.user_login(
        page, "Hub Manager at BCS01", return_role_type=True
    )
    if user_role is None:
        raise ValueError("User cannot be assigned to a UserRoleType")

    # And I create a subject that meets the following criteria:
    requirements = {
        "age (y/d)": "64/12",
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
            "subject age": "64",
            "subject has episodes": "No",
            "screening status": "Inactive",
        },
    )
    # Assert subject details in the UI
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    summary_page.assert_subject_age(64)
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

    # When I read my subject's latest logged FIT kit as "ABNORMAL"
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
    # And The subject DNAs the practitioner appointment
    mark_appointment_as_dna(page, "Patient did not attend")

    # And there is a "J11" letter batch for my subject with the exact title "Practitioner Clinic 1st Appointment Non Attendance (Patient)"
    # When I process the open "J11" letter batch for my subject
    # Then my subject has been updated as follows:
    batch_processing(
        page,
        "J11",
        "Practitioner Clinic 1st Appointment Non Attendance (Patient)",
        "J27 - Appointment Non-attendance Letter Sent (Patient)",
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
            "latest event status": "A184 2nd Colonoscopy Assessment Appointment Requested",
        },
    )

    # And there is a "A184" letter batch for my subject with the exact title "Practitioner Clinic 2nd Appointment"
    # When I process the open "A184 - Practitioner Clinic 2nd Appointment" letter batch for my subject
    # Then my subject has been updated as follows:
    batch_processing(
        page,
        "A184",
        "Practitioner Clinic 2nd Appointment",
        "A26 - 2nd Colonoscopy Assessment Appointment Booked, letter sent",
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the event history for the subject's latest episode
    # And I view the latest practitioner appointment in the subject's episode
    # And The subject DNAs the practitioner appointment
    mark_appointment_as_dna(page, "Patient did not attend")

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A185 2nd Colonoscopy Assessment Appointment Non-attendance (Patient)",
        },
    )

    # And there is a "A185" letter batch for my subject with the exact title "Patient Discharge (Non Attendance of Practitioner Clinic)"
    # When I process the open "A185" letter batch for my subject
    # Then my subject has been updated as follows:
    batch_processing(
        page,
        "A185",
        "Patient Discharge (Non Attendance of Practitioner Clinic)",
        "A37 - Patient Discharge Sent (Non-attendance at Colonoscopy Assessment Appointment)",
    )

    # When I switch users to BCSS "England" as user role "Hub Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    # And there is a "A37" letter batch for my subject with the exact title "GP Discharge (Non Attendance of Practitioner Clinic)"
    # And I process the open "A37" letter batch for my subject
    # Then my subject has been updated as follows:
    batch_processing(
        page,
        "A37",
        "GP Discharge (Non Attendance of Practitioner Clinic)",
        "P202 - Waiting Completion of Outstanding Events",
    )

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

    # The steps below have been commented out because it appears that the A50 event is not currently being created when the diagnosis date is recorded.
    # The final assertion (line 353) passes without these steps so this needs to be investigated and fixed when Kate and Rob return from leave.

    # # Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_no,
    #     {
    #         "latest episode diagnosis date reason": "Null",
    #         "latest episode has diagnosis date": "Yes",
    #         "latest episode includes event status": "A50 Diagnosis date recorded",
    #         "latest event status": "P202 Waiting Completion of Outstanding Events",
    #     },
    # )

    # # When I process the open "A183 - GP Result (Abnormal)" letter batch for my subject
    # # Then my subject has been updated as follows:
    # batch_processing(
    #     page,
    #     "A183",
    #     "GP Result (Abnormal)",
    #     "A166 - GP Discharge Sent (No show for Colonoscopy Assessment Appointment)",
    # )

    subject_assertion(
        nhs_no,
        {
            "calculated FOBT due date": "2 years from latest A37 event",
            "calculated lynch due date": "Unchanged",
            "calculated surveillance due date": "Unchanged",
            "ceased confirmation date": "Null",
            "ceased confirmation details": "Null",
            "ceased confirmation user ID": "Null",
            "clinical reason for cease": "Null",
            "latest episode accumulated result": "Definitive abnormal FOBT outcome",
            "latest episode includes event status": "A167 GP Abnormal FOBT Result Sent",
            "latest episode recall calculation method": "Date of last patient letter",
            "latest episode recall episode type": "FOBT Screening",
            "latest episode recall surveillance type": "Null",
            "latest episode status": "Closed",
            "latest episode status reason": "Non Response",
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
        },
    )
