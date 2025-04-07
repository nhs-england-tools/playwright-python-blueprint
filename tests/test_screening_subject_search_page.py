import pytest
from sys import platform
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.screening_subject_search.subject_screening_search_page import (
    ScreeningStatusSearchOptions,
    LatestEpisodeStatusSearchOptions,
    SearchAreaSearchOptions,
)
from pages.screening_subject_search.subject_screening_summary import SubjectScreeningSummary
from utils.screening_subject_page_searcher import (
    search_subject_by_nhs_number,
    search_subject_by_surname,
    search_subject_by_forename,
    search_subject_by_dob,
    search_subject_by_postcode,
    search_subject_by_episode_closed_date,
    check_clear_filters_button_works,
    search_subject_by_status,
    search_subject_by_latest_event_status,
    search_subject_by_search_area,
)
from utils.user_tools import UserTools
from jproperties import Properties


@pytest.fixture
def tests_properties() -> dict:
    """
    Reads the 'bcss_tests.properties' file and populates a 'Properties' object.
    Returns a dictionary of properties for use in tests.

    Returns:
        dict: A dictionary containing the values loaded from the 'bcss_tests.properties' file.
    """
    configs = Properties()
    if platform == "win32":  # File path from content root is required on Windows OS
        with open("tests/bcss_tests.properties", "rb") as read_prop:
            configs.load(read_prop)
    elif platform == "darwin":  # Only the filename is required on macOS
        with open("bcss_tests.properties", "rb") as read_prop:
            configs.load(read_prop)
    return configs.properties


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as a test user and navigates to the
    screening_subject_search page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager State Registered")

    # Go to screening subject search page
    BasePage(page).go_to_screening_subject_search_page()


@pytest.mark.smoke
def test_search_screening_subject_by_nhs_number(
    page: Page, tests_properties: dict
) -> None:
    """
    Confirms a screening subject can be searched for, using their nhs number by doing the following:
    - Clear filters (if any filters have persisted the NHS number field is inactive)
    - Enter an NHS number
    - Press Tab (required after text input, to make the search button become active).
    - Click search button
    - Verify the Subject Screening Summary page is displayed
    """
    search_subject_by_nhs_number(page, tests_properties["nhs_number"])


def test_search_screening_subject_by_surname(
    page: Page, tests_properties: dict
) -> None:
    """
    Confirms a screening subject can be searched for, using their surname by doing the following:
    - Clear filters
    - Enter a surname
    - Press Tab (required after text input, to make the search button become active).
    - Click search button
    - Verify the subject summary page is displayed
    """
    search_subject_by_surname(page, tests_properties["surname"])


def test_search_screening_subject_by_forename(
    page: Page, tests_properties: dict
) -> None:
    """
    Confirms a screening subject can be searched for, using their forename by doing the following:
    - Clear filters
    - Enter a forename
    - Press Tab (required after text input, to make the search button become active).
    - Click search button
    - Verify the subject summary page is displayed
    """
    search_subject_by_forename(page, tests_properties["forename"])


def test_search_screening_subject_by_dob(page: Page, tests_properties: dict) -> None:
    """
    Confirms a screening subject can be searched for, using their date of birth by doing the following:
    - Clear filters
    - Enter a date in the dob field
    - Press Tab (required after text input, to make the search button become active).
    - Click search button
    - Verify the subject search results page is displayed
    """
    search_subject_by_dob(page, tests_properties["subject_dob"])


def test_search_screening_subject_by_postcode(page: Page) -> None:
    """
    Confirms a screening subject can be searched for, using their postcode by doing the following:
    - Clear filters
    - Enter a postcode
    - Press Tab (required after text input, to make the search button become active).
    - Click search button
    - Verify the subject search results page is displayed
    """
    search_subject_by_postcode(page, "*")


def test_search_screening_subject_by_episode_closed_date(
    page: Page, tests_properties: dict
) -> None:
    """
    Confirms a screening subject can be searched for, using their episode closed date by doing the following:
    - Clear filters
    - Enter an "episode closed date"
    - Press Tab (required after text input, to make the search button become active).
    - Click search button
    - Verify the subject search results page is displayed
    - Verify the results contain the date that was searched for
    """
    search_subject_by_episode_closed_date(page, tests_properties["episode_closed_date"])


