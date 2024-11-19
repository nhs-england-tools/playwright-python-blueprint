# Utility Guide: Date Time Utility

The Date Time Utility can be used to manipulate dates and times for various purposes,
such as asserting timestamp values, changing the format of a date, or returning the day of the week for a given date.

## Using the Date Time Utility

To use the Date Time Utility, import the 'DateTimeUtils' class into your test file and then call the DateTimeUtils
functions from within your tests, as required.

## Required arguments

The functions in this class require different arguments, including `datetime`, `str`, and `float`.
Look at the docstrings for each function to see what arguments are required.
The docstrings also specify when arguments are optional, and what the default values are when no argument is provided.

## Example usage

    from tests_utils.date_time_utils import DateTimeUtils

        def test_date_format(page: Page) -> None:
        expect(page.locator("#date")).to_contain_text(DateTimeUtils.current_datetime())
