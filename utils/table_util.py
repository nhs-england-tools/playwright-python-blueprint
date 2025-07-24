from playwright.sync_api import Page, Locator
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

        # Attempt to extract a second row of headers (commonly used for filters or alternate titles)
        second_row_headers = self.table.locator(
            "thead tr:nth-child(2) th"
        ).evaluate_all("ths => ths.map(th => th.innerText.trim())")

        # Use the second row only if it contains meaningful text (not filters, dropdowns, or placeholder values)
        if second_row_headers and all(
            h and not any(c in h.lower() for c in ("input", "all", "select"))
            for h in second_row_headers
        ):
            header_texts = second_row_headers
        logging.info(f"Second Row Headers Found: {second_row_headers}")

        for index, header in enumerate(header_texts):
            if column_name.strip().lower() == header.strip().lower():
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
        Retrieves headers from a table, supporting both standard and legacy structures.
        Returns:
            dict: A mapping of column index (1-based) to header text.
        """
        # Strategy 1: Try <thead> with <tr><th><span class="dt-column-title">Header</span></th>
        header_spans = self.page.locator(
            f"{self.table_id} > thead tr:first-child th span.dt-column-title"
        )
        if header_spans.count():
            try:
                header_texts = header_spans.evaluate_all(
                    "els => els.map(el => el.textContent.trim())"
                )
                print("[DEBUG] Parsed header texts:", repr(header_texts))
                return {idx + 1: text for idx, text in enumerate(header_texts)}
            except Exception as e:
                logging.warning(
                    f"[get_table_headers] span.dt-column-title fallback failed: {e}"
                )

        # Strategy 2: Fallback to standard <thead> > tr > th inner text
        header_cells = self.page.locator(f"{self.table_id} > thead tr").first.locator(
            "th"
        )
        if header_cells.count():
            try:
                header_texts = header_cells.evaluate_all(
                    "els => els.map(th => th.innerText.trim())"
                )
                return {idx + 1: text for idx, text in enumerate(header_texts)}
            except Exception as e:
                logging.warning(f"[get_table_headers] basic <th> fallback failed: {e}")

        # Strategy 3: Last resort — try to find header from tbody row (some old tables use <tbody> only)
        fallback_row = (
            self.table.locator("tbody tr").filter(has=self.page.locator("th")).first
        )
        if fallback_row.locator("th").count():
            try:
                header_texts = fallback_row.locator("th").evaluate_all(
                    "els => els.map(th => th.innerText.trim())"
                )
                return {idx + 1: text for idx, text in enumerate(header_texts)}
            except Exception as e:
                logging.warning(f"[get_table_headers] tbody fallback failed: {e}")

        logging.warning(
            f"[get_table_headers] No headers found for table: {self.table_id}"
        )
        return {}

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

    def get_footer_value_by_header(self, header_name: str) -> str:
        """
        Retrieves the value from the footer row for the given column header name.

        Args:
            header_name (str): The visible text of the column header.

        Returns:
            str: Text content of the corresponding footer cell.

        Raises:
            ValueError: If the column header is not found or cell is missing.
        """
        # First get the column index dynamically
        column_index = self.get_column_index(header_name)
        if column_index == -1:
            raise ValueError(f"Column '{header_name}' not found")

        # Try to locate footer cell in tbody (last row), or fallback to tfoot
        footer_cell_tbody = self.page.locator(
            f"{self.table_id} tbody tr:last-child td:nth-child({column_index})"
        )
        footer_cell_tfoot = self.page.locator(
            f"{self.table_id} tfoot tr td:nth-child({column_index})"
        )

        if footer_cell_tbody.count() and footer_cell_tbody.first.is_visible():
            return footer_cell_tbody.first.inner_text().strip()
        elif footer_cell_tfoot.count() and footer_cell_tfoot.first.is_visible():
            return footer_cell_tfoot.first.inner_text().strip()
        else:
            raise ValueError(f"No footer cell found under column '{header_name}'")

    def get_row_where(self, criteria: dict[str, str]) -> Locator | None:
        """
        Finds and returns the first table row matching the given header-value criteria.

        Args:
            criteria (dict[str, str]): A dictionary where keys are column headers and values are expected contents.

        Returns:
            Locator of the matching row or None if not found.
        """
        row_count = self.get_row_count()
        for i in range(row_count):
            row_data = self.get_row_data_with_headers(i)
            if all(
                row_data.get(key, "").strip() == value
                for key, value in criteria.items()
            ):
                return self.pick_row(i)
        return None
