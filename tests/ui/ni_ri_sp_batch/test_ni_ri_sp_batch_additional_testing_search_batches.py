import logging
import pytest
from pages.main_menu import MainMenuPage
from playwright.sync_api import expect, Page, Playwright
from pages.ni_ri_sp_batch_page import NiRiSpBatchPage
from utils import test_helpers
from utils.CheckDigitGenerator import CheckDigitGenerator
from utils.user_tools import UserTools
from utils.screenshot_tool import ScreenshotTool


# TC-11
def test_risp_batch_by_yob_counted_selected_visible_for_all_batches_in_this_bso(page : Page, ni_ri_sp_batch_page : NiRiSpBatchPage) -> None:
    """
    verify RI/SP Batch by Year of Birth has been counted and date time of select is in the past and visible in the search batches
    """
    #Logged into BSO3 as user3(PMA) and select 'Create RI/SP Batch' from the 'batch management' dropdown
    UserTools().user_login(page, "Ni Only BSO User - BS3")
    MainMenuPage(page).select_menu_option("Failsafe Reports", "Search Batches")
    ni_ri_sp_batch_page.assert_page_header("Search Batches")
    ni_ri_sp_batch_page.select_all_batches_in_this_bso_radio_btn()
    ScreenshotTool(page).take_screenshot("additional_testing_TC_11")
    bso_batch_id = "PMA254189C"
    batch_title = "Search Batches Test 1"
    ni_ri_sp_batch_page.click_on_search_btn_in_search_batches(bso_batch_id, batch_title)
    ni_ri_sp_batch_page.assert_bso_batch_id(bso_batch_id, should_exist=True)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_11_1")

