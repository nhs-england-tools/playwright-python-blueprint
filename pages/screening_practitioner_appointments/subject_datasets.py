from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from enum import Enum


class SubjectDatasets(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self.show_dataset_button = self.page.get_by_role("link", name="Show Dataset")

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

    def click_show_datasets(self) -> None:
        self.click(self.show_dataset_button)

    def save_dataset(self) -> None:
        self.click(self.save_dataset_button)

    def select_asa_grade_option(self, option: str) -> None:
        self.select_asa_grade_dropdowen.select_option(option)

    def select_fit_for_colonoscopy_option(self, option: str) -> None:
        self.select_fit_for_colonoscopy_dropdown.select_option(option)

    def click_dataset_complete_radio_button_yes(self) -> None:
        self.dataset_complete_radio_button_yes.check()

    def click_dataset_complete_radio_button_no(self) -> None:
        self.dataset_complete_radio_button_no.check()


class AsaGradeOptions(Enum):
    FIT = "17009"


class FitForColonoscopySspOptions(Enum):
    YES = "17058"
