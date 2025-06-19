import logging
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
