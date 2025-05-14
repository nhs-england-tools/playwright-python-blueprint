import pytest
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.user_tools import UserTools
from utils.screening_subject_page_searcher import verify_subject_event_status_by_nhs_no
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from utils.batch_processing import batch_processing
from pages.logout.log_out_page import LogoutPage
from pages.datasets.subject_datasets_page import SubjectDatasetsPage
from pages.screening_subject_search.handover_into_symptomatic_care_page import (
    HandoverIntoSymptomaticCarePage
)
from utils.calendar_picker import CalendarPicker
from datetime import datetime
from pages.screening_subject_search.record_diagnosis_date_page import (
    RecordDiagnosisDatePage,
)
from pages.screening_subject_search.diagnostic_test_outcome_page import (
    DiagnosticTestOutcomePage,OutcomeOfDiagnosticTest
)
from pages.datasets.investigation_dataset_page import (
    InvestigationDatasetsPage,
    SiteLookupOptions,
    PractitionerOptions,
    TestingClinicianOptions,
    AspirantEndoscopistOptions,
    DrugTypeOptions,
    BowelPreparationQualityOptions,
    ComfortOptions,
    EndoscopyLocationOptions,
    YesNoOptions,
    InsufflationOptions,
    OutcomeAtTimeOfProcedureOptions,
    LateOutcomeOptions,
    CompletionProofOptions,
    FailureReasonsOptions,
    PolypClassificationOptions,
    PolypAccessOptions,
    PolypInterventionModalityOptions,
    PolypInterventionDeviceOptions,
    PolypInterventionExcisionTechniqueOptions,
)
from pages.screening_subject_search.advance_fobt_screening_episode_page import (
    AdvanceFOBTScreeningEpisodePage,
)


# This should go into a util. Adding it here to avoid SonarQube duplication errors:
def go_to_investigation_datasets_page(page: Page, nhs_no) -> None:
    verify_subject_event_status_by_nhs_no(
        page, nhs_no, "A323 - Post-investigation Appointment NOT Required"
    )

    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()


def default_investigation_dataset_forms(page: Page) -> None:
    # Investigation Dataset
    InvestigationDatasetsPage(page).select_site_lookup_option(SiteLookupOptions.RL401)
    InvestigationDatasetsPage(page).select_practitioner_option(
        PractitionerOptions.AMID_SNORING
    )
    InvestigationDatasetsPage(page).select_testing_clinician_option(
        TestingClinicianOptions.BORROWING_PROPERTY
    )
    InvestigationDatasetsPage(page).select_aspirant_endoscopist_option(
        AspirantEndoscopistOptions.ITALICISE_AMNESTY
    )
    # Drug Information
    InvestigationDatasetsPage(page).click_show_drug_information()
    InvestigationDatasetsPage(page).select_drug_type_option1(DrugTypeOptions.BISACODYL)
    InvestigationDatasetsPage(page).fill_drug_type_dose1("10")
    # Ensocopy Information
    InvestigationDatasetsPage(page).click_show_endoscopy_information()
    InvestigationDatasetsPage(page).check_endoscope_inserted_yes()


def default_investigation_dataset_forms_continuation(page: Page) -> None:
    InvestigationDatasetsPage(page).select_bowel_preparation_quality_option(
        BowelPreparationQualityOptions.GOOD
    )
    InvestigationDatasetsPage(page).select_comfort_during_examination_option(
        ComfortOptions.NO_DISCOMFORT
    )
    InvestigationDatasetsPage(page).select_comfort_during_recovery_option(
        ComfortOptions.NO_DISCOMFORT
    )
    InvestigationDatasetsPage(page).select_endoscopist_defined_extent_option(
        EndoscopyLocationOptions.ILEUM
    )
    InvestigationDatasetsPage(page).select_scope_imager_used_option(YesNoOptions.YES)
    InvestigationDatasetsPage(page).select_retorted_view_option(YesNoOptions.NO)
    InvestigationDatasetsPage(page).fill_start_of_intubation_time("09:00")
    InvestigationDatasetsPage(page).fill_start_of_extubation_time("09:15")
    InvestigationDatasetsPage(page).fill_end_time_of_procedure("09:30")
    InvestigationDatasetsPage(page).fill_scope_id("A1")
    InvestigationDatasetsPage(page).select_insufflation_option(InsufflationOptions.AIR)
    InvestigationDatasetsPage(page).select_outcome_at_time_of_procedure_option(
        OutcomeAtTimeOfProcedureOptions.LEAVE_DEPARTMENT
    )
    InvestigationDatasetsPage(page).select_late_outcome_option(
        LateOutcomeOptions.NO_COMPLICATIONS
    )
    InvestigationDatasetsPage(page).click_show_completion_proof_information()
    # Completion Proof Information
    InvestigationDatasetsPage(page).select_completion_proof_option(
        CompletionProofOptions.PHOTO_ILEO
    )


