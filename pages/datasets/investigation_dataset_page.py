import re
from playwright.sync_api import Page, expect, Locator
from pages.base_page import BasePage
from enum import Enum, StrEnum
from utils.oracle.oracle_specific_functions.subject_datasets import (
    get_investigation_dataset_polyp_category,
    get_investigation_dataset_polyp_algorithm_size,
)
from typing import Optional, Any, Union, List
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
        self.reporting_radiologist_link = self.page.locator(
            "#UI_REPORTING_CLINICIAN_PIO_SELECT_LINK"
        )
        self.show_contrast_tagging_and_drug_information = self.page.locator(
            "#anchorContrastTaggingDrug"
        )
        self.show_radiology_information = self.page.locator("#anchorRadiology")
        self.aspirant_endoscopist_link = self.page.locator(
            "#UI_ASPIRANT_ENDOSCOPIST_PIO_SELECT_LINK"
        )
        self.aspirant_endoscopist_not_present = self.page.locator(
            "#UI_ASPIRANT_ENDOSCOPIST_NR"
        )
        self.show_drug_information_detail = self.page.locator("#anchorDrug")
        self.show_suspected_findings = self.page.locator("#anchorRadiologyFindings")
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
        self.show_radiology_failure_information_details = self.page.locator(
            "#anchorRadiologyFailure"
        )
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
        self.sections = self.page.locator(".DatasetSection")
        self.visible_search_text_input = self.page.locator(
            'input[id^="UI_SEARCH_"]:visible'
        )

        # Repeat strings:
        self.bowel_preparation_administered_string = "Bowel Preparation Administered"
        self.antibiotics_administered_string = "Antibiotics Administered"
        self.other_drugs_administered_string = "Other Drugs Administered"

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

    def select_testing_clinician_from_name(self, name: str) -> None:
        """
        This method is designed to select a testing clinician from the testing clinician options.
        It clicks on the testing clinician link then searches for the provided clinician.
        Then it selects this clinician from the options

        Args:
            name (str): The name of the testing clinician to select.
        """
        self.click(self.testing_clinician_link)
        self.visible_search_text_input.fill(name)
        self.visible_search_text_input.press("Enter")
        select_locator = self.page.locator(self.visible_ui_results_string)
        option_elements = select_locator.first.locator("option")
        option_elements.nth(-1).wait_for(state="visible")
        self.click(option_elements.nth(-1))

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

    def select_reporting_radiologist_option_index(self, option: int) -> None:
        """
        This method is designed to select a reporting radiologist from the reporting radiologist options.
        It clicks on the reporting radiologist link and selects the given option by index.

        Args:
            option (int): The index of the option to select from the reporting radiologist options.
        """
        self.click(self.reporting_radiologist_link)
        select_locator = self.page.locator(self.visible_ui_results_string)
        select_locator.first.wait_for(state="visible")
        # Find all option elements inside the select and click the one at the given index
        option_elements = select_locator.first.locator("option")
        option_elements.nth(option).wait_for(state="visible")
        self.click(option_elements.nth(option))

    def click_show_contrast_tagging_and_drug_information(self) -> None:
        """
        This method is designed to click on the show contrast tagging and drug information link.
        It clicks on the show contrast tagging and drug information link.
        """
        self.click(self.show_contrast_tagging_and_drug_information)

    def click_show_radiology_information(self) -> None:
        """
        This method is designed to click on the show radiology information link.
        It clicks on the show radiology information link.
        """
        self.click(self.show_radiology_information)

    def click_show_radiology_failure_information(self) -> None:
        """
        This method is designed to click on the show radiology failure information link.
        It clicks on the show radiology failure information link.
        """
        self.click(self.show_radiology_failure_information_details)

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

    def click_show_suspected_findings_details(self) -> None:
        """
        This method is designed to click on the show suspected findings details link.
        It clicks on the show suspected findings details link.
        """
        logging.info("[DEBUG] Clicking on Show Suspected Findings Details")
        self.page.wait_for_timeout(1000)
        self.show_suspected_findings.click()

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
        self.click(self.endoscope_inserted_yes)

    def check_endoscope_inserted_no(self) -> None:
        """
        This method is designed to check the endoscope inserted no option.
        It checks the endoscope inserted no option.
        """
        self.click(self.endoscope_inserted_no)

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
        expect(self.page.get_by_text(text)).to_contain_text(text, timeout=10000)

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

    def select_lookup_option_index(self, option: int) -> None:
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

    def populate_select_by_id(
        self, field_base: str, polyp_number: int, option: str
    ) -> None:
        """
        Populates a <select> element using a predictable ID pattern based on field name and polyp number.
        This method is useful when label-based selectors (e.g., using `right-of(:text(...))`) are unreliable
        due to ambiguous or repeated text labels on the page.
        Args:
            field_base (str): The base name of the field (e.g., "POLYP_PATHOLOGY_LOST").
            polyp_number (int): The polyp index (e.g., 1 for the first polyp).
            option (str): The value to be selected from the dropdown.
        Example:
            populate_select_by_id("POLYP_PATHOLOGY_LOST", 1, YesNoOptions.YES)
            # Selects 'Yes' in <select id="UI_POLYP_PATHOLOGY_LOST1_1">
        """
        field_id = f"UI_{field_base.upper()}{polyp_number}_1"
        locator = self.page.locator(f"select#{field_id}")
        locator.wait_for(state="visible")
        locator.select_option(option)

    def is_edit_dataset_button_visible(self) -> bool:
        """
        Checks if the Edit Dataset button is visible
        Returns:
            bool: True if the button is visible, False if it is not
        """
        return self.edit_dataset_button.is_visible()

    def is_dataset_section_present(self, dataset_section_name: str) -> Optional[bool]:
        """
        Checks if a section of the investigation dataset is present
        Args:
            dataset_section_name (str): The name of the section you want to check
                - Investigation Dataset
                - Drug Information
                - Endoscopy Information
                - etc...
        Returns:
            bool: True if it is present, False if it is not
        """
        logging.info(f"Start: Searching for dataset section '{dataset_section_name}'")

        count = self.sections.count()

        for i in range(count):
            section = self.sections.nth(i)
            heading = section.locator("h4")
            if (
                heading.inner_text().strip().lower()
                == dataset_section_name.strip().lower()
            ):
                logging.info(f"Dataset section '{dataset_section_name}' found.")
                return True

        logging.info(f"Dataset section '{dataset_section_name}' not found.")
        return False

    def get_dataset_section(self, dataset_section_name: str) -> Optional[Locator]:
        """
        Retrieves a dataset section by matching its header text.
        Only returns the locator if the section is visible.
        Searches through all elements representing dataset sections, looking for one whose
        first <h4> header text matches the provided section name (case-insensitive).
        Args:
            dataset_section_name (str): The name of the dataset section to locate.
        Returns:
            Optioanl[Locator]: A Playwright Locator for the matching section if visible, or None if not found or not visible.
        """
        logging.info(f"START: Looking for section '{dataset_section_name}'")

        list_of_sections = self.sections.all()
        section_found = None

        for section in list_of_sections:
            header = section.locator("h4")
            if header.count() > 0:
                header_text = header.first.inner_text().strip().lower()
                if (
                    header_text == dataset_section_name.strip().lower()
                    and section.is_visible()
                ):
                    section_found = section
                    break

        logging.info(
            f"Dataset section '{dataset_section_name}' found and visible: {section_found is not None}"
        )
        return section_found

    def is_dataset_section_on_page(
        self, dataset_section: str | List[str], should_be_present: bool = True
    ) -> None:
        """
        Asserts whether the specified dataset section(s) are present or not on the page.
        Args:
            dataset_section (str or List[str]): The name of the dataset section to check for presence,
                or a list of section names.
                Examples:
                    "Investigation Dataset"
                    ["Investigation Dataset", "Drug Information", "Endoscopy Information"]
            should_be_present (bool): If True, asserts the section(s) are present.
                                    If False, asserts the section(s) are not present.
        Raises:
            AssertionError: If the actual presence does not match should_be_present.
        """
        if isinstance(dataset_section, str):
            section_found = self.get_dataset_section(dataset_section) is not None
            if should_be_present:
                assert (
                    section_found
                ), f"Expected section '{dataset_section}' to be present, but it was not found."
                logging.info(f"Section '{dataset_section}' is present as expected.")
            else:
                assert (
                    not section_found
                ), f"Expected section '{dataset_section}' to be absent, but it was found."
                logging.info(f"Section '{dataset_section}' is absent as expected.")
        elif isinstance(dataset_section, list):
            for section_name in dataset_section:
                section_found = self.get_dataset_section(section_name) is not None
                if should_be_present:
                    assert (
                        section_found
                    ), f"Expected section '{section_name}' to be present, but it was not found."
                    logging.info(f"Section '{section_name}' is present as expected.")
                else:
                    assert (
                        not section_found
                    ), f"Expected section '{section_name}' to be absent, but it was found."
                    logging.info(f"Section '{section_name}' is absent as expected.")
        else:
            raise TypeError("dataset_section must be a string or a list of strings.")

    def get_dataset_subsection(
        self, dataset_section_name: str, dataset_subsection_name: str
    ) -> Optional[Locator]:
        """
        Retrieves a specific subsection within a dataset section by matching the subsection's header text.
        The method first searches through elements with the `.DatasetSubSection` class.
        If the subsection is not found, it continues searching within `.DatasetSubSectionGroup` elements.
        Args:
            dataset_section_name (str): The name of the dataset section that contains the subsection.
            dataset_subsection_name (str): The name of the subsection to locate.
        Returns:
            Optional[Locator]: A Playwright Locator for the found subsection, or None if not found.
        Raises:
            ValueError: If the specified dataset section cannot be found.
        """
        logging.info(
            f"START: Looking for subsection '{dataset_subsection_name}' in section '{dataset_section_name}'"
        )

        dataset_section = self.get_dataset_section(dataset_section_name)

        sub_section_found = None

        if dataset_section is None:
            raise ValueError(f"Dataset section '{dataset_section_name}' was not found.")

        # First, search through .DatasetSubSection
        list_of_sections = dataset_section.locator(".DatasetSubSection").all()
        for section in list_of_sections:
            header = section.locator("h5")
            if (
                header
                and header.inner_text().strip().lower()
                == dataset_subsection_name.strip().lower()
            ):
                sub_section_found = section
                break

        # If not found, search through .DatasetSubSectionGroup
        if sub_section_found is None:
            list_of_sections = dataset_section.locator(".DatasetSubSectionGroup").all()
            for section in list_of_sections:
                header = section.locator("h5")
                if (
                    header
                    and header.inner_text().strip().lower()
                    == dataset_subsection_name.strip().lower()
                ):
                    sub_section_found = section
                    break

        logging.info(
            f"Dataset subsection '{dataset_section_name}', '{dataset_subsection_name}' found: {sub_section_found is not None}"
        )
        return sub_section_found

    def are_fields_on_page(
        self,
        section_name: str,
        subsection_name: Optional[str],
        field_names: list[str],
        visible: Optional[bool] = None,
    ) -> bool:
        """
        Checks if the given fields are present in a section or subsection, with optional visibility checks.
        Args:
            section_name (str): The name of the dataset section.
            subsection_name (Optional[str]): The name of the subsection, if any.
            field_names (list[str]): List of field labels to check.
            visible (Optional[bool]):
                - True → fields must be visible
                - False → fields must be not visible
                - None → visibility doesn't matter (just check presence)
        Returns:
            bool: True if all conditions are met; False otherwise.
        """
        logging.info(
            f"START: Checking fields in section '{section_name}' and subsection '{subsection_name}'"
        )

        section = (
            self.get_dataset_section(section_name)
            if subsection_name is None
            else self.get_dataset_subsection(section_name, subsection_name)
        )

        if section is None:
            raise ValueError(f"Dataset section '{section_name}' was not found.")

        label_elements = section.locator(".label").all()
        label_texts = [label.inner_text() for label in label_elements]
        normalized_labels = [
            normalize_label(label) for label in label_texts if normalize_label(label)
        ]

        def label_matches(idx: int) -> bool:
            """
            Checks if the label at the given index matches the visibility condition.
            Args:
                idx (int): The index of the label to check.
            Returns:
                bool: True if the label matches the visibility condition, False otherwise.
            """
            if visible is True:
                return label_elements[idx].is_visible()
            if visible is False:
                field_container = label_elements[idx].locator(
                    "xpath=ancestor::*[contains(@class, 'row') or contains(@class, 'field')][1]"
                )
                is_container_visible = field_container.is_visible()
                logging.info(
                    f"Label visible: {label_elements[idx].is_visible()}, "
                    f"Container visible: {is_container_visible} → Effective: {is_container_visible}"
                )
                return not is_container_visible
            return True  # visibility doesn't matter

        for field_name in field_names:
            field_normalized = normalize_label(field_name)
            match_found = False

            for i, label in enumerate(normalized_labels):
                if field_normalized in label and label_matches(i):
                    match_found = True
                    break

            logging.info(
                f"Checking for field '{field_name}' (visible={visible}) → Match found: {match_found}"
            )

            if not match_found:
                logging.info(
                    f"Field '{field_name}' not found or visibility check failed."
                )
                logging.info(f"Available labels: {normalized_labels}")
                return False

        logging.info("All fields matched.")
        return True

    def check_visibility_of_drug_type(
        self, drug_type: str, drug_number: int, visible: bool
    ) -> None:
        """
        Checks the visibility of the drug type input cell.
        Args:
            drug_type (str): The drug type to check
            drug_number (int): The number of the drug type cell to check.
            expected_text (str): The expected text content of the cell.
        Raises:
            AssertionError: If the visibility does not match the expectation.
        """
        locator = self.get_drug_type_locator(drug_type, drug_number)
        actual_visibility = locator.is_visible()
        assert actual_visibility == visible, (
            f"The {ordinal(drug_number)} {drug_type} drug type input cell visibility was {actual_visibility}, "
            f"expected {visible}"
        )
        logging.info(
            f"The {ordinal(drug_number)} {drug_type} drug type input cell is "
            f"{'visible' if actual_visibility else 'not visible'} as expected"
        )

    def check_visibility_of_drug_dose(
        self, drug_type: str, drug_number: int, visible: bool
    ) -> None:
        """
        Asserts the visibility of the drug dose input cell and logs the result.
        Args:
            drug_type (str): The drug type to check.
            drug_number (int): The number of the drug dose cell to check.
            visible (bool): True if the field should be visible, False if it should not.
        Raises:
            AssertionError: If the visibility does not match the expectation.
        """
        locator = self.get_drug_dose_locator(drug_type, drug_number)
        actual_visibility = locator.is_visible()
        assert actual_visibility == visible, (
            f"The {ordinal(drug_number)} {drug_type} drug dose input cell visibility was {actual_visibility}, "
            f"expected {visible}"
        )
        logging.info(
            f"The {ordinal(drug_number)} {drug_type} drug dose input cell is "
            f"{'visible' if actual_visibility else 'not visible'} as expected"
        )

    def assert_drug_type_text(
        self, drug_type: str, drug_number: int, expected_text: str
    ) -> None:
        """
        Asserts that the drug type input cell contains the expected text.
        Args:
            drug_type (str): The drug type to check
            drug_number (int): The number of the drug type cell to check.
            expected_text (str): The expected text content of the cell.
        Raises:
            AssertionError: If the actual text does not match the expected text.
        """
        locator = self.get_drug_type_locator(drug_type, drug_number)
        actual_text = locator.input_value().strip()
        logging.info(
            f"Drug type text for drug {drug_number}: "
            f"'{to_enum_name_or_value(actual_text)}' "
            f"(expected: '{to_enum_name_or_value(expected_text)}')"
        )
        assert (
            actual_text == expected_text
        ), f"Expected drug type text '{to_enum_name_or_value(expected_text)}' but found '{to_enum_name_or_value(actual_text)}'"

    def assert_drug_dose_text(
        self, drug_type: str, drug_number: int, expected_text: str
    ) -> None:
        """
        Asserts that the drug dose input cell contains the expected text.
        Args:
            drug_type (str): The drug type to check
            drug_number (int): The number of the drug dose cell to check.
            expected_text (str): The expected text content of the cell.
        Raises:
            AssertionError: If the actual text does not match the expected text.
        """
        locator = self.get_drug_dose_locator(drug_type, drug_number)
        actual_text = locator.input_value().strip()
        logging.info(
            f"Drug dose text for drug {drug_number}: '{actual_text}' (expected: '{expected_text}')"
        )
        assert (
            actual_text == expected_text
        ), f"Expected drug dose text '{expected_text}' but found '{actual_text}'"

    def get_drug_type_locator(self, drug_type: str, drug_number: int) -> Locator:
        """
        Returns the locator for the matching drug type and number
        Args:
            drug_type (str): The drug type to check
            drug_number (int): The number of the drug to check
        """
        if drug_type == self.bowel_preparation_administered_string:
            locator_prefix = "#UI_BOWEL_PREP_DRUG"
        elif drug_type == self.antibiotics_administered_string:
            locator_prefix = "#UI_ANTIBIOTIC"
        elif drug_type == self.other_drugs_administered_string:
            locator_prefix = "#UI_DRUG"
        return self.page.locator(f"{locator_prefix}{drug_number}")

    def get_drug_dose_locator(self, drug_type: str, drug_number: int) -> Locator:
        """
        Returns the locator for the matching drug type and number
        Args:
            drug_type (str): The drug type to check
            drug_number (int): The number of the drug to check
        """
        if drug_type == self.bowel_preparation_administered_string:
            locator_prefix = "#UI_BOWEL_PREP_DRUG_DOSE"
        elif drug_type == self.antibiotics_administered_string:
            locator_prefix = "#UI_ANTIBIOTIC_DOSE"
        elif drug_type == self.other_drugs_administered_string:
            locator_prefix = "#UI_DOSE"
        return self.page.locator(f"{locator_prefix}{drug_number}")

    def assert_drug_type_options(
        self, drug_type: str, drug_number: int, expected_values: list
    ) -> None:
        """
        Asserts that the options in the drug type dropdown are as expected.
        Args:
            drug_type (str): The drug type to check
            drug_number (int): The number of the drug to check
            expected_values (list): A list containing all the options expected
        """
        locator = self.get_drug_type_locator(drug_type, drug_number)
        actual_options = locator.locator("option").all_text_contents()
        actual_options = [
            opt.strip() for opt in actual_options
        ]  # Strip whitespace for safety

        missing = [val for val in expected_values if val not in actual_options]

        assert not missing, (
            f"Missing expected dropdown values for drug {drug_number} ({drug_type}): {missing}. "
            f"Actual options: {actual_options}"
        )

        logging.info(
            f"The dropdown for {drug_type} drug {drug_number} contains expected values: {expected_values}"
        )

    def assert_all_drug_information(
        self, drug_information: dict, drug_type_label: str
    ) -> None:
        """
        Loops through a dictionary of drug types/doses and calls the relevant assertion methods
        Args:
            drug_information (dict): A dictionary containing all drug types and dosages to assert
            drug_type_label (str): The type of drug to do the assertion against. E.g. 'Bowel Preparation Administered'
        """
        # Extract all numbers from keys like 'drug_doseX' or 'drug_typeX'
        drug_numbers = [
            int(match.group(1))
            for key in drug_information
            if (
                match := re.match(
                    r"(?:drug|other_drug|antibiotic_drug)_(?:dose|type)(\d+)", key
                )
            )
        ]

        if not drug_numbers:
            logging.warning("No drug_type or drug_dose entries found.")
            return

        max_drug_number = max(drug_numbers)

        for drug_index in range(1, max_drug_number + 1):
            drug_type = (
                drug_information.get(f"drug_type{drug_index}")
                or drug_information.get(f"other_drug_type{drug_index}")
                or drug_information.get(f"antibiotic_drug_type{drug_index}")
            )
            drug_dose = (
                drug_information.get(f"drug_dose{drug_index}")
                or drug_information.get(f"other_drug_dose{drug_index}")
                or drug_information.get(f"antibiotic_drug_dose{drug_index}")
            )

            if drug_type is not None:
                self.assert_drug_type_text(drug_type_label, drug_index, drug_type)

                # Match-case to assert drug dose unit
                match drug_type:
                    case (
                        DrugTypeOptions.KLEAN_PREP
                        | DrugTypeOptions.PICOLAX
                        | DrugTypeOptions.MOVIPREP
                        | DrugTypeOptions.CITRAMAG
                        | DrugTypeOptions.PHOSPHATE_ENEMA
                        | DrugTypeOptions.MICROLAX_ENEMA
                        | DrugTypeOptions.CITRAFLEET
                        | DrugTypeOptions.PLENVU
                    ):
                        expected_unit = "Sachet(s)"
                    case DrugTypeOptions.SENNA_LIQUID:
                        expected_unit = "5ml Bottle(s)"
                    case (
                        DrugTypeOptions.SENNA
                        | DrugTypeOptions.BISACODYL
                        | DrugTypeOptions.OSMOSPREP
                    ):
                        expected_unit = "Tablet(s)"
                    case DrugTypeOptions.MANNITOL:
                        expected_unit = "Litre(s)"
                    case (
                        DrugTypeOptions.GASTROGRAFIN
                        | DrugTypeOptions.FLEET_PHOSPHO_SODA
                    ):
                        expected_unit = "Mls Solution"
                    case (
                        DrugTypeOptions.OTHER
                        | AntibioticsAdministeredDrugTypeOptions.OTHER_ANTIBIOTIC
                    ):
                        expected_unit = ""
                    case (
                        AntibioticsAdministeredDrugTypeOptions.AMOXYCILLIN
                        | AntibioticsAdministeredDrugTypeOptions.CEFOTAXIME
                        | AntibioticsAdministeredDrugTypeOptions.VANCOMYCIN
                    ):
                        expected_unit = "g"
                    case (
                        AntibioticsAdministeredDrugTypeOptions.CIPROFLAXACIN
                        | AntibioticsAdministeredDrugTypeOptions.CO_AMOXICLAV
                        | AntibioticsAdministeredDrugTypeOptions.GENTAMICIN
                        | AntibioticsAdministeredDrugTypeOptions.METRONIDAZOLE
                        | AntibioticsAdministeredDrugTypeOptions.TEICOPLANIN
                        | OtherDrugsAdministeredDrugTypeOptions.BUSCOPAN
                        | OtherDrugsAdministeredDrugTypeOptions.DIAZEMULS
                        | OtherDrugsAdministeredDrugTypeOptions.GLUCAGON
                        | OtherDrugsAdministeredDrugTypeOptions.HYDROCORTISONE
                        | OtherDrugsAdministeredDrugTypeOptions.MEPTAZINOL
                        | OtherDrugsAdministeredDrugTypeOptions.MIDAZOLAM
                        | OtherDrugsAdministeredDrugTypeOptions.PETHIDINE
                        | OtherDrugsAdministeredDrugTypeOptions.PROPOFOL
                    ):
                        expected_unit = "mg"
                    case (
                        OtherDrugsAdministeredDrugTypeOptions.ALFENTANYL
                        | OtherDrugsAdministeredDrugTypeOptions.FENTANYL
                        | OtherDrugsAdministeredDrugTypeOptions.FLUMAZENIL
                        | OtherDrugsAdministeredDrugTypeOptions.NALOXONE
                    ):
                        expected_unit = "mcg"
                    case _:
                        expected_unit = None

                if expected_unit is not None:
                    self.assert_drug_dose_unit_text(
                        drug_type_label, drug_index, expected_unit
                    )

            if drug_dose is not None:
                self.assert_drug_dose_text(drug_type_label, drug_index, drug_dose)

    def get_drug_dose_unit_locator(self, drug_type: str, drug_number: int) -> Locator:
        """
        Returns the locator for the matching drug type and number
        Args:
            drug_type (str): The drug type to check
            drug_number (int): The number of the drug to check
        """
        if drug_type == self.bowel_preparation_administered_string:
            locator_prefix = "#spanBowelPrepDrugDosageUnit"
        elif drug_type == self.antibiotics_administered_string:
            locator_prefix = "#spanAntibioticDosageUnit"
        elif drug_type == self.other_drugs_administered_string:
            locator_prefix = "#spanDosageUnit"
        return self.page.locator(f"{locator_prefix}{drug_number}")

    def assert_drug_dose_unit_text(
        self, drug_type: str, drug_number: int, expected_text: str
    ) -> None:
        """
        Asserts that the drug dose unit contains the expected text.
        Args:
            drug_type (str): The drug type to check
            drug_number (int): The number of the drug dose cell to check.
            expected_text (str): The expected text content of the cell.
        Raises:
            AssertionError: If the actual text does not match the expected text.
        """
        locator = self.get_drug_dose_unit_locator(drug_type, drug_number)
        actual_text = locator.inner_text().strip()
        logging.info(
            f"Drug dose unit text for drug {drug_number}: '{actual_text}' (expected: '{expected_text}')"
        )
        assert (
            actual_text == expected_text
        ), f"Expected drug unit dose text '{expected_text}' but found '{actual_text}'"

    def assert_drug_dosage_unit_text(
        self, drug_type: str, drug_number: int, expected_text: str
    ) -> None:
        """
        Asserts that the drug dosage unit contains the expected text.

        Args:
            drug_type (str): The drug type to check
            drug_number (int): The number of the drug dosage unit cell to check.
            expected_text (str): The expected text content of the cell.

        Raises:
            AssertionError: If the actual text does not match the expected text.
        """
        locator = self.get_drug_dosage_text_locator(drug_type, drug_number)
        actual_text = locator.inner_text().strip()

        logging.info(
            f"Drug dosage unit text for drug {drug_number}: "
            f"'{actual_text}' (expected: '{expected_text}')"
        )

        assert actual_text == expected_text, (
            f"Expected drug dosage unit text '{expected_text}' "
            f"but found '{actual_text}'"
        )

    def get_drug_dosage_text_locator(self, drug_type: str, drug_number: int) -> Locator:
        """
        Returns the drug dosage text locator for the matching drug type and number
        Args:
            drug_type (str): The drug type to check
            drug_number (int): The number of the drug to check
        """
        if drug_type == self.bowel_preparation_administered_string:
            locator_prefix = "#HILITE_spanBowelPrepDrugDosageUnit"
        elif drug_type == self.antibiotics_administered_string:
            locator_prefix = "#HILITE_spanAntibioticDosageUnit"
        return self.page.locator(f"{locator_prefix}{drug_number}")


