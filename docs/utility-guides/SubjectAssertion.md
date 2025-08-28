# Utility Guide: Subject Assertion Utility

This guide explains the purpose and usage of the `subject_assertion` utility found in [`utils/subject_assertion.py`](../../utils/subject_assertion.py).
It is designed to assert that a subject with a given NHS number matches specified criteria in the database, and provides detailed logging when criteria do not match.

---

## Table of Contents

- [Utility Guide: Subject Assertion Utility](#utility-guide-subject-assertion-utility)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Required Arguments](#required-arguments)
  - [How It Works](#how-it-works)
  - [Example Usage](#example-usage)
  - [Behaviour Details](#behaviour-details)
  - [Best Practices](#best-practices)
  - [Reference](#reference)

---

## Overview

The `subject_assertion` function is used to verify that a subject in the database matches a set of criteria.
If the subject does not match all criteria, the function will iteratively loop through each criteria (except NHS number), logging any criteria that caused the assertion to fail.

---

## Required Arguments

- `nhs_number` (`str`): The NHS number of the subject to check.
- `criteria` (`dict`): A dictionary of criteria to match against the subject's attributes.

---

## How It Works

1. The function first checks if the subject with the given NHS number matches all provided criteria.
2. If not, it checks one criterion at a time and retries the assertion.
3. This process continues until all criteria have been checked.
4. If a match is found only after removing criteria, the failed criteria are logged.
5. The function returns `True` only if all criteria match on the first attempt; otherwise, it returns `False`.

---

## Example Usage

Below are examples of how to use `subject_assertion` in your tests:

```python
import pytest
from utils.subject_assertion import subject_assertion

pytestmark = [pytest.mark.utils_local]

def test_subject_assertion_true():
    nhs_number = "9233639266"
    criteria = {"screening status": "Inactive", "subject age": "> 28"}
    assert subject_assertion(nhs_number, criteria) is True
```

See `tests_utils/test_subject_assertion_util.py` for more examples.

---

## Behaviour Details

- The function always keeps the NHS number criterion.
- If a match is found only after removing criteria, the failed criteria are logged in the format:
  - Failed criteria: Key: 'key1', Value: 'value1'
- The function will only return `True` if all criteria match on the first attempt.

---

## Best Practices

- Use this utility to validate subject data in database-driven tests.
- Review logs for failed criteria to diagnose why assertions did not pass.
- Always provide the NHS number as part of your criteria.

---

## Reference

- [`utils/subject_assertion.py`](../../utils/subject_assertion.py)
- [`tests_utils/test_subject_assertion_util.py`](../../tests_utils/test_subject_assertion_util.py)
- [SubjectSelectionQueryBuilder Utility Guide](SubjectSelectionQueryBuilder.md)
