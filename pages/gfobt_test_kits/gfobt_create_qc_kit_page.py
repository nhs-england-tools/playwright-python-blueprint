from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from enum import Enum


class CreateQCKitPage(BasePage):
    """Create QC Kit page locators and methods for interacting with the page."""

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
        self.kit_has_saved = self.page.locator("th")

    def verify_create_qc_kit_title(self) -> None:
        """Verify the Create QC Kit page title contains text "Create QC Kit"."""
        self.bowel_cancer_screening_page_title_contains_text(
            "Create QC Kit"
        )

    def go_to_reading1dropdown(self, option: str) -> None:
        """Selects a given option from the reading 1 dropdown."""
        self.reading1dropdown.select_option(option)

    def go_to_reading2dropdown(self, option: str) -> None:
        """Selects a given option from the reading 2 dropdown."""
        self.reading2dropdown.select_option(option)

    def go_to_reading3dropdown(self, option: str) -> None:
        """Selects a given option from the reading 3 dropdown."""
        self.reading3dropdown.select_option(option)

    def go_to_reading4dropdown(self, option: str) -> None:
        """Selects a given option from the reading 4 dropdown."""
        self.reading4dropdown.select_option(option)

    def go_to_reading5dropdown(self, option: str) -> None:
        """Selects a given option from the reading 5 dropdown."""
        self.reading5dropdown.select_option(option)

    def go_to_reading6dropdown(self, option: str) -> None:
        """Selects a given option from the reading 6 dropdown."""
        self.reading6dropdown.select_option(option)

    def go_to_save_kit(self) -> None:
        """Clicks the Save Kit button."""
        self.click(self.save_kit)

    def verify_kit_has_saved(self) -> None:
        """Verify the kit has saved by checking the page contains the text "A quality control kit has been created with the following values:"."""
        expect(self.kit_has_saved).to_contain_text(
            "A quality control kit has been created with the following values:"
        )


class ReadingDropdownOptions(Enum):
    """Enum for the 'Create QC Kit Page' reading dropdown options."""

    NEGATIVE = "NEGATIVE"
    POSITIVE = "POSITIVE"
    UNUSED = "UNUSED"
