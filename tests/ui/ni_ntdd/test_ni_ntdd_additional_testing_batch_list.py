from itertools import count
import playwright
import pytest
from pages.main_menu import MainMenuPage
from playwright.sync_api import expect, Page, Playwright
from datetime import datetime
from pages.ni_ri_sp_batch_page import NiRiSpBatchPage
from utils.CheckDigitGenerator import CheckDigitGenerator
from utils.user_tools import UserTools
from utils.screenshot_tool import ScreenshotTool


@pytest.fixture()
def login_and_create_ntdd_batch(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> dict:
    """Fixture to log in and create a NTDD batch."""
    # Logged into BSO3 as user3(PMA) and select 'Create NTDD Batch' from the 'batch management' dropdown
    UserTools().user_login(page, "Ni Only BSO User - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create NTDD Batch")
    ni_ri_sp_batch_page.assert_page_header("Create NTDD Batch")
    batch_title = f"ntdd-{datetime.now()}"
    check_digit = CheckDigitGenerator().generate_check_digit()
    ni_ri_sp_batch_page.enter_bso_batch_id(check_digit)
    ni_ri_sp_batch_page.enter_batch_title(batch_title)
    ni_ri_sp_batch_page.select_ntd_end_date(5)
    ni_ri_sp_batch_page.select_range_by_age()
    ni_ri_sp_batch_page.enter_ntdd_start_age_year("50")
    ni_ri_sp_batch_page.enter_ntdd_start_age_month("1")
    ni_ri_sp_batch_page.enter_ntdd_end_age_year("70")
    ni_ri_sp_batch_page.enter_ntdd_end_age_month("11")
    ni_ri_sp_batch_page.check_include_younger_women()
    ni_ri_sp_batch_page.click_count_button()
    return {"batch_title": batch_title, "check_digit": check_digit}

# TC-6
def test_count_display_for_ntdd_with_blank_selected_date_selected_and_rejected_fields(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage, login_and_create_ntdd_batch: dict
) -> None:
    """verify NTDD Batch by Year of Birth has been counted and counted is not selected assert Select Date, Selected, and Rejected fields are blank"""
    # Logged into BSO3 as user3(PMA) and select 'Create NTDD Batch' from the 'batch management' dropdown
    ScreenshotTool(page).take_screenshot("additional_testing_TC_6")
    ni_ri_sp_batch_page.assert_page_header("Amend NTDD Batch")
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    ni_ri_sp_batch_page.assert_page_header("Batch List")
    ni_ri_sp_batch_page.assert_entered_bso_batch_id_and_filtered_row_value(
        login_and_create_ntdd_batch["check_digit"]
    )
    ni_ri_sp_batch_page.assert_select_date_cell_value("")
    ni_ri_sp_batch_page.assert_selected_cell_value("")
    ni_ri_sp_batch_page.assert_rejected_cell_value("")
    ScreenshotTool(page).take_screenshot("additional_testing_TC_6_1")


# TC-7, TC-8
def test_count_display_for_ntdd_with_selected_date_selected_and_rejected_fields(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage, login_and_create_ntdd_batch: dict
) -> None:
    """verify NTDD Batch by Year of Birth has been counted and counted is selected assert Select Date, Selected, and Rejected fields should not be blank"""
    # Logged into BSO3 as user3(PMA) and select 'Create NTDD Batch' from the 'batch management' dropdown
    ScreenshotTool(page).take_screenshot("additional_testing_TC_7")
    ni_ri_sp_batch_page.assert_page_header("Amend NTDD Batch")
    ni_ri_sp_batch_page.click_count_select_button()
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    ni_ri_sp_batch_page.assert_page_header("Batch List")
    ni_ri_sp_batch_page.select_ntdd_from_drop_down()
    ni_ri_sp_batch_page.select_no_from_failsafe_flag_drop_down()
    ScreenshotTool(page).take_screenshot("additional_testing_TC_7_1")
    ni_ri_sp_batch_page.assert_entered_bso_batch_id_and_filtered_row_value(
        login_and_create_ntdd_batch["check_digit"]
    )
    ScreenshotTool(page).take_screenshot("additional_testing_TC_7_2")
    ni_ri_sp_batch_page.assert_select_date_cell_value_is_not_null("")
    ni_ri_sp_batch_page.assert_selected_cell_value_is_not_null("")
    ni_ri_sp_batch_page.assert_rejected_cell_value_is_not_null("")


# TC-9
def test_count_display_for_ntdd_batch_with_selected_date_selected_and_rejected_fields_search_by_bso_batch_id_and_batch_title(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage, login_and_create_ntdd_batch: dict
) -> None:
    """verify NTDD Batch by Year of Birth has been counted and counted is selected assert Select Date, Selected, and Rejected fields has a value and
    search by bso batch id and batch title
    """
    # Logged into BSO3 as user3(PMA) and select 'Create NTDD Batch' from the 'batch management' dropdown
    ScreenshotTool(page).take_screenshot("additional_testing_TC_9")
    ni_ri_sp_batch_page.assert_page_header("Amend NTDD Batch")
    ni_ri_sp_batch_page.click_count_select_button()
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    ni_ri_sp_batch_page.assert_page_header("Batch List")
    ni_ri_sp_batch_page.search_by_bso_batch_id_and_batch_title(
        login_and_create_ntdd_batch["check_digit"],
        login_and_create_ntdd_batch["batch_title"],
    )
    ScreenshotTool(page).take_screenshot("additional_testing_TC_9_1")
