# Utility Guide: Dataset Field Utility

The Dataset Field utility allows for selecting different locators dynamically.<br>
For example, on the investigation dataset, if we want to select the input locator for the `Start of intubation time` field, we can do this by providing the utility with the name of the field

    DatasetFieldUtil(page).populate_input_locator_for_field(
        "Start of intubation time", "09:00"
    )

## Table of Contents

- [Utility Guide: Dataset Field Utility](#utility-guide-dataset-field-utility)
  - [Table of Contents](#table-of-contents)
  - [Using the DatasetFieldUtil class](#using-the-datasetfieldutil-class)
    - [Required Args](#required-args)
    - [How to use this method](#how-to-use-this-method)

## Using the DatasetFieldUtil class

You can initialise the DatasetFieldUtil class by using the following code in your test file:

    from utils.dataset_field_util import DatasetFieldUtil

This will allow you to use the following methods:

1. populate_input_locator_for_field
   1. This will allow you to populate the field next to the given text where the type is `input`
2. populate_select_locator_for_field
   1. This will allow you to populate the field next to the given text where the type is `select`
3. populate_input_locator_for_field_inside_div
   1. This will allow you to populate the field next to the given text where the type is `input`, and inside of a specified container
4. populate_select_locator_for_field_inside_div
   1. This will allow you to populate the field next to the given text where the type is `select`, and inside of a specified container

### Required Args

`populate_input_locator_for_field` / `populate_select_locator_for_field`

- text:
  - Type: `str`
  - The text of the element you want to interact with.
- value/option:
  - Type: `str`
  - The value or option you want to input / select (depending on what method is called)

`populate_input_locator_for_field_inside_div` / `populate_select_locator_for_field_inside_div`

- text:
  - Type: `str`
  - The text of the element you want to interact with.
- div:
  - Type: `str`
  - The ID of the container that the element belongs in.
- value/option:
  - Type: `str`
  - The value or option you want to input / select (depending on what method is called)

### How to use this method

To use this method simply import the DatasetFieldUtil class and call one of the methods, providing the necessary arguments.<br>
The example below is using options that can be imported from `pages.datasets.investigation_dataset_page`

    from utils.dataset_field_util import DatasetFieldUtil
    from pages.datasets.investigation_dataset_page import (
    InsufflationOptions,
    PolypClassificationOptions,
    )

    # populate_input_locator_for_field
    DatasetFieldUtil(page).populate_input_locator_for_field(
        "End time of procedure", "09:30"
    )

    # populate_select_locator_for_field
    DatasetFieldUtil(page).populate_select_locator_for_field(
        "Insufflation", InsufflationOptions.AIR
    )

    # populate_input_locator_for_field_inside_div
    DatasetFieldUtil(page).populate_input_locator_for_field_inside_div(
        "Estimate of whole polyp size", "divPolypNumber1Section", "15"
    )

    # populate_select_locator_for_field_inside_div
    DatasetFieldUtil(page).populate_select_locator_for_field_inside_div(
        "Classification", "divPolypNumber1Section", PolypClassificationOptions.IS
    )
