# Utility Guide: Table Utility

The Table Utilities module (`utils/table_util.py`) provides helper functions to interact with and validate HTML tables in Playwright-based UI tests.
**This utility is designed to be used inside Page Object Model (POM) classes** to simplify table interactions and assertions.

## Table of Contents

- [Utility Guide: Table Utility](#utility-guide-table-utility)
  - [Table of Contents](#table-of-contents)
  - [Using the Table Utility](#using-the-table-utility)
  - [Example usage](#example-usage)
    - [Get Column Index](#get-column-index)
      - [Example](#example)
    - [Click First Link In Column](#click-first-link-in-column)
      - [Example](#example-1)
    - [Click First Input In Column](#click-first-input-in-column)
      - [Example](#example-2)
    - [Format Inner Text](#format-inner-text)
      - [Example](#example-3)
    - [Get Table Headers](#get-table-headers)
      - [Example](#example-4)
    - [Get Row Count](#get-row-count)
      - [Example](#example-5)
    - [Pick Row](#pick-row)
      - [Example](#example-6)
    - [Pick Random Row](#pick-random-row)
      - [Example](#example-7)
    - [Pick Random Row Number](#pick-random-row-number)
      - [Example](#example-8)
    - [Get Row Data With Headers](#get-row-data-with-headers)
      - [Example](#example-9)
    - [Get Full Table With Headers](#get-full-table-with-headers)
      - [Example](#example-10)

## Using the Table Utility

To use the Table Utility, import the `TableUtils` class into your Page Object Model (POM) file and instantiate it for each table you want to interact with.

```python
from utils.table_util import TableUtils

class ReportsPage(BasePage):
    """Reports Page locators, and methods for interacting with the page."""

    def __init__(self, page):
        super().__init__(page)
        self.page = page

        # Initialize TableUtils for different tables by passing the page and table selector
        self.reports_table = TableUtils(page, "#listReportDataTable")
        self.subjects_table = TableUtils(page, "#subjInactiveOpenEpisodes")
```

## Example usage

Below are examples of how to use `TableUtils` methods inside your POM methods or tests:

```python
# Click the first NHS number link in the reports table
self.reports_table.click_first_link_in_column("NHS Number")

# Get the index of the "Status" column
status_col_index = self.reports_table.get_column_index("Status")

# Click the first checkbox in the "Select" column
self.subjects_table.click_first_input_in_column("Select")

# Get all table headers as a dictionary
headers = self.reports_table.get_table_headers()

# Get the number of visible rows in the table
row_count = self.reports_table.get_row_count()

# Pick a specific row (e.g., row 2)
row_locator = self.reports_table.pick_row(2)

# Pick a random row and click a link in the "Details" column
random_row = self.reports_table.pick_random_row()
random_row.locator("td").nth(self.reports_table.get_column_index("Details") - 1).locator("a").click()

# Get data for a specific row as a header-value dictionary
row_data = self.reports_table.get_row_data_with_headers(1)

# Get the entire table as a dictionary of rows
full_table = self.reports_table.get_full_table_with_headers()
```

---

### Get Column Index

Returns the index (1-based) of a specified column name. Returns -1 if not found.

#### Example

```python
col_index = self.reports_table.get_column_index("Date")
```

### Click First Link In Column

Clicks on the first hyperlink present in a specified column.

#### Example

```python
self.reports_table.click_first_link_in_column("NHS Number")
```

### Click First Input In Column

Clicks on the first input element (e.g., checkbox/radio) in a specific column.

#### Example

```python
self.reports_table.click_first_input_in_column("Select")
```

### Format Inner Text

Formats inner text of a row string into a dictionary.

#### Example

```python
row_dict = self.reports_table.format_inner_text("123\tJohn Doe\tActive")
```

### Get Table Headers

Extracts and returns table headers as a dictionary.

#### Example

```python
headers = self.reports_table.get_table_headers()
```

### Get Row Count

Returns the count of visible rows in the table.

#### Example

```python
count = self.reports_table.get_row_count()
```

### Pick Row

Returns a locator for a specific row (1-based).

#### Example

```python
row_locator = self.reports_table.pick_row(3)
```

### Pick Random Row

Picks and returns a locator for a random visible row.

#### Example

```python
random_row = self.reports_table.pick_random_row()
```

### Pick Random Row Number

Returns the number of a randomly selected row.

#### Example

```python
random_row_number = self.reports_table.pick_random_row_number()
```

### Get Row Data With Headers

Returns a dictionary of header-value pairs for a given row.

#### Example

```python
row_data = self.reports_table.get_row_data_with_headers(2)
```

### Get Full Table With Headers

Constructs a dictionary of the entire table content.

#### Example

```python
full_table = self.reports_table.get_full_table_with_headers()
```

---

For more details on each function's implementation, refer to the source code in `utils/table_util.py`.
