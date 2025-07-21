import logging
import pytest
from datetime import datetime
from playwright.sync_api import Page
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
    FailureReasonsOptions,
    PolypClassificationOptions,
    PolypAccessOptions,
    PolypInterventionModalityOptions,
    PolypInterventionDeviceOptions,
    PolypInterventionExcisionTechniqueOptions,
    PolypTypeOptions,
    SerratedLesionSubTypeOptions,
    PolypExcisionCompleteOptions,
)
from pages.datasets.subject_datasets_page import SubjectDatasetsPage
from pages.logout.log_out_page import LogoutPage
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
    get_subject_with_investigation_dataset_ready,
    go_from_investigation_dataset_complete_to_a259_status,
    get_subject_with_a99_status,
    go_from_a99_status_to_a259_status,
)

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
    "endoscopist defined extent": EndoscopyLocationOptions.DESCENDING_COLON,
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


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.investigation_dataset_tests
def test_identify_diminutive_rectal_hyperplastic_polyp_from_histology_a(
    page: Page,
) -> None:
    """
    This test identifies a diminutive rectal hyperplastic polyp from histology results. (BCSS-4659 - A)
    """
    df = get_subject_with_investigation_dataset_ready()
    nhs_no = df.iloc[0]["subject_nhs_number"]
    logging.info(f"NHS Number: {nhs_no}")

    UserTools.user_login(page, "Screening Centre Manager at BCS001")
    BasePage(page).click_main_menu_link()
    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)

    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    polyp_1_information = {
        "location": EndoscopyLocationOptions.RECTUM,
        "classification": PolypClassificationOptions.IP,
        "estimate of whole polyp size": "6",
        "polyp access": PolypAccessOptions.EASY,
        "left in situ": YesNoOptions.NO,
    }

    polyp_1_intervention = {
        "modality": PolypInterventionModalityOptions.POLYPECTOMY,
        "device": PolypInterventionDeviceOptions.HOT_SNARE,
        "excised": YesNoOptions.YES,
        "retrieved": YesNoOptions.YES,
    }

    polyp_1_histology = {
        "date of receipt": datetime.today(),
        "date of reporting": datetime.today(),
        "pathology provider": -1,
        "pathologist": -1,
        "polyp type": PolypTypeOptions.SERRATED_LESION,
        "serrated lesion sub type": SerratedLesionSubTypeOptions.HYPERPLASTIC_POLYP,
        "polyp excision complete": PolypExcisionCompleteOptions.R1,
        "polyp size": "5",
    }

    polyp_2_information = {
        "location": EndoscopyLocationOptions.RECTUM,
        "classification": PolypClassificationOptions.ISP,
        "estimate of whole polyp size": "1",
        "polyp access": PolypAccessOptions.EASY,
        "left in situ": YesNoOptions.NO,
    }

    polyp_2_intervention = {
        "modality": PolypInterventionModalityOptions.EMR,
        "device": PolypInterventionDeviceOptions.HOT_SNARE,
        "excised": YesNoOptions.YES,
        "retrieved": YesNoOptions.YES,
    }

    polyp_2_histology = {
        "date of receipt": datetime.today(),
        "date of reporting": datetime.today(),
        "pathology provider": -1,
        "pathologist": -1,
        "polyp type": PolypTypeOptions.SERRATED_LESION,
        "serrated lesion sub type": SerratedLesionSubTypeOptions.HYPERPLASTIC_POLYP,
        "polyp excision complete": PolypExcisionCompleteOptions.R1,
        "polyp size": "1",
    }

    polyp_3_information = {
        "location": EndoscopyLocationOptions.RECTUM,
        "classification": PolypClassificationOptions.IS,
        "estimate of whole polyp size": "2",
        "polyp access": PolypAccessOptions.EASY,
        "left in situ": YesNoOptions.NO,
    }

    polyp_3_intervention = {
        "modality": PolypInterventionModalityOptions.ESD,
        "device": PolypInterventionDeviceOptions.ENDOSCOPIC_KNIFE,
        "excised": YesNoOptions.YES,
        "retrieved": YesNoOptions.YES,
    }

    polyp_3_histology = {
        "date of receipt": datetime.today(),
        "date of reporting": datetime.today(),
        "pathology provider": -1,
        "pathologist": -1,
        "polyp type": PolypTypeOptions.SERRATED_LESION,
        "serrated lesion sub type": SerratedLesionSubTypeOptions.HYPERPLASTIC_POLYP,
        "polyp excision complete": PolypExcisionCompleteOptions.R1,
        "polyp size": "3",
    }

    polyp_4_information = {
        "location": EndoscopyLocationOptions.RECTUM,
        "classification": PolypClassificationOptions.IIC,
        "estimate of whole polyp size": "5",
        "polyp access": PolypAccessOptions.EASY,
        "left in situ": YesNoOptions.NO,
    }

    polyp_4_intervention = {
        "modality": PolypInterventionModalityOptions.POLYPECTOMY,
        "device": PolypInterventionDeviceOptions.HOT_SNARE,
        "excised": YesNoOptions.YES,
        "retrieved": YesNoOptions.YES,
        "excision technique": PolypInterventionExcisionTechniqueOptions.PIECE_MEAL,
    }

    polyp_4_histology = {
        "date of receipt": datetime.today(),
        "date of reporting": datetime.today(),
        "pathology provider": -1,
        "pathologist": -1,
        "polyp type": PolypTypeOptions.SERRATED_LESION,
        "serrated lesion sub type": SerratedLesionSubTypeOptions.HYPERPLASTIC_POLYP,
        "polyp excision complete": PolypExcisionCompleteOptions.R1,
        "polyp size": "4",
    }

    polyp_information = [
        polyp_1_information,
        polyp_2_information,
        polyp_3_information,
        polyp_4_information,
    ]
    polyp_intervention = [
        polyp_1_intervention,
        polyp_2_intervention,
        polyp_3_intervention,
        polyp_4_intervention,
    ]
    polyp_histology = [
        polyp_1_histology,
        polyp_2_histology,
        polyp_3_histology,
        polyp_4_histology,
    ]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        polyp_information=polyp_information,
        polyp_intervention=polyp_intervention,
        polyp_histology=polyp_histology,
    )

    polyp_category_string = "Diminutive rectal hyperplastic polyp"
    InvestigationDatasetsPage(page).expect_text_to_be_visible("Abnormal")
    InvestigationDatasetsPage(page).assert_polyp_alogrithm_size(1, "5")
    InvestigationDatasetsPage(page).assert_polyp_categrory(1, polyp_category_string)
    InvestigationDatasetsPage(page).assert_polyp_alogrithm_size(2, "1")
    InvestigationDatasetsPage(page).assert_polyp_categrory(2, polyp_category_string)
    InvestigationDatasetsPage(page).assert_polyp_alogrithm_size(3, "3")
    InvestigationDatasetsPage(page).assert_polyp_categrory(3, polyp_category_string)
    InvestigationDatasetsPage(page).assert_polyp_alogrithm_size(4, "5")
    InvestigationDatasetsPage(page).assert_polyp_categrory(4, polyp_category_string)

    logging.info("Marking investigation dataset not complete")
    InvestigationDatasetsPage(page).click_edit_dataset_button()
    InvestigationDatasetsPage(page).check_dataset_incomplete_checkbox()
    InvestigationDatasetsPage(page).click_save_dataset_button()
    for polyp_number in range(1, 5):
        InvestigationDatasetsPage(page).assert_polyp_alogrithm_size(polyp_number, None)
        InvestigationDatasetsPage(page).assert_polyp_categrory(polyp_number, None)

    LogoutPage(page).log_out()


