# Utility Guide: Call and Recall

The **Call and Recall utility** provides helper methods for executing Call and Recall stored procedures in BCSS.<br>
These utilities interact directly with the **OracleDB** backend to run failsafe checks and initiate FOBT screening invitations.

## Table of Contents

- [Utility Guide: Call and Recall](#utility-guide-call-and-recall)
  - [Table of Contents](#table-of-contents)
  - [Summary of Utility Methods](#summary-of-utility-methods)
  - [Main Methods](#main-methods)
    - [`run_failsafe`](#run_failsafe)
    - [`invite_subject_for_fobt_screening`](#invite_subject_for_fobt_screening)
  - [Prerequisites](#prerequisites)
  - [Supporting Classes](#supporting-classes)
  - [Example Usage](#example-usage)

---

## Summary of Utility Methods

| Method                                 | Purpose                                                                 | Key Arguments                        | Expected Behaviour |
|----------------------------------------|-------------------------------------------------------------------------|--------------------------------------|--------------------|
| `run_failsafe`                         | Runs the **failsafe trawl** for a given subject.                        | `nhs_no` (`str`)                     | Executes stored procedure `pkg_fobt_call.p_failsafe_trawl` and checks success. |
| `invite_subject_for_fobt_screening`    | Transitions a subject into an **invited state** for FOBT screening.     | `nhs_no` (`str`), `user_role` (`UserRoleType`) | Executes database transition (ID `58`) to create an FOBT episode. |

---

## Main Methods

### `run_failsafe`

Runs the failsafe trawl stored procedure for a subject identified by their NHS number.

**Arguments:**

- `nhs_no` (`str`): The NHS number of the subject.

**How it works:**

1. Looks up the subject ID for the provided NHS number.
2. Connects to the OracleDB with a 30-second call timeout.
3. Executes `pkg_fobt_call.p_failsafe_trawl`.
4. Asserts that the stored procedure reports success.
5. Cleans up database connections and cursors.
6. Logs success/failure.

**Raises:**

- `AssertionError` if the stored procedure does not report success.
- Database connection errors if OracleDB cannot be accessed.

---

### `invite_subject_for_fobt_screening`

Transitions the subject into an **invited state** for FOBT screening.

**Arguments:**

- `nhs_no` (`str`): The NHS number of the subject.
- `user_role` (`UserRoleType`): The role of the user initiating the transition.

**How it works:**

1. Resolves the subject ID for the given NHS number.
2. Fetches the **PIO user ID** for the given `user_role` from the `UserRepository`.
3. Creates a `DatabaseTransitionParameters` object with:
   - `transition_id = 58` (invite to FOBT screening),
   - `subject_id` for the subject,
   - `user_id` of the PIO,
   - `rollback_on_failure = 'Y'`.
4. Executes the transition using `GeneralRepository`.
5. Logs success/failure.

**Raises:**

- `oracledb.DatabaseError` if the stored procedure execution fails.

---

## Prerequisites

Before using the Call and Recall utility, ensure that the following prerequisites are met:

1. **Database Access**: The utility requires access to the OracleDB instance where the relevant stored procedures are defined.

2. **NHS Number**: A valid NHS number must be provided for the subject being processed.

3. **Environment Variables**: As this utility relies on the `UserTools` utility you must ensure that you have correctly created and populated a `local.env` file. For more information on this [See the README](../../README.md)

---

## Supporting Classes

These classes are required by the utility:

- `OracleDB` — Provides database connection and helper functions (e.g. resolve subject ID from NHS number).
- `GeneralRepository` — Executes transitions in the database.
- `DatabaseTransitionParameters` — Holds configuration for a transition (IDs, rollback policy).
- `UserRoleType` — Enum-like class describing different user roles.
- `UserRepository` — Maps user roles to PIO IDs.

---

## Example Usage

```python
from utils.user_tools import UserTools
from utils.call_and_recall_utils import CallAndRecallUtils

# Log in with a user and populate the user_role variable
user_role = UserTools.user_login(
    page, "Hub Manager State Registered at BCS01", return_role_type=True
)

# Create the utility
call_and_recall = CallAndRecallUtils()

# Example 1: Run failsafe for a subject
call_and_recall.run_failsafe("9434765919")

# Example 2: Invite a subject to FOBT screening
call_and_recall.invite_subject_for_fobt_screening(
    nhs_no="9434765919",
    user_role=user_role,
)
```
