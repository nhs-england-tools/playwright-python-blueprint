# Utility Guide: Calendar Picker

The Calendar Picker utility provides functions for interacting with the different calendar pickers found throughout BCSS.<br>
**On BCSS there are three different calendar types:**

1. **V1 Calendar Picker:**
   Seen on pages like the Screening Subject Search page. This calendar allows users to change the year/month in increments of 1 using the `<<`, `<`, `>`, `>>` buttons.

2. **V2 Calendar Picker:**
   Seen on pages like the Active Batch List page. This calendar allows users to expand the view of dates for faster navigation to previous/future dates.

3. **Appointments Calendar:**
   Seen on appointment booking pages. This consists of two calendars side by side, with cell background colours indicating appointment availability. Navigation is also via `<<`, `<`, `>`, `>>` buttons.

**You must use the applicable function for the calendar type you are interacting with.**

## Table of Contents

- [Utility Guide: Calendar Picker](#utility-guide-calendar-picker)
  - [Table of Contents](#table-of-contents)
  - [Summary of Calendar Types](#summary-of-calendar-types)
  - [Main Methods](#main-methods)
    - [`calendar_picker_ddmmyyyy` (V1 Calendar Picker)](#calendar_picker_ddmmyyyy-v1-calendar-picker)
    - [`calendar_picker_ddmonyy` (V2 Calendar Picker)](#calendar_picker_ddmonyy-v2-calendar-picker)
    - [`v1_calendar_picker` (V1 Calendar Picker)](#v1_calendar_picker-v1-calendar-picker)
    - [`v2_calendar_picker` (V2 Calendar Picker)](#v2_calendar_picker-v2-calendar-picker)
    - [`book_first_eligible_appointment` (Appointments Calendar)](#book_first_eligible_appointment-appointments-calendar)
  - [Supporting Methods](#supporting-methods)
  - [Example Usage](#example-usage)

---

## Summary of Calendar Types

| Calendar Type           | Where Seen                        | Navigation Style                                  | Main Method(s) to Use                |
|------------------------ |-----------------------------------|---------------------------------------------------|--------------------------------------|
| V1 Calendar Picker      | Screening Subject Search, others  | Year/month navigation with `<<`, `<`, `>`, `>>`   | `calendar_picker_ddmmyyyy`, `v1_calendar_picker` |
| V2 Calendar Picker      | Active Batch List, others         | Expandable view for fast navigation               | `calendar_picker_ddmonyy`, `v2_calendar_picker`  |
| Appointments Calendar   | Appointment booking pages         | Two calendars, cell colours for availability      | `book_first_eligible_appointment`    |

---

## Main Methods

### `calendar_picker_ddmmyyyy` (V1 Calendar Picker)

Inputs a date as a string in the format `dd/mm/yyyy` (e.g. 16/01/2025) into a field, instead of using the picker UI.

**Arguments:**

- `date` (`datetime`): The date you want to enter.
- `locator` (`Locator`): The Playwright locator for the field.

**How it works:**
Formats the date using DateTimeUtils and enters it directly into the field.

---

### `calendar_picker_ddmonyy` (V2 Calendar Picker)

Inputs a date as a string in the format `dd mon yy` (e.g. 16 Jan 25) into a field, instead of using the picker UI.

**Arguments:**

- `date` (`datetime`): The date you want to enter.
- `locator` (`Locator`): The Playwright locator for the field.

**How it works:**
Formats the date using DateTimeUtils (with OS-specific handling) and enters it directly into the field.

---

### `v1_calendar_picker` (V1 Calendar Picker)

Uses the navigation buttons (`<<`, `<`, `>`, `>>`) to select a date in the V1 calendar picker.

**Arguments:**

- `date` (`datetime`): The date you want to select.

**How it works:**
Determines how many years/months to traverse, navigates using the appropriate buttons, and selects the day.

---

### `v2_calendar_picker` (V2 Calendar Picker)

Uses the navigation controls to select a date in the V2 calendar picker, which allows for faster navigation by expanding the view.

**Arguments:**

- `date` (`datetime`): The date you want to select.

**How it works:**
Calculates the required navigation steps, expands the picker view as needed, and selects the desired date.

---

### `book_first_eligible_appointment` (Appointments Calendar)

Selects the first day with available appointment slots in the appointments calendar (which shows two months side by side).

**Arguments:**

- `current_month_displayed` (`str`): The current month displayed by the calendar.
- `locator` (`Locator`): The locator for the appointment day cells.
- `bg_colours` (`list`): List of background colours indicating available slots.

**How it works:**
Navigates through months and selects the first available appointment date based on cell background colour.

---

## Supporting Methods

These methods are used internally by the main methods above:

- `calculate_years_and_months_to_traverse`
- `traverse_years_in_v1_calendar`
- `traverse_months_in_v1_calendar`
- `calculate_v2_calendar_variables`
- `v2_calendar_picker_traverse_back`
- `v2_calendar_picker_traverse_forward`
- `select_day`
- `book_appointments_go_to_month`
- `check_for_eligible_appointment_dates`

---

## Example Usage

```python
from utils.calendar_picker import CalendarPicker
from datetime import datetime

# Example 1: Input a date as a string for V1 calendar picker
CalendarPicker(page).calendar_picker_ddmmyyyy(datetime(2025, 1, 16), page.locator("#date-input"))

# Example 2: Input a date as a string for V2 calendar picker
CalendarPicker(page).calendar_picker_ddmonyy(datetime(2025, 1, 16), page.locator("#date-input"))

# Example 3: Use the V1 calendar picker to select a date
CalendarPicker(page).v1_calendar_picker(datetime(2025, 1, 16))

# Example 4: Use the V2 calendar picker to select a date
CalendarPicker(page).v2_calendar_picker(datetime(2025, 1, 16))

# Example 5: Book the first eligible appointment in the appointments calendar
# In this example, we use hard-coded variables. In our actual tests, these values are obtained from Page Object Models (POMs). See [C4] for a more practical example.
CalendarPicker(page).book_first_eligible_appointment(
    current_month_displayed="January",
    locator=page.locator(".appointment-day"),
    bg_colours=["#00FF00", "#99FF99"]  # Example colours for available slots
)
```

> **Tip:** Always use the function that matches the calendar type you are interacting with in BCSS.

For more details on each function's implementation, refer to the source code in `utils/calendar_picker.py`.
