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
from utils.datasets.investigation_datasets import (
    get_default_general_information,
    get_default_drug_information,
    get_default_endoscopy_information,
    get_normal_smokescreen_information,
)
from utils.sspi_change_steps import SSPIChangeSteps
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
from pages.screening_subject_search.contact_with_patient_page import (
    ContactWithPatientPage,
)
from pages.organisations.organisations_page import OrganisationSwitchPage
from pages.datasets.investigation_dataset_page import (
    InvestigationDatasetsPage,
    FailureReasonsOptions,
)
from pages.screening_subject_search.reopen_fobt_screening_episode_page import (
    ReopenFOBTScreeningEpisodePage,
)


@pytest.mark.usefixtures("setup_org_and_appointments")
@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.fobt_regression_tests
def test_scenario_10(page: Page) -> None:
    """
    Scenario: 10: Normal result from diagnostic tests

    S9-S10-S43-A8-A183-A25-J10-A99-(A167)-A165-A99-A59-A259-A315-(A50)-A361-A323-A317-A318-A380-A99-A59-A259-A360-A410-A415-A416-A316-A430-S61-C203 [SSCL10a] A416-A316-A430-S61-C203 [SSCL12a]

    This scenario tests progression of an FOBT episode to closure on S61 Normal from diagnostic test results (but not symptomatic procedure results). It tests both in-age and below-age closures, and a reopen to confirm the diagnostic test result and outcome. This reopen removes the diagnostic test outcome and the recall calculation method, but does NOT remove the diagnostic test result or change the accumulated episode result.

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
    > Process A183 result letter (A167) (1.11)
    > Awaiting decision to proceed > A165 (1.12)
    > Suitable for colonoscopy > A99 (1.12)
    > Invite for diagnostic test > A59 (2.1)
    > Attend diagnostic test > A259 (2.1)
    > Complete investigation dataset - no result (2.1)
    > Enter diagnostic test outcome - failed test, refer another > A315 (2.1)
    > Record diagnosis date (A50)
    > Post-investigation appointment not required > A361 (2.1)
    > Record patient contact - post-investigation appointment not required > A323 (2.1) > A317 > A318 (2.5)
    > Process A318 letter batch > A380 (2.5)
    > Record patient contact - suitable for colonoscopy > A99 (2.3)
    > Invite for diagnostic test > A59 (2.1)
    > Attend diagnostic test > A259 (2.1)
    > Complete investigation dataset - normal result (2.1)
    > Post-investigation appointment required > A360 (2.1)
    > Book post-investigation appointment > A410 (2.4)
    > Process A410 letter batch > A415 (2.4)
    > Attend post-investigation appointment > A416 (2.4)
    > Enter diagnostic test outcome - investigation complete > A316 > A430 (2.4)
    > Process A430 letter batch > S61 (2.4) > C203 (2.8, 1.13)
    > Check recall [SSCL10a]
    > Reopen to Confirm Diagnostic Test Result and Outcome > A416 (2.4)
    > SSPI update changes subject to below-age
    > Enter diagnostic test outcome - investigation complete > A316 > A430 (2.4)
    > Process A430 letter batch > S61 (2.4) > C203 (2.8, 1.13)
    > Check recall [SSCL12a]
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
    builder = SubjectSelectionQueryBuilder()

    query, bind_vars = builder.build_subject_selection_query(
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
    OracleDB().exec_bcss_timed_events(None, nhs_no)

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
    subject_assertion(nhs_no, {"latest event status": "A8 Abnormal"})

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
        page,
        "A183",
        "Practitioner Clinic 1st Appointment",
        "A25 - 1st Colonoscopy Assessment Appointment Booked, letter sent",
    )

    # When I switch users to BCSS "England" as user role "Specialist Screening Practitioner"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Specialist Screening Practitioner at BCS009 & BCS001")
    OrganisationSwitchPage(page).select_organisation_by_id("BCS001")
    OrganisationSwitchPage(page).click_continue()

    # And I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I view the event history for the subject's latest episode
    SubjectScreeningSummaryPage(page).expand_episodes_list()
    SubjectScreeningSummaryPage(page).click_first_fobt_episode_link()

    # And I view the latest practitioner appointment in the subject's episode
    EpisodeEventsAndNotesPage(page).click_most_recent_view_appointment_link()

    # And I attend the subject's practitioner appointment "2 days ago"
    AppointmentDetailPage(page).mark_appointment_as_attended(
        datetime.today() - timedelta(2)
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
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_suitable_for_endoscopic_test_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no, {"latest event status": "A99 Suitable for Endoscopic Test"}
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
        "A99 - Suitable for Endoscopic Test",
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest episode includes event status": "A167 GP Abnormal FOBT Result Sent",
            "latest event status": "A99 Suitable for Endoscopic Test",
        },
    )

    # When I switch users to BCSS "England" as user role "Specialist Screening Practitioner"
    LogoutPage(page).log_out(close_page=False)
    BasePage(page).go_to_log_in_page()
    UserTools.user_login(page, "Specialist Screening Practitioner at BCS009 & BCS001")
    OrganisationSwitchPage(page).select_organisation_by_id("BCS001")
    OrganisationSwitchPage(page).click_continue()

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I advance the subject's episode for "Waiting Decision to Proceed with Diagnostic Test"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(
        page
    ).click_waiting_decision_to_proceed_with_diagnostic_test()

    # Then my subject has been updated as follows:
    AdvanceFOBTScreeningEpisodePage(page).verify_latest_event_status_value(
        "A165 - Waiting Decision to Proceed with Diagnostic Test"
    )

    # When I view the advance episode options
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
        "A59 - Invited for Diagnostic Test"
    )

    # When I select the advance episode option for "Attend Diagnostic Test"
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_attend_diagnostic_test_button()

    # And I attend the subject's diagnostic test yesterday
    AttendDiagnosticTestPage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today() - timedelta(1))
    AttendDiagnosticTestPage(page).click_save_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A259 Attended Diagnostic Test",
        },
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I edit the Investigation Dataset for this subject
    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    # And I add the following bowel preparation drugs and values within the Investigation Dataset for this subject:
    drug_information = get_default_drug_information()

    # And I set the following fields and values within the Investigation Dataset for this subject:
    general_information = get_default_general_information()
    endoscopy_information = get_default_endoscopy_information()
    endoscopy_information["procedure type"] = "diagnostic"

    # And I set the following failure reasons within the Investigation Dataset for this subject:
    failure_information = {
        "failure reasons": FailureReasonsOptions.PAIN,
    }

    # And I mark the Investigation Dataset as completed
    # When I press the save Investigation Dataset button
    # And I press OK on my confirmation prompt
    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
    )

    # Then the Investigation Dataset result message, which I will cancel, is "No Result"
    InvestigationDatasetsPage(page).expect_text_to_be_visible("No Result")

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest episode accumulated result": "No result",
        },
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I select the advance episode option for "Enter Diagnostic Test Outcome"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_enter_diagnostic_test_outcome_button()

    # And I select Outcome of Diagnostic Test "Failed Test - Refer Another"
    DiagnosticTestOutcomePage(page).select_test_outcome_option(
        OutcomeOfDiagnosticTest.FAILED_TEST_REFER_ANOTHER
    )

    # And I save the Diagnostic Test Outcome
    DiagnosticTestOutcomePage(page).click_save_button()

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest event status": "A315 Diagnostic Test Outcome Entered",
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
        "latest event status": "A315 Diagnostic Test Outcome Entered",
    }
    subject_assertion(nhs_no, criteria)

    # When I advance the subject's episode for "Other Post-investigation Contact Required"
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_other_post_investigation_button()

    # Then my subject has been updated as follows:
    AdvanceFOBTScreeningEpisodePage(page).verify_latest_event_status_value(
        "A361 - Other Post-investigation Contact Required"
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I select the advance episode option for "Record other post-investigation contact"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(
        page
    ).click_record_other_post_investigation_contact_button()

    # And I confirm the patient outcome dropdown has the following options:
    ContactWithPatientPage(page).verify_contact_with_patient_page_is_displayed()
    ContactWithPatientPage(page).verify_outcome_select_options(
        [
            "Post-investigation Appointment Not Required",
            "Post-investigation Appointment Required",
            "No outcome",
        ]
    )

    # And I record contact with the subject with outcome "Post-investigation Appointment Not Required"
    ContactWithPatientPage(page).record_post_investigation_appointment_not_required()

    # Then my subject has been updated as follows:
    criteria = {
        "latest episode includes event status": "A323 Post-investigation Appointment NOT Required"
    }
    subject_assertion(nhs_no, criteria)

    # Then my subject has been updated as follows:
    criteria = {
        "latest episode includes event status": "A317 Post-investigation Contact Made",
        "latest event status": "A318 Post-investigation Appointment NOT Required - Result Letter Created",
    }
    subject_assertion(nhs_no, criteria)

    # And there is a "A318" letter batch for my subject with the exact title "Result Letters - No Post-investigation Appointment"
    # When I process the open "A318" letter batch for my subject
    batch_processing(
        page,
        "A318",
        "Result Letters - No Post-investigation Appointment",
        "A380 - Failed Diagnostic Test - Refer Another",
    )

    # When I select the advance episode option for "Record Contact with Patient"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_record_contact_with_patient_button()

    # And I record contact with the subject with outcome "Suitable for Endoscopic Test"
    ContactWithPatientPage(page).record_contact("Suitable for Endoscopic Test")

    # Then my subject has been updated as follows:
    AdvanceFOBTScreeningEpisodePage(page).verify_latest_event_status_value(
        "A99 - Suitable for Endoscopic Test"
    )

    # When I view the advance episode options
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
        "A59 - Invited for Diagnostic Test"
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
        nhs_no,
        {
            "latest event status": "A259 Attended Diagnostic Test",
        },
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I edit the Investigation Dataset for this subject
    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    # And I apply the "Normal_Smokescreen" Investigation Dataset Scenario
    # And I mark the Investigation Dataset as completed
    # When I press the save Investigation Dataset button
    (
        general_information,
        drug_information,
        endoscopy_information,
        failure_information,
        completion_information,
    ) = get_normal_smokescreen_information()
    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
    )

    # Then the Investigation Dataset result message, which I will cancel, is "Normal (No Abnormalities Found)"
    InvestigationDatasetsPage(page).expect_text_to_be_visible(
        "Normal (No Abnormalities Found)"
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest episode accumulated result": "Normal (No Abnormalities Found)",
        },
    )

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I select the advance episode option for "Enter Diagnostic Test Outcome"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_enter_diagnostic_test_outcome_button()

    # And I select Outcome of Diagnostic Test "Investigation Complete"
    DiagnosticTestOutcomePage(page).select_test_outcome_option(
        OutcomeOfDiagnosticTest.INVESTIGATION_COMPLETE
    )

    # And I save the Diagnostic Test Outcome
    DiagnosticTestOutcomePage(page).click_save_button()

    # Then my subject has been updated as follows:
    criteria = {
        "which diagnostic test": "Latest not-void test in latest episode",
        "diagnostic test has outcome": "Investigation Complete",
        "diagnostic test has result": "Normal (No Abnormalities Found)",
        "latest event status": "A315 Diagnostic Test Outcome Entered",
    }
    subject_assertion(nhs_no, criteria)

    # When I advance the subject's episode for "Post-investigation Appointment Required"
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(
        page
    ).click_post_investigation_appointment_required_button()

    # Then my subject has been updated as follows:
    AdvanceFOBTScreeningEpisodePage(page).verify_latest_event_status_value(
        "A360 - Post-investigation Appointment Required"
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
        criteria={
            "latest event status": "A410 Post-investigation Appointment Made",
        },
    )

    # And there is a "A410" letter batch for my subject with the exact title "Post-Investigation Appointment Invitation Letter"
    # When I process the open "A410" letter batch for my subject
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
        },
    )

    # Then my subject has been updated as follows:
    subject_assertion(
        nhs_no,
        {
            "latest episode includes event status": "A316 Post-investigation Appointment Attended",
            "latest event status": "A430 Post-investigation Appointment Attended - Diagnostic Result Letter not Printed",
        },
    )

    # And there is a "A430" letter batch for my subject with the exact title "Result Letters Following Post-investigation Appointment"
    # When I process the open "A430" letter batch for my subject
    batch_processing(
        page,
        "A430",
        "Result Letters Following Post-investigation Appointment",
        "S61 - Normal (No Abnormalities Found) ",
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
        "latest episode accumulated result": "Normal (No Abnormalities Found)",
        "latest episode recall calculation method": "Diagnostic Test Date",
        "latest episode recall episode type": "FOBT Screening",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Closed",
        "latest episode status reason": "Episode Complete",
        "latest event status": "S61 Normal (No Abnormalities Found)",
        "lynch due date": "Null",
        "lynch due date date of change": "Unchanged",
        "lynch due date reason": "Unchanged",
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

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I reopen the subject's episode for "Reopen to Confirm Diagnostic Test Result and Outcome"
    SubjectScreeningSummaryPage(page).click_reopen_fobt_screening_episode_button()
    ReopenFOBTScreeningEpisodePage(
        page
    ).click_reopen_to_confirm_diagnostic_test_result_and_outcome_button()

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
        "diagnostic test has outcome": "No",
        "diagnostic test has result": "Normal (No Abnormalities Found)",
        "latest episode accumulated result": "Normal (No Abnormalities Found)",
        "latest episode includes event code": "E67 Reopen to Confirm Diagnostic Test Result and Outcome",
        "latest episode recall calculation method": "Null",
        "latest episode recall episode type": "Null",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Open",
        "latest episode status reason": "Null",
        "latest event status": "A416 Post-investigation Appointment Attended",
        "lynch due date": "Null",
        "lynch due date date of change": "Unchanged",
        "lynch due date reason": "Unchanged",
        "screening due date": "Calculated FOBT Due Date",
        "screening due date date of change": "Today",
        "screening due date reason": "Reopened episode",
        "surveillance due date": "Null",
        "surveillance due date date of change": "Unchanged",
        "surveillance due date reason": "Unchanged",
    }
    subject_assertion(nhs_no, criteria)

    # When I receive an SSPI update to change their date of birth to "32" years old
    SSPIChangeSteps().sspi_update_to_change_dob_received(nhs_no, 32)

    # Then my subject has been updated as follows:
    subject_assertion(nhs_no, {"subject age": "32"})

    # When I view the subject
    screening_subject_page_searcher.navigate_to_subject_summary_page(page, nhs_no)

    # And I select the advance episode option for "Enter Diagnostic Test Outcome"
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_enter_diagnostic_test_outcome_button()

    # And I select Outcome of Diagnostic Test "Investigation Complete"
    DiagnosticTestOutcomePage(page).select_test_outcome_option(
        OutcomeOfDiagnosticTest.INVESTIGATION_COMPLETE
    )

    # And I save the Diagnostic Test Outcome
    DiagnosticTestOutcomePage(page).click_save_button()

    # Then my subject has been updated as follows:
    criteria = {
        "which diagnostic test": "Latest not-void test in latest episode",
        "diagnostic test has outcome": "Investigation Complete",
        "diagnostic test has result": "Normal (No Abnormalities Found)",
        "latest episode includes event status": "A316 Post-investigation Appointment Attended",
        "latest episode accumulated result": "Normal (No Abnormalities Found)",
        "latest event status": "A430 Post-investigation Appointment Attended - Diagnostic Result Letter not Printed",
    }
    subject_assertion(nhs_no, criteria)

    # When I process the open "A430" letter batch for my subject
    batch_processing(
        page,
        "A430",
        "Result Letters Following Post-investigation Appointment",
        "S61 - Normal (No Abnormalities Found) ",
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
        "latest episode accumulated result": "Normal (No Abnormalities Found)",
        "latest episode recall calculation method": "Diagnostic Test Date",
        "latest episode recall episode type": "FOBT Screening",
        "latest episode recall surveillance type": "Null",
        "latest episode status": "Closed",
        "latest episode status reason": "Episode Complete",
        "latest event status": "S61 Normal (No Abnormalities Found)",
        "lynch due date": "Null",
        "lynch due date date of change": "Unchanged",
        "lynch due date reason": "Unchanged",
        "screening due date": "Null",
        "screening due date date of change": "Today",
        "screening due date reason": "Awaiting failsafe",
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
