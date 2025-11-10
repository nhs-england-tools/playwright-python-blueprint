from socket import TCP_NODELAY
from pypdf import PageRange
import pytest
import logging
from datetime import datetime, timedelta
from playwright.sync_api import Page
from classes.subject import subject
from classes.subject.subject import Subject
from classes.user.user import User
from pages.screening_subject_search import refer_to_mdt_page
from pages.screening_subject_search.non_neoplastic_result_from_symptomatic_procedure_page import NonNeoplasticResultFromSymptomaticProcedurePage
from utils.calendar_picker import CalendarPicker
from utils.user_tools import UserTools
from utils.subject_assertion import subject_assertion
from utils import screening_subject_page_searcher
from utils.batch_processing import batch_processing,assert_batch_present_in_active_list,assert_batch_not_present_in_active_list
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
    ReasonForSymptomaticReferral,
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
    SerratedLesionSubTypeOptions,
    YesNoOptions,
    EndoscopyLocationOptions,
    CompletionProofOptions,
    PolypAccessOptions,
    PolypClassificationOptions,
    PolypInterventionDeviceOptions,
    PolypInterventionExcisionTechniqueOptions,
    PolypInterventionModalityOptions,
    PolypInterventionRetrievedOptions,
    PolypTypeOptions,
    AdenomaSubTypeOptions,
    PolypExcisionCompleteOptions,
    PolypDysplasiaOptions,
    YesNoUncertainOptions,
    ReasonPathologyLostOptions,
)
from pages.screening_subject_search.reopen_fobt_screening_episode_page import (
    ReopenFOBTScreeningEpisodePage,
)
from pages.screening_subject_search.contact_with_patient_page import (
    ContactWithPatientPage,
)
from pages.screening_subject_search.refer_to_mdt_page import(ReferToMdtPage)
from pages.screening_subject_search.lnpcp_result_from_symptomatic_procedure_page import (LnpcpResultFromSymptomaticProcedure)
from pages.screening_subject_search.handover_into_symptomatic_care_page import (HandoverIntoSymptomaticCarePage)
from classes.repositories.person_repository import PersonRepository
from classes.repositories.episode_repository import EpisodeRepository
from utils.sspi_change_steps import SSPIChangeSteps
from pages.organisations.organisations_page import OrganisationSwitchPage
from utils.call_and_recall_utils import CallAndRecallUtils
from utils.oracle.subject_creation_util import CreateSubjectSteps


@pytest.mark.wip
@pytest.mark.usefixtures("setup_org_and_appointments")
# @pytest.mark.vpn_required
# @pytest.mark.regression
# @pytest.mark.fobt_regression_tests


