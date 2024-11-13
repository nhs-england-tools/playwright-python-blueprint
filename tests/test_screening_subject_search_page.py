import pytest
from playwright.sync_api import Page, expect
from pages.login import BcssLoginPage
from pages.screening_subject_search_page import ScreeningSubjectPage


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    # Log in to BCSS
    login_page = BcssLoginPage(page)
    login_page.login_as_user_bcss401()

    # Go to screening subject search page
    page.get_by_role("link", name="Screening Subject Search").click()


@pytest.mark.smoke
def test_search_screening_subject_by_nhs_number(page: Page) -> None:
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
    # Enter a surname
    page.locator("#A_C_Surname").fill("Absurd")

    # Press Tab (required after text input, to make the search button become active).
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject summary page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Screening Summary")


def test_search_screening_subject_by_forename(page: Page) -> None:
    # Enter a forename
    page.get_by_label("Forename").fill("Pentagram")

    # Press Tab (required after text input, to make the search button become active).
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject summary page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Screening Summary")


def test_search_screening_subject_by_dob(page: Page) -> None:
    # Enter a date in the dob field
    page.locator("#A_C_DOB_From").fill("11/01/1934")

    # Press Tab (required after text input, to make the search button become active).
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_postcode(page: Page) -> None:
    # Enter a postcode
    page.locator("#A_C_Postcode").fill("*")

    # Press Tab (required after text input, to make the search button become active).
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_criteria_clear_filters_button(page: Page) -> None:
    # Enter number in NHS field and verify value
    page.get_by_label("NHS Number").fill("34344554353")
    expect(page.get_by_label("NHS Number")).to_have_value("34344554353")

    # Click clear filters button and verify field is empty
    page.get_by_role("button", name="Clear Filters").click()
    expect(page.get_by_label("NHS Number")).to_be_empty()


# Tests for searching via the status drop down list
def test_search_screening_subject_by_status_call(page: Page, self=None) -> None:
    # Select status from dropdown
    ScreeningSubjectPage(page).select_status_call()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_inactive(page: Page, self=None) -> None:
    # Select status from dropdown
    ScreeningSubjectPage(page).select_status_inactive()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_opt_in(page: Page, self=None) -> None:
    # Select status from dropdown
    ScreeningSubjectPage(page).select_status_opt_in()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_recall(page: Page, self=None) -> None:
    # Select status from dropdown
    ScreeningSubjectPage(page).select_status_recall()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_self_referral(page: Page, self=None) -> None:
    # Select status from dropdown
    ScreeningSubjectPage(page).select_status_self_referral()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_surveillance(page: Page, self=None) -> None:
    # Select status from dropdown
    ScreeningSubjectPage(page).select_status_surveillance()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_seeking_further_data(page: Page, self=None) -> None:
    # Select status from dropdown
    ScreeningSubjectPage(page).select_status_seeking_further_data()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_ceased(page: Page, self=None) -> None:
    # Select status from dropdown
    ScreeningSubjectPage(page).select_status_ceased()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_bowel_scope(page: Page, self=None) -> None:
    # Select status from dropdown
    ScreeningSubjectPage(page).select_status_bowel_scope()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_lynch_surveillance(page: Page, self=None) -> None:
    # Select status from dropdown
    ScreeningSubjectPage(page).select_status_lynch_surveillance()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_lynch_self_referral(page: Page, self=None) -> None:
    # Select status from dropdown
    ScreeningSubjectPage(page).select_status_lynch_self_referral()

    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")

    # Click search button
    page.get_by_role("button", name="Search").click()

    # Verify the subject search results page is displayed
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Screening Summary")
