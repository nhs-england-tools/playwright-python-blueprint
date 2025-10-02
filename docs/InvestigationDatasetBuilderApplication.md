# Investigation Dataset Builder Application

This application is a Streamlit-based tool for interactively building investigation dataset definitions for use with the `complete_dataset_with_args` method in the `InvestigationDatasetCompletion` class. It allows users to select and configure dataset sections, fill in fields, and copy the resulting Python code (including necessary `Enum` imports) for use in their tests.

---

## Table of Contents

- [Investigation Dataset Builder Application](#investigation-dataset-builder-application)
  - [Table of Contents](#table-of-contents)
  - [How to Use the Application](#how-to-use-the-application)
    - [What this can be used for](#what-this-can-be-used-for)
    - [Pre-requisites](#pre-requisites)
    - [Launching the App](#launching-the-app)
    - [Selecting and Filling Sections](#selecting-and-filling-sections)
    - [Viewing and Copying Output](#viewing-and-copying-output)
  - [Maintaining the Application](#maintaining-the-application)
    - [Overview of `dataset_fields.json`](#overview-of-dataset_fieldsjson)
    - [JSON Field Options Reference](#json-field-options-reference)
    - [Adding a New Section](#adding-a-new-section)
      - [Adding a Section with Drugs](#adding-a-section-with-drugs)
    - [Registering a Section Renderer](#registering-a-section-renderer)
    - [Editing or Removing Sections and Fields](#editing-or-removing-sections-and-fields)
    - [Purpose of "groups" and "fields"](#purpose-of-groups-and-fields)
    - [Adding New `Enum` Types](#adding-new-enum-types)
    - [Adding Custom Types](#adding-custom-types)
    - [Available Section Renderers](#available-section-renderers)
    - [Troubleshooting](#troubleshooting)
  - [Example Section Entry in `dataset_fields.json`](#example-section-entry-in-dataset_fieldsjson)
  - [Summary](#summary)

---

## How to Use the Application

### What this can be used for

This application can be used to create the necessary dictionaries in order to populate an investigation dataset<br>
During the conversion on the automation tests from selenium to playwright it can be used for the following feature file steps (There are more but these are just examples):

- And I add the following bowel preparation drugs and values within the Investigation Dataset for this subject:
- And I set the following fields and values within the Investigation Dataset for this subject:

### Pre-requisites

Before running the application, ensure you have the following:

- Python 3.10 or later installed.
- **It is strongly recommended to use a Python virtual environment.**<br>
  To create and activate a virtual environment, follow the steps in the [README](../README.md#2-set-up-a-virtual-environment-recommended).
- All required Python packages installed. This can be done with `pip install -r requirements.txt` or `pip install -r ./requirements.txt`.

---

### Launching the App

1. **Open a terminal** in the project root directory.
2. Run the following command: `streamlit run investigation_dataset_ui.py`
3. The app will open in your default web browser.
4. You can also copy and paste the `Local URL` into a browser to access the app.

---

### Selecting and Filling Sections

- Use the **sidebar** on the left to select the section you want to work on (e.g., General Information, Drug Information, Endoscopy Information, etc.).
- For each section:
  - The relevant fields will be displayed.
  - Fill in the required fields. Optional fields can be added by ticking their checkbox.
  - For sections with drug groups or repeated entries, use the number input to specify how many entries you want, and fill in each entry as prompted.
  - Conditional fields will only appear when their conditions are met (e.g., if you select "Yes" for a parent field).

---

### Viewing and Copying Output

- As you fill in fields, the **output code block** at the bottom of each section updates in real time.
- This code block includes:
  - The necessary `Enum` imports for the section.
  - The Python dictionary representing your filled section.
- To use this output:
  - Select the whole code block manually and copy it, or use the copy button if available.
  - Paste the code into your test as needed.

---

## Maintaining the Application

### Overview of `dataset_fields.json`

The file `investigation_dataset_ui_app/dataset_fields.json` defines all available sections and their fields, including types, descriptions, and options.<br>
Each section is a JSON object with either a `"fields"` array (for normal sections) or a `"groups"` array (for drug sections).

---

### JSON Field Options Reference

Each field in the JSON can use the following options:

- `"key"`:<br>
  The unique identifier for the field.<br>
  Example: `"site"`, `"drug_typeX"`, `"drug_doseX"`

- `"type"`:<br>
  The type of the field.<br>
  Allowed values:
  - `"string"`: Free text input.
  - `"integer"`: Integer input.
  - `"integer_or_none"`: Integer input or None (empty).
  - `"float"`: Floating-point input.
  - `"date"` or `"datetime"`: Date input.
  - `"bool"`: Checkbox input.
  - `"yes_no"`: Dropdown with "yes" and "no".
  - `"therapeutic_diagnostic"`: Dropdown with "therapeutic" and "diagnostic".
  - `"time"`: Time input in HH:MM format.
  - `"multiselect"`: Multi-select dropdown (requires `"options"`).
  - `Enum` type name (e.g., `"DrugTypeOptions"`, `"YesNoOptions"`): Dropdown with `enum` values.
  - **Custom types**: See [Adding Custom Types](#adding-custom-types) below.<br>

- `"description"`:<br>
  A clear description of the field, shown in the UI.

- `"optional"`:<br>
  `true` or `false`.<br>
  If `true`, the field is optional and can be toggled with a checkbox.

- `"range"`:<br>
  For numeric fields, specifies allowed values.<br>
  Example: `"range": [-1, 10]`

- `"default"`:<br>
  The default value for the field.

- `"options"`:<br>
  For `"multiselect"` fields, a list of allowed values.

- `"multiple"`:<br>
  For drug fields, set to `true` to allow multiple entries (used with `"key": "drug_typeX"` and `"drug_doseX"`).

- `"conditional_on"`:<br>
  Used for conditional fields.<br>
  Example:<br>

  ```json
  "conditional_on": {
    "field": "left in situ",
    "value": "YesNoOptions.YES"
  }
  ```

  The field will only be shown if the referenced field matches the value.

- `"list"`:<br>
  If present and true, indicates the section is a list of entries (e.g., `polyp_information`).

- `"nested_list"`:<br>
  If present and true, indicates the section is a nested list (e.g., `polyp_intervention`).

---

### Adding a New Section

#### Adding a Section with Drugs

1. Add a new object to the JSON root with the section name as the key.
2. Add a `"groups"` array. Each group should have:
    - `"label"`: The group label shown in the UI.
    - `"fields"`: An array of drug fields, typically with keys like `"drug_typeX"` and `"drug_doseX"`, and `"multiple": true`.
3. Optionally, add a `"fields"` array for single-entry fields in the section.
4. Example:

   ```json
   "tagging_agent_given_drug_information": {
     "groups": [
       {
         "label": "Tagging Agent Drugs",
         "fields": [
           {
             "key": "drug_typeX",
             "type": "DrugTypeOptions",
             "description": "Tagging Agent Drug Type",
             "optional": true,
             "multiple": true
           },
           {
             "key": "drug_doseX",
             "type": "string",
             "description": "Tagging Agent Drug Dose",
             "optional": true,
             "multiple": true
           }
         ]
       }
     ]
   }
   ```

5. Save the file.

6. **Add the section to the sidebar:**<br>
   Add the section name to the `SECTIONS` list in `investigation_dataset_ui.py`.

7. **Register the section renderer:**<br>
   Add the section to the `SECTION_RENDERERS` dictionary in `investigation_dataset_ui.py`, using `show_drug_group_section_with_imports` as the renderer:

    ```python
   SECTION_RENDERERS = {
       ...
       "tagging_agent_given_drug_information": show_drug_group_section_with_imports,
       ...
   }
   ```

#### Adding a Normal Section

1. Add a new object to the JSON root with the section name as the key.
2. Add a `"fields"` array containing field definitions.
3. Each field should include:
    - `"key"`: The unique identifier for the field.
    - `"type"`: The type of the field (see above).
    - `"description"`: A clear description of the field.
    - `"optional"`: `true` or `false`.
    - Other keys as needed (`"range"`, `"default"`, `"conditional_on"`, etc.).
4. Example:

   ```json
   "general_information": {
     "fields": [
       {
         "key": "site",
         "type": "integer",
         "range": [-1, 10],
         "description": "Index for site lookup dropdown",
         "optional": false
       }
     ]
   }
   ```

5. Save the file.

6. **Add the section to the sidebar:**<br>
   Add the section name to the `SECTIONS` list in `investigation_dataset_ui.py`.

7. **Register the section renderer:**<br>
   Add the section to the `SECTION_RENDERERS` dictionary in `investigation_dataset_ui.py`, using `show_section_with_imports` as the renderer:

   ```python
   SECTION_RENDERERS = {
       ...
       "general_information": show_section_with_imports,
       ...
   }
   ```

---

### Registering a Section Renderer

Whenever you add a new section, you must register it in the `SECTION_RENDERERS` dictionary in `investigation_dataset_ui.py`.<br>
This dictionary maps section names to the appropriate rendering function.

- For normal sections, use `show_section_with_imports`.
- For drug group sections, use `show_drug_group_section_with_imports`.
- For complex/nested sections (e.g., polyp_information_and_intervention_and_histology), use a custom renderer or a lambda if the function does not accept arguments.

Example:

```python
SECTION_RENDERERS = {
    "general_information": show_section_with_imports,
    "drug_information": show_drug_group_section_with_imports,
    "polyp_information_and_intervention_and_histology": lambda _: show_polyp_information_and_intervention_and_histology(),
    ...
}
```

---

### Editing or Removing Sections and Fields

- **To edit a field or section:**<br>
  Find the relevant field or section and update its properties (e.g., `"description"`, `"type"`, `"optional"`, etc.).<br>
  Save the file and reload the app.

- **To remove a field or section:**<br>
  Delete the field object from the `"fields"` array or the section object from the root.<br>
  Save the file and reload the app.<br>
  Remove the section from `SECTIONS` and `SECTION_RENDERERS` if you want to fully remove it from the UI.

---

### Purpose of "groups" and "fields"

- **"fields"**:<br>
  Used for normal sections and for single-entry fields in drug sections.<br>
  Each field in `"fields"` is rendered as a single input in the UI.

- **"groups"**:<br>
  Used for sections that allow multiple drug entries (e.g., Drug Information, Tagging Agent Given Drug Information, Contrast Tagging and Drug).<br>
  Each group contains a `"label"` and a `"fields"` array.<br>
  Fields with `"key": "drug_typeX"` and `"drug_doseX"` and `"multiple": true` are rendered as repeated entries, with the user specifying how many drugs to enter.

---

### Adding New `Enum` Types

If you add new `Enum` types to `pages.datasets.investigation_dataset_page`, you must also:

- Add the `Enum` to the `ENUM_MAP` in `investigation_dataset_ui.py`:

  ```python
  ENUM_MAP = {
      ...
      "NewEnumType": NewEnumType,
  }
  ```

- Use the `Enum` type name in the `"type"` field of any relevant field in `dataset_fields.json`.

---

### Adding Custom Types

You can add custom types for fields that do not fit the standard types or enums.<br>
Examples include `"yes_no"` and `"therapeutic_diagnostic"`, which are handled as special dropdowns in the UI.

**To add a custom type:**

1. Choose a unique string for `"type"` (e.g., `"yes_no"`, `"therapeutic_diagnostic"`).
2. In your JSON field definition, set `"type"` to this string.
3. Ensure your `render_field` function in `investigation_dataset_ui.py` has a case for your custom type, rendering the appropriate widget (usually a dropdown/selectbox).
   - For `"yes_no"`, the UI will show a dropdown with "yes" and "no".
   - For `"therapeutic_diagnostic"`, the UI will show a dropdown with "therapeutic" and "diagnostic".
4. You can add more custom types by extending the `render_field` function with new cases in the `match-case` or `if` dispatch.

**Example:**

`dataset_fields.json`:

```json
{
  "key": "procedure type",
  "type": "therapeutic_diagnostic",
  "description": "If it was a procedure or diagnostic testing",
  "optional": false
}
```

`investigation_dataset_ui.py`, `render_field`:

```python
case "therapeutic_diagnostic":
    return _render_selectbox_field(
        key, desc, optional, widget_key, field, ["therapeutic", "diagnostic"]
    )
```

---

### Available Section Renderers

There are several renderers available for displaying sections in the UI.<br>
Choose the appropriate renderer based on the section's structure:

- **show_section_with_imports**<br>
  Use for standard sections that only have a `"fields"` array.<br>
  Renders all fields and outputs the code block with necessary imports.

- **show_drug_group_section_with_imports**<br>
  Use for sections that contain drug groups (i.e., have a `"groups"` array).<br>
  Renders each drug group, allows multiple entries, and outputs the code block with necessary imports.

- **show_polyp_information_and_intervention_and_histology**<br>
  Use for the polyp section, which is a complex/nested structure.<br>
  Outputs code blocks for polyp information, interventions, and histology, along with necessary imports.

- **Custom Renderers**<br>
  For any section with unique requirements, you can create a custom renderer function and register it in `SECTION_RENDERERS`.<br>
  If your renderer does not accept a section name argument, wrap it in a lambda:

  ```python
  "polyp_information_and_intervention_and_histology": lambda _: show_polyp_information_and_intervention_and_histology(),
  ```

---

### Troubleshooting

- **A section does not appear in the sidebar:**
  - Ensure it is listed in the `SECTIONS` array in `investigation_dataset_ui.py`.
  - Ensure the section exists in `dataset_fields.json`.
  - Ensure the section is registered in `SECTION_RENDERERS`.

- **A field does not appear in the UI:**
  - Check for typos in the field definition.
  - Ensure conditional fields have correct `"conditional_on"` logic.

- **`Enum` import is missing in the output:**
  - Ensure the field `"type"` matches an entry in `ENUM_MAP`.

- **App does not reload changes:**
  - Save your changes and refresh the `Streamlit` app in your browser.

- **Copy to clipboard does not work:**
  - Some browsers may not support auto-copy. Manually select and copy the code from the code block.

---

## Example Section Entry in `dataset_fields.json`

```json
"drug_information": {
  "groups": [
    {
      "label": "Bowel Preparation Administered Drugs",
      "fields": [
        {
          "key": "drug_typeX",
          "type": "DrugTypeOptions",
          "description": "Bowel Preparation Drug Type",
          "optional": true,
          "multiple": true
        },
        {
          "key": "drug_doseX",
          "type": "string",
          "description": "Bowel Preparation Drug Dose",
          "optional": true,
          "multiple": true
        }
      ]
    }
  ]
}
```

---

## Summary

- **All configuration is driven by `dataset_fields.json`.**
- **Descriptions, types, and options are fully customizable.**
- **No code changes are needed for most updates—just edit the JSON file.**
- **For new `Enum` types, add them to both the Python code and the JSON.**
- **For conditional fields, use the `"conditional_on"` property.**
- **Use `"groups"` for repeated drug entries, and `"fields"` for single-entry fields.**
- **Register new sections in both `SECTIONS` and `SECTION_RENDERERS`.**
- **Choose the correct renderer for your section structure.**
- **The output code block includes all necessary imports for easy integration.**
