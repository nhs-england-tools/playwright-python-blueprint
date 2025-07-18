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
  - [Using the InvestigationDatasetCompletion class with your own values](#using-the-investigationdatasetcompletion-class-with-your-own-values)
    - [Required Args](#required-args)
    - [How to use this method](#how-to-use-this-method)
    - [Example Usage](#example-usage-1)
    - [Supported Fields](#supported-fields)
      - [General Information](#general-information)
      - [Drug Information](#drug-information)
      - [Endoscopy Information](#endoscopy-information)
      - [Failure Information](#failure-information)
      - [Completion Proof Information](#completion-proof-information)
      - [Polyp Information (Optional)](#polyp-information-optional)
      - [Polyp Intervention (Optional)](#polyp-intervention-optional)
      - [Polyp Histology (Optional)](#polyp-histology-optional)

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

## Using the InvestigationDatasetCompletion class with your own values

You can initialise the class and use its method as follows:

```python
from utils.investigation_dataset_completion import InvestigationDatasetCompletion

completion_utility = InvestigationDatasetCompletion(page)
completion_utility.complete_dataset_with_args(
    general_information=...,
    drug_information=...,
    endoscopy_information=...,
    failure_information=...,
    completion_information=...,
    polyp_1_information=...,
    polyp_1_intervention=...,
    polyp_1_histology=...
)
```

### Required Args

All fields are `dict` objects containing key-value pairs that match the expected form inputs.

- `general_information` (required): Information about site, practitioner, and endoscopist.
- `drug_information` (required): Drugs used during the procedure.
- `endoscopy_information` (required): Field-value pairs describing procedure details.
- `failure_information` (required): Reasons for dataset failure.
- `completion_information` (optional): Completion proof values.
- `polyp_1_information` (optional): Data for a polyp entry.
- `polyp_1_intervention` (optional): Data for a polyp intervention.
- `polyp_1_histology` (optional): Histology data for the polyp.

### How to use this method

Call the `complete_dataset_with_args()` method to populate and submit the investigation dataset form. The method performs the following:

- Navigates to relevant form sections.
- Inputs field values using select/input locators.
- Handles optional sub-sections (e.g., polyps, interventions).
- Handles conditional logic for field population.
- Submits the form once complete.

---

### Example Usage

```python
completion_utility = InvestigationDatasetCompletion(page)

completion_utility.complete_dataset_with_args(
    general_information={
        "site": -1,
        "practitioner": -1,
        "testing clinician": -1,
        "aspirant endoscopist": None
    },
    drug_information = {
        "drug_type1": DrugTypeOptions.MANNITOL,
        "drug_dose1": "3",
    },
    endoscopy_information = {
        "endoscope inserted": "yes",
        "procedure type": "therapeutic",
        "bowel preparation quality": BowelPreparationQualityOptions.GOOD,
        "comfort during examination": ComfortOptions.NO_DISCOMFORT,
        "comfort during recovery": ComfortOptions.NO_DISCOMFORT,
        "endoscopist defined extent": EndoscopyLocationOptions.APPENDIX,
        "scope imager used": YesNoOptions.YES,
        "retroverted view": YesNoOptions.NO,
        "start of intubation time": "09:00",
        "start of extubation time": "09:30",
        "end time of procedure": "10:00",
        "scope id": "Autotest",
        "insufflation": InsufflationOptions.AIR,
        "outcome at time of procedure": OutcomeAtTimeOfProcedureOptions.LEAVE_DEPARTMENT,
        "late outcome": LateOutcomeOptions.NO_COMPLICATIONS,
    },
    failure_information={
        "failure reasons": FailureReasonsOptions.ADHESION
    },
    completion_information={
        "completion proof": CompletionProofOptions.VIDEO_APPENDIX
    },
    polyp_1_information={
        "location": EndoscopyLocationOptions.APPENDIX,
        "classification": PolypClassificationOptions.IS,
        "estimate of whole polyp size": "8",
        "polyp access": PolypAccessOptions.EASY,
        "left in situ": YesNoOptions.NO,
    },
    polyp_1_intervention={
        "modality": PolypInterventionModalityOptions.POLYPECTOMY,
        "device": PolypInterventionDeviceOptions.COLD_SNARE,
        "excised": YesNoOptions.YES,
        "retrieved": YesNoOptions.YES,
    },
    polyp_1_histology={
        "date of receipt": datetime.today(),
        "date of reporting": datetime.today(),
        "pathology provider": -1,
        "pathologist": -1,
        "polyp type": PolypTypeOptions.SERRATED_LESION,
        "serrated lesion sub type": SerratedLesionSubTypeOptions.MIXED_POLYP,
        "polyp excision complete": PolypExcisionCompleteOptions.R1,
        "polyp size": "10",
        "polyp dysplasia": PolypDysplasiaOptions.NOT_REPORTED,
        "polyp carcinoma": YesNoUncertainOptions.NO,
    }
)
```

---

### Supported Fields

#### General Information

| Field                   | Type    | Description                          |
|------------------------|---------|--------------------------------------|
| site                   | `int`   | Index in the site dropdown           |
| practitioner           | `int`   | Index in the practitioner dropdown   |
| testing clinician      | `int`   | Index in the clinician dropdown      |
| aspirant endoscopist   | `int or None` | Index or skip check if None   |

#### Drug Information

| Field        | Type  | Description                        |
|--------------|-------|------------------------------------|
| drug_type1   | str   | Drug name                          |
| drug_dose1   | str   | Dose                               |

#### Endoscopy Information

Supports dynamic keys like:

- `"endoscope inserted"`: `"yes"` or `"no"`
- `"procedure type"`: `"diagnostic"` or `"therapeutic"`
- `"bowel preparation quality"`: Option from dropdown
- `"start of intubation time"`: `"09:00"`
- `"scope id"`: Free text

#### Failure Information

| Field              | Type  | Description                              |
|-------------------|-------|------------------------------------------|
| failure reasons    | str   | Reason text for dataset failure          |

#### Completion Proof Information

| Field              | Type  | Description                              |
|-------------------|-------|------------------------------------------|
| completion proof   | str   | Value for the "Proof Parameters" field   |

#### Polyp Information (Optional)
<!--vale off-->
| Field                        | Type  | Description                          |
|-----------------------------|-------|--------------------------------------|
| location                    | str   | Polyp location                       |
| classification              | str   | Polyp classification                 |
| estimate of whole polyp size| str   | Size in mm                           |
| polyp access                | str   | Access difficulty                    |
| left in situ                | str   | `"Yes"` or `"No"`                    |
<!--vale on-->
#### Polyp Intervention (Optional)

| Field                                   | Type  | Description                     |
|----------------------------------------|-------|---------------------------------|
| modality                               | str   | E.g., `"Polypectomy"`           |
| device                                 | str   | E.g., `"Cold snare"`            |
| excised                                | str   | `"Yes"` or `"No"`               |
| retrieved                              | str   | `"Yes"` or `"No"`               |
| excision technique                     | str   | Optional technique detail       |
| polyp appears fully resected endoscopically | str | Option from dropdown        |

#### Polyp Histology (Optional)

| Field                     | Type        | Description                         |
|--------------------------|-------------|-------------------------------------|
| date of receipt          | `datetime`  | Date of receipt                     |
| date of reporting        | `datetime`  | Date of reporting                   |
| pathology provider       | `int`       | Index for provider                  |
| pathologist              | `int`       | Index for pathologist               |
| polyp type               | `str`       | E.g., `"Serrated Lesion"`           |
| serrated lesion sub type | `str`       | Subtype of serrated lesion          |
| adenoma sub type         | `str`       | Subtype of adenoma                  |
| polyp excision complete  | `str`       | Completion status                   |
| polyp size               | `str`       | Size in mm                          |
| polyp dysplasia          | `str`       | Dysplasia report                    |
| polyp carcinoma          | `str`       | `"Yes"`, `"No"`, or `"Uncertain"`   |

---

For more details on each function's implementation, refer to the source code in `utils/investigation_dataset.py`.