def normalize_label(text: str) -> str:
    """
    Normalizes a label by removing extra whitespace and converting to lowercase.
    Args:
        text (str): The label text to normalize.
    Returns:
        str: The normalized label text.
    """
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip().lower()


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
    GASTROGRAFIN = "200540~Mls Solution~204334"
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
    """Enum for Yes and No options"""

    YES = "17058"
    NO = "17059"


class YesNoDrugOptions(StrEnum):
    """Enum for Yes and No drug options"""

    YES = "17058"
    NO = "17059~~204341"


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
    BIOPSY = "17190~Suspicion of cancer"
    CHROMOSCOPY = "17198"
    HAEMOSTATIC_TECHNIQUE = "17194"
    SUBMUCOSAL_LIFT = "203005"
    TATTOOING = "17192"
    TISSUE_DESTRUCTION = "17191"


class PolypInterventionDeviceOptions(StrEnum):
    """Enum for polyp intervention device options"""

    HOT_SNARE = "17070"
    HOT_BIOPSY = "17071~En-bloc"
    COLD_SNARE = "17072"
    COLD_BIOPSY = "17073~En-bloc"
    ENDOSCOPIC_KNIFE = "17531"
    HOT_BIOPSY_FORCEPS = "17071~En-bloc"
    ARGON_BEAM = "17077"
    LASER = "17078"


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


