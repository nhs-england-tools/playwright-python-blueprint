from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from datetime import datetime
from utils.calendar_picker import CalendarPicker


class BatchListPage(BasePage):
    """Batch List Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Batch List - page filters
        self.id_filter = self.page.locator("#batchIdFilter")
        self.type_filter = self.page.locator("#batchTypeFilter")
        self.original_filter = self.page.locator("#originalBatchIdFilter")
        self.event_code_filter = self.page.locator("#eventCodeFilter")
        self.description_filter = self.page.locator("#eventDescriptionFilter")
        self.batch_split_by_filter = self.page.locator("#splitByFilter")
        self.screening_centre_filter = self.page.locator("#screeningCentreFilter")
        self.count_filter = self.page.locator("#countFilter")
        self.table_data = self.page.locator("td")
        self.batch_successfully_archived_msg = self.page.locator(
            'text="Batch Successfully Archived and Printed"'
        )
        self.deadline_calendar_picker = self.page.locator("i")
        self.deadline_date_filter = self.page.get_by_role("cell", name="").get_by_role(
            "textbox"
        )
        self.deadline_date_filter_with_input = self.page.locator(
            "input.form-control.filter.filtering"
        )
        self.deadline_date_clear_button = self.page.get_by_role("cell", name="Clear")

    def verify_batch_list_page_title(self, text) -> None:
        """Verify the Batch List page title is displayed as expected"""
        self.bowel_cancer_screening_page_title_contains_text(text)

    def verify_table_data(self, value) -> None:
        """Verify the table data is displayed as expected"""
        expect(self.table_data.filter(has_text=value)).to_be_visible()

    def enter_id_filter(self, search_text: str) -> None:
        """Enter text in the ID filter and press Enter"""
        self.id_filter.fill(search_text)
        self.id_filter.press("Enter")

    def enter_type_filter(self, search_text: str) -> None:
        """Enter text in the Type filter and press Enter"""
        self.type_filter.fill(search_text)
        self.type_filter.press("Enter")

    def enter_original_filter(self, search_text: str) -> None:
        """Enter text in the Original filter and press Enter"""
        self.original_filter.fill(search_text)
        self.original_filter.press("Enter")

    def enter_event_code_filter(self, search_text: str) -> None:
        """Enter text in the Event Code filter and press Enter"""
        self.event_code_filter.fill(search_text)
        self.event_code_filter.press("Enter")

    def enter_description_filter(self, search_text: str) -> None:
        """Enter text in the Description filter and press Enter"""
        self.description_filter.fill(search_text)
        self.description_filter.press("Enter")

    def enter_batch_split_by_filter(self, search_text: str) -> None:
        """Enter text in the 'Batch Split By' filter and press Enter"""
        self.batch_split_by_filter.fill(search_text)
        self.batch_split_by_filter.press("Enter")

    def enter_screening_centre_filter(self, search_text: str) -> None:
        """Enter text in the Screening Centre filter and press Enter"""
        self.screening_centre_filter.fill(search_text)
        self.screening_centre_filter.press("Enter")

    def enter_count_filter(self, search_text: str) -> None:
        """Enter text in the Count filter and press Enter"""
        self.count_filter.fill(search_text)
        self.count_filter.press("Enter")

    def enter_deadline_date_filter(self, date: datetime) -> None:
        """Enter a date in the Deadline Date filter and press Enter"""
        self.click(self.deadline_calendar_picker)
        CalendarPicker(self.page).v2_calendar_picker(date)

    def clear_deadline_filter_date(self) -> None:
        """Clear the date in the Deadline Date filter"""
        self.click(self.deadline_calendar_picker)
        self.click(self.deadline_date_clear_button)

    def verify_deadline_date_filter_input(self, expected_text: str) -> None:
        expect(self.deadline_date_filter_with_input).to_have_value(expected_text)


class ActiveBatchListPage(BatchListPage):
    """Active Batch List Page locators, and methods for interacting with the Active Batch List page"""

    def __init__(self, page):
        super().__init__(page)


class ArchivedBatchListPage(BatchListPage):
    """Archived Batch List Page locators, and methods for interacting with the Archived Batch List page"""

    def __init__(self, page):
        super().__init__(page)
