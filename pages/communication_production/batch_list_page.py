from playwright.sync_api import Page, expect, Locator
from pages.base_page import BasePage
from datetime import datetime
from pages.communication_production.communications_production_page import (
    CommunicationsProductionPage,
)
from utils.calendar_picker import CalendarPicker
from utils.table_util import TableUtils
import logging

BATCH_LIST_SELECTOR = "table#batchList"


class BatchListPage(BasePage):
    """Shared base class for both Active and Archived Batch List Pages."""

    def __init__(self, page: Page, table_selector: str = BATCH_LIST_SELECTOR):
        super().__init__(page)
        self.page = page
        self.table_selector = table_selector

        # Common filters
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

    def assert_column_present(self, column_name: str) -> None:
        """Asserts that the specified column is present in the table header."""
        headers = list(
            TableUtils(self.page, self.table_selector).get_table_headers().values()
        )
        assert (
            column_name in headers
        ), f"Column '{column_name}' not found in table headers"

    def assert_column_sortable(self, column_name: str) -> None:
        """Asserts that the specified column is marked as sortable in the UI."""
        sort_locator = self.page.locator(
            f"{self.table_selector} thead tr:first-child th span.dt-column-title",
            has_text=column_name,
        )
        assert (
            sort_locator.count() > 0
        ), f"Sortable header not found for column '{column_name}'"
        assert (
            sort_locator.first.get_attribute("role") == "button"
        ), f"Column '{column_name}' is not sortable"

    def assert_column_filterable(self, column_name: str) -> None:
        """Asserts that the specified column has a filter control in the second header row."""
        table = TableUtils(self.page, self.table_selector)
        column_index = (
            table.get_column_index(column_name) - 1
        )  # Convert 1-based to 0-based

        filter_locator = (
            self.page.locator(f"{self.table_selector} thead tr:nth-child(2) th")
            .nth(column_index)
            .locator("input, select, div.input-group")
        )
        assert (
            filter_locator.count() > 0
        ), f"Filter control not found for column '{column_name}'"

    def assert_batch_table_visible(self) -> None:
        """Asserts that the batch list table is present and rendered."""
        expect(self.page.locator(self.table_selector)).to_be_visible()

    def verify_batch_list_page_title(self, text) -> None:
        """Verify the Batch List page title is displayed as expected."""
        self.bowel_cancer_screening_page_title_contains_text(text)

    def verify_table_data(self, value) -> None:
        """Verify the table data is displayed as expected."""
        expect(self.table_data.filter(has_text=value)).to_be_visible()

    # Shared filter entry methods
    def enter_id_filter(self, search_text: str) -> None:
        self.id_filter.fill(search_text)
        self.id_filter.press("Enter")

    def enter_type_filter(self, option_text: str) -> None:
        """
        Selects the given option from the 'Type' filter dropdown.

        Args:
            option_text (str): The visible label of the option to select (e.g. "Original", "All")
        """
        self.type_filter.select_option(label=option_text)
        logging.info(f"[FILTER] Type filter set to '{option_text}'")

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
        """Verifies that the Deadline Date filter input has the expected value."""
        expect(self.deadline_date_filter_with_input).to_have_value(expected_text)

    def open_letter_batch(
        self,
        batch_type: str = "",
        status: str = "",
        level: str = "",
        description: str = "",
    ) -> None:
        """
        Finds and opens the batch row based on non-empty filters.

        Args:
            batch_type (str): Optional filter for batch type (e.g., "Original").
            status (str): Optional filter for batch status (e.g., "Open").
            level (str): Optional filter for batch level (e.g., "S1").
            description (str): Optional filter for batch description (e.g., "Pre-invitation (FIT)").
        """
        row_locator = self.page.locator(f"{self.table_selector} tbody tr")

        if batch_type:
            row_locator = row_locator.filter(
                has=self.page.locator("td", has_text=batch_type)
            )
        if status:
            row_locator = row_locator.filter(
                has=self.page.locator("td", has_text=status)
            )
        if level:
            row_locator = row_locator.filter(
                has=self.page.locator("td", has_text=level)
            )
        if description:
            row_locator = row_locator.filter(
                has=self.page.locator("td", has_text=description)
            )

        row = row_locator.first
        view_link = row.locator("a").first
        expect(view_link).to_be_visible()
        view_link.click()

    def select_first_batch_row(self, table_selector: str, timeout_ms: int = 0) -> None:
        """
        Clicks the first batch link in the specified batch list table.

        Args:
            table_selector (str): CSS selector for the table (e.g., "table#batchList").
            timeout_ms (int): Optional timeout to wait before interaction (default: 0).
        """
        first_link = self.page.locator(f"{table_selector} tbody tr td.id a").first
        if timeout_ms > 0:
            first_link.wait_for(timeout=timeout_ms)

        assert (
            first_link.count() > 0
        ), f"No batch links found in table '{table_selector}'"
        first_link.click()

    def navigate_to_active_batch_list_page(self) -> None:
        """
        Navigates to the active batch list page from anywhere in bcss (providing the main menu link is displayed).
        """
        self.click_main_menu_link()
        self.go_to_communications_production_page()
        CommunicationsProductionPage(self.page).go_to_active_batch_list_page()


