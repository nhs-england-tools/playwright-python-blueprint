# Utility Guide: Investigation Dataset Utility

The Investigation Dataset Utility provides methods to fill out the investigation dataset forms, and progress episodes, based on the age of the subject and the test results.

## Table of Contents

- [Utility Guide: Investigation Dataset Utility](#utility-guide-investigation-dataset-utility)
  - [Table of Contents](#table-of-contents)
  - [Using the Investigation Dataset Utility](#using-the-investigation-dataset-utility)
  - [Investigation Dataset Completion - Required Arguments](#investigation-dataset-completion---required-arguments)
  - [After Investigation Dataset Complete - Required Arguments](#after-investigation-dataset-complete---required-arguments)
  - [Investigation Dataset Specific Functions](#investigation-dataset-specific-functions)
  - [Example Usage](#example-usage)

## Using the Investigation Dataset Utility

To use the Investigation Dataset Utility, import the `InvestigationDatasetCompletion` and/or `AfterInvestigationDatasetComplete` classes from the `utils.investigation_dataset` directory into your test file and call the relevant methods as required.

## Investigation Dataset Completion - Required Arguments

The methods in this utility require specific arguments. Below is a summary of the required arguments for key methods:

  Required arguments for initialization:
      - page (Page): The Playwright Page object used for browser automation.

  Required arguments for main method:
      - nhs_no (str): The NHS number of the subject.
      - result (str): The result of the investigation dataset. Should be one of InvestigationDatasetResults (HIGH_RISK, LNPCP, NORMAL).

## After Investigation Dataset Complete - Required Arguments

The methods in this utility require specific arguments. Below is a summary of the required arguments for key methods:

  Required arguments for initialization:
      - page (Page): The Playwright Page object used for browser automation.

  Required arguments for main method:
      - result (str): The result of the investigation dataset. Should be one of InvestigationDatasetResults (HIGH_RISK, LNPCP, NORMAL).
      - younger (`bool`): True if the subject is younger than 70, False otherwise.

## Investigation Dataset Specific Functions

The `investigation_dataset` utility is used to complete the investigation dataset forms for a subject.It contains methods to fill out the forms, and progress episodes, based on the age of the subject and the test result. Below are their key functions:

1. **`complete_with_result(self, nhs_no: str, result: str) -> None`**
   This method fills out the investigation dataset forms based on the test result and the subject's age.

   - **Arguments**:
     - nhs_no (str): The NHS number of the subject.
     - result (str): The result of the investigation dataset. Should be one of InvestigationDatasetResults (HIGH_RISK, LNPCP NORMAL).

2. **`go_to_investigation_datasets_page(self, nhs_no) -> None`**
   This method navigates to the investigation datasets page for a subject.

   - **Arguments**:
     - nhs_no (str): The NHS number of the subject.

3. **`default_investigation_dataset_forms(self) -> None`**
   This method fills out the first part of the default investigation dataset form.

4. **`default_investigation_dataset_forms_continuation(self) -> None`**
   This method fills out the second part of the default investigation dataset form.

5. **`investigation_datasets_failure_reason(self) -> None`**
   This method fills out the failure reason section of the investigation dataset form.

6. **`polyps_for_high_risk_result(self) -> None`**
   This method fills out the polyp information section of the investigation dataset form to trigger a high risk result.

7. **`polyps_for_lnpcp_result(self) -> None`**
   This method fills out the polyp information section of the investigation dataset form to trigger a LNPCP result.

8. **`polyp1_intervention(self) -> None`**
   This method fills out the intervention section of the investigation dataset form for polyp 1.

9. **`save_investigation_dataset(self) -> None`**
   This method saves the investigation dataset form.

10. **`progress_episode_based_on_result(self, result: str, younger: bool) -> None`**
    This method progresses the episode based on the result of the investigation dataset.

    - **Arguments**:
      - result (str): The result of the investigation dataset. Should be one of InvestigationDatasetResults (HIGH_RISK, LNPCP, NORMAL).
      - younger (`bool`): True if the subject is younger than 50, False otherwise.

11. **`after_high_risk_result(self) -> None`**
    This method advances an episode that has a high-risk result.

12. **`after_lnpcp_result(self) -> None`**
    This method advances an episode that has a LNPCP result.

13. **`after_normal_result(self) -> None`**
    This method advances an episode that has a normal result.

14. **`handover_subject_to_symptomatic_care(self) -> None`**
    This method hands over a subject to symptomatic care.

15. **`record_diagnosis_date(self) -> None`**
    This method records the diagnosis date for a subject.

## Example Usage

```python
from playwright.sync_api import sync_playwright
from utils.investigation_dataset import (
    InvestigationDatasetCompletion,
    InvestigationDatasetResults,
    AfterInvestigationDatasetComplete,
)

def example_investigation_dataset_usage(nhs_no: str, result: str, younger: bool) -> None:
# Start Playwright and open a browser/page (simplified for example)
  with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      page = browser.new_page()

      # Complete the investigation dataset for a subject
      investigation = InvestigationDatasetCompletion(page)
      investigation.complete_with_result(nhs_no, result)

      # Progress the episode based on the result and subject's age
      after_investigation = AfterInvestigationDatasetComplete(page)
      after_investigation.progress_episode_based_on_result(result, younger)

      browser.close()

# Example usage:
example_investigation_dataset_usage(
    nhs_no="1234567890",
    result=InvestigationDatasetResults.HIGH_RISK,
    younger=True
)
```
