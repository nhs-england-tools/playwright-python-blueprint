from playwright.sync_api import Page,expect
from pages.base_page import BasePage
from enum import Enum

class CreateQCKit(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self.create_qc_kit_title = self.page.locator("#ntshPageTitle")
        # Reading dropdown locators
        self.reading1dropdown = self.page.locator("#A_C_Reading_999_0_0")
        self.reading2dropdown = self.page.locator("#A_C_Reading_999_0_1")
        self.reading3dropdown = self.page.locator("#A_C_Reading_999_1_0")
        self.reading4dropdown = self.page.locator("#A_C_Reading_999_1_1")
        self.reading5dropdown = self.page.locator("#A_C_Reading_999_2_0")
        self.reading6dropdown = self.page.locator("#A_C_Reading_999_2_1")
        self.save_kit = self.page.get_by_role("button", name="Save Kit")
        self.kit_has_saved=self.page.locator("th")

    def verify_create_qc_kit_title(self) -> None:
        expect(self.create_qc_kit_title).to_contain_text("Create QC Kit")

    def go_to_reading1dropdown(self, option: str)-> None:
        self.reading1dropdown.select_option(option)

    def go_to_reading2dropdown(self, option: str)-> None:
        self.reading2dropdown.select_option(option)

    def go_to_reading3dropdown(self, option: str)-> None:
        self.reading3dropdown.select_option(option)

    def go_to_reading4dropdown(self, option: str)-> None:
        self.reading4dropdown.select_option(option)

    def go_to_reading5dropdown(self, option: str)-> None:
        self.reading5dropdown.select_option(option)

    def go_to_reading6dropdown(self, option: str)-> None:
        self.reading6dropdown.select_option(option)

    def go_to_save_kit(self)-> None:
        self.click(self.save_kit)

    def verify_kit_has_saved(self) -> None:
        expect(self.kit_has_saved).to_contain_text("A quality control kit has been created with the following values:")

class ReadingDropdownOptions(Enum):
    NEGATIVE = "NEGATIVE"
    POSITIVE = "POSITIVE"
    UNUSED = "UNUSED"
