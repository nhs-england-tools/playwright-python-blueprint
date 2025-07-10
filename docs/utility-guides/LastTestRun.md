# Utility Guide: last_test_run

The `last_test_run` utility provides a simple way to track when specific tests were last executed. It is designed to help you avoid running setups for tests multiple times and instead does a check to see if the test has been run today.

---

## Table of Contents

- [Utility Guide: last\_test\_run](#utility-guide-last_test_run)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [When and Why to Use last\_test\_run](#when-and-why-to-use-last_test_run)
  - [Required Arguments](#required-arguments)
  - [last\_test\_run Methods](#last_test_run-methods)
  - [Example Usage](#example-usage)
  - [How It Works](#how-it-works)
  - [Implementation Details](#implementation-details)

---

## Overview

This utility manages a JSON file (`.test_last_runs.json`) that records the last date each test was run. It provides functions to load, save, and check this data, making it easy to implement "run once per day" logic in your test suite.

---

## When and Why to Use last_test_run

You might want to use this utility in scenarios such as:

- Avoiding repeated execution of slow or stateful tests within the same day.
- Ensuring setup or tear down routines only run once per day.
- Tracking test execution dates for reporting or debugging.

---

## Required Arguments

Each function in this utility requires specific arguments:

- `has_test_run_today(test_name: str) -> bool`:
  - `test_name` (str): The unique name of the test to check.

See the docstrings in the code for details on each function.

---

## last_test_run Methods

**The main methods provided are:**

- **load_last_run_data() -> Dict[str, Any]**
  Loads the last run data from the JSON file. Returns a dictionary mapping test names to their last run date.

- **save_last_run_data(data: Dict[str, Any]) -> None**
  Saves the provided dictionary to the JSON file.

- **has_test_run_today(test_name: str) -> `bool`**
  Checks if the given test has already run today. If not, updates the record to mark it as run today.

---

## Example Usage

```python
from utils.last_test_run import has_test_run_today

def test_expensive_setup():
    if has_test_run_today("test_expensive_setup"):
        print("Setup already run today, skipping.")
        return
    # ... perform expensive setup ...
    print("Setup complete.")
```

---

## How It Works

- The utility stores a mapping of test names to their last run date in `.test_last_runs.json`.
- When `has_test_run_today` is called, it checks if the test has already run today.
  - If yes, it returns `True`.
  - If no, it updates the file and returns `False`.

---

## Implementation Details

- The JSON file is created in the project root if it does not exist.
- If the file is empty or corrupted, the utility will safely return an empty dictionary and continue.
- All functions are type-annotated and documented with docstrings for clarity.

---

> **Note:**
> The `last_test_run` utility is available under `utils/last_test_run.py`.
> See the source code for more details and to extend its functionality as needed.
