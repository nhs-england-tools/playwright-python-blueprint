import pytest
from playwright.sync_api import Page, expect

from pages.bcss_home_page import MainMenu
from pages.login_page import BcssLoginPage


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    # Log in to BCSS
    BcssLoginPage(page).login_as_user_bcss401()

    # Go to gFOBT test kits page
    MainMenu(page).go_to_gfob_test_kits_page()


@pytest.mark.smoke
def test_gfob_test_kit_page_navigation(page: Page) -> None:
    # Test kit logging page opens as expected
    page.get_by_role("link", name="Test Kit Logging").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Test Kit Logging")
    page.get_by_role("link", name="Back").click()

    # Test kit reading page opens as expected
    page.get_by_role("link", name="Test Kit Reading").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Test Kit Quality Control Reading")
    page.get_by_role("link", name="Back").click()

    # View test kit result page opens as expected
    page.get_by_role("link", name="View Test Kit Result").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("View Test Kit Result")
    page.get_by_role("link", name="Back").click()

    # Create qc kit page opens as expected
    page.get_by_role("link", name="Create QC Kit").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Create QC Kit")

    # Return to main menu
    page.get_by_role("link", name="Main Menu").click()
    expect(page.locator("#ntshPageTitle")).to_contain_text("Main Menu")


def test_create_a_qc_kit(page: Page) -> None:
    # Navigate to create QC kit page
    page.get_by_role("link", name="Create QC Kit").click()

    # Select QC kit drop down options
    page.locator("#A_C_Reading_999_0_0").select_option("NEGATIVE")
    page.locator("#A_C_Reading_999_0_1").select_option("POSITIVE")
    page.locator("#A_C_Reading_999_1_0").select_option("POSITIVE")
    page.locator("#A_C_Reading_999_1_1").select_option("UNUSED")
    page.locator("#A_C_Reading_999_2_0").select_option("NEGATIVE")
    page.locator("#A_C_Reading_999_2_1").select_option("POSITIVE")

    # Click save
    page.get_by_role("button", name="Save Kit").click()

    # Verify kit has saved
    expect(page.locator("th")).to_contain_text("A quality control kit has been created with the following values:")
