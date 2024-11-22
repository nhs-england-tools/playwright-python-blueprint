from playwright.sync_api import Page, expect
from pages.login_page import BcssLoginPage


def test_successful_login_to_bcss(page: Page) -> None:
    BcssLoginPage(page).login_as_user_bcss401()
    expect(page.locator("#ntshAppTitle")).to_contain_text("Bowel Cancer Screening System")


def test_login_to_bcss_with_invalid_username(page: Page) -> None:
    username = "BCSSZZZ"
    password = "changeme"
    BcssLoginPage(page).login(username, password)
    expect(page.locator("body")).to_contain_text("Incorrect username or password.")


def test_login_to_bcss_with_invalid_password(page: Page) -> None:
    username = "BCSS401"
    password = "zzzzzz"
    BcssLoginPage(page).login(username, password)
    expect(page.locator("body")).to_contain_text("Incorrect username or password.")


def test_login_to_bcss_with_no_username_or_password(page: Page) -> None:
    username = ""
    password = ""
    BcssLoginPage(page).login(username, password)
    # Login should fail - verify that sign-in button is still visible
    expect(page.get_by_role("button", name="submit")).to_be_visible()