class ActiveBatchListPage(BatchListPage):
    """Active Batch List Page-specific methods."""

    def __init__(self, page: Page):
        super().__init__(page, table_selector=BATCH_LIST_SELECTOR)

    def select_first_active_batch(self) -> None:
        """Selects the first active batch in the batch list table."""
        self.select_first_batch_row(self.table_selector, timeout_ms=10000)

    def is_batch_present(self, batch_type: str) -> bool:
        """Checks if a batch of the given type exists in the active batch list.
        Args:
            batch_type (str): The type of the batch to check for e.g. "S1 - Pre-invitation (FIT)"
        """
        locator = self.page.locator(
            f"{self.table_selector} tbody tr td", has_text=batch_type
        )
        return locator.count() > 0

    def get_open_original_batch_row(self) -> Locator | None:
        """
        Returns the first table row where:
        - The 'Type' column contains 'Original'
        - The 'Status' column contains 'Open'

        Returns:
            Locator of the matching <tr> element, or None if not found.
        """
        table = TableUtils(self.page, BATCH_LIST_SELECTOR)
        row_count = table.get_row_count()

        for row in range(row_count):
            row_data = table.get_row_data_with_headers(row)
            if (
                row_data.get("Type", "").strip() == "Original"
                and row_data.get("Status", "").strip() == "Open"
            ):
                return table.pick_row(row)
        return None

    def assert_s83f_batch_present(self) -> None:
        self.enter_type_filter("Original")
        self.enter_event_code_filter("S83")
        self.enter_description_filter("Invitation & Test Kit (Self-referral) (FIT)")
        expect(
            self.table_data.filter(
                has_text="Invitation & Test Kit (Self-referral) (FIT)"
            )
        ).to_be_visible()


class ArchivedBatchListPage(BatchListPage):
    """Archived Batch List Page-specific setup."""

    def __init__(self, page: Page):
        super().__init__(page, table_selector=BATCH_LIST_SELECTOR)

    def select_first_archived_batch(self) -> None:
        """Selects the first archived batch in the batch list table."""
        self.select_first_batch_row("table#batchList", timeout_ms=10000)

    def get_archived_batch_row(
        self, batch_type: str, event_code: str, description: str
    ) -> Locator | None:
        """
        Returns the first archived batch row matching the specified Type, Event Code, and Description.
        Assumes columns appear in the following order:
        1. Batch ID
        2. Type
        3. Event Code
        4. Description
        5+ ...

        Args:
            batch_type (str): The target value in the 'Type' column (e.g., 'Original').
            event_code (str): The target value in the 'Event Code' column (e.g., 'S1').
            description (str): The target text in the 'Description' column (e.g., 'Pre-invitation (FIT)').

        Returns:
            Locator: The first <tr> element matching all criteria, or None if not found.
        """
        rows = self.page.locator(f"{self.table_selector} tbody tr")
        row_count = rows.count()
        if row_count == 0:
            return None

        for row in range(row_count):
            row = rows.nth(row)

            try:
                type_text = row.locator("td").nth(1).inner_text().strip()
                event_code_text = row.locator("td").nth(4).inner_text().strip()
                description_text = row.locator("td").nth(5).inner_text().strip()

                if (
                    batch_type.lower() in type_text.lower()
                    and event_code.lower() in event_code_text.lower()
                    and description.lower() in description_text.lower()
                ):
                    return row
            except IndexError:
                return None


class LetterBatchDetailsPage(BasePage):
    """Page object for the Letter Batch Details view."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.letter_table = self.page.locator("table#letterBatchDetails")

    def assert_letter_component_present(self, letter_type: str, format: str) -> None:
        """
        Asserts that a letter component with the given type and format is listed.
        This version works with div-based structures, not tables.

        Args:
            letter_type (str): Visible component description
            format (str): File format label (e.g., "PDF-A4-V03", "FIT-KIT-CSV")
        """
        descriptions = self.page.locator("div.letterDescription")
        formats = self.page.locator("div.letterFormat")
        match_found = False

        for i in range(min(descriptions.count(), formats.count())):
            if (
                letter_type.lower() in descriptions.nth(i).inner_text().lower()
                and format.lower() in formats.nth(i).inner_text().lower()
            ):
                match_found = True
                break

        assert (
            match_found
        ), f"Letter type '{letter_type}' with format '{format}' not found"

    def get_first_subject_nhs_number(self) -> str:
        """
        Retrieves the NHS number of the first subject listed in the letter batch details table.

        Returns:
            str: The NHS number of the subject.
        """
        table_utils = TableUtils(self.page, "table#letterBatchDetails")
        row_data = table_utils.get_row_data_with_headers(0)  # First row (0-based index)

        nhs_number = row_data.get("NHS Number")
        if not nhs_number:
            raise RuntimeError(
                "NHS Number not found in the first row of the letter batch table"
            )

        logging.info(f"Retrieved NHS number from batch: {nhs_number}")
        return nhs_number
