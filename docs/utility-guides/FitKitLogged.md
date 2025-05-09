# Utility Guide: Fit Kit Logged Utility

The Fit Kit Logged Utility provides methods to retrieve test data (fit kit test results) used by the compartment 3 tests, and splits them into two dataframes (one 'normal', one 'abnormal').

## Table of Contents

- [Utility Guide: Fit Kit Logged Utility](#utility-guide-fit-kit-logged-utility)
  - [Table of Contents](#table-of-contents)
  - [Using the Fit Kit Logged Utility](#using-the-fit-kit-logged-utility)
  - [Required Arguments](#required-arguments)
  - [Fit Kit Logged Specific Functions](#fit-kit-logged-specific-functions)
  - [Example Usage](#example-usage)

## Using the Fit Kit Logged Utility

To use the Fit Kit Logged Utility, import the `fit_kit_logged.py` module, from the `utils` directory, into your test file and call the `process_kit_data` method as required.

## Required Arguments

The methods in this utility require specific arguments. Below is a summary of the required arguments for key methods:

- `process_kit_data`: Requires `smokescreen_properties`(dict)
- `split_fit_kits`: Requires `kit_id_df`(pd.DataFrame), `smokescreen_properties`(dict)

## Fit Kit Logged Specific Functions

The `fit_kit_logged` Utility includes methods for retrieving FIT test kits from the DB and splitting them into 'Normal' and 'Abnormal' results. Below are their key functions:

1. **`process_kit_data(smokescreen_properties: dict) -> list`**
Retrieves the test data needed for compartment 3 and then splits it into two data frames, using the `split_fit_kits` method.

- **Arguments**:
  - `smokescreen_properties` (dict): A dictionary containing properties required to retrieve and process kit data.

- **Returns**:
  A list of tuples where each tuple contains a device ID (str) and a `boolean` flag (True for normal, False for abnormal).

1. **`split_fit_kits(kit_id_df: pd.DataFrame, smokescreen_properties: dict) -> tuple`**
This method splits the `dataframe` into two dataframes, one normal and one abnormal. It determines the number of normal and abnormal kits by using the `c3_eng_number_of_normal_fit_kits` parameter from `smokescreen_properties` for the number of normal, and then the rest are marked as abnormal.

- **Arguments**:
  - `kit_id_df` (pd.DataFrame): A `dataframe` containing fit kit IDs.
  - `smokescreen_properties` (dict): A dictionary containing the number of normal and abnormal fit kits to split.

- **Returns**:
  A tuple containing two dataframes:
  - `normal_fit_kit_df` (pd.DataFrame): `dataframe` containing normal fit kits.
  - `abnormal_fit_kit_df` (pd.DataFrame): `dataframe` containing abnormal fit kits.

## Example Usage

```python
from utils.fit_kit_logged import process_kit_data

def test_example_usage(smokescreen_properties: dict) -> None:
    # Find data, separate it into normal and abnormal, add results to the test records in the KIT_QUEUE table (i.e. mimic receiving results from the middleware) and get device IDs and their flags.
    device_ids = process_kit_data(smokescreen_properties)
    # Note: In this example, all of the code below this line is for context only and uses functions from other utilities.
    # Retrieve NHS numbers for each device_id and determine normal/abnormal status
    nhs_numbers = []
    normal_flags = []

    for device_id, is_normal in device_ids:
        nhs_number = update_kit_service_management_entity(
            device_id, is_normal, smokescreen_properties
        )
        nhs_numbers.append(nhs_number)
        normal_flags.append(is_normal)  # Store the flag (True for normal, False for abnormal).

test_example_usage()
```
