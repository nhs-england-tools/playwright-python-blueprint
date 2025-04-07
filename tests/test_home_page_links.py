import pytest
from playwright.sync_api import Page, expect
from utils.user_tools import UserTools
from pages.base_page import BasePage
from utils.date_time_utils import DateTimeUtils


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as a test user and results in the home page
    being displayed
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager State Registered")


@pytest.mark.smoke
def test_home_page_links_navigation(page: Page) -> None:
    """
    Confirms that homepage links are visible and clickable, and the expected pages open when clicking the links
    """
    homepage = BasePage(page)

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
    homepage.click_refresh_alerts_link()
    # Verify that the 'last updated' timestamp matches the current date and time
    (
        expect(page.locator('form[name="refreshCockpit"]')).to_contain_text(
            "Refresh alerts (last updated :" + DateTimeUtils.current_datetime()
        )
    )

    # Click the user guide link
    with page.expect_popup() as page1_info:
        # Check the user guide link works
        page.get_by_role("link", name="User guide").click()
    # Check that the user guide page can be accessed
    page1 = page1_info.value

    # Click 'help' link
    with page.expect_popup() as page2_info:
        # Check the help link works
        page.get_by_role("link", name="Help").click()
    # Check that the help page can be accessed
    page2 = page2_info.value
