# BCSS Playwright Test Suite

[![CI/CD Pull Request](https://github.com/nhs-england-tools/playwright-python-blueprint/actions/workflows/cicd-1-pull-request.yaml/badge.svg)](https://github.com/nhs-england-tools/playwright-python-blueprint/actions/workflows/cicd-1-pull-request.yaml)

This repository contains the automated UI test suite for the BCSS application, built using [Playwright Python](https://playwright.dev/python/). It provides a structured framework and reusable utilities to support consistent, maintainable test development across the project.

Playwright is the recommended UI testing tool for NHS England, as outlined on the [NHS England Tech Radar](https://radar.engineering.england.nhs.uk/), and has been adopted here to modernize and streamline our testing workflows.

## Origin of the Framework

This framework was originally based on the NHS England Playwright Python Blueprint and has since been tailored to meet the specific needs of the BCSS application. While the core utilities and conventions remain, the project has been extended with custom page object models (POMs) and new utility modules to support BCSS-specific workflows, data handling, and UI interactions.

Note: This project is actively maintained and evolving.

## Table of Contents

- [BCSS Playwright Test Suite](#bcss-playwright-test-suite)
  - [Origin of the Framework](#origin-of-the-framework)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
      - [1. Install Python 3.11 or higher](#1-install-python-311-or-higher)
      - [2. Set up a virtual environment (recommended)](#2-set-up-a-virtual-environment-recommended)
        - [First - Create the virtual environment](#first---create-the-virtual-environment)
        - [Next - Activate the virtual environment](#next---activate-the-virtual-environment)
    - [Installation \& Configuration](#installation--configuration)
      - [1. Install Dependencies](#1-install-dependencies)
      - [2. Environment Variables](#2-environment-variables)
      - [3. Test Configuration](#3-test-configuration)
    - [Running Tests](#running-tests)
      - [1. Basic Test Execution](#1-basic-test-execution)
      - [2. Test Filtering](#2-test-filtering)
      - [3. Viewing Trace Files](#3-viewing-trace-files)
    - [Test Structure and Conventions](#test-structure-and-conventions)
      - [1. File Organization](#1-file-organization)
      - [2. Naming Conventions](#2-naming-conventions)
      - [3. Test Function Anatomy](#3-test-function-anatomy)
      - [4. Markers and Tags](#4-markers-and-tags)
      - [5. Skipping and Expected Failures](#5-skipping-and-expected-failures)
    - [Page Object Model (POM) Guidelines](#page-object-model-pom-guidelines)
      - [1. What is a POM?](#1-what-is-a-pom)
      - [2. Location and Structure](#2-location-and-structure)
      - [3. Naming Convention](#3-naming-convention)
      - [4. Anatomy of a Page Class](#4-anatomy-of-a-page-class)
    - [Utility Modules](#utility-modules)
      - [1. Purpose of Utility Modules](#1-purpose-of-utility-modules)
      - [2. Example: Wait Utility](#2-example-wait-utility)
      - [3. Best Practices](#3-best-practices)
      - [4. Blueprint Utilities](#4-blueprint-utilities)
      - [5. BCSS Project Specific Utilities](#5-bcss-project-specific-utilities)
  - [Using the Jira Upload Script](#using-the-jira-upload-script)
  - [Contributing](#contributing)
    - [Contacts](#contacts)
    - [Licence](#licence)

## Getting Started

### Prerequisites

Follow these steps to make sure your system is ready to run the BCSS test framework.

#### 1. Install Python 3.11 or higher

This framework is built using Python, so you'll need to install it first. You can download the latest version from the official [Python](https://www.python.org/downloads/) website.

To check if Python is already installed, open a terminal or command prompt and run:

`python --version`

#### 2. Set up a virtual environment (recommended)

A virtual environment is like a sandbox—it keeps your project’s Python packages separate from everything else on your computer. This prevents version conflicts and makes your setup easier to manage.

Note: If you are using an IDE such as Visual Studio Code or PyCharm, you will normally be prompted to do this automatically.

##### First - Create the virtual environment

To create and activate a virtual environment, open your terminal or command prompt in the root folder of the project (where requirements.txt lives), then run:

`python -m venv .venv`

This creates a folder called .venv that contains a clean Python environment just for this project.

If you get an error like 'Python not found', try using Python3 instead:

`python3 -m venv .venv`

##### Next - Activate the virtual environment

This step tells your terminal to use the Python version and packages inside .venv.

On Windows (Command Prompt):

`.venv/Scripts/activate`

On Windows (PowerShell):

`.venv/Scripts/Activate.ps1`

On macOS/Linux:

`source .venv/bin/activate`

Once activated, your terminal will show the virtual environment name (e.g. (.venv)), indicating you're working inside it.

### Installation & Configuration

#### 1. Install Dependencies

Before configuring anything, make sure all required packages are installed by running:

`pip install -r requirements.txt`
`playwright install --with-deps`

(If you're running on Windows or macOS locally, `playwright install` alone is often enough. The `--with-deps` flag is most useful in Linux-based environments or CI pipelines.)

This installs all Python dependencies listed in the `requirements.txt` file, including Playwright and any custom utilities used in the BCSS framework.

Note: If you're using a virtual environment (recommended), activate it before running the install command (see previous steps).

#### 2. Environment Variables

Create a `local.env` file in the project root, by running `setup_env_file.py`, to store sensitive configuration values like credentials, URLs, or feature flags. Example:

```Bash
BASE_URL=https://bcss.example.com
USERNAME=test_user
PASSWORD=secure_password123
```

These variables are loaded automatically by the framework using `python-dotenv`, keeping secrets out of the codebase.
The actual values required for the `local.env` file can be obtained from one of the testers already using this framework.
Important Note: Ensure that `local.env` is added to your `.gitignore` to avoid accidentally committing secrets.

#### 3. Test Configuration

You can test the configuration has worked by running our example tests, which can be done using the following command (this will run all tests with tracing reports turned on, and in headed mode so you can see the browser execution):

`pytest --tracing on --headed`

Alternatively if you are using Visual Studio Code as your IDE, we have pre-configured this project to work with the
[Testing functionality](https://code.visualstudio.com/docs/editor/testing) so the example tests should be discovered automatically.

### Running Tests

#### 1. Basic Test Execution

To run all tests with tracing enabled:

`pytest --tracing on`

To run a specific test file:

`pytest tests/test_login.py --tracing on`

Tracing captures detailed information about each test run, including browser actions, network requests, and DOM snapshots.

#### 2. Test Filtering

Use markers or keywords to run subsets of tests:

`pytest -m "smoke" --tracing on`
`pytest -k "login" --tracing on`

You can combine flags like `-v (verbose)` and `--maxfail=1` to control output and failure behavior:

`pytest -v --maxfail=1 --tracing on`

#### 3. Viewing Trace Files

After running tests with tracing enabled, trace files are saved in the test-results folder.

To view a trace:

- Open [Playwright Trace Viewer](https://trace.playwright.dev/)
- Drag and drop the .zip file from the test-results folder into the browser window
- Use the interactive viewer to explore browser actions, network activity, and DOM snapshots
- This is especially useful for debugging failed tests or understanding complex UI flows.

### Test Structure and Conventions

#### 1. File Organization

All tests are located in the tests/ directory.

Each feature or module has its own test file, e.g.:

`test_login.py`

`test_user_profile.py`

#### 2. Naming Conventions

Test files: test_<feature>.py
Example: test_login_to_bcss.py

Page Object Models: <page>_page.py
Example: login_failure_screen_page.py

#### 3. Test Function Anatomy

Each test typically follows this structure:

```Python
def test_user_can_login(page):
    """
      Verifies that a predefined user can successfully log in and reach the BCSS home page.

      Steps:
          - Logs in using the 'Hub Manager State Registered at BCS01' user defined in users.json.
          - Asserts that the application title is visible and contains the expected text.
    """
    UserTools.user_login(page, "Hub Manager State Registered at BCS01") # Users are defined in users.json
    expect(page.locator("#ntshAppTitle")).to_contain_text(
        "Bowel Cancer Screening System"
    )
```

- Use Page Object Model (POM) for UI interactions
- Keep assertions clear and focused
- Avoid hard coded waits - prefer expect() or Playwright’s built-in waiting mechanisms

#### 4. Markers and Tags

Use @pytest.mark.<tag> to run a subset of tests as required:

```Python
@pytest.mark.smoke
def test_basic_login(page):
```

So for example running `pytest -m "smoke" --tracing on` will only run tests that have the 'smoke' mark.

pytest marks are defined in the `pytest.ini` file.

Common tags:
smoke: quick validation of core functionality
regression: full suite for release validation
slow: long-running tests

#### 5. Skipping and Expected Failures

Use Pytest decorators to manage test behavior:

```Python
@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature(page):


@pytest.mark.xfail(reason="Known bug in login flow")
def test_login_with_invalid_credentials(page):
```

### Page Object Model (POM) Guidelines

#### 1. What is a POM?

A Page Object Model is a design pattern that encapsulates UI interactions for a specific page or component into a dedicated class. This keeps test code clean, readable, and reusable.

Instead of writing raw selectors and actions in your test, you use methods from a page class:

```Python
def test_user_can_login(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("user@example.com", "securepassword")
    assert login_page.is_logged_in()
```

#### 2. Location and Structure

All POMs are stored in the pages/ directory.

Each file represents a single page or component, for example:

- login_page.py
- dashboard_page.py
- user_profile_page.py

#### 3. Naming Convention

- Class names: LoginPage, DashboardPage, etc.
- File names: lowercase with underscores, matching the class name (e.g. login_page.py)

#### 4. Anatomy of a Page Class

```Python
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("button[type='submit']")

    def navigate(self):
        self.page.goto("https://bcss.example.com/login")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def is_logged_in(self):
        return self.page.locator("text=Welcome").is_visible()
```

### Utility Modules

Utility modules help you abstract common functionality that doesn’t belong in a specific page class. This keeps your POMs lean and your tests DRY (Don’t Repeat Yourself).

#### 1. Purpose of Utility Modules

- Handle reusable actions (e.g. login, file uploads, date pickers)
- Provide custom assertions or wait conditions
- Manage test data generation or environment setup

#### 2. Example: Wait Utility

```Python
# utils/wait_utils.py

from playwright.sync_api import expect

def wait_for_element(page, selector, timeout=5000):
    """
    Waits for a specific element to become visible on the page within a given timeout.

    Args:
        page (Page): The Playwright page instance to operate on.
        selector (str): The CSS selector of the element to wait for.
        timeout (int, optional): Maximum time to wait for visibility in milliseconds. Defaults to 5000.

    Returns:
        None
    """
    expect(page.locator(selector)).to_be_visible(timeout=timeout)
```

#### 3. Best Practices

- Keep utilities modular and single-purpose.
- Avoid hard coding values - use configuration files or environment variables.
- Document each function with a short docstring.
- Use type hints for clarity and IDE support.

#### 4. Blueprint Utilities

This project was built on the existing NHS England Playwright Python Blueprint. The blueprint provides the following utility classes, that can be used to aid in testing:

| Utility                                                       | Description                                  |
| ------------------------------------------------------------- | -------------------------------------------- |
| [Axe](./docs/utility-guides/Axe.md)                           | Accessibility scanning using axe-core.       |
| [Date Time Utility](./docs/utility-guides/DateTimeUtility.md) | Basic functionality for managing date/times. |
| [NHSNumberTools](./docs/utility-guides/NHSNumberTools.md)     | Basic tools for working with NHS numbers.    |
| [User Tools](./docs/utility-guides/UserTools.md)              | Basic user management tool.                  |

#### 5. BCSS Project Specific Utilities

These utilities have been created specifically for the bcss playwright project:

| Utility                                                                                 | Description                                                                                                                                    |
| --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| [Appointments Utility](.docs/utility-guides/Appointments.md)                            | Automates appointment slot setup for multiple practitioners at a screening centre, including calendar navigation and slot configuration.       |
| [Batch Processing Utility](.docs/utility-guides/BatchProcessing.md)                     | Provides a one-stop function to process batches end-to-end, including preparation, printing, subject verification, and archive confirmation.   |
| [Calendar Picker](.docs/utility-guides/CalendarPicker.md)                               | Provides methods to interact with BCSS’s three distinct calendar types                                                                         |
| [Dataset Field Utility](.docs/utility-guides/DatasetField.md)                           | Dynamically locates and populates input/select fields based on label text, supporting both flat and nested dataset structures.                 |
| [Fit Kit Utility](.docs/utility-guides/FitKit.md)                                       | Provides methods to generate FIT device IDs, split test kits into normal/abnormal groups, and simulate compartment 3 workflows.                |
| [Investigation Dataset Utility](.docs/utility-guides/InvestigationDataset.md)           | Automates the completion and progression of investigation datasets based on subject age and result type, with support for custom field values. |
| [Last Test Run](.docs/utility-guides/LastTestRun.md)                                    | Tracks when specific tests were last executed to avoid redundant setups and enable “run once per day” logic.                                   |
| [Load Properties](.docs/utility-guides/LoadProperties.md)                               | Loads key-value pairs from `.properties` files to centralize configuration and avoid hard-coded values in tests.                               |
| [Manual Cease Workflow](.docs/utility-guides/ManualCease.md)                            | Automates subject creation, UI interaction, and DB verification for manual cease flows, including disclaimer handling.                         |
| [NHS Number Tools](.docs/utility-guides/NHSNumberTools.md)                              | Validates NHS numbers and formats them for display or input, ensuring compliance with NHS standards.                                           |
| [Notify Criteria Parser](.docs/utility-guides/NotifyCriteriaParser.md)                  | Parses compact Notify filter strings (e.g. "S1 (S1w) - sending") into structured components for use in selection builders and SQL queries.     |
| [Oracle Utility](.docs/utility-guides/Oracle.md)                                        | Provides direct access to Oracle DB for querying, executing stored procedures, and generating synthetic test subjects.                         |
| [PDF Reader](.docs/utility-guides/PDFReader.md)                                         | Extracts NHS numbers from PDF documents by scanning for "NHS No:" markers, returning results as a pandas DataFrame.                            |
| [Screening Subject Page Searcher](.docs/utility-guides/ScreeningSubjectPageSearcher.md) | Provides methods to search for subjects by NHS number, name, DOB, postcode, and status, and verify event status directly from the UI.          |
| [Subject Demographics](.docs/utility-guides/SubjectDemographics.md)                     | Updates subject demographic data such as DOB and postcode, with support for randomized age ranges and direct field manipulation.               |
| [Subject Notes](.docs/utility-guides/SubjectNotes.md)                                   | Verifies note content against database and UI, and confirms proper archiving of removed notes as obsolete.                                     |
| [Subject Selection Query Builder](.docs/utility-guides/SubjectSelectionQueryBuilder.md) | Dynamically builds SQL queries to retrieve subjects based on screening status, demographics, Notify messages, and more.                        |
| [Table Utility](.docs/utility-guides/TableUtil.md)                                      | Provides helper methods for interacting with HTML tables, including row selection, column indexing, and data extraction.                       |
| [User Tools](.docs/utility-guides/UserTools.md)                                         | Manages test user credentials via `users.json`, supports login automation, and retrieves user metadata for role-based testing.                 |

## Using the Jira Upload Script

Included with this code is a Jira Upload utility that will allow for the uploading of artifacts from test runs to
a Jira ticket directly. The script itself ([`jira_upload.py`](jira_upload.py)) can be invoked using the following
command:

```shell
python jira_upload.py
```

For this to work, you need to set the follow environment variables (which you can do via local.env):

| Key                   | Required | Description                                                                                            |
| --------------------- | -------- | ------------------------------------------------------------------------------------------------------ |
| `JIRA_URL`              | Yes      | The Jira instance url to connect to                                                                    |
| `JIRA_PROJECT_KEY`      | Yes      | The project key for the Jira project to upload to                                                      |
| `JIRA_API_KEY`          | Yes      | The Jira API key for your user, which can be generated in Jira via Profile > Personal Access Tokens    |
| `JIRA_TICKET_REFERENCE` | No       | The Jira ticket you want to default to, if required. Can be left blank to use branch-based referencing |

This command will do the following actions:

1. Work out the Jira ticket to upload to and confirm it is a valid reference, by using the following logic:
   1. If a `--jira-ref` value has been provided, use that value.
   2. If a `JIRA_TICKET_REFERENCE` environment variable exists, use that value.
   3. If none of the above, check if you are in a feature branch and if so, compiles the Jira ticket reference by combining the project key and the end of the feature branch (when in the format `feature/<shortcode>-<jira_ticket_number>`).
2. Check the `test-results/` directory (or custom directory if specified) for appropriate files under 10MB (Jira's file limit), specifically:
   1. HTML files (e.g. `report.html` generated by `pytest`).
   2. Trace Files (e.g. `test_name/trace.zip` generated by Playwright).
   3. Screenshots (e.g. `test_screenshot.png` generated by Playwright).
   4. CSV Files (e.g. `results.csv` generated during test execution from the UI).
3. Prompt the user to confirm that they are updating the correct ticket and the correct files are being uploaded. If files already exist on the ticket with a matching name, a unique name will be provided unless `--overwrite-files` is provided.
4. If `y` is selected, upload the files and add a comment (unless `--no-comment` is provided) to Jira outlining the files uploaded and if possible, the environment information from the test run (unless `--no-env-data` is provided).

You can also pass in the following arguments which will have the noted effects:

| Argument                      | Description                                                                                                                   |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `--jira-ref <Jira Reference>` | The Jira ticket to upload to. Will take precedence over auto-deriving from branch name and the set environment variable.      |
| `--results-dir <Directory>`   | The directory to point to. If not set, points to `test-results/` (the default directory for test results in this repository). |
| `--no-html`                   | Don't include HTML files in the upload.                                                                                       |
| `--no-trace`                  | Don't include Trace files (.zip) in the upload.                                                                               |
| `--no-csv`                    | Don't include CSV files in the upload.                                                                                        |
| `--no-screenshots`            | Don't include screenshots (.png) in the upload.                                                                               |
| `--no-comment`                | Don't add a Jira comment highlighting the results.                                                                            |
| `--no-env-data`               | Don't include environment data in the Jira comment (if getting environment data has been configured).                         |
| `--overwrite-files`           | If a filename exists on the ticket that matches those in the results directory, overwrite them.                               |
| `--auto-confirm`              | Will not ask if you want to proceed if provided, and will assume that yes has been pressed.                                   |

Further information on the available actions for this logic can be found in the [Jira Confluence Utility utility guide](./docs/utility-guides/JiraConfluenceUtil.md).

## Contributing

Further guidance on contributing to this project can be found in our [contribution](./CONTRIBUTING.md) page.

### Contacts

If you have any ideas or require support for this project, please [raise an issue via this repository](https://github.com/nhs-england-tools/playwright-python-blueprint/issues/new/choose) using the appropriate template.

If you have any general queries regarding this blueprint, please contact [dave.harding1@nhs.net](mailto:dave.harding1@nhs.net).

### Licence

Unless stated otherwise, the codebase is released under the [MIT License](LICENCE.md). This covers both the codebase and any sample code in the documentation.

Any HTML or Markdown documentation is [© Crown Copyright](https://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/crown-copyright/) and available under the terms of the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
