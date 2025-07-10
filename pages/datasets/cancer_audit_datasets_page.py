from playwright.sync_api import Page
from pages.base_page import BasePage
from enum import StrEnum
from utils.calendar_picker import CalendarPicker
from datetime import datetime
from pages.datasets.investigation_dataset_page import (
    EndoscopyLocationOptions as TumorLocationOptions,
)


class CancerAuditDatasetsPage(BasePage):
    """Subject Datasets Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Cancer audit datasets page locators
        self.dataset_complete_button = self.page.get_by_role("radio", name="Yes")
        self.staging_and_pretreatment_information_show_details_button = (
            self.page.locator("#anchorPreTreatment")
        )
        self.tumour_information_show_details_button = self.page.locator("#anchorTumour")
        self.add_new_treatment_button = self.page.get_by_role(
            "button", name="Add New Treatment"
        )
        self.save_dataset_button = self.page.locator(
            "#UI_DIV_BUTTON_SAVE1"
        ).get_by_role("button", name="Save Dataset")
        self.edit_dataset_button = self.page.locator(
            "#UI_DIV_BUTTON_EDIT1"
        ).get_by_role("button", name="Edit Dataset")
        # Types of Scan
        self.abdominal_ultrasound_checkbox = self.page.get_by_role(
            "checkbox", name="Abdominal Ultrasound"
        )
        self.ct_scan_checkbox = self.page.get_by_role("checkbox", name="CT Scan")
        self.endoanal_ultrasound_checkbox = self.page.get_by_role(
            "checkbox", name="Endoanal Ultrasound"
        )
        self.endorectal_ultrasound_checkbox = self.page.get_by_role(
            "checkbox", name="Endorectal Ultrasound"
        )
        self.mri_scan_checkbox = self.page.get_by_role("checkbox", name="MRI Scan")
        self.positron_emission_tomography_checkbox = self.page.get_by_role(
            "checkbox", name="Positron Emission Tomography"
        )
        # Metastases Location
        self.peritoneum_omentum_checkbox = self.page.get_by_role(
            "checkbox", name="Peritoneum/Omentum"
        )
        self.bone_checkbox = self.page.get_by_role("checkbox", name="Bone")
        self.lung_checkbox = self.page.get_by_role("checkbox", name="Lung")
        self.liver_checkbox = self.page.get_by_role("checkbox", name="Liver")
        self.other_checkbox = self.page.get_by_role("checkbox", name="Other")
        self.other_textbox = self.page.get_by_role(
            "textbox", name="Please enter the other"
        )
        # Other Staging and Pre-Treatment Information locators
        self.treatment_received_select = self.page.get_by_label(
            "Treatment Received", exact=True
        )
        # Tumour Information
        self.date_of_diagnosis_textbox = self.page.get_by_role(
            "textbox", name="Date of Diagnosis"
        )
        # Treatment Information
        self.date_of_treatment_textbox = self.page.get_by_role(
            "textbox", name="Date of Treatment Date of"
        )
        self.treatment_provider_lookup_link = self.page.locator("#UI_RESULTS_rnkylygq")
        self.consultant_lookup_link = self.page.locator("#UI_RESULTS_gpwbfppu")

    def check_dataset_complete_button(self) -> None:
        """Checks the 'Yes' radio button for dataset completion."""
        self.dataset_complete_button.check()

    def click_staging_and_pretreatment_information_show_details_button(self) -> None:
        """Clicks on the 'Show Details' button for the Staging and Pretreatment Information section."""
        self.click(self.staging_and_pretreatment_information_show_details_button)

    def click_tumour_information_show_details_button(self) -> None:
        """Clicks on the 'Show Details' button for the Tumour Information section."""
        self.click(self.tumour_information_show_details_button)

    def click_add_new_treatment_button(self) -> None:
        """Clicks on the 'Add New Treatment' button."""
        self.click(self.add_new_treatment_button)

    def click_save_dataset_button(self) -> None:
        """Clicks on the 'Save Dataset' button."""
        self.click(self.save_dataset_button)

    def click_edit_dataset_button(self) -> None:
        """Clicks on the 'Edit Dataset' button"""
        self.click(self.edit_dataset_button)

    def check_abdominal_ultrasound_checkbox(self) -> None:
        """Checks the 'Abdominal Ultrasound' checkbox."""
        self.abdominal_ultrasound_checkbox.check()

    def check_ct_scan_checkbox(self) -> None:
        """Checks the 'CT Scan' checkbox."""
        self.ct_scan_checkbox.check()

    def check_endoanal_ultrasound_checkbox(self) -> None:
        """Checks the 'Endoanal Ultrasound' checkbox."""
        self.endoanal_ultrasound_checkbox.check()

    def check_endorectal_ultrasound_checkbox(self) -> None:
        """Checks the 'Endorectal Ultrasound' checkbox."""
        self.endorectal_ultrasound_checkbox.check()

    def check_mri_scan_checkbox(self) -> None:
        """Checks the 'MRI Scan' checkbox."""
        self.mri_scan_checkbox.check()

    def check_positron_emission_tomography_checkbox(self) -> None:
        """Checks the 'Positron Emission Tomography' checkbox."""
        self.positron_emission_tomography_checkbox.check()

    def check_peritoneum_omentum_checkbox(self) -> None:
        """Checks the 'Peritoneum/Omentum' checkbox."""
        self.peritoneum_omentum_checkbox.check()

    def check_bone_checkbox(self) -> None:
        """Checks the 'Bone' checkbox."""
        self.bone_checkbox.check()

    def check_lung_checkbox(self) -> None:
        """Checks the 'Lung' checkbox."""
        self.lung_checkbox.check()

    def check_liver_checkbox(self) -> None:
        """Checks the 'Liver' checkbox."""
        self.liver_checkbox.check()

    def check_other_checkbox(self) -> None:
        """Checks the 'Other' checkbox."""
        self.other_checkbox.check()

    def fill_other_textbox(self, text: str) -> None:
        """Fills the 'Other' textbox with the provided text and presses Tab."""
        self.other_textbox.fill(text)
        self.other_textbox.press("Tab")

    def select_treatment_received_option(self, option: str) -> None:
        """Select and option from the 'Treatment Received' dropdown"""
        self.treatment_received_select.select_option(option)

    def fill_date_of_diagnosis_textbox(self, date: datetime) -> None:
        """Fills the 'Date of Diagnosis' textbox with the provided date."""
        CalendarPicker(self.page).calendar_picker_ddmmyyyy(
            date, self.date_of_diagnosis_textbox
        )

    def fill_date_of_treatment_textbox(self, date: datetime) -> None:
        """Fills the 'Date of Treatment' textbox with the provided date."""
        CalendarPicker(self.page).calendar_picker_ddmmyyyy(
            date, self.date_of_treatment_textbox
        )

    def select_treatment_provider_lookup_option(self, option: str) -> None:
        """Selects an option from the Treatment Provider lookup dropdown."""
        self.treatment_provider_lookup_link.select_option(option)

    def select_consultant_lookup_option(self, option: str) -> None:
        """Selects an option from the Consultant lookup dropdown."""
        self.consultant_lookup_link.select_option(option)

    def select_first_definitive_teatment_information_option(self, option: str) -> None:
        """Selects an option for the First Definitive Treatment Information."""
        self.page.locator(f"#UI_FIRST_DEFINITIVE_TREATMENT_1_{option}").check()


NOT_REPORTED_CODE = "202140~~202188"


class ASAGradeOptions(StrEnum):
    """Enum for ASA Grade options."""

    FIT = "17009"
    RELEVANT_DISEASE = "17010"
    RESTRICTIVE_DISEASE = "17011"
    LIFE_THREATENING_DISEASE = "17012"
    MORIBUND = "17013"
    NOT_KNOWN = "17015"


class YesNoOptions(StrEnum):
    """Enum for YesNo options."""

    YES = "17058"
    NO = "17059"


class MetastasesPresentOptions(StrEnum):
    """Enum for Metastases Present options."""

    CERTAIN = "17131~~202199"
    NONE = "17130"
    NOT_REPORTED = NOT_REPORTED_CODE


class FinalPreTreatmentTCategoryOptions(StrEnum):
    """Enum for Final Pre-Treatment T Category options."""

    CTX = "17356"
    CT0 = "202203"
    CT1 = "17357"
    CT2 = "17358"
    CT3 = "17359"
    CT4 = "17360"
    NOT_REPORTED = NOT_REPORTED_CODE


class FinalPreTreatmentNCategoryOptions(StrEnum):
    """Enum for Final Pre-Treatment N Category options."""

    CNX = "202201"
    CN0 = "17256"
    CN1 = "17257"
    CN2 = "17258"
    NOT_REPORTED = NOT_REPORTED_CODE


class ReasonNoTreatmentRecievedOptions(StrEnum):
    """Enum for Reason No Treatment Received options."""

    ADVANCED_DISEASE = "99016"
    DIED = "99017"
    MEDICALLY_UNFIT = "99014"
    NO_EVIDENCE_OF_CANCER = "99061"
    PATIENT_CHOICE = "99015"
    UNKNOWN = "99018"


class PreviouslyExcisedTumorOptions(StrEnum):
    """Enum for Previously Excised Tumor options."""

    YES = "17058~~305403"
    NO = "17059"
    UNKNOWN = "202197~~202204"
    NOT_REPORTED = "202140"


class TreatmentTypeOptions(StrEnum):
    """Enum for Treatment Type options."""

    SURGICAL = "202143"
    NON_SURGICAL = "202144"


class TreatmentGivenOptions(StrEnum):
    """Enum for Treatment Given options."""

    CHEMOTHERAPY = "202160~~202184,202217,202218,202219,202220,202221,202222,202223,202224,202225,202226,202227,202228,202287,305395,305397"
    RADIOTHERAPY = "202163~~202183,202217,202218,202287,305395,305397"
    CHEMOTHERAPY_AND_RADIOTHERAPY = "202161~~202217,202218,202287,305395,305397"
    IMMUNOTHERAPY = "202162~~202184,202217,202218,202219,202220,202221,202222,202223,202224,202225,202226,202227,202228,202287,305395,305397"
    SPECIALIST_PALLIATIVE_CARE = "202164~~202184,202217,202218,202219,202220,202221,202222,202223,202224,202225,202226,202227,202228,305395,305397"


class CancerTreatmentIntentOptions(StrEnum):
    """Enum for Cancer Treatment Intent options."""

    CURATIVE = "17370"
    PALLIATIVE = "17371"
    UNCERTAIN = "17372"
    NOT_KNOWN = "17373"


class NHSOrPrivateOptions(StrEnum):
    """Enum for NHS or Private options."""

    NHS = "202153~~202177,202178"
    PRIVATE = "202154~~202179"


class TreatmentProviderLookupOptions(StrEnum):
    """Enum for Treatment Provider lookup options."""

    ADVANCE_NURSE_PRACTITIONER_1 = "51905"
    ADVANCE_NURSE_PRACTITIONER_10 = "51914"
    ADVANCE_NURSE_PRACTITIONER_12 = "52313"
    ADVANCE_NURSE_PRACTITIONER_13 = "52314"
    ADVANCE_NURSE_PRACTITIONER_14 = "52315"
    ADVANCE_NURSE_PRACTITIONER_15 = "52316"
    ADVANCE_NURSE_PRACTITIONER_16 = "52317"
    ADVANCE_NURSE_PRACTITIONER_2 = "51906"
    ADVANCE_NURSE_PRACTITIONER_3 = "51907"
    ADVANCE_NURSE_PRACTITIONER_4 = "51908"
    ADVANCE_NURSE_PRACTITIONER_5 = "51909"
    ADVANCE_NURSE_PRACTITIONER_6 = "51910"
    ADVANCE_NURSE_PRACTITIONER_7 = "51911"
    ADVANCE_NURSE_PRACTITIONER_8 = "51912"
    ADVANCE_NURSE_PRACTITIONER_9 = "51913"
    ADVANCE_NURSE_PRACTITIONER_11 = "52310"
    ALFRED_SQUIRE_HEALTH_CENTRE = "51796"
    ASHMORE_PARK_CLINIC = "51797"
    BCS_RUSSELLS_HALL = "61273"
    BILSTON_HEALTH_CENTRE = "51798"
    BLAKENALL_MEADOW_PRACTICE = "42113"
    BRADLEY_CLINIC = "51799"
    BROOKLANDS_PARADE_CLINIC = "51800"
    BUSHBURY_HEALTH_CENTRE = "51801"


class ConsultantLookupOptions(StrEnum):
    """Enum for Consultant lookup options."""

    B_FRAME = "201"
    DAYDREAM_TRICEPS_ONCOLOGIST = "164"
    DAYDREAM_TRICEPS_SURGEON = "161"
    ENDURANCE_SNACK = "241"
    FROSTY_CRISPING = "461"
    SLAM_DAFFODIL = "181"