# TC-12
def test_risp_batch_by_yob_counted_selected_not_visible_for_all_batches_in_this_bso(page : Page, ni_ri_sp_batch_page : NiRiSpBatchPage) -> None:
    """
    verify RI/SP Batch by Year of Birth has been counted, date time of select is in the future and bso batch id is not visible in the search batches
    """
    #Logged into BSO3 as user3(PMA) and select 'Create RI/SP Batch' from the 'batch management' dropdown
    UserTools().user_login(page, "Ni Only BSO User - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    batch_title = test_helpers.generate_random_string(10)
    check_digit = CheckDigitGenerator().generate_check_digit()
    ni_ri_sp_batch_page.enter_bso_batch_id(check_digit)
    ni_ri_sp_batch_page.enter_batch_title(batch_title)
    ni_ri_sp_batch_page.enter_date_for_selection(5)
    ni_ri_sp_batch_page.click_count_button()
    ScreenshotTool(page).take_screenshot("additional_testing_TC_12")
    ni_ri_sp_batch_page.assert_page_header("Amend RI/SP Batch by Year of Birth")
    ni_ri_sp_batch_page.click_count_select_button()
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    ni_ri_sp_batch_page.assert_page_header("Batch List")
    ni_ri_sp_batch_page.search_by_bso_batch_id_and_batch_title(check_digit, batch_title)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_12_1")
    MainMenuPage(page).select_menu_option("Failsafe Reports ", "Search Batches")
    ni_ri_sp_batch_page.assert_page_header("Search Batches")
    ni_ri_sp_batch_page.select_all_batches_in_this_bso_radio_btn()
    ScreenshotTool(page).take_screenshot("additional_testing_TC_12_2")
    ni_ri_sp_batch_page.click_on_search_btn_in_search_batches(check_digit, batch_title)
    ni_ri_sp_batch_page.assert_bso_batch_id(check_digit, should_exist=False)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_12_3")

# TC-13
def test_risp_batch_by_yob_counted_selected_visible_for_gp_practice_in_any_bso(page : Page, ni_ri_sp_batch_page : NiRiSpBatchPage) -> None:
    """
    verify RI/SP Batch by Year of Birth has been counted and date time of select is in the past and visible in the search batches for GP practice in any BSO
    """
    #Logged into BSO3 as user3(PMA) and select 'Create RI/SP Batch' from the 'batch management' dropdown
    UserTools().user_login(page, "Ni Only BSO User - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    ni_ri_sp_batch_page.assert_page_header("Batch List")
    bso_batch_id = "PMA923851K"
    batch_title = "Search Batches by Gp Practice"
    ni_ri_sp_batch_page.search_by_bso_batch_id_and_batch_title(bso_batch_id, batch_title)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_13")
    MainMenuPage(page).select_menu_option("Failsafe Reports", "Search Batches")
    ni_ri_sp_batch_page.assert_page_header("Search Batches")
    ni_ri_sp_batch_page.select_gp_practice_in_any_bso_radio_btn("N00005")
    ni_ri_sp_batch_page.click_on_search_btn_in_search_batches(bso_batch_id, batch_title)
    ni_ri_sp_batch_page.assert_bso_batch_id(bso_batch_id, should_exist=True)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_13_1")

# TC-14
def test_risp_batch_by_yob_counted_selected_visible_for_gp_practice_group_in_this_bso(page : Page, ni_ri_sp_batch_page : NiRiSpBatchPage) -> None:
    """
    verify RI/SP Batch by Year of Birth has been counted and date time of select is in the past and visible in the search batches for GP practice group in this BSO
    """
    #Logged into BSO3 as user3(PMA) and select 'Create RI/SP Batch' from the 'batch management' dropdown
    UserTools().user_login(page, "Ni Only BSO User - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    ni_ri_sp_batch_page.assert_page_header("Batch List")
    bso_batch_id = "PMA796057K"
    batch_title = "Search Batch by Gp Group"
    ni_ri_sp_batch_page.search_by_bso_batch_id_and_batch_title(bso_batch_id, batch_title)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_14")
    MainMenuPage(page).select_menu_option("Failsafe Reports", "Search Batches")
    ni_ri_sp_batch_page.assert_page_header("Search Batches")
    ni_ri_sp_batch_page.select_gp_practice_group_in_this_bso_radio_btn("GP PRACTICE GROUP 1")
    ni_ri_sp_batch_page.click_on_search_btn_in_search_batches(bso_batch_id, batch_title)
    ni_ri_sp_batch_page.assert_bso_batch_id(bso_batch_id, should_exist=True)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_14_1")

# TC-15
def test_risp_batch_by_yob_counted_selected_visible_for_outcode_in_any_bso(page : Page, ni_ri_sp_batch_page : NiRiSpBatchPage) -> None:
    """
    verify RI/SP Batch by Year of Birth has been counted and date time of select is in the past and visible in the search batches for Outcode in any BSO
    """
    #Logged into BSO3 as user3(PMA) and select 'Create RI/SP Batch' from the 'batch management' dropdown
    UserTools().user_login(page, "Ni Only BSO User - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    ni_ri_sp_batch_page.assert_page_header("Batch List")
    bso_batch_id = "PMA969494Q"
    batch_title = "Search Batch By selected Outcode"
    ni_ri_sp_batch_page.search_by_bso_batch_id_and_batch_title(bso_batch_id, batch_title)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_15")
    MainMenuPage(page).select_menu_option("Failsafe Reports", "Search Batches")
    ni_ri_sp_batch_page.assert_page_header("Search Batches")
    ni_ri_sp_batch_page.select_outcode_in_any_bso_radio_btn("M14")
    ni_ri_sp_batch_page.click_on_search_btn_in_search_batches(bso_batch_id, batch_title)
    ni_ri_sp_batch_page.assert_bso_batch_id(bso_batch_id, should_exist=True)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_15_1")

# TC-16
def test_risp_batch_by_yob_counted_selected_visible_for_outcode_group_in_this_bso(page : Page, ni_ri_sp_batch_page : NiRiSpBatchPage) -> None:
    """
    verify RI/SP Batch by Year of Birth has been counted and date time of select is in the past and visible in the search batches for Outcode group in this BSO
    """
    #Logged into BSO3 as user3(PMA) and select 'Create RI/SP Batch' from the 'batch management' dropdown
    UserTools().user_login(page, "Ni Only BSO User - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    ni_ri_sp_batch_page.assert_page_header("Batch List")
    bso_batch_id = "PMA203887N"
    batch_title = "Search Batch By Outcode Group"
    ni_ri_sp_batch_page.search_by_bso_batch_id_and_batch_title(bso_batch_id, batch_title)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_16")
    MainMenuPage(page).select_menu_option("Failsafe Reports", "Search Batches")
    ni_ri_sp_batch_page.assert_page_header("Search Batches")
    ni_ri_sp_batch_page.select_outcode_group_in_this_bso_radio_btn("OUTCODE GROUP 2")
    ni_ri_sp_batch_page.click_on_search_btn_in_search_batches(bso_batch_id, batch_title)
    ni_ri_sp_batch_page.assert_bso_batch_id(bso_batch_id, should_exist=True)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_16_1")
