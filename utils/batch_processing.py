from pages.base_page import BasePage
from pages.communication_production.communications_production_page import (
    CommunicationsProductionPage,
)
from pages.communication_production.manage_active_batch_page import (
    ManageActiveBatchPage,
)
from pages.communication_production.batch_list_page import (
    ActiveBatchListPage,
    ArchivedBatchListPage,
)
from utils.screening_subject_page_searcher import verify_subject_event_status_by_nhs_no
from utils.oracle.oracle_specific_functions import get_nhs_no_from_batch_id
from utils.oracle.oracle import OracleDB
from utils.pdf_reader import extract_nhs_no_from_pdf
import os
import pytest
from playwright.sync_api import Page
import logging
import pandas as pd
from typing import Optional, Tuple


def batch_processing(
    page: Page,
    batch_type: str,
    batch_description: str,
    latest_event_status: str | list,
    run_timed_events: bool = False,
    get_subjects_from_pdf: bool = False,
    save_csv_as_df: bool = False,
) -> Optional[pd.DataFrame]:
    """
    Processes a batch in the BCSS UI by navigating to the batch, extracting subject NHS numbers (from the database or PDF),
    verifying each subject's event status in the UI, and optionally running timed events or returning batch data as a DataFrame.

    Args:
        page (Page): This is the playwright page object
        batch_type (str): The event code of the batch. E.g. S1 or S9
        batch_description (str): The description of the batch. E.g. Pre-invitation (FIT)
        latest_event_status (str | list): The status the subject will get updated to after the batch has been processed.
        run_timed_events (bool): An optional input that executes bcss_timed_events if set to True
        get_subjects_from_pdf (bool): An optional input to change the method of retrieving subjects from the batch from the DB to the PDF file.
        save_csv_as_df (bool): An optional input to save the CSV from batches as a pandas DF
    """
    logging.info(
        f"[BATCH PROCESSING] Processing {batch_type} - {batch_description} batch"
    )
    BasePage(page).click_main_menu_link()
    BasePage(page).go_to_communications_production_page()
    CommunicationsProductionPage(page).go_to_active_batch_list_page()
    ActiveBatchListPage(page).enter_event_code_filter(batch_type)

    batch_description_cells = page.locator(f"//td[text()='{batch_description}']")

    if (
        batch_description_cells.count() == 0
        and page.locator("td", has_text="No matching records found").is_visible()
    ):
        pytest.fail(f"No {batch_type} {batch_description} batch found")

    for i in range(batch_description_cells.count()):
        row = batch_description_cells.nth(i).locator("..")  # Get the parent row

        # Check if the row contains "Open"
        if row.locator("td", has_text="Open").count() > 0:
            # Find the first link in that row and click it
            link = row.locator("a").first
            link_text = link.inner_text()  # Get the batch id dynamically
            logging.info(
                f"[ASSERTIONS COMPLETE] Successfully found an open '{batch_type} - {batch_description}' batch"
            )
            link.click()
            break
        elif (i + 1) == batch_description_cells.count():
            pytest.fail(
                f"[ASSERTIONS FAILED] No open '{batch_type} - {batch_description}' batch found"
            )

    if get_subjects_from_pdf:
        logging.info(
            f"[UI METHOD] Getting NHS Numbers for batch {link_text} from the PDF File"
        )
        nhs_no_df, csv_df = prepare_and_print_batch(
            page, link_text, get_subjects_from_pdf, save_csv_as_df
        )
    else:
        logging.info(
            f"[DB METHOD] Getting NHS Numbers for batch {link_text} from the DB"
        )
        nhs_no_df, csv_df = prepare_and_print_batch(
            page, link_text, get_subjects_from_pdf, save_csv_as_df
        )
        nhs_no_df = get_nhs_no_from_batch_id(link_text)

    check_batch_in_archived_batch_list(page, link_text)

    if nhs_no_df is None:
        raise ValueError("No NHS numbers were retrieved for the batch")

    for subject in range(len(nhs_no_df)):
        nhs_no = nhs_no_df["subject_nhs_number"].iloc[subject]
        verify_subject_event_status_by_nhs_no(page, nhs_no, latest_event_status)

    if run_timed_events:
        OracleDB().exec_bcss_timed_events(nhs_no_df)

    if save_csv_as_df:
        return csv_df


