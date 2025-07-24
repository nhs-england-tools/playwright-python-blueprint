from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.table_util import TableUtils

DISPLAY_RS_SELECTOR = "#displayRS"


class LetterLibraryIndexPage(BasePage):
    """Letter Library Index Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.table_utils = TableUtils(self.page, DISPLAY_RS_SELECTOR)
        # Letter Library Index - page locators, methods

        self.letter_library_index_table = self.page.locator(DISPLAY_RS_SELECTOR)
        self.define_supplementary_letter_button = self.page.locator(
            "input.HeaderButtons[value='Define Supplementary Letter']"
        )
        self.letter_description_input = self.page.locator('input[name="A_C_LETT_DESC"]')
        self.destination_dropdown = self.page.locator("#A_C_DESTINATION_ID")
        self.priority_dropdown = self.page.locator("#A_C_PRIORITY_ID")
        self.signatory_input = self.page.locator("#A_C_SIGNATORY")
        self.job_title_input = self.page.locator("#A_C_JOB_TITLE")
        self.paragraph_input = self.page.locator("#A_C_PARAGRAPH_1")
        self.save_button = self.page.get_by_role("button", name="Save")
        self.event_code_input = self.page.get_by_role(
            "textbox", name="Enter text to filter the list"
        )

    def verify_letter_library_index_title(self) -> None:
        """Verify the Letter Library Index page title is displayed as expected"""
        self.bowel_cancer_screening_page_title_contains_text("Letter Library Index")

    def filter_by_letters_group(self, group_name: str) -> None:
        """
        Selects a letter group from the Letter Type dropdown on the Letter Library Index page.
        Triggers the postback and waits for the page to update.

        Args:
            group_name (str): Visible label of the desired letter group. Must be one of:
                - 'Discharge Letters (Patient)'
                - 'Discharge Letters (GP)'
                - 'Discharge Notification Cards To GP Practice'
                - '30 Day Questionnaire'
                - 'Surveillance Selection'
                - 'Invitation Letters'
                - 'MDT Referral Letter to GP'
                - 'Practitioner Clinic Letters'
                - 'Reminder Letters'
                - 'Result Letters (Patient)'
                - 'Result Communications (GP)'
                - 'Retest Letters'
                - 'Supplementary Letters'
                - 'Bowel Scope Hub Letters'
                - 'Genetic Service Letters'
        """
        dropdown = self.page.locator("#selLetterType")
        expect(dropdown).to_be_visible()

        # Select the option by its visible label
        dropdown.select_option(label=group_name)

        # Wait for the page to reload—this form triggers a postback
        self.page.wait_for_load_state("load")

    def filter_by_event_code(self, event_code: str) -> None:
        """
        Filters the letter library index by event code using the textbox input.

        Args:
            event_code (str): The event code to filter the list (e.g., 'S1')
        """
        expect(self.event_code_input).to_be_visible()
        self.event_code_input.click()
        self.event_code_input.fill(event_code)
        self.event_code_input.press("Enter")

    def click_first_letter_code_link_in_table(self) -> None:
        """Clicks the first link from the Letter Library Index table."""
        self.table_utils.click_first_link_in_column("Code")

    def click_define_supplementary_letter_button(self) -> None:
        """
        Clicks the 'Define Supplementary Letter' button

        Raises:
            AssertionError: If the button is not visible or interactive
        """
        button = self.define_supplementary_letter_button
        expect(button).to_be_visible()
        button.click()

    def define_supplementary_letter(
        self,
        description: str = "Define Letter",
        destination_id: str = "12057",
        priority_id: str = "12016",
        signatory: str = "signatory",
        job_title: str = "job title",
        paragraph_text: str = "body text",
    ) -> None:
        """
        Fills out the form to define a supplementary letter and confirms save via modal.

        Args:
            description (str): Letter description
            destination_id (str): Dropdown option for destination
            priority_id (str): Dropdown option for priority
            signatory (str): Signatory name
            job_title (str): Signatory's job title
            paragraph_text (str): Main body text of the letter
        """
        self.letter_description_input.fill(description)
        self.destination_dropdown.select_option(destination_id)
        self.priority_dropdown.select_option(priority_id)
        self.signatory_input.fill(signatory)
        self.job_title_input.fill(job_title)
        self.paragraph_input.fill(paragraph_text)

        # Save and accept dialog safely
        self.safe_accept_dialog(self.save_button)


class LetterDefinitionDetailPage(BasePage):
    """Page object for the Letter Definition detail view"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # Locators for each letter definition setting
        self.definition_table = self.page.locator("table#displayRS")
        self.current_version_label = self.page.get_by_text(
            "Current Version", exact=True
        )

    def assert_definition_setting(self, field_name: str, expected_value: str) -> None:
        """
        Asserts that a specific letter setting matches the expected value.

        Args:
            field_name (str): The label text (e.g., "Description")
            expected_value (str): The expected value shown beside the label
        """
        label_cell = self.page.locator("td.screenTableLabelCell", has_text=field_name)
        assert (
            label_cell.count() > 0
        ), f"[ASSERTION FAILED] Field label '{field_name}' not found"

        # The label is always followed by its corresponding input/value cell
        value_cell = label_cell.nth(0).locator("xpath=following-sibling::td[1]")
        actual_value = value_cell.inner_text().strip()

        assert (
            actual_value == expected_value
        ), f"[ASSERTION FAILED] For field '{field_name}', expected '{expected_value}', got '{actual_value}'"

    def has_current_version(self) -> bool:
        """
        Checks whether a version row exists with 'Current' as the type.

        Returns:
            bool: True if a current version row is present, False otherwise
        """
        version_table = self.page.locator("table#displayRS")
        current_row = (
            version_table.locator("tr")
            .filter(has=self.page.locator("td", has_text="Current"))
            .first
        )

        return current_row.count() > 0
