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
from utils.investigation_dataset import InvestigationDatasetCompletion

completion_utility = InvestigationDatasetCompletion(page)
completion_utility.complete_dataset_with_args(
    general_information=general_information,
    drug_information=drug_information,
    endoscopy_information=endoscopy_information,
    failure_information=failure_information,
    polyp_information=polyp_information,         # List of dicts, one per polyp
    polyp_intervention=polyp_intervention,       # List of dicts, one per polyp
    polyp_histology=polyp_histology              # List of dicts, one per polyp
)
```

### Required Args

All fields are `dict` objects containing key-value pairs that match the expected form inputs.
For polyps, you now pass **lists of dictionaries** (one per polyp) for `polyp_information`, `polyp_intervention`, and `polyp_histology`.

- `general_information` (required): Information about site, practitioner, and endoscopist.
- `drug_information` (required): Drugs used during the procedure.
- `endoscopy_information` (required): Field-value pairs describing procedure details.
- `failure_information` (required): Reasons for dataset failure.
- `completion_information` (optional): Completion proof values.
- `polyp_information` (optional): **List** of dicts, each for a polyp entry.
- `polyp_intervention` (optional): **List** of dicts, each for a polyp intervention.
- `polyp_histology` (optional): **List** of dicts, each for a polyp's histology.

### How to use this method

Call the `complete_dataset_with_args()` method to populate and submit the investigation dataset form. The method performs the following:

- Navigates to relevant form sections.
- Inputs field values using select/input locators.
- Handles optional sub-sections (e.g., polyps, interventions, histology) for **multiple polyps**.
- Handles conditional logic for field population.
- Submits the form once complete.

---

### Example Usage

Below is a real-world example based on the `test_identify_diminutive_rectal_hyperplastic_polyp_from_histology_a` test:

```python
from datetime import datetime
from utils.investigation_dataset import InvestigationDatasetCompletion
from pages.datasets.investigation_dataset_page import (
    DrugTypeOptions, BowelPreparationQualityOptions, ComfortOptions,
    EndoscopyLocationOptions, YesNoOptions, InsufflationOptions,
    OutcomeAtTimeOfProcedureOptions, LateOutcomeOptions, FailureReasonsOptions,
    PolypClassificationOptions, PolypAccessOptions, PolypInterventionModalityOptions,
    PolypInterventionDeviceOptions, PolypInterventionExcisionTechniqueOptions,
    PolypTypeOptions, SerratedLesionSubTypeOptions, PolypExcisionCompleteOptions
)

general_information = {
    "site": -1,
    "practitioner": -1,
    "testing clinician": -1,
    "aspirant endoscopist": None,
}

drug_information = {
    "drug_type1": DrugTypeOptions.MANNITOL,
    "drug_dose1": "3",
}

endoscopy_information = {
    "endoscope inserted": "yes",
    "procedure type": "therapeutic",
    "bowel preparation quality": BowelPreparationQualityOptions.GOOD,
    "comfort during examination": ComfortOptions.NO_DISCOMFORT,
    "comfort during recovery": ComfortOptions.NO_DISCOMFORT,
    "endoscopist defined extent": EndoscopyLocationOptions.DESCENDING_COLON,
    "scope imager used": YesNoOptions.YES,
    "retroverted view": YesNoOptions.NO,
    "start of intubation time": "09:00",
    "start of extubation time": "09:30",
    "end time of procedure": "10:00",
    "scope id": "Autotest",
    "insufflation": InsufflationOptions.AIR,
    "outcome at time of procedure": OutcomeAtTimeOfProcedureOptions.LEAVE_DEPARTMENT,
    "late outcome": LateOutcomeOptions.NO_COMPLICATIONS,
}

failure_information = {
    "failure reasons": FailureReasonsOptions.ADHESION,
}

# Example for 4 polyps
polyp_information = [
    {
        "location": EndoscopyLocationOptions.RECTUM,
        "classification": PolypClassificationOptions.IP,
        "estimate of whole polyp size": "6",
        "polyp access": PolypAccessOptions.EASY,
        "left in situ": YesNoOptions.NO,
    },
    {
        "location": EndoscopyLocationOptions.RECTUM,
        "classification": PolypClassificationOptions.ISP,
        "estimate of whole polyp size": "1",
        "polyp access": PolypAccessOptions.EASY,
        "left in situ": YesNoOptions.NO,
    },
    {
        "location": EndoscopyLocationOptions.RECTUM,
        "classification": PolypClassificationOptions.IS,
        "estimate of whole polyp size": "2",
        "polyp access": PolypAccessOptions.EASY,
        "left in situ": YesNoOptions.NO,
    },
    {
        "location": EndoscopyLocationOptions.RECTUM,
        "classification": PolypClassificationOptions.IIC,
        "estimate of whole polyp size": "5",
        "polyp access": PolypAccessOptions.EASY,
        "left in situ": YesNoOptions.NO,
    },
]

