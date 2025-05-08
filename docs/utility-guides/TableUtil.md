# Utility Guide: Table Utility

The Table Utilities module provides helper functions to interact with and validate HTML tables in Playwright-based UI tests.

## Table of Contents

- [Utility Guide: Table Utility](#utility-guide-table-utility)
  - [Table of Contents](#table-of-contents)
  - [Using the Table Utility](#using-the-table-utility)
  - [Example usage](#example-usage)
    - [Get Column Index](#get-column-index)
      - [Required Arguments](#required-arguments)
      - [How This Function Works](#how-this-function-works)
    - [Click First Link In Column](#click-first-link-in-column)
      - [Required Arguments](#required-arguments-1)
      - [How This Function Works](#how-this-function-works-1)
    - [Click First Input In Column](#click-first-input-in-column)
      - [Required Arguments](#required-arguments-2)
      - [How This Function Works](#how-this-function-works-2)
    - [Format Inner Text](#format-inner-text)
      - [Required Arguments](#required-arguments-3)
      - [How This Function Works](#how-this-function-works-3)
    - [Get Table Headers](#get-table-headers)
      - [Required Arguments](#required-arguments-4)
      - [How This Function Works](#how-this-function-works-4)
    - [Get Row Count](#get-row-count)
      - [Required Arguments](#required-arguments-5)
      - [How This Function Works](#how-this-function-works-5)
    - [Pick Row](#pick-row)
      - [Required Arguments](#required-arguments-6)
      - [How This Function Works](#how-this-function-works-6)
    - [Pick Random Row](#pick-random-row)
      - [Required Arguments](#required-arguments-7)
      - [How This Function Works](#how-this-function-works-7)
    - [Pick Random Row Number](#pick-random-row-number)
      - [Required Arguments](#required-arguments-8)
      - [How This Function Works](#how-this-function-works-8)
    - [Get Row Data With Headers](#get-row-data-with-headers)
      - [Required Arguments](#required-arguments-9)
      - [How This Function Works](#how-this-function-works-9)
    - [Get Full Table With Headers](#get-full-table-with-headers)
      - [Required Arguments](#required-arguments-10)
      - [How This Function Works](#how-this-function-works-10)

## Using the Table Utility

To use the Table Utility, import the `TableUtils` class into your POM file and then define the actions using the its methods as needed.

## Example usage

Below is an example of how the TableUtils used in reports_page.py

    from utils.table_util import TableUtils
    class ReportsPage(BasePage):
    """Reports Page locators, and methods for interacting with the page."""

      def __init__(self, page):
        super().__init__(page)
        self.page = page

        # Initialize TableUtils for different tables
        self.failsafe_reports_sub_links_table = TableUtils(page, "#listReportDataTable")
        self.fail_safe_reports_screening_subjects_with_inactive_open_episodes_table = (
            TableUtils(page, "#subjInactiveOpenEpisodes")
        )
      def click_failsafe_reports_sub_links(self):
        """Clicks the first NHS number link from the primary report table."""
        self.failsafe_reports_sub_links_table.click_first_link_in_column("NHS Number")

### Get Column Index

This function returns the index (1-based) of a specified column name. 1-based indexing means the first column is considered index 1 (not 0 as in Python lists).
If the column is not found, the function returns -1.

#### Required Arguments

- `column_name`:
  - Type: `str`
  - The visible header text of the column to locate.

#### How This Function Works

1. Attempts to identify table headers from <thead> or <tbody>.
2. Iterates through header cells and matches text with `column_name`.
3. Returns the index if found, otherwise raises an error.

### Click First Link In Column

Clicks on the first hyperlink present in a specified column.

#### Required Arguments

- `column_name`:
  - Type: `str`
  - The column in which the link needs to be found.

#### How This Function Works

1. Finds the index of the specified column.
2. Searches the first visible row in the column for an `<a>` tag.
3. Clicks the first available link found.

### Click First Input In Column

Clicks on the first input element (e.g., checkbox/radio) in a specific column.

#### Required Arguments

- `column_name`:
  - Type: `str`
  - The name of the column containing the input element.

#### How This Function Works

1. Locates the index of the specified column.
2. Checks the first visible row for an `<input>` tag in that column.
3. Clicks the first input found.

### Format Inner Text

Formats inner text of a row string into a dictionary.

#### Required Arguments

- data:
  - Type: `str`
  - Raw inner text of a table row (tab-delimited).

#### How This Function Works

1. Splits the string by tab characters (\t).
2. Enumerates the result and maps index to cell value.
3. Returns a dictionary representing the row.

### Get Table Headers

Extracts and returns table headers.

#### Required Arguments

- None

#### How This Function Works

1. Selects the first row inside <thead> (if available).
2. Captures the visible text of each <th>.
3. Returns a dictionary mapping index to header text.

### Get Row Count

Returns the count of visible rows in the table.

#### Required Arguments

- None

#### How This Function Works

1. Locates all <tr> elements inside <tbody>.
2. Filters to include only visible rows.
3. Returns the total count.

### Pick Row

Returns a locator for a specific row.

#### Required Arguments

- `row_number`:
  - Type: `int`
  - The row index to locate (1-based).

#### How This Function Works

1. Builds a locator for the nth <tr> inside <tbody>.
2. Returns the locator object.

### Pick Random Row

Picks and returns a random row locator.

#### Required Arguments

- None

#### How This Function Works

1. Gets all visible rows inside <tbody>.
2. Uses a secure random generator to pick one.
3. Returns the locator for that row.

### Pick Random Row Number

Returns the number of a randomly selected row.

#### Required Arguments

- None

#### How This Function Works

1. Retrieves visible rows from <tbody>.
2. Randomly selects an index using secrets.choice.
3. Returns the numeric index.

### Get Row Data With Headers

Returns a dictionary of header-value pairs for a given row.

#### Required Arguments

- `row_number`:
  - Type:int
  - Index of the target row (1-based).

#### How This Function Works

1. Extracts text from the specified row.
2. Retrieves headers using get_table_headers.
3. Maps each cell to its respective header.

### Get Full Table With Headers

Constructs a dictionary of the entire table content.

#### Required Arguments

- None

#### How This Function Works

1. Gets all visible rows.
2. Retrieves headers once.
3. Loops over each row and builds a dictionary using get_row_data_with_headers.
4. Returns a dictionary where each key is a row number.