def investigation_datasets_failure_reason(page: Page) -> None:
    # Failure Information
    InvestigationDatasetsPage(page).click_show_failure_information()
    InvestigationDatasetsPage(page).select_failure_reasons_option(
        FailureReasonsOptions.BLEEDING_INCIDENT
    )


def polyps_for_high_risk_result(page: Page) -> None:
    # Polyp Information
    InvestigationDatasetsPage(page).click_add_polyp_button()
    InvestigationDatasetsPage(page).select_polyp1_location_option(
        EndoscopyLocationOptions.ILEUM
    )
    InvestigationDatasetsPage(page).select_polyp1_classification_option(
        PolypClassificationOptions.LS
    )
    InvestigationDatasetsPage(page).fill_polyp1_size("15")
    InvestigationDatasetsPage(page).select_polyp1_access_option(
        PolypAccessOptions.NOT_KNOWN
    )
    polyp1_intervention(page)
    InvestigationDatasetsPage(page).click_add_polyp_button()
    InvestigationDatasetsPage(page).select_polyp2_location_option(
        EndoscopyLocationOptions.CAECUM
    )
    InvestigationDatasetsPage(page).select_polyp2_classification_option(
        PolypClassificationOptions.LS
    )
    InvestigationDatasetsPage(page).fill_polyp2_size("15")
    InvestigationDatasetsPage(page).select_polyp2_access_option(
        PolypAccessOptions.NOT_KNOWN
    )
    InvestigationDatasetsPage(page).click_polyp2_add_intervention_button()
    InvestigationDatasetsPage(page).select_polyp2_intervention_modality_option(
        PolypInterventionModalityOptions.EMR
    )
    InvestigationDatasetsPage(page).select_polyp2_intervention_device_option(
        PolypInterventionDeviceOptions.HOT_SNARE
    )
    InvestigationDatasetsPage(page).select_polyp2_intervention_excised_option(
        YesNoOptions.YES
    )
    InvestigationDatasetsPage(page).select_polyp2_intervention_retrieved_option(
        YesNoOptions.NO
    )
    InvestigationDatasetsPage(
        page
    ).select_polyp2_intervention_excision_technique_option(
        PolypInterventionExcisionTechniqueOptions.EN_BLOC
    )


def polyps_for_lnpcp_result(page: Page) -> None:
    # Polyp Information
    InvestigationDatasetsPage(page).click_add_polyp_button()
    InvestigationDatasetsPage(page).select_polyp1_location_option(
        EndoscopyLocationOptions.ILEUM
    )
    InvestigationDatasetsPage(page).select_polyp1_classification_option(
        PolypClassificationOptions.LS
    )
    InvestigationDatasetsPage(page).fill_polyp1_size("30")
    InvestigationDatasetsPage(page).select_polyp1_access_option(
        PolypAccessOptions.NOT_KNOWN
    )
    polyp1_intervention(page)


def polyp1_intervention(page: Page) -> None:
    InvestigationDatasetsPage(page).click_polyp1_add_intervention_button()
    InvestigationDatasetsPage(page).select_polyp1_intervention_modality_option(
        PolypInterventionModalityOptions.POLYPECTOMY
    )
    InvestigationDatasetsPage(page).select_polyp1_intervention_device_option(
        PolypInterventionDeviceOptions.HOT_SNARE
    )
    InvestigationDatasetsPage(page).select_polyp1_intervention_excised_option(
        YesNoOptions.YES
    )
    InvestigationDatasetsPage(page).select_polyp1_intervention_retrieved_option(
        YesNoOptions.NO
    )
    InvestigationDatasetsPage(
        page
    ).select_polyp1_intervention_excision_technique_option(
        PolypInterventionExcisionTechniqueOptions.EN_BLOC
    )


def save_investigation_dataset(page: Page) -> None:
    InvestigationDatasetsPage(page).check_dataset_complete_checkbox()
    InvestigationDatasetsPage(page).click_save_dataset_button()


