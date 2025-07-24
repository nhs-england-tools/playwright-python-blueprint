import pytest
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.communication_production.communications_production_page import (
    CommunicationsProductionPage,
)
from pages.communication_production.batch_list_page import (
    ArchivedBatchListPage,
)
from utils.user_tools import UserTools
from pages.communication_production.manage_archived_batch_page import (
    ManageArchivedBatchPage,
)


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page) -> None:
    """
    Before every test is executed, this fixture logs in to BCSS as a test user and navigates to the archived batch list page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager at BCS01")

    # Go to active batch list page
    BasePage(page).go_to_communications_production_page()
    CommunicationsProductionPage(page).go_to_archived_batch_list_page()


@pytest.mark.letters_tests
@pytest.mark.regression
def test_headings_on_archived_batch_list_screen(page: Page) -> None:
    """
    Scenario: Check headings on Archived Batch List Screen
    Given I log in to BCSS "England" as user role "HubManager"
    When I view the archived batch list
    Then the table contains a sortable and filterable column for each expected header
    """

    archived_batch_list_page = ArchivedBatchListPage(page)

    expected_columns = [
        "ID",
        "Type",
        "Original",
        "Letter Group",
        "Event Code",
        "Description",
        "Batch Split By",
        "Screening Centre",
        "Status",
        "Priority",
        "Date On Letter",
        "Date Archived",
        "Count",
    ]
    # The table contains a sortable and filterable column for each expected header
    for column in expected_columns:
        # Ensure the column is present
        archived_batch_list_page.assert_column_present(column)

        # Assert sortable UI attribute is present
        archived_batch_list_page.assert_column_sortable(column)

        # Assert filterable control is rendered
        archived_batch_list_page.assert_column_filterable(column)


@pytest.mark.letters_tests
@pytest.mark.regression
def test_navigation_to_manage_archived_batch_screen(page: Page) -> None:
    """
    Scenario: Check navigation from Archived Batch List Screen to Manage Archived Batch Screen
    Given I log in to BCSS "England" as user role "HubManager"
    When I view the archived batch list
    And I select an archived batch
    Then I view the details of an archived batch
    """
    archived_batch_list_page = ArchivedBatchListPage(page)

    # Ensure the archived batch table is visible
    archived_batch_list_page.assert_batch_table_visible()

    # Click into the first available archived batch
    archived_batch_list_page.select_first_archived_batch()

    # Assert navigation to the Manage Archived Batch page
    manage_batch_page = ManageArchivedBatchPage(page)
    manage_batch_page.assert_archived_batch_details_visible()
