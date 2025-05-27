# Utility Guide: Batch Processing

The Batch Processing utility provides a one-stop function for processing batches on the active batch list page, streamlining all necessary steps into a single call. **To process a batch, call the `batch_processing` function as described below.**

## Table of Contents

- [Utility Guide: Batch Processing](#utility-guide-batch-processing)
  - [Table of Contents](#table-of-contents)
  - [Example Usage](#example-usage)
  - [Functions Overview](#functions-overview)
    - [Batch Processing](#batch-processing)
      - [Required Arguments](#required-arguments)
      - [Optional Arguments](#optional-arguments)
      - [How This Function Works](#how-this-function-works)
    - [Prepare And Print Batch](#prepare-and-print-batch)
      - [Arguments](#arguments)
      - [Optional Arguments](#optional-arguments-1)
      - [How This Function Works](#how-this-function-works-1)
    - [Check Batch In Archived Batch List](#check-batch-in-archived-batch-list)
      - [Arguments](#arguments-1)
      - [How This Function Works](#how-this-function-works-2)

## Example Usage

```python
from utils.batch_processing import batch_processing

batch_processing(
    page=page,
    batch_type="S1",
    batch_description="Pre-invitation (FIT)",
    latest_event_status=["Status1", "Status2"],  # Can be str or  list[str]
    run_timed_events=True,
    get_subjects_from_pdf=False
)
```

## Functions Overview

For this utility we have the following functions:

- `batch_processing`
- `prepare_and_print_batch`
- `check_batch_in_archived_batch_list`

### Batch Processing

This is the **main entry point function** that should be called to process a batch. It manages and coordinates all the required steps by internally calling the other two functions and auxiliary utilities as needed.

#### Required Arguments

- `page`:
  - Type: `Page`
  - This is the playwright page object which is used to tell playwright what page the test is currently on.
- `batch_type`:
  - Type: `str`
  - This is the event code for the batch. For example: **S1** or **A323**
- `batch_description`:
  - Type: `str`
  - This is the description of the batch. For example: **Pre-invitation (FIT)** or **Post-investigation Appointment NOT Required**
- `latest_event_status`:
  - Type: `str | list[str] |`
  - This is the status or list of statuses the subject(s) will get updated to after the batch has been processed. It is used to check that the subject(s) have been updated to the correct status after a batch has been printed.

#### Optional Arguments

- `run_timed_events`:
  - Type: `bool`
  - If this is set to **True**, then bcss_timed_events will be executed against all the subjects found in the batch
  - These timed events simulate the passage of time-dependent processing steps.
- `get_subjects_from_pdf`:
  - Type: `bool`
  - If this is set to **True**, then the subjects will be retrieved from the downloaded PDF file instead of from the DB

#### How This Function Works

1. It starts off by navigating to the main menu if not already on this page. This is done to ensure that this can be called from any page
2. Once on the main menu it navigates to the active batch list
3. From here it fills in the search filters to narrow down the list of active batches to only those which match the arguments provided
4. Once only the expected batches are shown it checks the status column of the records
   1. If *Prepared* is found then it ignores it, otherwise if *Open* is found then it carries on
5. Now it extracts the ID of the batch and stores it in the local variable `link_text`, this is used later on to extracts the subjects in the batch from the DB
6. After the ID is stored, it clicks on the ID to get to the Manage Active Batch page
7. From Here it calls the `prepare_and_print_batch` function.
   1. If `get_subjects_from_pdf` was set to False it calls `get_nhs_no_from_batch_id`, which is imported from *utils.oracle.oracle_specific_functions*, to get the subjects from the DB and stores them as a pandas DataFrame - **nhs_no_df**
8. Once this is complete it calls the `check_batch_in_archived_batch_list` function
9. Finally, once that function is complete it calls `verify_subject_event_status_by_nhs_no` which is imported from *utils/screening_subject_page_searcher*

### Prepare And Print Batch

This is used when on the Manage Active Batch page.
It is in charge of pressing on the following button: **Prepare Batch**, **Retrieve** and **Confirm Printed**

#### Arguments

- `page`:
  - Type: `Page`
  - This is the playwright page object which is used to tell playwright what page the test is currently on.
- `link_text`:
  - Type: `str`
  - This is the batch ID of the batch currently being processed

#### Optional Arguments

- `get_subjects_from_pdf`:
  - Type: `bool`
  - If this is set to **True**, then the subjects will be retrieved from the downloaded PDF file instead of from the DB

#### How This Function Works

1. It starts off by clicking on the **Prepare Batch** button.
2. After this it waits for the button to turn into **Re-Prepare Batch**. Once this happens it means that the batch is ready to be printed.
3. Now It clicks on each **Retrieve** button visible.
   1. If `get_subjects_from_pdf` was set to True and the file is a **.pdf**, then it calls `extract_nhs_no_from_pdf`, which is imported from *utils/pdf_reader*, to get the subjects from the PDF and stores them as a pandas DataFrame - **nhs_no_df**
   2. For more Info on `extract_nhs_no_from_pdf` please look at: [`PDFReader`](PDFReader.md)
   3. After a file is downloaded, it gets deleted.
4. Then it clicks on each **Confirm Printed** button ensuring to handle the dialog that appears.
5. Finally it checks for the message: *Batch Successfully Archived and Printed*

### Check Batch In Archived Batch List

This function checks that the batch that was just prepared and printed is now visible in the archived batch list

#### Arguments

- `page`:
  - Type: `Page`
  - This is the playwright page object which is used to tell playwright what page the test is currently on.
- `link_text`:
  - Type: `str`
  - This is the batch ID of the batch currently being processed

#### How This Function Works

1. This starts off by navigating to the main menu.
2. From here it goes to the archived batch list page.
3. Once on the archived batch list page, it enters `link_text` into the ID filter.
4. Finally it checks that the batch is visible in the table.
