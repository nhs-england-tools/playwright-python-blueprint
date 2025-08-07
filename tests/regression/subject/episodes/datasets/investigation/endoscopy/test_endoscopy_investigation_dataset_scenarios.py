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

    drug_information = {
        "drug_type1": DrugTypeOptions.BISACODYL,
        "drug_dose1": "10",
        "drug_type2": DrugTypeOptions.CITRAFLEET,
        "drug_dose2": "20",
    }

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
        "General Anaesthetic",
        "Entonox",
        "Bowel Preparation Administered",
        "Antibiotics Administered",
        "Other Drugs Administered",
    ]
    InvestigationDatasetsPage(page).are_fields_on_page(
        "Investigation Dataset", None, field_names
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "General Anaesthetic", "No"
    )
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        "General Anaesthetic", ["Yes", "No"]
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text("Entonox", "No")
    DatasetFieldUtil(page).assert_select_to_right_has_values("Entonox", ["Yes", "No"])

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Bowel Preparation Administered", "Yes"
    )
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        "Bowel Preparation Administered", ["Yes", "No"]
    )

    assert (
        InvestigationDatasetsPage(page).check_visibility_of_drug_type(
            "Bowel Preparation Administered", 1, True
        )
    ) is True, (
        "The first Bowel Preparation Administered drug type input cell is not visible"
    )
    logging.info(
        "The first Bowel Preparation Administered drug type input cell is visible"
    )

    assert (
        InvestigationDatasetsPage(page).check_visibility_of_drug_dose(
            "Bowel Preparation Administered", 1, True
        )
    ) is True, (
        "The first Bowel Preparation Administered drug dose input cell is not visible"
    )
    logging.info(
        "The first Bowel Preparation Administered drug dose input cell is visible"
    )

    InvestigationDatasetsPage(page).assert_drug_type_text(
        "Bowel Preparation Administered", 1, ""
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        "Bowel Preparation Administered", 1, ""
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Antibiotics Administered", "No"
    )
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        "Antibiotics Administered", ["Yes", "No"]
    )

    assert (
        InvestigationDatasetsPage(page).check_visibility_of_drug_type(
            "Antibiotics Administered", 1, True
        )
    ) is False, "The first Antibiotics Administered drug type input cell is visible"
    logging.info(
        "The first Antibiotics Administered drug type input cell is not visible"
    )

    assert (
        InvestigationDatasetsPage(page).check_visibility_of_drug_dose(
            "Antibiotics Administered", 1, True
        )
    ) is False, "The first Antibiotics Administered drug dose input cell is visible"
    logging.info(
        "The first Antibiotics Administered drug dose input cell is not visible"
    )

    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Other Drugs Administered", "No"
    )
    DatasetFieldUtil(page).assert_select_to_right_has_values(
        "Other Drugs Administered", ["Yes", "No"]
    )

    assert (
        InvestigationDatasetsPage(page).check_visibility_of_drug_type(
            "Other Drugs Administered", 1, True
        )
    ) is False, "The first Other Drugs Administered drug type input cell is visible"
    logging.info(
        "The first Other Drugs Administered drug type input cell is not visible"
    )

    assert (
        InvestigationDatasetsPage(page).check_visibility_of_drug_dose(
            "Other Drugs Administered", 1, True
        )
    ) is False, "The first Other Drugs Administered drug dose input cell is visible"
    logging.info(
        "The first Other Drugs Administered drug dose input cell is not visible"
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
        "Bowel Preparation Administered", "divDrugDetails", YesNoDrugOptions.NO
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Bowel Preparation Administered", "No"
    )

    assert (
        InvestigationDatasetsPage(page).check_visibility_of_drug_type(
            "Bowel Preparation Administered", 1, False
        )
    ) is True, (
        "The first Bowel Preparation Administered drug type input cell is visible"
    )
    logging.info(
        "The first Bowel Preparation Administered drug type input cell is not visible"
    )

    assert (
        InvestigationDatasetsPage(page).check_visibility_of_drug_dose(
            "Bowel Preparation Administered", 1, False
        )
    ) is True, (
        "The first Bowel Preparation Administered drug dose input cell is visible"
    )
    logging.info(
        "The first Bowel Preparation Administered drug dose input cell is not visible"
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
        "Bowel Preparation Administered", "divDrugDetails", YesNoDrugOptions.YES
    )

    assert (
        InvestigationDatasetsPage(page).check_visibility_of_drug_type(
            "Bowel Preparation Administered", 1, True
        )
    ) is True, (
        "The first Bowel Preparation Administered drug type input cell is not visible"
    )
    logging.info(
        "The first Bowel Preparation Administered drug type input cell is visible"
    )

    assert (
        InvestigationDatasetsPage(page).check_visibility_of_drug_dose(
            "Bowel Preparation Administered", 1, True
        )
    ) is True, (
        "The first Bowel Preparation Administered drug dose input cell is not visible"
    )
    logging.info(
        "The first Bowel Preparation Administered drug dose input cell is visible"
    )
    InvestigationDatasetsPage(page).assert_drug_type_text(
        "Bowel Preparation Administered", 1, ""
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        "Bowel Preparation Administered", 1, ""
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
        "Bowel Preparation Administered", 1, list_of_options
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
        "Bowel Preparation Administered", "divDrugDetails", YesNoDrugOptions.NO
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Bowel Preparation Administered", "Yes"
    )

    InvestigationDatasetsPage(page).assert_dialog_text(
        "You cannot set Bowel Preparation Administered to this value as one or more Bowel Preparation Type is present"
    )
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        "Bowel Preparation Administered", "divDrugDetails", ""
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Bowel Preparation Administered", "Yes"
    )

    logging.info(
        "STEP: Can change Bowel Preparation Administered to No if neither Types nor Doses have been recorded"
    )
    InvestigationDatasetsPage(page).select_drug_type_option1("")
    InvestigationDatasetsPage(page).fill_drug_type_dose1("")
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        "Bowel Preparation Administered", "divDrugDetails", YesNoDrugOptions.NO
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Bowel Preparation Administered", "No"
    )

    assert (
        InvestigationDatasetsPage(page).check_visibility_of_drug_type(
            "Bowel Preparation Administered", 1, False
        )
    ) is True, (
        "The first Bowel Preparation Administered drug type input cell is visible"
    )
    logging.info(
        "The first Bowel Preparation Administered drug type input cell is not visible"
    )

    assert (
        InvestigationDatasetsPage(page).check_visibility_of_drug_dose(
            "Bowel Preparation Administered", 1, False
        )
    ) is True, (
        "The first Bowel Preparation Administered drug dose input cell is visible"
    )
    logging.info(
        "The first Bowel Preparation Administered drug dose input cell is not visible"
    )

    logging.info(
        "STEP: Put Bowel Preparation Administered back to Yes to allow Type/Dose validation"
    )

    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        "Bowel Preparation Administered", "divDrugDetails", YesNoDrugOptions.YES
    )
    DatasetFieldUtil(page).assert_cell_to_right_has_expected_text(
        "Bowel Preparation Administered", "Yes"
    )

    assert (
        InvestigationDatasetsPage(page).check_visibility_of_drug_type(
            "Bowel Preparation Administered", 1, True
        )
    ) is True, (
        "The first Bowel Preparation Administered drug type input cell is not visible"
    )
    logging.info(
        "The first Bowel Preparation Administered drug type input cell is visible"
    )

    assert (
        InvestigationDatasetsPage(page).check_visibility_of_drug_dose(
            "Bowel Preparation Administered", 1, True
        )
    ) is True, (
        "The first Bowel Preparation Administered drug dose input cell is not visible"
    )
    logging.info(
        "The first Bowel Preparation Administered drug dose input cell is visible"
    )

    InvestigationDatasetsPage(page).assert_drug_type_text(
        "Bowel Preparation Administered", 1, ""
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        "Bowel Preparation Administered", 1, ""
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
        "Bowel Preparation Administered", 1, "0.9"
    )

    InvestigationDatasetsPage(page).fill_drug_type_dose1("1")
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        "Bowel Preparation Administered", 1, "1"
    )

    InvestigationDatasetsPage(page).assert_dialog_text(
        "Number cannot have more than 1 decimal place"
    )
    InvestigationDatasetsPage(page).fill_drug_type_dose1("1.01")
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        "Bowel Preparation Administered", 1, "1.01"
    )

    InvestigationDatasetsPage(page).assert_dialog_text(
        "Number cannot be greater than 999"
    )
    InvestigationDatasetsPage(page).fill_drug_type_dose1("1000")
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        "Bowel Preparation Administered", 1, "1000"
    )

    InvestigationDatasetsPage(page).fill_drug_type_dose1("999.9")
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        "Bowel Preparation Administered", 1, "999.9"
    )

    logging.info("STEP: Cannot save a dataset with a drug Type but no Dose")
    InvestigationDatasetsPage(page).fill_drug_type_dose1("")
    InvestigationDatasetsPage(page).select_drug_type_option1(DrugTypeOptions.KLEAN_PREP)
    InvestigationDatasetsPage(page).assert_dialog_text(
        "Please enter a dose for this drug"
    )
    InvestigationDatasetsPage(page).click_save_dataset_button()
    InvestigationDatasetsPage(page).assert_drug_type_text(
        "Bowel Preparation Administered", 1, DrugTypeOptions.KLEAN_PREP
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        "Bowel Preparation Administered", 1, ""
    )

    logging.info("STEP: Cannot save a dataset with a drug Dose but no Type")
    InvestigationDatasetsPage(page).select_drug_type_option1("")
    InvestigationDatasetsPage(page).fill_drug_type_dose1("1")
    InvestigationDatasetsPage(page).assert_dialog_text(
        "To delete the drug you must also remove the drug dose"
    )
    InvestigationDatasetsPage(page).click_save_dataset_button()
    InvestigationDatasetsPage(page).assert_drug_type_text(
        "Bowel Preparation Administered", 1, ""
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        "Bowel Preparation Administered", 1, "1"
    )

    logging.info("STEP: The same drug cannot be entered more than once")
    drug_information = {
        "drug_type1": DrugTypeOptions.KLEAN_PREP,
        "drug_dose1": "1",
        "drug_type2": DrugTypeOptions.KLEAN_PREP,
        "drug_dose2": "2",
    }
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)
    InvestigationDatasetsPage(page).assert_dialog_text(
        "You may not select the same Bowel Preparation more than once."
    )
    InvestigationDatasetsPage(page).click_save_dataset_button()
    InvestigationDatasetsPage(page).assert_drug_type_text(
        "Bowel Preparation Administered", 1, DrugTypeOptions.KLEAN_PREP
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        "Bowel Preparation Administered", 1, "1"
    )
    InvestigationDatasetsPage(page).assert_drug_type_text(
        "Bowel Preparation Administered", 2, DrugTypeOptions.KLEAN_PREP
    )
    InvestigationDatasetsPage(page).assert_drug_dose_text(
        "Bowel Preparation Administered", 2, "2"
    )

    logging.info(
        "STEP: Check that all drug Types can be entered, and the correct Dose units and, for drug type 'Other' an inline warning message, are displayed"
    )
    drug_information = {
        "drug_type2": "",
        "drug_dose2": "",
        "drug_type1": "",
        "drug_dose1": "",
    }
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)
    drug_information = {
        "drug_type1": DrugTypeOptions.KLEAN_PREP,
        "drug_dose1": "1",
        "drug_type2": DrugTypeOptions.PICOLAX,
        "drug_dose2": "2.2",
        "drug_type3": DrugTypeOptions.SENNA_LIQUID,
        "drug_dose3": "3",
        "drug_type4": DrugTypeOptions.SENNA,
        "drug_dose4": "4.4",
        "drug_type5": DrugTypeOptions.MOVIPREP,
        "drug_dose5": "5",
        "drug_type6": DrugTypeOptions.BISACODYL,
        "drug_dose6": "6",
        "drug_type7": DrugTypeOptions.CITRAMAG,
        "drug_dose7": "7",
        "drug_type8": DrugTypeOptions.MANNITOL,
        "drug_dose8": "8",
        "drug_type9": DrugTypeOptions.GASTROGRAFIN,
        "drug_dose9": "9",
        "drug_type10": DrugTypeOptions.PHOSPHATE_ENEMA,
        "drug_dose10": "10",
        "drug_type11": DrugTypeOptions.MICROLAX_ENEMA,
        "drug_dose11": "11",
        "drug_type12": DrugTypeOptions.OSMOSPREP,
        "drug_dose12": "12",
        "drug_type13": DrugTypeOptions.FLEET_PHOSPHO_SODA,
        "drug_dose13": "13",
        "drug_type14": DrugTypeOptions.CITRAFLEET,
        "drug_dose14": "14",
        "drug_type15": DrugTypeOptions.PLENVU,
        "drug_dose15": "15",
        "drug_type16": DrugTypeOptions.OTHER,
        "drug_dose16": "999.9",
    }
    InvestigationDatasetCompletion(page).fill_out_drug_information(drug_information)
    InvestigationDatasetsPage(page).assert_all_drug_information(
        drug_information, "Bowel Preparation Administered"
    )
    InvestigationDatasetsPage(page).expect_text_to_be_visible(
        "Please record your bowel preparation regime in episode notes."
    )
    LogoutPage(page).log_out()


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
