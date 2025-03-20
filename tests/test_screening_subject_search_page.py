import pytest
from playwright.sync_api import Page, expect
from pages.bcss_home_page import MainMenu
from pages.screening_subject_search_page import ScreeningStatusSearchOptions, LatestEpisodeStatusSearchOptions, \
    SearchAreaSearchOptions
from utils.user_tools import UserTools


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as the specified user and navigates to the
    screening_subject_search page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager State Registered")

    # Go to screening subject search page
    MainMenu(page).go_to_screening_subject_search_page()


@pytest.mark.smoke
def test_search_screening_subject_by_nhs_number(page: Page) -> None:
    """
    Confirms a screening subject can be searched for, using their nhs number
    """
    # Clear filters (if any filters have persisted the NHS number field is inactive)
    page.get_by_role("button", name="Clear Filters").click()

    # Enter an NHS number
    page.get_by_label("NHS Number").fill("966 529 9271")

    # Press Tab (required after text input, to make the search button become active).
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the Subject Screening Summary page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Screening Summary")


def test_search_screening_subject_by_surname(page: Page) -> None:
    """
    Confirms a screening subject can be searched for, using their surname
    """
    # Enter a surname
    page.locator("#A_C_Surname").fill("Absurd")

    # Press Tab (required after text input, to make the search button become active).
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject summary page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Screening Summary")


def test_search_screening_subject_by_forename(page: Page) -> None:
    """
    Confirms a screening subject can be searched for, using their forename
    """
    # Enter a forename
    page.get_by_label("Forename").fill("Pentagram")

    # Press Tab (required after text input, to make the search button become active).
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject summary page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Screening Summary")


def test_search_screening_subject_by_dob(page: Page) -> None:
    """
    Confirms a screening subject can be searched for, using their date of birth
    """
    # Enter a date in the dob field
    page.locator("#A_C_DOB_From").fill("11/01/1934")

    # Press Tab (required after text input, to make the search button become active).
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_postcode(page: Page) -> None:
    """
    Confirms a screening subject can be searched for, using their postcode
    """
    # Enter a postcode
    page.locator("#A_C_Postcode").fill("*")

    # Press Tab (required after text input, to make the search button become active).
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_episode_closed_date(page: Page) -> None:
    """
    Confirms a screening subject can be searched for, using their episode closed date
    """
    # Enter an "episode closed date"
    page.get_by_label("Episode Closed Date").fill("22/09/2020")

    # Press Tab (required after text input, to make the search button become active).
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")

    # Verify the results contain the date that was searched for
    expect(page.locator("#displayRS")).to_contain_text("22/09/2020")


def test_search_criteria_clear_filters_button(page: Page) -> None:
    """
    Confirms the 'clear filters' button on the search page works as expected
    """
    # Enter number in NHS field and verify value
    page.get_by_label("NHS Number").fill("34344554353")
    expect(page.get_by_label("NHS Number")).to_have_value("34344554353")

    # Click clear filters button and verify field is empty
    page.get_by_role("button", name="Clear Filters").click()
    expect(page.get_by_label("NHS Number")).to_be_empty()


# Tests searching via the "Screening Status" drop down list
def test_search_screening_subject_by_status_call(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (call)
    """
    # Select status from dropdown
    ScreeningStatusSearchOptions(page).select_status_call()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_inactive(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (inactive)
    """
    # Select status from dropdown
    ScreeningStatusSearchOptions(page).select_status_inactive()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_opt_in(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (opt-in)
    """
    # Select status from dropdown
    ScreeningStatusSearchOptions(page).select_status_opt_in()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_recall(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (recall)
    """
    # Select status from dropdown
    ScreeningStatusSearchOptions(page).select_status_recall()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_self_referral(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (self-referral)
    """
    # Select status from dropdown
    ScreeningStatusSearchOptions(page).select_status_self_referral()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_surveillance(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (surveillance)
    """
    # Select status from dropdown
    ScreeningStatusSearchOptions(page).select_status_surveillance()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_seeking_further_data(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (seeking further data)
    """
    # Select status from dropdown
    ScreeningStatusSearchOptions(page).select_status_seeking_further_data()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_ceased(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (ceased)
    """
    # Select status from dropdown
    ScreeningStatusSearchOptions(page).select_status_ceased()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_bowel_scope(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (bowel scope)
    """
    # Select status from dropdown
    ScreeningStatusSearchOptions(page).select_status_bowel_scope()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_lynch_surveillance(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (lynch surveillance)
    """
    # Select status from dropdown
    ScreeningStatusSearchOptions(page).select_status_lynch_surveillance()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_lynch_self_referral(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the screening status (lynch self-referral)
    """
    # Select status from dropdown
    ScreeningStatusSearchOptions(page).select_status_lynch_self_referral()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Screening Summary")


# Tests searching via the "Latest Episode Status" drop down list
def test_search_screening_subject_by_latest_episode_status_open_paused(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the latest episode status (open-paused)
    """
    # Select status from dropdown
    LatestEpisodeStatusSearchOptions(page).select_status_open_paused()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_latest_episode_status_closed(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the latest episode status (closed)
    """
    # Select status from dropdown
    LatestEpisodeStatusSearchOptions(page).select_status_closed()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_latest_episode_status_no_episode(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the latest episode status (no episode)
    """
    # Select status from dropdown
    LatestEpisodeStatusSearchOptions(page).select_status_no_episode()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


# Tests searching via the "Search Area" drop down list
def test_search_screening_subject_by_home_hub(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the search area (home hub)
    """
    # Select screening status "recall" (searching by search area requires another search option to be selected)
    ScreeningStatusSearchOptions(page).select_status_recall()

    # Select "whole database" option from dropdown
    SearchAreaSearchOptions(page).select_search_area_home_hub()

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify search results are displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_gp_practice(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the search area (gp practice)
    """
    # Select screening status "call" (searching by search area requires another search option to be selected)
    ScreeningStatusSearchOptions(page).select_status_call()

    # Select search area from dropdown
    SearchAreaSearchOptions(page).select_search_area_gp_practice()

    # Enter GP practice code
    page.get_by_label("Appropriate Code").fill("C81001")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")

    # Verify springs health centre is visible in search results
    expect(page.locator("#displayRS")).to_contain_text("SPRINGS HEALTH CENTRE")


def test_search_screening_subject_by_ccg(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the search area (ccg)
    """
    # Select screening status "call" (searching by search area requires another search option to be selected)
    ScreeningStatusSearchOptions(page).select_status_call()

    # Select ccg option from dropdown
    SearchAreaSearchOptions(page).select_search_area_ccg()

    # Enter CCG code
    page.get_by_label("Appropriate Code").fill("Z1Z1Z")

    # Enter GP practice code
    page.get_by_label("GP Practice in CCG").fill("C81001")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify search results are displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_screening_centre(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the search area (screening centre)
    """
    # Select screening status "call" (searching by search area requires another search option to be selected)
    ScreeningStatusSearchOptions(page).select_status_call()

    # Select "screening centre" option from dropdown
    SearchAreaSearchOptions(page).select_search_area_screening_centre()

    # Enter a screening centre code
    page.get_by_label("Appropriate Code").fill("BCS001")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify search results are displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_whole_database(page: Page) -> None:
    """
    Confirms screening subjects can be searched for, using the search area (whole database)
    """
    # Select screening status "recall" (searching by search area requires another search option to be selected)
    ScreeningStatusSearchOptions(page).select_status_recall()

    # Select "whole database" option from dropdown
    SearchAreaSearchOptions(page).select_search_area_whole_database()

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify search results are displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")
