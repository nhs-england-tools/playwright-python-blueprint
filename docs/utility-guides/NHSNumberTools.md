# Utility Guide: NHS Number Tools

The NHS Number Tools utility provided by this blueprint allows for the easy management of NHS numbers, and provides
common functionality that may apply to many services in relation to NHS Number management.

## Table of Contents

- [Utility Guide: NHS Number Tools](#utility-guide-nhs-number-tools)
  - [Table of Contents](#table-of-contents)
  - [Using the NHS Number Tools class](#using-the-nhs-number-tools-class)
  - [`_nhs_number_checks()`: Checks if the NHS number is valid](#_nhs_number_checks-checks-if-the-nhs-number-is-valid)
    - [Required Arguments](#required-arguments)
    - [Raises](#raises)
  - [Example Usage for `_nhs_number_checks()`](#example-usage-for-_nhs_number_checks)
  - [`spaced_nhs_number()`: Returns Spaced NHS Number](#spaced_nhs_number-returns-spaced-nhs-number)
    - [Required Arguments](#required-arguments-1)
    - [Returns](#returns)
  - [Example Usage for `spaced_nhs_number()`](#example-usage-for-spaced_nhs_number)

## Using the NHS Number Tools class

You can initialise the NHS Number Tools class by using the following code in your test file:

```python
from utils.nhs_number_tools import NHSNumberTools
```

## `_nhs_number_checks()`: Checks if the NHS number is valid

The `_nhs_number_checks()` method does basic checks on NHS number value provided and raises an exception if the number is not valid

### Required Arguments

The following are required for `_nhs_number_checks()`:

| Argument   | Format | Description             |
| ---------- | ------ | ----------------------- |
| nhs_number | `str`  | The NHS number to check |

### Raises

NHSNumberToolsException: If the NHS number is not numeric or not 10 digits long.

## Example Usage for `_nhs_number_checks()`

```python
from utils.nhs_number_tools import NHSNumberTools
    incorrect_nhs_no = "A23456789"
    NHSNumberTools._nhs_number_checks(incorrect_nhs_no)
```

## `spaced_nhs_number()`: Returns Spaced NHS Number

The `spaced_nhs_number()` method is designed to take the provided NHS number and return it in a formatted
string of the format `nnn nnn nnnn`.  It's a static method so can be used in the following way

### Required Arguments

The following are required for `NHSNumberTools.spaced_nhs_number()`:

| Argument   | Format         | Description               |
| ---------- | -------------- | ------------------------- |
| nhs_number | `str` or `int` | The NHS number to format. |

### Returns

A `str` with the provided NHS number in `nnn nnn nnnn` format. For example, `NHSNumberTools.spaced_nhs_number(1234567890)` would return `123 456 7890`.

## Example Usage for `spaced_nhs_number()`

```python
from utils.nhs_number_tools import NHSNumberTools
# Return formatted NHS number
    spaced_nhs_number = NHSNumberTools.spaced_nhs_number("1234567890")
```
