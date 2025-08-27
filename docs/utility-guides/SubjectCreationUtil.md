# Utility Guide: Subject Creation Utility

This guide explains the purpose and usage of the `CreateSubjectSteps` utility found in [`utils/oracle/subject_creation_util.py`](../../utils/oracle/subject_creation_util.py).
It is designed to automate the creation of custom subjects for test scenarios, supporting a variety of criteria such as age, GP practice, and more.

---

## Table of Contents

- [Utility Guide: Subject Creation Utility](#utility-guide-subject-creation-utility)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Required Arguments](#required-arguments)
  - [How It Works](#how-it-works)
  - [Example Usage](#example-usage)
  - [Supported Criteria](#supported-criteria)
  - [Best Practices](#best-practices)
  - [Reference](#reference)

---

## Overview

The `CreateSubjectSteps` class provides methods to create, log, and verify subjects in the BCSS Playwright test suite. It interacts with the Oracle database to insert subjects with specific attributes, making it easy to set up test data for automated scenarios.

---

## Required Arguments

Each function in this utility requires specific arguments:

- `subject_requirements` (dict):
  A dictionary mapping human-readable field labels to desired values.
  Example: `{"age": "30"}` or `{"gp practice": "C81014"}`

---

## How It Works

- The utility generates a random subject and updates its attributes based on the provided requirements.
- Supported criteria are mapped to subject fields (e.g., age, NHS number, GP practice).
- The subject is inserted into the database using the `SubjectRepository`.
- The utility provides helper methods for safe string/date formatting and subject existence checks.

---

## Example Usage

Below are examples of how to use `CreateSubjectSteps` in your tests:

```python
import pytest
from utils.oracle.subject_creation_util import CreateSubjectSteps

@pytest.fixture
def subject_steps():
    return CreateSubjectSteps()

def test_create_custom_subject_age(subject_steps):
    expected_age = 30
    requirements = {"age": str(expected_age)}
    nhs_no = subject_steps.create_custom_subject(requirements)


def test_create_custom_subject_age_yd(subject_steps):
    expected_years = 65
    expected_days = 25
    requirements = {"age (y/d)": f"{expected_years}/{expected_days}"}
    nhs_no = subject_steps.create_custom_subject(requirements)

def test_create_custom_subject_gp_practice(subject_steps):
    requirements = {"gp practice": "C81014"}
    nhs_no = subject_steps.create_custom_subject(requirements)

def test_create_custom_subject_active_gp_practice(subject_steps):
    requirements = {"active gp practice in hub/sc": "BCS01/BCS001"}
    nhs_no = subject_steps.create_custom_subject(requirements)

def test_create_custom_subject_inactive_gp_practice(subject_steps):
    requirements = {"inactive gp practice": ""}
    nhs_no = subject_steps.create_custom_subject(requirements)

def test_create_custom_subject_invalid_criteria(subject_steps):
    requirements = {"invalid_field": "value"}
    with pytest.raises(ValueError) as excinfo:
        subject_steps.create_custom_subject(requirements)
    assert "The criteria provided (invalid_field) is not valid" in str(excinfo.value)
```

---

See `tests_utils/test_subject_creation_util.py` for more examples.

---

## Supported Criteria

You can create subjects with the following criteria:

| Criteria Key                      | Example Value         | Description                                                      |
|------------------------------------|----------------------|------------------------------------------------------------------|
| `nhs number`                      | `"9953536309"`       | Sets the NHS number                                              |
| `age`                             | `"30"`               | Sets the subject's age in years                                  |
| `age (y/d)`                       | `"65/25"`            | Sets the subject's age in years and days                         |
| `gp practice`                     | `"C81014"`           | Sets the GP practice code                                        |
| `active gp practice in hub/sc`    | `"BCS01/BCS001"`     | Sets an active GP practice linked to both hub and screening centre|
| `inactive gp practice`            | `""`                 | Sets an inactive GP practice                                     |

If an invalid criteria is provided, a `ValueError` will be raised.

---

## Best Practices

- Use this utility in test setup steps to ensure subjects have the required attributes before running scenario-specific tests.
- Always check for exceptions when providing custom criteria.
- Use the helper methods (`safe_string`, `safe_date`, `get_subject_details`) for logging and debugging.

---

## Reference

- [`utils/oracle/subject_creation_util.py`](../../utils/oracle/subject_creation_util.py)
- [`tests_utils/test_subject_creation_util.py`](../../tests_utils/test_subject_creation_util.py)
- [SubjectDemographics Utility Guide](SubjectDemographics.md)
- [DateTimeUtility Guide](DateTimeUtility.md)

---

For more details on each method's implementation, refer to the source code in `utils/oracle/subject_creation_util.py`.
