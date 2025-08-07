from playwright.sync_api import Page
from enum import StrEnum
from datetime import datetime
import logging
from typing import Optional
from pages.base_page import BasePage
from utils.screening_subject_page_searcher import verify_subject_event_status_by_nhs_no
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from pages.datasets.subject_datasets_page import SubjectDatasetsPage
from pages.screening_subject_search.handover_into_symptomatic_care_page import (
    HandoverIntoSymptomaticCarePage,
)
from utils.calendar_picker import CalendarPicker
from datetime import datetime
from pages.screening_subject_search.diagnostic_test_outcome_page import (
    DiagnosticTestOutcomePage,
    OutcomeOfDiagnosticTest,
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
from utils.dataset_field_util import DatasetFieldUtil
from pages.screening_subject_search.record_diagnosis_date_page import (
    RecordDiagnosisDatePage,
)


class InvestigationDatasetResults(StrEnum):
    """
    Enum containing the different investigation dataset results.
    This is stored here to result the risk of typo's when calling the methods.
    """

    HIGH_RISK = "High Risk"
    LNPCP = "LNPCP"
    NORMAL = "Normal"


class InvestigationDatasetCompletion:
    """
    This class is used to complete the investigation dataset forms for a subject.
    It contains methods to fill out the forms, and progress episodes, based on the
    age of the subject and the test result.

    This class provides methods to:
    - Navigate to the investigation datasets page for a subject.
    - Fill out investigation dataset forms with default or result-specific data.
    - Handle different investigation outcomes (e.g., HIGH_RISK, LNPCP, NORMAL) by populating relevant form fields and sections.
    - Add and configure polyp information and interventions to trigger specific result scenarios.
    - Save the completed investigation dataset.
    """

    def __init__(self, page: Page):
        self.page = page
        self.estimate_whole_polyp_size_string = "Estimate of whole polyp size"
        self.polyp_access_string = "Polyp Access"
        self.failure_reasons_string = "Failure Reasons"
        self.excision_technique_string = "Excision Technique"

        self.investigation_datasets_pom = InvestigationDatasetsPage(self.page)

    def complete_with_result(self, nhs_no: str, result: str) -> None:
        """This method fills out the investigation dataset forms based on the test result and the subject's age.
        Args:
            nhs_no (str): The NHS number of the subject.
            result (str): The result of the investigation dataset.
                Should be one of InvestigationDatasetResults (HIGH_RISK, LNPCP, NORMAL).
        """
        if result == InvestigationDatasetResults.HIGH_RISK:
            self.go_to_investigation_datasets_page(nhs_no)
            self.default_investigation_dataset_forms()
            self.investigation_datasets_pom.select_therapeutic_procedure_type()
            self.default_investigation_dataset_forms_continuation()
            self.investigation_datasets_failure_reason()
            self.polyps_for_high_risk_result()
            self.save_investigation_dataset()
        elif result == InvestigationDatasetResults.LNPCP:
            self.go_to_investigation_datasets_page(nhs_no)
            self.default_investigation_dataset_forms()
            self.investigation_datasets_pom.select_therapeutic_procedure_type()
            self.default_investigation_dataset_forms_continuation()
            self.investigation_datasets_failure_reason()
            self.polyps_for_lnpcp_result()
            self.save_investigation_dataset()
        elif result == InvestigationDatasetResults.NORMAL:
            self.go_to_investigation_datasets_page(nhs_no)
            self.default_investigation_dataset_forms()
            self.investigation_datasets_pom.select_diagnostic_procedure_type()
            self.default_investigation_dataset_forms_continuation()
            self.investigation_datasets_pom.click_show_failure_information()
            DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
                self.failure_reasons_string,
                "divFailureSection",
                FailureReasonsOptions.NO_FAILURE_REASONS,
            )
            self.save_investigation_dataset()
        else:
            logging.error("Incorrect result entered")

    def go_to_investigation_datasets_page(self, nhs_no) -> None:
        """This method navigates to the investigation datasets page for a subject.
        Args:
            nhs_no (str): The NHS number of the subject.
        """
        verify_subject_event_status_by_nhs_no(
            self.page, nhs_no, "A323 - Post-investigation Appointment NOT Required"
        )

        SubjectScreeningSummaryPage(self.page).click_datasets_link()
        SubjectDatasetsPage(self.page).click_investigation_show_datasets()

    def default_investigation_dataset_forms(self) -> None:
        """This method fills out the first part of the default investigation dataset form."""
        # Investigation Dataset
        self.investigation_datasets_pom.select_site_lookup_option(
            SiteLookupOptions.RL401
        )
        self.investigation_datasets_pom.select_practitioner_option(
            PractitionerOptions.AMID_SNORING
        )
        self.investigation_datasets_pom.select_testing_clinician_option(
            TestingClinicianOptions.BORROWING_PROPERTY
        )
        self.investigation_datasets_pom.select_aspirant_endoscopist_option(
            AspirantEndoscopistOptions.ITALICISE_AMNESTY
        )
        # Drug Information
        self.investigation_datasets_pom.click_show_drug_information()
        self.investigation_datasets_pom.select_drug_type_option1(
            DrugTypeOptions.BISACODYL
        )
        self.investigation_datasets_pom.fill_drug_type_dose1("10")
        # Endoscopy Information
        self.investigation_datasets_pom.click_show_endoscopy_information()
        self.investigation_datasets_pom.check_endoscope_inserted_yes()

    def default_investigation_dataset_forms_continuation(self) -> None:
        """This method fills out the second part of the default investigation dataset form."""
        DatasetFieldUtil(self.page).populate_select_locator_for_field(
            "Bowel preparation quality", BowelPreparationQualityOptions.GOOD
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field(
            "Comfort during examination", ComfortOptions.NO_DISCOMFORT
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field(
            "Comfort during recovery", ComfortOptions.NO_DISCOMFORT
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field(
            "Endoscopist defined extent", EndoscopyLocationOptions.ILEUM
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field(
            "Scope imager used", YesNoOptions.YES
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field(
            "Retroverted view", YesNoOptions.NO
        )
        DatasetFieldUtil(self.page).populate_input_locator_for_field(
            "Start of intubation time", "09:00"
        )
        DatasetFieldUtil(self.page).populate_input_locator_for_field(
            "Start of extubation time", "09:15"
        )
        DatasetFieldUtil(self.page).populate_input_locator_for_field(
            "End time of procedure", "09:30"
        )
        DatasetFieldUtil(self.page).populate_input_locator_for_field("Scope ID", "A1")
        DatasetFieldUtil(self.page).populate_select_locator_for_field(
            "Insufflation", InsufflationOptions.AIR
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field(
            "Outcome at time of procedure",
            OutcomeAtTimeOfProcedureOptions.LEAVE_DEPARTMENT,
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field(
            "Late outcome", LateOutcomeOptions.NO_COMPLICATIONS
        )
        self.investigation_datasets_pom.click_show_completion_proof_information()
        # Completion Proof Information
        DatasetFieldUtil(self.page).populate_select_locator_for_field(
            "Proof Parameters", CompletionProofOptions.PHOTO_ILEO
        )

    def investigation_datasets_failure_reason(self) -> None:
        """This method fills out the failure reason section of the investigation dataset form."""
        # Failure Information
        self.investigation_datasets_pom.click_show_failure_information()
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            self.failure_reasons_string,
            "divFailureSection",
            FailureReasonsOptions.BLEEDING_INCIDENT,
        )

    def polyps_for_high_risk_result(self) -> None:
        """This method fills out the polyp information section of the investigation dataset form to trigger a high risk result."""
        # Polyp Information
        self.investigation_datasets_pom.click_add_polyp_button()
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            "Location", "divPolypNumber1Section", EndoscopyLocationOptions.ILEUM
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            "Classification", "divPolypNumber1Section", PolypClassificationOptions.IS
        )
        DatasetFieldUtil(self.page).populate_input_locator_for_field_inside_div(
            self.estimate_whole_polyp_size_string, "divPolypNumber1Section", "15"
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            self.polyp_access_string,
            "divPolypNumber1Section",
            PolypAccessOptions.NOT_KNOWN,
        )
        self.polyp1_intervention()
        self.investigation_datasets_pom.click_add_polyp_button()
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            "Location", "divPolypNumber2Section", EndoscopyLocationOptions.CAECUM
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            "Classification", "divPolypNumber2Section", PolypClassificationOptions.IS
        )
        DatasetFieldUtil(self.page).populate_input_locator_for_field_inside_div(
            self.estimate_whole_polyp_size_string, "divPolypNumber2Section", "15"
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            self.polyp_access_string,
            "divPolypNumber2Section",
            PolypAccessOptions.NOT_KNOWN,
        )
        self.investigation_datasets_pom.click_polyp2_add_intervention_button()
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            "Modality",
            "divPolypTherapy2_1Section",
            PolypInterventionModalityOptions.EMR,
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            "Device",
            "divPolypTherapy2_1Section",
            PolypInterventionDeviceOptions.HOT_SNARE,
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            "Excised", "divPolypResected2_1", YesNoOptions.YES
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            "Retrieved", "divPolypTherapy2_1Section", YesNoOptions.NO
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            self.excision_technique_string,
            "divPolypTherapy2_1Section",
            PolypInterventionExcisionTechniqueOptions.EN_BLOC,
        )

    def polyps_for_lnpcp_result(self) -> None:
        """This method fills out the polyp information section of the investigation dataset form to trigger a LNPCP result."""
        # Polyp Information
        self.investigation_datasets_pom.click_add_polyp_button()
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            "Location", "divPolypNumber1Section", EndoscopyLocationOptions.ILEUM
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            "Classification", "divPolypNumber1Section", PolypClassificationOptions.IS
        )
        DatasetFieldUtil(self.page).populate_input_locator_for_field_inside_div(
            self.estimate_whole_polyp_size_string, "divPolypNumber1Section", "30"
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            self.polyp_access_string,
            "divPolypNumber1Section",
            PolypAccessOptions.NOT_KNOWN,
        )
        self.polyp1_intervention()

    def polyp1_intervention(self) -> None:
        """This method fills out the intervention section of the investigation dataset form for polyp 1."""
        self.investigation_datasets_pom.click_polyp1_add_intervention_button()
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            "Modality",
            "divPolypTherapy1_1Section",
            PolypInterventionModalityOptions.POLYPECTOMY,
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            "Device",
            "divPolypTherapy1_1Section",
            PolypInterventionDeviceOptions.HOT_SNARE,
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            "Excised", "divPolypResected1_1", YesNoOptions.YES
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            "Retrieved", "divPolypTherapy1_1Section", YesNoOptions.NO
        )
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            self.excision_technique_string,
            "divPolypTherapy1_1Section",
            PolypInterventionExcisionTechniqueOptions.EN_BLOC,
        )

    def save_investigation_dataset(self) -> None:
        """This method saves the investigation dataset form."""
        self.investigation_datasets_pom.check_dataset_complete_checkbox()
        self.investigation_datasets_pom.click_save_dataset_button()

    def complete_dataset_with_args(
        self,
        general_information: dict,
        drug_information: dict,
        endoscopy_information: dict,
        failure_information: dict,
        completion_information: Optional[dict] = None,
        polyp_information: Optional[list] = None,
        polyp_intervention: Optional[list] = None,
        polyp_histology: Optional[list] = None,
    ) -> None:
        """This method completes the investigation dataset with the provided dictionaries.
        Args:
            general_information (dict): A dictionary containing the general information to be filled in the form.
            drug_information (dict): A dictionary containing the drug information to be filled in the form.
            endoscopy_information (dict): A dictionary containing the endoscopy information to be filled in the form.
            failure_information (dict): A dictionary containing the failure information to be filled in the form.
            completion_information (Optional[dict]): An optional  dictionary containing the completion information to be filled in the form.
            polyp_information (Optional[list]): An optional list containing the polyp information to be filled in the form.
            polyp_intervention (Optional[list]): An optional list containing the polyp intervention to be filled in the form.
            polyp_histology (Optional[list]): An optional list containing the polyp histology to be filled in the form.
        """
        logging.info("Completing investigation dataset with the provided dictionaries")
        # Investigation Dataset
        self.investigation_datasets_pom.select_site_lookup_option_index(
            general_information["site"]
        )
        self.investigation_datasets_pom.select_practitioner_option_index(
            general_information["practitioner"]
        )
        self.investigation_datasets_pom.select_testing_clinician_option_index(
            general_information["testing clinician"]
        )

        if general_information["aspirant endoscopist"] is None:
            InvestigationDatasetsPage(
                self.page
            ).check_aspirant_endoscopist_not_present()
        else:
            InvestigationDatasetsPage(
                self.page
            ).select_aspirant_endoscopist_option_index(
                general_information["aspirant endoscopist"]
            )

        # Drug Information
        InvestigationDatasetsPage(self.page).click_show_drug_information()
        self.fill_out_drug_information(drug_information)

        logging.info("Filling out endoscopy information")
        self.fill_endoscopy_information(endoscopy_information)

        # Completion Proof Information
        if completion_information is not None:
            logging.info("Filling out completion proof information")
            InvestigationDatasetsPage(
                self.page
            ).click_show_completion_proof_information()
            DatasetFieldUtil(self.page).populate_select_locator_for_field(
                "Proof Parameters", completion_information["completion proof"]
            )

        # Failure Information
        logging.info("Filling out failure information")
        self.investigation_datasets_pom.click_show_failure_information()
        DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
            self.failure_reasons_string,
            "divFailureSection",
            failure_information["failure reasons"],
        )

        self.process_polyps(polyp_information, polyp_intervention, polyp_histology)

        logging.info("Saving the investigation dataset")
        self.investigation_datasets_pom.check_dataset_complete_checkbox()
        self.investigation_datasets_pom.click_save_dataset_button()

    def fill_out_drug_information(self, drug_information: dict) -> None:
        """
        This method completes the drug information section of the investigation dataset.
        Args:
            drug_information (dict): A dictionary containing the drug types and dosages.
        """
        logging.info("Filling out drug information")
        for key, value in drug_information.items():
            if key.startswith("drug_type"):
                index = key[len("drug_type") :]
                logging.info(f"Adding drug type {index}")
                select_locator = f"#UI_BOWEL_PREP_DRUG{index}"
                self.page.select_option(select_locator, value)
            elif key.startswith("drug_dose"):
                index = key[len("drug_dose") :]
                logging.info(f"Adding drug dose {index}")
                input_locator = f"#UI_BOWEL_PREP_DRUG_DOSE{index}"
                self.page.fill(input_locator, value)

    def process_polyps(
        self,
        polyp_information: Optional[list] = None,
        polyp_intervention: Optional[list] = None,
        polyp_histology: Optional[list] = None,
    ) -> None:
        """
        This method processes any polyps to be added to the dataset by calling the relevant methods.
        Args:
            polyp_information (Optional[list]): An optional list containing the polyp information to be filled in the form.
            polyp_intervention (Optional[list]): An optional list containing the polyp intervention to be filled in the form.
            polyp_histology (Optional[list]): An optional list containing the polyp histology to be filled in the form.
        """
        # Polyp Information
        if polyp_information is not None:
            for polyp_number, polyp_info in enumerate(polyp_information, start=1):
                logging.info(f"Filling out polyp {polyp_number} information")
                self.fill_polyp_x_information(polyp_info, polyp_number)

        # Polyp Intervention
        if polyp_intervention is not None:
            for polyp_number, intervention_entry in enumerate(
                polyp_intervention, start=1
            ):
                if isinstance(intervention_entry, list):
                    logging.info(
                        f"Filling multiple interventions for polyp {polyp_number}"
                    )
                    self.fill_polyp_x_multiple_interventions(
                        intervention_entry, polyp_number
                    )
                else:
                    logging.info(
                        f"Filling single intervention for polyp {polyp_number}"
                    )
                    self.fill_polyp_x_intervention(intervention_entry, polyp_number)

        # Polyp Histology
        if polyp_histology is not None:
            for polyp_number, polyp_histology_info in enumerate(
                polyp_histology, start=1
            ):
                logging.info(f"Filling out polyp {polyp_number} histology")
                self.fill_polyp_x_histology(polyp_histology_info, polyp_number)

    def fill_endoscopy_information(self, endoscopy_information: dict) -> None:
        """
        Fills out the endoscopy information section of the investigation dataset.
        Args:
            endoscopy_information (dict): A dictionary containing the endoscopy information to be filled in the form.
        """
        # Endoscopy Information
        self.investigation_datasets_pom.click_show_endoscopy_information()

        # Use for loop and match-case for endoscopy_information fields
        for key, value in endoscopy_information.items():
            match key:
                case "endoscope inserted":
                    if value == "yes":
                        InvestigationDatasetsPage(
                            self.page
                        ).check_endoscope_inserted_yes()
                    elif value == "no":
                        InvestigationDatasetsPage(
                            self.page
                        ).check_endoscope_inserted_no()
                case "procedure type":
                    if value == "therapeutic":
                        InvestigationDatasetsPage(
                            self.page
                        ).select_therapeutic_procedure_type()
                    elif value == "diagnostic":
                        InvestigationDatasetsPage(
                            self.page
                        ).select_diagnostic_procedure_type()
                case "bowel preparation quality":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        "Bowel preparation quality", value
                    )
                case "comfort during examination":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        "Comfort during examination", value
                    )
                case "comfort during recovery":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        "Comfort during recovery", value
                    )
                case "endoscopist defined extent":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        "Endoscopist defined extent", value
                    )
                case "scope imager used":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        "Scope imager used", value
                    )
                case "retroverted view":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        "Retroverted view", value
                    )
                case "start of intubation time":
                    DatasetFieldUtil(self.page).populate_input_locator_for_field(
                        "Start of intubation time", value
                    )
                case "start of extubation time":
                    DatasetFieldUtil(self.page).populate_input_locator_for_field(
                        "Start of extubation time", value
                    )
                case "end time of procedure":
                    DatasetFieldUtil(self.page).populate_input_locator_for_field(
                        "End time of procedure", value
                    )
                case "scope id":
                    DatasetFieldUtil(self.page).populate_input_locator_for_field(
                        "Scope ID", value
                    )
                case "insufflation":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        "Insufflation", value
                    )
                case "outcome at time of procedure":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        "Outcome at time of procedure", value
                    )
                case "late outcome":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        "Late outcome", value
                    )

    def fill_polyp_x_information(
        self, polyp_information: dict, polyp_number: int
    ) -> None:
        """
        Fills out the polyp information section of the investigation dataset for any polyp.
        Args:
            polyp_1_information (dict): A dictionary containing the polyp 1 information to be filled in the form.
        """
        # Polyp Information
        self.investigation_datasets_pom.click_add_polyp_button()
        for key, value in polyp_information.items():
            match key:
                case "location":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Location", f"divPolypNumber{polyp_number}Section", value
                    )
                case "classification":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Classification", f"divPolypNumber{polyp_number}Section", value
                    )
                case "estimate of whole polyp size":
                    DatasetFieldUtil(
                        self.page
                    ).populate_input_locator_for_field_inside_div(
                        self.estimate_whole_polyp_size_string,
                        f"divPolypNumber{polyp_number}Section",
                        value,
                    )
                case "polyp access":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        self.polyp_access_string,
                        f"divPolypNumber{polyp_number}Section",
                        value,
                    )
                case "secondary piece":
                    self.page.once("dialog", lambda dialog: dialog.accept())
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Secondary Piece",
                        f"divPolypSecondaryPiece{polyp_number}",
                        value,
                    )
                case "left in situ":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Left in Situ",
                        f"divLeftInSitu{polyp_number}",
                        value,
                    )
                case "reason left in situ":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Reason Left in Situ",
                        f"divLeftInSituReason{polyp_number}",
                        value,
                    )

    def fill_polyp_x_intervention(
        self, polyp_intervention: dict, polyp_number: int
    ) -> None:
        """
        Fills out the polyp 1 intervention section of the investigation dataset.
        Args:
            polyp_1_intervention (dict): A dictionary containing the polyp 1 intervention to be filled in the form.
        """
        self.investigation_datasets_pom.click_polyp_add_intervention_button(
            polyp_number
        )
        for key, value in polyp_intervention.items():
            match key:
                case "modality":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Modality",
                        f"divPolypTherapy{polyp_number}_1Section",
                        value,
                    )
                case "device":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Device",
                        f"divPolypTherapy{polyp_number}_1Section",
                        value,
                    )
                case "excised":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Excised", f"divPolypResected{polyp_number}_1", value
                    )
                case "retrieved":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Retrieved",
                        f"divPolypTherapy{polyp_number}_1Section",
                        value,
                    )
                case "excision technique":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        self.excision_technique_string,
                        f"divPolypTherapy{polyp_number}_1Section",
                        value,
                    )
                case "polyp appears fully resected endoscopically":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Polyp appears fully resected endoscopically",
                        f"divPolypAppearsFullyResected{polyp_number}_1",
                        value,
                    )
                case "intervention success":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Intervention Success",
                        f"divResectionSuccess{polyp_number}_1",
                        value,
                    )

    def fill_polyp_x_multiple_interventions(
        self, interventions: list[dict], polyp_number: int
    ) -> None:
        """
        Fills out multiple interventions for the given polyp.
        Args:
            interventions (list): A list of intervention dictionaries.
            polyp_number (int): The 1-based index of the polyp.
        """
        for i, intervention in enumerate(interventions, start=1):
            self.investigation_datasets_pom.click_polyp_add_intervention_button(
                polyp_number
            )
            for key, value in intervention.items():
                match key:
                    case "modality":
                        DatasetFieldUtil(
                            self.page
                        ).populate_select_locator_for_field_inside_div(
                            "Modality",
                            f"divPolypTherapy{polyp_number}_{i}Section",
                            value,
                        )
                    case "device":
                        DatasetFieldUtil(
                            self.page
                        ).populate_select_locator_for_field_inside_div(
                            "Device", f"divPolypTherapy{polyp_number}_{i}Section", value
                        )
                    case "excised":
                        DatasetFieldUtil(
                            self.page
                        ).populate_select_locator_for_field_inside_div(
                            "Excised", f"divPolypResected{polyp_number}_{i}", value
                        )
                    case "retrieved":
                        DatasetFieldUtil(
                            self.page
                        ).populate_select_locator_for_field_inside_div(
                            "Retrieved",
                            f"divPolypTherapy{polyp_number}_{i}Section",
                            value,
                        )
                    case "excision technique":
                        DatasetFieldUtil(
                            self.page
                        ).populate_select_locator_for_field_inside_div(
                            self.excision_technique_string,
                            f"divPolypTherapy{polyp_number}_{i}Section",
                            value,
                        )
                    case "polyp appears fully resected endoscopically":
                        DatasetFieldUtil(
                            self.page
                        ).populate_select_locator_for_field_inside_div(
                            "Polyp appears fully resected endoscopically",
                            f"divPolypAppearsFullyResected{polyp_number}_{i}",
                            value,
                        )
                    case "intervention success":
                        DatasetFieldUtil(
                            self.page
                        ).populate_select_locator_for_field_inside_div(
                            "Intervention Success",
                            f"divResectionSuccess{polyp_number}_{i}",
                            value,
                        )

    def fill_polyp_x_histology(self, polyp_histology: dict, polyp_number: int) -> None:
        """
        Fills out the polyp histology section of the investigation dataset.
        Args:
            polyp_histology (dict): A dictionary containing the polyp 1 histology to be filled in the form.
        """
        self.click_show_histology_details_if_present(polyp_number)
        for key, value in polyp_histology.items():
            match key:
                case "pathology lost":
                    self.investigation_datasets_pom.assert_dialog_text(
                        "Please consider raising an AVI", True
                    )
                    self.investigation_datasets_pom.populate_select_by_id(
                        "POLYP_PATHOLOGY_LOST", polyp_number, value
                    )
                case "reason pathology lost":
                    self.investigation_datasets_pom.populate_select_by_id(
                        "POLYP_PATHOLOGY_LOST_REASON", polyp_number, value
                    )
                case "date of receipt":
                    DatasetFieldUtil(
                        self.page
                    ).populate_input_locator_for_field_inside_div(
                        "Date of Receipt",
                        f"divPolypHistology{polyp_number}_1Details",
                        value.strftime("%d/%m/%Y"),
                    )
                case "date of reporting":
                    DatasetFieldUtil(
                        self.page
                    ).populate_input_locator_for_field_inside_div(
                        "Date of Reporting",
                        f"divPolypHistology{polyp_number}_1Details",
                        value.strftime("%d/%m/%Y"),
                    )
                case "pathology provider":
                    DatasetFieldUtil(self.page).click_lookup_link_inside_div(
                        "Pathology Provider",
                        f"divPolypHistology{polyp_number}_1Details",
                    )
                    self.investigation_datasets_pom.select_lookup_option_index(value)
                case "pathologist":
                    DatasetFieldUtil(self.page).click_lookup_link_inside_div(
                        "Pathologist",
                        f"divPolypHistology{polyp_number}_1Details",
                    )
                    self.investigation_datasets_pom.select_lookup_option_index(value)
                case "polyp type":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Polyp Type",
                        f"divPolypHistology{polyp_number}_1Details",
                        value,
                    )
                case "serrated lesion sub type":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Polyp Sub Type",
                        f"divSubTypeSerratedLesion{polyp_number}_1",
                        value,
                    )
                case "adenoma sub type":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Polyp Sub Type",
                        f"divSubTypeAdenoma{polyp_number}_1",
                        value,
                    )
                case "polyp excision complete":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Polyp Excision Complete",
                        f"divExcisionComplete{polyp_number}_1",
                        value,
                    )
                case "polyp size":
                    DatasetFieldUtil(
                        self.page
                    ).populate_input_locator_for_field_inside_div(
                        "Polyp Size",
                        f"divPolypHistology{polyp_number}_1Details",
                        value,
                    )
                case "polyp dysplasia":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Polyp Dysplasia",
                        f"divTumourFindings{polyp_number}_1",
                        value,
                    )
                case "polyp carcinoma":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Polyp Carcinoma",
                        f"divTumourFindings{polyp_number}_1",
                        value,
                    )

    def click_show_histology_details_if_present(self, polyp_number: int) -> None:
        """
        This method checks if the relevant "Show details" link for a polyp histology is present.
        If it is then it clicks it.
        Args:
            polyp_number (int): The polyp number for the histology you want to check
        """
        dynamic_id = f"anchorPolypHistology{polyp_number}_1"
        locator = self.page.locator(f"#{dynamic_id}")

        if locator.count() > 0:
            text = locator.inner_text().strip()
            if text == "Show details":
                locator.click()


