import logging
import pytest
from pytest import FixtureRequest
from datetime import datetime
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.datasets.investigation_dataset_page import (
    EndoscopyLocationOptions,
    YesNoOptions,
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
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from utils.investigation_dataset import (
    InvestigationDatasetCompletion,
)
from utils.screening_subject_page_searcher import (
    search_subject_episode_by_nhs_number,
)
from utils.datasets.investigation_datasets import (
    get_subject_with_investigation_dataset_ready,
    go_from_investigation_dataset_complete_to_a259_status,
    get_subject_with_a99_status,
    go_from_a99_status_to_a259_status,
    get_default_endoscopy_information,
    get_default_drug_information,
    get_default_general_information,
    complete_and_assert_investigation,
)
from utils.user_tools import UserTools

# Defining dictionaries used in tests
general_information = get_default_general_information()

drug_information = get_default_drug_information()

endoscopy_information = get_default_endoscopy_information()
endoscopy_information["endoscopist defined extent"] = EndoscopyLocationOptions.APPENDIX

failure_information = {
    "failure reasons": FailureReasonsOptions.ADHESION,
}

completion_information = {
    "completion proof": CompletionProofOptions.VIDEO_APPENDIX,
}

category_as_string = "Advanced colorectal polyp"


@pytest.fixture(autouse=True)
def before_test(page: Page, request: FixtureRequest) -> None:
    """
    Before each test this will get the relevant subject and navigate to their investigation dataset
    """
    if request.node.get_closest_marker("skip_before_test"):
        return
    df = get_subject_with_investigation_dataset_ready()
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

    complete_and_assert_investigation(
        page,
        general_information,
        drug_information,
        endoscopy_information,
        failure_information,
        polyp_1_information,
        polyp_1_intervention,
        polyp_1_histology,
        expected_category=category_as_string,
        expected_size="9",
    )


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

    complete_and_assert_investigation(
        page,
        general_information,
        drug_information,
        endoscopy_information,
        failure_information,
        polyp_1_information,
        polyp_1_intervention,
        polyp_1_histology,
        expected_category=category_as_string,
        expected_size="8",
    )


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

    complete_and_assert_investigation(
        page,
        general_information,
        drug_information,
        endoscopy_information,
        failure_information,
        polyp_1_information,
        polyp_1_intervention,
        polyp_1_histology,
        expected_category=category_as_string,
        expected_size="10",
    )


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

    complete_and_assert_investigation(
        page,
        general_information,
        drug_information,
        endoscopy_information,
        failure_information,
        polyp_1_information,
        polyp_1_intervention,
        polyp_1_histology,
        expected_category=category_as_string,
        expected_size="11",
    )


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

    complete_and_assert_investigation(
        page,
        general_information,
        drug_information,
        endoscopy_information,
        failure_information,
        polyp_1_information,
        polyp_1_intervention,
        polyp_1_histology,
        expected_category=category_as_string,
        expected_size="11",
    )


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

    complete_and_assert_investigation(
        page,
        general_information,
        drug_information,
        endoscopy_information,
        failure_information,
        polyp_1_information,
        polyp_1_intervention,
        polyp_1_histology,
        expected_category=category_as_string,
        expected_size="10",
    )


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

    complete_and_assert_investigation(
        page,
        general_information,
        drug_information,
        endoscopy_information,
        failure_information,
        polyp_1_information,
        polyp_1_intervention,
        polyp_1_histology,
        expected_category=category_as_string,
        expected_size="10",
    )


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

    complete_and_assert_investigation(
        page,
        general_information,
        drug_information,
        endoscopy_information,
        failure_information,
        polyp_1_information,
        polyp_1_intervention,
        polyp_1_histology,
        expected_category=category_as_string,
        expected_size="12",
    )


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

    complete_and_assert_investigation(
        page,
        general_information,
        drug_information,
        endoscopy_information,
        failure_information,
        polyp_1_information,
        polyp_1_intervention,
        polyp_1_histology,
        expected_category=category_as_string,
        expected_size="11",
    )


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

    complete_and_assert_investigation(
        page,
        general_information,
        drug_information,
        endoscopy_information,
        failure_information,
        polyp_1_information,
        polyp_1_intervention,
        polyp_1_histology,
        expected_category=category_as_string,
        expected_size="13",
    )


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

    complete_and_assert_investigation(
        page,
        general_information,
        drug_information,
        endoscopy_information,
        failure_information,
        polyp_1_information,
        polyp_1_intervention,
        polyp_1_histology,
        expected_category=category_as_string,
        expected_size="7",
    )


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

    complete_and_assert_investigation(
        page,
        general_information,
        drug_information,
        endoscopy_information,
        failure_information,
        polyp_1_information,
        polyp_1_intervention,
        polyp_1_histology,
        expected_category=category_as_string,
        expected_size="6",
    )


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

    complete_and_assert_investigation(
        page,
        general_information,
        drug_information,
        endoscopy_information,
        failure_information,
        polyp_1_information,
        polyp_1_intervention,
        polyp_1_histology,
        expected_category=category_as_string,
        expected_size="5",
    )


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

    complete_and_assert_investigation(
        page,
        general_information,
        drug_information,
        endoscopy_information,
        failure_information,
        polyp_1_information,
        polyp_1_intervention,
        polyp_1_histology,
        expected_category=category_as_string,
        expected_size="4",
    )


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

    complete_and_assert_investigation(
        page,
        general_information,
        drug_information,
        endoscopy_information,
        failure_information,
        polyp_1_information,
        polyp_1_intervention,
        polyp_1_histology,
        expected_category=category_as_string,
        expected_size="3",
    )


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

    complete_and_assert_investigation(
        page,
        general_information,
        drug_information,
        endoscopy_information,
        failure_information,
        polyp_1_information,
        polyp_1_intervention,
        polyp_1_histology,
        expected_category=category_as_string,
        expected_size="2",
    )


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

    complete_and_assert_investigation(
        page,
        general_information,
        drug_information,
        endoscopy_information,
        failure_information,
        polyp_1_information,
        polyp_1_intervention,
        polyp_1_histology,
        expected_category=category_as_string,
        expected_size="20",
    )


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.skip_before_test
@pytest.mark.investigation_dataset_tests
def test_identify_advanced_colorectal_polyp_from_histology_r(page: Page) -> None:
    """
    This test identifies an advanced colorectal polyp from histology results (BCSS-5567 - R).
    """
    df = get_subject_with_a99_status()

    nhs_no = df.iloc[0]["subject_nhs_number"]
    logging.info(f"NHS Number: {nhs_no}")

    UserTools.user_login(page, "Screening Centre Manager at BCS001")
    go_from_a99_status_to_a259_status(page, nhs_no)

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

    polyp_information = [polyp_1_information]
    polyp_intervention = [polyp_1_intervention]
    polyp_histology = [polyp_1_histology]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        polyp_information=polyp_information,
        polyp_intervention=polyp_intervention,
        polyp_histology=polyp_histology,
    )

    go_from_investigation_dataset_complete_to_a259_status(page)
    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    complete_and_assert_investigation(
        page,
        general_information,
        drug_information,
        endoscopy_information,
        failure_information,
        polyp_1_information,
        polyp_1_intervention,
        polyp_1_histology,
        expected_category=category_as_string,
        expected_size="6",
    )


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

    complete_and_assert_investigation(
        page,
        general_information,
        drug_information,
        endoscopy_information,
        failure_information,
        polyp_1_information,
        polyp_1_intervention,
        polyp_1_histology,
        expected_category=category_as_string,
        expected_size="32",
    )


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