class ReasonPathologyLostOptions(StrEnum):
    """Enum for reason pathology lost options"""

    LOST_IN_TRANSIT = "200561~~204337"
    DESTROYED_DURING_PROCESSING = "200562~~204337"


class PolypInterventionSuccessOptions(StrEnum):
    """Enum for polyp intervention success options"""

    SUCCESSFUL = "17200"
    UNSUCCESSFUL = "17201"


class PolypReasonLeftInSituOptions(StrEnum):
    """Enum for reasons a polyp was left in situ"""

    POLYP_TYPE = "200556"
    REQUIRES_ANOTHER_PROCEDURE = "200557"
    REQUIRES_SURGICAL_RESECTION = "200558"
    CANNOT_FIND_POLYP_ON_WITHDRAWAL = "200559"
    CLINICAL_DECISION_NOT_TO_EXCISE = "203082"


class AntibioticsAdministeredDrugTypeOptions(StrEnum):
    """Enum for antobiotics administered drug type options"""

    AMOXYCILLIN = "17941~g"
    CEFOTAXIME = "17950~g"
    CIPROFLAXACIN = "17945~mg"
    CO_AMOXICLAV = "17951~mg"
    GENTAMICIN = "17942~mg"
    METRONIDAZOLE = "17949~mg"
    TEICOPLANIN = "17944~mg"
    VANCOMYCIN = "17943~g"
    OTHER_ANTIBIOTIC = "305493"


