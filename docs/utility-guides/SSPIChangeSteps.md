# Utility Guide: SSPIChangeSteps

The `SSPIChangeSteps` utility provides a simple interface for simulating an SSPI update to change a subject's date of birth in the BCSS system. This is particularly useful for automated testing scenarios where you need to set a subject's age to a specific value.

---

## Table of Contents

- [Utility Guide: SSPIChangeSteps](#utility-guide-sspichangesteps)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Example Usage](#example-usage)
  - [Method Reference](#method-reference)
  - [Implementation Details](#implementation-details)

---

## Overview

The main method provided by this utility is:

```python
sspi_update_to_change_dob_received(nhs_no: str, age_to_change_to: int)
```

This method will:

- Retrieve the subject by NHS number.
- Calculate the correct date of birth for the specified age (taking leap years into account).
- Update the subject's date of birth in the database as if it was received from an SSPI update.

## Example Usage

```python
from utils.sspi_change_steps import SSPIChangeSteps

nhs_no = "1234567890"
target_age = 75

SSPIChangeSteps().sspi_update_to_change_dob_received(nhs_no, target_age)
```

This will update the subject with NHS number `1234567890` to have an age of 75.

---

## Method Reference

`sspi_update_to_change_dob_received`

```python
def sspi_update_to_change_dob_received(nhs_no: str, age_to_change_to: int) -> None
```

**Parameters:**

- `nhs_no` (str): The NHS number of the subject to update.
- `age_to_change_to` (int): The age to change the subject's date of birth to.

**Description:**

Calculates the correct date of birth for the given age and updates the subject in the database as if the change was received from an SSPI update.

---

## Implementation Details

- The utility uses the `Subject` and `PISubject` classes to represent and update subject data.
- The date of birth is calculated using `DateTimeUtils.calculate_birth_date_for_age`, which ensures the correct age is set, accounting for leap years.
- The update is performed as the automated process user (user ID 2).
