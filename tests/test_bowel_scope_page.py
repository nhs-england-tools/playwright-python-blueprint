import pytest
from playwright.sync_api import Page, expect
from pages.login import BcssLoginPage


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    # Log in to BCSS
    login_page = BcssLoginPage(page)
    login_page.login_as_user_bcss401()

    # Go to bowel scope page
    page.get_by_role("link", name="Bowel Scope").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Bowel Scope")


@pytest.mark.smoke
def test_bowel_scope_page_navigation(page: Page) -> None:
    # Bowel scope appointments page loads as expected
    page.get_by_role("link", name="View Bowel Scope Appointments").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Appointment Calendar")

    # Return to main menu
    page.get_by_role("link", name="Main Menu").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Main Menu")
