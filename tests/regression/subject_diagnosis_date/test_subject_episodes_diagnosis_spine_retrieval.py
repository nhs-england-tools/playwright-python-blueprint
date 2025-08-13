import pytest
from playwright.sync_api import Page, expect
from utils.user_tools import UserTools
from pages.base_page import BasePage
from pages.screening_subject_search.subject_spine_retrieval_search_page import SpineSearchPage
from pages.screening_subject_search.subject_screening_summary_page import SubjectScreeningSummaryPage

@pytest.mark.regression
@pytest.mark.spine_retrieval_search_tests
def test_user_can_search_for_subject_spine_retrieval(page: Page) -> None:
    """
    Tests to ensure that Spine searching is enabled for English users.
    """
    # Step 1: Log in as Hub Manager - State Registered (England)
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")
    BasePage(page).go_to_screening_subject_search_page()

    # Step 2: Perform spine demographic search
    spine_page = SpineSearchPage(page)
    spine_page_summary = SubjectScreeningSummaryPage(page)
    spine_page_summary.navigate_to_spine_search()
    spine_page.select_demographic_search()
    spine_page.enter_search_criteria(
        dob="06 May 1940",
        surname="vickers",
        forename="rob",
        gender="Male",
        postcode="ex25se"
    )
    spine_page.perform_search()

    # Step 3: Assert in-page alert message
    alert_message = spine_page.get_spine_alert_message()
    assert not alert_message, f"Unexpected alert shown: '{alert_message}'"
    f"Expected alert message not found. Got: '{alert_message}'"
