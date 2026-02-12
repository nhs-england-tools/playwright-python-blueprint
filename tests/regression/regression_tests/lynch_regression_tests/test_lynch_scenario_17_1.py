import logging
import pytest
from datetime import datetime, timedelta
from playwright.sync_api import Page
from classes.repositories.episode_repository import EpisodeRepository
from classes.repositories.general_repository import GeneralRepository
from pages.base_page import BasePage
from pages.datasets.colonoscopy_dataset_page import (
    ColonoscopyDatasetsPage,
    FitForColonoscopySspOptions,
)
from pages.datasets.investigation_dataset_page import (
    BowelPreparationQualityOptions,
    ComfortOptions,
    CompletionProofOptions,
    DrugTypeOptions,
    EndoscopyLocationOptions,
    FailureReasonsOptions,
    InsufflationOptions,
    InvestigationDatasetsPage,
    LateOutcomeOptions,
    OutcomeAtTimeOfProcedureOptions,
    PolypAccessOptions,
    PolypClassificationOptions,
    PolypReasonLeftInSituOptions,
    YesNoOptions,
)
from pages.datasets.subject_datasets_page import SubjectDatasetsPage
from pages.logout.log_out_page import LogoutPage
from pages.screening_practitioner_appointments.appointment_detail_page import (
    AppointmentDetailPage,
)
from pages.screening_subject_search.advance_lynch_surveillance_episode_page import (
    AdvanceLynchSurveillanceEpisodePage,
)
from pages.screening_subject_search.attend_diagnostic_test_page import (
    AttendDiagnosticTestPage,
)
from pages.screening_subject_search.contact_with_patient_page import (
    ContactWithPatientPage,
)
from pages.screening_subject_search.diagnostic_test_outcome_page import (
    DiagnosticTestOutcomePage,
    OutcomeOfDiagnosticTest,
    ReasonForSymptomaticReferral,
)
from pages.screening_subject_search.episode_events_and_notes_page import (
    EpisodeEventsAndNotesPage,
)
from pages.screening_subject_search.high_risk_findings_result_from_symptomatic_procedure_page import (
    HighRiskFindingsResultFromSymptomaticProcedure,
)
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from utils import screening_subject_page_searcher
from utils.appointments import book_appointments
from utils.batch_processing import batch_processing
from utils.calendar_picker import CalendarPicker
from utils.investigation_dataset import InvestigationDatasetCompletion
from utils.lynch_utils import LynchUtils
from utils.oracle.oracle import OracleDB
from utils.subject_assertion import subject_assertion
from utils.user_tools import UserTools