class OtherDrugsAdministeredDrugTypeOptions(StrEnum):
    """Enum for other drugs administered drug type options"""

    ALFENTANYL = "200252~mcg"
    BUSCOPAN = "17133~mg"
    DIAZEMULS = "17959~mg"
    FENTANYL = "17958~mcg"
    FLUMAZENIL = "17134~mcg"
    GLUCAGON = "17940~mg"
    HYDROCORTISONE = "17527~mg"
    MEPTAZINOL = "200251~mg"
    MIDAZOLAM = "17135~mg"
    NALOXONE = "17136~mcg~204333"
    PETHIDINE = "17137~mg"
    PROPOFOL = "17960~mg"


class EndoscopeNotInsertedOptions(StrEnum):
    """Enum for why endoscope not inserted options"""

    CLINICAL_REASON_ON_PR = "200541~Abnormalities allowed"
    CONSENT_REFUSED = "200542"
    EQUIPMENT_FAILURE = "200544"
    NO_BOWEL_PREPERATION = "200543"
    PATIENT_UNSUITABLE = "200545"
    SERVICE_INTERRUPTION = "203000"
    SOLID_STOLL_ON_PR = "200546"
    UNSCHEDULED_ATTENDANCE_TIME = "203001"


class SedationOptions(StrEnum):
    """Enum for sedation options"""

    UNSEDATED = "18504~Read-only"
    AWAKE = "17324"
    DROWSY = "17325"
    ASLEEP_BUT_RESPONDING_TO_NAME = "17326"
    ASLEEP_BUT_RESPONDING_TO_TOUCH = "17327"
    ASLEEP_AND_UNRESPONSIVE = "17328"


