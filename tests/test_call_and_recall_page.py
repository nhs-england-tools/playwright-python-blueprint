import pytest
from playwright.sync_api import Page, expect

from pages.bcss_home_page import MainMenu
from pages.login_page import BcssLoginPage


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    # Log in to BCSS
    BcssLoginPage(page).login_as_user_bcss401()

    # Go to call and recall page
    MainMenu(page).go_to_call_and_recall_page()


@pytest.mark.smoke
def test_call_and_recall_page_navigation(page: Page) -> None:
    # Planning and monitoring page loads as expected
    page.get_by_role("link", name="Planning and Monitoring").click()
    expect(page.locator("#page-title")).to_contain_text("Invitations Monitoring - Screening Centre")
    page.get_by_role("link", name="Back").click()

    # Generate invitations page loads as expected
    page.get_by_role("link", name="Generate Invitations").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Generate Invitations")
    page.get_by_role("link", name="Back").click()

    # Invitation generation progress page loads as expected
    page.get_by_role("link", name="Invitation Generation Progress").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Invitation Generation Progress")
    page.get_by_role("link", name="Back").click()

    # Non invitation days page loads as expected
    page.get_by_role("link", name="Non Invitation Days").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Non-Invitation Days")
    page.get_by_role("link", name="Back").click()

    # Age extension rollout page loads as expected
    page.get_by_role("link", name="Age Extension Rollout Plans").click()
    expect(page.locator("#page-title")).to_contain_text("Age Extension Rollout Plans")
    page.get_by_role("link", name="Back").click()

    # Return to main menu
    page.get_by_role("link", name="Main Menu").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Main Menu")


def test_view_an_invitation_plan(page: Page) -> None:
    # Go to planning and monitoring page
    page.get_by_role("link", name="Planning and Monitoring").click()

    # Select a screening centre
    page.get_by_role("link", name="BCS009").click()

    # Select an invitation plan
    page.get_by_role("row", name="07 May 2024 16:43:57").get_by_role("link").click()

    # Verify invitation page is displayed
    expect(page.locator("#page-title")).to_contain_text("View a plan")