@pytest.mark.vpn_required
@pytest.mark.regression
@pytest.mark.investigation_dataset_tests
def test_identify_diminutive_rectal_hyperplastic_polyp_from_histology_b(
    page: Page,
) -> None:
    """
    This test identifies a diminutive rectal hyperplastic polyp from histology results. (BCSS-4659 - B)
    """
    df = get_subject_with_a99_status()
    nhs_no = df.iloc[0]["subject_nhs_number"]
    logging.info(f"NHS Number: {nhs_no}")

    UserTools.user_login(page, "Screening Centre Manager at BCS001")

    go_from_a99_status_to_a259_status(page, nhs_no)

    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    polyp__information = [
        {
            "location": EndoscopyLocationOptions.RECTUM,
            "classification": PolypClassificationOptions.LST_NG,
            "estimate of whole polyp size": "4",
            "polyp access": PolypAccessOptions.EASY,
            "left in situ": YesNoOptions.NO,
        }
    ]
    polyp_intervention = [
        {
            "modality": PolypInterventionModalityOptions.EMR,
            "device": PolypInterventionDeviceOptions.COLD_SNARE,
            "excised": YesNoOptions.YES,
            "retrieved": YesNoOptions.YES,
            "excision technique": PolypInterventionExcisionTechniqueOptions.EN_BLOC,
        }
    ]
    polyp_histology = [
        {
            "date of receipt": datetime.today(),
            "date of reporting": datetime.today(),
            "pathology provider": -1,
            "pathologist": -1,
            "polyp type": PolypTypeOptions.SERRATED_LESION,
            "serrated lesion sub type": SerratedLesionSubTypeOptions.HYPERPLASTIC_POLYP,
            "polyp excision complete": PolypExcisionCompleteOptions.R1,
            "polyp size": "2",
        }
    ]

    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        polyp_information=polyp__information,
        polyp_intervention=polyp_intervention,
        polyp_histology=polyp_histology,
    )
    # Enter the test outcome > A315
    go_from_investigation_dataset_complete_to_a259_status(page)
    SubjectScreeningSummaryPage(page).click_datasets_link()
    SubjectDatasetsPage(page).click_investigation_show_datasets()

    # Complete the investigation dataset
    InvestigationDatasetCompletion(page).complete_dataset_with_args(
        general_information=general_information,
        drug_information=drug_information,
        endoscopy_information=endoscopy_information,
        failure_information=failure_information,
        polyp_information=polyp__information,
        polyp_intervention=polyp_intervention,
        polyp_histology=polyp_histology,
    )

    InvestigationDatasetsPage(page).expect_text_to_be_visible("Abnormal")
    InvestigationDatasetsPage(page).assert_polyp_alogrithm_size(1, "2")
    InvestigationDatasetsPage(page).assert_polyp_categrory(
        1, "Diminutive rectal hyperplastic polyp"
    )

    logging.info("Marking investigation dataset not complete")
    InvestigationDatasetsPage(page).click_edit_dataset_button()
    InvestigationDatasetsPage(page).check_dataset_incomplete_checkbox()
    InvestigationDatasetsPage(page).click_save_dataset_button()
    InvestigationDatasetsPage(page).assert_polyp_alogrithm_size(1, None)
    InvestigationDatasetsPage(page).assert_polyp_categrory(1, None)
    LogoutPage(page).log_out()
