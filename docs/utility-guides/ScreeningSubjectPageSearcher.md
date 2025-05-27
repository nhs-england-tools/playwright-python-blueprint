# Utility Guide: Screening Subject Page Searcher

The Screening Subject Search utility provides methods for:

- Searching for subjects using various parameters (NHS Number, forename, surname, DOB, postcode, episode closed date, status, or latest event status)
- Verifying a subject's event status using their NHS number

## Table of Contents

- [Utility Guide: Screening Subject Page Searcher](#utility-guide-screening-subject-page-searcher)
  - [Table of Contents](#table-of-contents)
  - [Functions Overview](#functions-overview)
    - [The page object parameter](#the-page-object-parameter)
    - [Function Summaries \& Example Usage](#function-summaries--example-usage)
      - [verify\_subject\_event\_status\_by\_nhs\_no](#verify_subject_event_status_by_nhs_no)
      - [Search Functions](#search-functions)
      - [check\_clear\_filters\_button\_works](#check_clear_filters_button_works)

## Functions Overview

The following functions are available:

- `verify_subject_event_status_by_nhs_no`
- `search_subject_by_nhs_number`
- `search_subject_by_surname`
- `search_subject_by_forename`
- `search_subject_by_dob`
- `search_subject_by_postcode`
- `search_subject_by_episode_closed_date`
- `search_subject_by_status`
- `search_subject_by_latest_event_status`
- `search_subject_by_search_area`
- `check_clear_filters_button_works`

### The page object parameter

All functions require the Playwright `page` object as their first argument.

---

### Function Summaries & Example Usage

#### verify_subject_event_status_by_nhs_no

Navigates to the subject screening search page and searches for the provided NHS Number. Then this checks that the latest event status of the subject matches the expected value(s).

**Arguments:**

- `page`: Playwright page object
- `nhs_no`: `str` — The subject's NHS number
- `latest_event_status`: `str | list[str]` — The expected status or list of statuses to verify

**Example:**

```python
verify_subject_event_status_by_nhs_no(page, "1234567890", "S61 - Normal (No Abnormalities Found)")
verify_subject_event_status_by_nhs_no(page, "1234567890", ["S61 - Normal (No Abnormalities Found)", "A158 - High-risk findings"])
```

---

#### Search Functions

All search functions follow a similar pattern: they clear filters, fill in the relevant field, and perform a search.

**Available search functions:**

- `search_subject_by_nhs_number(page, nhs_no: str)`
- `search_subject_by_surname(page, surname: str)`
- `search_subject_by_forename(page, forename: str)`
- `search_subject_by_dob(page, dob: str)`
- `search_subject_by_postcode(page, postcode: str)`
- `search_subject_by_episode_closed_date(page, episode_closed_date: str)`
- `search_subject_by_status(page, status: str)`
- `search_subject_by_latest_event_status(page, status: str)`
- `search_subject_by_search_area(page, status: str, search_area: str, code: str = None, gp_practice_code: str = None)`

**Example:**

```python
search_subject_by_nhs_number(page, "1234567890")
search_subject_by_surname(page, "Smith")
search_subject_by_forename(page, "John")
search_subject_by_dob(page, "1970-01-01")
search_subject_by_postcode(page, "AB12 3CD")
search_subject_by_episode_closed_date(page, "2023-12-31")
search_subject_by_status(page, "Call")
search_subject_by_latest_event_status(page, "S61 - Normal (No Abnormalities Found)")
search_subject_by_search_area(page, "Call", "Whole Database", code="XYZ", gp_practice_code="ABC123")
```

---

#### check_clear_filters_button_works

Checks that the "clear filters" button works as intended. It enters the provided NHS number, clicks the clear filters button, and then verifies that the filters are cleared.

**Arguments:**

- `page`: Playwright page object
- `nhs_no`: `str` — The subject's NHS number

**Example:**

```python
check_clear_filters_button_works(page, "1234567890")
```

---

For more details on each function's implementation, refer to the source code.