def prepare_and_print_batch(
    page: Page,
    link_text: str,
    get_subjects_from_pdf: bool = False,
    save_csv_as_df: bool = False,
) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """
    This prepares the batch, retrieves the files and confirms them as printed
    Once those buttons have been pressed it waits for the message 'Batch Successfully Archived'

    Args:
        page (Page): This is the playwright page object
        link_text (str): The batch ID
        get_subjects_from_pdf (bool): An optional input to change the method of retrieving subjects from the batch from the DB to the PDF file.
        save_csv_as_df (bool): An optional input to save the csv as a dataframe

    Returns:
        nhs_no_df (pd.DataFrame | None): if get_subjects_from_pdf is True, this is a DataFrame with the column 'subject_nhs_number' and each NHS number being a record, otherwise it is None
    """
    csv_df = None
    ManageActiveBatchPage(page).click_prepare_button()
    page.wait_for_timeout(
        1000
    )  # This one second timeout does not affect the time to execute, as it is just used to ensure the reprepare batch button is clicked and does not instantly advance to the next step
    ManageActiveBatchPage(page).reprepare_batch_text.wait_for(timeout=60000)

    # This loops through each Retrieve button and clicks each one
    retrieve_button_count = 0
    try:
        for retrieve_button in range(
            ManageActiveBatchPage(page).retrieve_button.count()
        ):
            retrieve_button_count += 1
            logging.debug(f"Clicking retrieve button {retrieve_button_count}")
            # Start waiting for the pdf download
            with page.expect_download() as download_info:
                # Perform the action that initiates download. The line below is running in a FOR loop to click every retrieve button as in some cases more than 1 is present
                ManageActiveBatchPage(page).retrieve_button.nth(retrieve_button).click()
            download_file = download_info.value
            file = download_file.suggested_filename
            # Wait for the download process to complete and save the downloaded file in a temp folder
            download_file.save_as(file)
            if file.endswith(".pdf") and get_subjects_from_pdf:
                nhs_no_df = extract_nhs_no_from_pdf(file)
            elif file.endswith(".csv") and save_csv_as_df:
                csv_df = pd.read_csv(file)
            else:
                nhs_no_df = None
            os.remove(file)  # Deletes the file after extracting the necessary data
    except Exception as e:
        pytest.fail(f"No retrieve button available to click: {str(e)}")

    # This loops through each Confirm printed button and clicks each one
    try:
        for confirm_printed_button in range(retrieve_button_count):
            logging.debug(
                f"Clicking confirm printed button {confirm_printed_button + 1}"
            )
            ManageActiveBatchPage(page).safe_accept_dialog(
                ManageActiveBatchPage(page).confirm_button.nth(0)
            )
    except Exception as e:
        pytest.fail(f"No confirm printed button available to click: {str(e)}")

    try:
        ActiveBatchListPage(page).batch_successfully_archived_msg.wait_for()

        logging.info(f"[BATCH PROCESSING] Batch {link_text} successfully archived")
    except Exception as e:
        pytest.fail(
            f"[BATCH PROCESSING] Batch successfully archived message is not shown: {str(e)}"
        )
    return nhs_no_df, csv_df


def check_batch_in_archived_batch_list(page: Page, link_text) -> None:
    """
    Checks the the batch that was just prepared and printed is now visible in the archived batch list.

    Args:
        page (Page): This is the playwright page object
        link_text (str): The batch ID
    """
    BasePage(page).click_main_menu_link()
    BasePage(page).go_to_communications_production_page()
    CommunicationsProductionPage(page).go_to_archived_batch_list_page()
    ArchivedBatchListPage(page).enter_id_filter(link_text)
    try:
        ArchivedBatchListPage(page).verify_table_data(link_text)
        logging.info(
            f"[UI ASSERTIONS] Batch {link_text} visible in archived batch list"
        )
    except Exception as e:
        logging.error(
            f"[UI ASSERTIONS] Batch {link_text} not visible in archived batch list: {str(e)}"
        )
