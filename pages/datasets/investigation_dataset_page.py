from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from enum import StrEnum


class InvestigationDatasetsPage(BasePage):
    """Investigation Datasets Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # Colonoscopy datasets page locators
        self.site_lookup_link = self.page.locator("#UI_SITE_SELECT_LINK")
        self.practitioner_link = self.page.locator("#UI_SSP_PIO_SELECT_LINK")
        self.testing_clinician_link = self.page.locator(
            "#UI_CONSULTANT_PIO_SELECT_LINK"
        )
        self.aspirant_endoscopist_link = self.page.locator(
            "#UI_ASPIRANT_ENDOSCOPIST_PIO_SELECT_LINK"
        )
        self.show_drug_information_detail = self.page.locator("#anchorDrug")
        self.drug_type_option1 = self.page.locator("#UI_BOWEL_PREP_DRUG1")
        self.drug_type_dose1 = self.page.locator("#UI_BOWEL_PREP_DRUG_DOSE1")
        self.show_endoscopy_information_details = self.page.locator(
            "#anchorColonoscopy"
        )
        self.endoscope_inserted_yes = self.page.locator("#radScopeInsertedYes")
        self.theraputic_procedure_type = self.page.get_by_role(
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
            "link", name="Add Intervention"
        )
        self.polyp2_add_intervention_button = self.page.locator(
            "#spanPolypInterventionLink2"
        ).get_by_role("link", name="Add Intervention")
        self.dataset_complete_checkbox = self.page.locator("#radDatasetCompleteYes")
        self.save_dataset_button = self.page.locator(
            "#UI_DIV_BUTTON_SAVE1"
        ).get_by_role("button", name="Save Dataset")

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

    def select_theraputic_procedure_type(self) -> None:
        """
        This method is designed to select the therapeutic procedure type.
        It selects the therapeutic procedure type.
        """
        self.theraputic_procedure_type.check()

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

    LP = "17296"
    LSP = "200596"
    LS = "17295"
    LLA = "200595"
    LLB = "200591"
    LLC = "200592"
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


class PolypInterventionExcisionTechniqueOptions(StrEnum):
    """Enum for polyp intervention excision technique options"""

    EN_BLOC = "17751"
    PIECE_MEAL = "17750~~305578"
