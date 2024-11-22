import pytest
from playwright.sync_api import Page, expect

from pages.bcss_home_page import MainMenu
from pages.login_page import BcssLoginPage


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    # Log in to BCSS
    BcssLoginPage(page).login_as_user_bcss401()

    # Go to fit test kits page
    MainMenu(page).go_to_fit_test_kits_page()


@pytest.mark.smoke
def test_fit_test_kits_page_navigation(page: Page) -> None:
    # Verify FIT rollout summary page opens as expected
    page.get_by_role("link", name="FIT Rollout Summary").click()
    expect(page.locator("body")).to_contain_text("FIT Rollout Summary")
    page.get_by_role("link", name="Back").click()

    # Verify Log Devices page opens as expected
    page.get_by_role("link", name="Log Devices").click()
    expect(page.locator("#page-title")).to_contain_text("Scan Device")
    page.get_by_role("link", name="Back").click()

    # Verify View FIT Kit Result page opens as expected
    page.get_by_role("link", name="View FIT Kit Result").click()
    expect(page.locator("body")).to_contain_text("View FIT Kit Result")
    page.get_by_role("link", name="Back").click()

    # Verify Kit Service Management page opens as expected
    page.get_by_role("link", name="Kit Service Management").click()
    expect(page.locator("#page-title")).to_contain_text("Kit Service Management")
    page.get_by_role("link", name="Back").click()

    # Verify Kit Result Audit page opens as expected
    page.get_by_role("link", name="Kit Result Audit").click()
    expect(page.locator("#page-title")).to_contain_text("Kit Result Audit")
    page.get_by_role("link", name="Back").click()

    # Verify View Algorithm page opens as expected
    page.get_by_role("link", name="View Algorithm").click()
    expect(page.locator("body")).to_contain_text("Select Algorithm")
    page.get_by_role("link", name="Back").click()

    # Verify View Screening Centre FIT page opens as expected
    page.get_by_role("link", name="View Screening Centre FIT").click()
    expect(page.locator("body")).to_contain_text("Select Screening Centre")
    page.get_by_role("link", name="Back").click()

    # Verify Screening Incidents List page opens as expected
    page.get_by_role("link", name="Screening Incidents List").click()
    expect(page.locator("#page-title")).to_contain_text("Screening Incidents List")
    page.get_by_role("link", name="Back").click()

    # Verify FIT QC Products page opens as expected
    page.get_by_role("link", name="Manage QC Products").click()
    expect(page.locator("#page-title")).to_contain_text("FIT QC Products")
    page.get_by_role("link", name="Back").click()

    # Verify Maintain Analysers page opens as expected
    page.get_by_role("link", name="Maintain Analysers").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Maintain Analysers")
    page.get_by_role("link", name="Back").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("FIT Test Kits")

    # Return to main menu
    page.get_by_role("link", name="Main Menu").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Main Menu")
