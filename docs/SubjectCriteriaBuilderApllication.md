# Subject Criteria Builder Application

This application is a Streamlit-based tool for interactively building subject selection criteria for the NHS BCSS system. It allows users to search, select, and configure criteria keys, view descriptions, choose from allowed values, and copy the resulting criteria as JSON. It also generates the corresponding SQL query and, if required, allows you to select a user or enter a subject's NHS number to populate the query context.

---

## Table of Contents

- [Subject Criteria Builder Application](#subject-criteria-builder-application)
  - [Table of Contents](#table-of-contents)
  - [How to Use the Application](#how-to-use-the-application)
    - [Pre-requisites](#pre-requisites)
    - [Launching the App](#launching-the-app)
    - [Searching for Criteria](#searching-for-criteria)
    - [Selecting and Configuring a Criterion](#selecting-and-configuring-a-criterion)
    - [User and Subject Dependencies](#user-and-subject-dependencies)
    - [Copying the Criteria](#copying-the-criteria)
    - [Resetting the Builder and Hiding Criteria](#resetting-the-builder-and-hiding-criteria)
  - [Maintaining the Application](#maintaining-the-application)
    - [Updating `criteria.json`](#updating-criteriajson)
      - [To add a new criterion](#to-add-a-new-criterion)
      - [To edit a criterion](#to-edit-a-criterion)
      - [To remove a criterion](#to-remove-a-criterion)
      - [About the `dependencies` field](#about-the-dependencies-field)
    - [Adding New Criteria Keys](#adding-new-criteria-keys)
    - [Editing Allowed Values or Descriptions](#editing-allowed-values-or-descriptions)
    - [Troubleshooting](#troubleshooting)
  - [Example Entry in `criteria.json`](#example-entry-in-criteriajson)
  - [Summary](#summary)

---

## How to Use the Application

### Pre-requisites

Before running the application, you must create a `local.env` file containing your Oracle database credentials.<br>
You can generate a template for this file by running:

```bash
python setup_env_file.py
```

After running the script, open the generated `local.env` file and populate the following fields with your Oracle credentials:

```env
ORACLE_USERNAME=your_oracle_username
ORACLE_DB=your_oracle_db
ORACLE_PASS=your_oracle_password
```

These credentials are required for the application to connect to the Oracle database and populate user and subject objects.

---

### Launching the App

1. **Open a terminal** in the project root directory.
2. Run the following command:  `streamlit run subject_criteria_builder.py`
3. The app will open in your default web browser.
4. You can also copy and paste the `Local URL` into a browser to access the app.

---

### Searching for Criteria

- Use the **search bar** at the top to filter criteria keys by name or description.
- The list updates as you type, showing only matching criteria.
- You can hide or show the search bar and criteria list using the "Hide Criteria/Search" and "Show Criteria/Search" buttons at the top.

---

### Selecting and Configuring a Criterion

1. **Expand a criterion** by clicking the ➕ button next to its name.
2. The expanded section shows:
   - **Description:** An explanation of what the key is and what input is expected.
   - **Dropdown:** If the key has a set of allowed values (from `criteria.json`), a dropdown will appear for you to select from.
   - **Text Input:** You can always enter a custom value, even if a dropdown is present.
3. **Collapse** the criterion by clicking the ✖ button.

---

### User and Subject Dependencies

Some criteria require additional context, such as a User or Subject object.<br>
If you select a criterion that has a dependency on "User" or "Subject" (as defined in `criteria.json`):

- **User Dependency:**
  - A section will appear allowing you to select a user from the list defined in `users.json`.
  - Once selected, the user's name and username are displayed, and a populated user object is created for use in the SQL query.

- **Subject Dependency:**
  - A section will appear allowing you to enter a subject's NHS number.
  - Once entered, the application will attempt to populate a subject object using this NHS number for use in the SQL query.

These sections will remain visible as long as any selected criteria require them.

---

### Copying the Criteria

- As you configure criteria, the **Final Criteria Dictionary** at the bottom updates in real time.
- To copy the criteria you can either select the whole code block manually or click on the copy button that is at the top right of this code block.

---

### Resetting the Builder and Hiding Criteria

- Click the **🔄 Reset Criteria Builder** button at the top to clear all selections and start over.
- Use the **🙈 Hide Criteria/Search** and **👁️ Show Criteria/Search** buttons to hide or show the search bar and criteria list.

---

## Maintaining the Application

### Updating `criteria.json`

The file `subject_criteria_builder/criteria.json` defines all available criteria keys, their descriptions, allowed values, and dependencies.

Each entry in the file looks like this:

```json
{
  "key": "NHS_NUMBER",
  "value_source": "",
  "notes": "Enter the 10-digit NHS Number of the subject you want to search for."
}
```

Or, with allowed values and dependencies:

```json
{
  "key": "SUBJECT_HUB_CODE",
  "value_source": "SubjectHubCode.by_description",
  "notes": "Select the hub or organisation for the subject.",
  "allowed_values": [
    "user's hub",
    "user's organisation"
  ],
  "dependencies": [
    "User"
  ]
}
```

- **`key`:** The unique identifier for the criterion (must match the code).
- **`value_source`:** (Optional) The source of the value, can be left blank. This refers to the class + method used in the subject selection query builder. This is not used by the code but is there to allow easier tracking/mapping.
- **`notes`:** A clear, user-focused description of what the key is and what the user should input.
- **`allowed_values`:** (Optional) An array of allowed values for the dropdown selection.
- **`dependencies`:** (Optional) An array that can include `"User"` and/or `"Subject"`. If present, the app will prompt for a user selection or subject NHS number as needed.

#### To add a new criterion

1. Add a new object to the JSON array with the following fields:
   - `"key"`: The `Enum` member name (must match the code).
   - `"value_source"`: (Optional) The value source, can be left blank.
   - `"notes"`: A clear, user-focused description of what the key is and what the user should input.
   - `"allowed_values"`: (Optional) An array of allowed values for the dropdown selection.
   - `"dependencies"`: (Optional) An array containing `"User"` and/or `"Subject"` if the criterion requires additional context.

2. Save the file. The app will automatically pick up the new key on reload.

#### To edit a criterion

- Find the object with the matching `"key"` and update the `"notes"`, `"allowed_values"`, or `"dependencies"` as needed.
- Save the file and reload the app.

#### To remove a criterion

- Delete the object from the JSON array.
- Save the file and reload the app.

#### About the `dependencies` field

- If a criterion requires a User or Subject context, add a `"dependencies"` array to its entry, e.g.:

  ```json
  "dependencies": ["User"]
  ```

  or

  ```json
  "dependencies": ["Subject"]
  ```

  or both:

  ```json
  "dependencies": ["User", "Subject"]
  ```

- The application will automatically show the relevant input sections when any selected criteria require these dependencies.

---

### Adding New Criteria Keys

If you add new keys to the `SubjectSelectionCriteriaKey` `Enum` in your code, you should also add a corresponding entry in `criteria.json` with a description (`notes`), and (optionally) allowed values and dependencies.

---

### Editing Allowed Values or Descriptions

- **Allowed Values:** Update the `"allowed_values"` array for any key to change the dropdown options shown to users.
- **Descriptions:** Update the `"notes"` field to clarify what the key is for or what input is expected.
- **Dependencies:** Update the `"dependencies"` array to control when the app prompts for user or subject context.

---

### Troubleshooting

- **A key does not appear in the UI:**
  Ensure it exists in both the `SubjectSelectionCriteriaKey` `Enum` and in `criteria.json`.

- **Dropdown is missing for a key:**
  Add or update the `"allowed_values"` array for that key in `criteria.json`.

- **Descriptions are unclear or missing:**
  Update the `"notes"` field for the relevant key in `criteria.json`.

- **App does not reload changes:**
  Save your changes and refresh the `Streamlit` app in your browser.

- **Copy to clipboard does not work:**
  Some browsers may not support auto-copy. Manually select and copy the JSON from the code block.

- **Oracle DB errors:**
  Ensure your `local.env` file is present and contains valid values for `ORACLE_USERNAME`, `ORACLE_DB`, and `ORACLE_PASS`.

---

## Example Entry in `criteria.json`

```json
{
  "key": "SCREENING_STATUS",
  "value_source": "ScreeningStatusType.by_description_case_insensitive",
  "notes": "Select the current screening status for the subject.",
  "allowed_values": [
    "Call",
    "Inactive",
    "Opt-in",
    "Recall",
    "Self-referral",
    "Surveillance",
    "Ceased"
  ],
  "dependencies": ["Subject"]
}
```

---

## Summary

- **All configuration is driven by `criteria.json`.**
- **Descriptions, allowed values, and dependencies are fully customizable.**
- **No code changes are needed for most updates—just edit the JSON file.**
- **For new `Enum` keys, add them to both the `SubjectSelectionCriteriaKey` `Enum` and the JSON.**
- **For criteria that require user or subject context, use the `dependencies` field.**