def test_search_criteria_clear_filters_button(
    page: Page, tests_properties: dict
) -> None:
    """
    Confirms the 'clear filters' button on the search page works as expected by doing the following:
    - Enter number in NHS field and verify value
    - Click clear filters button and verify field is empty
    """
    check_clear_filters_button_works(page, tests_properties["nhs_number"])


# Tests searching via the "Screening Status" drop down list
def test_search_screening_subject_by_status_call(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (call) by doing the following:
    - Clear filters
    - Select status from dropdown
    - Pressing Tab is required after text input, to make the search button become active.
    - Click search button
    - Verify the subject search results page is displayed
    """
    search_subject_by_status(page, ScreeningStatusSearchOptions.CALL_STATUS.value)


def test_search_screening_subject_by_status_inactive(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (call) by doing the following:
    - Clear filters
    - Select status from dropdown
    - Pressing Tab is required after text input, to make the search button become active.
    - Click search button
    - Verify the subject search results page is displayed
    """
    search_subject_by_status(page, ScreeningStatusSearchOptions.INACTIVE_STATUS.value)


def test_search_screening_subject_by_status_opt_in(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (call) by doing the following:
    - Clear filters
    - Select status from dropdown
    - Pressing Tab is required after text input, to make the search button become active.
    - Click search button
    - Verify the subject search results page is displayed
    """
    search_subject_by_status(page, ScreeningStatusSearchOptions.OPT_IN_STATUS.value)


def test_search_screening_subject_by_status_recall(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (call) by doing the following:
    - Clear filters
    - Select status from dropdown
    - Pressing Tab is required after text input, to make the search button become active.
    - Click search button
    - Verify the subject search results page is displayed
    """
    search_subject_by_status(page, ScreeningStatusSearchOptions.RECALL_STATUS.value)


def test_search_screening_subject_by_status_self_referral(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (call) by doing the following:
    - Clear filters
    - Select status from dropdown
    - Pressing Tab is required after text input, to make the search button become active.
    - Click search button
    - Verify the subject search results page is displayed
    """
    search_subject_by_status(
        page, ScreeningStatusSearchOptions.SELF_REFERRAL_STATUS.value
    )


def test_search_screening_subject_by_status_surveillance(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (call) by doing the following:
    - Clear filters
    - Select status from dropdown
    - Pressing Tab is required after text input, to make the search button become active.
    - Click search button
    - Verify the subject search results page is displayed
    """
    search_subject_by_status(
        page, ScreeningStatusSearchOptions.SURVEILLANCE_STATUS.value
    )


def test_search_screening_subject_by_status_seeking_further_data(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (call) by doing the following:
    - Clear filters
    - Select status from dropdown
    - Pressing Tab is required after text input, to make the search button become active.
    - Click search button
    - Verify the subject search results page is displayed
    """
    search_subject_by_status(
        page, ScreeningStatusSearchOptions.SEEKING_FURTHER_DATA_STATUS.value
    )


def test_search_screening_subject_by_status_ceased(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (call) by doing the following:
    - Clear filters
    - Select status from dropdown
    - Pressing Tab is required after text input, to make the search button become active.
    - Click search button
    - Verify the subject search results page is displayed
    """
    search_subject_by_status(page, ScreeningStatusSearchOptions.CEASED_STATUS.value)


def test_search_screening_subject_by_status_bowel_scope(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (call) by doing the following:
    - Clear filters
    - Select status from dropdown
    - Pressing Tab is required after text input, to make the search button become active.
    - Click search button
    - Verify the subject search results page is displayed
    """
    search_subject_by_status(
        page, ScreeningStatusSearchOptions.BOWEL_SCOPE_STATUS.value
    )


def test_search_screening_subject_by_status_lynch_surveillance(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (call) by doing the following:
    - Clear filters
    - Select status from dropdown
    - Pressing Tab is required after text input, to make the search button become active.
    - Click search button
    - Verify the subject search results page is displayed
    """
    search_subject_by_status(
        page, ScreeningStatusSearchOptions.LYNCH_SURVEILLANCE_STATUS.value
    )


def test_search_screening_subject_by_status_lynch_self_referral(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (call) by doing the following:
    - Clear filters
    - Select status from dropdown
    - Pressing Tab is required after text input, to make the search button become active.
    - Click search button
    - Verify the subject search results page is displayed
    """
    search_subject_by_status(
        page, ScreeningStatusSearchOptions.LYNCH_SELF_REFERRAL_STATUS.value
    )


# search_subject_by_latest_event_status
def test_search_screening_subject_by_latest_episode_status_open_paused(
    page: Page,
) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (call) by doing the following:
    - Clear filters
    - Select status from dropdown
    - Pressing Tab is required after text input, to make the search button become active.
    - Click search button
    - Verify the subject search results page is displayed
    """
    search_subject_by_latest_event_status(
        page, LatestEpisodeStatusSearchOptions.OPEN_PAUSED_STATUS.value
    )


def test_search_screening_subject_by_latest_episode_status_closed(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (call) by doing the following:
    - Clear filters
    - Select status from dropdown
    - Pressing Tab is required after text input, to make the search button become active.
    - Click search button
    - Verify the subject search results page is displayed
    """
    search_subject_by_latest_event_status(
        page, LatestEpisodeStatusSearchOptions.CLOSED_STATUS.value
    )


def test_search_screening_subject_by_latest_episode_status_no_episode(
    page: Page,
) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (call) by doing the following:
    - Clear filters
    - Select status from dropdown
    - Pressing Tab is required after text input, to make the search button become active.
    - Click search button
    - Verify the subject search results page is displayed
    """
    search_subject_by_latest_event_status(
        page, LatestEpisodeStatusSearchOptions.NO_EPISODE_STATUS.value
    )


# Tests searching via the "Search Area" drop down list
def test_search_screening_subject_by_home_hub(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the search area (home hub) by doing the following:
    - Clear filters
    - Select screening status "recall" (searching by search area requires another search option to be selected)
    - Select "Home Hub" option from dropdown
    - Click search button
    - Verify search results are displayed
    """
    search_subject_by_search_area(
        page,
        ScreeningStatusSearchOptions.RECALL_STATUS.value,
        SearchAreaSearchOptions.SEARCH_AREA_HOME_HUB.value,
    )


def test_search_screening_subject_by_gp_practice(
    page: Page, tests_properties: dict
) -> None:
    """
    Confirms screening subjects can be searched for, using the search area (home hub) by doing the following:
    - Clear filters
    - Select screening status "recall" (searching by search area requires another search option to be selected)
    - Select "GP Practice" option from dropdown
    - Enter GP practice code
    - Click search button
    - Verify search results are displayed
    # Verify springs health centre is visible in search results
    """
    search_subject_by_search_area(
        page,
        ScreeningStatusSearchOptions.CALL_STATUS.value,
        SearchAreaSearchOptions.SEARCH_AREA_GP_PRACTICE.value,
        tests_properties["gp_practice_code"],
    )
    SubjectScreeningSummary(page).verify_result_contains_text("SPRINGS HEALTH CENTRE")


def test_search_screening_subject_by_ccg(page: Page, tests_properties: dict) -> None:
    """
    Confirms screening subjects can be searched for, using the search area (ccg) by doing the following:
    - Clear filters
    - Select screening status "call" (searching by search area requires another search option to be selected)
    - Select "CCG" from dropdown
    - Enter CCG code
    - Enter GP practice code
    - Click search button
    - Verify search results are displayed
    """
    search_subject_by_search_area(
        page,
        ScreeningStatusSearchOptions.CALL_STATUS.value,
        SearchAreaSearchOptions.SEARCH_AREA_CCG.value,
        tests_properties["ccg_code"],
        tests_properties["gp_practice_code"],
    )


def test_search_screening_subject_by_screening_centre(
    page: Page, tests_properties: dict
) -> None:
    """
    Confirms screening subjects can be searched for, using the search area (screening centre) by doing the following:
    - Clear filters
    - Select screening status "call" (searching by search area requires another search option to be selected)
    - Select "Screening Centre" option from dropdown
    - Enter a screening centre code
    - Click search button
    - Verify search results are displayed
    """
    search_subject_by_search_area(
        page,
        ScreeningStatusSearchOptions.CALL_STATUS.value,
        SearchAreaSearchOptions.SEARCH_AREA_CCG.value,
        tests_properties["screening_centre_code"],
    )


def test_search_screening_subject_by_whole_database(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the search area (whole database) by doing the following:
    - Clear filters
    - Select screening status "recall" (searching by search area requires another search option to be selected)
    - Select "whole database" option from dropdown
    - Click search button
    - Verify search results are displayed"
    """
    search_subject_by_search_area(
        page,
        ScreeningStatusSearchOptions.RECALL_STATUS.value,
        SearchAreaSearchOptions.SEARCH_AREA_WHOLE_DATABASE.value,
    )