def after_high_risk_result(page: Page) -> None:
    InvestigationDatasetsPage(page).expect_text_to_be_visible("High-risk findings")
    BasePage(page).click_back_button()

    # The following code is on the subject datasets page
    expect(page.get_by_text("** Completed **").nth(1)).to_be_visible()
    BasePage(page).click_back_button()

    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    # The following code is on the advance fobt screening episode page
    AdvanceFOBTScreeningEpisodePage(page).click_enter_diagnostic_test_outcome_button()

    # The following code is on the diagnostic test outcome page
    DiagnosticTestOutcomePage(page).verify_diagnostic_test_outcome("High-risk findings")
    DiagnosticTestOutcomePage(page).select_test_outcome_option(OutcomeOfDiagnosticTest.REFER_SURVEILLANCE)
    DiagnosticTestOutcomePage(page).click_save_button()

def after_lnpcp_result(page: Page) -> None:
    InvestigationDatasetsPage(page).expect_text_to_be_visible("LNPCP")
    BasePage(page).click_back_button()

    # The following code is on the subject datasets page
    expect(page.get_by_text("** Completed **").nth(1)).to_be_visible()
    BasePage(page).click_back_button()

    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # The following code is on the advance fobt screening episode page
    AdvanceFOBTScreeningEpisodePage(page).click_enter_diagnostic_test_outcome_button()

    # The following code is on the diagnostic test outcome page
    DiagnosticTestOutcomePage(page).verify_diagnostic_test_outcome("LNPCP")
    DiagnosticTestOutcomePage(page).select_test_outcome_option(OutcomeOfDiagnosticTest.REFER_SURVEILLANCE)
    DiagnosticTestOutcomePage(page).click_save_button()

def handover_subject_to_symptomatic_care(page: Page) -> None:
    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A394 - Handover into Symptomatic Care for Surveillance - Patient Age"
    )
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # The following code is on the advance fobt screening episode page
    AdvanceFOBTScreeningEpisodePage(page).click_handover_into_symptomatic_care_button()

    # The following code is on the handover into symptomatic care page
    HandoverIntoSymptomaticCarePage(page).select_referral_dropdown_option("20445")
    HandoverIntoSymptomaticCarePage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())
    HandoverIntoSymptomaticCarePage(page).select_consultant("201")
    HandoverIntoSymptomaticCarePage(page).fill_notes("Test Automation")
    HandoverIntoSymptomaticCarePage(page).click_save_button()

    SubjectScreeningSummaryPage(page).wait_for_page_title()
    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A385 - Handover into Symptomatic Care"
    )


