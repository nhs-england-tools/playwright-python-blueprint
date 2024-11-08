import pytest
from playwright.sync_api import Page, expect
from pages.login import BcssLoginPage


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    # Log in to BCSS
    login_page = BcssLoginPage(page)
    login_page.login_as_user_bcss401()

    # Go to Lynch Surveillance page
    page.get_by_role("link", name="Lynch Surveillance").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Lynch Surveillance")


@pytest.mark.smoke
def test_lynch_surveillance_page_navigation(page: Page) -> None:
    # 'Set lynch invitation rates' page loads as expected
    page.get_by_role("link", name="Set Lynch Invitation Rates").click()
    expect(page.locator("#page-title")).to_contain_text("Set Lynch Surveillance Invitation Rates")

    # Return to main menu
    page.get_by_role("link", name="Main Menu").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Main Menu")