class ExaminationQualityOptions(StrEnum):
    """Enum for examination quality options"""

    GOOD = "17016"
    ADEQUATE_FAIR = "17017"
    POOR = "17995~Enema down scope~204376"
    NOT_REPORTED = "202140"


class ScanPositionOptions(StrEnum):
    """Enum for number of scan positions"""

    SINGLE = "204373"
    DUAL = "204374"
    TRIPLE = "204375"
    NOT_REPORTED = "202140"


class ProcedureOutcomeOptions(StrEnum):
    """Enum for outcome at time of procedure"""

    LEAVE_DEPARTMENT = "17148~Complications are optional"
    UNPLANNED_ADMISSION = "17147~Complications are mandatory"


class SegmentalInadequacyOptions(StrEnum):
    """Enum for segmental inadequacy"""

    YES = "17058"
    NO = "17059~~307113"


class IntracolonicSummaryCodeOptions(StrEnum):
    """Enum for intracolonic summary code"""

    CX_INADEQUATE_STUDY = "203167~~204409,307112"
    C1_NORMAL_OR_SMALL_POLYPS = "203168"
    C2_POLYPS_6_9MM = "203169~~203178"
    C3A_POLYPS_1_9MM = "203170~~203178"
    C3B_POLYPS_GE_10MM = "203171~~203178"
    C3C_INDETERMINATE_STRICTURE = "203172"
    C4A_MANY_SMALL_POLYPS = "203173~~203178"
    C4B_MANY_POLYPS_GE_10MM = "203174~~203178"
    C5A_COLON_MASS_MALIGNANT = "203175~~203179"
    C5B_NO_TUMOUR_ADDITIONAL = "203176~~203179"
    NOT_REPORTED = "203177"


