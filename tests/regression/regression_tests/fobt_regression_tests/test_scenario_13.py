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
from utils.appointments import book_appointments
from utils.oracle.oracle import OracleDB
from utils.investigation_dataset import InvestigationDatasetCompletion
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from pages.screening_subject_search.diagnostic_test_outcome_page import (
    DiagnosticTestOutcomePage,
    OutcomeOfDiagnosticTest,
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
from classes.repositories.person_repository import PersonRepository
from classes.repositories.episode_repository import EpisodeRepository
from utils.sspi_change_steps import SSPIChangeSteps
from pages.organisations.organisations_page import OrganisationSwitchPage


@pytest.mark.usefixtures("setup_org_and_appointments")
@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.fobt_regression_tests
def test_scenario_13(page: Page) -> None:
    """
    Scenario: 13: LNPCP result from diagnostic tests

    S9-S10-S43-A8-A183-A25-J10-A99-(A50)-A59-A259-S92-C203 [SSCL36a] (A167)-A259-A315-A361-A323-A317-A318-A157-C203 [SSCL52a]

    In this scenario, the diagnostic test gives a result of LNPCP, but an SSPI cease closes the episode after the dataset is completed (so the episode result has been set) but before the test outcome has been entered.  The abnormal result letter is only printed after the episode has been closed.  The scenario proves that it is possible to uncease a subject from Embarkation by reopening the episode.  On reopen, the diagnostic test outcome is entered and the episode is progressed to completion, putting the subject into Surveillance.

    Scenario summary:

    > Find an in-age subject at S9 whose episode started recently before today (1.1)
    > Run timed events > creates S9 letter (1.1)
    > Process S9 letter batch > S10 (1.1)
    > Log kit > S43 (1.2)
    > Read kit with ABNORMAL result > A8 (1.3)
    > Invite for colonoscopy assessment > A183 (1.11)
    > Process A183 appointment letter > A25 (1.11)
    > Attend assessment appointment > J10 (1.11)
    > Suitable for colonoscopy > A99 (1.12)
    > Record diagnosis date (A50)
    > Invite for diagnostic test > A59 (2.1)
    > Attend diagnostic test > A259 (2.1)
    > Complete investigation dataset – LNPCP (2.1)
    > SSPI update ceases for embarkation > S92 > C203 (1.13)
    > Check recall [SSCL36a]
    > Process A183 result letter (A167) (1.11)
    > Reopen episode for subject decision > A259 (2.1)
    > Enter diagnostic test outcome – refer surveillance > A315 (2.1)
    > Post-investigation appointment not required > A361 (2.1)
    > Record patient contact – post-investigation appointment not required > A323 (2.1) > A317 > A318 (2.5)
    > Process A318 letter batch > A157 (2.5) > C203 (2.8, 1.13)
    > Check recall [SSCL52a]
    """
    # Given I log in to BCSS "England" as user role "Hub Manager"
    user_role = UserTools.user_login(
        page, "Hub Manager State Registered at BCS01", return_role_type=True
    )
    if user_role is None:
        raise ValueError("This user cannot be assigned to a UserRoleType")

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
        criteria=criteria,
        user=User(),
        subject=Subject(),
        subjects_to_retrieve=1,
    )

    nhs_no_df = OracleDB().execute_query(query=query, parameters=bind_vars)
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
    FitKitLogged().log_fit_kits(page=page, fit_kit=fit_kit, sample_date=datetime.now())

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
    screening_subject_page_searcher.navigate_to_subject_summary_page(
        page=page, nhs_no=nhs_no
    )

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

    # And I attend the subject's practitioner appointment "2 days ago"
    AppointmentDetailPage(page).mark_appointment_as_attended(
        datetime.today() - timedelta(days=2)
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_number=nhs_no,
        criteria={
            "latest event status": "J10 Attended Colonoscopy Assessment Appointment",
        },
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(
        page=page, nhs_no=nhs_no
    )

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
    screening_subject_page_searcher.navigate_to_subject_summary_page(
        page=page, nhs_no=nhs_no
    )

    # And I advance the subject's episode for "Suitable for Endoscopic Test"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_suitable_for_endoscopic_test_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_number=nhs_no,
        criteria={"latest event status": "A99 Suitable for Endoscopic Test"},
    )

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
        "latest event status": "A99 Suitable for Endoscopic Test",
    }
    subject_assertion(nhs_no, criteria)

    # When I view the advance episode options
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # And I select Diagnostic Test Type "Colonoscopy"
    AdvanceFOBTScreeningEpisodePage(page).select_test_type_dropdown_option(
        "Colonoscopy"
    )

    # And I enter a Diagnostic Test First Offered Appointment Date of "today"
    AdvanceFOBTScreeningEpisodePage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())

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

    # And I attend the subject's diagnostic test yesterday
    AttendDiagnosticTestPage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today() - timedelta(days=1))
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

    # And there is a clinician who meets the following criteria:
    user = User.from_user_role_type(user_role)
    criteria = {
        "Person has current role": "Accredited Screening Colonoscopist",
        "Person has current role in organisation": "User's SC",
        "Resect & Discard accreditation status": "None",
    }
    query = PersonRepository().build_person_selection_query(
        criteria=criteria, person=None, required_person_count=1, user=user, subject=None
    )
    logging.info(f"Final query: {query}")
    df = OracleDB().execute_query(query)
    person_name = (
        f"{df["person_family_name"].iloc[0]} {df["person_given_name"].iloc[0]}"
    )

    # And I add the following bowel preparation drugs and values within the Investigation Dataset for this subject:
    drug_information = {"drug_type1": DrugTypeOptions.MANNITOL, "drug_dose1": "3"}

    # And I set the following fields and values within the Investigation Dataset for this subject:
    general_information = {
        "site": 1,
        "practitioner": 1,
        "testing clinician": person_name,
        "aspirant endoscopist": None,
    }
    endoscopy_information = {
        "endoscope inserted": "yes",
        "procedure type": "therapeutic",
        "bowel preparation quality": BowelPreparationQualityOptions.GOOD,
        "comfort during examination": ComfortOptions.NO_DISCOMFORT,
        "comfort during recovery": ComfortOptions.NO_DISCOMFORT,
        "endoscopist defined extent": EndoscopyLocationOptions.APPENDIX,
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

    # And I set the following completion proof values within the Investigation Dataset for this subject:
    completion_information = {"completion proof": CompletionProofOptions.VIDEO_APPENDIX}

    # And I set the following failure reasons within the Investigation Dataset for this subject:
    failure_information = {"failure reasons": FailureReasonsOptions.ADHESION}

    # And I add new polyp 1 with the following fields and values within the Investigation Dataset for this subject:
    # And I add new polyp 2 with the following fields and values within the Investigation Dataset for this subject:
    # And I add new polyp 3 with the following fields and values within the Investigation Dataset for this subject:
    polyp_information = [
        {
            "location": EndoscopyLocationOptions.ANASTOMOSIS,
            "classification": PolypClassificationOptions.IP,
            "estimate of whole polyp size": "11",
            "polyp access": PolypAccessOptions.EASY,
            "left in situ": YesNoOptions.NO,
        },
        {
            "location": EndoscopyLocationOptions.CAECUM,
            "classification": PolypClassificationOptions.LST_NG,
            "estimate of whole polyp size": "5",
            "polyp access": PolypAccessOptions.EASY,
            "left in situ": YesNoOptions.NO,
        },
        {
            "location": EndoscopyLocationOptions.HEPATIC_FLEXURE,
            "classification": PolypClassificationOptions.LST_NG,
            "estimate of whole polyp size": "21",
            "polyp access": PolypAccessOptions.EASY,
            "left in situ": YesNoOptions.NO,
        },
    ]

    # And I add intervention 1 for polyp 1 with the following fields and values within the Investigation Dataset for this subject:
    # And I add intervention 1 for polyp 2 with the following fields and values within the Investigation Dataset for this subject:
    # And I add intervention 1 for polyp 3 with the following fields and values within the Investigation Dataset for this subject:
    polyp_intervention = [
        [
            {
                "modality": PolypInterventionModalityOptions.POLYPECTOMY,
                "device": PolypInterventionDeviceOptions.HOT_SNARE,
                "excised": YesNoOptions.YES,
                "retrieved": PolypInterventionRetrievedOptions.YES,
            }
        ],
        [
            {
                "modality": PolypInterventionModalityOptions.EMR,
                "device": PolypInterventionDeviceOptions.HOT_SNARE,
                "excised": YesNoOptions.YES,
                "retrieved": PolypInterventionRetrievedOptions.YES,
                "excision technique": PolypInterventionExcisionTechniqueOptions.EN_BLOC,
            }
        ],
        [
            {
                "modality": PolypInterventionModalityOptions.POLYPECTOMY,
                "device": PolypInterventionDeviceOptions.HOT_SNARE,
                "excised": YesNoOptions.YES,
                "retrieved": PolypInterventionRetrievedOptions.YES,
                "excision technique": PolypInterventionExcisionTechniqueOptions.PIECE_MEAL,
                "polyp appears fully resected endoscopically": YesNoOptions.YES,
            }
        ],
    ]

    # And I update histology details for polyp 1 with the following fields and values within the Investigation Dataset for this subject:
    # And I update histology details for polyp 2 with the following fields and values within the Investigation Dataset for this subject:
    # And I update histology details for polyp 3 with the following fields and values within the Investigation Dataset for this subject:
    polyp_histology = [
        {
            "date of receipt": datetime.today(),
            "date of reporting": datetime.today(),
            "pathology provider": 1,
            "pathologist": 1,
            "polyp type": PolypTypeOptions.ADENOMA,
            "adenoma sub type": AdenomaSubTypeOptions.NOT_REPORTED,
            "polyp excision complete": PolypExcisionCompleteOptions.R1,
            "polyp size": "13",
            "polyp dysplasia": PolypDysplasiaOptions.NOT_REPORTED,
            "polyp carcinoma": YesNoUncertainOptions.NO,
        },
        {
            "date of receipt": datetime.today(),
            "date of reporting": datetime.today(),
            "pathology provider": 1,
            "pathologist": 1,
            "polyp type": PolypTypeOptions.ADENOMA,
            "adenoma sub type": AdenomaSubTypeOptions.TUBULOVILLOUS_ADENOMA,
            "polyp excision complete": PolypExcisionCompleteOptions.R1,
            "polyp size": "4",
            "polyp dysplasia": PolypDysplasiaOptions.NOT_REPORTED,
            "polyp carcinoma": YesNoUncertainOptions.NO,
        },
        {
            "pathology lost": YesNoOptions.YES,
            "reason pathology lost": ReasonPathologyLostOptions.LOST_IN_TRANSIT,
        },
    ]

    # When I press the save Investigation Dataset button
    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
        polyp_information=polyp_information,
        polyp_intervention=polyp_intervention,
        polyp_histology=polyp_histology,
    )

    # Then the Investigation Dataset result message, which I will cancel, is "LNPCP"
    InvestigationDatasetsPage(page).expect_text_to_be_visible("LNPCP")

    # Then I confirm the Polyp Algorithm Size for Polyp 1 is 13
    InvestigationDatasetsPage(page).assert_polyp_algorithm_size(1, "13")

    # And I confirm the Polyp Algorithm Size for Polyp 2 is 4
    InvestigationDatasetsPage(page).assert_polyp_algorithm_size(2, "4")

    # And I confirm the Polyp Algorithm Size for Polyp 3 is 21
    InvestigationDatasetsPage(page).assert_polyp_algorithm_size(3, "21")

    # And I confirm the Polyp Category for Polyp 1 is "Advanced colorectal polyp"
    InvestigationDatasetsPage(page).assert_polyp_category(
        1, "Advanced colorectal polyp"
    )

    # And I confirm the Polyp Category for Polyp 2 is "Premalignant polyp"
    InvestigationDatasetsPage(page).assert_polyp_category(2, "Premalignant polyp")

    # And I confirm the Polyp Category for Polyp 3 is "LNPCP"
    InvestigationDatasetsPage(page).assert_polyp_category(3, "LNPCP")

    # And I confirm the Episode Result is "LNPCP"
    EpisodeRepository().confirm_episode_result(nhs_no, "LNPCP")

    # When I process an SSPI update for deduction reason "Embarkation"
    SSPIChangeSteps().process_sspi_deduction_by_description(nhs_no, "Embarkation")

    # Then my subject has been updated as follows:
    criteria = {
        "which diagnostic test": "Latest not-void test in latest episode",
        "calculated FOBT Due Date": "Unchanged",
        "calculated Lynch due date": "Null",
        "calculated Surveillance Due Date": "3 years from episode end",
        "ceased confirmation date": "Today",
        "ceased confirmation details": "SSPI deduction for emigration received.",
        "ceased confirmation user ID": "Automated process ID",
        "clinical reason for cease": "Null",
        "latest episode accumulated result": "LNPCP",
        "latest episode recall calculation method": "Episode end date",
        "latest episode recall episode type": "Surveillance - LNPCP",
        "latest episode recall surveillance type": "LNPCP",
        "latest episode status": "Closed",
        "latest episode status reason": "Individual has left the country",
        "latest event status": "S92 Close Screening Episode via Interrupt",
        "lynch due date": "Null",
        "lynch due date reason": "Unchanged",
        "lynch due date date of change": "Unchanged",
        "pre-interrupt event status": "A259 Attended Diagnostic Test",
        "screening Due Date": "Null",
        "screening Due Date Date of change": "Today",
        "screening Due Date Reason": "Ceased",
        "screening Status": "Ceased",
        "screening status date of change": "Today",
        "screening status reason": "Individual has left the country",
        "surveillance Due Date": "Null",
        "surveillance due date date of change": "Unchanged",
        "surveillance due date reason": "Unchanged",
        "symptomatic procedure date": "Null",
        "symptomatic procedure result": "Null",
        "screening referral type": "Null",
    }
    subject_assertion(nhs_no, criteria)

    # When I switch users to BCSS "England" as user role "Hub Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    user_role = UserTools.user_login(
        page, "Hub Manager State Registered at BCS01", return_role_type=True
    )
    if user_role is None:
        raise ValueError("User cannot be assigned to a UserRoleType")

    # And there is a "A183" letter batch for my subject with the exact title "GP Result (Abnormal)"
    # And I process the open "A183 - GP Result (Abnormal)" letter batch for my subject
    batch_processing(page, "A183", "GP Result (Abnormal)")

    # Then my subject has been updated as follows:
    criteria = {
        "latest episode includes event status": "A167 GP Abnormal FOBT Result Sent",
        "latest episode status": "Closed",
        "latest event status": "S92 Closed Screening Episode via Interrupt",
        "screening status": "Ceased",
    }
    subject_assertion(nhs_no, criteria)

    # When I switch users to BCSS "England" as user role "Specialist Screening Practitioner"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Specialist Screening Practitioner at BCS009 & BCS001")
    OrganisationSwitchPage(page).select_organisation_by_id("BCS001")
    OrganisationSwitchPage(page).click_continue()

    # And I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I reopen the subject's episode for "Reopen due to subject or patient decision"
    SubjectScreeningSummaryPage(page).click_reopen_fobt_screening_episode_button()
    ReopenFOBTScreeningEpisodePage(
        page
    ).click_reopen_due_to_subject_or_patient_decision()

    # Then my subject has been updated as follows:
    criteria = {
        "which diagnostic test": "Latest not-void test in latest episode",
        "calculated fobt due date": "As at episode start",
        "calculated lynch due date": "Null",
        "calculated surveillance due date": "Null",
        "ceased confirmation date": "Null",
        "ceased confirmation details": "Null",
        "ceased confirmation user id": "Null",
        "clinical reason for cease": "Null",
        "latest episode accumulated result": "LNPCP",
        "latest episode diagnosis date reason": "Null",
        "latest episode has diagnosis date": "Yes",
        "latest episode includes event code": "E72 Reopen due to subject or patient decision",
        "latest episode recall calculation method": "Episode end date",
        "latest episode recall episode type": "Null",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Open",
        "latest episode status reason": "Null",
        "latest event status": "A259 Attended Diagnostic Test",
        "screening due date": "Calculated FOBT due date",
        "screening due date date of change": "Today",
        "screening due date reason": "Reopened episode",
        "screening status": "NOT: Ceased",
        "screening status date of change": "Today",
        "screening status reason": "Reopened episode",
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

    # And I select the advance episode option for "Enter Diagnostic Test Outcome"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_enter_diagnostic_test_outcome_button()

    # And I select Outcome of Diagnostic Test "Refer Surveillance (BCSP)"
    DiagnosticTestOutcomePage(page).select_test_outcome_option(
        OutcomeOfDiagnosticTest.REFER_SURVEILLANCE
    )

    # And I save the Diagnostic Test Outcome
    DiagnosticTestOutcomePage(page).click_save_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {"latest event status": "A315 Diagnostic Test Outcome Entered"},
    )

    # When I advance the subject's episode for "Other Post-investigation Contact Required"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_other_post_investigation_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {"latest event status": "A361 Other Post-investigation Contact Required"},
    )

    # When I select the advance episode option for "Record other post-investigation contact"
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
            "latest event status": "A318 Post-investigation Appointment NOT Required - Result Letter Created",
        },
    )

    # And there is a "A318" letter batch for my subject with the exact title "Result Letters - No Post-investigation Appointment"
    # When I process the open "A318" letter batch for my subject
    batch_processing(page, "A318", "Result Letters - No Post-investigation Appointment")

    # Then my subject has been updated as follows:
    criteria = {
        "which diagnostic test": "Latest not-void test in latest episode",
        "calculated fobt due date": "Unchanged",
        "calculated lynch due date": "Null",
        "calculated surveillance due date": "3 years from diagnostic test",
        "ceased confirmation date": "Null",
        "ceased confirmation details": "Null",
        "ceased confirmation user id": "Null",
        "clinical reason for cease": "Null",
        "latest episode accumulated result": "LNPCP",
        "latest episode recall calculation method": "Diagnostic test date",
        "latest episode recall episode type": "Surveillance - LNPCP",
        "latest episode recall surveillance type": "LNPCP",
        "latest episode status": "Closed",
        "latest episode status reason": "Episode Complete",
        "latest event status": "A157 LNPCP",
        "lynch due date": "Null",
        "lynch due date reason": "Unchanged",
        "lynch due date date of change": "Unchanged",
        "screening due date": "Null",
        "screening due date date of change": "Today",
        "screening due date reason": "Result referred to Surveillance",
        "screening status": "Surveillance",
        "screening status date of change": "Today",
        "screening status reason": "Result referred to Surveillance",
        "surveillance due date": "Calculated Surveillance Due Date",
        "surveillance due date date of change": "Today",
        "surveillance due date reason": "Result - LNPCP",
        "symptomatic procedure date": "Null",
        "symptomatic procedure result": "Null",
        "screening referral type": "Null",
    }
    subject_assertion(nhs_no, criteria)

    LogoutPage(page).log_out()
