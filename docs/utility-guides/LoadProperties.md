# Utility Guide: Load Properties

The Load Properties Utility can be used to retrieve values from a properties file.

## Table of Contents

- [Utility Guide: Load Properties](#utility-guide-load-properties)
  - [Table of Contents](#table-of-contents)
  - [How This Works](#how-this-works)
  - [Adding to the Properties File](#adding-to-the-properties-file)
  - [Using the Load Properties Utility](#using-the-load-properties-utility)
  - [Example Usage](#example-usage)

## How This Works

This utility uses the `jproperties` package to load the properties files.<br>
There is a class `PropertiesFile`, containing the locations of both files:

1. `self.smokescreen_properties_file`: tests/smokescreen/bcss_smokescreen_tests.properties
2. `self.general_properties_file`: tests/bcss_tests.properties

The method `get_properties()` will load either one of these based on the input provided.<br>
To ensure that there are no mistakes when providing this input there are two additional methods to call that will do this for you:

1. `get_smokescreen_properties()`: Which will load `self.smokescreen_properties_file`
2. `get_general_properties()`: Which will load `self.general_properties_file`

## Adding to the Properties File

To add values to the properties file follow the format:

```java
# ----------------------------------
#   Example Values
# ----------------------------------
example_value_1=value1
example_value_2=value2
```

**Reasoning for storing values in the properties file:**

1. Properties files use key-value pairs because they provide a simple, organized, and flexible way to store configuration data.

2. Each line in the file assigns a value to a key (For example, c1_daily_invitation_rate=10). This makes it easy to look up and change values as needed.

3. Using key-value pairs in properties files helps keep your tests clean, flexible, and easy to maintain by avoiding hard-coded values in your test scripts.

**Why avoid hard coded values in tests?**

1. Maintainability: If we need to update a value (like a test organization ID or a rate), we only have to change it in one place—the properties file—instead of searching through all your test code.

2. Reusability: The same test code can be run with different data just by changing the properties file, making your tests more flexible.

3. Separation of Concerns: Test logic stays in your code, while test data and configuration are kept separate in the properties file.

4. Readability: It’s easier to see and manage all your test settings and data in one file.

5. Environment Flexibility: We can have different properties files for different environments (e.g., Development, Test, Production) without changing your test code.

## Using the Load Properties Utility

To use this utility in a test reference the pytest fixture in `conftest.py`.<br>
There is no need to import anything as any fixtures in `conftest.py` will be automatically discovered by pytest.
Here there are two fixtures:

1. `smokescreen_properties` - which is used to load the file: tests/smokescreen/bcss_smokescreen_tests.properties
2. `get_general_properties` - which is used to load the file: tests/bcss_tests.properties

## Example Usage

```python
def test_example_1(page: Page, general_properties: dict) -> None:
    print(
        general_properties["example_value_1"]
    )
```
