import pytest
from playwright.sync_api import Page, expect

from pages.bcss_home_page import MainMenu
from pages.login_page import BcssLoginPage


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    # Log in to BCSS
    BcssLoginPage(page).login_as_user_bcss401()

    # Go to download page
    MainMenu(page).go_to_download_page()


@pytest.mark.smoke
def test_download_facility_page_navigation(page: Page) -> None:
    # Individual download request and retrieval page loads as expected
    page.get_by_role("link", name="Individual Download Request").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Individual Download Request and Retrieval")

    # Individual download request and retrieval page contains warning message
    expect(page.locator("form[name=\"frm\"]")).to_contain_text("Warning - FS Screening data will not be downloaded")
    page.get_by_role("link", name="Back", exact=True).click()

    # List of Individual downloads page loads as expected
    page.get_by_role("link", name="List of Individual Downloads").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("List of Individual Downloads")
    page.get_by_role("link", name="Back", exact=True).click()

    # Batch download request and retrieval page loads as expected
    page.get_by_role("link", name="Batch Download Request and").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Batch Download Request and Retrieval")

    # Batch download request and retrieval page contains warning message
    expect(page.locator("form[name=\"frm\"]")).to_contain_text("Warning - FS Screening data will not be downloaded")
    page.get_by_role("link", name="Back", exact=True).click()

    # Return to main menu
    page.get_by_role("link", name="Main Menu").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Main Menu")
