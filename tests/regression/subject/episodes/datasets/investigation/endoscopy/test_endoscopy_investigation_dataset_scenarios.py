import logging
import pytest
from playwright.sync_api import Page
from pages.logout.log_out_page import LogoutPage
from pages.base_page import BasePage
from pages.datasets.investigation_dataset_page import (
    InvestigationDatasetsPage,
    EndoscopyLocationOptions,
    YesNoOptions,
    FailureReasonsOptions,
    PolypClassificationOptions,
    PolypAccessOptions,
    PolypInterventionModalityOptions,
    PolypInterventionDeviceOptions,
    PolypInterventionExcisionTechniqueOptions,
    CompletionProofOptions,
    ReasonPathologyLostOptions,
    DrugTypeOptions,
    YesNoDrugOptions,
    AntibioticsAdministeredDrugTypeOptions,
    OtherDrugsAdministeredDrugTypeOptions,
    EndoscopeNotInsertedOptions,
    BowelPreparationQualityOptions,
    SedationOptions,
)
from classes.user import User
from classes.subject import Subject
from utils.oracle.oracle import OracleDB
from utils.oracle.subject_selection_query_builder import SubjectSelectionQueryBuilder
from pages.datasets.subject_datasets_page import SubjectDatasetsPage
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from utils.investigation_dataset import (
    InvestigationDatasetCompletion,
)
from utils.screening_subject_page_searcher import (
    search_subject_episode_by_nhs_number,
)
from utils.user_tools import UserTools
from utils.datasets.investigation_datasets import (
    get_default_general_information,
    get_default_drug_information,
    get_default_endoscopy_information,
)
from copy import deepcopy
from pages.organisations.organisations_page import OrganisationSwitchPage
from pages.login.select_job_role_page import SelectJobRolePage
from typing import Optional
from utils.dataset_field_util import DatasetFieldUtil

general_information = get_default_general_information()

drug_information = get_default_drug_information()

endoscopy_information = get_default_endoscopy_information()

bowel_preparation_administered_string = "Bowel Preparation Administered"
antibiotics_administered_string = "Antibiotics Administered"
other_drugs_administered_string = "Other Drugs Administered"
general_anaesthetic_string = "General Anaesthetic"
sedation_during_recovery_string = "Sedation during recovery"
sedation_during_examination_string = "Sedation during examination"
div_drug_details_string = "divDrugDetails"
div_sedation_exam_string = "divSedationExam"
div_sedation_recovery_string = "divSedationRecovery"


@pytest.mark.regression
@pytest.mark.vpn_required
@pytest.mark.investigation_dataset_tests
@pytest.mark.bcss_additional_tests
@pytest.mark.colonoscopy_dataset_tests
@pytest.mark.skip(reason="Marked with ignore tag in the Selenium Framework")
def test_record_a_dataset_with_100_polyps_or_more(
    page: Page,
) -> None:
    """
    Scenario: I want to record a dataset with 100 polyps or more (amend number in test below)
    """

    # Number of times to repeat the entries
    number_of_repeats = 100
    logging.info(f"Number of Polyps to add: {number_of_repeats}")

    criteria = {
        "latest episode status": "open",
        "latest episode latest investigation dataset": "colonoscopy_new",
        "latest event status": "A259",
    }
    user = User()
    subject = Subject()

    builder = SubjectSelectionQueryBuilder()

    query, bind_vars = builder.build_subject_selection_query(
        criteria=criteria,
        user=user,
        subject=subject,
        subjects_to_retrieve=1,
    )

    df = OracleDB().execute_query(query, bind_vars)
    nhs_no = df.iloc[0]["subject_nhs_number"]
    logging.info(f"NHS Number: {nhs_no}")

    UserTools.user_login(page, "Screening Centre Manager at BCS001")
    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)

    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    endoscopy_information["endoscopist defined extent"] = EndoscopyLocationOptions.ILEUM

    drug_info_list = [
        (DrugTypeOptions.BISACODYL, "10"),
        (DrugTypeOptions.CITRAFLEET, "20"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, bowel_preparation_administered_string
    )

    failure_information = {
        "failure reasons": FailureReasonsOptions.NO_FAILURE_REASONS,
    }

    completion_information = {
        "completion proof": CompletionProofOptions.PHOTO_ILEO,
    }

    polyp_information = [
        {
            "location": EndoscopyLocationOptions.RECTUM,
            "classification": PolypClassificationOptions.IIA,
            "estimate of whole polyp size": "1",
            "polyp access": PolypAccessOptions.EASY,
            "left in situ": YesNoOptions.NO,
        }
    ]

    polyp_intervention = [
        {
            "modality": PolypInterventionModalityOptions.POLYPECTOMY,
            "device": PolypInterventionDeviceOptions.HOT_SNARE,
            "excised": YesNoOptions.YES,
            "retrieved": YesNoOptions.YES,
            "excision technique": PolypInterventionExcisionTechniqueOptions.PIECE_MEAL,
        }
    ]

    polyp_histology = [
        {
            "pathology lost": YesNoOptions.YES,
            "reason pathology lost": ReasonPathologyLostOptions.LOST_IN_TRANSIT,
        }
    ]

    # Create new lists with X repeated deep copies of the initial dicts
    polyp_information = [
        deepcopy(polyp_information[0]) for _ in range(number_of_repeats)
    ]
    polyp_intervention = [
        deepcopy(polyp_intervention[0]) for _ in range(number_of_repeats)
    ]
    polyp_histology = [deepcopy(polyp_histology[0]) for _ in range(number_of_repeats)]

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

    InvestigationDatasetsPage(page).expect_text_to_be_visible("High-risk findings")
    LogoutPage(page).log_out()


@pytest.mark.regression
@pytest.mark.vpn_required
@pytest.mark.investigation_dataset_tests
@pytest.mark.bcss_additional_tests
@pytest.mark.colonoscopy_dataset_tests
def test_check_different_hub_roles_access_to_edit_endoscopy_investigation_dataset(
    page: Page,
) -> None:
    """
    Scenario: Check different hub roles' access to edit an endoscopy investigation dataset
    This scenario only checks roles which have permission to at least view a dataset.
    """
    nhs_no = get_subject_with_incomplete_endoscopy_investigation_dataset()

    check_role_access_to_edit_investigation_dataset(
        page,
        nhs_no,
        role="Hub Director State Registered at BCS03",
        edit_access=False,
        role_logging="ROLE: Hub Director - state registered : view only",
    )

    LogoutPage(page).log_out(False)

    check_role_access_to_edit_investigation_dataset(
        page,
        nhs_no,
        role="Hub Manager at BCS01",
        edit_access=False,
        role_logging="ROLE: Hub Manager : view only",
    )

    LogoutPage(page).log_out(False)

    check_role_access_to_edit_investigation_dataset(
        page,
        nhs_no,
        role="Hub Manager State Registered at BCS01",
        edit_access=False,
        role_logging="ROLE: Hub Manager - state registered : view only",
    )

    LogoutPage(page).log_out(False)

    check_role_access_to_edit_investigation_dataset(
        page,
        nhs_no,
        role="Team Leader at BCS01",
        edit_access=False,
        role_logging="ROLE: Team Leader : view only",
    )

    LogoutPage(page).log_out(False)

    check_role_access_to_edit_investigation_dataset(
        page,
        nhs_no,
        role="Senior Screening Assistant at BCS01",
        edit_access=False,
        role_logging="ROLE: Senior Screening Assistant : view only",
    )

    LogoutPage(page).log_out(False)

    check_role_access_to_edit_investigation_dataset(
        page,
        nhs_no,
        role="Screening Assistant at BCS02",
        edit_access=False,
        role_logging="ROLE: Screening Assistant : view only",
    )

    LogoutPage(page).log_out()


@pytest.mark.regression
@pytest.mark.vpn_required
@pytest.mark.investigation_dataset_tests
@pytest.mark.bcss_additional_tests
@pytest.mark.colonoscopy_dataset_tests
def test_check_different_screening_centre_roles_access_to_edit_endoscopy_investigation_dataset(
    page: Page,
) -> None:
    """
    Scenario: Check different screening centre roles' access to edit an endoscopy investigation dataset
    This scenario only checks roles which have permission to at least view a dataset.
    """
    nhs_no = get_subject_with_incomplete_endoscopy_investigation_dataset()

    check_role_access_to_edit_investigation_dataset(
        page,
        nhs_no,
        role="Screening Centre Manager at BCS001",
        edit_access=True,
        role_logging="ROLE: Screening Centre Manager : edit",
    )

    LogoutPage(page).log_out(False)

    check_role_access_to_edit_investigation_dataset(
        page,
        nhs_no,
        role="Specialist Screening Practitioner at BCS009 & BCS001",
        edit_access=True,
        role_logging="ROLE: Specialist Screening Practitioner (SSP) : edit",
    )

    LogoutPage(page).log_out(False)

    check_role_access_to_edit_investigation_dataset(
        page,
        nhs_no,
        role="Screening Practitioner at BCS001",
        edit_access=True,
        role_logging="ROLE: Screening Practitioner (SP) : edit",
        role_type="Screening Practitioner",
    )

    LogoutPage(page).log_out(False)

    check_role_access_to_edit_investigation_dataset(
        page,
        nhs_no,
        role="Assistant Screening Practitioner at BCS001",
        edit_access=True,
        role_logging="ROLE: Assistant Screening Practitioner (ASP) : edit",
    )

    LogoutPage(page).log_out(False)

    check_role_access_to_edit_investigation_dataset(
        page,
        nhs_no,
        role="BCSS Support - SC at BCS001",
        edit_access=True,
        role_logging="ROLE: BCSS Support - SC : edit",
    )

    LogoutPage(page).log_out(False)

    check_role_access_to_edit_investigation_dataset(
        page,
        nhs_no,
        role="Screening Coordinator at BCS001",
        edit_access=False,
        role_logging="ROLE: FS Screening Coordinator : view only",
        role_type="FS Screening Coordinator",
    )

    LogoutPage(page).log_out(False)

    check_role_access_to_edit_investigation_dataset(
        page,
        nhs_no,
        role="Screening Centre Clerk at BCS001",
        edit_access=False,
        role_logging="ROLE: Screening Centre Clerk : view only",
        role_type="Screening Centre Clerk",
    )

    LogoutPage(page).log_out()


@pytest.mark.regression
@pytest.mark.vpn_required
@pytest.mark.investigation_dataset_tests
@pytest.mark.bcss_additional_tests
@pytest.mark.colonoscopy_dataset_tests
def test_check_different_national_and_qa_roles_access_to_edit_endoscopy_investigation_dataset(
    page: Page,
) -> None:
    """
    Scenario: Check different national and QA roles' access to edit an endoscopy investigation dataset
    This scenario only checks roles which have permission to at least view a dataset.
    """
    nhs_no = get_subject_with_incomplete_endoscopy_investigation_dataset()

    check_role_access_to_edit_investigation_dataset(
        page,
        nhs_no,
        role="National Data Analyst at BCS0",
        edit_access=False,
        role_logging="ROLE: National Data Analyst : view only",
    )

    LogoutPage(page).log_out(False)

    check_role_access_to_edit_investigation_dataset(
        page,
        nhs_no,
        role="National QA User at BCS0",
        edit_access=False,
        role_logging="ROLE: National QA User : view only",
    )

    LogoutPage(page).log_out()


@pytest.mark.regression
@pytest.mark.vpn_required
@pytest.mark.investigation_dataset_tests
@pytest.mark.bcss_additional_tests
@pytest.mark.colonoscopy_dataset_tests
def test_check_correct_sections_displayed_in_colonoscopy_investigation_dataset(
    page: Page,
) -> None:
    """
    Scenario: Check the correct sections are displayed in new Colonoscopy investigation dataset
    This scenario just checks that the dataset contains the expected sections and that they are labelled for an endoscopy dataset rather than a radiology dataset.
    """
    nhs_no = get_subject_with_new_colonoscopy_investigation_dataset()

    UserTools.user_login(page, "Screening Centre Manager at BCS001")
    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)

    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    InvestigationDatasetsPage(page).bowel_cancer_screening_page_title_contains_text(
        "Investigation Datasets"
    )

    assert (
        InvestigationDatasetsPage(page).is_dataset_section_present(
            "Investigation Dataset"
        )
        is True
    ), "'Investigation Dataset' section should exist"
    assert (
        InvestigationDatasetsPage(page).is_dataset_section_present("Drug Information")
        is True
    ), "'Drug Information' section should exist"
    assert (
        InvestigationDatasetsPage(page).is_dataset_section_present(
            "Contrast, Tagging & Drug Information"
        )
        is False
    ), "'Contrast, Tagging & Drug Information' section should NOT exist"
    assert (
        InvestigationDatasetsPage(page).is_dataset_section_present(
            "Endoscopy Information"
        )
        is True
    ), "'Endoscopy Information' section should exist"
    assert (
        InvestigationDatasetsPage(page).is_dataset_section_present(
            "Radiology Information"
        )
        is False
    ), "'Radiology Information' section should NOT exist"
    assert (
        InvestigationDatasetsPage(page).is_dataset_section_present(
            "Completion Proof Information"
        )
        is True
    ), "'Completion Proof Information' section should exist"
    assert (
        InvestigationDatasetsPage(page).is_dataset_section_present(
            "Failure Information"
        )
        is True
    ), "'Failure Information' section should exist"
    assert (
        InvestigationDatasetsPage(page).is_dataset_section_present("Polyp Information")
        is True
    ), "'Polyp Information' section should exist"
    assert (
        InvestigationDatasetsPage(page).is_dataset_section_present(
            "Suspected Polyp Information"
        )
        is False
    ), "'Suspected Polyp Information' section should NOT exist"
    assert (
        InvestigationDatasetsPage(page).is_dataset_section_present(
            "Colorectal Cancer Information"
        )
        is True
    ), "'Colorectal Cancer Information' section should exist"
    assert (
        InvestigationDatasetsPage(page).is_dataset_section_present(
            "Suspected Colorectal Cancer Information"
        )
        is False
    ), "'Suspected Colorectal Cancer Information' section should NOT exist"
    assert (
        InvestigationDatasetsPage(page).is_dataset_section_present(
            "Complication Information"
        )
        is True
    ), "'Complication Information' section should exist"
    assert (
        InvestigationDatasetsPage(page).is_dataset_section_present("Other Findings")
        is True
    ), "'Other Findings' section should exist"
    assert (
        InvestigationDatasetsPage(page).is_dataset_section_present("Suspected Findings")
        is False
    ), "'Suspected Findings' section should NOT exist"
    LogoutPage(page).log_out()


