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
from utils.appointments import book_appointments, book_post_investigation_appointment
from utils.oracle.oracle import OracleDB
from utils.investigation_dataset import InvestigationDatasetCompletion
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from pages.screening_subject_search.diagnostic_test_outcome_page import (
    DiagnosticTestOutcomePage,
    OutcomeOfDiagnosticTest,
    ReasonForOnwardReferral,
)
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
from pages.screening_subject_search.attend_diagnostic_test_page import (
    AttendDiagnosticTestPage,
)
from pages.screening_subject_search.record_diagnosis_date_page import (
    RecordDiagnosisDatePage,
)
from pages.datasets.subject_datasets_page import SubjectDatasetsPage
from pages.datasets.colonoscopy_dataset_page import (
    ColonoscopyDatasetsPage,
    FitForColonoscopySspOptions,
)
from pages.datasets.investigation_dataset_page import (
    InvestigationDatasetsPage,
    FailureReasonsOptions,
    DrugTypeOptions,
    BowelPreparationQualityOptions,
    ComfortOptions,
    EndoscopyLocationOptions,
    InsufflationOptions,
    LateOutcomeOptions,
    OutcomeAtTimeOfProcedureOptions,
    YesNoOptions,
    EndoscopyLocationOptions,
)
from pages.screening_subject_search.non_neoplastic_result_from_symptomatic_procedure_page import (NonNeoplasticResultFromSymptomaticProcedurePage)
from utils.subject_demographics import SubjectDemographicUtil
from pages.screening_subject_search.reopen_fobt_screening_episode_page import (
    ReopenFOBTScreeningEpisodePage,
)
from pages.screening_subject_search.return_from_symptomatic_referral_page import (
    ReturnFromSymptomaticReferralPage,
)
from pages.screening_subject_search.contact_with_patient_page import (
    ContactWithPatientPage,
)


