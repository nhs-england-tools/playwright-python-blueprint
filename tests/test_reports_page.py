import pytest
from playwright.sync_api import Page, expect
from pages.login import BcssLoginPage


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    # Log in to BCSS
    login_page = BcssLoginPage(page)
    login_page.login_as_user_bcss401()

    # Open reports page
    page.get_by_role("link", name="Reports").click()


@pytest.mark.smoke
def test_reports_page_navigation(page: Page) -> None:
    # Bureau reports link is visible
    expect(page.get_by_text("Bureau Reports")).to_be_visible()

    # Failsafe reports page opens as expected
    page.get_by_role("link", name="Failsafe Reports").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Failsafe Reports")
    page.get_by_role("link", name="Back").click()

    # Operational reports page opens as expected
    page.get_by_role("link", name="Operational Reports").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Operational Reports")
    page.get_by_role("link", name="Back").click()

    # Strategic reports page opens as expected
    page.get_by_role("link", name="Strategic Reports").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Strategic Reports")
    page.get_by_role("link", name="Back").click()

    # Cancer waiting times reports page opens as expected
    page.get_by_role("link", name="Cancer Waiting Times Reports").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Cancer Waiting Times Reports")
    page.get_by_role("link", name="Back").click()

    # Dashboard opens as expected TODO - this step may be failing legitimately
    # page.get_by_role("link", name="Dashboard").click()
    # expect(page.locator("#ntshPageTitle")).to_contain_text("Dashboard")
    # page.get_by_role("link", name="Back").click()

    # QA Report : Dataset Completion link is visible
    expect(page.get_by_text("QA Report : Dataset Completion")).to_be_visible()

    # Return to main menu
    page.get_by_role("link", name="Main Menu").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Main Menu")