def test_scenario_14(page: Page) -> None:
    """
        Scenario: 14: LNPCP result from symptomatic procedure

        S9-S10-S43-A8-A183-(A50)-A25-J10-A99-A59-A259-A315-A360-A410-A415-A416-A316-A348-(A167)-A372-A373-A374-A157-A394-A385-A382-A383-C203 [SSCL25d] A372-A373-A374-A372-A373-A374-A157-C203 [SSCL52a]

        This scenario tests progression of an FOBT episode to closure with an episode result of LNPCP, having a diagnostic test result of High-risk findings, and a symptomatic procedure result of LNPCP.  It checks that the reopen to re-record the symptomatic result downgrades the episode result to High-risk findings.  This scenario also tests that closure on LNPCP for an in-age subject refers them to Surveillance, while an over-age subject is discharged, even if (because FOBT recall is 2 years and Surveillance recall is 3 years) they would be in-age for FOBT screening.  When the subject's age is changed to 72 by the SSPI update, this makes today their 72nd birthday.  Because recall is based on the date of their symptomatic procedure (yesterday), this calculates their surveillance due date as the day before their 75th birthday, when they are still in the age range.  The first closure uses the diagnostic test date as the basis for recall, while the second closure uses the symptomatic procedure date.

        Note that ceased confirmation details come from the Handover into Symptomatic Care form.

        Scenario summary:

    > Find an in-age subject at S9 whose episode started recently before today (1.1)
    > SSPI update changes subject to over-age
    > Run timed events > creates S9 letter (1.1)
    > Process S9 letter batch > S10 (1.1)
    > Log kit > S43 (1.2)
    > Read kit with ABNORMAL result > A8 (1.3)
    > Invite for colonoscopy assessment > A183 (1.11)
    > Record diagnosis date (A50)
    > Process A183 appointment letter > A25 (1.11)
    > Attend assessment appointment > J10 (1.11)
    > Suitable for colonoscopy > A99 (1.12)
    > Invite for diagnostic test > A59 (2.1)
    > Attend diagnostic test > A259 (2.1)
    > Complete investigation dataset – High-risk findings (2.1)
    > Enter diagnostic test outcome – refer symptomatic > A315 (2.1)
    > Post-investigation appointment required > A360 (2.1)
    > Book post-investigation appointment > A410 (2.4)
    > Process A410 letter batch > A415 (2.4)
    > Attend post-investigation appointment > A416 > A316 (2.4)
    > MDT required - record MDT > A348 (2.6)
    > Process A183 result letter (A167) (1.11)
    > Process A348 letter batch > A372 (2.6)
    > Record symptomatic result – LNPCP > A373 (2.7)
    > Refer Surveillance > A374 (2.7)
    > Process A374 letter batch > A157 (2.7) > A394 (2.8)
    > Handover to GP practice > A385 (1.14)
    > Process A385 letter batch > A382 (1.14)
    > Process A382 letter batch > A383 > C203 (1.14)
    > Check recall [SSCL25d]
    > Reopen to re-record symptomatic result > A372 (2.7)
    > SSPI update changes subject to in-age
    > Record symptomatic result - Non-neoplastic > A373 (2.7)
    > Refer Surveillance > A374 (2.7)
    > Redirect to re-record symptomatic result > A372 (2.7)
    > Record symptomatic result - LNPCP > A373 (2.7)
    > Refer Surveillance > A374 (2.7)
    > Process A374 letter batch > A157 (2.7) > C203 (2.8, 1.13)
    > Check recall [SSCL52a]
    """
    # # Given I log in to BCSS "England" as user role "Hub Manager"
    # user_role = UserTools.user_login(
    #     page, "Hub Manager at BCS01", return_role_type=True
    # )
    # if user_role is None:
    #     raise ValueError("This user cannot be assigned to a UserRoleType")

    # # And there is a subject who meets the following criteria:
    # criteria = {
    #     "latest event status": "S9 Pre-Invitation Sent",
    #     "latest episode kit class": "FIT",
    #     "latest episode started": "Within the last 6 months",
    #     "latest episode type": "FOBT",
    #     "subject age": "Between 60 and 72",
    #     "subject has unprocessed sspi updates": "No",
    #     "subject has user dob updates": "No",
    #     "subject hub code": "User's hub",
    # }

    # user = User().from_user_role_type(user_role)

    # query, bind_vars = SubjectSelectionQueryBuilder().build_subject_selection_query(
    #     criteria=criteria,
    #     user=user,
    #     subject=Subject(),
    #     subjects_to_retrieve=1,
    # )

    # nhs_no_df = OracleDB().execute_query(query=query, parameters=bind_vars)
    # nhs_no = nhs_no_df["subject_nhs_number"].iloc[0]

    # # Then Comment: NHS number
    # logging.info(f"[SUBJECT RETRIEVAL] Retrieved subject's NHS number: {nhs_no}")

    user_role = UserTools.user_login(
        page, "Hub Manager at BCS01", return_role_type=True
    )
    nhs_no = "9832913438"

    # When I receive an SSPI update to change their date of birth to "77" years old
    SSPIChangeSteps().sspi_update_to_change_dob_received(nhs_no, 77)

    # # Then my subject has been updated as follows:
    # criteria = {"subject age": "77"}
    # subject_assertion(nhs_no, criteria)

    # # When I run Timed Events for my subject
    # OracleDB().exec_bcss_timed_events(nhs_number=nhs_no)

    # # Then there is a "S9" letter batch for my subject with the exact title "Invitation & Test Kit (FIT)"
    # # When I process the open "S9" letter batch for my subject
    # batch_processing(
    #     page=page,
    #     batch_type="S9",
    #     batch_description="Invitation & Test Kit (FIT)",
    #     latest_event_status="S10 - Invitation & Test Kit Sent",
    # )

    # # When I log my subject's latest unlogged FIT kit
    # fit_kit = FitKitGeneration().get_fit_kit_for_subject_sql(nhs_no, False, False)
    # FitKitLogged().log_fit_kits(page=page, fit_kit=fit_kit, sample_date=datetime.now())

    # # Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_no,
    #     {"latest event status": "S43 Kit Returned and Logged (Initial Test)"},
    # )

    # # When I read my subject's latest logged FIT kit as "ABNORMAL"
    # FitKitLogged().read_latest_logged_kit(
    #     user=user_role, kit_type=2, kit=fit_kit, kit_result="ABNORMAL"
    # )

    # # Then my subject has been updated as follows:
    # subject_assertion(nhs_no, {"latest event status": "A8 Abnormal"})

    # # When I view the subject
    # screening_subject_page_searcher.navigate_to_subject_summary_page(
    #     page=page, nhs_no=nhs_no
    # )

    # # And I choose to book a practitioner clinic for my subject
    # SubjectScreeningSummaryPage(page).click_book_practitioner_clinic_button()

    # # And I select "BCS001" as the screening centre where the practitioner appointment will be held
    # # And I set the practitioner appointment date to "today"
    # # And I book the "earliest" available practitioner appointment on this date
    # book_appointments(
    #     page=page,
    #     screening_centre="BCS001 - Wolverhampton Bowel Cancer Screening Centre",
    #     site="The Royal Hospital (Wolverhampton)",
    # )

    # # Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_no,
    #     {
    #         "latest event status": "A183 1st Colonoscopy Assessment Appointment Requested"
    #     },
    # )

    # # And there is a "A183" letter batch for my subject with the exact title "Practitioner Clinic 1st Appointment"
    # assert_batch_present_in_active_list(
    #     page,
    #     batch_type="A183",
    #     batch_description="Practitioner Clinic 1st Appointment",
    # )
    # # And there is a "A183" letter batch for my subject with the exact title "GP Result (Abnormal)"
    # assert_batch_present_in_active_list(
    #     page,
    #     batch_type="A183",
    #     batch_description="GP Result (Abnormal)",
    # )
    # # And I view the subject
    # screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    # # And I view the advance episode options
    # SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    # # And I select the advance episode option for "Record Diagnosis Date"
    # AdvanceFOBTScreeningEpisodePage(page).click_record_diagnosis_date_button()
    # # And I enter a Diagnosis Date of "today"
    # RecordDiagnosisDatePage(page).enter_date_in_diagnosis_date_field(datetime.today())
    # # And I save Diagnosis Date Information
    # RecordDiagnosisDatePage(page).click_save_button()
    # # Then my subject has been updated as follows:
    # criteria = {
    #     "latest episode diagnosis date reason": "Null",
    #     "latest episode has diagnosis date": "Yes",
    #     "latest episode includes event status": "A50 Diagnosis date recorded",
    #     "latest event status": "A183 1st Colonoscopy Assessment Appointment Requested ",
    # }

    # # When I process the open "A183 - 1st Colonoscopy Assessment Appointment" letter batch for my subject
    # batch_processing(
    #     page,
    #     "A183",
    #     "Practitioner Clinic 1st Appointment",
    #     "A25 - 1st Colonoscopy Assessment Appointment Booked, letter sent",
    # )

    # # When I switch users to BCSS "England" as user role "Screening Centre Manager"
    # LogoutPage(page).log_out(close_page=False)
    # BasePage(page).go_to_log_in_page()
    # user_role = UserTools.user_login(page, "Screening Centre Manager at BCS001", True)
    # if user_role is None:
    #     raise ValueError("User role is none")

    # # And I view the subject
    # screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # # And I view the event history for the subject's latest episode
    # SubjectScreeningSummaryPage(page).expand_episodes_list()
    # SubjectScreeningSummaryPage(page).click_first_fobt_episode_link()

    # # And I view the latest practitioner appointment in the subject's episode
    # EpisodeEventsAndNotesPage(page).click_most_recent_view_appointment_link()

    # # And I attend the subject's practitioner appointment "2 days ago"
    # AppointmentDetailPage(page).mark_appointment_as_attended(
    #     datetime.today() - timedelta(days=2)
    # )

    # # Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_number=nhs_no,
    #     criteria={
    #         "latest event status": "J10 Attended Colonoscopy Assessment Appointment",
    #     },
    # )

    # # When I view the subject
    # screening_subject_page_searcher.navigate_to_subject_summary_page(
    #     page=page, nhs_no=nhs_no
    # )

    # # And I edit the Colonoscopy Assessment Dataset for this subject
    # SubjectScreeningSummaryPage(page).click_datasets_link()
    # SubjectDatasetsPage(page).click_colonoscopy_show_datasets()

    # # And I update the Colonoscopy Assessment Dataset with the following values:
    # ColonoscopyDatasetsPage(page).select_fit_for_colonoscopy_option(
    #     option=FitForColonoscopySspOptions.YES
    # )
    # ColonoscopyDatasetsPage(page).click_dataset_complete_radio_button_yes()

    # # And I save the Colonoscopy Assessment Dataset
    # ColonoscopyDatasetsPage(page).save_dataset()

    # # And I view the subject
    # screening_subject_page_searcher.navigate_to_subject_summary_page(
    #     page=page, nhs_no=nhs_no
    # )

    # # And I advance the subject's episode for "Suitable for Endoscopic Test"
    # SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    # AdvanceFOBTScreeningEpisodePage(page).click_suitable_for_endoscopic_test_button()

    # # Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_number=nhs_no,
    #     criteria={"latest event status": "A99 Suitable for Endoscopic Test"},
    # )

    # # When I view the subject
    # screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # # And I view the advance episode options
    # SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    # # And I select Diagnostic Test Type
    # AdvanceFOBTScreeningEpisodePage(page).select_test_type_dropdown_option(
    #     "Colonoscopy"
    # )
    # # And I enter a Diagnostic Test First Offered Appointment Date of "today"
    # AdvanceFOBTScreeningEpisodePage(page).click_calendar_button()
    # CalendarPicker(page).v1_calender_picker(datetime.today())
    # # And I advance the subject's episode for "Invite for Diagnostic Test >>"
    # AdvanceFOBTScreeningEpisodePage(page).click_invite_for_diagnostic_test_button()
    # # Then my subject has been updated as follows:
    # AdvanceFOBTScreeningEpisodePage(page).verify_latest_event_status_value(
    #     latest_event_status="A59 - Invited for Diagnostic Test"
    # )
    # # And I select the advance episode option for "Attend Diagnostic Test"
    # screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    # SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    # AdvanceFOBTScreeningEpisodePage(page).click_attend_diagnostic_test_button()
    # # And I attend the subject's diagnostic test yesterday
    # AttendDiagnosticTestPage(page).click_calendar_button()
    # CalendarPicker(page).v1_calender_picker(datetime.today() - timedelta(days=1))
    # AttendDiagnosticTestPage(page).click_save_button()
    # # Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_number=nhs_no,
    #     criteria={
    #         "latest event status": "A259 Attended Diagnostic Test",
    #     },
    # )

    # # When I view the subject
    # screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # # And I edit the Investigation Dataset for this subject
    # SubjectScreeningSummaryPage(page).click_datasets_link()
    # SubjectDatasetsPage(page).click_investigation_show_datasets()

    # # And there is a clinician who meets the following criteria:
    # user = User.from_user_role_type(user_role)
    # criteria = {
    #     "Person has current role": "Accredited Screening Colonoscopist",
    #     "Person has current role in organisation": "User's SC",
    #     "Resect & Discard accreditation status": "None",
    # }
    # query = PersonRepository().build_person_selection_query(
    #     criteria=criteria, person=None, required_person_count=1, user=user, subject=None
    # )
    # logging.info(f"Final query: {query}")
    # df = OracleDB().execute_query(query)
    # person_name = (
    #     f"{df["person_family_name"].iloc[0]} {df["person_given_name"].iloc[0]}"
    # )

    # # And I add the following bowel preparation drugs and values within the Investigation Dataset for this subject:
    # drug_information = {"drug_type1": DrugTypeOptions.MANNITOL, "drug_dose1": "3"}

    # # And I set the following fields and values within the Investigation Dataset for this subject:
    # general_information = {
    #     "site": 1,
    #     "practitioner": 1,
    #     "testing clinician": person_name,
    #     "aspirant endoscopist": None,
    # }
    # endoscopy_information = {
    #     "endoscope inserted": "yes",
    #     "procedure type": "therapeutic",
    #     "bowel preparation quality": BowelPreparationQualityOptions.GOOD,
    #     "comfort during examination": ComfortOptions.NO_DISCOMFORT,
    #     "comfort during recovery": ComfortOptions.NO_DISCOMFORT,
    #     "endoscopist defined extent": EndoscopyLocationOptions.APPENDIX,
    #     "scope imager used": YesNoOptions.YES,
    #     "retroverted view": YesNoOptions.NO,
    #     "start of intubation time": "09:00",
    #     "start of extubation time": "09:30",
    #     "end time of procedure": "10:00",
    #     "scope id": "Autotest",
    #     "insufflation": InsufflationOptions.AIR,
    #     "outcome at time of procedure": OutcomeAtTimeOfProcedureOptions.LEAVE_DEPARTMENT,
    #     "late outcome": LateOutcomeOptions.NO_COMPLICATIONS,
    # }

    # # And I set the following completion proof values within the Investigation Dataset for this subject:
    # completion_information = {"completion proof": CompletionProofOptions.VIDEO_APPENDIX}

    # # And I set the following failure reasons within the Investigation Dataset for this subject:
    # failure_information = {"failure reasons": FailureReasonsOptions.ADHESION}

    # # And I add new polyp 1 with the following fields and values within the Investigation Dataset for this subject:
    # # And I add new polyp 2 with the following fields and values within the Investigation Dataset for this subject:
    # # And I add new polyp 3 with the following fields and values within the Investigation Dataset for this subject:
    # # And I add new polyp 4 with the following fields and values within the Investigation Dataset for this subject:
    # # And I add new polyp 5 with the following fields and values within the Investigation Dataset for this subject:
    # polyp_information = [
    #     {
    #         "location": EndoscopyLocationOptions.CAECUM,
    #         "classification": PolypClassificationOptions.LST_NG,
    #         "estimate of whole polyp size": "10",
    #         "polyp access": PolypAccessOptions.EASY,
    #         "left in situ": YesNoOptions.NO,
    #     },
    #     {
    #         "location": EndoscopyLocationOptions.ASCENDING_COLON,
    #         "classification": PolypClassificationOptions.IIA,
    #         "estimate of whole polyp size": "8",
    #         "polyp access": PolypAccessOptions.EASY,
    #         "left in situ": YesNoOptions.NO,
    #     },
    #     {
    #         "location": EndoscopyLocationOptions.HEPATIC_FLEXURE,
    #         "classification": PolypClassificationOptions.IIB,
    #         "estimate of whole polyp size": "9",
    #         "polyp access": PolypAccessOptions.EASY,
    #         "left in situ": YesNoOptions.NO,
    #     },
    #     {
    #         "location": EndoscopyLocationOptions.TRANSVERSE_COLON,
    #         "classification": PolypClassificationOptions.IIC,
    #         "estimate of whole polyp size": "7",
    #         "polyp access": PolypAccessOptions.EASY,
    #         "left in situ": YesNoOptions.NO,
    #     },
    #     {
    #         "location": EndoscopyLocationOptions.SPLENIC_FLEXURE,
    #         "classification": PolypClassificationOptions.LST_G,
    #         "estimate of whole polyp size": "8",
    #         "polyp access": PolypAccessOptions.EASY,
    #         "left in situ": YesNoOptions.NO,
    #     }
    # ]

    # # And I add intervention 1 for polyp 1 with the following fields and values within the Investigation Dataset for this subject:
    # # And I add intervention 1 for polyp 2 with the following fields and values within the Investigation Dataset for this subject:
    # # And I add intervention 1 for polyp 3 with the following fields and values within the Investigation Dataset for this subject:
    # # And I add intervention 1 for polyp 4 with the following fields and values within the Investigation Dataset for this subject:
    # # And I add intervention 1 for polyp 5 with the following fields and values within the Investigation Dataset for this subject:
    # polyp_intervention = [
    #     [
    #         {
    #             "modality": PolypInterventionModalityOptions.EMR,
    #             "device": PolypInterventionDeviceOptions.HOT_SNARE,
    #             "excised": YesNoOptions.YES,
    #             "retrieved": PolypInterventionRetrievedOptions.YES,
    #             "excision technique": PolypInterventionExcisionTechniqueOptions.EN_BLOC,
    #         }
    #     ],
    #     [
    #         {
    #             "modality": PolypInterventionModalityOptions.POLYPECTOMY,
    #             "device": PolypInterventionDeviceOptions.HOT_SNARE,
    #             "excised": YesNoOptions.YES,
    #             "retrieved": PolypInterventionRetrievedOptions.YES,
    #             "excision technique": PolypInterventionExcisionTechniqueOptions.PIECE_MEAL,
    #         }
    #     ],
    #     [
    #         {
    #             "modality": PolypInterventionModalityOptions.ESD,
    #             "device": PolypInterventionDeviceOptions.HOT_SNARE,
    #             "excised": YesNoOptions.YES,
    #             "retrieved": PolypInterventionRetrievedOptions.NO,
    #             "excision technique": PolypInterventionExcisionTechniqueOptions.EN_BLOC,
    #         }
    #     ],
    #     [
    #         {
    #             "modality": PolypInterventionModalityOptions.EMR,
    #             "device": PolypInterventionDeviceOptions.HOT_SNARE,
    #             "excised": YesNoOptions.YES,
    #             "retrieved": PolypInterventionRetrievedOptions.YES,
    #             "excision technique": PolypInterventionExcisionTechniqueOptions.PIECE_MEAL,
    #         }

    #     ],
    #     [
    #         {
    #             "modality": PolypInterventionModalityOptions.POLYPECTOMY,
    #             "device": PolypInterventionDeviceOptions.HOT_SNARE,
    #             "excised": YesNoOptions.YES,
    #             "retrieved": PolypInterventionRetrievedOptions.YES,
    #             "excision technique": PolypInterventionExcisionTechniqueOptions.EN_BLOC,
    #         }
    #     ]
    # ]

    # # And I update histology details for polyp 1 with the following fields and values within the Investigation Dataset for this subject:
    # # And I update histology details for polyp 2 with the following fields and values within the Investigation Dataset for this subject:
    # # And I update histology details for polyp 3 with the following fields and values within the Investigation Dataset for this subject:
    # # And I update histology details for polyp 4 with the following fields and values within the Investigation Dataset for this subject:
    # # And I update histology details for polyp 5 with the following fields and values within the Investigation Dataset for this subject:
    # polyp_histology = [
    #     {
    #         "date of receipt": datetime.today(),
    #         "date of reporting": datetime.today(),
    #         "pathology provider": 1,
    #         "pathologist": 1,
    #         "polyp type": PolypTypeOptions.SERRATED_LESION,
    #         "serrated lesion sub type": SerratedLesionSubTypeOptions.MIXED_POLYP,
    #         "polyp excision complete": PolypExcisionCompleteOptions.R1,
    #         "polyp size": "9",
    #         "polyp dysplasia": PolypDysplasiaOptions.NO_DYSPLASIA,
    #         "polyp carcinoma": YesNoUncertainOptions.NO,
    #     },
    #     {
    #         "date of receipt": datetime.today(),
    #         "date of reporting": datetime.today(),
    #         "pathology provider": 1,
    #         "pathologist": 1,
    #         "polyp type": PolypTypeOptions.SERRATED_LESION,
    #         "serrated lesion sub type": SerratedLesionSubTypeOptions.MIXED_POLYP,
    #         "polyp excision complete": PolypExcisionCompleteOptions.R1,
    #         "polyp size": "7",
    #         "polyp dysplasia": PolypDysplasiaOptions.NOT_REPORTED,
    #         "polyp carcinoma": YesNoUncertainOptions.NO,
    #     },
    #     {},
    #     {
    #         "date of receipt": datetime.today(),
    #         "date of reporting": datetime.today(),
    #         "pathology provider": 1,
    #         "pathologist": 1,
    #         "polyp type": PolypTypeOptions.SERRATED_LESION,
    #         "serrated lesion sub type": SerratedLesionSubTypeOptions.SESSILE_SERRATED_LESION,
    #         "polyp excision complete": PolypExcisionCompleteOptions.R1,
    #         "polyp size": "8",
    #         "polyp carcinoma": YesNoUncertainOptions.NO,
    #     },
    #     {
    #         "date of receipt": datetime.today(),
    #         "date of reporting": datetime.today(),
    #         "pathology provider": 1,
    #         "pathologist": 1,
    #         "polyp type": PolypTypeOptions.ADENOMA,
    #         "adenoma sub type": AdenomaSubTypeOptions.TUBULAR_ADENOMA,
    #         "polyp excision complete": PolypExcisionCompleteOptions.R1,
    #         "polyp size": "7",
    #         "polyp dysplasia": PolypDysplasiaOptions.LOW_GRADE_DYSPLASIA,
    #         "polyp carcinoma": YesNoUncertainOptions.NO,
    #     },
    # ]

    # # When I press the save Investigation Dataset button
    # InvestigationDatasetCompletion(page).complete_dataset_with_args(
    #     general_information=general_information,
    #     drug_information=drug_information,
    #     endoscopy_information=endoscopy_information,
    #     failure_information=failure_information,
    #     completion_information=completion_information,
    #     polyp_information=polyp_information,
    #     polyp_intervention=polyp_intervention,
    #     polyp_histology=polyp_histology,
    # )

    # # Then the Investigation Dataset result message, which I will cancel, is "High-risk findings"
    # InvestigationDatasetsPage(page).expect_text_to_be_visible("High-risk findings")

    # # Then I confirm the Polyp Algorithm Size for Polyp 1 is 9
    # InvestigationDatasetsPage(page).assert_polyp_algorithm_size(1, "9")

    # # And I confirm the Polyp Algorithm Size for Polyp 2 is 8
    # InvestigationDatasetsPage(page).assert_polyp_algorithm_size(2, "8")

    # # And I confirm the Polyp Algorithm Size for Polyp 3 is 9
    # InvestigationDatasetsPage(page).assert_polyp_algorithm_size(3, "9")

    # # And I confirm the Polyp Algorithm Size for Polyp 4 is 8
    # InvestigationDatasetsPage(page).assert_polyp_algorithm_size(4, "8")

    # # And I confirm the Polyp Algorithm Size for Polyp 5 is 7
    # InvestigationDatasetsPage(page).assert_polyp_algorithm_size(5, "7")

    # # And I confirm the Polyp Category for Polyp 1 is "Premalignant polyp"
    # InvestigationDatasetsPage(page).assert_polyp_category(1, "Premalignant polyp")

    # # And I confirm the Polyp Category for Polyp 2 is "Premalignant polyp"
    # InvestigationDatasetsPage(page).assert_polyp_category(2, "Premalignant polyp")

    # # And I confirm the Polyp Category for Polyp 3 is "Premalignant polyp"
    # InvestigationDatasetsPage(page).assert_polyp_category(3, "Premalignant polyp")

    # # And I confirm the Polyp Category for Polyp 4 is "Premalignant polyp"
    # InvestigationDatasetsPage(page).assert_polyp_category(4, "Premalignant polyp")

    # # And I confirm the Polyp Category for Polyp 5 is "Premalignant polyp"
    # InvestigationDatasetsPage(page).assert_polyp_category(5, "Premalignant polyp")

    # #  When I view the subject
    # screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # # And I advance the subject's episode for "Enter Diagnostic Test Outcome"
    # SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    # AdvanceFOBTScreeningEpisodePage(page).click_enter_diagnostic_test_outcome_button()
    # # And I select "Refer Symptomatic" as the diagnostic test outcome
    # DiagnosticTestOutcomePage(page).select_test_outcome_option(
    #     OutcomeOfDiagnosticTest.REFER_SYMPTOMATIC
    # )
    # # And I select Reason for Symptomatic Referral value "Corrective Surgery"
    # DiagnosticTestOutcomePage(page).select_reason_for_symptomatic_referral_option(
    #     ReasonForSymptomaticReferral.CORRECTIVE_SURGERY
    # )
    # # And I save the Diagnostic Test Outcome information
    # DiagnosticTestOutcomePage(page).click_save_button()
    # # Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_no,
    #     {
    #         "latest event status": "A315 Diagnostic Test Outcome Entered",
    #     },
    # )

    # # When I advance the subject's episode for "Post-investigation Appointment Required"
    # SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    # AdvanceFOBTScreeningEpisodePage(page).click_post_investigation_appointment_required_button()
    # #    Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_no,
    #     {
    #         "latest event status": "A360 Post-investigation Appointment Required",
    #     },
    # )
    # # When I view the subject
    # screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    # # And I choose to book a practitioner clinic for my subject
    # SubjectScreeningSummaryPage(page).click_book_practitioner_clinic_button()
    # #  And I set the practitioner appointment date to "today"
    # # And I book the "earliest" available practitioner appointment on this date
    # book_post_investigation_appointment(
    #     page, "The Royal Hospital (Wolverhampton)", 1
    # )
    # # Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_no,
    #     {
    #         "latest event status": "A410 Post-investigation Appointment Made",
    #     },
    # )
    # # And there is a "A410" letter batch for my subject with the exact title "Post-Investigation Appointment Invitation Letter"
    # # When I process the open "A410 - Post-Investigation Appointment Invitation Letter" letter batch for my subject
    # batch_processing(
    #     page,
    #     "A410",
    #     "Post-Investigation Appointment Invitation Letter",
    # )
    # # Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_no,
    #     {
    #         "latest event status": "A415 Post-investigation Appointment Invitation Letter Printed",
    #     },
    # )

    # #  When I view the subject
    # screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    # # And I view the event history for the subject's latest episode
    # SubjectScreeningSummaryPage(page).expand_episodes_list()
    # SubjectScreeningSummaryPage(page).click_first_fobt_episode_link()
    # # And I view the latest practitioner appointment in the subject's episode
    # EpisodeEventsAndNotesPage(page).click_most_recent_view_appointment_link()
    # # And I attend the subject's practitioner appointment "today"
    # AppointmentDetailPage(page).mark_appointment_as_attended(datetime.today())
    # # Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_number=nhs_no,
    #     criteria={
    #         "latest episode includes event status": "A416 Post-investigation Appointment Attended ",
    #         "latest event status": "A316 Post-investigation Appointment Attended ",
    #     },
    # )

    # #  When I view the subject
    # screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    # # When I select the advance episode option for "MDT Referral Required"
    # SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    # AdvanceFOBTScreeningEpisodePage(page).click_mdt_referral_required_button()
    # # # And I enter simple MDT information
    # ReferToMdtPage(page).enter_date_in_Mdt_discussion_date_field(datetime.today())
    # ReferToMdtPage(page).select_mdt_location_lookup(1)
    # ReferToMdtPage(page).click_record_MDT_appointment_button()
    # #  Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_no,
    #     {
    #         "latest event status": "A348 MDT Referral Required",
    #     },
    # )
    # # And there is a "A348" letter batch for my subject with the exact title "GP Letter Indicating Referral to MDT"
    # assert_batch_present_in_active_list(
    #     page=page,
    #     batch_type="A348",
    #     batch_description="GP Letter Indicating Referral to MDT",
    # )

    # # When I switch users to BCSS "England" as user role "Senior Screening Assistant"
    # LogoutPage(page).log_out(close_page=False)
    # BasePage(page).go_to_log_in_page()
    # user_role = UserTools.user_login(page, "Senior Screening Assistant at BCS01", True)

    # # And I process the open "A183 - GP Result (Abnormal)" letter batch for my subject
    # batch_processing(
    #     page,
    #     "A183",
    #     "GP Result (Abnormal)",
    # )
    # # Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_no,
    #     {
    #         "latest event status": "A348 MDT Referral Required",
    #         "latest episode includes event status": "A167 GP Abnormal FOBT Result Sent"
    #     }
    # )

    # # When I switch users to BCSS "England" as user role "Specialist Screening Practitioner"
    # LogoutPage(page).log_out(close_page=False)
    # BasePage(page).go_to_log_in_page()
    # user_role = UserTools.user_login(
    #     page, "Specialist Screening Practitioner at BCS009 & BCS001", True
    # )
    # OrganisationSwitchPage(page).select_organisation_by_id("BCS001")
    # OrganisationSwitchPage(page).click_continue()

    # # And I process the open "A348" letter batch for my subject
    # batch_processing(
    #     page,
    #     "A348",
    #     "GP Letter Indicating Referral to MDT",
    # )
    # # Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_no,
    #     {
    #         "latest event status": "A372 Refer Symptomatic, GP Letter Printed",
    #     },
    # )

    # # When I view the advance episode options
    # screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    # SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    # # And I select the advance episode option for "LNPCP Result from Symptomatic Procedure"
    # AdvanceFOBTScreeningEpisodePage(page).click_lnpcp_result_from_symptomatic_procedure_button()
    # # And I set  the Date of Symptomatic Procedure to "yesterday"
    # LnpcpResultFromSymptomaticProcedure(page).enter_date_of_symptomatic_procedure(datetime.today() - timedelta(days=1))

    # # And the Screening Interval is 36 months
    # LnpcpResultFromSymptomaticProcedure(page).assert_text_in_alert_textbox(
    #     "recall interval of 36 months"
    # )
    # # And I select test number 1
    # LnpcpResultFromSymptomaticProcedure(page).select_test_number(1)
    # # And I save the Result from Symptomatic Procedure
    # LnpcpResultFromSymptomaticProcedure(page).click_save_button()
    # # Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_no,
    #     {
    #         "Which diagnostic test": "Latest not-void test in latest episode",
    #         "Latest episode accumulated result": "LNPCP",
    #         "latest event status": "A373 Symptomatic result recorded",
    #         "Symptomatic procedure date": "Yesterday",
    #         "Symptomatic procedure result":"LNPCP",
    #     },
    # )

    # # When I advance the subject's episode for "Refer to Surveillance after Symptomatic Referral"
    # SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # AdvanceFOBTScreeningEpisodePage(
    #     page
    # ).click_refer_to_survelliance_after_symptomatic_referral_button()

    # # Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_no,
    #     {
    #         "latest event status": "A374 Refer to Surveillance after Symptomatic Referral",
    #     },
    # )

    # # And there is a "A374" letter batch for my subject with the exact title "Return Surveillance Letter after Referral to Symptomatic"
    # assert_batch_present_in_active_list(
    #         page=page,
    #         batch_type="A374",
    #         batch_description="Return Surveillance Letter after Referral to Symptomatic",
    #     )
    # # When I process the open "A374" letter batch for my subject
    # batch_processing(
    #         page,
    #         "A374",
    #         "Return Surveillance Letter after Referral to Symptomatic",
    #     )
    # subject_assertion(
    #         nhs_no,
    #         {
    #             "Latest episode includes event status": "A157 LNPCP  ",
    #             "latest event status": "A394 Handover into Symptomatic Care for Surveillance - Patient Age ",
    #         },
    #     )

    # # When I view the Subject
    # screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    # # And I select the advance episode option for "Handover into Symptomatic Care"
    # SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    # AdvanceFOBTScreeningEpisodePage(page).click_handover_into_symptomatic_care_button()

    # # And I fill in Handover into Symptomatic Care form with Referral to Patient's GP Practice
    # HandoverIntoSymptomaticCarePage(page).select_referral_dropdown_option(
    #     "Referral to Patient's GP Practice"
    # )
    # # HandoverIntoSymptomaticCarePage(page).click_calendar_button()
    # # CalendarPicker(page).v1_calender_picker(datetime.today())
    # # HandoverIntoSymptomaticCarePage(page).select_consultant("201")
    # HandoverIntoSymptomaticCarePage(page).fill_notes("Handover notes - refer to GP practice")
    # HandoverIntoSymptomaticCarePage(page).click_save_button()

    # subject_assertion(
    #     nhs_no,
    #     {
    #         "latest event status": "A385 Handover into Symptomatic Care",
    #     },
    # )

    # # And there is a "A385" letter batch for my subject with the exact title "Handover into Symptomatic Care Adenoma Surveillance, Age - GP Letter"
    # assert_batch_present_in_active_list(
    #     page=page,
    #     batch_type="A385",
    #     batch_description="Handover into Symptomatic Care Adenoma Surveillance, Age - GP Letter",
    # )
    # # When I process the open "A385" letter batch for my subject
    # batch_processing(
    #     page,
    #     "A385",
    #     "Handover into Symptomatic Care Adenoma Surveillance, Age - GP Letter",
    # )

    # subject_assertion(
    #     nhs_no,
    #     {
    #         "latest event status": "A382 Handover into Symptomatic Care - GP Letter Printed ",
    #     },
    # )
    # # And there is a "A382" letter batch for my subject with the exact title "Handover into Symptomatic Care Adenoma Surveillance - Patient Letter"
    # # When I process the open "A382" letter batch for my subject
    # batch_processing(
    #     page,
    #     "A382",
    #     "Handover into Symptomatic Care Adenoma Surveillance - Patient Letter",
    # )
    # subject_assertion(
    #     nhs_no,
    #     {
    #         "which diagnostic test": "Latest not-void test in latest episode",
    #         "calculated fobt due date": "2 years from diagnostic test",
    #         "calculated lynch due date": "Null",
    #         "calculated surveillance due date": "Unchanged",
    #         "ceased confirmation date": "Today",
    #         "ceased confirmation details": "Handover notes - refer to GP practice",
    #         "ceased confirmation user id": "User's ID",
    #         "clinical reason for cease": "Null",
    #         "latest episode recall calculation method": "Diagnostic test date",
    #         "latest episode recall episode type": "Surveillance - LNPCP",
    #         "latest episode recall surveillance type": "Null",
    #         "latest episode status": "Closed",
    #         "latest episode status reason": "Discharged from Screening into Symptomatic care",
    #         "latest event status": "A383 Handover into Symptomatic Care - Patient Letter Printed",
    #         "lynch due date": "Null",
    #         "lynch due date date of change": "Unchanged",
    #         "lynch due date reason": "Unchanged",
    #         "screening due date": "Null",
    #         "screening due date date of change": "Today",
    #         "screening due date reason": "Discharge from Screening - Age",
    #         "screening status": "Ceased",
    #         "screening status date of change": "Today",
    #         "screening status reason": "Outside Screening Population",
    #         "surveillance due date": "Null",
    #         "surveillance due date date of change": "Unchanged",
    #         "surveillance due date reason": "Unchanged",
    #         "symptomatic procedure date": "Yesterday",
    #         "symptomatic procedure result": "LNPCP",
    #         "screening referral type": "Null",
    #     },
    #     user_role
    # )

    # When I view the subject
    # screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    # # Then I "cannot" reopen the subject's episode
    # SubjectScreeningSummaryPage(page).assert_reopen_episode_button_not_visible()
    # # When I switch users to BCSS "England" as user role "Screening Centre Manager"
    # user_role = UserTools.user_login(page, "Screening Centre Manager at BCS001", True)
    # # And I view the subject
    # screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    # # And I reopen the subject's episode for "Reopen to Re-record Outcome from Symptomatic Referral"
    # SubjectScreeningSummaryPage(page).click_reopen_fobt_screening_episode_button()
    # ReopenFOBTScreeningEpisodePage(page).click_reopen_to_rerecord_outcome_from_symptomatic_referral_button()
    # subject_assertion(
    #     nhs_no,
    #     {
    #         "which diagnostic test": "Latest not-void test in latest episode",
    #         "calculated fobt due date": "As at episode start",
    #         "calculated lynch due date": "Null",
    #         "calculated surveillance due date": "Unchanged",
    #         "ceased confirmation date": "Null",
    #         "ceased confirmation details": "Null",
    #         "ceased confirmation user id": "Null",
    #         "clinical reason for cease": "Null",
    #         "latest episode accumulated result": "High-risk findings",
    #         "latest episode includes event code": "E372 Reopen to Re-record Outcome from Symptomatic Referral",
    #         "latest episode recall calculation method": "Diagnostic test date",
    #         "latest episode recall episode type": "Null",
    #         "latest episode recall surveillance type": "Null",
    #         "latest episode status": "Open",
    #         "latest episode status reason": "Null",
    #         "latest event status": "A372 Refer Symptomatic, GP Letter Printed",
    #         "screening due date": "Calculated FOBT due date",
    #         "screening due date date of change": "Today",
    #         "screening due date reason": "Reopened episode",
    #         "screening status": "NOT: Ceased",
    #         "screening status date of change": "Today",
    #         "screening status reason": "Reopened episode",
    #         "surveillance due date": "Null",
    #         "surveillance due date reason": "Unchanged",
    #         "surveillance due date date of change": "Unchanged",
    #         "symptomatic procedure date": "Null",
    #         "symptomatic procedure result": "Null",
    #         "screening referral type": "Null",
    #     },
    # )

    # # When I receive an SSPI update to change their date of birth to "72" years old
    # SSPIChangeSteps().sspi_update_to_change_dob_received(nhs_no, 72)
    # # Then my subject has been updated as follows:
    # subject_assertion(nhs_no, {"subject age": "72"})
    # # When I view the advance episode options
    # screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    # SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    # # And I select the advance episode option for "Non-neoplastic and Other Non-bowel Cancer Result"
    # AdvanceFOBTScreeningEpisodePage(page).click_non_neoplastic_and_other_non_bowel_cancer_result_button()
    # # And I set the Date of Symptomatic Procedure to "today"
    # NonNeoplasticResultFromSymptomaticProcedurePage(page).enter_date_of_symptomatic_procedure(datetime.today())
    # # And the Screening Interval is 36 months
    # NonNeoplasticResultFromSymptomaticProcedurePage(page).assert_text_in_alert_textbox(
    #     "recall interval of 36 months"
    # )
    # # And I select test number 1
    # NonNeoplasticResultFromSymptomaticProcedurePage(page).select_test_number(1)
    # # And I save the Result from Symptomatic Procedure
    # NonNeoplasticResultFromSymptomaticProcedurePage(page).click_save_button()
    # # Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_no,
    #     {
    #         "which diagnostic test": "Latest not-void test in latest episode",
    #         "latest episode accumulated result": "High-risk findings",
    #         "latest event status": "A373 Symptomatic result recorded",
    #         "symptomatic procedure date": "Today",
    #         "symptomatic procedure result": "Non-neoplastic",
    #     },
    # )

    # # When I advance the subject's episode for "Refer to Surveillance after Symptomatic Referral"
    # SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    # AdvanceFOBTScreeningEpisodePage(
    #     page
    # ).click_refer_to_survelliance_after_symptomatic_referral_button()
    # # Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_no,
    #     {
    #         "latest event status": "A374 Refer to Surveillance after Symptomatic Referral",
    #     },
    # )
    # # And there is a "A374" letter batch for my subject with the exact title "Return Surveillance Letter after Referral to Symptomatic"
    # assert_batch_present_in_active_list(
    #     page=page,
    #     batch_type="A374",
    #     batch_description="Return Surveillance Letter after Referral to Symptomatic",
    # )
    # # When I view the advance episode options
    # screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    # SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    # # And I interrupt the subject's episode for "Redirect to Re-record the Outcome of Symptomatic Referral"
    # AdvanceFOBTScreeningEpisodePage(page).check_exception_circumstances_checkbox()
    # AdvanceFOBTScreeningEpisodePage(
    #     page).click_redirect_to_rerecord_the_outcome_of_symptomatic_referral_button()
    # # Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_no,
    #     {
    #         "which diagnostic test": "Latest not-void test in latest episode",
    #         "calculated fobt due date": "As at episode start",
    #         "calculated lynch due date": "Null",
    #         "calculated surveillance due date": "Unchanged",
    #         "ceased confirmation date": "Null",
    #         "ceased confirmation details": "Null",
    #         "ceased confirmation user id": "Null",
    #         "clinical reason for cease": "Null",
    #         "latest episode accumulated result": "High-risk findings",
    #         "latest episode includes event code": "E372 Reopen to Re-record Outcome from Symptomatic Referral",
    #         "latest episode recall calculation method": "Diagnostic test date",
    #         "latest episode recall episode type": "Null",
    #         "latest episode recall surveillance type": "Null",
    #         "latest episode status": "Open",
    #         "latest episode status reason": "Null",
    #         "latest event status": "A375 Redirect to Re-record the Outcome of Symptomatic Referral",
    #         "screening due date": "Calculated FOBT due date",
    #         "screening due date date of change": "Today",
    #         "screening due date reason": "Reopened episode",
    #         "screening status": "NOT: Ceased",
    #         "screening status date of change": "Today",
    #         "screening status reason": "Reopened episode",
    #         "surveillance due date": "Null",
    #         "surveillance due date reason": "Unchanged",
    #         "surveillance due date date of change": "Unchanged",
    #         "symptomatic procedure date": "Null",
    #         "symptomatic procedure result": "Null",
    #         "screening referral type": "Null",
    #     },
    # )
    # # And there is no "A374" letter batch for my subject with the exact title "Return Surveillance Letter after Referral to Symptomatic"
    # assert_batch_not_present_in_active_list(
    #     page=page,
    #     batch_type="A374",
    #     batch_description="Return Surveillance Letter after Referral to Symptomatic",
    # )
    # # When I view the advance episode options
    # screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    # # And I select the advance episode option for "LNPCP Result from Symptomatic Procedure"
    # SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    # AdvanceFOBTScreeningEpisodePage(page).click_lnpcp_result_from_symptomatic_procedure_button()
    # # And I set the Date of Symptomatic Procedure to "yesterday"
    # LnpcpResultFromSymptomaticProcedure(page).enter_date_of_symptomatic_procedure(datetime.today() - timedelta(days=1))
    # # And the Screening Interval is 36 months
    # LnpcpResultFromSymptomaticProcedure(page).assert_text_in_alert_textbox(
    #     "recall interval of 36 months"
    # )
    # # And I select test number 2
    # LnpcpResultFromSymptomaticProcedure(page).select_test_number(2)
    # # And I save the Result from Symptomatic Procedure
    # LnpcpResultFromSymptomaticProcedure(page).click_save_button()
    # # Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_no,
    #     {
    #         "which diagnostic test": "Latest not-void test in latest episode",
    #         "latest episode accumulated result": "LNPCP",
    #         "latest event status": "A373 Symptomatic result recorded",
    #         "symptomatic procedure date": "Yesterday",
    #         "symptomatic procedure result": "LNPCP",
    #     },
    # )
    # # When I advance the subject's episode for "Refer to Surveillance after Symptomatic Referral"
    # SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    # AdvanceFOBTScreeningEpisodePage(
    #     page
    # ).click_refer_to_survelliance_after_symptomatic_referral_button()
    # # Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_no,
    #     {
    #         "latest event status": "A374 Refer to Surveillance after Symptomatic Referral",
    #     },
    # )
    # # And there is a "A374" letter batch for my subject with the exact title "Return Surveillance Letter after Referral to Symptomatic"
    # assert_batch_present_in_active_list(
    #     page=page,
    #     batch_type="A374",
    #     batch_description="Return Surveillance Letter after Referral to Symptomatic",
    # )
    # # When I process the open "A374" letter batch for my subject
    # batch_processing(
    #     page,
    #     "A374",
    #     "Return Surveillance Letter after Referral to Symptomatic",
    # )
    # # Then my subject has been updated as follows:
    # subject_assertion(
    #     nhs_no,
    #     {
    #         "which diagnostic test": "Latest not-void test in latest episode",
    #         "calculated fobt due date": "Unchanged",
    #         "calculated lynch due date": "Null",
    #         "calculated surveillance due date": "3 years from symptomatic procedure",
    #         "ceased confirmation date": "Null",
    #         "ceased confirmation details": "Null",
    #         "ceased confirmation user id": "Null",
    #         "clinical reason for cease": "Null",
    #         "latest episode accumulated result": "LNPCP",
    #         "latest episode recall calculation method": "Symptomatic Procedure date",
    #         "latest episode recall episode type": "Surveillance - LNPCP",
    #         "latest episode recall surveillance type": "LNPCP",
    #         "latest episode status": "Closed",
    #         "latest episode status reason": "Episode Complete",
    #         "latest event status": "A157 LNPCP",
    #         "lynch due date": "Null",
    #         "lynch due date date of change": "Unchanged",
    #         "lynch due date reason": "Unchanged",
    #         "screening due date": "Null",
    #         "screening due date date of change": "Today",
    #         "screening due date reason": "Result referred to Surveillance",
    #         "screening status": "Surveillance",
    #         "screening status date of change": "Today",
    #         "screening status reason": "Result Referred to Surveillance",
    #         "surveillance due date": "Calculated Surveillance Due Date",
    #         "surveillance due date date of change": "Today",
    #         "surveillance due date reason": "Result - LNPCP",
    #         "symptomatic procedure date": "Yesterday",
    #         "symptomatic procedure result": "LNPCP",
    #         "screening referral type": "Null",
    #     },
    # )

