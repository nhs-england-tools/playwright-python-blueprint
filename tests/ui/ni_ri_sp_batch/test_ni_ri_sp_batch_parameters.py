from itertools import count
import pytest
from pages.main_menu import MainMenuPage
from playwright.sync_api import expect, Page, Playwright
from pages.ni_ri_sp_batch_page import NiRiSpBatchPage
from utils import test_helpers
from utils.CheckDigitGenerator import CheckDigitGenerator
from utils.user_tools import UserTools
from utils.screenshot_tool import ScreenshotTool


# TC-1
def test_create_ri_sp_batch_using_selected_gp_practice_codes_and_all_outcodes(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """Test to create ri/sp batch using "specify by gp practice" and "all outcodes" """
    # Logged into BSO3 as user3(PMA) and select 'Create RI/SP Batch' from the 'batch management' dropdown
    UserTools().user_login(page, "Ni Only BSO User - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    batch_title = test_helpers.generate_random_string(10)
    check_digit = CheckDigitGenerator().generate_check_digit()
    ni_ri_sp_batch_page.enter_bso_batch_id(check_digit)
    ni_ri_sp_batch_page.enter_batch_title(batch_title)
    ni_ri_sp_batch_page.enter_date_for_selection(5)
    ni_ri_sp_batch_page.enter_include_year_of_birth_from("1955")
    ni_ri_sp_batch_page.enter_include_year_of_birth_to("1975")
    ni_ri_sp_batch_page.select_include_specified_practices()
    ni_ri_sp_batch_page.enter_excluded_gp_practices_filter("N00005")
    ni_ri_sp_batch_page.select_excluded_gp_practices_from_list("N00005")
    ni_ri_sp_batch_page.click_gp_practices_select_move()
    ni_ri_sp_batch_page.click_count_button()
    ScreenshotTool(page).take_screenshot("batch_parameters_TC_1")
    ni_ri_sp_batch_page.assert_page_header("Amend RI/SP Batch by Year of Birth")
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    ni_ri_sp_batch_page.assert_page_header("Batch List")
    ni_ri_sp_batch_page.assert_entered_bso_batch_id_and_filterd_row_value(check_digit)
    ScreenshotTool(page).take_screenshot("batch_parameters_TC_1.1")


# TC-2
def test_create_ri_sp_batch_using_selected_gp_practice_groups_and_all_outcodes(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """Test to create ri/sp batch using "selected gp practice groups" and "all outcodes" """
    # Logged into BSO3 as user3(PMA) and select 'Create RI/SP Batch' from the 'batch management' dropdown
    UserTools().user_login(page, "Ni Only BSO User - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    batch_title = test_helpers.generate_random_string(10)
    check_digit = CheckDigitGenerator().generate_check_digit()
    ni_ri_sp_batch_page.enter_bso_batch_id(check_digit)
    ni_ri_sp_batch_page.enter_batch_title(batch_title)
    ni_ri_sp_batch_page.enter_date_for_selection(5)
    ni_ri_sp_batch_page.select_specify_by_gp_practice_group()
    ni_ri_sp_batch_page.select_excluded_gp_practice_groups("GP PRACTICE GROUP 1")
    ni_ri_sp_batch_page.click_gp_practice_groups_select_move()
    ni_ri_sp_batch_page.click_count_button()
    ScreenshotTool(page).take_screenshot("batch_parameters_TC_2")
    ni_ri_sp_batch_page.assert_page_header("Amend RI/SP Batch by Year of Birth")
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    ni_ri_sp_batch_page.assert_page_header("Batch List")
    ni_ri_sp_batch_page.assert_entered_bso_batch_id_and_filterd_row_value(check_digit)
    ScreenshotTool(page).take_screenshot("batch_parameters_TC_2.1")


# TC-3
def test_create_ri_sp_batch_using_all_gp_practices_and_selected_outcodes(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """Test to create ri/sp batch using "include all gp practices" and "specify by outcode" """
    # Logged into BSO3 as user3(PMA) and select 'Create RI/SP Batch' from the 'batch management' dropdown
    UserTools().user_login(page, "Ni Only BSO User - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    batch_title = test_helpers.generate_random_string(10)
    check_digit = CheckDigitGenerator().generate_check_digit()
    ni_ri_sp_batch_page.enter_bso_batch_id(check_digit)
    ni_ri_sp_batch_page.enter_batch_title(batch_title)
    ni_ri_sp_batch_page.enter_date_for_selection(5)
    ni_ri_sp_batch_page.enter_include_year_of_birth_from("1955")
    ni_ri_sp_batch_page.enter_include_year_of_birth_to("1975")
    ni_ri_sp_batch_page.select_include_specified_outcodes()
    ni_ri_sp_batch_page.enter_excluded_outcodes_filter("M12")
    ni_ri_sp_batch_page.select_excluded_outcodes_from_list("M12")
    ni_ri_sp_batch_page.click_outcodes_select_move()
    ni_ri_sp_batch_page.click_count_button()
    ScreenshotTool(page).take_screenshot("batch_parameters_TC_3")
    ni_ri_sp_batch_page.assert_page_header("Amend RI/SP Batch by Year of Birth")
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    ni_ri_sp_batch_page.assert_page_header("Batch List")
    ni_ri_sp_batch_page.assert_entered_bso_batch_id_and_filterd_row_value(check_digit)
    ScreenshotTool(page).take_screenshot("batch_parameters_TC_3.1")


# TC-4
def test_create_ri_sp_batch_using_include_all_gp_practices_and_selected_outcode_groups(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """Test to create ri/sp batch using "include all gp practices" and "selected outcode groups" """
    # Logged into BSO3 as user3(PMA) and select 'Create RI/SP Batch' from the 'batch management' dropdown
    UserTools().user_login(page, "Ni Only BSO User - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    batch_title = test_helpers.generate_random_string(10)
    check_digit = CheckDigitGenerator().generate_check_digit()
    ni_ri_sp_batch_page.enter_bso_batch_id(check_digit)
    ni_ri_sp_batch_page.enter_batch_title(batch_title)
    ni_ri_sp_batch_page.enter_date_for_selection(5)
    ni_ri_sp_batch_page.select_specify_by_outcode_group()
    ni_ri_sp_batch_page.select_excluded_outcode_groups("OUTCODE GROUP 1")
    ni_ri_sp_batch_page.click_outcode_groups_select_move()
    ni_ri_sp_batch_page.click_count_button()
    ScreenshotTool(page).take_screenshot("batch_parameters_TC_4")
    ni_ri_sp_batch_page.assert_page_header("Amend RI/SP Batch by Year of Birth")
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    ni_ri_sp_batch_page.assert_page_header("Batch List")
    ni_ri_sp_batch_page.assert_entered_bso_batch_id_and_filterd_row_value(check_digit)
    ScreenshotTool(page).take_screenshot("batch_parameters_TC_4.1")


# TC-5
def test_create_ri_sp_batch_using_selected_out_codes_and_selected_gp_practices(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """Test to create ri/sp batch using "specify by gp practices" and "specify by outcode" """
    # Logged into BSO3 as user3(PMA) and select 'Create RI/SP Batch' from the 'batch management' dropdown
    UserTools().user_login(page, "Ni Only BSO User - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    batch_title = test_helpers.generate_random_string(10)
    check_digit = CheckDigitGenerator().generate_check_digit()
    ni_ri_sp_batch_page.enter_bso_batch_id(check_digit)
    ni_ri_sp_batch_page.enter_batch_title(batch_title)
    ni_ri_sp_batch_page.enter_date_for_selection(5)
    ni_ri_sp_batch_page.enter_include_year_of_birth_from("1955")
    ni_ri_sp_batch_page.enter_include_year_of_birth_to("1975")
    ni_ri_sp_batch_page.select_include_specified_practices()
    ni_ri_sp_batch_page.enter_excluded_gp_practices_filter("N00007")
    ni_ri_sp_batch_page.select_excluded_gp_practices_from_list("N00007")
    ni_ri_sp_batch_page.click_gp_practices_select_move()
    ni_ri_sp_batch_page.select_include_specified_outcodes()
    ni_ri_sp_batch_page.enter_excluded_outcodes_filter("M11")
    ni_ri_sp_batch_page.select_excluded_outcodes_from_list("M11")
    ni_ri_sp_batch_page.click_outcodes_select_move()
    ni_ri_sp_batch_page.click_count_button()
    ScreenshotTool(page).take_screenshot("batch_parameters_TC_5")
    ni_ri_sp_batch_page.assert_page_header("Amend RI/SP Batch by Year of Birth")
    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    ni_ri_sp_batch_page.assert_page_header("Batch List")
    ni_ri_sp_batch_page.assert_entered_bso_batch_id_and_filterd_row_value(check_digit)
    ScreenshotTool(page).take_screenshot("batch_parameters_TC_5.1")
