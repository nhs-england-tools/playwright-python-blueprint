import logging
import pytest
from pages.main_menu import MainMenuPage
from playwright.sync_api import expect, Page, Playwright
from pages.ni_ri_sp_batch_page import NiRiSpBatchPage
from utils import test_helpers
from utils.CheckDigitGenerator import CheckDigitGenerator
from utils.user_tools import UserTools
from utils.screenshot_tool import ScreenshotTool


# TC-17.1.1
def test_ntdd_counted_selected_visible_for_gp_practice_in_any_bso(page : Page, ni_ri_sp_batch_page : NiRiSpBatchPage) -> None:
    """
    verify ntdd has been counted and date time of select is in the past and visible in the search batches for GP practice in any BSO
    """
    #Logged into BSO3 as user3(PMA)
    UserTools().user_login(page, "Ni Only BSO User - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    ni_ri_sp_batch_page.assert_page_header("Batch List")
    bso_batch_id = "PMA806229T"
    batch_title = "Search Batches NTDD Selected Gp Practice"
    ni_ri_sp_batch_page.search_by_bso_batch_id_and_batch_title(bso_batch_id, batch_title)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_17-1-1_a")
    MainMenuPage(page).select_menu_option("Failsafe Reports", "Search Batches")
    ni_ri_sp_batch_page.assert_page_header("Search Batches")
    ni_ri_sp_batch_page.select_gp_practice_in_any_bso_radio_btn("N00007")
    ni_ri_sp_batch_page.click_on_search_btn_in_search_batches(bso_batch_id, batch_title)
    ni_ri_sp_batch_page.assert_bso_batch_id(bso_batch_id, should_exist=True)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_17-1-1_b")


# TC-17.1.2
def test_ntdd_counted_selected_visible_for_gp_practice_group_in_this_bso(page : Page, ni_ri_sp_batch_page : NiRiSpBatchPage) -> None:
    """
    verify ntdd has been counted and date time of select is in the past and visible in the search batches for GP practice group in this BSO
    """
    #Logged into BSO3 as user3(PMA)
    UserTools().user_login(page, "Ni Only BSO User - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    ni_ri_sp_batch_page.assert_page_header("Batch List")
    bso_batch_id = "PMA316521Q"
    batch_title = "SearchBatch NTDD GpPractice Groups"
    ni_ri_sp_batch_page.search_by_bso_batch_id_and_batch_title(bso_batch_id, batch_title)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_17-1-2_a")
    MainMenuPage(page).select_menu_option("Failsafe Reports", "Search Batches")
    ni_ri_sp_batch_page.assert_page_header("Search Batches")
    ni_ri_sp_batch_page.select_gp_practice_group_in_this_bso_radio_btn("GP PRACTICE GROUP 1")
    ni_ri_sp_batch_page.click_on_search_btn_in_search_batches(bso_batch_id, batch_title)
    ni_ri_sp_batch_page.assert_bso_batch_id(bso_batch_id, should_exist=True)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_17-1-2_b")


# TC-18.1.1
def test_ntdd_counted_selected_visible_for_outcode_in_any_bso(page : Page, ni_ri_sp_batch_page : NiRiSpBatchPage) -> None:
    """
    verify ntdd has been counted and date time of select is in the past and visible in the search batches for Outcode in any BSO
    """
    #Logged into BSO3 as user3(PMA)
    UserTools().user_login(page, "Ni Only BSO User - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    ni_ri_sp_batch_page.assert_page_header("Batch List")
    bso_batch_id = "PMA761960U"
    batch_title = "Search Batch Selected Outcode"
    ni_ri_sp_batch_page.search_by_bso_batch_id_and_batch_title(bso_batch_id, batch_title)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_18-1-1_a")
    MainMenuPage(page).select_menu_option("Failsafe Reports", "Search Batches")
    ni_ri_sp_batch_page.assert_page_header("Search Batches")
    ni_ri_sp_batch_page.select_outcode_in_any_bso_radio_btn("M12")
    ni_ri_sp_batch_page.click_on_search_btn_in_search_batches(bso_batch_id, batch_title)
    ni_ri_sp_batch_page.assert_bso_batch_id(bso_batch_id, should_exist=True)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_18-1-1_b")


# TC-18.1.2
def test_ntdd_counted_selected_visible_for_outcode_group_in_this_bso(page : Page, ni_ri_sp_batch_page : NiRiSpBatchPage) -> None:
    """
    verify ntdd has been counted and date time of select is in the past and visible in the search batches for Outcode group in this BSO
    """
    #Logged into BSO3 as user3(PMA)
    UserTools().user_login(page, "Ni Only BSO User - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    ni_ri_sp_batch_page.assert_page_header("Batch List")
    bso_batch_id = "PMA210997T"
    batch_title = "SearchBatch NTDD Outcode groups"
    ni_ri_sp_batch_page.search_by_bso_batch_id_and_batch_title(bso_batch_id, batch_title)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_18-1-2_a")
    MainMenuPage(page).select_menu_option("Failsafe Reports", "Search Batches")
    ni_ri_sp_batch_page.assert_page_header("Search Batches")
    ni_ri_sp_batch_page.select_outcode_group_in_this_bso_radio_btn("OUTCODE GROUP 2")
    ni_ri_sp_batch_page.click_on_search_btn_in_search_batches(bso_batch_id, batch_title)
    ni_ri_sp_batch_page.assert_bso_batch_id(bso_batch_id, should_exist=True)
    ScreenshotTool(page).take_screenshot("additional_testing_TC_18-1-2_b")
