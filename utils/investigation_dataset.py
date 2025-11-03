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
    to_enum_name_or_value,
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
        self.outcome_at_time_of_procedure_string = "Outcome at time of procedure"

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
            self.outcome_at_time_of_procedure_string,
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
        general_information: Optional[dict] = None,
        drug_information: Optional[dict] = None,
        endoscopy_information: Optional[dict] = None,
        failure_information: Optional[dict] = None,
        completion_information: Optional[dict] = None,
        polyp_information: Optional[list] = None,
        polyp_intervention: Optional[list] = None,
        polyp_histology: Optional[list] = None,
        contrast_tagging_and_drug: Optional[dict] = None,
        tagging_agent_given_drug_information: Optional[dict] = None,
        radiology_information: Optional[dict] = None,
        suspected_findings: Optional[dict] = None,
    ) -> None:
        """
        Completes the investigation dataset using the provided dictionaries for each section.

        Args:
            general_information (Optional[dict]): General dataset fields (site, practitioner, clinician, etc.).
            drug_information (Optional[dict]): Drug types and dosages for the main drug section.
            endoscopy_information (Optional[dict]): Endoscopy procedure details and related fields.
            failure_information (Optional[dict]): Failure reasons and related information.
            completion_information (Optional[dict]): Completion proof parameters.
            polyp_information (Optional[list[dict]]): List of polyp information dictionaries.
            polyp_intervention (Optional[list[dict] or list[list[dict]]]): List of interventions per polyp, or lists of interventions for each polyp.
            polyp_histology (Optional[list[dict]]): List of polyp histology dictionaries.
            contrast_tagging_and_drug (Optional[dict]): Contrast, tagging agent, and drug information.
            tagging_agent_given_drug_information (Optional[dict]): Tagging agent drug types and doses.
            radiology_information (Optional[dict]): Radiology section fields.
            suspected_findings (Optional[dict]): Suspected findings section fields
        """
        logging.info("Completing investigation dataset with the provided dictionaries")
        # Investigation Dataset
        if general_information is not None:
            logging.info("Filling out general information")
            self.fill_out_general_information(general_information)

        # Drug Information
        if drug_information is not None:
            InvestigationDatasetsPage(self.page).click_show_drug_information()
            self.fill_out_drug_information(drug_information)

        if endoscopy_information:
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
        if failure_information is not None:
            logging.info("Filling out failure information")
            self.investigation_datasets_pom.click_show_failure_information()
            DatasetFieldUtil(self.page).populate_select_locator_for_field_inside_div(
                self.failure_reasons_string,
                "divFailureSection",
                failure_information["failure reasons"],
            )

        self.process_polyps(polyp_information, polyp_intervention, polyp_histology)

        # Contrast, Tagging & Drug Information
        if contrast_tagging_and_drug is not None:
            logging.info("Filling out contrast, tagging & drug information")
            self.fill_out_contrast_tagging_and_drug_information(
                contrast_tagging_and_drug
            )

        if tagging_agent_given_drug_information is not None:
            logging.info("Filling out tagging agent given drug information")
            self.fill_out_tagging_agent_given_drug_information(
                tagging_agent_given_drug_information
            )

            # Radiology Information
        if radiology_information is not None:
            logging.info("Filling out radiology information")
            self.fill_out_radiology_information(radiology_information)

        # Suspected Findings
        if suspected_findings is not None:
            logging.info("Filling out suspected findings")
            self.fill_out_suspected_findings(suspected_findings)

        # Save the dataset
        logging.info("Saving the investigation dataset")
        self.investigation_datasets_pom.check_dataset_complete_checkbox()
        self.investigation_datasets_pom.click_save_dataset_button()

    def fill_out_suspected_findings(self, suspected_findings: dict) -> None:
        """
        Populates the Suspected Findings section of the Investigation Dataset form.
        """
        logging.info("Starting fill_out_suspected_findings")
        try:
            logging.info("About to click suspected findings details")
            self.investigation_datasets_pom.click_show_suspected_findings_details()
            logging.info("Clicked suspected findings details successfully")
        except Exception as e:
            logging.error(f"Error clicking on Show Suspected Findings Details: {e}")
            raise
        for key, value in suspected_findings.items():
            match key:
                case "extracolonic summary code":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        "Extracolonic Summary Code", value
                    )

    def fill_out_general_information(self, general_information: dict) -> None:
        """
        Populates the General Information section of the Investigation Dataset form.

        This method fills in site, practitioner, clinician, and radiologist details,
        as well as referral fitness and aspirant endoscopist status. It gracefully handles
        optional fields and skips any that are not provided in the input dictionary.

        Args:
            general_information (dict): A dictionary containing general dataset fields.
                Expected keys include:
                    - "site" (int): Index for site lookup dropdown.
                    - "practitioner" (int): Index for practitioner dropdown.
                    - "testing clinician" (int): Index for testing clinician dropdown.
                    - "reporting radiologist" (Optional[int]): Index for radiologist dropdown.
                    - "fit for subsequent endoscopic referral" (Optional[str]): Enum value for referral fitness.
                    - "aspirant endoscopist" (Optional[int or None]): Index for aspirant dropdown, or None to mark absence.
        """
        self.investigation_datasets_pom.select_site_lookup_option_index(
            general_information["site"]
        )
        self.investigation_datasets_pom.select_practitioner_option_index(
            general_information["practitioner"]
        )
        testing_clinician = general_information["testing clinician"]
        if isinstance(testing_clinician, int):
            self.investigation_datasets_pom.select_testing_clinician_option_index(
                testing_clinician
            )
        elif isinstance(testing_clinician, str):
            self.investigation_datasets_pom.select_testing_clinician_from_name(
                testing_clinician
            )

        if general_information.get("reporting radiologist") is not None:
            InvestigationDatasetsPage(
                self.page
            ).select_reporting_radiologist_option_index(
                general_information["reporting radiologist"]
            )

        if (
            general_information.get("fit for subsequent endoscopic referral")
            is not None
        ):
            DatasetFieldUtil(self.page).populate_select_locator_for_field(
                "Fit for Subsequent Endoscopic Referral",
                general_information["fit for subsequent endoscopic referral"],
            )

        if "aspirant endoscopist" in general_information:
            aspirant = general_information["aspirant endoscopist"]
            if aspirant is None:
                InvestigationDatasetsPage(
                    self.page
                ).check_aspirant_endoscopist_not_present()
            else:
                InvestigationDatasetsPage(
                    self.page
                ).select_aspirant_endoscopist_option_index(aspirant)

    def fill_out_contrast_tagging_and_drug_information(
        self, contrast_tagging_and_drug: dict
    ) -> None:
        logging.info("🧪 Filling out Contrast, Tagging & Drug Information")
        self.investigation_datasets_pom.click_show_contrast_tagging_and_drug_information()

        # Use for loop and match-case for endoscopy_information fields
        for key, value in contrast_tagging_and_drug.items():
            match key:
                case "iv buscopan administered":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        "IV Buscopan Administered", value
                    )
                case "contraindicated":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "contraindicated", "UI_BUSCOPAN_CONTRAINDICATED_ROW", value
                    )
                case "iv contrast administered":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        "IV Contrast Administered", value
                    )
                case "reason":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Reason", "UI_CONTRAST_ADMINISTERED_REASON_ROW", value
                    )
                case "tagging agent given":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        "Tagging Agent Given", value
                    )
                case "additional bowel preparation administered":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        "Additional Bowel Preparation Administered", value
                    )
                case k if k.startswith(("drug_type", "drug_dose")):
                    # Extract all drug-related keys/values from the main dict
                    drug_info = {
                        dk: dv
                        for dk, dv in contrast_tagging_and_drug.items()
                        if dk.startswith(("drug_type", "drug_dose"))
                    }
                    # Call the existing drug filling method once
                    self.fill_out_drug_information(drug_info)

    def fill_out_drug_information(self, drug_information: dict) -> None:
        """
        This method completes the drug information section of the investigation dataset.
        Args:
            drug_information (dict): A dictionary containing the drug types and dosages.
        """
        logging.info("Filling out drug information")

        # Define mapping for each drug type/dose prefix and their selectors
        drug_map = {
            "drug_type": ("#UI_BOWEL_PREP_DRUG{}", True),
            "drug_dose": ("#UI_BOWEL_PREP_DRUG_DOSE{}", False),
            "antibiotic_drug_type": ("#UI_ANTIBIOTIC{}", True),
            "antibiotic_drug_dose": ("#UI_ANTIBIOTIC_DOSE{}", False),
            "other_drug_type": ("#UI_DRUG{}", True),
            "other_drug_dose": ("#UI_DOSE{}", False),
        }

        for key, value in drug_information.items():
            for prefix, (selector_template, is_select) in drug_map.items():
                if key.startswith(prefix):
                    index = key[len(prefix) :]
                    if is_select:
                        logging.info(
                            f"Adding {prefix.replace('_', ' ')} {index}: {to_enum_name_or_value(value)}"
                        )
                        self.page.select_option(selector_template.format(index), value)
                    else:
                        logging.info(
                            f"Adding {prefix.replace('_', ' ')} {index}: {value}"
                        )
                        self.page.fill(selector_template.format(index), value)
                    break

    def fill_out_tagging_agent_given_drug_information(
        self, drug_information: dict
    ) -> None:
        """
        This method completes the tagging agent given drug information section of the investigation dataset.
        Args:
            drug_information (dict): A dictionary containing the drug types, dosages, and tagging agent status.
                Expected keys:
                    - "tagging agent given": Enum value for tagging agent administered (e.g. YES/NO)
                    - "drug_type{n}": Enum value for drug type at index n
                    - "drug_dose{n}": String value for drug dose at index n
        """
        logging.info("Filling out tagging agent given drug information")

        # Handle tagging agent administered status
        if "tagging agent given" in drug_information:
            logging.info(
                f"Setting tagging agent given: {to_enum_name_or_value(drug_information['tagging agent given'])}"
            )
            self.page.select_option(
                "#UI_TAGGING_AGENT_GIVEN_DRUGS_ADMINISTERED",
                drug_information["tagging agent given"],
            )

        # Define mapping for drug type/dose fields
        drug_map = {
            "drug_type": ("#UI_TAGGING_AGENT_GIVEN_DRUG{}", True),
            "drug_dose": ("#UI_TAGGING_AGENT_GIVEN_DRUG_DOSE{}", False),
        }

        for key, value in drug_information.items():
            for prefix, (selector_template, is_select) in drug_map.items():
                if key.startswith(prefix):
                    index = key[len(prefix) :]
                    if is_select:
                        logging.info(
                            f"Adding {prefix.replace('_', ' ')} {index}: {to_enum_name_or_value(value)}"
                        )
                        self.page.select_option(selector_template.format(index), value)
                    else:
                        logging.info(
                            f"Adding {prefix.replace('_', ' ')} {index}: {value}"
                        )
                        self.page.fill(selector_template.format(index), value)
                    break

    def fill_out_radiology_information(self, radiology_data: dict) -> None:
        """
        This method completes the Radiology Information section of the investigation dataset.
        Args:
            radiology_data (dict): A dictionary containing radiology field keys and their values.
        """
        logging.info("Filling out Radiology Information")

        self.investigation_datasets_pom.click_show_radiology_information()
        self.investigation_datasets_pom.click_show_radiology_failure_information()

        # Use for loop and match-case for radiology data fields
        for key, value in radiology_data.items():
            match key:
                case "examination quality":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        "Examination Quality", value
                    )
                case "scan position":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        "Number of Scan Positions", value
                    )
                case "procedure outcome":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        self.outcome_at_time_of_procedure_string, value
                    )
                case "late outcome":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        "Late Outcome", value
                    )
                case "segmental inadequacy":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        "Segmental Inadequacy", value
                    )
                case "intracolonic summary code":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Intracolonic Summary Code",
                        "divIntracolonicSummaryCode",
                        value,
                    )

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
                case "detection assistant used":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        "Detection Assistant (AI) used?", value
                    )
                case "insufflation":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        "Insufflation", value
                    )
                case "outcome at time of procedure":
                    DatasetFieldUtil(self.page).populate_select_locator_for_field(
                        self.outcome_at_time_of_procedure_string, value
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
                case "optical diagnosis":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Optical Diagnosis",
                        f"divPolypOpticalDiagnosis{polyp_number}",
                        value,
                    )
                case "estimate of whole polyp size":
                    DatasetFieldUtil(
                        self.page
                    ).populate_input_locator_for_field_inside_div(
                        self.estimate_whole_polyp_size_string,
                        f"divPolypNumber{polyp_number}Section",
                        value,
                    )
                case "optical diagnosis confidence":
                    DatasetFieldUtil(
                        self.page
                    ).populate_select_locator_for_field_inside_div(
                        "Optical Diagnosis Confidence",
                        f"divPolypOpticalDiagnosisConfidence{polyp_number}",
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
                case "image id":
                    DatasetFieldUtil(
                        self.page
                    ).populate_input_locator_for_field_inside_div(
                        "Image ID", f"divPolypImageId{polyp_number}_1", value
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
                    case "image id":
                        DatasetFieldUtil(
                            self.page
                        ).populate_input_locator_for_field_inside_div(
                            "Image ID", f"divPolypImageId{polyp_number}_{i}", value
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

        if locator.is_visible():
            text = locator.inner_text().strip()
            if text == "Show details":
                locator.click()

    def clear_drug_type_and_doses_inputs(self, drug_type: str, count: int = 1) -> None:
        """
        Clears all drug type and dose inputs on the page for the specified drug type.
        Args:
            drug_type (str): The drug type label (should be one of the class string constants).
            count (int): The number of drug types and doses to clear. Default is 1.
        """
        if (
            drug_type
            == InvestigationDatasetsPage(
                self.page
            ).bowel_preparation_administered_string
        ):
            type_prefix = "drug_type"
            dose_prefix = "drug_dose"
        elif (
            drug_type
            == InvestigationDatasetsPage(self.page).antibiotics_administered_string
        ):
            type_prefix = "antibiotic_drug_type"
            dose_prefix = "antibiotic_drug_dose"
        elif (
            drug_type
            == InvestigationDatasetsPage(self.page).other_drugs_administered_string
        ):
            type_prefix = "other_drug_type"
            dose_prefix = "other_drug_dose"
        else:
            raise ValueError(f"Unknown drug_type: {drug_type}")

        drug_information = {}
        for i in range(1, count + 1):
            drug_information[f"{type_prefix}{i}"] = ""
            drug_information[f"{dose_prefix}{i}"] = ""

        self.fill_out_drug_information(drug_information)

        for i in range(1, count + 1):
            InvestigationDatasetsPage(self.page).assert_drug_type_text(drug_type, i, "")
            InvestigationDatasetsPage(self.page).assert_drug_dose_text(drug_type, i, "")

    def build_drug_information_dict(
        self, drug_info_list: list[tuple], drug_type: str, skip_none: bool = True
    ) -> dict:
        """
        Builds a drug information dictionary for use with InvestigationDatasetCompletion.fill_out_drug_information,
        automatically selecting the correct key prefixes based on the drug_type.

        Args:
            drug_info_list (list[tuple[object, str]]):
                A list of (drug_type_value, drug_dose_value) pairs.
            drug_type (str):
                The drug section label, e.g. "Bowel Preparation Administered",
                "Antibiotics Administered", or "Other Drugs Administered".
            skip_none (bool):
                If True, skips adding keys with None or empty string values.

        Returns:
            dict[str, object]:
                A dictionary with keys like "drug_type1", "drug_dose1", etc.,
                suitable for passing to fill_out_drug_information.
        """
        prefix_map = {
            "Bowel Preparation Administered": ("drug_type", "drug_dose"),
            "Antibiotics Administered": (
                "antibiotic_drug_type",
                "antibiotic_drug_dose",
            ),
            "Other Drugs Administered": ("other_drug_type", "other_drug_dose"),
        }
        if drug_type not in prefix_map:
            raise ValueError(f"Unknown drug_type: {drug_type}")

        type_prefix, dose_prefix = prefix_map[drug_type]
        drug_information = {}
        for idx, (drug_type_val, drug_dose_val) in enumerate(drug_info_list, start=1):
            if not skip_none or drug_type_val not in (None, ""):
                drug_information[f"{type_prefix}{idx}"] = drug_type_val
            if not skip_none or drug_dose_val not in (None, ""):
                drug_information[f"{dose_prefix}{idx}"] = drug_dose_val
        return drug_information


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