polyp_intervention = [
    {
        "modality": PolypInterventionModalityOptions.POLYPECTOMY,
        "device": PolypInterventionDeviceOptions.HOT_SNARE,
        "excised": YesNoOptions.YES,
        "retrieved": YesNoOptions.YES,
    },
    {
        "modality": PolypInterventionModalityOptions.EMR,
        "device": PolypInterventionDeviceOptions.HOT_SNARE,
        "excised": YesNoOptions.YES,
        "retrieved": YesNoOptions.YES,
    },
    {
        "modality": PolypInterventionModalityOptions.ESD,
        "device": PolypInterventionDeviceOptions.ENDOSCOPIC_KNIFE,
        "excised": YesNoOptions.YES,
        "retrieved": YesNoOptions.YES,
    },
    {
        "modality": PolypInterventionModalityOptions.POLYPECTOMY,
        "device": PolypInterventionDeviceOptions.HOT_SNARE,
        "excised": YesNoOptions.YES,
        "retrieved": YesNoOptions.YES,
        "excision technique": PolypInterventionExcisionTechniqueOptions.PIECE_MEAL,
    },
]

polyp_histology = [
    {
        "date of receipt": datetime.today(),
        "date of reporting": datetime.today(),
        "pathology provider": -1,
        "pathologist": -1,
        "polyp type": PolypTypeOptions.SERRATED_LESION,
        "serrated lesion sub type": SerratedLesionSubTypeOptions.HYPERPLASTIC_POLYP,
        "polyp excision complete": PolypExcisionCompleteOptions.R1,
        "polyp size": "5",
    },
    {
        "date of receipt": datetime.today(),
        "date of reporting": datetime.today(),
        "pathology provider": -1,
        "pathologist": -1,
        "polyp type": PolypTypeOptions.SERRATED_LESION,
        "serrated lesion sub type": SerratedLesionSubTypeOptions.HYPERPLASTIC_POLYP,
        "polyp excision complete": PolypExcisionCompleteOptions.R1,
        "polyp size": "1",
    },
    {
        "date of receipt": datetime.today(),
        "date of reporting": datetime.today(),
        "pathology provider": -1,
        "pathologist": -1,
        "polyp type": PolypTypeOptions.SERRATED_LESION,
        "serrated lesion sub type": SerratedLesionSubTypeOptions.HYPERPLASTIC_POLYP,
        "polyp excision complete": PolypExcisionCompleteOptions.R1,
        "polyp size": "3",
    },
    {
        "date of receipt": datetime.today(),
        "date of reporting": datetime.today(),
        "pathology provider": -1,
        "pathologist": -1,
        "polyp type": PolypTypeOptions.SERRATED_LESION,
        "serrated lesion sub type": SerratedLesionSubTypeOptions.HYPERPLASTIC_POLYP,
        "polyp excision complete": PolypExcisionCompleteOptions.R1,
        "polyp size": "4",
    },
]

