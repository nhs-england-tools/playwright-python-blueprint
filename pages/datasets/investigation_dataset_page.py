from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from enum import StrEnum
from utils.oracle.oracle_specific_functions import (
    get_investigation_dataset_polyp_category,
    get_investigation_dataset_polyp_algorithm_size,
)
from typing import Optional
import logging


class InvestigationDatasetsPage(BasePage):
    """Investigation Datasets Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self.add_intervention_string = "Add Intervention"

        # Investigation datasets page locators
        self.site_lookup_link = self.page.locator("#UI_SITE_SELECT_LINK")
        self.practitioner_link = self.page.locator("#UI_SSP_PIO_SELECT_LINK")
        self.testing_clinician_link = self.page.locator(
            "#UI_CONSULTANT_PIO_SELECT_LINK"
        )
        self.aspirant_endoscopist_link = self.page.locator(
            "#UI_ASPIRANT_ENDOSCOPIST_PIO_SELECT_LINK"
        )
        self.aspirant_endoscopist_not_present = self.page.locator(
            "#UI_ASPIRANT_ENDOSCOPIST_NR"
        )
        self.show_drug_information_detail = self.page.locator("#anchorDrug")
        self.drug_type_option1 = self.page.locator("#UI_BOWEL_PREP_DRUG1")
        self.drug_type_dose1 = self.page.locator("#UI_BOWEL_PREP_DRUG_DOSE1")
        self.show_endoscopy_information_details = self.page.locator(
            "#anchorColonoscopy"
        )
        self.endoscope_inserted_yes = self.page.locator("#radScopeInsertedYes")
        self.endoscope_inserted_no = self.page.locator("#radScopeInsertedNo")
        self.therapeutic_procedure_type = self.page.get_by_role(
            "radio", name="Therapeutic"
        )
        self.diagnostic_procedure_type = self.page.get_by_role(
            "radio", name="Diagnostic"
        )
        self.show_completion_proof_information_details = self.page.locator(
            "#anchorCompletionProof"
        )
        self.show_failure_information_details = self.page.locator("#anchorFailure")
        self.add_polyp_button = self.page.get_by_role("button", name="Add Polyp")
        self.polyp1_add_intervention_button = self.page.get_by_role(
            "link", name=self.add_intervention_string
        )
        self.polyp2_add_intervention_button = self.page.locator(
            "#spanPolypInterventionLink2"
        ).get_by_role("link", name=self.add_intervention_string)
        self.dataset_complete_checkbox = self.page.locator("#radDatasetCompleteYes")
        self.dataset_incomplete_checkbox = self.page.locator("#radDatasetCompleteNo")
        self.save_dataset_button = self.page.locator(
            "#UI_DIV_BUTTON_SAVE1"
        ).get_by_role("button", name="Save Dataset")
        self.polyp1_pathology_provider = self.page.locator(
            "#UI_POLYP_PATHOLOGY_ORG_SITE_SELECT_LINK1_1"
        )
        self.polyp1_pathologist = self.page.locator(
            "#UI_POLYP_PATHOLOGIST_PIO_SELECT_LINK1_1"
        )
        self.polyp_information_show_details = self.page.locator("#anchorPolyp")
        self.polyp_1_intervention_show_information = self.page.locator(
            "#anchorPolypTherapy1_1"
        )
        self.polyp_1_histology_show_information = self.page.locator(
            "#anchorPolypHistology1_1"
        )
        self.edit_dataset_button = self.page.locator(
            "#UI_DIV_BUTTON_EDIT1"
        ).get_by_role("button", name="Edit Dataset")
        self.visible_ui_results_string = 'select[id^="UI_RESULTS_"]:visible'

    def select_site_lookup_option(self, option: str) -> None:
        """
        This method is designed to select a site from the site lookup options.
        It clicks on the site lookup link and selects the given option.

        Args:
            option (str): The option to select from the aspirant endoscopist options.
        """
        self.click(self.site_lookup_link)
        option_locator = self.page.locator(f'[value="{option}"]:visible')
        option_locator.wait_for(state="visible")
        self.click(option_locator)

    def select_site_lookup_option_index(self, option: int) -> None:
        """
        This method is designed to select a site from the site lookup options.
        It clicks on the site lookup link and selects the given option by index.

        Args:
            option (int): The index of the option to select from the site lookup options.
        """
        self.click(self.site_lookup_link)
        select_locator = self.page.locator(self.visible_ui_results_string)
        select_locator.first.wait_for(state="visible")
        # Find all option elements inside the select and click the one at the given index
        option_elements = select_locator.first.locator("option")
        option_elements.nth(option).wait_for(state="visible")
        self.click(option_elements.nth(option))

    def select_practitioner_option(self, option: str) -> None:
        """
        This method is designed to select a practitioner from the practitioner options.
        It clicks on the practitioner link and selects the given option.

        Args:
            option (str): The option to select from the aspirant endoscopist options.
        """
        self.click(self.practitioner_link)
        option_locator = self.page.locator(f'[value="{option}"]:visible')
        option_locator.wait_for(state="visible")
        self.click(option_locator)

    def select_practitioner_option_index(self, option: int) -> None:
        """
        This method is designed to select a practitioner from the practitioner options.
        It clicks on the practitioner link and selects the given option by index.

        Args:
            option (int): The index of the option to select from the practitioner options.
        """
        self.click(self.practitioner_link)
        select_locator = self.page.locator(self.visible_ui_results_string)
        select_locator.first.wait_for(state="visible")
        # Find all option elements inside the select and click the one at the given index
        option_elements = select_locator.first.locator("option")
        option_elements.nth(option).wait_for(state="visible")
        self.click(option_elements.nth(option))

    def select_testing_clinician_option(self, option: str) -> None:
        """
        This method is designed to select a testing clinician from the testing clinician options.
        It clicks on the testing clinician link and selects the given option.

        Args:
            option (str): The option to select from the aspirant endoscopist options.
        """
        self.click(self.testing_clinician_link)
        option_locator = self.page.locator(f'[value="{option}"]:visible')
        option_locator.wait_for(state="visible")
        self.click(option_locator)

    def select_testing_clinician_option_index(self, option: int) -> None:
        """
        This method is designed to select a testing clinician from the testing clinician options.
        It clicks on the testing clinician link and selects the given option by index.

        Args:
            option (int): The index of the option to select from the testing clinician options.
        """
        self.click(self.testing_clinician_link)
        select_locator = self.page.locator(self.visible_ui_results_string)
        select_locator.first.wait_for(state="visible")
        # Find all option elements inside the select and click the one at the given index
        option_elements = select_locator.first.locator("option")
        option_elements.nth(option).wait_for(state="visible")
        self.click(option_elements.nth(option))

    def select_aspirant_endoscopist_option(self, option: str) -> None:
        """
        This method is designed to select an aspirant endoscopist from the aspirant endoscopist options.
        It clicks on the aspirant endoscopist link and selects the given option.

        Args:
            option (str): The option to select from the aspirant endoscopist options.
        """
        self.click(self.aspirant_endoscopist_link)
        option_locator = self.page.locator(f'[value="{option}"]:visible')
        option_locator.wait_for(state="visible")
        self.click(option_locator)

    def select_aspirant_endoscopist_option_index(self, option: int) -> None:
        """
        This method is designed to select an aspirant endoscopist from the aspirant endoscopist options.
        It clicks on the aspirant endoscopist link and selects the given option by index.

        Args:
            option (int): The index of the option to select from the aspirant endoscopist options.
        """
        self.click(self.aspirant_endoscopist_link)
        select_locator = self.page.locator(self.visible_ui_results_string)
        select_locator.first.wait_for(state="visible")
        # Find all option elements inside the select and click the one at the given index
        option_elements = select_locator.first.locator("option")
        option_elements.nth(option).wait_for(state="visible")
        self.click(option_elements.nth(option))

    def check_aspirant_endoscopist_not_present(self) -> None:
        """
        This method is designed to check the aspirant endoscopist not present option.
        It checks the aspirant endoscopist not present option.
        """
        self.aspirant_endoscopist_not_present.check()

    def click_show_drug_information(self) -> None:
        """
        This method is designed to click on the show drug information link.
        It clicks on the show drug information link.
        """
        self.click(self.show_drug_information_detail)

    def select_drug_type_option1(self, option: str) -> None:
        """
        This method is designed to select a drug type from the first drug type options.
        It clicks on the drug type option and selects the given option.

        Args:
            option (str): The option to select from the aspirant endoscopist options.
        """
        self.click(self.drug_type_option1)
        self.drug_type_option1.select_option(option)

    def fill_drug_type_dose1(self, dose: str) -> None:
        """
        This method is designed to fill in the drug type dose for the first drug type options.
        It fills in the given dose.

        Args:
            dose (str): The dose to fill in for the drug type.
        """
        self.click(self.drug_type_dose1)
        self.drug_type_dose1.fill(dose)

    def click_show_endoscopy_information(self) -> None:
        """
        This method is designed to click on the show endoscopy information link.
        It clicks on the show endoscopy information link.
        """
        self.click(self.show_endoscopy_information_details)

    def check_endoscope_inserted_yes(self) -> None:
        """
        This method is designed to check the endoscope inserted yes option.
        It checks the endoscope inserted yes option.
        """
        self.endoscope_inserted_yes.check()

    def check_endoscope_inserted_no(self) -> None:
        """
        This method is designed to check the endoscope inserted no option.
        It checks the endoscope inserted no option.
        """
        self.endoscope_inserted_no.check()

    def select_therapeutic_procedure_type(self) -> None:
        """
        This method is designed to select the therapeutic procedure type.
        It selects the therapeutic procedure type.
        """
        self.therapeutic_procedure_type.check()

    def select_diagnostic_procedure_type(self) -> None:
        """
        This method is designed to select the diagnostic procedure type.
        It selects the diagnostic procedure type.
        """
        self.diagnostic_procedure_type.check()

    def click_show_completion_proof_information(self) -> None:
        """
        This method is designed to click on the show completion proof information link.
        It clicks on the show completion proof information link.
        """
        self.click(self.show_completion_proof_information_details)

    def click_show_failure_information(self) -> None:
        """
        This method is designed to click on the show failure information link.
        It clicks on the show failure information link.
        """
        self.click(self.show_failure_information_details)

    def click_add_polyp_button(self) -> None:
        """
        This method is designed to click on the add polyp button.
        It clicks on the add polyp button.
        """
        self.click(self.add_polyp_button)
        self.page.wait_for_timeout(1000)

    def click_polyp1_add_intervention_button(self) -> None:
        """
        This method is designed to click on the add intervention button for polyp 1.
        It clicks on the add intervention button for polyp 1.
        """
        self.click(self.polyp1_add_intervention_button)

    def click_polyp2_add_intervention_button(self) -> None:
        """
        This method is designed to click on the add intervention button for polyp 2.
        It clicks on the add intervention button for polyp 2.
        """
        self.click(self.polyp2_add_intervention_button)

    def check_dataset_complete_checkbox(self) -> None:
        """
        This method is designed to check the dataset complete checkbox.
        It checks the dataset complete checkbox.
        """
        self.dataset_complete_checkbox.check()

    def check_dataset_incomplete_checkbox(self) -> None:
        """
        This method is designed to check the dataset incomplete checkbox.
        It checks the dataset incomplete checkbox.
        """
        self.dataset_incomplete_checkbox.check()

    def click_save_dataset_button(self) -> None:
        """
        This method is designed to click on the save dataset button.
        It clicks on the save dataset button.
        """
        self.safe_accept_dialog(self.save_dataset_button)

    def expect_text_to_be_visible(self, text: str) -> None:
        """
        This method is designed to expect a text to be visible on the page.
        It checks if the given text is visible.

        Args:
            text (str): The text to check for visibility.
        """
        expect(self.page.get_by_text(text)).to_contain_text(text)

    def select_polyp1_pathology_provider_option_index(self, option: int) -> None:
        """
        This method is designed to select a pathology provider from the pathology provider options.
        It clicks on the pathology provider link and selects the given option by index.

        Args:
            option (int): The index of the option to select from the pathology provider options.
        """
        self.click(self.polyp1_pathology_provider)
        select_locator = self.page.locator(self.visible_ui_results_string)
        select_locator.first.wait_for(state="visible")
        # Find all option elements inside the select and click the one at the given index
        option_elements = select_locator.first.locator("option")
        option_elements.nth(option).wait_for(state="visible")
        self.click(option_elements.nth(option))

    def select_polyp1_pathologist_option_index(self, option: int) -> None:
        """
        This method is designed to select a pathologist from the pathologist options.
        It clicks on the pathologist link and selects the given option by index.

        Args:
            option (int): The index of the option to select from the pathologist options.
        """
        self.click(self.polyp1_pathologist)
        select_locator = self.page.locator(self.visible_ui_results_string)
        select_locator.first.wait_for(state="visible")
        # Find all option elements inside the select and click the one at the given index
        option_elements = select_locator.first.locator("option")
        option_elements.nth(option).wait_for(state="visible")
        self.click(option_elements.nth(option))

    def select_loopup_option_index(self, option: int) -> None:
        """
        This method is designed to select a lookup option by index.
        It clicks on the lookup link and selects the given option by index.

        Args:
            option (int): The index of the option to select from the lookup options.
        """
        select_locator = self.page.locator(self.visible_ui_results_string)
        select_locator.first.wait_for(state="visible")
        # Find all option elements inside the select and click the one at the given index
        option_elements = select_locator.first.locator("option")
        option_elements.nth(option).wait_for(state="visible")
        self.click(option_elements.nth(option))

    def click_edit_dataset_button(self) -> None:
        """
        This method is designed to click on the edit dataset button.
        It clicks on the edit dataset button.
        """
        self.click(self.edit_dataset_button)

    def assert_polyp_algorithm_size(
        self, polyp_number: int, expected_value: Optional[str]
    ) -> None:
        """
        This method asserts that the polyp size is as expected.
        It retrieves the polyp size from the page and compares it with the expected value.

        Args:
            polyp_number (int): The number of the polyp to check (1 or 2).
            expected_value (int): The expected value of the polyp size.
        """
        dataset_id = self.get_dataset_id()
        if dataset_id == -1:
            raise ValueError("Dataset ID not found in the URL.")
        actual_value = get_investigation_dataset_polyp_algorithm_size(
            dataset_id, polyp_number
        )

        # Assert that the actual value matches the expected value
        logging.info(
            f"Checking Polyp {polyp_number} algorithm size: actual={actual_value}, expected={expected_value}"
        )

        if actual_value is None or expected_value is None:
            assert (
                actual_value == expected_value
            ), f"Expected '{expected_value}', but got '{actual_value}'"
        else:
            assert (
                str(actual_value).strip() == str(expected_value).strip()
            ), f"Expected '{expected_value}', but got '{actual_value}'"

    def assert_polyp_category(
        self, polyp_number: int, expected_value: Optional[str]
    ) -> None:
        """
        This method asserts that the polyp category is as expected.
        It retrieves the polyp category from the page and compares it with the expected value.

        Args:
            polyp_number (int): The number of the polyp to check (1 or 2).
            expected_value (str): The expected value of the polyp category.
        """
        dataset_id = self.get_dataset_id()
        if dataset_id == -1:
            raise ValueError("Dataset ID not found in the URL.")
        actual_value = get_investigation_dataset_polyp_category(
            dataset_id, polyp_number
        )

        # Assert that the actual value matches the expected value
        logging.info(
            f"Checking Polyp {polyp_number} category: actual={actual_value}, expected={expected_value}"
        )

        if actual_value is None or expected_value is None:
            assert (
                actual_value == expected_value
            ), f"Expected '{expected_value}', but got '{actual_value}'"
        else:
            assert (
                str(actual_value).strip() == str(expected_value).strip()
            ), f"Expected '{expected_value}', but got '{actual_value}'"

    def get_dataset_id(self) -> int:
        """
        Extracts the dataset id from the current URL using Playwright.
        Returns -1 if not found.
        """
        url = self.page.url  # Playwright's current page URL
        if "?" not in url:
            return -1
        query_string = url.split("?", 1)[1]
        params = query_string.split("&")
        dataset_id = -1
        for param in params:
            if param.startswith("id="):
                try:
                    dataset_id = int(param.split("=", 1)[1])
                except ValueError:
                    dataset_id = -1
        return dataset_id

    def click_polyp_add_intervention_button(self, polyp_number: int) -> None:
        """
        Clicks the add intervention button for the specified polyp number.

        Args:
            polyp_number (int): The number of the polyp.
        """

        self.click(
            self.page.locator(f"#spanPolypInterventionLink{polyp_number}").get_by_role(
                "link", name=self.add_intervention_string
            )
        )


class SiteLookupOptions(StrEnum):
    """Enum for site lookup options"""

    RL401 = "35317"
    RL402 = "42805"
    RL403 = "42804"
    RL404 = "42807"
    RL405 = "42808"


class PractitionerOptions(StrEnum):
    """
    Enum for practitioner options
    Only the first four options are present in this class
    """

    AMID_SNORING = "1251"
    ASTONISH_ETHANOL = "82"
    DEEP_POLL_DERBY = "2033"
    DOORFRAME_THIRSTY = "2034"


class TestingClinicianOptions(StrEnum):
    """Enum for testing clinician options"""

    __test__ = False

    BORROWING_PROPERTY = "886"
    CLAUSE_CHARTING = "918"
    CLUTTER_PUMMEL = "916"
    CONSONANT_TRACTOR = "101"


class AspirantEndoscopistOptions(StrEnum):
    """Enum for aspirant endoscopist options"""

    ITALICISE_AMNESTY = "1832"


class DrugTypeOptions(StrEnum):
    """Enum for drug type options"""

    BISACODYL = "200537~Tablet(s)"
    KLEAN_PREP = "200533~Sachet(s)"
    PICOLAX = "200534~Sachet(s)"
    SENNA_LIQUID = "203067~5ml Bottle(s)"
    SENNA = "200535~Tablet(s)"
    MOVIPREP = "200536~Sachet(s)"
    CITRAMAG = "200538~Sachet(s)"
    MANNITOL = "200539~Litre(s)"
    GASTROGRAFIN = "200540~Mls Solution"
    PHOSPHATE_ENEMA = "200528~Sachet(s)"
    MICROLAX_ENEMA = "200529~Sachet(s)"
    OSMOSPREP = "203063~Tablet(s)"
    FLEET_PHOSPHO_SODA = "203064~Mls Solution"
    CITRAFLEET = "203065~Sachet(s)"
    PLENVU = "305487~Sachet(s)"
    OTHER = "203066"


class BowelPreparationQualityOptions(StrEnum):
    """Enum for bowel preparation quality options"""

    EXCELLENT = "305579"
    GOOD = "17016"
    FAIR = "17017"
    POOR = "17995~Enema down scope~305582"
    INADEQUATE = "305581~~305582"


class ComfortOptions(StrEnum):
    """Enum for comfort during examination / recovery options"""

    NO_DISCOMFORT = "18505"
    MINIMAL_DISCOMFORT = "17273"
    MILD_DISCOMFORT = "17274"
    MODERATE_DISCOMFORT = "17275"
    SEVERE_DISCOMFORT = "17276"


class EndoscopyLocationOptions(StrEnum):
    """Enum for endoscopy location options"""

    ANUS = "17231~Scope not inserted clinical reason~204342"
    RECTUM = "17232~Scope not inserted clinical reason~204342"
    SIGMOID_COLON = "17233"
    DESCENDING_COLON = "17234"
    SPLENIC_FLEXURE = "17235"
    TRANSVERSE_COLON = "17236"
    HEPATIC_FLEXURE = "17237"
    ASCENDING_COLON = "17238"
    CAECUM = "17239~Colonoscopy Complete"
    ILEUM = "17240~Colonoscopy Complete"
    ANASTOMOSIS = "17241~Colonoscopy Complete"
    APPENDIX = "17242~Colonoscopy Complete"


class YesNoOptions(StrEnum):
    """Enum for scope imager used options"""

    YES = "17058"
    NO = "17059"


class InsufflationOptions(StrEnum):
    """Enum for insufflation options"""

    AIR = "200547"
    CO2 = "200548"
    CO2_AIR = "200549"
    AIR_CO2 = "200550"
    WATER = "306410"
    WATER_CO2 = "305727"
    WATER_AIR = "305728"
    WATER_AIR_CO2 = "305729"


class OutcomeAtTimeOfProcedureOptions(StrEnum):
    """Enum for outcome at time of procedure options"""

    LEAVE_DEPARTMENT = "17148~Complications are optional"
    PLANNED_ADMISSION = "17998~Complications are optional"
    UNPLANNED_ADMISSION = "17147~Complications are mandatory"


class LateOutcomeOptions(StrEnum):
    """Enum for late outcome options"""

    NO_COMPLICATIONS = "17216~Complications are not required"
    CONDITION_RESOLVED = "17217~Complications are mandatory"
    TELEPHONE_CONSULTATION = "17218~Complications are mandatory"
    OUTPATIENT_CONSULTATION = "17219~Complications are mandatory"
    HOSPITAL_ADMISSION = "17220~Complications are mandatory"


class CompletionProofOptions(StrEnum):
    """Enum for completion proof options"""

    PHOTO_ANASTOMOSIS = "200573"
    PHOTO_APPENDIX = "200574"
    PHOTO_ILEO = "200575"
    PHOTO_TERMINAL_ILEUM = "200576"
    VIDEO_ANASTOMOSIS = "200577"
    VIDEO_APPENDIX = "200578"
    VIDEO_ILEO = "200579"
    VIDEO_TERMINAL_ILEUM = "200580"
    NOT_POSSIBLE = "203007"


class FailureReasonsOptions(StrEnum):
    """Enum for failure reasons options"""

    NO_FAILURE_REASONS = "18500"
    ADHESION = "17165"
    ADVERSE_REACTION_BOWEL = "200253~AVI"
    ADVERSE_REACTION_IV = "17767~AVI"
    ANAPHYLACTIC_REACTION = "17978"
    BLEEDING_INCIDENT = "205148"
    BLEEDING_MINOR = "205149~AVI"
    BLEEDING_INTERMEDIATE = "205150~AVI"
    BLEEDING_MAJOR = "205151~AVI"
    BLEEDING_UNCLEAR = "205152~AVI"
    CARDIAC_ARREST = "17161~AVI"
    CARDIO_RESPIRATORY = "200598~AVI"
    DEATH = "17176~AVI"
    EQUIPMENT_FAILURE = "17173~AVI"
    LOOPING = "17166"
    OBSTRUCTION = "17170~AVI, Requires Other Finding"
    PAIN = "17155"
    PATIENT_UNWELL = "17164~AVI"
    PERFORATION = "205153~AVI"


class PolypClassificationOptions(StrEnum):
    """Enum for polyp classification options"""

    IP = "17296"
    ISP = "200596"
    IS = "17295"
    IIA = "200595"
    IIB = "200591"
    IIC = "200592"
    LST_G = "200593"
    LST_NG = "200594"
    LLA_C = "200683"


class PolypAccessOptions(StrEnum):
    """Enum for polyp access options"""

    EASY = "305583"
    DIFFICULT = "305584"
    NOT_KNOWN = "17060"


class PolypInterventionModalityOptions(StrEnum):
    """Enum for polyp intervention modality options"""

    POLYPECTOMY = "17189~Resection"
    EMR = "17193~Resection"
    ESD = "17520~Resection"


class PolypInterventionDeviceOptions(StrEnum):
    """Enum for polyp intervention device options"""

    HOT_SNARE = "17070"
    HOT_BIOPSY = "17071~En-bloc"
    COLD_SNARE = "17072"
    COLD_BIOPSY = "17073~En-bloc"
    ENDOSCOPIC_KNIFE = "17531"


class PolypInterventionExcisionTechniqueOptions(StrEnum):
    """Enum for polyp intervention excision technique options"""

    EN_BLOC = "17751"
    PIECE_MEAL = "17750~~305578"


class PolypTypeOptions(StrEnum):
    """Enum for polyp type options"""

    ADENOMA = "17299~Sub Type Applicable~204351,306411,306420"
    SERRATED_LESION = "17061~Sub Type Applicable"
    INFLAMATORY_POLYP = "17300~Sub Type Not Applicable"
    PEUTZ_JEGHERS_POLYP = "17301~Sub Type Not Applicable"
    JUVENILE_POLYP = "17302~Sub Type Not Applicable"
    OTHER_POLYP = "17062~Sub Type Applicable"
    NORMAL_MUCOSA = "17518~Sub Type Not Applicable"


class AdenomaSubTypeOptions(StrEnum):
    """Enum for adenoma sub type options"""

    TUBULAR_ADENOMA = "17292"
    TUBULOVILLOUS_ADENOMA = "17293"
    VILLOUS_ADENOMA = "17294"
    NOT_REPORTED = "203004"


class SerratedLesionSubTypeOptions(StrEnum):
    """Enum for serrated lesion sub type options"""

    HYPERPLASTIC_POLYP = "17090~~306420"
    MIXED_POLYP = "204347~~204351,305572,306411"
    SESSILE_SERRATED_LESION = "204348~~306411,306420"
    SESSILE_SERRATED_LESION_WITH_DYSPLASIA = "204349~~204351,306411"
    TRADITIONAL_SERRATED_ADENOMA = "204350~~204351,306411"


class OtherPolypSubTypeOptions(StrEnum):
    """Enum for other polyp sub type options"""

    NEURO_ENDOCRINE_TUMOUR = "17092"
    LYMPHOID = "17093"
    LIPOMA = "17094"
    STROMAL = "17095"
    OTHER_POLYP = "17096"


class PolypExcisionCompleteOptions(StrEnum):
    """Enum for polyp excision complete options"""

    R0 = "305574"
    R1 = "305575"
    NOT_ASSESSABLE = "17522"


class PolypDysplasiaOptions(StrEnum):
    """Enum for polyp dysplasia options"""

    NO_DYSPLASIA = "20300"
    LOW_GRADE_DYSPLASIA = "17970"
    HIGH_GRADE_DYSPLASIA = "17971"
    NOT_REPORTED = "204336"


class YesNoUncertainOptions(StrEnum):
    """Enum for polyp carcinoma options"""

    YES = "17058"
    NO = "17059"
    UNCERTAIN = "17105"
