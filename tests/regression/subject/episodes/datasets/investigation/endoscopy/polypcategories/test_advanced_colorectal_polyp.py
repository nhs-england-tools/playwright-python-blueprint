import logging
import pytest
import pandas as pd
from pytest import FixtureRequest
from datetime import datetime
from playwright.sync_api import Page
from classes.subject import Subject
from classes.user import User
from pages.base_page import BasePage
from pages.datasets.investigation_dataset_page import (
    InvestigationDatasetsPage,
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
    PolypTypeOptions,
    AdenomaSubTypeOptions,
    SerratedLesionSubTypeOptions,
    PolypExcisionCompleteOptions,
    PolypDysplasiaOptions,
    YesNoUncertainOptions,
)
from pages.datasets.subject_datasets_page import SubjectDatasetsPage
from pages.logout.log_out_page import LogoutPage
from pages.screening_subject_search.attend_diagnostic_test_page import (
    AttendDiagnosticTestPage,
)
from pages.screening_subject_search.contact_with_patient_page import (
    ContactWithPatientPage,
)
from pages.screening_subject_search.diagnostic_test_outcome_page import (
    DiagnosticTestOutcomePage,
    OutcomeOfDiagnosticTest,
)
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from pages.screening_subject_search.advance_fobt_screening_episode_page import (
    AdvanceFOBTScreeningEpisodePage,
)
from utils.batch_processing import batch_processing
from utils.calendar_picker import CalendarPicker
from utils.investigation_dataset import (
    InvestigationDatasetCompletion,
)
from utils.oracle.oracle import OracleDB
from utils.oracle.subject_selection_query_builder import SubjectSelectionQueryBuilder
from utils.screening_subject_page_searcher import (
    search_subject_episode_by_nhs_number,
)
from utils.user_tools import UserTools

# Defining dictionaries used in tests
general_information = {
    "site": -1,
    "practitioner": -1,
    "testing clinician": -1,
    "aspirant endoscopist": None,
}

drug_information = {
    "drug_type1": DrugTypeOptions.MANNITOL,
    "drug_dose1": "3",
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

failure_information = {
    "failure reasons": FailureReasonsOptions.ADHESION,
}

completion_information = {
    "completion proof": CompletionProofOptions.VIDEO_APPENDIX,
}


@pytest.fixture(autouse=True)
def before_test(page: Page, request: FixtureRequest) -> None:
    """
    Before each test this will get the relevant subject and navigate to their investigation dataset
    """
    if request.node.get_closest_marker("skip_before_test"):
        return
    df = obtain_test_data()
    nhs_no = df.iloc[0]["subject_nhs_number"]
    logging.info(f"NHS Number: {nhs_no}")

    UserTools.user_login(page, "Screening Centre Manager at BCS001")
    BasePage(page).click_main_menu_link()
    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)

    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.investigation_dataset_tests
