import pytest
from playwright.sync_api import Page, expect

import pages.bcss_home_page
from pages.login import BcssLoginPage
from pages.bcss_home_page import BcssHomePage


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    # Log in to BCSS
    username = "BCSS401"
    password = "changeme"
    login_page = BcssLoginPage(page)
    login_page.login(username, password)


@pytest.mark.smoke
def test_home_page_links_navigation(page: Page) -> None:
    homepage = BcssHomePage(page)

    # Click 'show sub menu' link
    homepage.click_sub_menu_link()
    # Verify a sub menu is visible
    expect(page.get_by_role("link", name="List All Sites")).to_be_visible()

    # Click 'hide sub menu' link
    homepage.click_hide_sub_menu_link()
    # Verify sub menu is hidden (alerts are visible)
    expect(page.get_by_role("cell", name="Alerts", exact=True)).to_be_visible()

    # Click 'select org' link
    homepage.click_select_org_link()
    # Verify select org page is displayed
    expect(page.locator("form")).to_contain_text("Choose an Organisation")

    # Click the 'back' link
    homepage.click_back_button()
    # Verify main menu is displayed
    expect(page.get_by_role("cell", name="Alerts", exact=True)).to_be_visible()

    # Click release notes link
    homepage.click_release_notes_link()
    # Verify release notes are displayed
    expect(page.locator("#page-title")).to_contain_text("Release Notes")
    # Click the 'back' button
    homepage.click_back_button()

    # Click the refresh alerts link
    homepage.click_refresh_alerts_link()  # TODO - verify last updated date/time is correct
    # expect(page.locator("form[name=\"refreshCockpit\"]")).to_have_text("Refresh alerts (last updated :25/10/2024 15:06)")

    # Click the user guide link
    homepage.click_user_guide_link()  # TODO - verify correct new tab has opened

    # Click 'help' link
    homepage.click_help_link()  # TODO - verify correct new tab has opened