class AfterInvestigationDatasetComplete:
    """
    This class is used to progress the episode based on the result of the investigation dataset.
    It contains methods to handle the different outcomes of the investigation dataset.
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        self.a318_latest_event_status_string = (
            "A318 - Post-investigation Appointment NOT Required - Result Letter Created"
        )

    def progress_episode_based_on_result(self, result: str, younger: bool) -> None:
        """This method progresses the episode based on the result of the investigation dataset.
        Args:
            result (str): The result of the investigation dataset.
                Should be one of InvestigationDatasetResults (HIGH_RISK, LNPCP, NORMAL).
            younger (bool): True if the subject is younger than 70, False otherwise.
        """
        if result == InvestigationDatasetResults.HIGH_RISK:
            self.after_high_risk_result()
            if younger:
                self.record_diagnosis_date()
            else:
                self.handover_subject_to_symptomatic_care()
        elif result == InvestigationDatasetResults.LNPCP:
            self.after_lnpcp_result()
            if younger:
                self.record_diagnosis_date()
            else:
                self.handover_subject_to_symptomatic_care()
        elif result == InvestigationDatasetResults.NORMAL:
            self.after_normal_result()
            self.record_diagnosis_date()
        else:
            logging.error("Incorrect result entered")

    def after_high_risk_result(self) -> None:
        """This method advances an episode that has a high-risk result."""
        InvestigationDatasetsPage(self.page).expect_text_to_be_visible(
            "High-risk findings"
        )
        BasePage(self.page).click_back_button()

        # The following code is on the subject datasets page
        SubjectDatasetsPage(self.page).check_investigation_dataset_complete()
        BasePage(self.page).click_back_button()

        SubjectScreeningSummaryPage(
            self.page
        ).click_advance_fobt_screening_episode_button()
        # The following code is on the advance fobt screening episode page
        AdvanceFOBTScreeningEpisodePage(
            self.page
        ).click_enter_diagnostic_test_outcome_button()

        # The following code is on the diagnostic test outcome page
        DiagnosticTestOutcomePage(self.page).verify_diagnostic_test_outcome(
            "High-risk findings"
        )
        DiagnosticTestOutcomePage(self.page).select_test_outcome_option(
            OutcomeOfDiagnosticTest.REFER_SURVEILLANCE
        )
        DiagnosticTestOutcomePage(self.page).click_save_button()

    def after_lnpcp_result(self) -> None:
        """This method advances an episode that has a LNPCP result."""
        InvestigationDatasetsPage(self.page).expect_text_to_be_visible("LNPCP")
        BasePage(self.page).click_back_button()

        # The following code is on the subject datasets page
        SubjectDatasetsPage(self.page).check_investigation_dataset_complete()
        BasePage(self.page).click_back_button()

        SubjectScreeningSummaryPage(
            self.page
        ).click_advance_fobt_screening_episode_button()

        # The following code is on the advance fobt screening episode page
        AdvanceFOBTScreeningEpisodePage(
            self.page
        ).click_enter_diagnostic_test_outcome_button()

        # The following code is on the diagnostic test outcome page
        DiagnosticTestOutcomePage(self.page).verify_diagnostic_test_outcome("LNPCP")
        DiagnosticTestOutcomePage(self.page).select_test_outcome_option(
            OutcomeOfDiagnosticTest.REFER_SURVEILLANCE
        )
        DiagnosticTestOutcomePage(self.page).click_save_button()

    def after_normal_result(self) -> None:
        """This method advances an episode that has a normal result."""
        InvestigationDatasetsPage(self.page).expect_text_to_be_visible(
            "Normal (No Abnormalities"
        )
        BasePage(self.page).click_back_button()

        # The following code is on the subject datasets page
        SubjectDatasetsPage(self.page).check_investigation_dataset_complete()
        BasePage(self.page).click_back_button()

        SubjectScreeningSummaryPage(
            self.page
        ).click_advance_fobt_screening_episode_button()

        # The following code is on the advance fobt screening episode page
        AdvanceFOBTScreeningEpisodePage(
            self.page
        ).click_enter_diagnostic_test_outcome_button()

        # The following code is on the diagnostic test outcome page
        DiagnosticTestOutcomePage(self.page).verify_diagnostic_test_outcome(
            "Normal (No Abnormalities"
        )
        DiagnosticTestOutcomePage(self.page).select_test_outcome_option(
            OutcomeOfDiagnosticTest.INVESTIGATION_COMPLETE
        )
        DiagnosticTestOutcomePage(self.page).click_save_button()

        SubjectScreeningSummaryPage(self.page).verify_latest_event_status_value(
            self.a318_latest_event_status_string
        )

    def handover_subject_to_symptomatic_care(self) -> None:
        """This method hands over a subject to symptomatic care."""
        SubjectScreeningSummaryPage(self.page).verify_latest_event_status_value(
            "A394 - Handover into Symptomatic Care for Surveillance - Patient Age"
        )
        SubjectScreeningSummaryPage(
            self.page
        ).click_advance_fobt_screening_episode_button()

        # The following code is on the advance fobt screening episode page
        AdvanceFOBTScreeningEpisodePage(
            self.page
        ).click_handover_into_symptomatic_care_button()

        # The following code is on the handover into symptomatic care page
        HandoverIntoSymptomaticCarePage(self.page).select_referral_dropdown_option(
            "20445"
        )
        HandoverIntoSymptomaticCarePage(self.page).click_calendar_button()
        CalendarPicker(self.page).v1_calender_picker(datetime.today())
        HandoverIntoSymptomaticCarePage(self.page).select_consultant("201")
        HandoverIntoSymptomaticCarePage(self.page).fill_notes("Test Automation")
        HandoverIntoSymptomaticCarePage(self.page).click_save_button()

        SubjectScreeningSummaryPage(self.page).wait_for_page_title()
        SubjectScreeningSummaryPage(self.page).verify_latest_event_status_value(
            "A385 - Handover into Symptomatic Care"
        )

    def record_diagnosis_date(self) -> None:
        """This method records the diagnosis date for a subject."""
        SubjectScreeningSummaryPage(self.page).verify_latest_event_status_value(
            self.a318_latest_event_status_string
        )
        SubjectScreeningSummaryPage(
            self.page
        ).click_advance_fobt_screening_episode_button()

        # The following code is on the advance fobt screening episode page
        AdvanceFOBTScreeningEpisodePage(self.page).click_record_diagnosis_date_button()

        # The following code is on the record diagnosis date page
        RecordDiagnosisDatePage(self.page).enter_date_in_diagnosis_date_field(
            datetime.today()
        )
        RecordDiagnosisDatePage(self.page).click_save_button()

        SubjectScreeningSummaryPage(self.page).verify_latest_event_status_value(
            self.a318_latest_event_status_string
        )
