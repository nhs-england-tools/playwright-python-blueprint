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
)
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
    CompletionProofOptions,
    EndoscopyLocationOptions,
    OpticalDiagnosisConfidenceOptions,
    OpticalDiagnosisOptions,
    PolypAccessOptions,
    PolypClassificationOptions,
    PolypExcisionCompleteOptions,
    PolypInterventionDeviceOptions,
    PolypInterventionModalityOptions,
    PolypInterventionRetrievedOptions,
    PolypTypeOptions,
    SerratedLesionSubTypeOptions,
)
from classes.repositories.person_repository import PersonRepository
from pages.login.select_job_role_page import SelectJobRolePage


@pytest.mark.usefixtures("setup_org_and_appointments")
@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.fobt_regression_tests
def test_scenario_11(page: Page) -> None:
    """
    Scenario: 11: Abnormal result from diagnostic tests

    S9-S10-S43-A8-A183-A25-J10-A99-A59-A259-A360-A410-A415-A417-A422-A360-A410-A415-A416-(A50)-A316-A430-(A167)-A65-C203 [SSCL10a]

    This scenario tests a fairly straight-forward progression of an FOBT episode to closure on A65 Abnormal from diagnostic test results (but not symptomatic procedure results). The investigation dataset is only completed after the post-investigation appointment pathway has been selected.

    The diagnostic test is carried out by a clinician accredited for Resect & Discard: polyp categories of retrieved and resected & discarded polyps are checked as follows:


    > Polyp 1 (retrieved) category is Diminutive Rectal Hyperplastic: would be "Other" if it had been resected and discarded.
    > Polyp 2 (r&d) category is Other: would be LNPCP if it did not have optical diagnosis of "Other".
    > Polyp 3 (r&d) category is Other: would be Advanced colorectal if it did not have optical diagnosis of "Other".
    > Polyp 4 (r&d) category is Other: would be Premalignant if it did not have optical diagnosis of "Other".
    > Polyp 5 (r&d) category is Diminutive rectal hyperplastic.
    > Polyp 6 (r&d) category is Premalignant: size < 10mm.


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
    > Invite for diagnostic test > A59 (2.1)
    > Attend diagnostic test > A259 (2.1)
    > Post-investigation appointment required > A360 (2.1)
    > Complete investigation dataset – abnormal (2.1)
    > Book post-investigation appointment > A410 (2.4)
    > Process A410 letter batch > A415 (2.4)
    > SC cancel post-investigation appointment > A417 (2.4)
    > Process A417 letter batch > A422 (2.4)
    > Post-investigation appointment required > A360 (2.1)
    > Book post-investigation appointment > A410 (2.4)
    > Process A410 letter batch > A415 (2.4)
    > Attend post-investigation appointment > A416 (2.4)
    > Record diagnosis date (A50)
    > Enter diagnostic test outcome – investigation complete > A316 > A430 (2.4)
    > Process A183 result letter (A167) (1.11)
    > Process A430 letter batch > A65 (2.4) > C203 (2.8, 1.13)
    > Check recall [SSCL10a]
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
        criteria=criteria,
        user=User(),
        subject=Subject(),
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
    FitKitLogged().log_fit_kits(page, fit_kit, datetime.now())

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {"latest event status": "S43 Kit Returned and Logged (Initial Test)"},
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
    criteria = {
        "latest event status": "A183 1st Colonoscopy Assessment Appointment Requested"
    }
    subject_assertion(
        nhs_no,
        criteria,
    )

    # And there is a "A183" letter batch for my subject with the exact title "Practitioner Clinic 1st Appointment"
    # When I process the open "A183 - Practitioner Clinic 1st Appointment" letter batch for my subject
    # Then my subject has been updated as follows:
    batch_processing(
        page=page,
        batch_type="A183",
        batch_description="Practitioner Clinic 1st Appointment",
        latest_event_status="A25 - 1st Colonoscopy Assessment Appointment Booked, letter sent",
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
        nhs_number=nhs_no,
        criteria={"latest event status": "A99 Suitable for Endoscopic Test"},
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the advance episode options
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # And I select Diagnostic Test Type "Colonoscopy"
    AdvanceFOBTScreeningEpisodePage(page).select_test_type_dropdown_option(
        text="Colonoscopy"
    )

    # And I enter a Diagnostic Test First Offered Appointment Date of "tomorrow"
    AdvanceFOBTScreeningEpisodePage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(date=datetime.today() + timedelta(days=1))

    # And I advance the subject's episode for "Invite for Diagnostic Test >>"
    AdvanceFOBTScreeningEpisodePage(page).click_invite_for_diagnostic_test_button()

    # Then my subject has been updated as follows:
    AdvanceFOBTScreeningEpisodePage(page).verify_latest_event_status_value(
        latest_event_status="A59 - Invited for Diagnostic Test"
    )

    # When I select the advance episode option for "Attend Diagnostic Test"
    screening_subject_page_searcher.navigate_to_subject_summary_page(
        page=page, nhs_no=nhs_no
    )
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_attend_diagnostic_test_button()

    # And I attend the subject's diagnostic test today
    AttendDiagnosticTestPage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(date=datetime.today())
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

    # And I edit the Investigation Dataset for this subject
    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    user = User.from_user_role_type(user_role)
    criteria = {
        "Person has current role": "Accredited Screening Colonoscopist",
        "Person has current role in organisation": "User's SC",
        "Latest resect & discard accreditation start date": "Within the last 2 years",
    }
    query = PersonRepository().build_person_selection_query(
        criteria=criteria, person=None, required_person_count=1, user=user, subject=None
    )
    logging.info(f"Final query: {query}")
    df = OracleDB().execute_query(query)
    person_name = (
        f"{df["person_family_name"].iloc[0]} {df["person_given_name"].iloc[0]}"
    )

    # And I set the following fields and values within the "Investigation Dataset" section of the investigation dataset:
    general_information = {
        "site": 1,
        "practitioner": 1,
        "testing clinician": person_name,
        "aspirant endoscopist": None,
    }

    # When I add the following "bowel preparation administered" drugs and doses within the Investigation Dataset for this subject:
    drug_information = {"drug_type1": DrugTypeOptions.MANNITOL, "drug_dose1": "3"}

    # And I set the following fields and values within the "Endoscopy Information" section of the investigation dataset:
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
        "detection assistant used": YesNoOptions.YES,
        "insufflation": InsufflationOptions.AIR,
        "outcome at time of procedure": OutcomeAtTimeOfProcedureOptions.LEAVE_DEPARTMENT,
        "late outcome": LateOutcomeOptions.NO_COMPLICATIONS,
    }

    # And I set the following completion proof values within the Investigation Dataset for this subject:
    completion_information = {"completion proof": CompletionProofOptions.VIDEO_APPENDIX}

    # And I set the following failure reasons within the Investigation Dataset for this subject:
    failure_information = {"failure reasons": FailureReasonsOptions.NO_FAILURE_REASONS}

    # When I add new polyp 1 with the following fields and values within the Investigation Dataset for this subject:
    # And I add new polyp 2 with the following fields and values within the Investigation Dataset for this subject:
    # And I add new polyp 3 with the following fields and values within the Investigation Dataset for this subject:
    # And I add new polyp 4 with the following fields and values within the Investigation Dataset for this subject:
    # And I add new polyp 5 with the following fields and values within the Investigation Dataset for this subject:
    # And I add new polyp 6 with the following fields and values within the Investigation Dataset for this subject:
    polyp_information = [
        {
            "location": EndoscopyLocationOptions.RECTUM,
            "classification": PolypClassificationOptions.IP,
            "optical diagnosis": OpticalDiagnosisOptions.OTHER_POLYP_NEOPLASTIC,
            "estimate of whole polyp size": "6",
            "optical diagnosis confidence": OpticalDiagnosisConfidenceOptions.HIGH,
            "polyp access": PolypAccessOptions.EASY,
            "left in situ": YesNoOptions.NO,
        },
        {
            "location": EndoscopyLocationOptions.CAECUM,
            "classification": PolypClassificationOptions.LST_NG,
            "optical diagnosis": OpticalDiagnosisOptions.OTHER_POLYP_NON_NEOPLASTIC,
            "estimate of whole polyp size": "25",
            "optical diagnosis confidence": OpticalDiagnosisConfidenceOptions.HIGH,
            "polyp access": PolypAccessOptions.EASY,
            "left in situ": YesNoOptions.NO,
        },
        {
            "location": EndoscopyLocationOptions.DESCENDING_COLON,
            "classification": PolypClassificationOptions.IP,
            "optical diagnosis": OpticalDiagnosisOptions.OTHER_POLYP_NEOPLASTIC,
            "estimate of whole polyp size": "11",
            "optical diagnosis confidence": OpticalDiagnosisConfidenceOptions.LOW,
            "polyp access": PolypAccessOptions.EASY,
            "left in situ": YesNoOptions.NO,
        },
        {
            "location": EndoscopyLocationOptions.ASCENDING_COLON,
            "classification": PolypClassificationOptions.ISP,
            "optical diagnosis": OpticalDiagnosisOptions.OTHER_POLYP_NON_NEOPLASTIC,
            "estimate of whole polyp size": "4",
            "optical diagnosis confidence": OpticalDiagnosisConfidenceOptions.HIGH,
            "polyp access": PolypAccessOptions.EASY,
            "left in situ": YesNoOptions.NO,
        },
        {
            "location": EndoscopyLocationOptions.RECTUM,
            "classification": PolypClassificationOptions.ISP,
            "optical diagnosis": OpticalDiagnosisOptions.SERRATED_HYPERPLASTIC_SSL,
            "estimate of whole polyp size": "5",
            "optical diagnosis confidence": OpticalDiagnosisConfidenceOptions.HIGH,
            "polyp access": PolypAccessOptions.EASY,
            "left in situ": YesNoOptions.NO,
        },
        {
            "location": EndoscopyLocationOptions.SIGMOID_COLON,
            "classification": PolypClassificationOptions.IS,
            "optical diagnosis": OpticalDiagnosisOptions.SERRATED_HYPERPLASTIC_SSL,
            "estimate of whole polyp size": "4",
            "optical diagnosis confidence": OpticalDiagnosisConfidenceOptions.LOW,
            "polyp access": PolypAccessOptions.EASY,
            "left in situ": YesNoOptions.NO,
        },
    ]

    # And I add intervention 1 for polyp 1 with the following fields and values within the Investigation Dataset for this subject:
    # And I add intervention 1 for polyp 2 with the following fields and values within the Investigation Dataset for this subject:
    # And I add intervention 1 for polyp 3 with the following fields and values within the Investigation Dataset for this subject:
    # And I add intervention 1 for polyp 4 with the following fields and values within the Investigation Dataset for this subject:
    # And I add intervention 1 for polyp 5 with the following fields and values within the Investigation Dataset for this subject:
    # And I add intervention 1 for polyp 6 with the following fields and values within the Investigation Dataset for this subject:
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
                "retrieved": PolypInterventionRetrievedOptions.NO_RESECT_AND_DISCARD,
                "image id": "AUTO TEST POLYP 2",
            }
        ],
        [
            {
                "modality": PolypInterventionModalityOptions.POLYPECTOMY,
                "device": PolypInterventionDeviceOptions.COLD_SNARE,
                "excised": YesNoOptions.YES,
                "retrieved": PolypInterventionRetrievedOptions.NO_RESECT_AND_DISCARD,
                "image id": "AUTO TEST POLYP 3",
            }
        ],
        [
            {
                "modality": PolypInterventionModalityOptions.ESD,
                "device": PolypInterventionDeviceOptions.ENDOSCOPIC_KNIFE,
                "excised": YesNoOptions.YES,
                "retrieved": PolypInterventionRetrievedOptions.NO_RESECT_AND_DISCARD,
                "image id": "AUTO TEST POLYP 4",
            }
        ],
        [
            {
                "modality": PolypInterventionModalityOptions.POLYPECTOMY,
                "device": PolypInterventionDeviceOptions.HOT_SNARE,
                "excised": YesNoOptions.YES,
                "retrieved": PolypInterventionRetrievedOptions.NO_RESECT_AND_DISCARD,
                "image id": "AUTO TEST POLYP 5",
            }
        ],
        [
            {
                "modality": PolypInterventionModalityOptions.EMR,
                "device": PolypInterventionDeviceOptions.HOT_SNARE,
                "excised": YesNoOptions.YES,
                "retrieved": PolypInterventionRetrievedOptions.NO_RESECT_AND_DISCARD,
                "image id": "AUTO TEST POLYP 6",
            }
        ],
    ]

    # And I update histology details for polyp 1 with the following fields and values within the Investigation Dataset for this subject:
    polyp_histology = [
        {
            "date of receipt": datetime.today(),
            "date of reporting": datetime.today(),
            "pathology provider": 1,
            "pathologist": 1,
            "polyp type": PolypTypeOptions.SERRATED_LESION,
            "serrated lesion sub type": SerratedLesionSubTypeOptions.HYPERPLASTIC_POLYP,
            "polyp excision complete": PolypExcisionCompleteOptions.R1,
            "polyp size": "5",
        }
    ]

    # And I mark the Investigation Dataset as complete
    # And I press the save Investigation Dataset button
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

    # Then the Investigation Dataset result message, which I will cancel, is "Abnormal"
    InvestigationDatasetsPage(page).expect_text_to_be_visible("Abnormal")

    # Then I confirm the Polyp Algorithm Size for Polyp 1 is 5
    InvestigationDatasetsPage(page).assert_polyp_algorithm_size(1, "5")

    # And I confirm the Polyp Category for Polyp 1 is "Diminutive Rectal Hyperplastic Polyp"
    InvestigationDatasetsPage(page).assert_polyp_category(
        1, "Diminutive rectal hyperplastic polyp"
    )

    # And I confirm the Polyp Algorithm Size for Polyp 2 is 25
    InvestigationDatasetsPage(page).assert_polyp_algorithm_size(2, "25")

    # And I confirm the Polyp Category for Polyp 2 is "Other polyp"
    InvestigationDatasetsPage(page).assert_polyp_category(2, "Other polyp")

    # And I confirm the Polyp Algorithm Size for Polyp 3 is 11
    InvestigationDatasetsPage(page).assert_polyp_algorithm_size(3, "11")

    # And I confirm the Polyp Category for Polyp 3 is "Other polyp"
    InvestigationDatasetsPage(page).assert_polyp_category(3, "Other polyp")

    # And I confirm the Polyp Algorithm Size for Polyp 4 is 4
    InvestigationDatasetsPage(page).assert_polyp_algorithm_size(4, "4")

    # And I confirm the Polyp Category for Polyp 4 is "Other polyp"
    InvestigationDatasetsPage(page).assert_polyp_category(4, "Other polyp")

    # And I confirm the Polyp Algorithm Size for Polyp 5 is 5
    InvestigationDatasetsPage(page).assert_polyp_algorithm_size(5, "5")

    # And I confirm the Polyp Category for Polyp 5 is "Diminutive rectal hyperplastic polyp"
    InvestigationDatasetsPage(page).assert_polyp_category(
        5, "Diminutive rectal hyperplastic polyp"
    )

    # And I confirm the Polyp Algorithm Size for Polyp 6 is 4
    InvestigationDatasetsPage(page).assert_polyp_algorithm_size(6, "4")

    # And I confirm the Polyp Category for Polyp 6 is "Premalignant polyp"
    InvestigationDatasetsPage(page).assert_polyp_category(6, "Premalignant polyp")

    # And my subject has been updated as follows:
    subject_assertion(nhs_no, {"latest episode accumulated result": "Abnormal"})

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I choose to book a practitioner clinic for my subject
    SubjectScreeningSummaryPage(page).click_book_practitioner_clinic_button()

    # And I set the practitioner appointment date to "today"
    # And I book the earliest available post investigation appointment on this date
    book_post_investigation_appointment(page, "The Royal Hospital (Wolverhampton)", 1)

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no, {"latest event status": "A410 Post-investigation Appointment Made"}
    )

    # And there is a "A410" letter batch for my subject with the exact title "Post-Investigation Appointment Invitation Letter"
    # When I process the open "A410 - Post-Investigation Appointment Invitation Letter" letter batch for my subject
    batch_processing(
        page,
        "A410",
        "Post-Investigation Appointment Invitation Letter",
        "A415 - Post-investigation Appointment Invitation Letter Printed",
    )

    # When I view the event history for the subject's latest episode
    SubjectScreeningSummaryPage(page).expand_episodes_list()
    SubjectScreeningSummaryPage(page).click_first_fobt_episode_link()

    # And I view the latest practitioner appointment in the subject's episode
    EpisodeEventsAndNotesPage(page).click_most_recent_view_appointment_link()

    # And The Screening Centre cancels the practitioner appointment with reason "Screening Centre Cancelled"
    AppointmentDetailPage(page).check_cancel_radio()
    AppointmentDetailPage(page).select_reason_for_cancellation_option(
        ReasonForCancellationOptions.SCREENING_CENTRE_CANCELLED
    )

    # And I press OK on my confirmation prompt
    AppointmentDetailPage(page).click_save_button(accept_dialog=True)

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A417 Post-investigation Appointment Cancelled by SC",
        },
    )

    # And there is a "A417" letter batch for my subject with the exact title "Post-Investigation Appointment Cancelled (Screening Centre)"
    # When I process the open "A417" letter batch for my subject
    batch_processing(
        page,
        "A417",
        "Post-Investigation Appointment Cancelled (Screening Centre)",
        "A422 - Post-investigation Appointment Cancellation Letter Printed",
    )

    # When I advance the subject's episode for "Post-investigation Appointment Required"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(
        page
    ).click_post_investigation_appointment_required_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_number=nhs_no,
        criteria={
            "latest event status": "A360 Post-investigation Appointment Required",
        },
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I choose to book a practitioner clinic for my subject
    SubjectScreeningSummaryPage(page).click_book_practitioner_clinic_button()

    # And I set the practitioner appointment date to "today"
    # And I book the earliest available post investigation appointment on this date
    book_post_investigation_appointment(
        page=page,
        site="The Royal Hospital (Wolverhampton)",
        screening_practitioner_index=1,
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A410 Post-investigation Appointment Made",
        },
    )

    # And there is a "A410" letter batch for my subject with the exact title "Post-Investigation Appointment Invitation Letter"
    # When I process the open "A410 - Post-Investigation Appointment Invitation Letter" letter batch for my subject
    batch_processing(
        page=page,
        batch_type="A410",
        batch_description="Post-Investigation Appointment Invitation Letter",
        latest_event_status="A415 - Post-investigation Appointment Invitation Letter Printed",
    )

    # When I view the subject
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
        nhs_no,
        {
            "latest event status": "A416 Post-investigation Appointment Attended",
        },
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
        "latest event status": "A416 Post-investigation Appointment Attended",
    }
    subject_assertion(nhs_no, criteria)

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I select the advance episode option for "Enter Diagnostic Test Outcome"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_enter_diagnostic_test_outcome_button()

    # And I select Outcome of Investigation Complete
    DiagnosticTestOutcomePage(page).select_test_outcome_option(
        OutcomeOfDiagnosticTest.INVESTIGATION_COMPLETE
    )

    # And I save the Diagnostic Test Outcome
    DiagnosticTestOutcomePage(page).click_save_button()

    # Then my subject has been updated as follows:
    criteria = {
        "latest episode includes event status": "A316 Post-investigation Appointment Attended",
        "latest event status": "A430 Post-investigation Appointment Attended - Diagnostic Result Letter not Printed",
    }
    subject_assertion(nhs_no, criteria)

    # When I switch users to BCSS "England" as user role "Hub Manager"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    # And I process the open "A183 - GP Result (Abnormal)" letter batch for my subject
    batch_processing(
        page,
        "A183",
        "GP Result (Abnormal)",
    )

    # Then my subject has been updated as follows:
    criteria = {
        "latest episode includes event status": "A167 GP Abnormal FOBT Result Sent",
        "latest event status": "A430 Post-investigation Appointment Attended - Diagnostic Result Letter not Printed",
    }
    subject_assertion(nhs_no, criteria)

    # When I switch users to BCSS "England" as user role "Screening Centre Clerk"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Screening Centre Clerk at BCS001")
    SelectJobRolePage(page).select_option_for_job_role("Screening Centre Clerk")
    SelectJobRolePage(page).click_continue_button()

    # And there is a "A430" letter batch for my subject with the exact title "Result Letters Following Post-investigation Appointment"
    # And I process the open "A430" letter batch for my subject
    batch_processing(
        page,
        "A430",
        "Result Letters Following Post-investigation Appointment",
    )
    # Then my subject has been updated as follows:
    criteria = {
        "which diagnostic test": "Latest not-void test in latest episode",
        "calculated fobt due date": "2 years from diagnostic test",
        "calculated lynch due date": "Null",
        "calculated surveillance due date": "Unchanged",
        "ceased confirmation date": "Null",
        "ceased confirmation details": "Null",
        "ceased confirmation user id": "Null",
        "clinical reason for cease": "Null",
        "latest episode accumulated result": "Abnormal",
        "latest episode recall calculation method": "Diagnostic test date",
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
        "symptomatic procedure date": "Null",
        "symptomatic procedure result": "Null",
        "screening referral type": "Null",
    }
    subject_assertion(nhs_no, criteria)
    LogoutPage(page).log_out()