@pytest.mark.usefixtures("setup_org_and_appointments")
@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.lynch_regression_tests
def test_lynch_scenario_17_1(page: Page) -> None:
    """
    Scenario: : 17.1 - High-risk findings result from symptomatic procedure - self referral

    G4-G2-G3-A183-A25-J10-A99-A59-A259-A361-A323-A317-A353-A372-A373-A377-A158-Lynch over age [SSCL53d]

    In this scenario, the subject is referred for a symptomatic procedure following a diagnostic test which a result of Abnormal.  The result of the symptomatic procedure is High-risk findings.

    Subject summary:

    > Process Lynch diagnosis for a new over-age subject suitable for immediate self-referral
    > Self refer the subject
    > Run Lynch invitations > G4 (5.1)
    > Process G4 letter batch > G2 (5.1)
    > Run timed events > G3 (5.1)
    > Book appointment > A183 (1.11)
    > Process A183 letter batch > A25 (1.11)
    > Attend appointment > J10 (1.12)
    > Suitable for Endoscopic Test > A99 (2.1)
    > Invite for Diagnostic Test > A59 (2.1)
    > Attend test > A259 (2.1)
    > Abnormal > A315 (2.1)
    > Other Post-investigation Contact Required > A361 (2.1)
    > Post-investigation Appointment Not Required > A317 (2.1)
    > MDT Referral Not Required > A353 (2.6)
    > Process A353 letter batch > A372 (2.7)
    > High-risk findings Result from Symptomatic Procedure > A373 (2.7)
    > Refer Lynch > A377 (2.7)
    > Process A377 letter batch > A158 (2.1)
    > Check recall [SSCL53d]
    """
    # Given I log in to BCSS "England" as user role "Hub Manager"
    user_role = UserTools.user_login(
        page, "Hub Manager State Registered at BCS01", return_role_type=True
    )
    if user_role is None:
        raise ValueError("User cannot be assigned to a UserRoleType")

    # When I receive Lynch diagnosis "MSH6" for a new subject in my hub aged "75" with diagnosis date "3 years ago" and last colonoscopy date "2 years ago"
    nhs_no = LynchUtils(page).insert_validated_lynch_patient_from_new_subject_with_age(
        age="75",
        gene="MSH6",
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
            "Subject lower lynch age": "35",
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
            "subject lower lynch age": "35",
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

    logging.info("Progress the episode through the required pathway to closure")

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

    # And I attend the subject's practitioner appointment "yesterday"
    AppointmentDetailPage(page).mark_appointment_as_attended(
        datetime.today() - timedelta(days=1)
    )

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

    # And I view the advance episode options
    SubjectScreeningSummaryPage(page).click_advance_lynch_surveillance_episode_button()

    # And I select Diagnostic Test Type "Colonoscopy"
    AdvanceLynchSurveillanceEpisodePage(page).select_test_type_dropdown_option(
        "Colonoscopy"
    )

    # And I enter a Diagnostic Test First Offered Appointment Date of "today"
    AdvanceLynchSurveillanceEpisodePage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())

    # And I advance the subject's episode for "Invite for Diagnostic Test >>"
    AdvanceLynchSurveillanceEpisodePage(page).click_invite_for_diagnostic_test_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "which diagnostic test": "Latest test in latest episode",
            "diagnostic test proposed type": "Colonoscopy",
            "diagnostic test confirmed type": "Null",
            "diagnostic test intended extent": "Null",
            "latest event status": "A59 Invited for Diagnostic Test",
        },
    )

    # When I select the advance episode option for "Attend Diagnostic Test"
    AdvanceLynchSurveillanceEpisodePage(page).click_attend_diagnostic_test_button()

    # Then I confirm the value of the diagnostic test attendance field "Proposed Type of Test" is "Colonoscopy"
    AttendDiagnosticTestPage(page).confirm_proposed_type_of_test(
        "Proposed Type of Test", "Colonoscopy"
    )

    # And I confirm the value of the diagnostic test attendance field "Actual Type of Test" is "Colonoscopy"
    AttendDiagnosticTestPage(page).confirm_proposed_type_of_test(
        "Actual Type of Test", "Colonoscopy"
    )

    # When I attend the subject's diagnostic test
    AttendDiagnosticTestPage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())
    AttendDiagnosticTestPage(page).click_save_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "which diagnostic test": "Latest test in latest episode",
            "diagnostic test proposed type": "Colonoscopy",
            "diagnostic test confirmed type": "Colonoscopy",
            "diagnostic test intended extent": "Null",
            "latest event status": "A259 Attended Diagnostic Test",
        },
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I edit the Investigation Dataset for this subject
    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    # Confirm on the investigation Datasets Page
    InvestigationDatasetsPage(page).bowel_cancer_screening_page_title_contains_text(
        "Investigation Datasets"
    )

    # Then message "WARNING - Resect & Discard is not appropriate for a Lynch patient." is displayed at the top of the investigation dataset
    InvestigationDatasetsPage(page).message_is_displayed(
        "WARNING - Resect & Discard is not appropriate for a Lynch patient."
    )

    # And I open all minimized sections on the dataset
    InvestigationDatasetsPage(page).open_all_minimized_sections()

    # When I set the following fields and values within the "Investigation Dataset" section of the investigation dataset:
    InvestigationDatasetCompletion(page).fill_out_general_information(
        {
            "practitioner": 1,
            "site": 1,
            "testing clinician": 1,
            "aspirant endoscopist": None,
        }
    )

    # And I add the following "Bowel Preparation Administered" drugs and doses within the Investigation Dataset for this subject:
    InvestigationDatasetCompletion(page).fill_out_drug_information(
        {
            "drug_dose1": "3",
            "drug_type1": DrugTypeOptions.MANNITOL,
        }
    )

    # And I set the following fields and values within the "Endoscopy Information" section of the investigation dataset:
    InvestigationDatasetCompletion(page).fill_endoscopy_information(
        {
            "endoscope inserted": "yes",
            "procedure type": "diagnostic",
            "bowel preparation quality": BowelPreparationQualityOptions.GOOD,
            "comfort during recovery": ComfortOptions.NO_DISCOMFORT,
            "comfort during examination": ComfortOptions.NO_DISCOMFORT,
            "endoscopist defined extent": EndoscopyLocationOptions.CAECUM,
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
    )

    InvestigationDatasetCompletion(page).fill_out_completion_information(
        {"completion proof": CompletionProofOptions.VIDEO_APPENDIX}
    )

    InvestigationDatasetCompletion(page).fill_out_failure_information(
        {"failure reasons": FailureReasonsOptions.NO_FAILURE_REASONS}
    )

    # When I add new polyp 1 with the following fields and values within the Investigation Dataset for this subject:
    InvestigationDatasetCompletion(page).fill_polyp_x_information(
        {
            "location": EndoscopyLocationOptions.CAECUM,
            "classification": PolypClassificationOptions.LST_NG,
            "estimate of whole polyp size": "20",
            "polyp access": PolypAccessOptions.EASY,
            "reason left in situ": PolypReasonLeftInSituOptions.DIAGNOSTIC_PROCEDURE,
        },
        1,
    )

    # And I mark the Investigation Dataset as completed
    InvestigationDatasetsPage(page).check_dataset_complete_checkbox()

    # Then the Investigation Dataset result message, which I will cancel, is "Abnormal, procedure incomplete"
    InvestigationDatasetsPage(page).click_save_dataset_button_assert_dialog(
        "Abnormal, procedure incomplete"
    )

    # And I press the save Investigation Dataset button
    InvestigationDatasetsPage(page).click_save_dataset_button()

    # Then I confirm the Episode Result is "Abnormal"
    EpisodeRepository().confirm_episode_result(nhs_no, "Abnormal")

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I select the advance episode option for "Enter Diagnostic Test Outcome"
    SubjectScreeningSummaryPage(page).click_advance_lynch_surveillance_episode_button()
    AdvanceLynchSurveillanceEpisodePage(
        page
    ).click_enter_diagnostic_test_outcome_button()

    # Then I confirm the Outcome Of Diagnostic Test dropdown has the following options:
    DiagnosticTestOutcomePage(page).test_outcome_dropdown_contains_options(
        [
            "Refer Another Diagnostic Test",
            "Refer Symptomatic",
        ],
    )

    # When I select Outcome of "Refer Symptomatic"
    DiagnosticTestOutcomePage(page).select_test_outcome_option(
        OutcomeOfDiagnosticTest.REFER_SYMPTOMATIC
    )

    # Then the text "Diagnostic Test Date resulting in a recall due date" is not visible
    DiagnosticTestOutcomePage(page).text_is_visible(
        "Diagnostic Test Date resulting in a recall due date", False
    )

    # When I select Reason for Symptomatic Referral value "Suspected Cancer Surgery"
    DiagnosticTestOutcomePage(page).select_reason_for_symptomatic_referral_option(
        ReasonForSymptomaticReferral.SUSPECTED_CANCER_SURGERY
    )
    # And I save the Diagnostic Test Outcome
    DiagnosticTestOutcomePage(page).click_save_button()

    # When I advance the subject's episode for "Other Post-investigation Contact Required"
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    SubjectScreeningSummaryPage(page).click_advance_lynch_surveillance_episode_button()
    AdvanceLynchSurveillanceEpisodePage(
        page
    ).click_other_post_investigation_contact_required_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A361 Other Post-investigation Contact Required",
        },
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I select the advance episode option for "Record other post-investigation contact"
    SubjectScreeningSummaryPage(page).click_advance_lynch_surveillance_episode_button()
    AdvanceLynchSurveillanceEpisodePage(
        page
    ).click_record_other_post_investigation_contact_button()

    # Then I confirm the Contact with Patient page is displayed
    ContactWithPatientPage(page).verify_contact_with_patient_page_is_displayed()

    # Then I confirm the patient outcome dropdown has the following options:
    ContactWithPatientPage(page).patient_outcome_dropdown_contains_options(
        [
            "Post-investigation Appointment Not Required",
            "Post-investigation Appointment Required",
            "No outcome",
        ]
    )

    # When I record contact with the subject with outcome "Post-investigation Appointment Not Required"
    ContactWithPatientPage(page).record_post_investigation_appointment_not_required()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest episode includes event status": "A323 Post-investigation Appointment NOT Required",
            "latest event status": "A317 Post-investigation Contact Made",
        },
    )

    # When I view the advance episode options
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    SubjectScreeningSummaryPage(page).click_advance_lynch_surveillance_episode_button()

    # And I advance the subject's episode for "MDT Referral Not Required"
    AdvanceLynchSurveillanceEpisodePage(page).click_mdt_referral_not_required_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A353 MDT Referral Not Required",
        },
    )

    # And there is a "A353" letter batch for my subject with the exact title "GP Letter Indicating Referral to Symptomatic (Lynch)"
    # When I process the open "A353" letter batch for my subject
    batch_processing(
        page, "A353", "GP Letter Indicating Referral to Symptomatic (Lynch)"
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A372 Refer Symptomatic, GP Letter Printed",
        },
    )

    # When I view the advance episode options
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    SubjectScreeningSummaryPage(page).click_advance_lynch_surveillance_episode_button()

    # Then I "can" advance the subject's episode for "High-risk findings Result from Symptomatic Procedure"
    AdvanceLynchSurveillanceEpisodePage(page).can_advance_episode(
        "High-risk findings Result from Symptomatic Procedure", True
    )

    # When I select the advance episode option for "High-risk findings Result from Symptomatic Procedure"
    AdvanceLynchSurveillanceEpisodePage(
        page
    ).click_high_risk_findings_result_from_symptomatic_procedure_button()

    # And I set the Date of Symptomatic Procedure to "yesterday"
    HighRiskFindingsResultFromSymptomaticProcedure(
        page
    ).enter_date_of_symptomatic_procedure(datetime.today() - timedelta(days=1))

    # Then the Screening Interval is 24 months
    HighRiskFindingsResultFromSymptomaticProcedure(page).assert_text_in_alert_textbox(
        "recall interval of 24 months"
    )

    # When I select test number 2
    HighRiskFindingsResultFromSymptomaticProcedure(page).select_test_number(2)

    # And I save the Result from Symptomatic Procedure
    HighRiskFindingsResultFromSymptomaticProcedure(page).click_save_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "which diagnostic test": "Latest not-void test in latest episode",
            "latest episode accumulated result": "High-risk findings",
            "latest event status": "A373 Symptomatic result recorded",
            "symptomatic procedure date": "Yesterday",
            "symptomatic procedure result": "High-risk findings",
        },
    )

    # When I advance the subject's episode for "Return to Lynch after symptomatic referral"
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    SubjectScreeningSummaryPage(page).click_advance_lynch_surveillance_episode_button()
    AdvanceLynchSurveillanceEpisodePage(
        page
    ).click_return_to_lynch_after_symptomatic_referral_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A377 Return to Lynch after symptomatic referral",
        },
    )

    # And there is a "A377" letter batch for my subject with the exact title "Return to Lynch after symptomatic referral"
    # When I process the open "A377" letter batch for my subject
    batch_processing(page, "A377", "Return to Lynch after symptomatic referral")

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "Which diagnostic test": "Latest not-void test in latest episode",
            "Calculated FOBT Due Date": "Null",
            "Calculated Lynch Due Date": "2 years from Symptomatic Procedure",
            "Calculated Surveillance Due Date": "Null",
            "Ceased confirmation date": "Today",
            "Ceased confirmation details": "Outside screening population at recall.",
            "Ceased confirmation user ID": "User's ID",
            "Clinical reason for cease": "Null",
            "Latest episode recall calculation method": "Symptomatic Procedure date",
            "Latest episode recall episode type": "Lynch Surveillance",
            "Latest episode recall surveillance type": "Null",
            "Latest episode status": "Closed",
            "Latest episode status reason": "Episode Complete",
            "Latest event status": "A158 High-risk findings",
            "Lynch due date": "Null",
            "Lynch due date date of change": "Today",
            "Lynch due date reason": "Ceased",
            "Previous screening status": "Lynch Self-referral",
            "Screening due date": "Null",
            "Screening due date date of change": "Unchanged",
            "Screening due date reason": "Unchanged",
            "Screening referral type": "Null",
            "Screening status": "Ceased",
            "Screening status date of change": "Today",
            "Screening status reason": "Outside Screening Population",
            "Surveillance due date": "Null",
            "Surveillance due date reason": "Unchanged",
            "Surveillance due date date of change": "Unchanged",
            "Symptomatic procedure date": "Yesterday",
            "Symptomatic procedure result": "High-risk findings",
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
