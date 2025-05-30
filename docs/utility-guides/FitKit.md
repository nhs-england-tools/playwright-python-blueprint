# Utility Guide: Fit Kit Utility

This guide covers both the Fit Kit Generation and Fit Kit Logged utilities, which together provide methods to generate, manage, and process FIT test kits for testing purposes.

## Table of Contents

- [Utility Guide: Fit Kit Utility](#utility-guide-fit-kit-utility)
  - [Table of Contents](#table-of-contents)
  - [Fit Kit Generation Utility](#fit-kit-generation-utility)
    - [Overview](#overview)
    - [How to Use](#how-to-use)
    - [Required Arguments](#required-arguments)
    - [Key Methods](#key-methods)
    - [Example Usage](#example-usage)
  - [Fit Kit Logged Utility](#fit-kit-logged-utility)
    - [Overview](#overview-1)
    - [How to Use](#how-to-use-1)
    - [Required Arguments](#required-arguments-1)
    - [Key Methods](#key-methods-1)
    - [Example Usage](#example-usage-1)
      - [1st Example - Basic](#1st-example---basic)
      - [2nd Example - Compartment 3](#2nd-example---compartment-3)

---

## Fit Kit Generation Utility

### Overview

The Fit Kit Generation Utility (`FitKitGeneration` class) provides methods to generate and manage FIT test kits for testing purposes. It retrieves kit IDs from the database, calculates check digits, and formats them as FIT Device IDs ready for use in tests.

### How to Use

Import the `FitKitGeneration` class from `utils/fit_kit.py` and use its methods to generate and process FIT kit IDs.

```python
from utils.fit_kit import FitKitGeneration
```

### Required Arguments

- `create_fit_id_df`: Requires `tk_type_id` (int), `hub_id` (int), and `no_of_kits_to_retrieve` (int).

### Key Methods

1. **`create_fit_id_df(tk_type_id: int, hub_id: int, no_of_kits_to_retrieve: int) -> pd.DataFrame`**
   - Retrieves kit IDs from the database, calculates check digits, and generates FIT Device IDs.
   - **Returns:** A pandas DataFrame with the processed FIT Device IDs.

2. **`calculate_check_digit(kit_id: str) -> str`**
   - Calculates and appends a check digit to the given kit ID.

3. **`convert_kit_id_to_fit_device_id(kit_id: str) -> str`**
   - Converts a kit ID into a FIT Device ID by appending an expiry date and a fixed suffix.

> **Tip:**
> To obtain a pandas DataFrame containing a list of FIT Kits to use, you only need to call the `create_fit_id_df` method. This method internally calls the other two methods to generate the correct check digits and expiration tags.

### Example Usage

```python
from utils.fit_kit import FitKitGeneration

def example_usage() -> None:
    tk_type_id = 2
    hub_id = 101
    no_of_kits_to_retrieve = 2

    fit_kit_gen = FitKitGeneration()
    fit_kit_df = fit_kit_gen.create_fit_id_df(tk_type_id, hub_id, no_of_kits_to_retrieve)
    print("Processed FIT Kit DataFrame:")
    print(fit_kit_df)
```

---

## Fit Kit Logged Utility

### Overview

The Fit Kit Logged Utility (`FitKitLogged` class) provides methods to retrieve test data (fit kit test results) used by the compartment 3 tests, and splits them into two dataframes: one for 'normal' results and one for 'abnormal' results.

### How to Use

Import the `FitKitLogged` class from `utils/fit_kit.py` and use its methods to process and split FIT kit data.

```python
from utils.fit_kit import FitKitLogged
```

### Required Arguments

- `process_kit_data`: Requires `smokescreen_properties` (dict)
- `split_fit_kits`: Requires `kit_id_df` (pd.DataFrame), `smokescreen_properties` (dict)

### Key Methods

1. **`process_kit_data(smokescreen_properties: dict) -> list`**
   - Retrieves test data for compartment 3 and splits it into normal and abnormal kits using `split_fit_kits`.
   - **Returns:** A list of tuples, each containing a device ID (str) and a `boolean` flag (`True` for normal, `False` for abnormal).

2. **`split_fit_kits(kit_id_df: pd.DataFrame, smokescreen_properties: dict) -> tuple[pd.DataFrame, pd.DataFrame]`**
   - Splits the DataFrame into two: one for normal kits and one for abnormal kits, based on the numbers specified in `smokescreen_properties`.
   - **Returns:** A tuple containing two DataFrames: `(normal_fit_kit_df, abnormal_fit_kit_df)`.

> **How it works:**
>
> - The number of normal and abnormal kits is determined by the `c3_eng_number_of_normal_fit_kits` and `c3_eng_number_of_abnormal_fit_kits` keys in the `smokescreen_properties` dictionary.
> - The utility retrieves the required number of kits, splits them, and returns device IDs with their normal/abnormal status.

### Example Usage

#### 1st Example - Basic

This example is showing how the utility can be used to get a pandas `dataframe` containing a list of normal / abnormal kits.

```python
from utils.fit_kit import FitKitLogged

def test_example_usage(smokescreen_properties: dict) -> None:
    fit_kit_logged = FitKitLogged()
    # Retrieve and split FIT kit data
    device_ids = fit_kit_logged.process_kit_data(smokescreen_properties)
    # Example: process device IDs and their normal/abnormal status
    for device_id, is_normal in device_ids:
        print(f"Device ID: {device_id}, Normal: {is_normal}")
```

#### 2nd Example - Compartment 3

This example is showing how we are using this utility in compartment 3.

```python
from utils.fit_kit import FitKitLogged
from utils.oracle.oracle_specific_functions import update_kit_service_management_entity

def test_compartment_3(page: Page, smokescreen_properties: dict):
    device_ids = FitKitLogged().process_kit_data(smokescreen_properties)
    nhs_numbers = []
    normal_flags = []

    for device_id, is_normal in device_ids:
        nhs_number = update_kit_service_management_entity(
            device_id, is_normal, smokescreen_properties
        )
        nhs_numbers.append(nhs_number)
        normal_flags.append(is_normal)
```

---

For more details on each method's implementation, refer to the source code in `utils/fit_kit.py`.
