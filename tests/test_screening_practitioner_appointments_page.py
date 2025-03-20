import pytest
from playwright.sync_api import Page, expect
from pages.bcss_home_page import MainMenu
from utils.user_tools import UserTools


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as the specified user and navigates to the
    screening_practitioner_appointments page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager State Registered")

    # Go to screening practitioner appointments page
    MainMenu(page).go_to_screening_practitioner_appointments_page()


@pytest.mark.smoke
def test_screening_practitioner_appointments_page_navigation(page: Page) -> None:
    """
    Confirms screening_practitioner_appointments page loads and the expected links are visible
    and clickable (where the user has required permissions).
    """
    # Verify View appointments page opens as expected
    page.get_by_role("link", name="View appointments").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Appointment Calendar")
    page.get_by_role("link", name="Back").click()

    # Verify Patients that Require Colonoscopy Assessment Appointments page opens as expected
    page.get_by_role("link", name="Patients that Require").click()
    expect(page.locator("#page-title")).to_contain_text("Patients that Require Colonoscopy Assessment Appointments")
    page.get_by_role("link", name="Back").click()

    # Verify below links are visible (not clickable due to user role permissions)
    expect(page.get_by_text("Patients that Require Colonoscopy Assessment Appointments - Bowel Scope")).to_be_visible()
    expect(page.get_by_text("Patients that Require Surveillance Appointments")).to_be_visible()
    expect(page.get_by_text("Patients that Require Post-")).to_be_visible()
    expect(page.get_by_text("Set Availability")).to_be_visible()

    # Return to main menu
    page.get_by_role("link", name="Main Menu").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Main Menu")
