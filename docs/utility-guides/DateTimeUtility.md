# Utility Guide: Date Time Utility

The Date Time Utility provides a set of helper functions for manipulating dates and times in your tests.
You can use it to assert timestamp values, change the format of a date, calculate date differences, add or subtract time, and more.

## Table of Contents

- [Utility Guide: Date Time Utility](#utility-guide-date-time-utility)
  - [Table of Contents](#table-of-contents)
  - [Using the Date Time Utility](#using-the-date-time-utility)
  - [Main Features](#main-features)
  - [Example Usage](#example-usage)
  - [Method Reference](#method-reference)
    - [`current_datetime(format_date: str = "%d/%m/%Y %H:%M") -> str`](#current_datetimeformat_date-str--dmy-hm---str)
    - [`format_date(date: datetime, format_date: str = "%d/%m/%Y") -> str`](#format_datedate-datetime-format_date-str--dmy---str)
    - [`add_days(date: datetime, days: float) -> datetime`](#add_daysdate-datetime-days-float---datetime)
    - [`get_day_of_week_for_today(date: datetime) -> str`](#get_day_of_week_for_todaydate-datetime---str)
    - [`get_a_day_of_week(date: datetime) -> str`](#get_a_day_of_weekdate-datetime---str)
    - [`report_timestamp_date_format() -> str`](#report_timestamp_date_format---str)
    - [`fobt_kits_logged_but_not_read_report_timestamp_date_format() -> str`](#fobt_kits_logged_but_not_read_report_timestamp_date_format---str)
    - [`screening_practitioner_appointments_report_timestamp_date_format() -> str`](#screening_practitioner_appointments_report_timestamp_date_format---str)
    - [`month_string_to_number(string: str) -> int`](#month_string_to_numberstring-str---int)

## Using the Date Time Utility

To use the Date Time Utility, import the `DateTimeUtils` class from `utils.date_time_utils` into your test file and call its methods as needed.

```python
from utils.date_time_utils import DateTimeUtils
```

## Main Features

- Get the current date/time in various formats
- Format dates to different string representations
- Add or subtract days from a date
- Get the day of the week for a given date
- Get formatted timestamps for different report types
- Convert a month name string to its corresponding number

---

## Example Usage

```python
from utils.date_time_utils import DateTimeUtils
from datetime import datetime

# Get the current date and time as a string
now_str = DateTimeUtils.current_datetime()
print(now_str)  # e.g. '28/05/2025 14:30'

# Format a datetime object as 'dd/mm/yyyy'
formatted = DateTimeUtils.format_date(datetime(2025, 1, 16))
print(formatted)  # '16/01/2025'

# Add 5 days to a date
future_date = DateTimeUtils.add_days(datetime(2025, 1, 16), 5)
print(future_date)  # datetime object for 21/01/2025

# Get the day of the week for a date
weekday = DateTimeUtils.get_day_of_week_for_today(datetime(2025, 1, 16))
print(weekday)  # 'Thursday'

# Get the day of the week (alias method)
weekday2 = DateTimeUtils.get_a_day_of_week(datetime(2025, 1, 16))
print(weekday2)  # 'Thursday'

# Get the current timestamp in report format
report_timestamp = DateTimeUtils.report_timestamp_date_format()
print(report_timestamp)  # e.g. '28/05/2025 at 14:30:00'

# Get the current timestamp in FOBT kits report format
fobt_timestamp = DateTimeUtils.fobt_kits_logged_but_not_read_report_timestamp_date_format()
print(fobt_timestamp)  # e.g. '28 May 2025 14:30:00'

# Get the current timestamp in screening practitioner appointments report format
spa_timestamp = DateTimeUtils.screening_practitioner_appointments_report_timestamp_date_format()
print(spa_timestamp)  # e.g. '28.05.2025 at 14:30:00'

# Convert a month name to its number
month_num = DateTimeUtils().month_string_to_number("February")
print(month_num)  # 2

month_num_short = DateTimeUtils().month_string_to_number("Sep")
print(month_num_short)  # 9
```

---

## Method Reference

### `current_datetime(format_date: str = "%d/%m/%Y %H:%M") -> str`

Returns the current date as a string in the specified format.

### `format_date(date: datetime, format_date: str = "%d/%m/%Y") -> str`

Formats a given `datetime` object as a string.

### `add_days(date: datetime, days: float) -> datetime`

Adds a specified number of days to a given date.

### `get_day_of_week_for_today(date: datetime) -> str`

Returns the day of the week for the given date.

### `get_a_day_of_week(date: datetime) -> str`

Alias for `get_day_of_week_for_today`.

### `report_timestamp_date_format() -> str`

Returns the current date and time in the format `'dd/mm/yyyy at hh:mm:ss'`.

### `fobt_kits_logged_but_not_read_report_timestamp_date_format() -> str`

Returns the current date and time in the format `'dd Mon yyyy hh:mm:ss'`.

### `screening_practitioner_appointments_report_timestamp_date_format() -> str`

Returns the current date and time in the format `'dd.mm.yyyy at hh:mm:ss'`.

### `month_string_to_number(string: str) -> int`

Converts a month name (full or short, case-insensitive) to its corresponding number (1-12).

---

Refer to the source code and function docstrings in `utils/date_time_utils.py` for more details and any additional helper methods.