@pytest.mark.regression
@pytest.mark.vpn_required
@pytest.mark.investigation_dataset_tests
@pytest.mark.bcss_additional_tests
@pytest.mark.colonoscopy_dataset_tests
def test_check_field_visibility_and_default_values_in_colonoscopy_investigation_dataset(
    page: Page,
) -> None:
    """
    Scenario: Check field visibility and default values in the Investigation Dataset section of a new Colonoscopy investigation dataset
    The top section of the investigation dataset, labelled Investigation Dataset but referred to as the Diagnostic Test section in the spec, contains mostly read-only fields.  This scenario checks that the expected fields are included, and carries out limited checks of the default values (many of these values can only be sensibly tested in a scenario which creates the test from scratch).
    """
    nhs_no = get_subject_with_new_colonoscopy_investigation_dataset()

    UserTools.user_login(page, "Screening Centre Manager at BCS001")
    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)

    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    InvestigationDatasetsPage(page).bowel_cancer_screening_page_title_contains_text(
        "Investigation Datasets"
    )

    field_names = [
        "Proposed Type of Test",
        "Actual Type of Test",
        "First Offered Appointment Date",
        "Actual Appointment Date",
        "Attended Screening Centre",
        "Diagnostic Test Result",
        "Outcome of Diagnostic Test",
        "Reason for Onward Referral",
        "Onward Referring Clinician",
        "Site",
        "Practitioner in Attendance",
        "Name of Practitioner",
        "Testing Clinician",
        "Resect and Discard Accreditation",
        "Aspirant Endoscopist",
        "Number of Polyps Seen",
        "Number of Polyps Excised",
        "Number of Polyps Resected & Discarded",
        "Number of Polyps Retrieved",
        "Number of Cancers Seen",
        "Dataset Last Updated",
        "Dataset Complete?",
    ]
    InvestigationDatasetsPage(page).are_fields_on_page(
        "Investigation Dataset", None, field_names
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Actual Type of Test", "Colonoscopy"
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Practitioner in Attendance", "Yes"
    )

    DatasetFieldUtil(page).assert_select_to_right_has_values(
        "Practitioner in Attendance", ["Yes", "No"]
    )

    DatasetFieldUtil(page).assert_checkbox_to_right_is_ticked_or_not(
        "Aspirant Endoscopist", "Unticked"
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Number of Polyps Seen", "0"
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Number of Polyps Excised", "0"
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Number of Polyps Resected & Discarded", "0"
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Number of Polyps Retrieved", "0"
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Number of Cancers Seen", "0"
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Dataset Last Updated", ""
    )

    DatasetFieldUtil(page).assert_radio_to_right_is_selected("Dataset Complete?", "No")
    LogoutPage(page).log_out()


@pytest.mark.regression
@pytest.mark.vpn_required
@pytest.mark.investigation_dataset_tests
@pytest.mark.bcss_additional_tests
@pytest.mark.colonoscopy_dataset_tests
def test_check_cross_field_validation_is_mandatory_at_completion(page: Page) -> None:
    """
    Scenario: Check cross-field validation between Practitioner In Attendance and Name of Practitioner, Practitioner In Attendance is mandatory at dataset completion
    """
    nhs_no = get_subject_with_new_colonoscopy_investigation_dataset()

    UserTools.user_login(page, "Screening Centre Manager at BCS001")

    logging.info(
        "STEP: By default, Practitioner in Attendance is 'Yes' and Name of Practitioner is visible"
    )

    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)

    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    InvestigationDatasetsPage(page).bowel_cancer_screening_page_title_contains_text(
        "Investigation Datasets"
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Practitioner in Attendance", "Yes"
    )
    field_names = ["Name of Practitioner"]
    InvestigationDatasetsPage(page).are_fields_on_page(
        "Investigation Dataset", None, field_names
    )

    InvestigationDatasetsPage(page).select_site_lookup_option_index(-1)
    InvestigationDatasetsPage(page).select_practitioner_option_index(-1)
    InvestigationDatasetsPage(page).assert_dialog_text(
        "You Must Remove the Practitioner below before you can change this value"
    )
    DatasetFieldUtil(page).populate_select_locator_for_field(
        "Practitioner in Attendance", YesNoOptions.NO
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Practitioner in Attendance", "Yes"
    )

    logging.info(
        "STEP: Practitioner in Attendance can be set to 'No' if no practitioner has been selected"
    )
    InvestigationDatasetsPage(page).select_practitioner_option_index(0)
    DatasetFieldUtil(page).populate_select_locator_for_field(
        "Practitioner in Attendance", YesNoOptions.NO
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Practitioner in Attendance", "No"
    )
    assert (
        InvestigationDatasetsPage(page).are_fields_on_page(
            "Investigation Dataset", None, field_names, visible=False
        )
    ) is True, "Name of Practitioner is visible when it should not be"

    logging.info(
        "STEP: Name of Practitioner is not displayed if Practitioner in Attendance is null"
    )
    DatasetFieldUtil(page).populate_select_locator_for_field(
        "Practitioner in Attendance", ""
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Practitioner in Attendance", ""
    )
    assert (
        InvestigationDatasetsPage(page).are_fields_on_page(
            "Investigation Dataset", None, field_names, visible=False
        )
    ) is True, "Name of Practitioner is visible when it should not be"
    LogoutPage(page).log_out()


@pytest.mark.regression
@pytest.mark.vpn_required
@pytest.mark.investigation_dataset_tests
@pytest.mark.bcss_additional_tests
@pytest.mark.colonoscopy_dataset_tests
def test_check_behaviour_of_aspirant_endoscopist_fields(page: Page) -> None:
    """
    Scenario: Check the behaviour of the Aspirant Endoscopist fields
    This tests:
    > Aspirant Endoscopist Not Present field is enabled until an Aspirant Endoscopist is selected
    > If Aspirant Endoscopist Not Present is ticked, it is automatically unticked and disabled when an Aspirant Endoscopist is selected
    > Aspirant Endoscopist Participation is only displayed if an Aspirant Endoscopist is selected
    > Aspirant Endoscopist Participation is only displayed if an Aspirant Endoscopist defaults to Operator
    """
    nhs_no = get_subject_with_new_colonoscopy_investigation_dataset()

    UserTools.user_login(page, "Screening Centre Manager at BCS001")

    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)

    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    InvestigationDatasetsPage(page).bowel_cancer_screening_page_title_contains_text(
        "Investigation Datasets"
    )

    DatasetFieldUtil(page).assert_checkbox_to_right_is_enabled(
        "Aspirant Endoscopist lookup", True
    )
    assert (
        InvestigationDatasetsPage(page).are_fields_on_page(
            "Investigation Dataset",
            None,
            ["Aspirant Endoscopist Participation"],
            visible=False,
        )
    ) is True, "Aspirant Endoscopist Participation is visible when it should not be"

    InvestigationDatasetsPage(page).check_aspirant_endoscopist_not_present()

    DatasetFieldUtil(page).assert_checkbox_to_right_is_ticked_or_not(
        "Aspirant Endoscopist lookup", "Ticked"
    )
    assert (
        InvestigationDatasetsPage(page).are_fields_on_page(
            "Investigation Dataset",
            None,
            ["Aspirant Endoscopist Participation"],
            visible=False,
        )
    ) is True, "Aspirant Endoscopist Participation is visible when it should not be"

    InvestigationDatasetsPage(page).select_aspirant_endoscopist_option_index(-1)
    DatasetFieldUtil(page).assert_checkbox_to_right_is_enabled(
        "Aspirant Endoscopist lookup", False
    )
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        "Aspirant Endoscopist Participation", ["Operator", "Spectator"]
    )
    LogoutPage(page).log_out()


