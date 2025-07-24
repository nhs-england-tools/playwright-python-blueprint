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


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
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
def test_headings_on_active_batch_list_screen(page: Page) -> None:
    """
    Scenario: Check headings on Active Batch List Screen
    Given I log in to BCSS "England" as user role "HubManager"
    When I view the active batch list
    Then the table contains a sortable and filterable column for "<Column Name>"
    """
    batch_list_page = ActiveBatchListPage(page)

    expected_columns = [
        "ID",
        "Type",
        "Original",
        "Event Code",
        "Description",
        "Batch Split By",
        "Screening Centre",
        "Status",
        "Priority",
        "Deadline",
        "Count",
    ]
    # The table contains a sortable and filterable column for each expected header
    for column in expected_columns:
        # Ensure the column is present
        batch_list_page.assert_column_present(column)

        # Assert sortable UI attribute is present
        batch_list_page.assert_column_sortable(column)

        # Assert filterable control is rendered
        batch_list_page.assert_column_filterable(column)


@pytest.mark.letters_tests
@pytest.mark.regression
def test_navigation_to_manage_active_batch_screen(page: Page) -> None:
    """
    Scenario: Check navigation from Active Batch List Screen to Manage Active Batch Screen
    Given I log in to BCSS "England" as user role "HubManager"
    When I view the active batch list
    And I select an active batch
    Then I view the details of an active batch
    """
    batch_list_page = ActiveBatchListPage(page)

    # Ensure the batch list table is visible
    batch_list_page.assert_batch_table_visible()

    # Click into the first available batch link
    batch_list_page.select_first_active_batch()

    # Assert navigation to the Manage Active Batch page
    manage_batch_page = ManageActiveBatchPage(page)
    manage_batch_page.assert_active_batch_details_visible()