class ExtracolonicSummaryCodeOptions(StrEnum):
    """Enum for extracolonic summary code options"""

    E1_NORMAL_VARIANT = "204382"
    E2_INCIDENTAL_KNOWN = "204383"
    E3_INCOMPLETE_CHARACTERISATION = "204384"
    E4_IMPORTANT_REQUIRES_ACTION = "204385"
    E5_SIGNIFICANT_NEW_FINDING = "204386"
    NOT_REPORTED = "202140"


class TaggingAgentDrugAdministeredOptions(StrEnum):
    """Enum for tagging agent drug administered options"""

    YES = "17058~~204368"
    NO = "17059"
    NOT_REPORTED = "202140"


class AdditionalBowelPrepAdministeredOptions(str, Enum):
    YES = "17058~~204414"
    NO = "17059"
    NOT_REPORTED = "202140"


class IVContrastAdministeredOptions(StrEnum):
    """Enum for iv contrast administered options"""

    YES = "17058~~204367"
    NO = "17059~~204334"
    NOT_REPORTED = "202140"


class IVBuscopanAdministeredOptions(StrEnum):
    """Enum for Yes/No options specific to IV Buscopan Administered fields"""

    YES = "17058~~204365"
    NO = "17059~~204366"
    NOT_REPORTED = "202140"