@pytest.mark.regression
@pytest.mark.vpn_required
@pytest.mark.investigation_dataset_tests
@pytest.mark.bcss_additional_tests
@pytest.mark.colonoscopy_dataset_tests
def test_check_dropdown_lists_and_default_values_for_drug_information(
    page: Page,
) -> None:
    """
    Scenario: Check dropdown lists and default field values in the Drug Information section of a new Colonoscopy investigation dataset
    """
    nhs_no = get_subject_with_new_colonoscopy_investigation_dataset()

    UserTools.user_login(page, "Screening Centre Manager at BCS001")

    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)

    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    InvestigationDatasetsPage(page).bowel_cancer_screening_page_title_contains_text(
        "Investigation Datasets"
    )

    InvestigationDatasetsPage(page).click_show_drug_information()
    field_names = [
        general_anaesthetic_string,
        "Entonox",
        bowel_preparation_administered_string,
        antibiotics_administered_string,
        other_drugs_administered_string,
    ]
    InvestigationDatasetsPage(page).are_fields_on_page(
        "Investigation Dataset", None, field_names
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        general_anaesthetic_string, "No"
    )
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        general_anaesthetic_string, ["Yes", "No"]
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text("Entonox", "No")
    DatasetFieldUtil(page).assert_select_to_right_has_values("Entonox", ["Yes", "No"])

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        bowel_preparation_administered_string, "Yes"
    )
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        bowel_preparation_administered_string, ["Yes", "No"]
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_type(
        bowel_preparation_administered_string, 1, True
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_dose(
        bowel_preparation_administered_string, 1, True
    )

    InvestigationDatasetsPage(page).assert_drug_type_text(
        bowel_preparation_administered_string, 1, ""
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        bowel_preparation_administered_string, 1, ""
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        antibiotics_administered_string, "No"
    )
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        antibiotics_administered_string, ["Yes", "No"]
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_type(
        antibiotics_administered_string, 1, True
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_dose(
        antibiotics_administered_string, 1, True
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        other_drugs_administered_string, "No"
    )
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        other_drugs_administered_string, ["Yes", "No"]
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_type(
        other_drugs_administered_string, 1, True
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_dose(
        other_drugs_administered_string, 1, True
    )
    LogoutPage(page).log_out()


@pytest.mark.regression
@pytest.mark.vpn_required
@pytest.mark.investigation_dataset_tests
@pytest.mark.bcss_additional_tests
@pytest.mark.colonoscopy_dataset_tests
def test_check_behaviour_of_drug_information_fields_in_incomplete_dataset(
    page: Page,
) -> None:
    """
    Scenario: Check the behaviour of the Bowel Preparation Administered fields in the Drug Information section in an incomplete endoscopy investigation dataset
    This scenario tests:
    > The contents of dropdown lists.
    > The default values of fields.
    > The visibility of drug type/dose fields.
    > The correct dose units are displayed.
    Immediate validation:
    > A "drug administered" field cannot be set to "No" or null if associated drugs and doses are listed.
    > Dose values must be within the valid range for the drug type, and have the valid number of decimal places (although invalid values are not removed).
    "On save" validation:
    > Bowel Preparation Administered cannot be set to "No" if the Endoscopist Defined Extent is beyond Rectum. (The reverse of this is not tested as this scenario does not save changes).
    > The same drug type cannot be selected more than once
    > A drug type cannot be entered without a dose (*).
    > A dose cannot be entered without a drug type (*).
    """
    nhs_no = get_subject_younger_than_70_with_new_colonsocopy_dataset()
    logging.info(f"NHS Number: {nhs_no}")

    UserTools.user_login(page, "Screening Centre Manager at BCS001")

    logging.info(
        "STEP: Bowel Preparation Administered Type and Dose fields are not displayed if Bowel Preparation Administered = No"
    )
    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)

    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    InvestigationDatasetsPage(page).bowel_cancer_screening_page_title_contains_text(
        "Investigation Datasets"
    )

    InvestigationDatasetsPage(page).click_show_drug_information()

    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        bowel_preparation_administered_string,
        div_drug_details_string,
        YesNoDrugOptions.NO,
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        bowel_preparation_administered_string, "No"
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_type(
        bowel_preparation_administered_string, 1, False
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_dose(
        bowel_preparation_administered_string, 1, False
    )

    logging.info(
        "STEP: On save validation: bowel preparation must be administered if the Endoscopist Defined Extent is anything other than Rectum or Anus"
    )
    InvestigationDatasetsPage(page).click_show_endoscopy_information()
    DatasetFieldUtil(page).populate_select_locator_for_field(
        "Endoscopist defined extent", EndoscopyLocationOptions.SIGMOID_COLON
    )
    InvestigationDatasetsPage(page).assert_dialog_text(
        "Bowel preparation must be administered unless the endoscopist defined extent is the rectum or anus."
    )
    InvestigationDatasetsPage(page).click_save_dataset_button()

    logging.info(
        "STEP: Bowel Preparation Administered Type and Dose fields are displayed if Bowel Preparation Administered = Yes.  Check default values and dropdown options."
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        bowel_preparation_administered_string,
        div_drug_details_string,
        YesNoDrugOptions.YES,
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_type(
        bowel_preparation_administered_string, 1, True
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_dose(
        bowel_preparation_administered_string, 1, True
    )

    InvestigationDatasetsPage(page).assert_drug_type_text(
        bowel_preparation_administered_string, 1, ""
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        bowel_preparation_administered_string, 1, ""
    )

    list_of_options = [
        "Klean Prep",
        "Picolax",
        "Senna Liquid",
        "Senna",
        "Moviprep",
        "Bisacodyl",
        "Citramag",
        "Mannitol",
        "Gastrografin",
        "Phosphate enema",
        "Microlax enema",
        "Osmosprep",
        "Fleet Phospho-soda",
        "Citrafleet",
        "Plenvu",
        "Other",
    ]
    InvestigationDatasetsPage(page).assert_drug_type_options(
        bowel_preparation_administered_string, 1, list_of_options
    )

    logging.info(
        "STEP: Cannot change Bowel Preparation Administered to No or null if a Type and Dose have been recorded"
    )

    InvestigationDatasetsPage(page).select_drug_type_option1(DrugTypeOptions.KLEAN_PREP)
    InvestigationDatasetsPage(page).fill_drug_type_dose1("1")
    InvestigationDatasetsPage(page).assert_dialog_text(
        "You cannot set Bowel Preparation Administered to this value as one or more Bowel Preparation Type is present"
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        bowel_preparation_administered_string,
        div_drug_details_string,
        YesNoDrugOptions.NO,
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        bowel_preparation_administered_string, "Yes"
    )

    InvestigationDatasetsPage(page).assert_dialog_text(
        "You cannot set Bowel Preparation Administered to this value as one or more Bowel Preparation Type is present"
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        bowel_preparation_administered_string, div_drug_details_string, ""
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        bowel_preparation_administered_string, "Yes"
    )

    logging.info(
        "STEP: Can change Bowel Preparation Administered to No if neither Types nor Doses have been recorded"
    )
    InvestigationDatasetsPage(page).select_drug_type_option1("")
    InvestigationDatasetsPage(page).fill_drug_type_dose1("")
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        bowel_preparation_administered_string,
        div_drug_details_string,
        YesNoDrugOptions.NO,
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        bowel_preparation_administered_string, "No"
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_type(
        bowel_preparation_administered_string, 1, False
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_dose(
        bowel_preparation_administered_string, 1, False
    )

    logging.info(
        "STEP: Put Bowel Preparation Administered back to Yes to allow Type/Dose validation"
    )

    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        bowel_preparation_administered_string,
        div_drug_details_string,
        YesNoDrugOptions.YES,
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        bowel_preparation_administered_string, "Yes"
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_type(
        bowel_preparation_administered_string, 1, True
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_dose(
        bowel_preparation_administered_string, 1, True
    )

    InvestigationDatasetsPage(page).assert_drug_type_text(
        bowel_preparation_administered_string, 1, ""
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        bowel_preparation_administered_string, 1, ""
    )

    logging.info(
        "STEP: Dose must be within the allowed range of values, and have the right number of decimal places"
    )
    InvestigationDatasetsPage(page).assert_dialog_text("You cannot enter a value of 0")
    InvestigationDatasetsPage(page).fill_drug_type_dose1("0")

    InvestigationDatasetsPage(page).assert_dialog_text(
        "The minimum Bowel preparation quantity allowed is 1"
    )
    InvestigationDatasetsPage(page).fill_drug_type_dose1("0.9")
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        bowel_preparation_administered_string, 1, "0.9"
    )

    InvestigationDatasetsPage(page).fill_drug_type_dose1("1")
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        bowel_preparation_administered_string, 1, "1"
    )

    InvestigationDatasetsPage(page).assert_dialog_text(
        "Number cannot have more than 1 decimal place"
    )
    InvestigationDatasetsPage(page).fill_drug_type_dose1("1.01")
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        bowel_preparation_administered_string, 1, "1.01"
    )

    InvestigationDatasetsPage(page).assert_dialog_text(
        "Number cannot be greater than 999"
    )
    InvestigationDatasetsPage(page).fill_drug_type_dose1("1000")
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        bowel_preparation_administered_string, 1, "1000"
    )

    InvestigationDatasetsPage(page).fill_drug_type_dose1("999.9")
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        bowel_preparation_administered_string, 1, "999.9"
    )

    logging.info("STEP: Cannot save a dataset with a drug Type but no Dose")
    InvestigationDatasetsPage(page).fill_drug_type_dose1("")
    InvestigationDatasetsPage(page).select_drug_type_option1(DrugTypeOptions.KLEAN_PREP)
    InvestigationDatasetsPage(page).assert_dialog_text(
        "Please enter a dose for this drug"
    )
    InvestigationDatasetsPage(page).click_save_dataset_button()
    InvestigationDatasetsPage(page).assert_drug_type_text(
        bowel_preparation_administered_string, 1, DrugTypeOptions.KLEAN_PREP
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        bowel_preparation_administered_string, 1, ""
    )

    logging.info("STEP: Cannot save a dataset with a drug Dose but no Type")
    InvestigationDatasetsPage(page).select_drug_type_option1("")
    InvestigationDatasetsPage(page).fill_drug_type_dose1("1")
    InvestigationDatasetsPage(page).assert_dialog_text(
        "To delete the drug you must also remove the drug dose"
    )
    InvestigationDatasetsPage(page).click_save_dataset_button()
    InvestigationDatasetsPage(page).assert_drug_type_text(
        bowel_preparation_administered_string, 1, ""
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        bowel_preparation_administered_string, 1, "1"
    )

    logging.info("STEP: The same drug cannot be entered more than once")

    drug_info_list = [
        (DrugTypeOptions.KLEAN_PREP, "1"),
        (DrugTypeOptions.KLEAN_PREP, "2"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, bowel_preparation_administered_string
    )

    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)
    InvestigationDatasetsPage(page).assert_dialog_text(
        "You may not select the same Bowel Preparation more than once."
    )
    InvestigationDatasetsPage(page).click_save_dataset_button()
    InvestigationDatasetsPage(page).assert_drug_type_text(
        bowel_preparation_administered_string, 1, DrugTypeOptions.KLEAN_PREP
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        bowel_preparation_administered_string, 1, "1"
    )
    InvestigationDatasetsPage(page).assert_drug_type_text(
        bowel_preparation_administered_string, 2, DrugTypeOptions.KLEAN_PREP
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        bowel_preparation_administered_string, 2, "2"
    )

    logging.info(
        "STEP: Check that all drug Types can be entered, and the correct Dose units and, for drug type 'Other' an inline warning message, are displayed"
    )
    InvestigationDatasetCompletion(page).clear_drug_type_and_doses_inputs(
        bowel_preparation_administered_string, 2
    )
    drug_info_list = [
        (DrugTypeOptions.KLEAN_PREP, "1"),
        (DrugTypeOptions.PICOLAX, "2.2"),
        (DrugTypeOptions.SENNA_LIQUID, "3"),
        (DrugTypeOptions.SENNA, "4.4"),
        (DrugTypeOptions.MOVIPREP, "5"),
        (DrugTypeOptions.BISACODYL, "6"),
        (DrugTypeOptions.CITRAMAG, "7"),
        (DrugTypeOptions.MANNITOL, "8"),
        (DrugTypeOptions.GASTROGRAFIN, "9"),
        (DrugTypeOptions.PHOSPHATE_ENEMA, "10"),
        (DrugTypeOptions.MICROLAX_ENEMA, "11"),
        (DrugTypeOptions.OSMOSPREP, "12"),
        (DrugTypeOptions.FLEET_PHOSPHO_SODA, "13"),
        (DrugTypeOptions.CITRAFLEET, "14"),
        (DrugTypeOptions.PLENVU, "15"),
        (DrugTypeOptions.OTHER, "999.9"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, bowel_preparation_administered_string
    )

    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)
    InvestigationDatasetsPage(page).assert_all_drug_information(
        drug_information, bowel_preparation_administered_string
    )
    InvestigationDatasetsPage(page).expect_text_to_be_visible(
        "Please record your bowel preparation regime in episode notes."
    )
    LogoutPage(page).log_out()


@pytest.mark.regression
@pytest.mark.vpn_required
@pytest.mark.investigation_dataset_tests
@pytest.mark.bcss_additional_tests
@pytest.mark.colonoscopy_dataset_tests
def test_check_behaviour_of_antibiotics_administered_fields_in_incomplete_dataset(
    page: Page,
) -> None:
    """
    Scenario: Check the behaviour of the Antibiotics Administered fields in the Drug Information section in an incomplete endoscopy investigation dataset
    This checks:
    > The contents of dropdown lists
    > The default values of fields
    > The visibility of drug type/dose fields
    > The dose units
    > A "drug administered" field cannot be set to "No" or null if associated drugs and doses are listed
    > The same drug type cannot be selected more than once
    > Validation of dose values
    """
    nhs_no = get_subject_younger_than_70_with_new_colonsocopy_dataset()

    logging.info(
        "STEP: Antibiotics Administered Type and Dose fields are not displayed if Antibiotics Administered = No"
    )

    UserTools.user_login(page, "Screening Centre Manager at BCS001")

    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)

    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    InvestigationDatasetsPage(page).bowel_cancer_screening_page_title_contains_text(
        "Investigation Datasets"
    )

    InvestigationDatasetsPage(page).click_show_drug_information()
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        antibiotics_administered_string, div_drug_details_string, YesNoOptions.YES
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        antibiotics_administered_string, "Yes"
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_type(
        antibiotics_administered_string, 1, True
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_dose(
        antibiotics_administered_string, 1, True
    )

    InvestigationDatasetsPage(page).assert_drug_type_text(
        antibiotics_administered_string, 1, ""
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        antibiotics_administered_string, 1, ""
    )

    list_of_options = [
        "Amoxycillin",
        "Cefotaxime",
        "Ciproflaxacin",
        "Co-amoxiclav",
        "Gentamicin",
        "Metronidazole",
        "Teicoplanin",
        "Vancomycin",
        "Other antibiotic",
    ]
    InvestigationDatasetsPage(page).assert_drug_type_options(
        antibiotics_administered_string, 1, list_of_options
    )

    logging.info(
        "STEP: Cannot change Antibiotics Administered to No or null if a Type and Dose have been recorded"
    )

    drug_info_list = [
        (AntibioticsAdministeredDrugTypeOptions.AMOXYCILLIN, "1"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, antibiotics_administered_string
    )

    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_type_text(
        antibiotics_administered_string,
        1,
        AntibioticsAdministeredDrugTypeOptions.AMOXYCILLIN,
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        antibiotics_administered_string, 1, "1"
    )

    InvestigationDatasetsPage(page).assert_dialog_text(
        "You cannot set Antibiotics Administered to this value as Antibiotics exist"
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        antibiotics_administered_string, div_drug_details_string, YesNoOptions.NO
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        antibiotics_administered_string, "Yes"
    )

    InvestigationDatasetsPage(page).assert_dialog_text(
        "You cannot set Antibiotics Administered to this value as Antibiotics exist"
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        antibiotics_administered_string, div_drug_details_string, ""
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        antibiotics_administered_string, "Yes"
    )

    logging.info(
        "STEP: Can change Antibiotics Administered to No if neither Types nor Doses have been recorded"
    )

    InvestigationDatasetCompletion(page).clear_drug_type_and_doses_inputs(
        antibiotics_administered_string
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        antibiotics_administered_string, div_drug_details_string, YesNoOptions.NO
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        antibiotics_administered_string, "No"
    )

    logging.info(
        "STEP: Dose must be within the allowed range of values, and have the right number of decimal places"
    )

    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        antibiotics_administered_string, div_drug_details_string, YesNoOptions.YES
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        antibiotics_administered_string, "Yes"
    )

    InvestigationDatasetsPage(page).assert_dialog_text("You cannot enter a value of 0")

    drug_info_list = [
        (None, "0"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, antibiotics_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        antibiotics_administered_string, 1, "0"
    )

    drug_info_list = [
        (None, "0.01"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, antibiotics_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        antibiotics_administered_string, 1, "0.01"
    )

    InvestigationDatasetsPage(page).assert_dialog_text(
        "Number cannot have more than 2 decimal places"
    )
    drug_info_list = [
        (None, "1.123"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, antibiotics_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        antibiotics_administered_string, 1, "1.123"
    )

    InvestigationDatasetsPage(page).assert_dialog_text(
        "Number cannot be greater than 9999999"
    )
    drug_info_list = [
        (None, "10000000"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, antibiotics_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        antibiotics_administered_string, 1, "10000000"
    )

    drug_info_list = [
        (None, "9999999.99"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, antibiotics_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        antibiotics_administered_string, 1, "9999999.99"
    )

    logging.info("STEP: Cannot save a dataset with a drug Type but no Dose")

    InvestigationDatasetCompletion(page).clear_drug_type_and_doses_inputs(
        antibiotics_administered_string
    )

    drug_info_list = [
        (AntibioticsAdministeredDrugTypeOptions.AMOXYCILLIN, None),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, antibiotics_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_dialog_text(
        "Please enter a dose for this drug"
    )
    InvestigationDatasetsPage(page).click_save_dataset_button()
    InvestigationDatasetsPage(page).assert_drug_type_text(
        antibiotics_administered_string,
        1,
        AntibioticsAdministeredDrugTypeOptions.AMOXYCILLIN,
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        antibiotics_administered_string, 1, ""
    )

    logging.info("STEP: Cannot save a dataset with a drug Dose but no Type")

    InvestigationDatasetCompletion(page).clear_drug_type_and_doses_inputs(
        antibiotics_administered_string
    )

    drug_info_list = [
        (None, "1"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, antibiotics_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)
    InvestigationDatasetsPage(page).assert_dialog_text(
        "To delete the drug you must also remove the drug dose"
    )
    InvestigationDatasetsPage(page).click_save_dataset_button()
    InvestigationDatasetsPage(page).assert_drug_type_text(
        antibiotics_administered_string, 1, ""
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        antibiotics_administered_string, 1, "1"
    )

    logging.info("STEP: The same drug cannot be entered more than once")

    InvestigationDatasetCompletion(page).clear_drug_type_and_doses_inputs(
        antibiotics_administered_string
    )

    drug_info_list = [
        (AntibioticsAdministeredDrugTypeOptions.AMOXYCILLIN, "1"),
        (AntibioticsAdministeredDrugTypeOptions.AMOXYCILLIN, "2"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, antibiotics_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)
    InvestigationDatasetsPage(page).assert_dialog_text(
        "You may not select the same Antibiotic more than once."
    )
    InvestigationDatasetsPage(page).click_save_dataset_button()
    InvestigationDatasetsPage(page).assert_drug_type_text(
        antibiotics_administered_string,
        1,
        AntibioticsAdministeredDrugTypeOptions.AMOXYCILLIN,
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        antibiotics_administered_string, 1, "1"
    )
    InvestigationDatasetsPage(page).assert_drug_type_text(
        antibiotics_administered_string,
        2,
        AntibioticsAdministeredDrugTypeOptions.AMOXYCILLIN,
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        antibiotics_administered_string, 2, "2"
    )

    logging.info(
        "STEP: Check that all drug Types can be entered, and the correct Dose units and, for drug type 'Other' an inline warning message, are displayed"
    )

    InvestigationDatasetCompletion(page).clear_drug_type_and_doses_inputs(
        antibiotics_administered_string, 2
    )

    drug_info_list = [
        (AntibioticsAdministeredDrugTypeOptions.AMOXYCILLIN, "0.01"),
        (AntibioticsAdministeredDrugTypeOptions.CEFOTAXIME, "2.2"),
        (AntibioticsAdministeredDrugTypeOptions.CIPROFLAXACIN, "3.33"),
        (AntibioticsAdministeredDrugTypeOptions.CO_AMOXICLAV, "4"),
        (AntibioticsAdministeredDrugTypeOptions.GENTAMICIN, "5"),
        (AntibioticsAdministeredDrugTypeOptions.METRONIDAZOLE, "6.06"),
        (AntibioticsAdministeredDrugTypeOptions.TEICOPLANIN, "7"),
        (AntibioticsAdministeredDrugTypeOptions.VANCOMYCIN, "8.88"),
        (AntibioticsAdministeredDrugTypeOptions.OTHER_ANTIBIOTIC, "9999999.99"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, antibiotics_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_all_drug_information(
        drug_information, antibiotics_administered_string
    )
    InvestigationDatasetsPage(page).assert_drug_dosage_unit_text(
        antibiotics_administered_string,
        9,
        "Please record antibiotic details and dosage in episode notes.",
    )
    LogoutPage(page).log_out()


@pytest.mark.regression
@pytest.mark.vpn_required
@pytest.mark.investigation_dataset_tests
@pytest.mark.bcss_additional_tests
@pytest.mark.colonoscopy_dataset_tests
def test_check_behaviour_of_other_drugs_administered_fields_in_incomplete_dataset(
    page: Page,
) -> None:
    """
    Scenario: Check the behaviour of the Other Drugs Administered fields in the Drug Information section in an incomplete endoscopy investigation dataset
    This checks:
    The contents of dropdown lists
    The default values of fields
    The visibility of drug type/dose fields
    The dose units
    A "drug administered" field cannot be set to "No" or null if associated drugs and doses are listed
    The same drug type cannot be selected more than once
    Validation of dose values - when entering a new drug line, and when updating an existing dose
    """
    nhs_no = get_subject_younger_than_70_with_new_colonsocopy_dataset()

    logging.info(
        "STEP: Other Drugs Administered Type and Dose fields are not displayed if Other Drugs Administered = No"
    )

    UserTools.user_login(page, "Screening Centre Manager at BCS001")

    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)

    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    InvestigationDatasetsPage(page).bowel_cancer_screening_page_title_contains_text(
        "Investigation Datasets"
    )

    InvestigationDatasetsPage(page).click_show_drug_information()
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        other_drugs_administered_string, div_drug_details_string, YesNoOptions.NO
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        other_drugs_administered_string, "No"
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_type(
        other_drugs_administered_string, 1, False
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_dose(
        other_drugs_administered_string, 1, False
    )

    logging.info(
        "STEP: Other Drugs Administered Type and Dose fields are displayed if Other Drugs Administered = Yes.  Check default values and dropdown options."
    )

    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        other_drugs_administered_string, div_drug_details_string, YesNoOptions.YES
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        other_drugs_administered_string, "Yes"
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_type(
        other_drugs_administered_string, 1, True
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_dose(
        other_drugs_administered_string, 1, True
    )

    InvestigationDatasetsPage(page).assert_drug_type_text(
        other_drugs_administered_string, 1, ""
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, ""
    )

    list_of_options = [
        "Alfentanyl",
        "Buscopan",
        "Diazemuls",
        "Fentanyl",
        "Flumazenil",
        "Glucagon",
        "Hydrocortisone",
        "Meptazinol",
        "Midazolam",
        "Naloxone",
        "Pethidine",
        "Propofol",
    ]
    InvestigationDatasetsPage(page).assert_drug_type_options(
        other_drugs_administered_string, 1, list_of_options
    )

    logging.info(
        "STEP: Cannot change Other Drugs Administered to No or null if a Type and Dose have been recorded"
    )

    drug_info_list = [
        (OtherDrugsAdministeredDrugTypeOptions.ALFENTANYL, "1"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_dialog_text(
        "You cannot set Drugs Administered to this value as Drugs exist"
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        other_drugs_administered_string, div_drug_details_string, YesNoOptions.NO
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        other_drugs_administered_string, "Yes"
    )

    logging.info(
        "STEP: Can change Other Drugs Administered to No if neither Types nor Doses have been recorded"
    )

    InvestigationDatasetCompletion(page).clear_drug_type_and_doses_inputs(
        other_drugs_administered_string
    )

    InvestigationDatasetsPage(page).assert_drug_type_text(
        other_drugs_administered_string, 1, ""
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, ""
    )

    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        other_drugs_administered_string, div_drug_details_string, YesNoOptions.NO
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        other_drugs_administered_string, "No"
    )

    logging.info(
        "STEP: Dose must be within the allowed range of values, and have the right number of decimal places"
    )

    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        other_drugs_administered_string, div_drug_details_string, YesNoOptions.YES
    )

    drug_info_list = [
        (OtherDrugsAdministeredDrugTypeOptions.ALFENTANYL, "0"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )

    InvestigationDatasetsPage(page).assert_dialog_text("You cannot enter a value of 0")
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_type_text(
        other_drugs_administered_string,
        1,
        OtherDrugsAdministeredDrugTypeOptions.ALFENTANYL,
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "0"
    )

    drug_info_list = [
        (None, "0.01"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "0.01"
    )

    drug_info_list = [
        (None, "1.123"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetsPage(page).assert_dialog_text(
        "Number cannot have more than 2 decimal places"
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "1.123"
    )

    drug_info_list = [
        (None, "10000000"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetsPage(page).assert_dialog_text(
        "Number cannot be greater than 9999999"
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "10000000"
    )

    drug_info_list = [
        (None, "9999999.99"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "9999999.99"
    )

    drug_info_list = [
        (None, "15"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    logging.info("STEP: Fentanyl has a specific Dose range")

    drug_info_list = [
        (OtherDrugsAdministeredDrugTypeOptions.FENTANYL, None),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    drug_info_list = [
        (None, "11.99"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetsPage(page).assert_dialog_text(
        "The recommended dose for Fentanyl is 12 - 100 mcg. Please check and re-enter as necessary.",
        True,
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_type_text(
        other_drugs_administered_string,
        1,
        OtherDrugsAdministeredDrugTypeOptions.FENTANYL,
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "11.99"
    )

    drug_info_list = [
        (None, "12"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "12"
    )

    drug_info_list = [
        (None, "100.01"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetsPage(page).assert_dialog_text(
        "The recommended dose for Fentanyl is 12 - 100 mcg. Please check and re-enter as necessary.",
        True,
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_type_text(
        other_drugs_administered_string,
        1,
        OtherDrugsAdministeredDrugTypeOptions.FENTANYL,
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "100.01"
    )

    drug_info_list = [
        (None, "100"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "100"
    )

    logging.info("STEP: Pethidine has a specific Dose range")

    InvestigationDatasetCompletion(page).clear_drug_type_and_doses_inputs(
        other_drugs_administered_string
    )

    drug_info_list = [
        (OtherDrugsAdministeredDrugTypeOptions.PETHIDINE, "24.99"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetsPage(page).assert_dialog_text(
        "The recommended dose for Pethidine is 25 - 100 mg. Please check and re-enter as necessary.",
        True,
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_type_text(
        other_drugs_administered_string,
        1,
        OtherDrugsAdministeredDrugTypeOptions.PETHIDINE,
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "24.99"
    )

    drug_info_list = [
        (None, "25"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "25"
    )

    drug_info_list = [
        (None, "100.01"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetsPage(page).assert_dialog_text(
        "The recommended dose for Pethidine is 25 - 100 mg. Please check and re-enter as necessary.",
        True,
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "100.01"
    )

    drug_info_list = [
        (None, "100"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "100"
    )

    logging.info("STEP: Buscopan has a specific Dose range")

    InvestigationDatasetCompletion(page).clear_drug_type_and_doses_inputs(
        other_drugs_administered_string
    )

    drug_info_list = [
        (OtherDrugsAdministeredDrugTypeOptions.BUSCOPAN, "9.99"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetsPage(page).assert_dialog_text(
        "The recommended dose for Buscopan is 10 - 40 mg. Please check and re-enter as necessary.",
        True,
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_type_text(
        other_drugs_administered_string,
        1,
        OtherDrugsAdministeredDrugTypeOptions.BUSCOPAN,
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "9.99"
    )

    drug_info_list = [
        (None, "10"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "10"
    )

    drug_info_list = [
        (None, "40.01"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetsPage(page).assert_dialog_text(
        "The recommended dose for Buscopan is 10 - 40 mg. Please check and re-enter as necessary.",
        True,
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "40.01"
    )

    drug_info_list = [
        (None, "40"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "40"
    )

    logging.info("STEP: Midazolam has a specific Dose range for patients aged under 70")

    InvestigationDatasetCompletion(page).clear_drug_type_and_doses_inputs(
        other_drugs_administered_string
    )

    drug_info_list = [
        (OtherDrugsAdministeredDrugTypeOptions.MIDAZOLAM, "0.99"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetsPage(page).assert_dialog_text(
        "The recommended dose for Midazolam is 1 - 5 mg for patients under 70 years old. Please check and re-enter as necessary.",
        True,
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_type_text(
        other_drugs_administered_string,
        1,
        OtherDrugsAdministeredDrugTypeOptions.MIDAZOLAM,
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "0.99"
    )

    drug_info_list = [
        (None, "1"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "1"
    )

    drug_info_list = [
        (None, "5.01"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetsPage(page).assert_dialog_text(
        "The recommended dose for Midazolam is 1 - 5 mg for patients under 70 years old. Please check and re-enter as necessary.",
        True,
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "5.01"
    )

    drug_info_list = [
        (None, "5"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "5"
    )

    logging.info("STEP: Cannot save a dataset with a drug Type but no Dose")

    InvestigationDatasetCompletion(page).clear_drug_type_and_doses_inputs(
        other_drugs_administered_string
    )

    drug_info_list = [
        (OtherDrugsAdministeredDrugTypeOptions.ALFENTANYL, None),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_dialog_text(
        "Please enter a dose for this drug"
    )
    InvestigationDatasetsPage(page).click_save_dataset_button()
    InvestigationDatasetsPage(page).assert_drug_type_text(
        other_drugs_administered_string,
        1,
        OtherDrugsAdministeredDrugTypeOptions.ALFENTANYL,
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, ""
    )

    logging.info("STEP: Cannot save a dataset with a drug Dose but no Type ")

    InvestigationDatasetCompletion(page).clear_drug_type_and_doses_inputs(
        other_drugs_administered_string
    )

    drug_info_list = [
        (None, "1"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)
    InvestigationDatasetsPage(page).assert_dialog_text(
        "To delete the drug you must also remove the drug dose"
    )
    InvestigationDatasetsPage(page).click_save_dataset_button()
    InvestigationDatasetsPage(page).assert_drug_type_text(
        other_drugs_administered_string, 1, ""
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "1"
    )

    logging.info("STEP: If Naxolone is selected, an alert is displayed")

    InvestigationDatasetCompletion(page).clear_drug_type_and_doses_inputs(
        other_drugs_administered_string
    )

    drug_info_list = [
        (OtherDrugsAdministeredDrugTypeOptions.NALOXONE, None),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetsPage(page).assert_dialog_text(
        "NALOXONE is a reversal agent, are you sure this is correct?  If so please raise an AVI.",
        True,
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_type_text(
        other_drugs_administered_string,
        1,
        OtherDrugsAdministeredDrugTypeOptions.NALOXONE,
    )

    logging.info("STEP: The same drug cannot be entered more than once")

    InvestigationDatasetCompletion(page).clear_drug_type_and_doses_inputs(
        other_drugs_administered_string
    )

    drug_info_list = [
        (OtherDrugsAdministeredDrugTypeOptions.ALFENTANYL, "1"),
        (OtherDrugsAdministeredDrugTypeOptions.ALFENTANYL, "2"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)
    InvestigationDatasetsPage(page).assert_dialog_text(
        "You may not select the same Drug more than once."
    )
    InvestigationDatasetsPage(page).click_save_dataset_button()

    InvestigationDatasetsPage(page).assert_drug_type_text(
        other_drugs_administered_string,
        1,
        OtherDrugsAdministeredDrugTypeOptions.ALFENTANYL,
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "1"
    )
    InvestigationDatasetsPage(page).assert_drug_type_text(
        other_drugs_administered_string,
        2,
        OtherDrugsAdministeredDrugTypeOptions.ALFENTANYL,
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 2, "2"
    )

    logging.info(
        "STEP: Check that all drug Types can be entered, and the correct Dose units are displayed"
    )

    InvestigationDatasetCompletion(page).clear_drug_type_and_doses_inputs(
        other_drugs_administered_string, 2
    )

    drug_info_list = [
        (OtherDrugsAdministeredDrugTypeOptions.ALFENTANYL, "1.01"),
        (OtherDrugsAdministeredDrugTypeOptions.BUSCOPAN, "10.2"),
        (OtherDrugsAdministeredDrugTypeOptions.DIAZEMULS, "3"),
        (OtherDrugsAdministeredDrugTypeOptions.FENTANYL, "12"),
        (OtherDrugsAdministeredDrugTypeOptions.FLUMAZENIL, "5.55"),
        (OtherDrugsAdministeredDrugTypeOptions.GLUCAGON, "6"),
        (OtherDrugsAdministeredDrugTypeOptions.HYDROCORTISONE, "7"),
        (OtherDrugsAdministeredDrugTypeOptions.MEPTAZINOL, "8"),
        (OtherDrugsAdministeredDrugTypeOptions.MIDAZOLAM, "5"),
        (OtherDrugsAdministeredDrugTypeOptions.PETHIDINE, "25"),
        (OtherDrugsAdministeredDrugTypeOptions.PROPOFOL, "9999999.99"),
        (OtherDrugsAdministeredDrugTypeOptions.NALOXONE, "10"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetsPage(page).assert_dialog_text(
        "NALOXONE is a reversal agent, are you sure this is correct?  If so please raise an AVI.",
        True,
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)
    InvestigationDatasetsPage(page).assert_all_drug_information(
        drug_information, other_drugs_administered_string
    )

    LogoutPage(page).log_out()


@pytest.mark.regression
@pytest.mark.vpn_required
@pytest.mark.investigation_dataset_tests
@pytest.mark.bcss_additional_tests
@pytest.mark.colonoscopy_dataset_tests
def test_check_drug_validation_for_subject_older_than_70_in_incomplete_dataset(
    page: Page,
) -> None:
    """
    Scenario: Check drug dose validation specific to a subject aged 70 or older in an incomplete endoscopy investigation dataset
    This checks the drug dose validation for Midazolam, which has a different recommended range for subjects aged 70 or older.
    """
    nhs_no = get_subject_older_than_70_with_new_colonsocopy_dataset()

    UserTools.user_login(page, "Screening Centre Manager at BCS001")

    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)

    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    InvestigationDatasetsPage(page).bowel_cancer_screening_page_title_contains_text(
        "Investigation Datasets"
    )
    InvestigationDatasetsPage(page).click_show_drug_information()
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        other_drugs_administered_string, div_drug_details_string, YesNoOptions.YES
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        other_drugs_administered_string, "Yes"
    )

    InvestigationDatasetsPage(page).check_visibility_of_drug_type(
        other_drugs_administered_string, 1, True
    )
    InvestigationDatasetsPage(page).check_visibility_of_drug_dose(
        other_drugs_administered_string, 1, True
    )
    InvestigationDatasetsPage(page).assert_drug_type_text(
        other_drugs_administered_string, 1, ""
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, ""
    )

    drug_info_list = [
        (OtherDrugsAdministeredDrugTypeOptions.MIDAZOLAM, "0.99"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetsPage(page).assert_dialog_text(
        "The recommended dose for Midazolam is 1 - 2.5 mg for patients aged 70 or over. Please check and re-enter as necessary.",
        True,
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_type_text(
        other_drugs_administered_string,
        1,
        OtherDrugsAdministeredDrugTypeOptions.MIDAZOLAM,
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "0.99"
    )

    drug_info_list = [
        (None, "1"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "1"
    )

    drug_info_list = [
        (None, "2.51"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetsPage(page).assert_dialog_text(
        "The recommended dose for Midazolam is 1 - 2.5 mg for patients aged 70 or over. Please check and re-enter as necessary.",
        True,
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)

    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "2.51"
    )

    drug_info_list = [
        (None, "2.5"),
    ]
    drug_information = InvestigationDatasetCompletion(page).build_drug_information_dict(
        drug_info_list, other_drugs_administered_string
    )
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        other_drugs_administered_string, 1, "2.5"
    )

    LogoutPage(page).log_out()


@pytest.mark.regression
@pytest.mark.vpn_required
@pytest.mark.investigation_dataset_tests
@pytest.mark.bcss_additional_tests
@pytest.mark.colonoscopy_dataset_tests
def test_check_dropdown_lists_and_default_field_values_in_endoscopy_information_section(
    page: Page,
) -> None:
    """
    Scenario: Check dropdown lists and default field values in the Endoscopy Information section of a new Colonoscopy investigation dataset
    """
    nhs_no = get_subject_with_new_colonoscopy_investigation_dataset()
    UserTools.user_login(page, "Screening Centre Manager at BCS001")
    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)
    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    InvestigationDatasetsPage(page).bowel_cancer_screening_page_title_contains_text(
        "Investigation Datasets"
    )
    InvestigationDatasetsPage(page).click_show_endoscopy_information()
    field_names = [
        "Endoscope inserted",
        "Procedure type",
        "Bowel preparation quality",
        "Comfort during examination",
        "Comfort during recovery",
        sedation_during_examination_string,
        sedation_during_recovery_string,
        "Endoscopist defined extent",
        "Scope imager used",
        "Retroverted view",
        "Start of intubation time",
        "Start of extubation time",
        "End time of procedure",
        "Scope ID",
        "Detection assistant (AI) used?",
        "Insufflation",
        "Outcome at time of procedure",
        "Late outcome",
    ]
    InvestigationDatasetsPage(page).are_fields_on_page(
        "Endoscopy Information", None, field_names
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Endoscope inserted", YesNoOptions.YES
    )
    InvestigationDatasetsPage(page).are_fields_on_page(
        "Endoscopy Information", None, ["Why Endoscope Not Inserted"], False
    )
    DatasetFieldUtil(page).assert_radio_to_right_is_selected(
        "Procedure type", "Diagnostic", "divColonoscopeFields"
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Bowel preparation quality", ""
    )
    dropdown_values = [
        "Excellent",
        "Good",
        "Adequate/Fair",
        "Poor",
        "Inadequate",
    ]
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        "Bowel preparation quality", dropdown_values
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Comfort during examination", ""
    )
    dropdown_values = [
        "No discomfort",
        "Minimal discomfort",
        "Mild discomfort",
        "Moderate discomfort",
        "Severe discomfort",
    ]
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        "Comfort during examination", dropdown_values
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Comfort during recovery", ""
    )
    dropdown_values = [
        "No discomfort",
        "Minimal discomfort",
        "Mild discomfort",
        "Moderate discomfort",
        "Severe discomfort",
    ]
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        "Comfort during recovery", dropdown_values
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        sedation_during_examination_string, "Unsedated", "divSedationExamReadOnly"
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        sedation_during_recovery_string, "Unsedated", "divSedationRecoveryReadOnly"
    )
    InvestigationDatasetsPage(page).are_fields_on_page(
        "Endoscopy Information", None, ["Intended extent of examination"], False
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Endoscopist defined extent", ""
    )
    dropdown_values = [
        "Anus",
        "Rectum",
        "Sigmoid Colon",
        "Descending Colon",
        "Splenic Flexure",
        "Transverse Colon",
        "Hepatic Flexure",
        "Ascending Colon",
        "Caecum",
        "Ileum",
        "Anastomosis",
        "Appendix",
    ]
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        "Endoscopist defined extent", dropdown_values
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Scope imager used", ""
    )
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        "Scope imager used", ["Yes", "No"]
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Retroverted view", ""
    )
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        "Retroverted view", ["Yes", "No"]
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Start of intubation time", ""
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Start of extubation time", ""
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "End time of procedure", ""
    )
    InvestigationDatasetsPage(page).are_fields_on_page(
        "Endoscopy Information", None, ["Withdrawal time"], False
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text("Scope ID", "")
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Detection Assistant (AI) used?", "No"
    )
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        "Detection Assistant (AI) used?", ["Yes", "No"]
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text("Insufflation", "")
    dropdown_values = [
        "Air",
        "Carbon Dioxide",
        "Carbon Dioxide changed to Air mid procedure",
        "Air changed to Carbon Dioxide mid procedure",
        "Water",
        "Water and Carbon Dioxide",
        "Water and Air",
        "Water and Carbon Dioxide and Air",
    ]
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        "Insufflation", dropdown_values
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Outcome at time of procedure", ""
    )
    dropdown_values = [
        "Leave department",
        "Planned hospital admission for observation/social reasons",
        "Unplanned hospital admission",
    ]
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        "Outcome at time of procedure", dropdown_values
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text("Late outcome", "")
    dropdown_values = [
        "No complications",
        "Condition resolved",
        "Telephone consultation",
        "Outpatient consultation",
        "Hospital admission",
    ]
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        "Late outcome", dropdown_values
    )

    LogoutPage(page).log_out()


@pytest.mark.regression
@pytest.mark.vpn_required
@pytest.mark.investigation_dataset_tests
@pytest.mark.bcss_additional_tests
@pytest.mark.colonoscopy_dataset_tests
def test_validation_of_scope_id_field_in_endoscopy_information_section(
    page: Page,
) -> None:
    """
    Scenario: Check the validation of the Scope ID field in the Endoscopy Information section in an incomplete Colonoscopy investigation dataset
    Scope ID can't contain invalid characters.  This validation is both immediate and on save.
    """
    nhs_no = get_subject_with_new_colonoscopy_investigation_dataset()
    UserTools.user_login(page, "Screening Centre Manager at BCS001")
    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)
    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    InvestigationDatasetsPage(page).bowel_cancer_screening_page_title_contains_text(
        "Investigation Datasets"
    )
    InvestigationDatasetsPage(page).click_show_endoscopy_information()

    InvestigationDatasetsPage(page).assert_dialog_text(
        'Certain characters may not be used in the Scope ID field.  Please remove the following: <>,",&,¬,£'
    )
    DatasetFieldUtil(page).populate_input_locator_for_field("Scope ID", '<> " & ¬ £')
    InvestigationDatasetsPage(page).assert_dialog_text(
        'Certain characters may not be used in the Scope ID field.  Please remove the following: <>,",&,¬,£'
    )
    InvestigationDatasetsPage(page).click_save_dataset_button()

    LogoutPage(page).log_out()


@pytest.mark.regression
@pytest.mark.vpn_required
@pytest.mark.investigation_dataset_tests
@pytest.mark.bcss_additional_tests
@pytest.mark.colonoscopy_dataset_tests
def test_behaviour_of_edoscope_inserted_fields_in_endoscopy_information_section(
    page: Page,
) -> None:
    """
    Scenario: Check the behaviour of the Endoscope Inserted fields in the Endoscopy Information section in an incomplete Colonoscopy investigation dataset
    """
    nhs_no = get_subject_with_new_colonoscopy_investigation_dataset()
    UserTools.user_login(page, "Screening Centre Manager at BCS001")
    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)
    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    InvestigationDatasetsPage(page).bowel_cancer_screening_page_title_contains_text(
        "Investigation Datasets"
    )

    logging.info("STEP: By default Endoscope Inserted = Yes")
    InvestigationDatasetsPage(page).click_show_endoscopy_information()

    DatasetFieldUtil(page).assert_radio_to_right_is_selected(
        "Endoscope Inserted", "Yes"
    )
    sections_to_check = [
        "Failure Information",
        "Polyp Information",
        "Colorectal Cancer Information",
        "Complication Information",
        "Other Findings",
    ]
    InvestigationDatasetsPage(page).is_dataset_section_on_page(sections_to_check)

    logging.info(
        "STEP: Changing Endoscope Inserted to No removes most fields and sections"
    )

    InvestigationDatasetsPage(page).check_endoscope_inserted_no()
    DatasetFieldUtil(page).assert_radio_to_right_is_selected("Endoscope Inserted", "No")
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Why Endoscope Not Inserted", ""
    )
    dropdown_values = [
        "Clinical reason on PR",
        "Consent refused",
        "Equipment failure",
        "No bowel preparation",
        "Patient unsuitable",
        "Service interruption",
        "Solid stool on PR",
        "Unscheduled attendance time",
    ]
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        "Why Endoscope Not Inserted", dropdown_values
    )
    field_names = [
        "Procedure type",
        "Bowel preparation quality",
        "Comfort during examination",
        "Comfort during recovery",
        "Intended extent of examination",
        "Endoscopist defined extent",
        "Scope imager used",
        "Retroverted view",
        "Start of intubation time",
        "Start of extubation time",
        "End time of procedure",
        "Withdrawal time",
        "Scope ID",
        "Detection Assistant (AI) Used?",
        "Insufflation",
        "Outcome at time of procedure",
        "Late outcome",
    ]
    InvestigationDatasetsPage(page).are_fields_on_page(
        "Endoscopy Information", None, field_names, False
    )
    sections_to_check = [
        "Failure Information",
        "Complication Information",
    ]
    InvestigationDatasetsPage(page).is_dataset_section_on_page(sections_to_check, False)

    logging.info(
        "STEP: For most Why Endoscope Not Inserted values, polyps, cancers or other findings cannot be recorded"
    )

    DatasetFieldUtil(page).populate_select_locator_for_field(
        "Why Endoscope Not Inserted", EndoscopeNotInsertedOptions.EQUIPMENT_FAILURE
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Why Endoscope Not Inserted", "Equipment failure"
    )
    sections_to_check = [
        "Polyp Information",
        "Colorectal Cancer Information",
        "Other Findings",
    ]
    InvestigationDatasetsPage(page).is_dataset_section_on_page(sections_to_check, False)

    logging.info(
        "STEP: Why Endoscope Not Inserted values 'Clinical reason on PR' does allow polyps, cancers or other findings to be recorded"
    )

    DatasetFieldUtil(page).populate_select_locator_for_field(
        "Why Endoscope Not Inserted", EndoscopeNotInsertedOptions.CLINICAL_REASON_ON_PR
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Why Endoscope Not Inserted", "Clinical reason on PR"
    )
    InvestigationDatasetsPage(page).is_dataset_section_on_page(sections_to_check)

    logging.info(
        "STEP: Endoscope Inserted can only be changed back to Yes if there is no Why Endoscope Not Inserted value"
    )

    InvestigationDatasetsPage(page).assert_dialog_text(
        "You cannot change 'Endoscope inserted' to 'Yes' as details have been entered for Why Endoscope Not Inserted."
    )
    InvestigationDatasetsPage(page).check_endoscope_inserted_yes()

    DatasetFieldUtil(page).populate_select_locator_for_field(
        "Why Endoscope Not Inserted", ""
    )
    InvestigationDatasetsPage(page).check_endoscope_inserted_yes()
    DatasetFieldUtil(page).assert_radio_to_right_is_selected(
        "Endoscope Inserted", "Yes"
    )

    LogoutPage(page).log_out()


@pytest.mark.regression
@pytest.mark.vpn_required
@pytest.mark.investigation_dataset_tests
@pytest.mark.bcss_additional_tests
@pytest.mark.colonoscopy_dataset_tests
def test_cross_field_validation_between_bowel_prep_administered_and_quality_fields_in_investigation_dataset(
    page: Page,
) -> None:
    """
    Scenario: Check cross-field validation between the Bowel Preparation Administered and Bowel Preparation Quality fields in an incomplete Colonoscopy investigation dataset
    """
    nhs_no = get_subject_with_new_colonoscopy_investigation_dataset()
    UserTools.user_login(page, "Screening Centre Manager at BCS001")
    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)
    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    InvestigationDatasetsPage(page).bowel_cancer_screening_page_title_contains_text(
        "Investigation Datasets"
    )

    logging.info(
        "STEP: The Bowel Preparation Quality field is not displayed if Bowel Preparation Administered = No"
    )

    InvestigationDatasetsPage(page).click_show_drug_information()
    InvestigationDatasetsPage(page).click_show_endoscopy_information()
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        bowel_preparation_administered_string,
        div_drug_details_string,
        YesNoDrugOptions.NO,
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        bowel_preparation_administered_string, "No"
    )
    InvestigationDatasetsPage(page).are_fields_on_page(
        "Endoscopy Information", None, ["Bowel preparation quality"], False
    )

    logging.info(
        "STEP: Bowel Preparation Administered cannot be changed to No if a Bowel Preparation Quality value has been selected"
    )

    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        bowel_preparation_administered_string,
        div_drug_details_string,
        YesNoDrugOptions.YES,
    )
    DatasetFieldUtil(page).populate_select_locator_for_field(
        "Bowel preparation quality", BowelPreparationQualityOptions.EXCELLENT
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        bowel_preparation_administered_string, "Yes"
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Bowel preparation quality", "Excellent"
    )

    InvestigationDatasetsPage(page).assert_dialog_text(
        "You cannot set Bowel Preparation Administered to this value as a Bowel Preparation Quality value exists"
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        bowel_preparation_administered_string,
        div_drug_details_string,
        YesNoDrugOptions.NO,
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        bowel_preparation_administered_string, "Yes"
    )

    logging.info(
        "STEP: Bowel Preparation Administered cannot be removed if a Bowel Preparation Quality value has been selected"
    )

    InvestigationDatasetsPage(page).assert_dialog_text(
        "You cannot set Bowel Preparation Administered to this value as a Bowel Preparation Quality value exists"
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        bowel_preparation_administered_string,
        div_drug_details_string,
        "",
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        bowel_preparation_administered_string, "Yes"
    )

    logging.info(
        "STEP: Bowel Preparation Administered can be removed if a Bowel Preparation Quality value has been selected"
    )

    DatasetFieldUtil(page).populate_select_locator_for_field(
        "Bowel preparation quality", ""
    )
    DatasetFieldUtil(page).populate_select_locator_for_field(
        bowel_preparation_administered_string, YesNoDrugOptions.NO
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        bowel_preparation_administered_string, "No"
    )

    LogoutPage(page).log_out()


@pytest.mark.regression
@pytest.mark.vpn_required
@pytest.mark.investigation_dataset_tests
@pytest.mark.bcss_additional_tests
@pytest.mark.colonoscopy_dataset_tests
def test_cross_field_validation_between_general_anaesthetic_other_drugs_and_sedation_fields_in_investigation_dataset(
    page: Page,
) -> None:
    """
    Scenario: Check cross-field validation between the General Anaesthetic/Other Drugs Administered and the Sedation fields in an incomplete Colonoscopy investigation dataset
    If both of the General Anaesthetic and Other Drugs Administered fields are set to 'No', then the two Sedation fields are read only and set to 'Unsedated'.
    If both the General Anaesthetic and Other Drugs Administered fields are set to 'Yes', and one or both of the Sedation fields holds a value other than 'Unsedated' then one of General Anaesthetic or Other Drugs Administered can be set to 'No' without a warning.  It is only when the only remaining 'Yes', in these two fields, is set to 'No' that the warning is displayed.
    Unlike some of the other cross-validated fields, General Anaesthetic and Other Drugs Administered can be set to null even if the Sedation fields hold a value other than 'Unsedated'.
    """
    nhs_no = get_subject_with_new_colonoscopy_investigation_dataset()
    UserTools.user_login(page, "Screening Centre Manager at BCS001")
    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)
    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    InvestigationDatasetsPage(page).bowel_cancer_screening_page_title_contains_text(
        "Investigation Datasets"
    )

    logging.info(
        "STEP: If just General Anaesthetic was administered, the two Sedation felds are enabled"
    )

    InvestigationDatasetsPage(page).click_show_drug_information()
    InvestigationDatasetsPage(page).click_show_endoscopy_information()

    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        general_anaesthetic_string,
        div_drug_details_string,
        YesNoOptions.YES,
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        other_drugs_administered_string,
        div_drug_details_string,
        YesNoOptions.NO,
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        general_anaesthetic_string, "Yes"
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        other_drugs_administered_string, "No"
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        sedation_during_examination_string, ""
    )

    dropdown_values = [
        "Unsedated",
        "Awake",
        "Drowsy",
        "Asleep but responding to name",
        "Asleep but responding to touch",
        "Asleep and unresponsive",
    ]
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        sedation_during_examination_string, dropdown_values
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        sedation_during_examination_string, ""
    )
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        sedation_during_recovery_string, dropdown_values
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        sedation_during_recovery_string, ""
    )

    logging.info(
        "STEP: If Sedation During Examination indicates the subject WAS sedated, General Anaesthetic and Other Drugs Administered can be changed, as long as at least one of them is Yes"
    )

    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        other_drugs_administered_string,
        div_drug_details_string,
        YesNoOptions.YES,
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        sedation_during_examination_string,
        div_sedation_exam_string,
        SedationOptions.ASLEEP_AND_UNRESPONSIVE,
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        general_anaesthetic_string,
        div_drug_details_string,
        YesNoOptions.NO,
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        general_anaesthetic_string, "No"
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        other_drugs_administered_string, "Yes"
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        sedation_during_examination_string, "Asleep and unresponsive"
    )

    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        general_anaesthetic_string,
        div_drug_details_string,
        YesNoOptions.YES,
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        other_drugs_administered_string,
        div_drug_details_string,
        YesNoOptions.NO,
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        general_anaesthetic_string, "Yes"
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        other_drugs_administered_string, "No"
    )

    logging.info(
        "STEP: If Sedation values indicate the subject WAS sedated, General Anaesthetic can't be set to No if Other Drugs Administered is already set to No"
    )

    InvestigationDatasetsPage(page).assert_dialog_text(
        "You cannot set General Anaesthetic to 'No' as Sedation during examination indicates that the patient was sedated"
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        general_anaesthetic_string,
        div_drug_details_string,
        YesNoOptions.NO,
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        general_anaesthetic_string, "Yes"
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        other_drugs_administered_string, "No"
    )

    logging.info(
        "STEP: If Sedation values indicate the subject WAS sedated, General Anaesthetic can be null"
    )

    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        general_anaesthetic_string,
        div_drug_details_string,
        "",
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        general_anaesthetic_string, ""
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        other_drugs_administered_string, "No"
    )

    logging.info(
        "STEP: If Sedation During Recovery indicates the subject WAS sedated, General Anaesthetic and Other Drugs Administered can be changed, as long as at least one of them is Yes"
    )

    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        sedation_during_examination_string,
        div_sedation_exam_string,
        SedationOptions.UNSEDATED,
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        sedation_during_recovery_string,
        div_sedation_recovery_string,
        SedationOptions.AWAKE,
    )

    InvestigationDatasetsPage(page).assert_dialog_text(
        "You cannot set General Anaesthetic to 'No' as Sedation during recovery indicates that the patient was sedated"
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        general_anaesthetic_string,
        div_drug_details_string,
        YesNoOptions.NO,
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        general_anaesthetic_string, ""
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        other_drugs_administered_string, "No"
    )

    logging.info(
        "STEP: If both Sedation values indicate the subject was Unsedated, and Other Drugs Administered is already No, General Anaesthetic can also be set to No - and the two Sedation fields then become read only"
    )

    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        sedation_during_examination_string,
        div_sedation_exam_string,
        SedationOptions.UNSEDATED,
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        sedation_during_recovery_string,
        div_sedation_recovery_string,
        SedationOptions.UNSEDATED,
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        general_anaesthetic_string,
        div_drug_details_string,
        YesNoOptions.NO,
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        general_anaesthetic_string, "No"
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        other_drugs_administered_string, "No"
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        sedation_during_examination_string, "Unsedated", "divSedationExamReadOnly"
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        sedation_during_recovery_string, "Unsedated", "divSedationRecoveryReadOnly"
    )

    logging.info(
        "STEP: If one or both of General Anaesthetic or Other Drugs Administered are set to Yes, the two Sedation fields become editable, retaining a previously manually set value of 'Unsedated'"
    )

    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        general_anaesthetic_string,
        div_drug_details_string,
        YesNoOptions.NO,
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        other_drugs_administered_string,
        div_drug_details_string,
        YesNoOptions.YES,
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        general_anaesthetic_string, "No"
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        other_drugs_administered_string, "Yes"
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        sedation_during_examination_string, "Unsedated"
    )
    dropdown_values = [
        "Unsedated",
        "Awake",
        "Drowsy",
        "Asleep but responding to name",
        "Asleep but responding to touch",
        "Asleep and unresponsive",
    ]
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        sedation_during_examination_string, dropdown_values
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        sedation_during_recovery_string, "Unsedated"
    )
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        sedation_during_recovery_string, dropdown_values
    )

    logging.info(
        "STEP: If just Other Drugs were administered, the two Sedation felds are enabled"
    )

    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        sedation_during_examination_string,
        div_sedation_exam_string,
        SedationOptions.ASLEEP_BUT_RESPONDING_TO_TOUCH,
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        general_anaesthetic_string, "No"
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        other_drugs_administered_string, "Yes"
    )

    logging.info(
        "STEP: If Sedation During Examination indicates the subject WAS sedated, Other Drugs Administered can't be set to No if General Anaesthetic is already set to No"
    )

    InvestigationDatasetsPage(page).assert_dialog_text(
        "You cannot set Drugs Administered to 'No' as Sedation during examination indicates that the patient was sedated"
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        other_drugs_administered_string,
        div_drug_details_string,
        YesNoOptions.NO,
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        other_drugs_administered_string, "Yes"
    )

    logging.info(
        "STEP: If Sedation values indicate the subject WAS sedated, Other Drugs Administered can be null"
    )

    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        other_drugs_administered_string,
        div_drug_details_string,
        "",
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        other_drugs_administered_string, ""
    )

    logging.info(
        "STEP: If Sedation During Recovery indicates the subject WAS sedated, Other Drugs Administered can't be set to No if General Anaesthetic is already set to No"
    )

    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        sedation_during_examination_string,
        div_sedation_exam_string,
        SedationOptions.UNSEDATED,
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        sedation_during_recovery_string,
        div_sedation_recovery_string,
        SedationOptions.AWAKE,
    )

    InvestigationDatasetsPage(page).assert_dialog_text(
        "You cannot set Drugs Administered to 'No' as Sedation during recovery indicates that the patient was sedated"
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        other_drugs_administered_string,
        div_drug_details_string,
        YesNoOptions.NO,
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        other_drugs_administered_string, ""
    )

    logging.info(
        "STEP: If both Sedation values indicate the subject was Unsedated, and General Anaesthetic is already No, Other Drugs Administered can also be set to No - and the two Sedation fields then become read only"
    )

    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        sedation_during_examination_string,
        div_sedation_exam_string,
        SedationOptions.UNSEDATED,
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        sedation_during_recovery_string,
        div_sedation_recovery_string,
        SedationOptions.UNSEDATED,
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        other_drugs_administered_string,
        div_drug_details_string,
        YesNoOptions.NO,
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        other_drugs_administered_string, "No"
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        sedation_during_examination_string, "Unsedated", "divSedationExamReadOnly"
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        sedation_during_recovery_string, "Unsedated", "divSedationRecoveryReadOnly"
    )

    LogoutPage(page).log_out()


# Helper Functions


def check_role_access_to_edit_investigation_dataset(
    page: Page,
    nhs_no: str,
    role: str,
    edit_access: bool,
    role_logging: str,
    role_type: Optional[str] = None,
) -> None:
    """
    Verifies whether a user with a specific role has access to edit the Investigation Dataset.
    This function logs in as a given user role, navigates to the subject's investigation dataset,
    and asserts the visibility of the "Edit Dataset" button based on expected access.
    Args:
        page (Page): The Playwright page object for interacting with the UI.
        nhs_no (str): NHS number used to search for the subject.
        role (str): The user role to log in as.
        edit_access (bool): True if the role is expected to have edit access; False otherwise.
        role_logging (str): Descriptive log message for tracking which role is being tested.
        role_type (Optional[str]): Optional job role selection (e.g., if multiple job roles exist).
    Raises:
        AssertionError: If the visibility of the "Edit Dataset" button does not match the expected access.
    """
    logging.info(role_logging)
    UserTools.user_login(page, role)

    if (
        role == "Specialist Screening Practitioner at BCS009 & BCS001"
        or role == "Assistant Screening Practitioner at BCS001"
    ):
        OrganisationSwitchPage(page).select_organisation_by_id("BCS001")
        OrganisationSwitchPage(page).click_continue()

    if role_type:
        SelectJobRolePage(page).select_option_for_job_role(role_type)
        SelectJobRolePage(page).click_continue_button()

    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)
    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()
    InvestigationDatasetsPage(page).bowel_cancer_screening_page_title_contains_text(
        "Investigation Datasets"
    )

    if edit_access:
        assert InvestigationDatasetsPage(
            page
        ).is_edit_dataset_button_visible(), (
            "Expected 'Edit Dataset' button to be visible, but it was hidden."
        )
        logging.info("'Edit Dataset' button is correctly visible.")
    else:
        assert not InvestigationDatasetsPage(
            page
        ).is_edit_dataset_button_visible(), (
            "Expected 'Edit Dataset' button to be hidden, but it was visible."
        )
        logging.info("'Edit Dataset' button is correctly hidden.")


def get_subject_with_incomplete_endoscopy_investigation_dataset() -> str:
    """
    Gets a subject with the following criteria:
        "latest episode status": "open"
        "latest episode latest investigation dataset": "endoscopy_incomplete"
    Returns:
        str: The nhs number of a subject matching the criteria
    """
    criteria = {
        "latest episode status": "open",
        "latest episode latest investigation dataset": "endoscopy_incomplete",
    }
    user = User()
    subject = Subject()

    builder = SubjectSelectionQueryBuilder()

    query, bind_vars = builder.build_subject_selection_query(
        criteria=criteria,
        user=user,
        subject=subject,
        subjects_to_retrieve=1,
    )

    df = OracleDB().execute_query(query, bind_vars)
    nhs_no = df.iloc[0]["subject_nhs_number"]
    logging.info(f"NHS Number: {nhs_no}")
    return nhs_no


def get_subject_with_new_colonoscopy_investigation_dataset() -> str:
    """
    Gets a subject with the following criteria:
        "latest episode status": "open",
        "latest episode latest investigation dataset": "colonoscopy_new",
    Returns:
        str: The nhs number of a subject matching the criteria
    """
    criteria = {
        "latest episode status": "open",
        "latest episode latest investigation dataset": "colonoscopy_new",
    }
    user = User()
    subject = Subject()

    builder = SubjectSelectionQueryBuilder()

    query, bind_vars = builder.build_subject_selection_query(
        criteria=criteria,
        user=user,
        subject=subject,
        subjects_to_retrieve=1,
    )

    df = OracleDB().execute_query(query, bind_vars)
    nhs_no = df.iloc[0]["subject_nhs_number"]
    logging.info(f"NHS Number: {nhs_no}")
    return nhs_no


def get_subject_younger_than_70_with_new_colonsocopy_dataset() -> str:
    """
    Gets a subject with the following criteria:
        "latest episode status": "open",
        "latest episode latest investigation dataset": "colonoscopy_new",
        "subject age": "< 70"
    Returns:
        str: The nhs number of a subject matching the criteria
    """
    criteria = {
        "latest episode status": "open",
        "latest episode latest investigation dataset": "colonoscopy_new",
        "subject age": "< 70",
    }
    user = User()
    subject = Subject()

    builder = SubjectSelectionQueryBuilder()

    query, bind_vars = builder.build_subject_selection_query(
        criteria=criteria,
        user=user,
        subject=subject,
        subjects_to_retrieve=1,
    )

    df = OracleDB().execute_query(query, bind_vars)
    nhs_no = df.iloc[0]["subject_nhs_number"]
    logging.info(f"NHS Number: {nhs_no}")
    return nhs_no


def get_subject_older_than_70_with_new_colonsocopy_dataset() -> str:
    """
    Gets a subject with the following criteria:
        "latest episode status": "open",
        "latest episode latest investigation dataset": "colonoscopy_new",
        "subject age": ">= 70"
    Returns:
        str: The nhs number of a subject matching the criteria
    """
    criteria = {
        "latest episode status": "open",
        "latest episode latest investigation dataset": "colonoscopy_new",
        "subject age": ">= 70",
    }
    user = User()
    subject = Subject()

    builder = SubjectSelectionQueryBuilder()

    query, bind_vars = builder.build_subject_selection_query(
        criteria=criteria,
        user=user,
        subject=subject,
        subjects_to_retrieve=1,
    )

    df = OracleDB().execute_query(query, bind_vars)
    nhs_no = df.iloc[0]["subject_nhs_number"]
    logging.info(f"NHS Number: {nhs_no}")
    return nhs_no
