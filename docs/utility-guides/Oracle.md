# Utility Guide: Oracle

The Oracle Utility provides an easy way to interact with an Oracle database directly from your Playwright test suite. It can be used to run SQL queries or stored procedures on the Oracle database.

## When and Why to Use the Oracle Utility

You might use this utility for:

- Running SQL queries or stored procedures on the Oracle database

- Validating application workflows against live database records

- Creating test data dynamically via helper functions

- Verifying data integrity after system events

## Table of Contents

- [Utility Guide: Oracle](#utility-guide-oracle)
  - [When and Why to Use the Oracle Utility](#when-and-why-to-use-the-oracle-utility)
  - [Table of Contents](#table-of-contents)
  - [Using the Oracle Utility](#using-the-oracle-utility)
  - [Required arguments](#required-arguments)
  - [Oracle Utility Methods](#oracle-utility-methods)
  - [Example usage](#example-usage)
  - [Oracle Specific Functions](#oracle-specific-functions)
    - [How to Add New Oracle-Specific Functions](#how-to-add-new-oracle-specific-functions)
    - [Example Usage](#example-usage-1)

## Using the Oracle Utility

To use the Oracle Utility, import the 'OracleDB' class into your test file and then call the OracleDB methods from within your tests, as required.

```python
from utils.oracle.oracle import OracleDB
```

## Required arguments

The functions in this class require different arguments.<br>
Look at the docstrings for each function to see what arguments are required.<br>
The docstrings also specify when arguments are optional, and what the default values are when no argument is provided.

## Oracle Utility Methods

**The main methods provided by OracleDB are:**

- **connect_to_db(self)**: Connects to the Oracle database using credentials from environment variables.
- **disconnect_from_db(self, conn)**: Closes the provided Oracle database connection.
- **execute_query(self, query, params=None)**: Executes a SQL query with optional parameters and returns the results as a pandas DataFrame.
- **execute_stored_procedure(self, `procedure_name`, params=None)**: Executes a named stored procedure with optional parameters.
- **exec_bcss_timed_events(self, nhs_number_df)**: Runs the `bcss_timed_events` stored procedure for each NHS number provided in a DataFrame.
- **get_subject_id_from_nhs_number(self, nhs_number)**: Retrieves the `subject_screening_id` for a given NHS number.
- **create_subjects_via_sspi(...)**: Creates synthetic subjects using stored procedure `PKG_SSPI.p_process_pi_subject`

For full implementation details, see utils/oracle/oracle.py.

## Example usage

```python
from utils.oracle.oracle import OracleDB

def test_oracle_query() -> None:
    query = """
    SELECT column_a,
           column_b,
           column_c
    FROM example_table
    WHERE condition_1 = :condition1
      AND condition_2 = :condition2
    """
    params = {
        "condition1": 101,
        "condition2": 202,
    }
    result_df = OracleDB().execute_query(query, params)
    print(result_df)

def run_stored_procedure() -> None:
    OracleDB().execute_stored_procedure("bcss_timed_events")

def create_subjects_dynamically() -> None:
OracleDB().create_subjects_via_sspi(
    count=5,
    screening_centre="BCS01",
    base_age=60,
    start_offset=-2,
    end_offset=4,
    nhs_start=9200000000
)
```

---

## Oracle Specific Functions

Oracle-specific functions are now organized into separate files under `utils/oracle/oracle_specific_functions/` for better maintainability and discoverability.<br>
Each file groups related functions by their domain or purpose.

Below is a table showing the current structure and which functions are found in each file:

| File Name                                 | Functions/Classes Included                                                                                   |
|--------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| **enums.py**                              | `SqlQueryValues` (common `enum` values for queries)                                                            |
| **kit_management.py**                      | `get_kit_id_from_db`, `get_kit_id_logged_from_db`, `get_service_management_by_device_id`,<br>`update_kit_service_management_entity`, `execute_fit_kit_stored_procedures` |
| **organisation_parameters.py**             | `set_org_parameter_value`, `get_org_parameter_value`, `check_parameter`                                      |
| **screening_colonoscopist.py**             | `build_accredited_screening_colonoscopist_query`, `get_accredited_screening_colonoscopist_in_bcs001`         |
| **subject_address.py**                     | `check_if_subject_has_temporary_address`                                                                     |
| **subject_appointment.py**                 | `get_subjects_for_appointments`, `get_subjects_with_booked_appointments`                                     |
| **subject_batch.py**                       | `get_nhs_no_from_batch_id`                                                                                   |
| **supporting_notes.py**                    | `get_subjects_by_note_count`, `get_supporting_notes`, `get_subjects_with_multiple_notes`                     |
| **investigation_dataset.py**               | `get_investigation_dataset_polyp_category`, `get_investigation_dataset_polyp_algorithm_size`,<br>`get_subjects_for_investigation_dataset_updates` |
| **subject_selector.py**                    | `SubjectSelector` (class for subject selection logic)                                                        |

> **Note:**
> If you are looking for a specific function, check the relevant file in `utils/oracle/oracle_specific_functions/`.
> Common values used in queries are placed in `enums.py` as the `SqlQueryValues` class.

---

### How to Add New Oracle-Specific Functions

- Add your new function to the most appropriate file in `utils/oracle/oracle_specific_functions/`.
- If your function does not fit an existing category, create a new file with a descriptive name.
- Document your function with a clear docstring.
- If your function uses common query values, consider adding them to `enums.py`.
- Once done add the function to the table above

---

### Example Usage

```python
from utils.oracle.oracle import OracleDB
from utils.oracle.oracle_specific_functions.enums import SqlQueryValues

def example_query() -> pd.DataFrame:
    """
    Example function to demonstrate OracleDB usage for querying subject NHS numbers.
    Returns:
        pd.DataFrame: Query results as a pandas DataFrame.
    """
    example_df = OracleDB().execute_query(
        f"""subject_nhs_number
    from ep_subject_episode_t
    where se.latest_event_status_id in ({SqlQueryValues.S10_EVENT_STATUS}, {SqlQueryValues.S19_EVENT_STATUS})""")

    return example_df
```

> **Note:**<br>
> The Oracle utility and its helper functions are available under utils/oracle/.<br>
> See the source code for more details.
