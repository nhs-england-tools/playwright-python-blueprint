import pytest
from playwright.sync_api import Page
from utils.user_tools import UserTools
from utils.table_util import TableUtils
from pages.base_page import BasePage
from utils.screening_subject_page_searcher import search_subject_by_surname
from pages.screening_subject_search.subject_screening_search_page import (
    SubjectScreeningPage,
)

@pytest.mark.regression
@pytest.mark.subject_search
def test_user_can_search_for_subject_and_results_are_returned(page: Page):
    """
    Verify that User can log in to BCSS "England" as user role "Hub Manager - State Registered"
    Navigate it to the Subject Search Criteria Page & added value "S*" to the "Surname" search field
    Clicking on the search button on the subject search criteria page
    Then Verifies that search results contain Surnames beginning with S
    """

    # Log in as Hub Manager - State Registered (England)
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    # Navigate to the Subject Search Criteria Page
    BasePage(page).go_to_screening_subject_search_page()

    # Add value "S*" to the "Surname" search field
    # click search button on the subject search criteria page
    search_subject_by_surname(page, "S*")

    # Assert that some results are returned with the surname starting with "S*"
    TableUtils(
        page, SubjectScreeningPage(page).results_table_locator
    ).assert_surname_in_table("S*")
