# Utility Guide: Fit Kit Generation

The Fit Kit Generation Utility provides methods to generate and manage FIT test kits for testing purposes.

## Table of Contents

- [Utility Guide: Fit Kit Generation](#utility-guide-fit-kit-generation)
  - [Table of Contents](#table-of-contents)
  - [Using the Fit Kit Generation Utility](#using-the-fit-kit-generation-utility)
  - [Required Arguments](#required-arguments)
  - [Fit Kit Generation Specific Functions](#fit-kit-generation-specific-functions)
  - [Example Usage](#example-usage)

## Using the Fit Kit Generation Utility

To use the Fit Kit Generation Utility, import the `fit_kit_generation` module, from the `utils` directory, into your test file and call its methods from within your tests, as required. To generate the fit kit IDs, the only method required is `create_fit_id_df`. This will return a `dataframe` with all the transformations already taking place.

## Required Arguments

The methods in this utility require specific arguments. Below is a summary of the required arguments for key methods:

- `generate_kit`: Requires `batch_id` (int) and `kit_type` (str).

## Fit Kit Generation Specific Functions

The Fit Kit Generation Utility includes methods for generating, validating, and managing FIT test kits. These methods are designed to streamline the process of creating test kits for various scenarios. Below are some key functions:

1. **`create_fit_id_df(tk_type_id: int, hub_id: int, no_of_kits: int) -> DataFrame`**
   Creates a DataFrame containing FIT kit IDs based on the provided parameters.
   - **Arguments**:
     - `tk_type_id` (int): The type ID of the test kit.
     - `hub_id` (int): The hub ID associated with the kits.
     - `no_of_kits` (int): The number of kits to retrieve.
   - **Returns**: A pandas DataFrame with the FIT kit IDs.

2. **`calculate_check_digit(kit_id: str) -> str`**
   Calculates and appends a check digit to the given kit ID.
   - **Arguments**:
     - `kit_id` (str): The kit ID to process.
   - **Returns**: The kit ID with the appended check digit.

3. **`convert_kit_id_to_fit_device_id(kit_id: str) -> str`**
   Converts a kit ID into a FIT Device ID.
   - **Arguments**:
     - `kit_id` (str): The kit ID to convert.
   - **Returns**: The corresponding FIT Device ID.

## Example Usage

```python
from utils.fit_kit_generation import create_fit_id_df, calculate_check_digit, convert_kit_id_to_fit_device_id

def example_usage() -> None:
    # Example inputs
    tk_type_id = 1
    hub_id = 101
    no_of_kits_to_retrieve = 2

    # Calling the fit_kit_df method will do the following:
      # Step 1: Retrieve and process FIT kit data
      # Step 2: Calculate a check digit for a single kit ID
      # Step 3: Convert a kit ID to a FIT Device ID

    fit_kit_df = create_fit_id_df(tk_type_id, hub_id, no_of_kits_to_retrieve)
    print("Processed FIT Kit DataFrame:")
    print(fit_kit_df)

example_usage()