def test_identify_advanced_colorectal_polyp_from_histology_a(page: Page) -> None:
    """
    This test identifies an advanced colorectal polyp from histology results. (BCSS-5567 - A)
    """
    endoscopy_information["endoscopist defined extent"] = (
        EndoscopyLocationOptions.DESCENDING_COLON
    )

    polyp_1_information = make_polyp_1_information(
        **{
            "location": EndoscopyLocationOptions.RECTUM,
            "classification": PolypClassificationOptions.IP,
        }
    )

    polyp_1_intervention = make_polyp_1_intervention(
        **{"device": PolypInterventionDeviceOptions.HOT_SNARE}
    )

    polyp_1_histology = make_polyp_1_histology(
        **{
            "serrated lesion sub type": SerratedLesionSubTypeOptions.TRADITIONAL_SERRATED_ADENOMA,
            "polyp size": "9",
        }
    )
    del polyp_1_histology["adenoma sub type"]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        polyp_1_information=polyp_1_information,
        polyp_1_intervention=polyp_1_intervention,
        polyp_1_histology=polyp_1_histology,
    )

    assert_test_results(page, "9")


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.investigation_dataset_tests
def test_identify_advanced_colorectal_polyp_from_histology_b(page: Page) -> None:
    """
    This test identifies an advanced colorectal polyp from histology results (BCSS-5567 - B).
    """
    polyp_1_information = make_polyp_1_information(
        **{
            "location": EndoscopyLocationOptions.SIGMOID_COLON,
            "classification": PolypClassificationOptions.ISP,
            "estimate of whole polyp size": "9",
            "excision technique": PolypInterventionExcisionTechniqueOptions.EN_BLOC,
        }
    )

    polyp_1_intervention = make_polyp_1_intervention(
        **{"modality": PolypInterventionModalityOptions.EMR},
    )

    polyp_1_histology = make_polyp_1_histology(
        **{
            "polyp size": "8",
            "serrated lesion sub type": SerratedLesionSubTypeOptions.TRADITIONAL_SERRATED_ADENOMA,
        }
    )
    del polyp_1_histology["adenoma sub type"]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
        polyp_1_information=polyp_1_information,
        polyp_1_intervention=polyp_1_intervention,
        polyp_1_histology=polyp_1_histology,
    )

    assert_test_results(page, "8")


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.investigation_dataset_tests
def test_identify_advanced_colorectal_polyp_from_histology_c(page: Page) -> None:
    """
    This test identifies an advanced colorectal polyp from histology results (BCSS-5567 - C).
    """
    polyp_1_information = make_polyp_1_information(
        **{
            "location": EndoscopyLocationOptions.DESCENDING_COLON,
        }
    )

    polyp_1_intervention = make_polyp_1_intervention(
        **{
            "modality": PolypInterventionModalityOptions.ESD,
            "device": PolypInterventionDeviceOptions.ENDOSCOPIC_KNIFE,
            "excision technique": PolypInterventionExcisionTechniqueOptions.EN_BLOC,
        }
    )

    polyp_1_histology = make_polyp_1_histology()
    del polyp_1_histology["adenoma sub type"]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
        polyp_1_information=polyp_1_information,
        polyp_1_intervention=polyp_1_intervention,
        polyp_1_histology=polyp_1_histology,
    )

    assert_test_results(page, "10")


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.investigation_dataset_tests
def test_identify_advanced_colorectal_polyp_from_histology_d(page: Page) -> None:
    """
    This test identifies an advanced colorectal polyp from histology results (BCSS-5567 - D).
    """
    polyp_1_information = make_polyp_1_information(
        **{
            "location": EndoscopyLocationOptions.SPLENIC_FLEXURE,
            "classification": PolypClassificationOptions.IIA,
            "estimate of whole polyp size": "9",
        }
    )

    polyp_1_intervention = make_polyp_1_intervention(
        **{
            "excision technique": PolypInterventionExcisionTechniqueOptions.PIECE_MEAL,
        }
    )

    polyp_1_histology = make_polyp_1_histology(
        **{
            "polyp size": "11",
        }
    )
    del polyp_1_histology["adenoma sub type"]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
        polyp_1_information=polyp_1_information,
        polyp_1_intervention=polyp_1_intervention,
        polyp_1_histology=polyp_1_histology,
    )

    assert_test_results(page, "11")


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.investigation_dataset_tests
def test_identify_advanced_colorectal_polyp_from_histology_e(page: Page) -> None:
    """
    This test identifies an advanced colorectal polyp from histology results (BCSS-5567 - E).
    """
    polyp_1_information = make_polyp_1_information(
        **{
            "location": EndoscopyLocationOptions.TRANSVERSE_COLON,
            "classification": PolypClassificationOptions.IIB,
            "estimate of whole polyp size": "11",
        }
    )

    polyp_1_intervention = make_polyp_1_intervention(
        **{
            "modality": PolypInterventionModalityOptions.EMR,
            "excision technique": PolypInterventionExcisionTechniqueOptions.PIECE_MEAL,
            "polyp appears fully resected endoscopically": YesNoOptions.YES,
        }
    )

    polyp_1_histology = make_polyp_1_histology(
        **{
            "serrated lesion sub type": SerratedLesionSubTypeOptions.HYPERPLASTIC_POLYP,
            "polyp size": "9",
        }
    )
    del polyp_1_histology["polyp dysplasia"]
    del polyp_1_histology["polyp carcinoma"]
    del polyp_1_histology["adenoma sub type"]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
        polyp_1_information=polyp_1_information,
        polyp_1_intervention=polyp_1_intervention,
        polyp_1_histology=polyp_1_histology,
    )

    assert_test_results(page, "11")


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.investigation_dataset_tests
def test_identify_advanced_colorectal_polyp_from_histology_f(page: Page) -> None:
    """
    This test identifies an advanced colorectal polyp from histology results (BCSS-5567 - F).
    """
    polyp_1_information = make_polyp_1_information(
        **{
            "location": EndoscopyLocationOptions.HEPATIC_FLEXURE,
            "classification": PolypClassificationOptions.IIC,
        }
    )

    polyp_1_intervention = make_polyp_1_intervention(
        **{
            "modality": PolypInterventionModalityOptions.ESD,
            "device": PolypInterventionDeviceOptions.HOT_SNARE,
            "excision technique": PolypInterventionExcisionTechniqueOptions.PIECE_MEAL,
        }
    )

    polyp_1_histology = make_polyp_1_histology(
        **{
            "serrated lesion sub type": SerratedLesionSubTypeOptions.SESSILE_SERRATED_LESION,
        }
    )
    del polyp_1_histology["polyp dysplasia"]
    del polyp_1_histology["adenoma sub type"]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
        polyp_1_information=polyp_1_information,
        polyp_1_intervention=polyp_1_intervention,
        polyp_1_histology=polyp_1_histology,
    )

    assert_test_results(page, "10")


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.investigation_dataset_tests
def test_identify_advanced_colorectal_polyp_from_histology_g(page: Page) -> None:
    """
    This test identifies an advanced colorectal polyp from histology results (BCSS-5567 - G).
    """
    polyp_1_information = make_polyp_1_information(
        **{
            "location": EndoscopyLocationOptions.ASCENDING_COLON,
            "classification": PolypClassificationOptions.LST_G,
        }
    )

    polyp_1_intervention = make_polyp_1_intervention(
        **{
            "excision technique": PolypInterventionExcisionTechniqueOptions.EN_BLOC,
        }
    )

    polyp_1_histology = make_polyp_1_histology(
        **{
            "polyp type": PolypTypeOptions.ADENOMA,
            "polyp dysplasia": PolypDysplasiaOptions.LOW_GRADE_DYSPLASIA,
        }
    )
    del polyp_1_histology["serrated lesion sub type"]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
        polyp_1_information=polyp_1_information,
        polyp_1_intervention=polyp_1_intervention,
        polyp_1_histology=polyp_1_histology,
    )

    assert_test_results(page, "10")


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.investigation_dataset_tests
def test_identify_advanced_colorectal_polyp_from_histology_h(page: Page) -> None:
    """
    This test identifies an advanced colorectal polyp from histology results (BCSS-5567 - H).
    """
    polyp_1_information = make_polyp_1_information(
        **{
            "location": EndoscopyLocationOptions.CAECUM,
            "classification": PolypClassificationOptions.LST_NG,
            "estimate of whole polyp size": "10",
        }
    )

    polyp_1_intervention = make_polyp_1_intervention(
        **{
            "modality": PolypInterventionModalityOptions.EMR,
            "excision technique": PolypInterventionExcisionTechniqueOptions.EN_BLOC,
        }
    )

    polyp_1_histology = make_polyp_1_histology(
        **{
            "polyp type": PolypTypeOptions.ADENOMA,
            "polyp size": "12",
        }
    )
    del polyp_1_histology["serrated lesion sub type"]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
        polyp_1_information=polyp_1_information,
        polyp_1_intervention=polyp_1_intervention,
        polyp_1_histology=polyp_1_histology,
    )

    assert_test_results(page, "12")


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.investigation_dataset_tests
def test_identify_advanced_colorectal_polyp_from_histology_i(page: Page) -> None:
    """
    This test identifies an advanced colorectal polyp from histology results (BCSS-5567 - I).
    """
    polyp_1_information = make_polyp_1_information(
        **{
            "location": EndoscopyLocationOptions.ILEUM,
            "classification": PolypClassificationOptions.IIA,
            "estimate of whole polyp size": "9",
        }
    )

    polyp_1_intervention = make_polyp_1_intervention(
        **{
            "modality": PolypInterventionModalityOptions.ESD,
            "device": PolypInterventionDeviceOptions.HOT_SNARE,
            "excision technique": PolypInterventionExcisionTechniqueOptions.EN_BLOC,
        }
    )

    polyp_1_histology = make_polyp_1_histology(
        **{
            "polyp type": PolypTypeOptions.ADENOMA,
            "adenoma sub type": AdenomaSubTypeOptions.VILLOUS_ADENOMA,
            "polyp size": "11",
            "polyp dysplasia": PolypDysplasiaOptions.LOW_GRADE_DYSPLASIA,
        }
    )
    del polyp_1_histology["serrated lesion sub type"]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
        polyp_1_information=polyp_1_information,
        polyp_1_intervention=polyp_1_intervention,
        polyp_1_histology=polyp_1_histology,
    )

    assert_test_results(page, "11")


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.investigation_dataset_tests
def test_identify_advanced_colorectal_polyp_from_histology_j(page: Page) -> None:
    """
    This test identifies an advanced colorectal polyp from histology results (BCSS-5567 - J).
    """
    polyp_1_information = make_polyp_1_information(
        **{
            "location": EndoscopyLocationOptions.ANASTOMOSIS,
            "classification": PolypClassificationOptions.IP,
            "estimate of whole polyp size": "11",
        }
    )

    polyp_1_intervention = make_polyp_1_intervention()

    polyp_1_histology = make_polyp_1_histology(
        **{
            "polyp type": PolypTypeOptions.ADENOMA,
            "adenoma sub type": AdenomaSubTypeOptions.NOT_REPORTED,
            "polyp size": "13",
            "polyp carcinoma": YesNoUncertainOptions.UNCERTAIN,
        }
    )
    del polyp_1_histology["serrated lesion sub type"]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
        polyp_1_information=polyp_1_information,
        polyp_1_intervention=polyp_1_intervention,
        polyp_1_histology=polyp_1_histology,
    )

    assert_test_results(page, "13")


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.investigation_dataset_tests
def test_identify_advanced_colorectal_polyp_from_histology_k(page: Page) -> None:
    """
    This test identifies an advanced colorectal polyp from histology results (BCSS-5567 - K).
    """
    polyp_1_information = make_polyp_1_information(
        **{
            "classification": PolypClassificationOptions.ISP,
            "estimate of whole polyp size": "6",
        }
    )

    polyp_1_intervention = make_polyp_1_intervention(
        **{
            "modality": PolypInterventionModalityOptions.EMR,
            "excision technique": PolypInterventionExcisionTechniqueOptions.PIECE_MEAL,
        }
    )

    polyp_1_histology = make_polyp_1_histology(
        **{
            "polyp size": "7",
            "polyp dysplasia": PolypDysplasiaOptions.HIGH_GRADE_DYSPLASIA,
        }
    )
    del polyp_1_histology["adenoma sub type"]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
        polyp_1_information=polyp_1_information,
        polyp_1_intervention=polyp_1_intervention,
        polyp_1_histology=polyp_1_histology,
    )

    assert_test_results(page, "7")


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.investigation_dataset_tests
def test_identify_advanced_colorectal_polyp_from_histology_l(page: Page) -> None:
    """
    This test identifies an advanced colorectal polyp from histology results (BCSS-5567 - L).
    """
    polyp_1_information = make_polyp_1_information(
        **{
            "location": EndoscopyLocationOptions.RECTUM,
            "estimate of whole polyp size": "6",
        }
    )

    polyp_1_intervention = make_polyp_1_intervention(
        **{
            "modality": PolypInterventionModalityOptions.ESD,
            "device": PolypInterventionDeviceOptions.ENDOSCOPIC_KNIFE,
            "excision technique": PolypInterventionExcisionTechniqueOptions.PIECE_MEAL,
        }
    )

    polyp_1_histology = make_polyp_1_histology(
        **{
            "polyp size": "5",
            "polyp dysplasia": PolypDysplasiaOptions.LOW_GRADE_DYSPLASIA,
        }
    )
    del polyp_1_histology["adenoma sub type"]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
        polyp_1_information=polyp_1_information,
        polyp_1_intervention=polyp_1_intervention,
        polyp_1_histology=polyp_1_histology,
    )

    assert_test_results(page, "6")


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.investigation_dataset_tests
def test_identify_advanced_colorectal_polyp_from_histology_m(page: Page) -> None:
    """
    This test identifies an advanced colorectal polyp from histology results (BCSS-5567 - M).
    """
    polyp_1_information = make_polyp_1_information(
        **{
            "location": EndoscopyLocationOptions.SIGMOID_COLON,
            "classification": PolypClassificationOptions.IIA,
            "estimate of whole polyp size": "4",
        }
    )

    polyp_1_intervention = make_polyp_1_intervention(
        **{
            "excision technique": PolypInterventionExcisionTechniqueOptions.EN_BLOC,
        }
    )

    polyp_1_histology = make_polyp_1_histology(
        **{
            "polyp type": PolypTypeOptions.ADENOMA,
            "polyp size": "5",
            "polyp dysplasia": PolypDysplasiaOptions.HIGH_GRADE_DYSPLASIA,
        }
    )
    del polyp_1_histology["serrated lesion sub type"]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
        polyp_1_information=polyp_1_information,
        polyp_1_intervention=polyp_1_intervention,
        polyp_1_histology=polyp_1_histology,
    )

    assert_test_results(page, "5")


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.investigation_dataset_tests
def test_identify_advanced_colorectal_polyp_from_histology_n(page: Page) -> None:
    """
    This test identifies an advanced colorectal polyp from histology results (BCSS-5567 - N).
    """
    polyp_1_information = make_polyp_1_information(
        **{
            "location": EndoscopyLocationOptions.DESCENDING_COLON,
            "classification": PolypClassificationOptions.IIB,
            "estimate of whole polyp size": "5",
        }
    )

    polyp_1_intervention = make_polyp_1_intervention(
        **{
            "modality": PolypInterventionModalityOptions.EMR,
            "excision technique": PolypInterventionExcisionTechniqueOptions.EN_BLOC,
        }
    )

    polyp_1_histology = make_polyp_1_histology(
        **{
            "polyp type": PolypTypeOptions.ADENOMA,
            "adenoma sub type": AdenomaSubTypeOptions.TUBULOVILLOUS_ADENOMA,
            "polyp size": "4",
            "polyp dysplasia": PolypDysplasiaOptions.HIGH_GRADE_DYSPLASIA,
        }
    )
    del polyp_1_histology["serrated lesion sub type"]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
        polyp_1_information=polyp_1_information,
        polyp_1_intervention=polyp_1_intervention,
        polyp_1_histology=polyp_1_histology,
    )

    assert_test_results(page, "4")


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.investigation_dataset_tests
def test_identify_advanced_colorectal_polyp_from_histology_o(page: Page) -> None:
    """
    This test identifies an advanced colorectal polyp from histology results (BCSS-5567 - O).
    """
    polyp_1_information = make_polyp_1_information(
        **{
            "location": EndoscopyLocationOptions.SPLENIC_FLEXURE,
            "classification": PolypClassificationOptions.IIC,
            "estimate of whole polyp size": "2",
        }
    )

    polyp_1_intervention = make_polyp_1_intervention(
        **{
            "modality": PolypInterventionModalityOptions.ESD,
            "device": PolypInterventionDeviceOptions.HOT_SNARE,
            "excision technique": PolypInterventionExcisionTechniqueOptions.EN_BLOC,
        }
    )

    polyp_1_histology = make_polyp_1_histology(
        **{
            "polyp type": PolypTypeOptions.ADENOMA,
            "adenoma sub type": AdenomaSubTypeOptions.VILLOUS_ADENOMA,
            "polyp size": "3",
            "polyp dysplasia": PolypDysplasiaOptions.HIGH_GRADE_DYSPLASIA,
        }
    )
    del polyp_1_histology["serrated lesion sub type"]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
        polyp_1_information=polyp_1_information,
        polyp_1_intervention=polyp_1_intervention,
        polyp_1_histology=polyp_1_histology,
    )

    assert_test_results(page, "3")


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.investigation_dataset_tests
def test_identify_advanced_colorectal_polyp_from_histology_p(page: Page) -> None:
    """
    This test identifies an advanced colorectal polyp from histology results (BCSS-5567 - P).
    """
    polyp_1_information = make_polyp_1_information(
        **{
            "location": EndoscopyLocationOptions.TRANSVERSE_COLON,
            "classification": PolypClassificationOptions.LST_G,
            "estimate of whole polyp size": "1",
        }
    )

    polyp_1_intervention = make_polyp_1_intervention(
        **{
            "excision technique": PolypInterventionExcisionTechniqueOptions.PIECE_MEAL,
        }
    )

    polyp_1_histology = make_polyp_1_histology(
        **{
            "polyp type": PolypTypeOptions.ADENOMA,
            "adenoma sub type": AdenomaSubTypeOptions.NOT_REPORTED,
            "polyp size": "2",
            "polyp dysplasia": PolypDysplasiaOptions.HIGH_GRADE_DYSPLASIA,
        }
    )
    del polyp_1_histology["serrated lesion sub type"]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
        polyp_1_information=polyp_1_information,
        polyp_1_intervention=polyp_1_intervention,
        polyp_1_histology=polyp_1_histology,
    )

    assert_test_results(page, "2")


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.investigation_dataset_tests
def test_identify_advanced_colorectal_polyp_from_histology_q(page: Page) -> None:
    """
    This test identifies an advanced colorectal polyp from histology results (BCSS-5567 - Q).
    """
    polyp_1_information = make_polyp_1_information(
        **{
            "location": EndoscopyLocationOptions.HEPATIC_FLEXURE,
            "classification": PolypClassificationOptions.IP,
            "estimate of whole polyp size": "19",
        }
    )

    polyp_1_intervention = make_polyp_1_intervention(
        **{
            "modality": PolypInterventionModalityOptions.EMR,
        }
    )

    polyp_1_histology = make_polyp_1_histology(
        **{
            "polyp type": PolypTypeOptions.ADENOMA,
            "adenoma sub type": AdenomaSubTypeOptions.VILLOUS_ADENOMA,
            "polyp size": "20",
        }
    )
    del polyp_1_histology["serrated lesion sub type"]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
        polyp_1_information=polyp_1_information,
        polyp_1_intervention=polyp_1_intervention,
        polyp_1_histology=polyp_1_histology,
    )

    assert_test_results(page, "20")


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.skip_before_test
@pytest.mark.investigation_dataset_tests
def test_identify_advanced_colorectal_polyp_from_histology_r(page: Page) -> None:
    """
    This test identifies an advanced colorectal polyp from histology results (BCSS-5567 - R).
    """
    criteria = {
        "latest episode has colonoscopy assessment dataset": "yes_complete",
        "latest episode has diagnostic test": "no",
        "latest event status": "A99",
        "latest episode type": "FOBT",
        "latest episode started": "less than 4 years ago",
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
    BasePage(page).click_main_menu_link()
    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()

    AdvanceFOBTScreeningEpisodePage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())

    AdvanceFOBTScreeningEpisodePage(page).select_test_type_dropdown_option(
        "Colonoscopy"
    )

    AdvanceFOBTScreeningEpisodePage(page).click_invite_for_diagnostic_test_button()
    AdvanceFOBTScreeningEpisodePage(page).verify_latest_event_status_value(
        "A59 - Invited for Diagnostic Test"
    )

    AdvanceFOBTScreeningEpisodePage(page).click_attend_diagnostic_test_button()

    AttendDiagnosticTestPage(page).select_actual_type_of_test_dropdown_option(
        "Colonoscopy"
    )
    AttendDiagnosticTestPage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())
    AttendDiagnosticTestPage(page).click_save_button()
    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A259 - Attended Diagnostic Test"
    )

    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    polyp_1_information = make_polyp_1_information(
        **{
            "location": EndoscopyLocationOptions.ASCENDING_COLON,
            "classification": PolypClassificationOptions.LST_NG,
            "estimate of whole polyp size": "5",
        }
    )

    polyp_1_intervention = make_polyp_1_intervention(
        **{
            "modality": PolypInterventionModalityOptions.ESD,
            "device": PolypInterventionDeviceOptions.HOT_SNARE,
            "excision technique": PolypInterventionExcisionTechniqueOptions.PIECE_MEAL,
        }
    )

    polyp_1_histology = make_polyp_1_histology(
        **{
            "serrated lesion sub type": SerratedLesionSubTypeOptions.TRADITIONAL_SERRATED_ADENOMA,
            "polyp size": "6",
            "polyp dysplasia": PolypDysplasiaOptions.LOW_GRADE_DYSPLASIA,
        }
    )
    del polyp_1_histology["adenoma sub type"]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
        polyp_1_information=polyp_1_information,
        polyp_1_intervention=polyp_1_intervention,
        polyp_1_histology=polyp_1_histology,
    )

    # Enter the test outcome > A315
    BasePage(page).click_back_button()
    BasePage(page).click_back_button()
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_enter_diagnostic_test_outcome_button()
    DiagnosticTestOutcomePage(page).select_test_outcome_option(
        OutcomeOfDiagnosticTest.FAILED_TEST_REFER_ANOTHER
    )
    DiagnosticTestOutcomePage(page).click_save_button()
    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A315 - Diagnostic Test Outcome Entered"
    )

    # Make post investigation contact > A361
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_other_post_investigation_button()
    AdvanceFOBTScreeningEpisodePage(page).verify_latest_event_status_value(
        "A361 - Other Post-investigation Contact Required"
    )

    AdvanceFOBTScreeningEpisodePage(
        page
    ).click_record_other_post_investigation_contact_button()
    ContactWithPatientPage(page).select_direction_dropdown_option("To patient")
    ContactWithPatientPage(page).select_caller_id_dropdown_index_option(1)
    ContactWithPatientPage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())
    ContactWithPatientPage(page).enter_start_time("11:00")
    ContactWithPatientPage(page).enter_end_time("12:00")
    ContactWithPatientPage(page).enter_discussion_record_text("Test Automation")
    ContactWithPatientPage(page).select_outcome_dropdown_option(
        "Post-investigation Appointment Not Required"
    )
    ContactWithPatientPage(page).click_save_button()
    BasePage(page).click_back_button()
    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A318 - Post-investigation Appointment NOT Required - Result Letter Created"
    )

    # Process the A318 letters > A380
    batch_processing(
        page,
        "A318",
        "Result Letters - No Post-investigation Appointment",
        "A380 - Failed Diagnostic Test - Refer Another",
    )

    # Another contact to bring the subject back to A99
    SubjectScreeningSummaryPage(page).click_advance_fobt_screening_episode_button()
    AdvanceFOBTScreeningEpisodePage(page).click_record_contact_with_patient_button()
    ContactWithPatientPage(page).select_direction_dropdown_option("To patient")
    ContactWithPatientPage(page).select_caller_id_dropdown_index_option(1)
    ContactWithPatientPage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())
    ContactWithPatientPage(page).enter_start_time("11:00")
    ContactWithPatientPage(page).enter_end_time("12:00")
    ContactWithPatientPage(page).enter_discussion_record_text("Test Automation")
    ContactWithPatientPage(page).select_outcome_dropdown_option(
        "Suitable for Endoscopic Test"
    )
    ContactWithPatientPage(page).click_save_button()
    AdvanceFOBTScreeningEpisodePage(page).verify_latest_event_status_value(
        "A99 - Suitable for Endoscopic Test"
    )

    # Invite for 2nd diagnostic test > A59 - check options
    AdvanceFOBTScreeningEpisodePage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())
    AdvanceFOBTScreeningEpisodePage(page).select_test_type_dropdown_option_2(
        "Colonoscopy"
    )
    AdvanceFOBTScreeningEpisodePage(page).click_invite_for_diagnostic_test_button()
    AdvanceFOBTScreeningEpisodePage(page).click_attend_diagnostic_test_button()
    AttendDiagnosticTestPage(page).select_actual_type_of_test_dropdown_option(
        "Colonoscopy"
    )
    AttendDiagnosticTestPage(page).click_calendar_button()
    CalendarPicker(page).v1_calender_picker(datetime.today())
    AttendDiagnosticTestPage(page).click_save_button()
    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        "A259 - Attended Diagnostic Test"
    )
    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
        polyp_1_information=polyp_1_information,
        polyp_1_intervention=polyp_1_intervention,
        polyp_1_histology=polyp_1_histology,
    )

    assert_test_results(page, "6")


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.investigation_dataset_tests
def test_identify_advanced_colorectal_polyp_from_histology_s(page: Page) -> None:
    """
    This test identifies an advanced colorectal polyp from histology results (BCSS-5567 - S).
    """
    polyp_1_information = make_polyp_1_information(
        **{
            "location": EndoscopyLocationOptions.ILEUM,
            "classification": PolypClassificationOptions.IP,
            "estimate of whole polyp size": "30",
        }
    )

    polyp_1_intervention = make_polyp_1_intervention(
        **{
            "device": PolypInterventionDeviceOptions.HOT_SNARE,
        }
    )

    polyp_1_histology = make_polyp_1_histology(
        **{
            "polyp size": "32",
        }
    )
    del polyp_1_histology["adenoma sub type"]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        completion_information=completion_information,
        polyp_1_information=polyp_1_information,
        polyp_1_intervention=polyp_1_intervention,
        polyp_1_histology=polyp_1_histology,
    )

    assert_test_results(page, "32")


