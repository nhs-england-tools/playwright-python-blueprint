import logging
import pytest
from playwright.sync_api import Page
from classes.repositories.general_repository import GeneralRepository
from pages.base_page import BasePage
from pages.logout.log_out_page import LogoutPage
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
def test_lynch_scenario_3_1(page: Page) -> None:
    """
    Scenario: 3.1 - DNA colonoscopy assessment twice - self referral

    G4-G2-G3-A183-A25-J11-J27-A184-A26-A185-A37-A166-C203 over age range [SSCL5b(A166)]

    This scenario tests where the patient is discharged from their Lynch episode because they DNA their colonoscopy assessment appointment twice.

    Subject summary:

    > Process Lynch diagnosis for a new over-age subject suitable for immediate  self-referral
    > Run Lynch invitations > G4 (5.1)
    > Process G4 letter batch > G2 (5.1)
    > Run timed events > G3 (5.1)
    > Book appointment > A183 (1.11)
    > Process A183 letter batch > A25 (1.11)
    > Subject DNA > J11 (1.11)
    > Process J11 letter batch > J27 (1.11)
    > Book appointment > A184 (1.11)
    > Process A184 letter batch > A26 (1.11)
    > Subject DNA > A185 (1.11)
    > Process A185 letter batch > A37 (1.11)
    > Process A37 letter batch > A166 (1.11)
    > Check recall [SSCL5b(A166)]
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
    # And The subject DNAs the practitioner appointment
    AppointmentAttendance(page).mark_as_dna("Patient did not attend")

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "J11 1st Colonoscopy Assessment Appointment Non-attendance (Patient)",
        },
    )

    # And there is a "J11" letter batch for my subject with the exact title "Practitioner Clinic 1st Appointment Non Attendance (Patient) (Lynch)"
    # When I process the open "J11" letter batch for my subject
    batch_processing(
        page,
        "J11",
        "Practitioner Clinic 1st Appointment Non Attendance (Patient) (Lynch)",
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
            "latest event status": "A184 2nd Colonoscopy Assessment Appointment Requested",
        },
    )

    # And there is a "A184" letter batch for my subject with the exact title "Practitioner Clinic 2nd Appointment (Lynch)"
    # When I process the open "A184" letter batch for my subject
    batch_processing(page, "A184", "Practitioner Clinic 2nd Appointment (Lynch)")

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A26 2nd Colonoscopy Assessment Appointment Booked, letter sent",
        },
    )

    # And I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the event history for the subject's latest episode
    # And I view the latest practitioner appointment in the subject's episode
    # And The subject DNAs the practitioner appointment
    AppointmentAttendance(page).mark_as_dna("Patient did not attend")

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A185 2nd Colonoscopy Assessment Appointment Non-attendance (Patient)",
        },
    )

    # And there is a "A185" letter batch for my subject with the exact title "Patient Discharge (Non Attendance of Practitioner Clinic) (Lynch)"
    # When I process the open "A185" letter batch for my subject
    batch_processing(
        page,
        "A185",
        "Patient Discharge (Non Attendance of Practitioner Clinic) (Lynch)",
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A37 Patient Discharge Sent (Non-attendance at Colonoscopy Assessment Appointment)",
        },
    )

    # When I switch users to BCSS "England" as user role "Hub Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    user_role = UserTools.user_login(
        page, "Hub Manager State Registered at BCS01", True
    )
    if user_role is None:
        raise ValueError("User cannot be assigned to a UserRoleType")

    # And there is a "A37" letter batch for my subject with the exact title "GP Discharge (Non Attendance of Practitioner Clinic) (Lynch)"
    # When I process the open "A37" letter batch for my subject
    batch_processing(
        page,
        "A37",
        "GP Discharge (Non Attendance of Practitioner Clinic) (Lynch)",
    )

    logging.info("Check subject details against closure scenario SSCL5b(A166)")

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "Calculated FOBT due date": "Null",
            "Calculated lynch due date": "2 years from latest A37 event",
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
            "Latest episode status reason": "Non Response",
            "Latest event status": "A166 GP Discharge Sent (No show for Colonoscopy Assessment Appointment)",
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
            "Surveillance due date date of change": "Null",
            "Surveillance due date reason": "Null",
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
