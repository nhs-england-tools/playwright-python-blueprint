# Utility Guide: Oracle

The Oracle Utility provides an easy way to interact with an Oracle database directly from your Playwright test suite.It can be used to run SQL queries or stored procedures on the Oracle database.

## When and Why to Use the Oracle Utility

You might need to use this utility in scenarios such as:

- To run SQL queries or stored procedures on the Oracle database.
- Verifying that data is correctly written to or updated in the database after a workflow is completed in your application.

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
```

---

## Oracle Specific Functions

This contains SQL queries that can be used to run tests.<br>
These are all stored in one location to make it easier to edit the query at a later date and to make it accessible to multiple tests.

Common values are placed in the `SqlQueryValues` class to avoid repeating the same values in the queries.

## How to Add New Oracle-Specific Functions

- Define a new function in `utils/oracle/oracle_specific_functions.py`.
- Create your SQL query, `parameterizing` as needed.
- Call the  relevant methods from the oracle `util` based on your needs (e.g., `execute_query`, stored procedure methods, etc.).
- Return the result in the appropriate format for your function.
- Document the function with a clear docstring.

## Example Usage

```python
from utils.oracle.oracle import OracleDB

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
