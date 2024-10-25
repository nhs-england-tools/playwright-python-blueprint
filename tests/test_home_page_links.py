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


@pytest.mark.smoke
def test_home_page_links_navigation(page: Page) -> None:
    # Click 'show sub menu' link
    page.get_by_role("link", name="Show Sub-menu").click()
    # Verify a sub menu is visible
    expect(page.get_by_role("link", name="List All Sites")).to_be_visible()
    # Click 'hide sub menu' link
    page.get_by_role("link", name="Hide Sub-menu").click()
    # Verify sub menu is hidden (alerts are visible)
    expect(page.get_by_role("cell", name="Alerts", exact=True)).to_be_visible()
    # Click 'select org' link
    page.get_by_role("link", name="Select Org").click()
    # Verify select org page is displayed
    expect(page.locator("form")).to_contain_text("Choose an Organisation")
    # Click the 'back' link
    page.get_by_role("link", name="Back").click()
    # Verify main menu is displayed
    expect(page.get_by_role("cell", name="Alerts", exact=True)).to_be_visible()
    # Click release notes link
    page.get_by_role("link", name="- Release Notes").click()
    # Verify release notes are displayed
    expect(page.locator("#page-title")).to_contain_text("Release Notes")
    # Click the 'back' link
    page.get_by_role("link", name="Back").click()
    # Click the refresh alerts link
    page.get_by_role("link", name="Refresh alerts").click()  # TODO - verify last updated date/time is correct
    # Click the user guide link
    page.get_by_role("link", name="User guide").click()  # TODO - verify correct new tab has opened
    # Click 'help' link
    page.get_by_role("link", name="Help").click()  # TODO - verify correct new tab has opened
