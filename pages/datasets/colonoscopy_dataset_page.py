from playwright.sync_api import Page
from pages.base_page import BasePage
from enum import Enum


class ColonoscopyDatasetsPage(BasePage):
    """Colonoscopy Datasets Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # Colonoscopy datasets page locators
        self.save_dataset_button = self.page.locator(
            "#UI_DIV_BUTTON_SAVE1"
        ).get_by_role("button", name="Save Dataset")

        self.select_asa_grade_dropdown = self.page.get_by_label("ASA Grade")

        self.select_fit_for_colonoscopy_dropdown = self.page.get_by_label(
            "Fit for Colonoscopy (SSP)"
        )

        self.dataset_complete_radio_button_yes = self.page.get_by_role(
            "radio", name="Yes"
        )

        self.dataset_complete_radio_button_no = self.page.get_by_role(
            "radio", name="No"
        )

    def save_dataset(self) -> None:
        """Clicks the Save Dataset button on the colonoscopy datasets page."""
        self.click(self.save_dataset_button)

    def select_asa_grade_option(self, option: str) -> None:
        """
        This method is designed to select a specific grade option from the colonoscopy dataset page, ASA Grade dropdown menu.
        Args:
            option (str): The ASA grade option to be selected. This should be a string that matches one of the available options in the dropdown menu.
                Valid options are: "FIT", "RELEVANT_DISEASE", "UNABLE_TO_ASSESS", RESTRICTIVE_DISEASE, "LIFE_THREATENING_DISEASE", "MORIBUND", "NOT_APPLICABLE", or "NOT_KNOWN".
        Returns:
            None
        """
        self.select_asa_grade_dropdown.select_option(option)

    def select_fit_for_colonoscopy_option(self, option: str) -> None:
        """
        This method is designed to select a specific option from the colonoscopy dataset page, Fit for Colonoscopy (SSP) dropdown menu.
        Args:
            option (str): The option to be selected. This should be a string that matches one of the available options in the dropdown menu.
                Valid options are: "YES", "NO", or "UNABLE_TO_ASSESS".
        Returns:
            None
        """
        self.select_fit_for_colonoscopy_dropdown.select_option(option)

    def click_dataset_complete_radio_button_yes(self) -> None:
        """Clicks the 'Yes' radio button for the dataset complete option."""
        self.dataset_complete_radio_button_yes.check()

    def click_dataset_complete_radio_button_no(self) -> None:
        """Clicks the 'No' radio button for the dataset complete option."""
        self.dataset_complete_radio_button_no.check()


class AsaGradeOptions(Enum):
    FIT = "17009"
    RELEVANT_DISEASE = "17010"
    RESTRICTIVE_DISEASE = "17011"
    LIFE_THREATENING_DISEASE = "17012"
    MORIBUND = "17013"
    NOT_APPLICABLE = "17014"
    NOT_KNOWN = "17015"


class FitForColonoscopySspOptions(Enum):
    YES = "17058"
    NO = "17059"
    UNABLE_TO_ASSESS = "17954"
