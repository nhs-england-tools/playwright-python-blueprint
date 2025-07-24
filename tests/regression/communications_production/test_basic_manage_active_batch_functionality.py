import pytest
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.communication_production.communications_production_page import (
    CommunicationsProductionPage,
)
from pages.communication_production.batch_list_page import ActiveBatchListPage
from utils.user_tools import UserTools
from pages.communication_production.manage_active_batch_page import (
    ManageActiveBatchPage,
)
from utils.batch_processing import prepare_and_print_batch


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page) -> None:
    """
    Before every test is executed, this fixture logs in to BCSS as a test user and navigates to the active batch list page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager at BCS01")

    # Go to active batch list page
    BasePage(page).go_to_communications_production_page()
    CommunicationsProductionPage(page).go_to_active_batch_list_page()


@pytest.mark.letters_tests
@pytest.mark.regression
def test_prepare_retrieve_and_confirm_active_letter_batch(page: Page) -> None:
    """
    Scenario: I can prepare, retrieve and confirm a letter batch of any number of files
    Given I log in to BCSS "England" as user role "HubManagerStateRegistered"
    When I view the active batch list
    And there are open letter batches to process in the active batch list
    Then I view the "Original" type "Open" status active letter batch
    And I prepare the letter batch
    And I retrieve and confirm the letters
    """
    # Access Active Batch List
    batch_list_page = ActiveBatchListPage(page)

    # Ensure the active batch list table is visible
    batch_list_page.assert_batch_table_visible()

    # Locate the first batch with type "Original" and status "Open"
    row = batch_list_page.get_open_original_batch_row()
    if not row:
        pytest.skip("No open 'Original' batches found in the active batch list.")

    # Capture the batch ID from the selected row and click to open
    batch_id = row.locator("a").first.inner_text()
    row.locator("a").first.click()

    # Assert that Manage Active Batch page has loaded
    manage_page = ManageActiveBatchPage(page)
    manage_page.assert_active_batch_details_visible()

    # Prepare, retrieve and confirm the batch using utility method
    prepare_and_print_batch(page, link_text=batch_id)