@pytest.mark.wip2

def test_create_subjects_for_scneario_13(page: Page) -> None:
    """ """
    user_role = UserTools.user_login(
        page, "Hub Manager State Registered at BCS01", True
    )
    if user_role is None:
        raise ValueError("User Role is None")
    requirements = {
        "age (y/d)": "65/25",
        "active gp practice in hub/sc": "BCS01/BCS001",
    }
    nhs_no = CreateSubjectSteps().create_custom_subject(requirements)
    if nhs_no is None:
        raise ValueError("NHS No is 'None'")
    CallAndRecallUtils().run_failsafe(nhs_no)
    CallAndRecallUtils().invite_subject_for_fobt_screening(nhs_no, user_role)
    batch_processing(
        page,
        "S1",
        "Pre-invitation (FIT)",
    )
    logging.info(f"Subject NHS Number: {nhs_no}")

@pytest.mark.wip3
def test_test(page: Page) -> None:
    user_role = UserTools.user_login(
        page, "Hub Manager at BCS01", return_role_type=True
    )
    if user_role is None:
        raise ValueError("This user cannot be assigned to a UserRoleType")
    criteria = {
        "latest event status": "S9 Pre-Invitation Sent",
        "latest episode kit class": "FIT",
        "latest episode started": "Within the last 6 months",
        "latest episode type": "FOBT",
        "subject age": "Between 60 and 72",
        "subject has unprocessed sspi updates": "No",
        "subject has user dob updates": "No",
        "subject hub code": "User's hub",
    }
 
    user = User().from_user_role_type(user_role)
 
    query, bind_vars = SubjectSelectionQueryBuilder().build_subject_selection_query(
        criteria=criteria,
        user=user,
        subject=Subject(),
        subjects_to_retrieve=1,
    )

    nhs_no_df = OracleDB().execute_query(query=query, parameters=bind_vars)
    nhs_no = nhs_no_df["subject_nhs_number"].iloc[0]

    logging.info(f"[SUBJECT RETRIEVAL] Retrieved subject's NHS number: {nhs_no}")