@pytest.mark.usefixtures("setup_org_and_appointments")
@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.fobt_regression_tests
def test_scenario_12(page: Page) -> None:
    """
    Scenario: 12: Abnormal result from symptomatic procedure, then refer for another diagnostic test

    S9-S10-S43-A8-A183-(A167)-A25-J10-A99-A59-A259-A315-A360-A410-A415-A416-A316-A353-A372-A373-A358-A65-P202-(A52)-A65-C203 [SSCL10a] [SSDOB8] [SSDOB11] A372-A373-A358-(A50)-A65-C203 [SSCL12a] A372-A373-A389-A361-A323-A317-A319-A395

    This scenario tests progression of an FOBT episode to closure on A65 Abnormal from symptomatic procedure result, and checks that following referral for symptomatic procedure the "lowest" result possible is Abnormal, even if diagnostic test results were "No result" and the symptomatic procedure result is non-neoplastic. This scenario tests both in-age and below-age closures, and a reopen to re-record the symptomatic result, and checks that recall can be based on either the diagnostic test date or the symptomatic procedure date. It also tests timed episode closure from P202 when no diagnosis date is entered (the reason is removed during the reopen), and manually changing a subject's age outside of an open episode to check a couple of the DOB change rules.

    BCSS-17906 NOTE: The pathway for referring for another diagnostic test following symptomatic procedure is currently incomplete, so stopping at A361

    Scenario summary:

    > Find an in-age subject at S9 whose episode started recently before today (1.1)
    > Run timed events > creates S9 letter (1.1)
    > Process S9 letter batch > S10 (1.1)
    > Log kit > S43 (1.2)
    > Read kit with ABNORMAL result > A8 (1.3)
    > Invite for colonoscopy assessment > A183 (1.11)
    > Process A183 result letter (A167) (1.11)
    > Process A183 appointment letter > A25 (1.11)
    > Attend assessment appointment > J10 (1.11)
    > Suitable for colonoscopy > A99 (1.12)
    > Invite for diagnostic test > A59 (2.1)
    > Attend diagnostic test > A259 (2.1)
    > Complete investigation dataset – failed test, no result (2.1)
    > Enter diagnostic test outcome – refer symptomatic > A315 (2.1)
    > Post-investigation appointment required > A360 (2.1)
    > Book post-investigation appointment > A410 (2.4)
    > Process A410 letter batch > A415 (2.4)
    > Attend post-investigation appointment > A416 > A316 (2.4)
    > MDT not required > A353 (2.6)
    > Process A353 letter batch > A372 (2.6)
    > Record symptomatic result - non-neoplastic > A373 (2.7)
    > Refer FOBT > A358 (2.7)
    > Process A358 letter batch > A65 (2.7) > P202
    > Run timed events > (A52) > A65 > C203 (2.8, 1.13)
    > Check recall [SSCL10a]
    > Manual update changes subject to over-age
    > Check subject changes [SSDOB8]
    > Manual update changes subject to below-age
    > Check subject changes [SSDOB11]
    > Reopen to Re-record Outcome from Symptomatic Referral > A372 (2.7)
    > Record symptomatic result - non-neoplastic > A373 (2.7)
    > Refer FOBT > A358 (2.7)
    > Record diagnosis date > (A50)
    > Process A358 letter batch > A65 (2.7) > C203 (2.8, 1.13)
    > Check recall [SSCL12a]
    > Reopen to Re-record Outcome from Symptomatic Referral > A372 (2.7)
    > Record symptomatic result - non-neoplastic > A373 (2.7)
    > Refer another diagnostic test > A389 (2.7)
    > Post-investigation appointment not required > A361 (2.1)
    > Record patient contact – post-investigation appointment not required > A323 (2.1) > A317 > A319 (2.5)
    > Process A319 letter batch > A395 (2.5)
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

    query, bind_vars = SubjectSelectionQueryBuilder().build_subject_selection_query(
        criteria,
        User(),
        Subject(),
        1,
    )

    nhs_no_df = OracleDB().execute_query(query, bind_vars)
    nhs_no = nhs_no_df["subject_nhs_number"].iloc[0]

    # Then Comment: NHS number
    logging.info(f"[SUBJECT RETRIEVAL] Retrieved subject's NHS number: {nhs_no}")

    # When I run Timed Events for my subject
    OracleDB().exec_bcss_timed_events(nhs_number=nhs_no)

    # Then there is a "S9" letter batch for my subject with the exact title "Invitation & Test Kit (FIT)"
    # When I process the open "S9" letter batch for my subject
    batch_processing(
        page=page,
        batch_type="S9",
        batch_description="Invitation & Test Kit (FIT)",
        latest_event_status="S10 - Invitation & Test Kit Sent",
    )

    # When I log my subject's latest unlogged FIT kit
    fit_kit = FitKitGeneration().get_fit_kit_for_subject_sql(nhs_no, False, False)
    FitKitLogged().log_fit_kits(page, fit_kit, datetime.now())

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {"latest event status": "S43 Kit Returned and Logged (Initial Test)"},
    )

    # When I read my subject's latest logged FIT kit as "ABNORMAL"
    FitKitLogged().read_latest_logged_kit(
        user=user_role, kit_type=2, kit=fit_kit, kit_result="ABNORMAL"
    )

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
        page=page,
        screening_centre="BCS001 - Wolverhampton Bowel Cancer Screening Centre",
        site="The Royal Hospital (Wolverhampton)",
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A183 1st Colonoscopy Assessment Appointment Requested"
        },
    )
    # And there is a "A183" letter batch for my subject with the exact title "GP Result (Abnormal)"
    # When I process the open "A183 - GP Result (Abnormal)" letter batch for my subject
    batch_processing(page, "A183", "GP Result (Abnormal)")

    # Then my subject has been updated as follows:
    criteria = {
        "latest episode includes event status": "A167 GP Abnormal FOBT Result Sent",
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

    # When I switch users to BCSS "England" as user role "Screening Centre Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    user_role = UserTools.user_login(page, "Screening Centre Manager at BCS001", True)
    if user_role is None:
        raise ValueError("User role is none")

    # And I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the event history for the subject's latest episode
    SubjectScreeningSummaryPage(page).expand_episodes_list()
    SubjectScreeningSummaryPage(page).click_first_fobt_episode_link()

    # And I view the latest practitioner appointment in the subject's episode
    EpisodeEventsAndNotesPage(page).click_most_recent_view_appointment_link()

    # And I attend the subject's practitioner appointment "yesterday"
    AppointmentDetailPage(page).mark_appointment_as_attended(
        datetime.today() - timedelta(days=1)
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_number=nhs_no,
        criteria={
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
        option=FitForColonoscopySspOptions.YES
    )
    ColonoscopyDatasetsPage(page).click_dataset_complete_radio_button_yes()

    # And I save the Colonoscopy Assessment Dataset
    ColonoscopyDatasetsPage(page).save_dataset()

    # And I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I advance the subject's episode for "Suitable for Endoscopic Test"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_suitable_for_endoscopic_test_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {"latest event status": "A99 Suitable for Endoscopic Test"},
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the advance episode options
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # And I select Diagnostic Test Type "Colonoscopy"
    AdvanceFOBTScreeningEpisodePage(page).select_test_type_dropdown_option(
        "Colonoscopy"
    )

    # And I enter a Diagnostic Test First Offered Appointment Date of "tomorrow"
    AdvanceFOBTScreeningEpisodePage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today() + timedelta(days=1))

    # And I advance the subject's episode for "Invite for Diagnostic Test >>"
    AdvanceFOBTScreeningEpisodePage(page).click_invite_for_diagnostic_test_button()

    # Then my subject has been updated as follows:
    AdvanceFOBTScreeningEpisodePage(page).verify_latest_event_status_value(
        latest_event_status="A59 - Invited for Diagnostic Test"
    )

    # When I select the advance episode option for "Attend Diagnostic Test"
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_attend_diagnostic_test_button()

    # And I attend the subject's diagnostic test today
    AttendDiagnosticTestPage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())
    AttendDiagnosticTestPage(page).click_save_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_number=nhs_no,
        criteria={
            "latest event status": "A259 Attended Diagnostic Test",
        },
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I edit the Investigation Dataset for this subject
    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    # And I set the following fields and values within the "Investigation Dataset" section of the investigation dataset:
    general_information = {
        "site": 1,
        "practitioner": 1,
        "testing clinician": 1,
        "aspirant endoscopist": None,
    }

    # When I add the following "bowel preparation administered" drugs and doses within the Investigation Dataset for this subject:
    drug_information = {"drug_type1": DrugTypeOptions.MANNITOL, "drug_dose1": "3"}

    # And I set the following fields and values within the "Endoscopy Information" section of the investigation dataset:
    endoscopy_information = {
        "endoscope inserted": "yes",
        "procedure type": "diagnostic",
        "bowel preparation quality": BowelPreparationQualityOptions.FAIR,
        "comfort during examination": ComfortOptions.MODERATE_DISCOMFORT,
        "comfort during recovery": ComfortOptions.MINIMAL_DISCOMFORT,
        "endoscopist defined extent": EndoscopyLocationOptions.DESCENDING_COLON,
        "scope imager used": YesNoOptions.YES,
        "retroverted view": YesNoOptions.NO,
        "start of intubation time": "09:00",
        "start of extubation time": "09:30",
        "end time of procedure": "10:00",
        "scope id": "Autotest",
        "insufflation": InsufflationOptions.AIR,
        "outcome at time of procedure": OutcomeAtTimeOfProcedureOptions.LEAVE_DEPARTMENT,
        "late outcome": LateOutcomeOptions.NO_COMPLICATIONS,
    }

    # And I set the following failure reasons within the Investigation Dataset for this subject:
    failure_information = {"failure reasons": FailureReasonsOptions.PAIN}

    # And I mark the Investigation Dataset as complete
    # And I press the save Investigation Dataset button
    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
    )

    # Then the Investigation Dataset result message, which I will cancel, is "No Result"
    InvestigationDatasetsPage(page).expect_text_to_be_visible("No Result")

    # And my subject has been updated as follows:
    subject_assertion(nhs_no, {"latest episode accumulated result": "No result"})

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I select the advance episode option for "Enter Diagnostic Test Outcome"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_enter_diagnostic_test_outcome_button()

    # And I select Outcome of Diagnostic Test "Refer Symptomatic"
    DiagnosticTestOutcomePage(page).select_test_outcome_option(
        OutcomeOfDiagnosticTest.REFER_SYMPTOMATIC
    )
    # And I select Reason for Symptomatic Referral value "Corrective Surgery"
    DiagnosticTestOutcomePage(page).select_reason_for_onward_referral(
        ReasonForOnwardReferral.CORRECTIVE_SURGERY
    )

    # And I save the Diagnostic Test Outcome
    DiagnosticTestOutcomePage(page).click_save_button()

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # When I advance the subject's episode for "Post-investigation Appointment Required"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(
        page
    ).click_post_investigation_appointment_required_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A360 Post-investigation Appointment Required",
        },
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I choose to book a practitioner clinic for my subject
    SubjectScreeningSummaryPage(page).click_book_practitioner_clinic_button()

    # And I set the practitioner appointment date to "today"
    # And I book the earliest available post investigation appointment on this date
    book_post_investigation_appointment(page, "The Royal Hospital (Wolverhampton)", 1)

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A410 Post-investigation Appointment Made",
        },
    )

    # And there is a "A410" letter batch for my subject with the exact title "Post-Investigation Appointment Invitation Letter"
    # When I process the open "A410" letter batch for my subject
    # Then my subject has been updated as follows:
    batch_processing(
        page,
        "A410",
        "Post-Investigation Appointment Invitation Letter",
        "A415 - Post-investigation Appointment Invitation Letter Printed",
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the event history for the subject's latest episode
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
            "latest episode includes event status": "A416 Post-investigation Appointment Attended",
            "latest event status": "A316 Post-investigation Appointment Attended",
        },
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I advance the subject's episode for "MDT Referral Not Required"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_mdt_referral_not_required_button()

    # Then my subject has been updated as follows:
    subject_assertion(nhs_no, {"latest event status": "A353 MDT Referral Not Required"})

    # And there is a "A353" letter batch for my subject with the exact title "GP Letter Indicating Referral to Symptomatic"
    # When I process the open "A353" letter batch for my subject

    batch_processing(
        page,
        "A353",
        "GP Letter Indicating Referral to Symptomatic",
        "A372 - Refer Symptomatic, GP Letter Printed",
    )

    # When I view the advance episode options
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # And I select the advance episode option for "Non-neoplastic and Other Non-bowel Cancer Result"
    AdvanceFOBTScreeningEpisodePage(
        page
    ).click_non_neoplastic_and_other_non_bowel_cancer_result_button()

    # And I set the Date of Symptomatic Procedure to "yesterday"
    NonNeoplasticResultFromSymptomaticProcedurePage(
        page
    ).enter_date_of_symptomatic_procedure(datetime.now() - timedelta(days=1))

    # And the Screening Interval is 24 months
    NonNeoplasticResultFromSymptomaticProcedurePage(page).assert_text_in_alert_textbox(
        "recall interval of 24 months"
    )

    # And I select test number 1
    NonNeoplasticResultFromSymptomaticProcedurePage(page).select_test_number(1)

    # And I save the Result from Symptomatic Procedure
    NonNeoplasticResultFromSymptomaticProcedurePage(page).click_save_button()

    # Then my subject has been updated as follows:
    criteria = {
        "which diagnostic test": "Latest not-void test in latest episode",
        "latest episode accumulated result": "Abnormal",
        "latest event status": "A373 Symptomatic result recorded",
        "symptomatic procedure date": "Yesterday",
        "symptomatic procedure result": "Non-neoplastic",
    }
    subject_assertion(nhs_no, criteria)

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # When I advance the subject's episode for "Return to FOBT after Symptomatic Referral"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(
        page
    ).click_return_to_fobt_after_symptomatic_referral_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {"latest event status": "A358 Return to FOBT after Symptomatic Referral"},
    )

    # And there is a "A358" letter batch for my subject with the exact title "Return FOBT Letter after Referral to Symptomatic"
    # When I process the open "A358" letter batch for my subject
    # Then my subject has been updated as follows:
    # When I run Timed Events for my subject
    batch_processing(
        page,
        "A358",
        "Return FOBT Letter after Referral to Symptomatic",
        "P202 - Waiting Completion of Outstanding Events",
        True,
    )

    # Then my subject has been updated as follows:
    criteria = {
        "which diagnostic test": "Latest not-void test in latest episode",
        "calculated fobt due date": "2 years from symptomatic procedure",
        "calculated lynch due date": "Null",
        "calculated surveillance due date": "Unchanged",
        "ceased confirmation date": "Null",
        "ceased confirmation details": "Null",
        "ceased confirmation user id": "Null",
        "clinical reason for cease": "Null",
        "latest episode accumulated result": "Abnormal",
        "latest episode diagnosis date reason": "System closure after no input of diagnosis date",
        "latest episode has diagnosis date": "No",
        "latest episode includes event status": "A52 No diagnosis date recorded",
        "latest episode recall calculation method": "Symptomatic procedure date",
        "latest episode recall episode type": "FOBT Screening",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Closed",
        "latest episode status reason": "Episode Complete",
        "latest event status": "A65 Abnormal",
        "lynch due date": "Null",
        "lynch due date reason": "Unchanged",
        "lynch due date date of change": "Unchanged",
        "screening due date": "Calculated FOBT Due Date",
        "screening due date date of change": "Today",
        "screening due date reason": "Recall",
        "screening status": "Recall",
        "screening status reason": "Recall",
        "surveillance due date": "Null",
        "surveillance due date date of change": "Unchanged",
        "surveillance due date reason": "Unchanged",
        "symptomatic procedure date": "Yesterday",
        "symptomatic procedure result": "Non-neoplastic",
        "screening referral type": "Null",
    }
    subject_assertion(nhs_no, criteria)

    # When I view the subject
    # And I update the subject's date of birth to make them 82 years old
    # And I update the subject's postcode to "AA1 2BB"
    # And I save my changes to the subject's demographics
    # Then I get a confirmation prompt that "contains" "This change to the DoB will result in the subject being above the eligible age range for screening"
    # When I press OK on my confirmation prompt
    SubjectDemographicUtil(page).updated_subject_demographics(
        nhs_no,
        82,
        "AA1 2BB",
        "This change to the DoB will result in the subject being above the eligible age range for screening",
    )

    # Then my subject has been updated as follows:
    criteria = {
        "calculated fobt due date": "Unchanged",
        "calculated lynch due date": "Null",
        "calculated surveillance due date": "Unchanged",
        "ceased confirmation date": "Today",
        "ceased confirmation details": "Change of DOB requires cease due to age.",
        "ceased confirmation user id": "User's ID",
        "clinical reason for cease": "Null",
        "lynch due date": "Null",
        "lynch due date reason": "Unchanged",
        "lynch due date date of change": "Unchanged",
        "previous screening status": "Recall",
        "screening due date": "Null",
        "screening due date date of change": "Today",
        "screening due date reason": "Ceased",
        "screening status": "Ceased",
        "screening status date of change": "Today",
        "screening status reason": "Outside Screening Population",
        "subject age": "82",
        "surveillance due date": "Null",
        "surveillance due date date of change": "Unchanged",
        "surveillance due date reason": "Unchanged",
    }
    subject_assertion(nhs_no, criteria, user_role)

    # When I view the subject
    # And I update the subject's date of birth to make them 42 years old
    # And I update the subject's postcode to "AA1 2BB"
    # And I save my changes to the subject's demographics
    # Then I get a confirmation prompt that "contains" "This change to the DoB will result in the subject falling below the eligible age for screening"
    # When I press OK on my confirmation prompt
    SubjectDemographicUtil(page).updated_subject_demographics(
        nhs_no,
        42,
        "AA1 2BB",
        "This change to the DoB will result in the subject falling below the eligible age for screening",
    )

    #  Then my subject has been updated as follows:
    criteria = {
        "calculated fobt due date": "Unchanged",
        "calculated lynch due date": "Null",
        "calculated surveillance due date": "Unchanged",
        "ceased confirmation date": "Null",
        "ceased confirmation details": "Null",
        "ceased confirmation user id": "Null",
        "clinical reason for cease": "Null",
        "lynch due date": "Null",
        "lynch due date reason": "Unchanged",
        "lynch due date date of change": "Unchanged",
        "previous screening status": "Ceased",
        "screening due date": "Null",
        "screening due date date of change": "Today",
        "screening due date reason": "Awaiting Failsafe",
        "screening status": "Recall",
        "screening status date of change": "Today",
        "screening status reason": "Opt-in due to error",
        "subject age": "42",
        "surveillance due date": "Null",
        "surveillance due date date of change": "Unchanged",
        "surveillance due date reason": "Unchanged",
    }
    subject_assertion(nhs_no, criteria)

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I reopen the subject's episode for "Reopen to Re-record Outcome from Symptomatic Referral"
    SubjectScreeningSummaryPage(page).click_reopen_fobt_screening_episode_button()
    ReopenFOBTScreeningEpisodePage(
        page
    ).click_reopen_to_rerecord_outcome_from_symptomatic_referral_button()

    # Then my subject has been updated as follows:
    criteria = {
        "which diagnostic test": "Latest not-void test in latest episode",
        "calculated fobt due date": "As at episode start",
        "calculated lynch due date": "Null",
        "calculated surveillance due date": "Unchanged",
        "ceased confirmation date": "Null",
        "ceased confirmation details": "Null",
        "ceased confirmation user id": "Null",
        "clinical reason for cease": "Null",
        "latest episode accumulated result": "No Result",
        "latest episode diagnosis date reason": "Null",
        "latest episode has diagnosis date": "No",
        "latest episode includes event code": "E372 Reopen to Re-record Outcome from Symptomatic Referral",
        "latest episode recall calculation method": "Symptomatic procedure date",
        "latest episode recall episode type": "Null",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Open",
        "latest episode status reason": "Null",
        "latest event status": "A372 Refer Symptomatic, GP Letter Printed",
        "screening due date": "Calculated FOBT Due Date",
        "screening due date date of change": "Today",
        "screening due date reason": "Reopened episode",
        "surveillance due date": "Null",
        "surveillance due date date of change": "Unchanged",
        "surveillance due date reason": "Unchanged",
        "symptomatic procedure date": "Null",
        "symptomatic procedure result": "Null",
        "screening referral type": "Null",
    }
    subject_assertion(nhs_number=nhs_no, criteria=criteria)

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # When I view the advance episode options
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # And I select the advance episode option for "Non-neoplastic and Other Non-bowel Cancer Result"
    AdvanceFOBTScreeningEpisodePage(
        page=page
    ).click_non_neoplastic_and_other_non_bowel_cancer_result_button()

    # And I set the Date of Symptomatic Procedure to "today"
    NonNeoplasticResultFromSymptomaticProcedurePage(
        page
    ).enter_date_of_symptomatic_procedure(datetime.now())

    # And the Screening Interval is 24 months
    NonNeoplasticResultFromSymptomaticProcedurePage(page).assert_text_in_alert_textbox(
        expected_text="recall interval of 24 months"
    )

    # And I select test number 1
    NonNeoplasticResultFromSymptomaticProcedurePage(page).select_test_number(1)

    # And I save the Result from Symptomatic Procedure
    NonNeoplasticResultFromSymptomaticProcedurePage(page).click_save_button()

    # Then my subject has been updated as follows:
    criteria = {
        "which diagnostic test": "Latest not-void test in latest episode",
        "latest episode accumulated result": "Abnormal",
        "latest event status": "A373 Symptomatic result recorded",
        "symptomatic procedure date": "today",
        "symptomatic procedure result": "Non-neoplastic",
    }
    subject_assertion(nhs_no, criteria)

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # When I advance the subject's episode for "Return to FOBT after Symptomatic Referral"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(
        page
    ).click_return_to_fobt_after_symptomatic_referral_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {"latest event status": "A358 Return to FOBT after Symptomatic Referral"},
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I select the advance episode option for "Record Diagnosis Date"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
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
    }
    subject_assertion(nhs_no, criteria)

    # And there is a "A358" letter batch for my subject with the exact title "Return FOBT Letter after Referral to Symptomatic"
    # When I process the open "A358" letter batch for my subject
    batch_processing(page, "A358", "Return FOBT Letter after Referral to Symptomatic")

    # Then my subject has been updated as follows:
    criteria = {
        "which diagnostic test": "Latest not-void test in latest episode",
        "calculated fobt due date": "2 years from symptomatic procedure",
        "calculated lynch due date": "Null",
        "calculated surveillance due date": "Unchanged",
        "ceased confirmation date": "Null",
        "ceased confirmation details": "Null",
        "ceased confirmation user id": "Null",
        "clinical reason for cease": "Null",
        "latest episode accumulated result": "Abnormal",
        "latest episode recall calculation method": "Symptomatic procedure date",
        "latest episode recall episode type": "FOBT Screening",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Closed",
        "latest episode status reason": "Episode Complete",
        "latest event status": "A65 Abnormal",
        "lynch due date": "Null",
        "lynch due date reason": "Unchanged",
        "lynch due date date of change": "Unchanged",
        "screening due date": "Null",
        "screening due date date of change": "Today",
        "screening due date reason": "Awaiting failsafe",
        "screening status": "Recall",
        "surveillance due date": "Null",
        "surveillance due date date of change": "Unchanged",
        "surveillance due date reason": "Unchanged",
        "symptomatic procedure date": "Today",
        "symptomatic procedure result": "Non-neoplastic",
        "screening referral type": "Null",
    }
    subject_assertion(nhs_no, criteria)

    # When Comment:
    logging.info(
        "Now reopen the episode to re-record the symptomatic result, and this time refer for another diagnostic test"
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I reopen the subject's episode for "Reopen to Re-record Outcome from Symptomatic Referral"
    SubjectScreeningSummaryPage(page).click_reopen_fobt_screening_episode_button()
    ReopenFOBTScreeningEpisodePage(
        page
    ).click_reopen_to_rerecord_outcome_from_symptomatic_referral_button()

    # Then my subject has been updated as follows:
    criteria = {
        "which diagnostic test": "Latest not-void test in latest episode",
        "calculated fobt due date": "As at episode start",
        "calculated lynch due date": "Null",
        "calculated surveillance due date": "Unchanged",
        "ceased confirmation date": "Null",
        "ceased confirmation details": "Null",
        "ceased confirmation user id": "Null",
        "clinical reason for cease": "Null",
        "latest episode accumulated result": "No Result",
        "latest episode diagnosis date reason": "Null",
        "latest episode has diagnosis date": "Yes",
        "latest episode includes event code": "E372 Reopen to Re-record Outcome from Symptomatic Referral",
        "latest episode recall calculation method": "Symptomatic procedure date",
        "latest episode recall episode type": "Null",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Open",
        "latest episode status reason": "Null",
        "latest event status": "A372 Refer Symptomatic, GP Letter Printed",
        "screening due date": "Calculated FOBT Due Date",
        "screening due date date of change": "Today",
        "screening due date reason": "Reopened episode",
        "surveillance due date": "Null",
        "surveillance due date date of change": "Unchanged",
        "surveillance due date reason": "Unchanged",
        "symptomatic procedure date": "Null",
        "symptomatic procedure result": "Null",
        "screening referral type": "Null",
    }
    subject_assertion(nhs_no, criteria)

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # When I view the advance episode options
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # And I select the advance episode option for "Non-neoplastic and Other Non-bowel Cancer Result"
    AdvanceFOBTScreeningEpisodePage(
        page
    ).click_non_neoplastic_and_other_non_bowel_cancer_result_button()

    # And I set the Date of Symptomatic Procedure to "today"
    NonNeoplasticResultFromSymptomaticProcedurePage(
        page
    ).enter_date_of_symptomatic_procedure(datetime.now())

    # And the Screening Interval is 24 months
    NonNeoplasticResultFromSymptomaticProcedurePage(page).assert_text_in_alert_textbox(
        "recall interval of 24 months"
    )

    # And I select test number 1
    NonNeoplasticResultFromSymptomaticProcedurePage(page).select_test_number(1)

    # And I save the Result from Symptomatic Procedure
    NonNeoplasticResultFromSymptomaticProcedurePage(page).click_save_button()

    # Then my subject has been updated as follows:
    criteria = {
        "which diagnostic test": "Latest not-void test in latest episode",
        "latest episode accumulated result": "Abnormal",
        "latest event status": "A373 Symptomatic result recorded",
        "symptomatic procedure date": "Today",
        "symptomatic procedure result": "Non-neoplastic",
    }
    subject_assertion(nhs_no, criteria)

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # When I select the advance episode option for "Refer Another Diagnostic Test after return from Symptomatic Referral"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(
        page
    ).click_refer_another_diagnostic_test_after_return_from_symptomatic_referral_button()

    # And I select Referral Type of "Radiological" for the Diagnostic Test Referral Following Symptomatic Procedure
    ReturnFromSymptomaticReferralPage(
        page
    ).select_radiological_or_endoscopic_referral_option("Radiological")

    # And I select Reason for Onward Referral of "Further Clinical Assessment" for the Diagnostic Test Referral Following Symptomatic Procedure
    ReturnFromSymptomaticReferralPage(page).select_reason_for_onward_referral_option(
        "Further Clinical Assessment"
    )

    # And I save the Diagnostic Test Referral Following Symptomatic Procedure
    ReturnFromSymptomaticReferralPage(page).click_save_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A389 Refer Another Diagnostic Test after return from Symptomatic Referral"
        },
    )

    # When Comment:
    logging.info(
        "Temporary pathway until the Return from Symptomatic Referral - Refer Another Diagnostic Test screen is built in BCSS-16246"
    )

    # When I advance the subject's episode for "Other Post-investigation Contact Required"
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_other_post_investigation_button()

    # Then my subject has been updated as follows:
    criteria = {
        "latest event status": "A361 Other Post-investigation Contact Required",
    }
    subject_assertion(nhs_no, criteria)

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # When I select the advance episode option for "Record other post-investigation contact"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(
        page
    ).click_record_other_post_investigation_contact_button()

    # And I record contact with the subject with outcome "Post-investigation Appointment Not Required"
    ContactWithPatientPage(page).record_post_investigation_appointment_not_required()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest episode includes event status": "A323 Post-investigation Appointment NOT Required",
        },
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest episode includes event status": "A317 Post-investigation Contact Made",
            "latest event status": "A319 Refer follow-up test after return from symptomatic referral letter (Patient & GP)",
        },
    )

    # And there is a "A319" letter batch for my subject with the exact title "Result Letters - Refer another test after symptomatic referral"
    # When I process the open "A319" letter batch for my subject
    # Then my subject has been updated as follows:
    batch_processing(
        page=page,
        batch_type="A319",
        batch_description="Result Letters - Refer another test after symptomatic referral",
        latest_event_status="A395 - Refer Another Diagnostic Test",
    )

    LogoutPage(page).log_out()
