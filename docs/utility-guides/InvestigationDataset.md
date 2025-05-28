# Utility Guide: Investigation Dataset Utility

The Investigation Dataset Utility provides methods to fill out the investigation dataset forms and progress episodes based on the age of the subject and the test results.<br>
**Note:** This utility uses predetermined variables and logic to select input field values and progress forms. There is currently no way to alter which options are selected for each field, results are determined by the utility's internal logic.

## Table of Contents

- [Utility Guide: Investigation Dataset Utility](#utility-guide-investigation-dataset-utility)
  - [Table of Contents](#table-of-contents)
  - [Using the Investigation Dataset Utility](#using-the-investigation-dataset-utility)
  - [InvestigationDatasetCompletion Class](#investigationdatasetcompletion-class)
    - [Required Arguments](#required-arguments)
    - [Key Methods](#key-methods)
  - [AfterInvestigationDatasetComplete Class](#afterinvestigationdatasetcomplete-class)
    - [Required Arguments](#required-arguments-1)
    - [Key Methods](#key-methods-1)
  - [InvestigationDatasetResults Class](#investigationdatasetresults-class)
  - [Example Usage](#example-usage)

## Using the Investigation Dataset Utility

To use the Investigation Dataset Utility, import the `InvestigationDatasetCompletion`, `AfterInvestigationDatasetComplete`, and `InvestigationDatasetResults` classes from the `utils.investigation_dataset` module into your test file and call the relevant methods as required.

```python
from utils.investigation_dataset import (
    InvestigationDatasetCompletion,
    AfterInvestigationDatasetComplete,
    InvestigationDatasetResults,
)
```

The **InvestigationDatasetCompletion** and **AfterInvestigationDatasetComplete** classes are meant to be used one after another. this is because once the methods in the first class complete, you are on the correct page to call the methods in the other class. For further clarity on this please use the example provided at the bottom of the guide as a reference.

---

## InvestigationDatasetCompletion Class

This class is responsible for filling out the investigation dataset forms for a subject.
**All field selections are made using predetermined values within the utility.**

### Required Arguments

- `page (Page)`: The Playwright Page object used for browser automation.

### Key Methods

- **`complete_with_result(self, nhs_no: str, result: str) -> None`**
  Fills out the investigation dataset forms based on the test result and the subject's age.
  - `nhs_no (str)`: The NHS number of the subject.
  - `result (str)`: The result of the investigation dataset. Should be one of `InvestigationDatasetResults` (`HIGH_RISK`, `LNPCP`, `NORMAL`).

- **`go_to_investigation_datasets_page(self, nhs_no) -> None`**
  Navigates to the investigation datasets page for a subject.

- **`default_investigation_dataset_forms(self) -> None`**
  Fills out the first part of the default investigation dataset form.

- **`default_investigation_dataset_forms_continuation(self) -> None`**
  Fills out the second part of the default investigation dataset form.

- **`investigation_datasets_failure_reason(self) -> None`**
  Fills out the failure reason section of the investigation dataset form.

- **`polyps_for_high_risk_result(self) -> None`**
  Fills out the polyp information section of the investigation dataset form to trigger a high risk result.

- **`polyps_for_lnpcp_result(self) -> None`**
  Fills out the polyp information section of the investigation dataset form to trigger a LNPCP result.

- **`polyp1_intervention(self) -> None`**
  Fills out the intervention section of the investigation dataset form for polyp 1.

- **`save_investigation_dataset(self) -> None`**
  Saves the investigation dataset form.

---

## AfterInvestigationDatasetComplete Class

This class provides methods to progress an episode after the investigation dataset has been completed.
**All field selections and progressions are made using predetermined values within the utility.**

### Required Arguments

- `page (Page)`: The Playwright Page object used for browser automation.

- **For main progression method:**
  - `result (str)`: The result of the investigation dataset. Should be one of `InvestigationDatasetResults` (`HIGH_RISK`, `LNPCP`, `NORMAL`).
  - `younger (bool)`: `True` if the subject is between 50-70, `False` otherwise.

### Key Methods

- **`progress_episode_based_on_result(self, result: str, younger: bool) -> None`**
  Progresses the episode according to the investigation result and whether the subject is younger than 70.

- **`after_high_risk_result(self) -> None`**
  Advances an episode that has a high-risk result using predetermined field values.

- **`after_lnpcp_result(self) -> None`**
  Advances an episode that has a LNPCP result using predetermined field values.

- **`after_normal_result(self) -> None`**
  Advances an episode that has a normal result using predetermined field values.

- **`handover_subject_to_symptomatic_care(self) -> None`**
  Hands over a subject to symptomatic care.

- **`record_diagnosis_date(self) -> None`**
  Records the diagnosis date for a subject.

---

## InvestigationDatasetResults Class

This `enum` provides the possible result values for the investigation dataset:

- `HIGH_RISK`
- `LNPCP`
- `NORMAL`

---

## Example Usage

```python
from playwright.sync_api import Page
from utils.investigation_dataset import (
    InvestigationDatasetCompletion,
    AfterInvestigationDatasetComplete,
    InvestigationDatasetResults,
)

nhs_no="1234567890",
result=InvestigationDatasetResults.HIGH_RISK,
younger=True

investigation = InvestigationDatasetCompletion(page)
investigation.complete_with_result(nhs_no, result)

# Progress the episode based on the result and subject's age
after_investigation = AfterInvestigationDatasetComplete(page)
after_investigation.progress_episode_based_on_result(result, younger)
```

---

For more details on each function's implementation, refer to the source code in `utils/investigation_dataset.py`.