def obtain_test_data() -> pd.DataFrame:
    """
    This function builds a query to retrieve subjects based on specific criteria
    and returns a DataFrame containing the results.
    """
    criteria = {
        "latest episode status": "open",
        "latest episode latest investigation dataset": "colonoscopy_new",
        "latest episode started": "less than 4 years ago",
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
    return df


def make_polyp_1_information(**overrides):
    """
    Create a dictionary containing default information about Polyp 1.

    This includes standard attributes such as location, classification,
    size, access, and whether it was left in situ.

    Parameters:
        **overrides: Arbitrary keyword arguments to override any default values.

    Returns:
        dict: A dictionary representing polyp information.
    """
    data = {
        "location": EndoscopyLocationOptions.APPENDIX,
        "classification": PolypClassificationOptions.IS,
        "estimate of whole polyp size": "8",
        "polyp access": PolypAccessOptions.EASY,
        "left in situ": YesNoOptions.NO,
    }
    data.update(overrides)
    return data


def make_polyp_1_intervention(**overrides):
    """
    Create a dictionary containing default intervention data for Polyp 1.

    This includes the intervention modality, device used, and whether
    the polyp was excised and retrieved.

    Parameters:
        **overrides: Arbitrary keyword arguments to override any default values.

    Returns:
        dict: A dictionary representing polyp intervention details.
    """
    data = {
        "modality": PolypInterventionModalityOptions.POLYPECTOMY,
        "device": PolypInterventionDeviceOptions.COLD_SNARE,
        "excised": YesNoOptions.YES,
        "retrieved": YesNoOptions.YES,
    }
    data.update(overrides)
    return data


def make_polyp_1_histology(**overrides):
    """
    Create a dictionary containing default histology data for Polyp 1.

    This includes pathology-related information such as dates, provider,
    pathologist, polyp type, subtypes, excision completeness, size,
    dysplasia, and carcinoma status.

    Parameters:
        **overrides: Arbitrary keyword arguments to override any default values.

    Returns:
        dict: A dictionary representing polyp histology details.
    """
    data = {
        "date of receipt": datetime.today(),
        "date of reporting": datetime.today(),
        "pathology provider": -1,
        "pathologist": -1,
        "polyp type": PolypTypeOptions.SERRATED_LESION,
        "serrated lesion sub type": SerratedLesionSubTypeOptions.MIXED_POLYP,
        "adenoma sub type": AdenomaSubTypeOptions.TUBULAR_ADENOMA,
        "polyp excision complete": PolypExcisionCompleteOptions.R1,
        "polyp size": "10",
        "polyp dysplasia": PolypDysplasiaOptions.NOT_REPORTED,
        "polyp carcinoma": YesNoUncertainOptions.NO,
    }
    data.update(overrides)
    return data


def assert_test_results(page: Page, expected_size: str) -> None:
    """
    This function asserts that the polyp algorithm size and category match the expected values.
    """
    logging.info(
        f"Asserting test results\nExpected result: Abnormal\nExpected size: {expected_size}\nExpected category: Advanced colorectal polyp"
    )
    InvestigationDatasetsPage(page).expect_text_to_be_visible("Abnormal")
    InvestigationDatasetsPage(page).assert_polyp_alogrithm_size(1, expected_size)
    InvestigationDatasetsPage(page).assert_polyp_categrory(
        1, "Advanced colorectal polyp"
    )
    InvestigationDatasetsPage(page).click_edit_dataset_button()
    InvestigationDatasetsPage(page).check_dataset_incomplete_checkbox()
    InvestigationDatasetsPage(page).click_save_dataset_button()
    InvestigationDatasetsPage(page).assert_polyp_alogrithm_size(1, None)
    InvestigationDatasetsPage(page).assert_polyp_categrory(1, None)
    logging.info("Test results asserted successfully.")

    LogoutPage(page).log_out()
