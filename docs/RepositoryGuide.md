# BCSS Playwright Automation Repository Reference

This document provides a comprehensive reference for all Page Object Models (POMs), classes, utilities, and UI applications available in this repository.<br>
It is intended to help developers and testers understand the structure, usage, and capabilities of each component.

---

## Table of Contents

- [BCSS Playwright Automation Repository Reference](#bcss-playwright-automation-repository-reference)
  - [Table of Contents](#table-of-contents)
  - [Directory Structure](#directory-structure)
  - [Page Object Models (POMs)](#page-object-models-poms)
    - [Usage Examples](#usage-examples)
    - [Naming Conventions](#naming-conventions)
  - [Classes](#classes)
    - [Useful Classes](#useful-classes)
      - [When to Use](#when-to-use)
      - [Why Use](#why-use)
      - [How to Use](#how-to-use)
      - [Why Use Repositories?](#why-use-repositories)
      - [Example: Using a Repository in a Test](#example-using-a-repository-in-a-test)
    - [Class Descriptions](#class-descriptions)
    - [Relationships/Dependencies](#relationshipsdependencies)
    - [Utility Classes](#utility-classes)
  - [Utilities](#utilities)
    - [Available Utilities](#available-utilities)
  - [UI Applications](#ui-applications)
  - [Conftest \& Fixtures](#conftest--fixtures)
    - [Available Fixtures](#available-fixtures)
    - [Example Usage](#example-usage)
      - [Using as a Function Argument](#using-as-a-function-argument)
      - [Using the @pytest.mark.usefixtures Decorator](#using-the-pytestmarkusefixtures-decorator)
      - [Using Both](#using-both)
    - [Custom CLI Options](#custom-cli-options)

---

## Directory Structure

- pages/: Page Object Models
- classes/: Domain models, repositories, enums
- utils/: Utility modules
- docs/: Documentation and guides
- tests/: Automated test scripts

---

## Page Object Models (POMs)

All POMs are located in the `pages/` directory.<br>
Each POM encapsulates locators and methods for interacting with a specific page or feature in the UI.<br>
The purpose of POMs is to promote reusability and maintainability of the automation code by providing a clear structure for page interactions.<br>

The POMs have been organised into folders based on the main menu within the UI to allow for easier navigation.<br>
POMs follow the naming convention of `<page_name>_page.py` to clearly indicate their purpose.<br>
All of the POMs inherit the `BasePage` POM. This is so that they can leverage common functionality such as the common click method.<br>

Please refer to the list below for all available POMs in this repository.

---

<details>
<summary><strong>Available POMs</strong></summary>
<!-- vale off -->

- base_page
- alerts/
  - alerts_page
- bowel_scope/
  - bowel_scope_appointments_page
  - bowel_scope_page
- call_and_recall/
  - age_extension_rollout_plans_page
  - call_and_recall_page
  - create_a_plan_page
  - generate_invitations_page
  - invitations_monitoring_page
  - invitations_plans_page
  - non_invitation_days_page
- communication_production/
  - batch_list_page
  - communication_production_page
  - electronic_communication_management_page
  - letter_library_index_page
  - manage_active_batch_page
  - manage_archived_batch_page
- contacts_list/
  - contacts_list_page
  - edit_contact_page
  - edit_my_contact_details_page
  - maintain_contacts_page
  - my_preference_settings_page
  - resect_and_discard_accreditation_history_page
  - view_contacts_page
- datasets/
  - cancer_audit_datasets_page
  - colonoscopy_dataset_page
  - investigation_dataset_page
  - subject_dataset_page
- download/
  - batch_download_request_and_retrieval_page
  - downloads_page
  - individual_download_request_and_retrieval_page
  - list_of_individual_downloads_page
- fit_test_kits/
  - fit_rollout_summary_page
  - fit_test_kits_page
  - kit_result_audit_page
  - kit_service_management_page
  - log_devices_page
  - maintain_analysers_page
  - manage_qc_products_page
  - screening_incidents_list_page
  - view_algorithms_page
  - view_fit_kit_result_page
  - view_screening_centre_fit_confguration_page
- gfobt_test_kits/
  - gfobt_create_qc_kit_page
  - gfobt_test_kit_logging_page
  - gfobt_test_kit_quality_control_reading_page
  - gfobt_test_kits_page
  - gfobt_view_test_kit_result_page
- login/
  - cognito_login_page
  - login_failure_screen_page
  - login_page
  - select_job_role_page
- logout/
  - log_out_page
- lynch_surveillance/
  - lynch_invitation_page
  - set_lynch_invitation_rates_page
- manual_cease/
  - manual_cease_page
- organisations/
  - create_organisation_page
  - create_site_page
  - list_all_organisations_page
  - list_all_sites_page
  - organisations_and_site_details_page
  - organisations_page
  - view_organisation_page
- reports/
  - reports_page
- screening_practitioner_appointments/
  - appointment_calendar_page
  - appointment_detail_page
  - book_appointment_page
  - colonoscopy_assessment_appointments_page
  - practitioner_availability_page
  - screening_practitioner_appointments_page
  - screening_practitioner_day_view_page
  - set_availability_page
- screening_subject_search/
  - advance_fobt_screening_episode_page
  - attend_diagnostic_test_page
  - close_fobt_screening_episode_page
  - contact_with_patient_page
  - diagnostic_test_outcome_page
  - episode_events_and_notes_page
  - handover_into_symptomatic_care_page
  - non_neoplastic_result_from_symptomatic_procedure_page
  - patient_advised_of_diagnosis_page
  - record_diagnosis_date_page
  - reopen_fobt_screening_episode_page
  - return_from_symptomatic_referral_page
  - subject_demographic_page
  - subject_episode_events_and_notes_page
  - subject_events_notes_page
  - subject_screening_search_page
  - subject_screening_summary_page
  - subject_spine_retrieval_search_page
- surveillance/
  - surveillance_summary_review_page

<!-- vale on -->
</details>

---

### Usage Examples

To use a POM in a test, instantiate the page object and call its methods:

```python
from pages.screening_subject_search.subject_screening_search_page import (
  SubjectScreeningPage,
  SearchAreaSearchOptions,
)

def test_search_user_by_nhs_number(page):
  nhs_number = "1234567890"
  SubjectScreeningPage(page).click_clear_filters_button()
  SubjectScreeningPage(page).click_episodes_filter()
  SubjectScreeningPage(page).nhs_number_filter.fill(nhs_number)
  SubjectScreeningPage(page).nhs_number_filter.press("Tab")
  SubjectScreeningPage(page).select_search_area_option(
    SearchAreaSearchOptions.SEARCH_AREA_WHOLE_DATABASE.value
  )
  SubjectScreeningPage(page).click_search_button()
```

---

### Naming Conventions

- **File Names:** Use lowercase with underscores, ending in `_page.py` (e.g., `login_page.py`, `reports_page.py`).
- **Class Names:** Use PascalCase, ending in `Page` (e.g., `LoginPage`, `ReportsPage`).

---

## Classes

This repository includes multiple classes which have been organised into categories to allow for easier navigation.<br>
All classes are located in the `classes/` directory.<br>
Each class encapsulates domain logic, data models, enums, repositories, or utility functions for the BCSS Playwright automation framework.<br>

---

<details>
<summary><strong>Available Classes</strong></summary>

- address/
  - address.py
  - address_contact_type.py
  - address_type.py
- appointment/
  - appointment_slot_type.py
  - appointment_status_type.py
- bowel_scope/
  - bowel_scope_dd_reason_for_change_type.py
- ceased/
  - ceased_confirmation_details.py
  - ceased_confirmation_user_id.py
  - clinical_cease_reason_type.py
  - manual_cease_requested.py
- data/
  - data_creation.py
- database/
  - database_error.py
  - database_transition_parameters.py
- datasets/
  - asa_grade_type.py
  - cancer_treatment_intent.py
  - final_pretreatment_m_category_type.py
  - final_pretreatment_n_category_type.py
  - final_pretreatment_t_category_type.py
  - intended_extent_type.py
  - location_type.py
  - metastases_location_type.py
  - metastases_present_type.py
  - previously_excised_tumour_type.py
  - reason_no_treatment_received_type.py
  - scan_type.py
  - symptomatic_procedure_result_type.py
  - treatment_given.py
  - treatment_type.py
- date/
  - date_description.py
  - date_description_utils.py
  - has_date_of_death_removal.py
  - has_user_dob_update.py
- deduction/
  - deduction_reason_types.py
- diagnostic/
  - diagnosis_date_reason_type.py
  - diagnostic_test_has_outcome_of_result.py
  - diagnostic_test_has_result.py
  - diagnostic_test_is_void.py
  - diagnostic_test_referral_type.py
  - diagnostic_test_type.py
  - which_diagnostic_test.py
- entities/
  - kit_service_management_entity.py
- episode/
  - episode_result_type.py
  - episode_status_reason_type.py
  - episode_status_type.py
  - episode_sub_type.py
  - episode_type.py
  - latest_episode_has_dataset.py
  - latest_episode_latest_investigation_dataset.py
  - prevalent_incident_status_type.py
  - subject_has_episode.py
- event/
  - event_code_type.py
  - event_status_type.py
- invitation/
  - invitation_plan.py
  - invitation_plan_status_type.py
  - invitation_plan_week.py
  - invited_since_age_extension.py
- kits/
  - analyser.py
  - analyser_result_code_type.py
  - kit_service_management_record.py
  - kit_status.py
  - kit_type.py
- lynch/
  - lynch_incident_episode_type.py
  - lynch_sdd_reason_for_change_type.py
- notify/
  - notify_event_status.py
  - notify_message_status.py
  - notify_message_type.py
- organisation/
  - organisation.py
  - organisation_complex.py
- person/
  - person.py
  - person_accreditation_status.py
  - person_data.py
  - person_role_status.py
  - person_selection_criteria_key.py
- recall/
  - recall_calculation_method_type.py
  - recall_episode_type.py
  - recall_surveillance_type.py
- referral/
  - has_referral_date.py
  - reason_for_onward_referral_type.py
  - reason_for_symptomatic_referral_type.py
- repositories/
  - analyser_repository.py
  - episode_repository.py
  - general_repository.py
  - invitation_repository.py
  - kit_service_management_repository.py
  - person_repository.py
  - subject_repository.py
  - user_repository.py
  - word_repository.py
- role/
  - role_type.py
- screening/
  - has_gp_practice.py
  - has_unprocessed_sspi_updates.py
  - hub_type.py
  - region_type.py
  - screening_referral_type.py
  - screening_status_type.py
  - ss_reason_for_change_type.py
  - subject_hub_code.py
  - subject_screening_centre_code.py
- subject/
  - gender_type.py
  - pi_subject.py
  - subject.py
- subject_selection_query_builder/
  - selection_builder_exception.py
  - subject_selection_criteria_key.py
- surveillance/
  - does_subject_have_surveillance_review_case.py
  - sdd_reason_for_change_type.py
  - ssdd_reason_for_change_type.py
  - surveillance_review_case_type.py
  - surveillance_review_status_type.py
- user/
  - user.py
  - user_role_type.py
- yes_no/
  - yes_no.py
  - yes_no_type.py

</details>

---

### Useful Classes

There are some classes that may be commonly used across multiple tests.<br>
These include:

- `Person` - Represents a person in the system, encapsulating their attributes and behaviors.
- `User` - Represents a user of the system, providing methods for user management and authentication.
- `Subject` - Represents a screening subject, providing methods to interact with subject data.
- `EpisodeRepository` - Provides methods to interact with episode data in the database.
- `SubjectRepository` - Provides methods to interact with subject data in the database.
- `PersonRepository` - Provides methods to manage person data.
- `UserRepository` - Provides methods to manage user data.

---

#### When to Use

Use these classes whenever you need to interact with core domain objects or perform database operations in your tests.
For example, when setting up test data, verifying database state after UI actions, or retrieving specific attributes for assertions.

#### Why Use

- They encapsulate business logic and data access, making tests cleaner and easier to maintain.
- They provide a consistent interface for interacting with the system under test.
- Repositories abstract away SQL/database details, allowing you to focus on test logic.

#### How to Use

- Instantiate the class or repository in your test.
- Call the relevant methods to fetch, create, update, or verify data.

Example usage in a test:

```python
from classes.repositories.subject_repository import SubjectRepository
from classes.person.person import Person

def test_subject_exists_in_db():
    repo = SubjectRepository()
    nhs_number = "1234567890"
    assert repo.find_by_nhs_number(nhs_number)

def test_person_attributes():
    person = Person(name="John Doe", dob="1980-01-01")
    assert person.name == "John Doe"
```

You can also use repositories to set up test data before running UI tests, or to verify that changes made in the UI are reflected in the database.

---

#### Why Use Repositories?

Repositories are used to abstract and encapsulate all database access and query logic for a specific domain (e.g., subjects, episodes, users).<br>
This pattern helps keep your test code clean, maintainable, and focused on business logic rather than SQL or data access details.
By using repositories, you can:

- Centralise and reuse query logic across tests.
- Reduce duplication and improve maintainability.

---

#### Example: Using a Repository in a Test

```python
from classes.repositories.subject_repository import SubjectRepository

def test_subject_exists_in_db():
    repo = SubjectRepository()
    nhs_number = "1234567890"
    assert repo.find_by_nhs_number(nhs_number)
```

You can also use repositories to fetch or update domain objects, set up test data, or verify database state after UI actions.

---

### Class Descriptions

<!-- vale off -->

| Folder                              | Description                                                        |
|--------------------------------------|--------------------------------------------------------------------|
| address                             | Models address data and types.                                     |
| appointment                         | Models appointment slots and statuses.                             |
| bowel_scope                         | Models bowel scope change reasons.                                 |
| ceased                              | Models cease confirmation details and reasons.                     |
| data                                | Data creation helpers for test setup.                              |
| database                            | Database error handling and transition parameter classes.          |
| datasets                            | Models for dataset fields, cancer treatment, and related enums.    |
| date                                | Date description and utility classes for parsing and formatting.   |
| deduction                           | Deduction reason types.                                            |
| diagnostic                          | Diagnostic test types, outcomes, and related logic.                |
| entities                            | Entity classes for kit management.                                 |
| episode                             | Models episode status, type, and related logic.                    |
| event                               | Event code and status types.                                       |
| invitation                          | Invitation plan and status models.                                 |
| kits                                | Kit management, types, and status classes.                         |
| lynch                               | Lynch syndrome incident and change reason types.                   |
| notify                              | Notification event and message status/types.                       |
| organisation                        | Organisation and complex organisation models.                      |
| person                              | Person models, accreditation, roles, and selection criteria.       |
| recall                              | Recall calculation and episode types.                              |
| referral                            | Referral date and reason types.                                    |
| repositories                        | Repository classes for DB access (depend on entity/data classes).  |
| role                                | Role type enums.                                                  |
| screening                           | Screening centre, status, and region models.                       |
| subject                             | Subject models, gender, and PI subject.                            |
| subject_selection_query_builder      | Selection builder and criteria key classes.                        |
| surveillance                        | Surveillance review and change reason types.                       |
| user                                | User models and role types.                                        |
| yes_no                              | Yes/No type enums.                                                 |

<!-- vale on -->

---

### Relationships/Dependencies

- **Repositories** depend on entity/data classes to perform DB operations.
- **EpisodeRepository**, **SubjectRepository**, **PersonRepository**, and **UserRepository** are central for test data setup and verification.
- **Enums** (e.g., status types, reason types) are used throughout models and repositories for consistency.

---

### Utility Classes

- Utility/helper classes simplify common tasks:
  - `date_description_utils.py`: Date parsing and formatting.
  - `data_creation.py`: Test data generation.
  - `database_transition_parameters.py`: DB transition configuration.
  - `kit_service_management_entity.py`: Kit management helpers.

---

## Utilities

Utility modules provide reusable functions and helpers for common tasks in test automation, such as database interaction, data generation, accessibility scanning, and more.<br>
All utility guides are located in the `docs/utility-guides/` directory. Each utility typically has a corresponding Python module in the `utils/` directory.<br>
Some utilities also have unit tests created. these unit tests are stored in `test_utils`.

---

### Available Utilities

- [Axe Utility](utility-guides/Axe.md)
- [Appointments Utility](utility-guides/Appointments.md)
- [Batch Processing Utility](utility-guides/BatchProcessing.md)
- [Calendar Picker Utility](utility-guides/CalendarPicker.md)
- [Call and Recall Utility](utility-guides/CallAndRecallUtils.md)
- [Dataset Field Utility](utility-guides/DatasetField.md)
- [Date Time Utility](utility-guides/DateTimeUtility.md)
- [Fit Kit Utility](utility-guides/FitKit.md)
- [Investigation Dataset Utility](utility-guides/InvestigationDataset.md)
- [Jira Confluence Utility](utility-guides/JiraConfluenceUtil.md)
- [Load Properties Utility](utility-guides/LoadProperties.md)
- [Manual Cease Workflow Utility](utility-guides/ManualCease.md)
- [NHS Number Tools Utility](utility-guides/NHSNumberTools.md)
- [Notify Criteria Parser Utility](utility-guides/NotifyCriteriaParser.md)
- [Oracle Utility](utility-guides/Oracle.md)
- [PDF Reader Utility](utility-guides/PDFReader.md)
- [Screening Subject Page Searcher Utility](utility-guides/ScreeningSubjectPageSearcher.md)
- [Subject Assertion Utility](utility-guides/SubjectAssertion.md)
- [Subject Creation Utility](utility-guides/SubjectCreationUtil.md)
- [Subject Demographics Utility](utility-guides/SubjectDemographics.md)
- [Subject Notes Utility](utility-guides/SubjectNotes.md)
- [Subject Selection Query Builder Utility](utility-guides/SubjectSelectionQueryBuilder.md)
- [Table Utility](utility-guides/TableUtil.md)
- [User Tools Utility](utility-guides/UserTools.md)

---

## UI Applications

This repository also includes a couple of UI applications.<br>
The UI applications can be used to assit with test creation or to obtain subject related SQL queries.<br>

Currently there are two applications available:

- [Subject Criteria Builder Application](docs/SubjectCriteriaBuilderApplication.md)
- [Investigation Dataset Application](docs/InvestigationDatasetBuilderApplication.md)

To see more information on these applications click on their respective links to view the guides surrounding these applications.

---

## Conftest & Fixtures

The `conftest.py` file is located at the root of the repository and is used to define reusable pytest fixtures and hooks for test setup, tear down, and configuration.<br>
Fixtures in `conftest.py` help manage environment variables, test data, organisational setup, and provide shared resources across multiple test files.

### Available Fixtures

- **`import_local_env_file`**
  Loads environment variables from `local.env` at the start of the test session.

- **`smokescreen_properties`**
  Loads properties from the smokescreen properties file for use in tests.

- **`general_properties`**
  Loads general properties from the main properties file for use in tests.

- **`setup_org_and_appointments`**
  Ensures required organisation parameters and appointments are set up before tests run. Only runs once per day per environment.

- **`subjects_to_run_for`**
  Retrieves the value of the `--subjects-to-run-for` CLI argument (default: 10).

---

### Example Usage

You can use fixtures in your tests by either:

- Adding them as function arguments
- Using the `@pytest.mark.usefixtures` decorator

---

#### Using as a Function Argument

```python
import pytest

def test_example(page: Page, general_properties: dict):
    # Access general properties loaded by the fixture
    assert "eng_screening_centre_id" in general_properties
```

---

#### Using the @pytest.mark.usefixtures Decorator

```python
import pytest

@pytest.mark.usefixtures("setup_org_and_appointments")
def test_my_function(page: Page):
    # Organisation and appointments are set up before this test runs
    # Your test code here
```

---

#### Using Both

```python
import pytest

@pytest.mark.usefixtures("setup_org_and_appointments")
def test_with_properties(page: Page, general_properties: dict):
    # Both fixtures are available
    org_id = general_properties["eng_screening_centre_id"]
    # Your test code here
```

---

### Custom CLI Options

You can pass custom options to pytest via the command line, such as:

```sh
pytest tests/test_setup.py::test_setup_subjects_as_a259 --subjects-to-run-for=5
```

This sets the number of subjects to run the test setup for using the `subjects_to_run_for` fixture.

---

For more details, see the comments and docstrings in [`conftest.py`](../conftest.py).
