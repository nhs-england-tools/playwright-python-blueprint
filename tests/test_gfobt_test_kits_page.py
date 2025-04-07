import pytest
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.gfobt_test_kits.gfobt_test_kits_page import GFOBTTestKits
from pages.gfobt_test_kits.gfobt_test_kit_logging_page import TestKitLogging
from pages.gfobt_test_kits.gfobt_test_kit_quality_control_reading_page import (
    TestKitQualityControlReading,
)
from pages.gfobt_test_kits.gfobt_view_test_kit_result import ViewTestKitResult
from pages.gfobt_test_kits.gfobt_create_qc_kit_page import (
    CreateQCKit,
    ReadingDropdownOptions,
)
from utils.user_tools import UserTools


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as a test user and navigates to the
    gfobt test kits page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager State Registered")

    # Go to gFOBT test kits page
    BasePage(page).go_to_gfobt_test_kits_page()


@pytest.mark.smoke
def test_gfobt_test_kit_page_navigation(page: Page) -> None:
    """
    Confirms all menu items are displayed on the gfobt test kits page, and that the relevant pages
    are loaded when the links are clicked
    """
    # Test kit logging page opens as expected
    GFOBTTestKits(page).go_to_test_kit_logging_page()
    TestKitLogging(page).verify_test_kit_logging_title()
    BasePage(page).click_back_button()

    # Test kit reading page opens as expected
    GFOBTTestKits(page).go_to_test_kit_result_page()
    TestKitQualityControlReading(page).verify_test_kit_logging_tile()
    BasePage(page).click_back_button()

    # View test kit result page opens as expected
    GFOBTTestKits(page).go_to_test_kit_result_page()
    ViewTestKitResult(page).verify_view_test_kit_result_title()
    BasePage(page).click_back_button()

    # Create qc kit page opens as expected
    GFOBTTestKits(page).go_to_create_qc_kit_page()
    CreateQCKit(page).verify_create_qc_kit_title()
    BasePage(page).click_back_button()

    # Return to main menu
    BasePage(page).click_main_menu_link()
    BasePage(page).main_menu_header_is_displayed()


def test_create_a_qc_kit(page: Page) -> None:
    """
    Confirms that a qc test kit can be created and that each of the dropdowns has an option set available for selection
    """
    # Navigate to create QC kit page
    GFOBTTestKits(page).go_to_create_qc_kit_page()

    # Select QC kit drop down options
    CreateQCKit(page).go_to_reading1dropdown(ReadingDropdownOptions.NEGATIVE.value)
    CreateQCKit(page).go_to_reading2dropdown(ReadingDropdownOptions.POSITIVE.value)
    CreateQCKit(page).go_to_reading3dropdown(ReadingDropdownOptions.POSITIVE.value)
    CreateQCKit(page).go_to_reading4dropdown(ReadingDropdownOptions.UNUSED.value)
    CreateQCKit(page).go_to_reading5dropdown(ReadingDropdownOptions.NEGATIVE.value)
    CreateQCKit(page).go_to_reading6dropdown(ReadingDropdownOptions.POSITIVE.value)

    # Click save
    CreateQCKit(page).go_to_save_kit()

    # Verify kit has saved
    CreateQCKit(page).verify_kit_has_saved()
