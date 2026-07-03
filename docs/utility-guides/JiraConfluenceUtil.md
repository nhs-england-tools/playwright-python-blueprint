# Utility Guide: JiraConfluenceUtil

The `JiraConfluenceUtil` utility provides methods for interacting with Jira and Confluence, specifically for uploading Playwright test results and metadata to Jira tickets.

> NOTE: For most use cases, you should use the [jira_upload.py](../../jira_upload.py) script as outlined in the [README](../../README.md).
> This guide is for developers who want to use the utility directly in custom workflows or scripts.

## Table of Contents

- [Utility Guide: JiraConfluenceUtil](#utility-guide-jiraconfluenceutil)
  - [Table of Contents](#table-of-contents)
  - [Using the JiraConfluenceUtil class](#using-the-jiraconfluenceutil-class)
    - [Required Environment Variables](#required-environment-variables)
    - [Initialise the class](#initialise-the-class)
  - [Public Methods](#public-methods)
    - [`get_issue_data`](#get_issue_data)
    - [`get_issue_summary_in_issue_data`](#get_issue_summary_in_issue_data)
    - [`check_attachment_exists_in_issue_data`](#check_attachment_exists_in_issue_data)
    - [`is_valid_jira_reference`](#is_valid_jira_reference)
    - [`determine_jira_reference_local`](#determine_jira_reference_local)
    - [`get_environment_metadata_if_available`](#get_environment_metadata_if_available)
    - [`is_file_is_less_than_jira_file_limit`](#is_file_is_less_than_jira_file_limit)
    - [`upload_test_results_dir_to_jira`](#upload_test_results_dir_to_jira)
  - [Example Usage](#example-usage)

## Using the JiraConfluenceUtil class

### Required Environment Variables

The following environment variables need to be set (in local.env if running locally) for any Jira-based actions:

- **JIRA_URL**: The Jira instance to upload to.
- **JIRA_PROJECT_KEY**: The Jira project key that should be uploaded to.
- **JIRA_API_KEY**: The API key to use to complete actions. Locally you should generate your own key, and use a bot in a pipeline/workflow.

The following environment variables are optional:

- **JIRA_TICKET_REFERENCE**: The Jira ticket to push to if set. If not, will attempt to derive the value from the git branch.

The following environment variables need to be set for any Confluence-based actions:

- **CONFLUENCE_URL**: The Confluence instance to upload to.
- **CONFLUENCE_API_KEY**: The API key to use to complete actions. Locally you should generate your own key, and use a bot in a pipeline/workflow.

### Initialise the class

You can initialise the class by importing and creating an instance:

```python
from utils.jira_confluence_util import JiraConfluenceUtil

util = JiraConfluenceUtil()
```

You can also specify a custom results directory:

```python
util = JiraConfluenceUtil(results_dir="path/to/results")
```

## Public Methods

### `get_issue_data`

```python
get_issue_data(ticket_id: str) -> dict | None
```

Checks if a Jira issue exists and returns its data as a dictionary, or `None` if not found.

---

### `get_issue_summary_in_issue_data`

```python
get_issue_summary_in_issue_data(issue_data: dict) -> str | None
```

Returns a summary string for the given Jira issue data in the format "[Ticket]: [Summary Line]", or `None` if not available.

---

### `check_attachment_exists_in_issue_data`

```python
check_attachment_exists_in_issue_data(issue_data: dict, filename: str) -> bool
```

Checks if a Jira issue already has an attachment with the specified filename.

---

### `is_valid_jira_reference`

```python
is_valid_jira_reference(ticket_id: str) -> bool
```

Validates that the Jira ticket reference is in the expected format (e.g., `SCM-1234` or `BSS2-5678`).

---

### `determine_jira_reference_local`

```python
determine_jira_reference_local() -> str
```

Determines the Jira ticket reference from the current git branch or if `JIRA_TICKET_REFERENCE` has been set.

This is currently configured to search for the format `feature/[Jira Reference]`, so for example:

- `feature/TEST-1234` would return `TEST-1234`.
- `feature/TEST-2345-feature-name` would return `TEST-2345`.

> NOTE: Depending on your projects branch naming strategy, you may want to modify this method to suit your needs
> accordingly.

---

### `get_environment_metadata_if_available`

```python
get_environment_metadata_if_available() -> str
```

This is method designed to return metadata for the environment under test. In this project, it is a stub method
designed to be overwritten.

> NOTE: You will need to populate this method with the code required to get the metadata for your environment.
> It is heavily recommended that you populate `results.json` with the data required, and then read the file
> using this method to extract the data required.

---

### `is_file_is_less_than_jira_file_limit`

```python
is_file_is_less_than_jira_file_limit(file_path: Path) -> bool
```

Checks if the file size is below the Jira upload limit (10MB).

---

### `upload_test_results_dir_to_jira`

```python
upload_test_results_dir_to_jira(
    ticket_id: str,
    overwrite_files: bool = True,
    include_html: bool = True,
    include_trace_files: bool = True,
    include_screenshots: bool = True,
    include_csv: bool = True,
    include_env_metadata: bool = True,
    add_comment: bool = True,
    automatically_accept: bool = False,
) -> None
```

Uploads files from the results directory to the specified Jira ticket.
Options allow you to control which file types are included, whether to overwrite existing files, add a comment, and auto-confirm the upload.

For any files over 10MB, they will **not** be uploaded using this method as they will exceed the default file size limit
set for Jira.

Each of the following arguments relate to the following actions:

- `overwrite_files` = If the file already exists on Jira, it will overwrite the file and use the same name if True. If false, it'll generate a unique filename based on the date/time of the upload.
- `include_html` = Will check for any `.html` files in the root of the `results_dir` provided and include them if under 10MB if True.
- `include_trace_files` = Will check for any `.zip` files in subdirectories of the `results_dir` provided and include them if under 10MB if True, renaming the file to include the subdirectory name.
- `include_screenshots` = Will check for any `.png` files in the rood directory `results_dir` provided and the `screenshot/` subdirectory and include them if under 10MB if True.
- `include_csv` = Will check for any `.csv` files in the root of the `results_dir` provided and include them if under 10MB if True.
- `include_env_metadata` = Will check for any environment metadata generated by `get_environment_metadata_if_available` and include it in the comment if True.
- `add_comment` = Will add a comment to Jira summarizing all the attachments and environment metadata if True.
- `automatically_accept` = Will bypass generating a terminal message that needs to be accepted and assume the answer was `y` if True.

---

## Example Usage

```python
from utils.jira_confluence_util import JiraConfluenceUtil

util = JiraConfluenceUtil()
ticket_id = util.determine_jira_reference_local()
if util.is_valid_jira_reference(ticket_id):
    util.upload_test_results_dir_to_jira(
        ticket_id=ticket_id,
        overwrite_files=True,
        include_html=True,
        include_trace_files=True,
        include_screenshots=True,
        include_csv=True,
        include_env_metadata=True,
        add_comment=True,
        automatically_accept=False
    )
```
