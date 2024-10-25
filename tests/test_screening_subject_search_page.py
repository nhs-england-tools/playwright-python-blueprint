import pytest
from playwright.sync_api import Page, expect
from pages.login import BcssLoginPage


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    # Log in to BCSS
    username = "BCSS401"
    password = "changeme"
    login_page = BcssLoginPage(page)
    login_page.login(username, password)

    # Go to screening centre search page
    page.get_by_role("link", name="Screening Subject Search").click()


@pytest.mark.smoke
def test_search_screening_subject_by_nhs_number(page: Page) -> None:
    page.get_by_label("NHS Number").fill("953 255 0682")
    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")
    page.get_by_role("button", name="Search").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Screening Summary")


def test_search_screening_subject_by_surname(page: Page) -> None:
    page.locator("#A_C_Surname").fill("Absurd")
    page.keyboard.press("Tab")
    page.get_by_role("button", name="Search").click()
    expect(page.locator("#displayRS")).to_contain_text("ABSURD")


def test_search_screening_subject_by_forename(page: Page) -> None:
    page.get_by_label("Forename").click()
    page.get_by_label("Forename").fill("Pentagram")
    page.keyboard.press("Tab")
    page.get_by_role("button", name="Search").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Screening Summary")


def test_search_screening_subject_by_dob(page: Page) -> None:
    page.locator("#A_C_DOB_From").click()
    page.locator("#A_C_DOB_From").fill("11/01/1934")
    page.keyboard.press("Tab")
    page.get_by_role("button", name="Search").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_postcode(page: Page) -> None:
    page.get_by_label("Postcode").click()
    page.get_by_label("Postcode").fill("yy11yy")
    page.keyboard.press("Tab")
    page.get_by_role("button", name="Search").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_screening_subject_by_status_call(page: Page) -> None:
    page.locator("#A_C_ScreeningStatus").select_option("4001")
    # Pressing Tab is required after text input, to make the search button become active.
    page.keyboard.press("Tab")
    page.wait_for_selector("#ntshPageButtons > input:nth-child(1)")
    page.get_by_role("button", name="Search").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Subject Search Results")


def test_search_criteria_clear_filters_button(page: Page) -> None:
    page.get_by_label("NHS Number").click()
    # Enter number in NHS field and verify value
    page.get_by_label("NHS Number").fill("34344554353")
    expect(page.get_by_label("NHS Number")).to_have_value("34344554353")
    # Click clear filters button and verify field is empty
    page.get_by_role("button", name="Clear Filters").click()
    expect(page.get_by_label("NHS Number")).to_be_empty()
