from turtle import title
from playwright.sync_api import Page, Locator, expect
from sqlalchemy import desc
from pages.base_page import BasePage
import logging
import secrets


class TableUtils:
    """
    A utility class providing functionality around tables in BCSS.
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
        self.table_id = table_locator  # Store the table locator as a string
        self.table = page.locator(
            table_locator
        )  # Create a locator object for the table

    def get_column_index(self, column_name: str) -> int:
        """
        Finds the column index dynamically based on column name.
        Works even if <thead> is missing and header is inside <tbody>.

        Args:
            column_name (str): Name of the column (e.g., 'NHS Number')

        Return:
            An int (1-based column index or -1 if not found)
        """
        # Try to find headers in <thead> first
        header_row = self.table.locator("thead tr").first
        if not header_row.locator("th").count():
            # Fallback: look for header in <tbody> if <thead> is missing or empty
            header_row = (
                self.table.locator("tbody tr").filter(has=self.page.locator("th")).first
            )

        headers = header_row.locator("th")

        # Extract first-row headers (general headers)
        header_texts = headers.evaluate_all("ths => ths.map(th => th.innerText.trim())")
        logging.info(f"First Row Headers Found: {header_texts}")

        # Extract detailed second-row headers if first-row headers seem generic
        second_row_headers = self.table.locator(
            "thead tr:nth-child(2) th"
        ).evaluate_all("ths => ths.map(th => th.innerText.trim())")
        # Merge both lists: Prioritize second-row headers if available
        if second_row_headers:
            header_texts = second_row_headers

        logging.info(f"Second Row Headers Found: {header_texts}")
        for index, header in enumerate(header_texts):
            if column_name.lower() in header.lower():
                return index + 1  # Convert to 1-based index
        return -1  # Column not found

    def click_first_link_in_column(self, column_name: str):
        """
        Clicks the first link found in the given column.

        Args:
            column_name (str): Name of the column containing links
        """
        column_index = self.get_column_index(column_name)
        if column_index == -1:
            raise ValueError(f"Column '{column_name}' not found in table")

        # Create a dynamic locator for the desired column
        link_locator = f"{self.table_id} tbody tr td:nth-child({column_index}) a"
        links = self.page.locator(link_locator)

        if links.count() > 0:
            links.first.click()
        else:
            logging.error(f"No links found in column '{column_name}'")

    def click_first_input_in_column(self, column_name: str):
        """
        Clicks the first input found in the given column. E.g. Radios

        Args:
            column_name (str): Name of the column containing inputs
        """
        column_index = self.get_column_index(column_name)
        if column_index == -1:
            raise ValueError(f"Column '{column_name}' not found in table")

        # Create a dynamic locator for the desired column
        input_locator = f"{self.table_id} tbody tr td:nth-child({column_index}) input"
        inputs = self.page.locator(input_locator)

        if inputs.count() > 0:
            inputs.first.click()
        else:
            logging.error(f"No inputs found in column '{column_name}'")

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
            secrets.randbelow(self.get_row_count())
        )

    def pick_random_row_number(self) -> int:
        """
        This picks a random row from the table in BCSS and returns its position

        Returns:
            An int representing a random row on the table.
        """
        return secrets.randbelow(self.get_row_count())

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

    def get_cell_value(self, column_name: str, row_index: int) -> str:
        """
        Retrieves the text value of a cell at the specified column(name) and row(index).

        Args:
            column_name (str): The name of the column containing the cell.
            row_index (int): The index of the row containing the cell.

        Returns:
            str: The text value of the cell.
        """
        column_index = self.get_column_index(column_name)
        if column_index == -1:
            raise ValueError(f"Column '{column_name}' not found in table")

        # Locate all <td> elements in the specified row and column
        cell_locator = (
            f"{self.table_id} tbody tr:nth-child({row_index}) td:nth-child({column_index})"
        )

        cell = self.page.locator(cell_locator).first

        if cell:
            return cell.inner_text()
        else:
            raise ValueError(
                f"No cell found at column '{column_name}' and row index {row_index}"
            )

    def assert_surname_in_table(self, surname_pattern: str) -> None:
        """
        Asserts that a surname matching the given pattern exists in the table.
        Args:
            surname_pattern (str): The surname or pattern to search for (supports '*' as a wildcard at the end).
        """
        # Locate all surname cells (adjust selector as needed)
        surname_criteria = self.page.locator(
            "//table//tr[position()>1]/td[3]"
        )  # Use the correct column index
        if surname_pattern.endswith("*"):
            prefix = surname_pattern[:-1]
            found = any(
                cell.inner_text().startswith(prefix)
                for cell in surname_criteria.element_handles()
            )
        else:
            found = any(
                surname_pattern == cell.inner_text()
                for cell in surname_criteria.element_handles()
            )
        assert found, f"No surname matching '{surname_pattern}' found in table."