completion_utility = InvestigationDatasetCompletion(page)
completion_utility.complete_dataset_with_args(
    general_information=general_information,
    drug_information=drug_information,
    endoscopy_information=endoscopy_information,
    failure_information=failure_information,
    polyp_information=polyp_information,
    polyp_intervention=polyp_intervention,
    polyp_histology=polyp_histology,
)
```

---

### Supported Fields

#### General Information

| Field                 | Type    | Example Value                                 | Description                          |
|-----------------------|---------|-----------------------------------------------|--------------------------------------|
| site                  | `int`   | -1                                            | Index in the site dropdown           |
| practitioner          | `int`   | -1                                            | Index in the practitioner dropdown   |
| testing clinician     | `int`   | -1                                            | Index in the clinician dropdown      |
| aspirant endoscopist  | `int or None` | None                                   | Index or skip check if None          |

#### Drug Information

| Field        | Type  | Example Value                | Description                        |
|--------------|-------|-----------------------------|------------------------------------|
| drug_type1   | str   | DrugTypeOptions.MANNITOL    | Drug name                          |
| drug_dose1   | str   | "3"                         | Dose                               |

#### Endoscopy Information
<!--vale off-->
| Field                        | Type    | Example Value                                         | Description                          |
|------------------------------|---------|-------------------------------------------------------|--------------------------------------|
| endoscope inserted           | str     | "yes"                                                | "yes" or "no"                        |
| procedure type               | str     | "therapeutic"                                        | "diagnostic" or "therapeutic"        |
| bowel preparation quality    | enum    | BowelPreparationQualityOptions.GOOD                   | Option from dropdown                 |
| comfort during examination   | enum    | ComfortOptions.NO_DISCOMFORT                          | Option from dropdown                 |
| comfort during recovery      | enum    | ComfortOptions.NO_DISCOMFORT                          | Option from dropdown                 |
| endoscopist defined extent   | enum    | EndoscopyLocationOptions.DESCENDING_COLON             | Option from dropdown                 |
| scope imager used            | enum    | YesNoOptions.YES                                      | Option from dropdown                 |
| retroverted view             | enum    | YesNoOptions.NO                                       | Option from dropdown                 |
| start of intubation time     | str     | "09:00"                                               | Time string                          |
| start of extubation time     | str     | "09:30"                                               | Time string                          |
| end time of procedure        | str     | "10:00"                                               | Time string                          |
| scope id                     | str     | "Autotest"                                            | Free text                            |
| insufflation                 | enum    | InsufflationOptions.AIR                               | Option from dropdown                 |
| outcome at time of procedure | enum    | OutcomeAtTimeOfProcedureOptions.LEAVE_DEPARTMENT      | Option from dropdown                 |
| late outcome                 | enum    | LateOutcomeOptions.NO_COMPLICATIONS                   | Option from dropdown                 |
<!--vale on-->
#### Failure Information
<!--vale off-->
| Field              | Type  | Example Value                       | Description                              |
|--------------------|-------|-------------------------------------|------------------------------------------|
| failure reasons    | enum  | FailureReasonsOptions.ADHESION       | Reason text for dataset failure          |
<!--vale on-->
#### Completion Proof Information
<!--vale off-->
| Field              | Type  | Example Value                       | Description                              |
|--------------------|-------|-------------------------------------|------------------------------------------|
| completion proof   | enum  | CompletionProofOptions.VIDEO_APPENDIX| Value for the "Proof Parameters" field   |
<!--vale on-->
#### Polyp Information (Optional)
<!--vale off-->
| Field                        | Type  | Example Value                                 | Description                          |
|------------------------------|-------|-----------------------------------------------|--------------------------------------|
| location                     | enum  | EndoscopyLocationOptions.RECTUM               | Polyp location                       |
| classification               | enum  | PolypClassificationOptions.IP                 | Polyp classification                 |
| estimate of whole polyp size | str   | "6"                                           | Size in mm                           |
| polyp access                 | enum  | PolypAccessOptions.EASY                       | Access difficulty                    |
| left in situ                 | enum  | YesNoOptions.NO                               | "Yes" or "No"                        |
<!--vale on-->
#### Polyp Intervention (Optional)
<!--vale off-->
| Field                                   | Type  | Example Value                                         | Description                     |
|------------------------------------------|-------|-------------------------------------------------------|---------------------------------|
| modality                                | enum  | PolypInterventionModalityOptions.POLYPECTOMY          | E.g., "Polypectomy"             |
| device                                  | enum  | PolypInterventionDeviceOptions.HOT_SNARE              | E.g., "Hot snare"               |
| excised                                 | enum  | YesNoOptions.YES                                      | "Yes" or "No"                   |
| retrieved                               | enum  | YesNoOptions.YES                                      | "Yes" or "No"                   |
| excision technique                      | enum  | PolypInterventionExcisionTechniqueOptions.PIECE_MEAL  | Optional technique detail       |
| polyp appears fully resected endoscopically | enum | YesNoOptions.YES                                  | Option from dropdown            |
<!--vale on-->
#### Polyp Histology (Optional)
<!--vale off-->
| Field                     | Type        | Example Value                                         | Description                         |
|---------------------------|-------------|-------------------------------------------------------|-------------------------------------|
| date of receipt           | `datetime`  | datetime.today()                                      | Date of receipt                     |
| date of reporting         | `datetime`  | datetime.today()                                      | Date of reporting                   |
| pathology provider        | `int`       | -1                                                    | Index for provider                  |
| pathologist               | `int`       | -1                                                    | Index for pathologist               |
| polyp type                | enum        | PolypTypeOptions.SERRATED_LESION                      | E.g., "Serrated Lesion"             |
| serrated lesion sub type  | enum        | SerratedLesionSubTypeOptions.HYPERPLASTIC_POLYP       | Subtype of serrated lesion          |
| adenoma sub type          | enum        | AdenomaSubTypeOptions.TUBULAR_ADENOMA                 | Subtype of adenoma                  |
| polyp excision complete   | enum        | PolypExcisionCompleteOptions.R1                       | Completion status                   |
| polyp size                | str         | "5"                                                   | Size in mm                          |
| polyp dysplasia           | enum        | PolypDysplasiaOptions.NOT_REPORTED                    | Dysplasia report                    |
| polyp carcinoma           | enum        | YesNoUncertainOptions.NO                              | "Yes", "No", or "Uncertain"         |
<!--vale on-->
---

For more details on each function's implementation, refer to the source code in `utils/investigation_dataset.py`.
