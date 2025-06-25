import logging
from datetime import datetime
from secrets import randbelow
from playwright.sync_api import Page, expect, Locator

logger = logging.getLogger(__name__)


class TableUtils:
    """
    A utility class providing functionality around tables in BS-Select.
    """

    def __init__(self, page: Page, table_locator: str) -> None:
        """
        Initializer for TableUtils.

        Args:
            page (playwright.sync_api.Page): The page the table is on.
            table_locator (str): The locator value to use to find the table.

        Returns:
            A TableUtils object ready to use.
        """
        self.page = page
        self.table_id = table_locator

    def _format_inner_text(self, data: str) -> dict:
        """
        This formats the inner text of a row to make it easier to manage

        Args:
            data (str): The .inner_text() of a table row.

        Returns:
            A dict with each column item from the row identified with its position.
        """
        dict_to_return = {}
        split_rows = data.split("\t")
        pos = 1
        for item in split_rows:
            dict_to_return[pos] = item
            pos += 1
        return dict_to_return

    def get_table_headers(self) -> dict:
        """
        This retrieves the headers from the table.

        Returns:
            A dict with each column item from the header row identified with its position.
        """
        headers = self.page.locator(f"{self.table_id} > thead tr").nth(0).inner_text()
        return self._format_inner_text(headers)

    def get_row_count(self) -> int:
        """
        This returns the total rows visible on the table (on the screen currently)

        Returns:
            An int with the total row count.
        """
        return self.page.locator(f"{self.table_id} > tbody tr").count()

    def pick_row(self, row_number: int) -> Locator:
        """
        This picks a selected row from table

        Args:
            row_id (str): The row number of the row to select.

        Returns:
            A playwright.sync_api.Locator with the row object.
        """
        return self.page.locator(f"{self.table_id} > tbody tr").nth(row_number)

    def pick_random_row(self) -> Locator:
        """
        This picks a random row from the visible rows in the table (full row)

        Returns:
            A playwright.sync_api.Locator with the row object.
        """
        return self.page.locator(f"{self.table_id} > tbody tr").nth(
            randbelow(self.get_row_count())
        )

    def pick_random_row_number(self) -> int:
        """
        This picks a random row from the table in BS-Select and returns its position

        Returns:
            An int representing a random row on the table.
        """
        return randbelow(self.get_row_count())

    def get_row_data_with_headers(self, row_number: int) -> dict:
        """
        This picks a selected row from table

        Args:
            row_number (str): The row number of the row to select.

        Returns:
            A dict object with keys representing the headers, and values representing the row contents.
        """
        headers = self.get_table_headers()
        row_data = self._format_inner_text(
            self.page.locator(f"{self.table_id} > tbody tr")
            .nth(row_number)
            .inner_text()
        )
        results = {}

        for key in headers:
            results[headers[key]] = row_data[key]

        return results

    def get_full_table_with_headers(self) -> dict:
        """
        This returns the full table as a dict of rows, with each entry having a header key / value pair.
        NOTE: The row count starts from 1 to represent the first row, not 0.

        Returns:
            A dict object with keys representing the rows, with values being a dict representing a header key / column value pair.
        """
        full_results = {}
        for row in range(self.get_row_count()):
            full_results[row + 1] = self.get_row_data_with_headers(row)
        return full_results

    def wait_for_table_to_populate(self) -> None:
        """
        This checks that the following phrases are no longer present in the body of the table:
        - "Waiting for typing to finish..."
        - "Searching..."
        """
        expect(self.page.locator(self.table_id)).not_to_contain_text(
            "Waiting for typing to finish..."
        )
        expect(self.page.locator(self.table_id)).not_to_contain_text(
            "Searching...", timeout=10000
        )

    def get_all_table_data(self, column_index: int) -> list[str]:
        """Get all data from a column across all pages"""
        all_data = []

        while True:
            # Get data from current page
            page_data = self.page.locator(f'tbody tr td:nth-child({column_index})').all_text_contents()
            all_data.extend(page_data)

            # Check if there's a next page
            next_button = self.page.locator(f'{self.table_id} li.paginate_button.next')
            is_disabled = "disabled" in next_button.get_attribute("class").split()
            if next_button.count() > 0 and not is_disabled:
                next_button.locator('a').click()
                self.page.wait_for_timeout(1500)  # Wait for page load
            else:
                break

        return all_data

    def get_current_page_data(self, column_index) -> list[str]:
        """Get data from current page only"""
        return self.page.locator(f'tbody tr td:nth-child({column_index})').all_text_contents()

    def get_column_index(self, header_text) -> list[str]:
        """Get column index by header text"""
        self.page.locator('table.dataTable').first.wait_for()
        headers = self.page.locator('thead th').all_text_contents()
        return headers.index(header_text) + 1

    def go_to_first_page(self) -> None:
        """Navigate to first page"""
        # Click on page 1 or Previous until we reach first page
        first_page = self.page.locator(f'{self.table_id} li.paginate_button a[data-dt-idx="1"]').first
        first_page.wait_for()
        if first_page.count() > 0:
            first_page.click()
            self.page.wait_for_timeout(1000)
        else:
            # Keep clicking Previous until disabled
            while True:
                prev_button = self.page.locator(f'{self.table_id} li.paginate_button.previous').first
                is_disabled = "disabled" in prev_button.get_attribute("class").split()
                if prev_button.count() > 0 and not is_disabled:
                    prev_button.wait_for()
                    prev_button.click()
                    self.page.wait_for_timeout(1000)
                else:
                    break

    def set_entries_per_page(self, entries=100) -> None:
        """Set number of entries per page"""
        dropdown = self.page.locator(f'{self.table_id} .dataTables_length select').first
        dropdown.wait_for()
        if dropdown.count() > 0:
            dropdown.select_option(str(entries))
            self.page.wait_for_timeout(1500)

    def is_sorted(self, data, column_type, ascending=True, **kwargs) -> bool:
        """Check if data is sorted"""
        if column_type == "numeric":
            clean_data = [int(val.replace(',', '').strip()) for val in data if val.strip() != ""]
        elif column_type == "text":
            clean_data = [str(val).strip().upper() for val in data]
        elif column_type == "date":
            date_format = kwargs.get('date_format', '%d-%b-%Y')
            clean_data = [datetime.strptime(val, date_format) for val in data if val != ""]
        else:
            clean_data = data

        if ascending:
            return clean_data == sorted(clean_data)
        else:
            return clean_data == sorted(clean_data, reverse=True)
