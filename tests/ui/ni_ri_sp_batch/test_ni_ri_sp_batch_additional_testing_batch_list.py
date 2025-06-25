from itertools import count
import playwright
import pytest
from pages.main_menu import MainMenuPage
from playwright.sync_api import expect, Page, Playwright
from pages.ni_ri_sp_batch_page import NiRiSpBatchPage
from utils import test_helpers
from utils.CheckDigitGenerator import CheckDigitGenerator
from utils.user_tools import UserTools
from utils.screenshot_tool import ScreenshotTool


# TC-1
@pytest.mark.tc1
@pytest.mark.ni3
def test_count_display_for_ri_sp_batch_with_blank_selected_date_selected_and_rejected_fields(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """verify RI/SP Batch by Year of Birth has been counted and counted is not selected assert Select Date, Selected, and Rejected fields are blank"""
    # Logged into BSO3 as user3(PMA) and select 'Create RI/SP Batch' from the 'batch management' dropdown
    UserTools().user_login(page, "Ni Only BSO User3 - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    batch_title = test_helpers.generate_random_string(10)
    check_digit = CheckDigitGenerator().generate_check_digit()
    ni_ri_sp_batch_page.enter_bso_batch_id(check_digit)
    ni_ri_sp_batch_page.enter_batch_title(batch_title)
    ni_ri_sp_batch_page.enter_date_for_selection(5)
    ni_ri_sp_batch_page.click_count_button()
    ScreenshotTool(page).take_screenshot("additional_testing_TC_1")
    ni_ri_sp_batch_page.assert_page_header("Amend RI/SP Batch by Year of Birth")
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    ni_ri_sp_batch_page.assert_page_header("Batch List")
    ni_ri_sp_batch_page.assert_entered_bso_batch_id_and_filtered_row_value(check_digit)
    ni_ri_sp_batch_page.assert_select_date_cell_value("")
    ni_ri_sp_batch_page.assert_selected_cell_value("")
    ni_ri_sp_batch_page.assert_rejected_cell_value("")
    ScreenshotTool(page).take_screenshot("additional_testing_TC_1_1")


# TC-2, TC-3
@pytest.mark.tc2
@pytest.mark.ni3
def test_count_display_for_ri_sp_batch_with_selected_date_selected_and_rejected_fields(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """verify RI/SP Batch by Year of Birth has been counted and counted is selected assert Select Date, Selected, and Rejected fields has a value"""
    # Logged into BSO3 as user3(PMA) and select 'Create RI/SP Batch' from the 'batch management' dropdown and 'No' from Failsafe Flag drop down
    UserTools().user_login(page, "Ni Only BSO User3 - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    batch_title = test_helpers.generate_random_string(10)
    check_digit = CheckDigitGenerator().generate_check_digit()
    ni_ri_sp_batch_page.enter_bso_batch_id(check_digit)
    ni_ri_sp_batch_page.enter_batch_title(batch_title)
    ni_ri_sp_batch_page.enter_date_for_selection(5)
    ni_ri_sp_batch_page.click_count_button()
    ScreenshotTool(page).take_screenshot("additional_testing_TC_2")
    ni_ri_sp_batch_page.assert_page_header("Amend RI/SP Batch by Year of Birth")
    ni_ri_sp_batch_page.click_count_select_button()
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    ni_ri_sp_batch_page.assert_page_header("Batch List")
    ni_ri_sp_batch_page.select_ri_sp_yob_from_drop_down()
    ni_ri_sp_batch_page.select_no_from_failsafe_flag_drop_down()
    ScreenshotTool(page).take_screenshot("additional_testing_TC_2_1")
    ni_ri_sp_batch_page.assert_entered_bso_batch_id_and_filtered_row_value(check_digit)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_2_2")
    ni_ri_sp_batch_page.assert_select_date_cell_value_is_not_null("")
    ni_ri_sp_batch_page.assert_selected_cell_value_is_not_null("")
    ni_ri_sp_batch_page.assert_rejected_cell_value_is_not_null("")


# TC-4
@pytest.mark.tc4
@pytest.mark.ni3
def test_count_display_for_ri_sp_batch_with_selected_date_selected_and_rejected_fields_search_by_bso_batch_id_and_batch_title(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """verify RI/SP Batch by Year of Birth has been counted and counted is selected assert Select Date, Selected, and Rejected fields has a value and
    search by bso batch id and batch title
    """
    # Logged into BSO3 as user3(PMA) and select 'Create RI/SP Batch' from the 'batch management' dropdown
    UserTools().user_login(page, "Ni Only BSO User3 - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    batch_title = test_helpers.generate_random_string(10)
    check_digit = CheckDigitGenerator().generate_check_digit()
    ni_ri_sp_batch_page.enter_bso_batch_id(check_digit)
    ni_ri_sp_batch_page.enter_batch_title(batch_title)
    ni_ri_sp_batch_page.enter_date_for_selection(5)
    ni_ri_sp_batch_page.click_count_button()
    ScreenshotTool(page).take_screenshot("additional_testing_TC_4")
    ni_ri_sp_batch_page.assert_page_header("Amend RI/SP Batch by Year of Birth")
    ni_ri_sp_batch_page.click_count_select_button()
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    ni_ri_sp_batch_page.assert_page_header("Batch List")
    ni_ri_sp_batch_page.search_by_bso_batch_id_and_batch_title(check_digit, batch_title)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_4_1")
