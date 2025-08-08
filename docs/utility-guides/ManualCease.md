# Utility Guide: Manual Cease Workflow

This utility facilitates creation, UI automation, and database verification for manual cease workflows in the BCSS Playwright test suite.<br> It includes:

  1. Generating a subject eligible for manual cease via database creation and timeline event execution.
  2. Performing the cease workflow through the browser UI, supporting both 'immediate' and 'with disclaimer' flows.
  3. Validating dynamic database fields after cease is completed.

## Table of Contents

- [Utility Guide: Manual Cease Workflow](#utility-guide-manual-cease-workflow)
  - [Table of Contents](#table-of-contents)
  - [Creating Subjects for Cease](#creating-subjects-for-cease)
    - [Arguments](#arguments)
    - [How to use this method](#how-to-use-this-method)
  - [UI Workflow Methods](#ui-workflow-methods)
    - [Standard Flow (with Disclaimer)](#standard-flow-with-disclaimer)
    - [Immediate Flow](#immediate-flow)
  - [DB Verification](#db-verification)
    - [Arguments](#arguments-1)
    - [How to use this method](#how-to-use-this-method-1)
  - [Enums and Constants](#enums-and-constants)
    - [EXPECT markers](#expect-markers)
    - [Status \& Reason Enums](#status--reason-enums)

## Creating Subjects for Cease

The `create_manual_cease_ready_subject` method creates a subject with Inactive screening status and executes timed events, preparing it for the cease flow.

### Arguments

  `screening_centre`:
    Type: str
    Screening centre to associate with the subject. Defaults to "BCS002".

  `base_age`:
    Type: int
    Age threshold used during subject creation. Defaults to 75.

### How to use this method

```python
from utils.manual_cease_util import create_manual_cease_ready_subject
nhs_number = create_manual_cease_ready_subject(screening_centre="BCS002", base_age=75)
```

## UI Workflow Methods

### Standard Flow (with Disclaimer)

`process_manual_cease_with_disclaimer(page: Page, reason: str = "Informed Dissent")` automates the full cease workflow including disclaimer steps.

```python
from utils.manual_cease_util import process_manual_cease_with_disclaimer
process_manual_cease_with_disclaimer(page, reason="Moved Away")
```

### Immediate Flow

`process_manual_cease_immediate(page: Page, reason: str = "Informed Dissent")` performs the cease workflow without recording disclaimer letters.

```python
from utils.manual_cease_util import process_manual_cease_immediate
process_manual_cease_immediate(page, reason="Deceased")
```

## DB Verification

The method `verify_manual_cease_db_fields_dynamic(nhs_number: str, expected: dict[str, object])` dynamically validates updated DB fields based on supplied expectations.

### Arguments

  nhs_number:
    Type: str
    NHS number of the subject to validate.

  expected:
    Type: dict[str, object]
    A dictionary mapping human-readable field labels to expected values. Supports assertions like TODAY, NULL, UNCHANGED, or direct values.

### How to use this method

```python
from utils.manual_cease_util import verify_manual_cease_db_fields_dynamic, EXPECT

verify_manual_cease_db_fields_dynamic(nhs_number, {
    "Screening Status": 4008,
    "Screening Status Reason": 43,
    "Ceased Confirmation Date": EXPECT.TODAY,
    "Ceased Confirmation Details": "AUTO TEST: notes"
})
```

## Enums and Constants

### EXPECT markers

Used in DB assertions to express flexible expectations.
  EXPECT.TODAY: Field must match today's date.
  EXPECT.NULL: Field must be null.
  EXPECT.UNCHANGED: Field must exist but is not asserted.
  EXPECT.MATCH_USER_ID: Field must be a valid user ID.

### Status & Reason Enums

The utility includes enums for easier mapping in test code:

```python
from utils.manual_cease_util import ScreeningStatus, ScreeningStatusReason

ScreeningStatus.CEASED        # → 4008
ScreeningStatusReason.DECEASED  # → 45
```

Refer to the source code in `utils/manual_cease_util.py` for additional mappings and helper logic.
