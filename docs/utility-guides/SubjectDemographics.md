# Utility Guide: Subject Demographics

The Subject Demographics utility provides helper methods for interacting with and updating subject demographic data within the BCSS Playwright automation framework.<br>
This includes:

1. Updating a subject's date of birth (DOB) to a random value within specific age ranges.
2. Navigating to the subject demographic page and updating fields such as postcode and DOB.

## Table of Contents

- [Utility Guide: Subject Demographics](#utility-guide-subject-demographics)
  - [Table of Contents](#table-of-contents)
  - [Using the SubjectDemographicUtil class](#using-the-subjectdemographicutil-class)
  - [Updating DOB](#updating-dob)
    - [Arguments](#arguments)
    - [How to use this method](#how-to-use-this-method)
  - [Other Utility Methods](#other-utility-methods)

## Using the SubjectDemographicUtil class

You can initialise the SubjectDemographicUtil class by using the following code in your test file:

```python
from utils.subject_demographics import SubjectDemographicUtil
```

## Updating DOB

The `update_subject_dob` method allows you to update a subject's date of birth, either to a specific value or to a random value within a chosen age range. The method will automatically navigate to the subject demographic page, fill in required fields (such as postcode if missing), and update the DOB.

### Arguments

- `nhs_no`:
  - Type: `str`
  - The NHS number of the subject you want to update.
- `random_dob`:
  - Type: `bool`
  - If `True`, the DOB will be set to a random value within the specified age range.
  - If `False`, the DOB will be set to the value provided in `new_dob`.
- `younger_subject`:
  - Type: `bool | None`
  - Determines the age range for the random DOB update (only used if `random_dob` is `True`):
    - `True`: Random age between 50-70 years old.
    - `False`: Random age between 75-100 years old.
    - `None`: Defaults to `False` (75-100 years old).
- `new_dob`:
  - Type: `datetime | None`
  - The new date of birth to set (only used if `random_dob` is `False`).

### How to use this method

To update a subject's DOB to a random value between 50-70:

```python
nhs_no = "9468743977"
SubjectDemographicUtil(page).update_subject_dob(nhs_no, random_dob=True, younger_subject=True)
```

To update a subject's DOB to a random value between 75-100:

```python
nhs_no = "9468743977"
SubjectDemographicUtil(page).update_subject_dob(nhs_no, random_dob=True, younger_subject=False)
```

To update a subject's DOB to a specific date:

```python
from datetime import datetime
nhs_no = "9468743977"
new_dob = datetime(1960, 5, 15)
SubjectDemographicUtil(page).update_subject_dob(nhs_no, random_dob=False, new_dob=new_dob)
```

## Other Utility Methods

- `random_dob_within_range(younger: bool) -> datetime`
  - Generates a random date of birth within the specified age range:
    - If `younger` is `True`, returns a DOB for age 50-70.
    - If `younger` is `False`, returns a DOB for age 75-100.

- `random_datetime(start: datetime, end: datetime) -> datetime`
  Generates a random date between two `datetime` objects.

Refer to the source code in `utils/subject_demographics.py` for more details on available methods and their usage.