class OpticalDiagnosisOptions(StrEnum):
    """Enum for Optical Diagnosis options"""

    ADEMONA = "17299~Sub Type Applicable"
    SERRATED_HYPERPLASTIC_SSL = "305742"
    OTHER_POLYP_NON_NEOPLASTIC = "305743"
    OTHER_POLYP_NEOPLASTIC = "305744"


class PolypInterventionRetrievedOptions(StrEnum):
    """Enum for Polyp Intervention Retrieved options"""

    YES = "17058"
    NO = "17059"
    NO_RESECT_AND_DISCARD = "305738"


class OpticalDiagnosisConfidenceOptions(StrEnum):
    """Enum for Optical Diagnosis Condifence options"""

    HIGH = "17752"
    LOW = "305746"


# Registry of all known Enums to search when matching string values
ALL_ENUMS: List[type[Enum]] = [
    obj
    for obj in globals().values()
    if (
        isinstance(obj, type)
        and issubclass(obj, Enum)
        and obj is not Enum
        and obj is not StrEnum  # Exclude only the base classes, not subclasses
    )
]


def to_enum_name_or_value(val: Any) -> Union[str, Any]:
    """
    Convert an Enum member or matching string value to its Enum name.

    If the input is:
    - An Enum member → returns the `.name` (e.g., "KLEAN_PREP")
    - A string matching any Enum value in ALL_ENUMS → returns that member's `.name`
    - Anything else → returns the value unchanged

    Args:
        val (Any): The value to convert. Can be an Enum member, a string,
                or any other type.

    Returns:
        Union[str, Any]: The Enum name (string) if matched, otherwise the original value.
    """
    # Directly handle Enum instances
    if isinstance(val, Enum):
        return val.name

    # Handle strings that match known Enum values
    if isinstance(val, str):
        for enum_cls in ALL_ENUMS:
            try:
                return enum_cls(val).name
            except ValueError:
                continue

    # Fallback: return unchanged
    return val


def ordinal(n: int) -> str:
    """
    Converts an integer to its ordinal representation (e.g., 1 -> '1st', 2 -> '2nd').
    """
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"
