from pages.base_page import BasePage
from pages.communication_production.communications_production_page import CommunicationsProduction
from pages.communication_production.manage_active_batch_page import ManageActiveBatch
from pages.communication_production.batch_list_page import ActiveBatchList, ArchivedBatchList
from utils.screening_subject_page_searcher import verify_subject_event_status_by_nhs_no
from utils.oracle.oracle_specific_functions import get_nhs_no_from_batch_id
from utils.oracle.oracle import OracleDB
import os
import pytest
from playwright.sync_api import Page
import logging


def batch_processing(
    page: Page,
    batch_type: str,
    batch_description: str,
    latest_event_status: str,
    run_timed_events: bool = False,
) -> None:
    """
    This util is used to process batches. It expects the following inputs:
    - page: This is playwright page variable
    - batch_type: This is the event code of the batch. E.g. S1 or S9
    - batch_description: This is the description of the batch. E.g. Pre-invitation (FIT)
    - latest_event_status: This is the status the subject will get updated to after the batch has been processed.
    - run_timed_events: This is an optional input that executes bcss_timed_events if set to True
    """
    logging.info(f"Processing {batch_type} - {batch_description} batch")
    BasePage(page).click_main_menu_link()
    BasePage(page).go_to_communications_production_page()
    CommunicationsProduction(page).go_to_active_batch_list_page()
    ActiveBatchList(page).enter_event_code_filter(batch_type)

    batch_description_cells = page.locator(f"//td[text()='{batch_description}']")

    if batch_description_cells.count() == 0 and page.locator(
        "td", has_text="No matching records found"
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
                f"Successfully found open '{batch_type} - {batch_description}' batch"
            )
            try:
                logging.info(
                    f"Attempting to get NHS Numbers for batch {link_text} from the DB"
                )
                nhs_no_df = get_nhs_no_from_batch_id(link_text)
                logging.info(
                    f"Successfully retrieved NHS Numbers from batch {link_text}"
                )
            except Exception as e:
                pytest.fail(
                    f"Failed to retrieve NHS Numbers from batch {link_text}, {str(e)}"
                )
            link.click()
            break
        elif (i + 1) == batch_description_cells.count():
            pytest.fail(f"No open '{batch_type} - {batch_description}' batch found")

    prepare_and_print_batch(page, link_text)

    check_batch_in_archived_batch_list(page, link_text)

    first_nhs_no = nhs_no_df["subject_nhs_number"].iloc[0]
    try:
        verify_subject_event_status_by_nhs_no(page, first_nhs_no, latest_event_status)
        logging.info(
            f"Successfully verified NHS number {first_nhs_no} with status {latest_event_status}"
        )
    except Exception as e:
        pytest.fail(f"Verification failed for NHS number {first_nhs_no}: {str(e)}")

    if run_timed_events:
        OracleDB().exec_bcss_timed_events(nhs_no_df)


def prepare_and_print_batch(page: Page, link_text) -> None:
    """
    This method prepares the batch, retreives the files and confirms them as printed
    Once those buttons have been pressed it waits for the message 'Batch Successfully Archived'
    """
    ManageActiveBatch(page).click_prepare_button()
    page.wait_for_timeout(
        1000
    )  # This one second timeout does not affect the time to execute, as it is just used to ensure the reprepare batch button is clicked and does not instantly advance to the next step
    ManageActiveBatch(page).reprepare_batch_text.wait_for()

    # This loops through each Retrieve button and clicks each one
    retrieve_button_count = 0
    try:
        for retrieve_button in range(ManageActiveBatch(page).retrieve_button.count()):
            retrieve_button_count += 1
            logging.info(f"Clicking retrieve button {retrieve_button_count}")
            # Start waiting for the pdf download
            with page.expect_download() as download_info:
                # Perform the action that initiates download. The line below is running in a FOR loop to click every retrieve button as in some cases more than 1 is present
                ManageActiveBatch(page).retrieve_button.nth(retrieve_button).click()
            download_file = download_info.value
            file = download_file.suggested_filename
            # Wait for the download process to complete and save the downloaded file in a temp folder
            download_file.save_as(file)
            os.remove(file)  # Deletes the file after extracting the necessary data
    except Exception as e:
        pytest.fail(f"No retrieve button available to click: {str(e)}")

    # This loops through each Confirm printed button and clicks each one
    try:
        for confirm_printed_button in range(retrieve_button_count):
            logging.info(
                f"Clicking confirm printed button {confirm_printed_button + 1}"
            )
            page.once("dialog", lambda dialog: dialog.accept())
            ManageActiveBatch(page).confirm_button.nth(0).click()
    except Exception as e:
        pytest.fail(f"No confirm printed button available to click: {str(e)}")

    try:
        ActiveBatchList(page).batch_successfully_archived_msg.wait_for()

        logging.info(f"Batch {link_text} successfully archived")
    except Exception as e:
        pytest.fail(f"Batch successfully archived message is not shown: {str(e)}")


def check_batch_in_archived_batch_list(page: Page, link_text) -> None:
    """
    This method checks the the batch that was just prepared and printed is now visible in the archived batch list
    """
    BasePage(page).click_main_menu_link()
    BasePage(page).go_to_communications_production_page()
    CommunicationsProduction(page).go_to_archived_batch_list_page()
    ArchivedBatchList(page).enter_id_filter(link_text)
    try:
        ArchivedBatchList(page).verify_table_data(link_text)
        logging.info(f"Batch {link_text} visible in archived batch list")
    except Exception as e:
        logging.error(f"Batch {link_text} not visible in archived batch list: {str(e)}")
