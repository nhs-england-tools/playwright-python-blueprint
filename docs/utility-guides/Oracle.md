# Utility Guide: Oracle

The Oracle Utility can be used to run SQL queries or stored procedures on the Oracle database.

## Table of Contents

- [Utility Guide: Oracle](#utility-guide-oracle)
  - [Table of Contents](#table-of-contents)
  - [Using the Oracle Utility](#using-the-oracle-utility)
  - [Required arguments](#required-arguments)
  - [Example usage](#example-usage)
  - [Oracle Specific Functions](#oracle-specific-functions)
  - [Example Usage](#example-usage-1)

## Using the Oracle Utility

To use the Oracle Utility, import the 'OracleDB' class into your test file and then call the OracleDB methods from within your tests, as required.

## Required arguments

The functions in this class require different arguments.<br>
Look at the docstrings for each function to see what arguments are required.<br>
The docstrings also specify when arguments are optional, and what the default values are when no argument is provided.

## Example usage

    from utils.oracle.oracle import OracleDB

    def test_oracle_query() -> None:

        query = """select column_a,
        column_b,
        column_c
        from example_table
        where condition_1 = :condition1
        and condition_2 = :condition2"""

        params = {
        "condition1": 101,
        "condition2": 202,
        }

        result_df = OracleDB().execute_query(query, params)

    def run_stored_procedure() -> None:

        OracleDB().execute_stored_procedure("bcss_timed_events")

## Oracle Specific Functions

This contains SQL queries that can be used to run tests.<br>
These are all stored in one location to make it easier to edit the query at a later date and to make it accessible to multiple tests.

Common values are placed in the `SqlQueryValues` class to avoid repeating the same values in the queries.

## Example Usage

    from oracle.oracle import OracleDB

    def example_query() -> pd.DataFrame:

        example_df = OracleDB().execute_query(
            f"""subject_nhs_number
        from ep_subject_episode_t
        where se.latest_event_status_id in ({SqlQueryValues.S10_EVENT_STATUS}, {SqlQueryValues.S19_EVENT_STATUS})""")

        return example_df