@pytest.mark.vpn_required
@pytest.mark.smokescreen
@pytest.mark.compartment6
def test_compartment_6(page: Page, smokescreen_properties: dict) -> None:
    """
    This is the main compartment 6 method
    Filling out the investigation datasets for different subjects to get different results for a diagnostic test.
    Printing the diagnostic test result letters.
    """

    # For the following tests old refers to if they are over 75 at recall
    # The recall period is 2 years from the last diagnostic test for a Normal or Abnormal diagnostic test result
    # or 3 years for someone who is going in to Surveillance (High-risk findings or LNPCP)

    UserTools.user_login(page, "Screening Centre Manager at BCS001")

    # This needs to be repeated for two subjects, one old and one not - High Risk Result
    # Older patient
    nhs_no = "9772286785"
    go_to_investigation_datasets_page(page, nhs_no)

    # The following code is on the investigation datasets page
    default_investigation_dataset_forms(page)
    InvestigationDatasetsPage(page).select_theraputic_procedure_type()
    default_investigation_dataset_forms_continuation(page)
    investigation_datasets_failure_reason(page)
    polyps_for_high_risk_result(page)
    save_investigation_dataset(page)
    after_high_risk_result(page)

    handover_subject_to_symptomatic_care(page)

    # Younger patient
    nhs_no = "9802397318"
    go_to_investigation_datasets_page(page, nhs_no)

    # The following code is on the investigation datasets page
    default_investigation_dataset_forms(page)
    InvestigationDatasetsPage(page).select_theraputic_procedure_type()
    default_investigation_dataset_forms_continuation(page)
    investigation_datasets_failure_reason(page)
    polyps_for_high_risk_result(page)
    save_investigation_dataset(page)
    after_high_risk_result(page)

    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A318 - Post-investigation Appointment NOT Required - Result Letter Created"
    )
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # The following code is on the advance fobt screening episode page
    AdvanceFOBTScreeningEpisodePage(page).click_record_diagnosis_date_button()

    # The following code is on the record diagnosis date page
    RecordDiagnosisDatePage(page).enter_date_in_diagnosis_date_field(datetime.today())
    RecordDiagnosisDatePage(page).click_save_button()

    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A318 - Post-investigation Appointment NOT Required - Result Letter Created"
    )

    # This needs to be repeated for two subjects, one old and one not - LNPCP Result
    # Older patient
    nhs_no = "9359523194"
    go_to_investigation_datasets_page(page, nhs_no)

    # The following code is on the investigation datasets page
    default_investigation_dataset_forms(page)
    InvestigationDatasetsPage(page).select_theraputic_procedure_type()
    default_investigation_dataset_forms_continuation(page)
    investigation_datasets_failure_reason(page)
    polyps_for_lnpcp_result(page)
    save_investigation_dataset(page)
    after_lnpcp_result(page)

    handover_subject_to_symptomatic_care(page)

    # Younger patient
    nhs_no = "9828941813"
    go_to_investigation_datasets_page(page, nhs_no)

    # The following code is on the investigation datasets page
    default_investigation_dataset_forms(page)
    InvestigationDatasetsPage(page).select_theraputic_procedure_type()
    default_investigation_dataset_forms_continuation(page)
    investigation_datasets_failure_reason(page)
    polyps_for_lnpcp_result(page)
    save_investigation_dataset(page)
    after_lnpcp_result(page)
    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A318 - Post-investigation Appointment NOT Required - Result Letter Created"
    )
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # The following code is on the advance fobt screening episode page
    AdvanceFOBTScreeningEpisodePage(page).click_record_diagnosis_date_button()

    # The following code is on the record diagnosis date page
    RecordDiagnosisDatePage(page).enter_date_in_diagnosis_date_field(datetime.today())
    RecordDiagnosisDatePage(page).click_save_button()

    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A318 - Post-investigation Appointment NOT Required - Result Letter Created"
    )

    # This needs to be repeated for 1 subject, age does not matter - Normal Result
    nhs_no_normal = "9852356488"
    go_to_investigation_datasets_page(page, nhs_no_normal)

    # The following code is on the investigation datasets page
    default_investigation_dataset_forms(page)
    InvestigationDatasetsPage(page).select_diagnostic_procedure_type()
    default_investigation_dataset_forms_continuation(page)
    InvestigationDatasetsPage(page).click_show_failure_information()
    InvestigationDatasetsPage(page).select_failure_reasons_option(
        FailureReasonsOptions.NO_FAILURE_REASONS
    )
    save_investigation_dataset(page)
    InvestigationDatasetsPage(page).expect_text_to_be_visible(
        "Normal (No Abnormalities"
    )
    BasePage(page).click_back_button()

    # The following code is on the subject datasets page
    expect(page.get_by_text("** Completed **").nth(1)).to_be_visible()
    BasePage(page).click_back_button()

    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # The following code is on the advance fobt screening episode page
    AdvanceFOBTScreeningEpisodePage(page).click_enter_diagnostic_test_outcome_button()

    # The following code is on the diagnostic test outcome page
    DiagnosticTestOutcomePage(page).verify_diagnostic_test_outcome(
        "Normal (No Abnormalities"
    )
    DiagnosticTestOutcomePage(page).select_test_outcome_option(OutcomeOfDiagnosticTest.INVESTIGATION_COMPLETE)
    DiagnosticTestOutcomePage(page).click_save_button()

    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A318 - Post-investigation Appointment NOT Required - Result Letter Created"
    )
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    # The following code is on the advance fobt screening episode page
    AdvanceFOBTScreeningEpisodePage(page).click_record_diagnosis_date_button()

    # The following code is on the record diagnosis date page
    RecordDiagnosisDatePage(page).enter_date_in_diagnosis_date_field(datetime.today())
    RecordDiagnosisDatePage(page).click_save_button()

    batch_processing(
        page,
        "A318",
        "Result Letters - No Post-investigation Appointment",
        [
            "S61 - Normal (No Abnormalities Found)",
            "A158 - High-risk findings",
            "A157 - LNPCP",
        ],
    )

    # This is to check for the status of a normal subject as this NHS Number cannot be retrieved from the DB
    verify_subject_event_status_by_nhs_no(
        page, nhs_no_normal, "S61 - Normal (No Abnormalities Found)"
    )

    batch_processing(
        page,
        "A385",
        "Handover into Symptomatic Care Adenoma Surveillance, Age - GP Letter",
        "A382 - Handover into Symptomatic Care - GP Letter Printed",
    )

    batch_processing(
        page,
        "A382",
        "Handover into Symptomatic Care Adenoma Surveillance - Patient Letter",
        "P202 - Waiting Completion of Outstanding Events",
    )

    LogoutPage(page).log_out()
