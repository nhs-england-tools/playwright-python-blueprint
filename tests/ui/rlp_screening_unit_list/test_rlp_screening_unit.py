import random
import secrets
import re
import string
import pytest
from playwright.sync_api import expect, Page, Playwright
from datetime import datetime
from pages.rlp_unit_list_page import ScreeningUnitListPage
from utils import test_helpers
from utils.screenshot_tool import ScreenshotTool
from utils.user_tools import UserTools
from pages.main_menu import MainMenuPage


## Scenario_01 ## Test_01, Test_3.1.4 ##
@pytest.mark.rlpunit
def test_all_data_loaded(
    page: Page, rlp_screening_unit_list_page: ScreeningUnitListPage, db_util
) -> None:
    """test to verify the correct number of 'Screening units' are displayed on the DB and UI"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    expect(page.get_by_text("Screening unit list", exact=True)).to_be_visible()
    db_row_count = rlp_screening_unit_list_page.screening_unit_list_count_in_db(db_util)
    ui_row_count = rlp_screening_unit_list_page.extract_paging_unit_list_count()
    assert db_row_count == int(ui_row_count)


## Scenario_02 ## Test 4.1.4, 7.1.1, 7.1.2, 8.1.1, 8.1.2, 9.1.1, 10.1.2, 10.1.3 ##
@pytest.mark.rlpunit
@pytest.mark.parametrize("unit_type", ["MOBILE", "STATIC"])
@pytest.mark.parametrize("unit_status", ["ACTIVE", "INACTIVE"])
def test_screening_unit_creation(
    page: Page,
    rlp_screening_unit_list_page: ScreeningUnitListPage,
    db_util,
    unit_type,
    unit_status,
) -> None:
    """User adds a Screening unit + assert the new entry is present in the UI table and added to the DB
    and the test will use unit_type and unit_status in all 4 variations
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")

    count_before = rlp_screening_unit_list_page.screening_unit_list_count_in_db(db_util)

    unit_name = f"Unit_name-{datetime.now()}"
    notes = test_helpers.generate_random_string(250)
    unit_data = {
        "unit_name": unit_name,
        "notes": notes,
        **{
            day: str(secrets.randbelow(999))
            for day in ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
        },
    }
    rlp_screening_unit_list_page.add_screening_unit(unit_data, unit_type, unit_status)
    rlp_screening_unit_list_page.click_add_screening_unit_btn_on_pop_up_window()
    page.wait_for_timeout(3000)
    rlp_screening_unit_list_page.verify_screening_unit_by_name(unit_name)
    ScreenshotTool(page).take_screenshot("rlp_unit_tc_4_7_8_9_10")
    count_after = rlp_screening_unit_list_page.screening_unit_list_count_in_db(db_util)
    assert count_after == count_before + 1


## Scenario 2 ### Test 4.2.3 - Negative ##
@pytest.mark.rlpunit
def test_screening_unit_cancellation(
    page: Page, rlp_screening_unit_list_page: ScreeningUnitListPage, db_util
) -> None:
    """Previously saved units = x, cancels adding 1 unit, returns back to list view of x"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    count_before = rlp_screening_unit_list_page.screening_unit_list_count_in_db(db_util)

    unit_name = f"Unit_cancel-{datetime.now()}"
    rlp_screening_unit_list_page.click_add_screening_unit_btn()
    rlp_screening_unit_list_page.enter_screening_unit_name_txt_box(unit_name)
    rlp_screening_unit_list_page.select_status_mobile_radio_btn()
    rlp_screening_unit_list_page.click_cancel_btn_on_pop_up_window()
    page.wait_for_timeout(3000)
    rlp_screening_unit_list_page.verify_unit_has_no_matching_records_available_in_the_table(
        unit_name
    )
    rlp_screening_unit_list_page.expect_no_matching_records_found_msg()
    ScreenshotTool(page).take_screenshot("rlp_unit_tc_4_negative")
    count_after = rlp_screening_unit_list_page.screening_unit_list_count_in_db(db_util)
    assert count_after == count_before


## Scenario 2 ## Test 5, 7.1.3, 8.1.3, 9.1.2 ##
@pytest.mark.rlpunit1
def test_defaults_are_set_correctly(
    page: Page, rlp_screening_unit_list_page: ScreeningUnitListPage
) -> None:
    """All defaults are set & displayed correctly"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    rlp_screening_unit_list_page.click_add_screening_unit_btn()
    expect(page.locator("input#unitNameText")).to_be_empty()
    expect(
        page.locator(
            "//input[@name='statusText' and @type='radio' and @value='ACTIVE']"
        )
    ).to_be_checked()
    expect(
        page.locator(
            "//input[@name='statusText' and @type='radio' and @value='INACTIVE']"
        )
    ).not_to_be_checked()
    expect(page.get_by_role("radio", name="Mobile")).not_to_be_checked()
    expect(page.get_by_role("radio", name="Static")).not_to_be_checked()
    for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        expect(page.get_by_role("textbox", name=day)).to_have_value("0")
    expect(page.locator("#notesText")).to_be_empty()
    ScreenshotTool(page).take_screenshot("rlp_unit_tc_5_7_8_9")


## Scenario 2 ## Test 6.1.1, 6.1.2, 6.1.3, 6.1.4 ##
@pytest.mark.rlpunit
@pytest.mark.parametrize("input_length", [3, 50])
def test_validate_add_new_unit_list_name_field(
    page: Page, rlp_screening_unit_list_page: ScreeningUnitListPage, input_length
) -> None:
    """Enters data into Screening Unit Name field on the 'Add a new unit' screen using input name lengths are 3 and 50"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")

    unit_name = test_helpers.generate_random_string(
        input_length
    )  # this method will generate string between 3 & 100 which will be unique each time
    rlp_screening_unit_list_page.verify_unit_has_no_matching_records_available_in_the_table(
        unit_name
    )

    rlp_screening_unit_list_page.create_unit(unit_name)
    rlp_screening_unit_list_page.verify_screening_unit_by_name(unit_name)
    ScreenshotTool(page).take_screenshot("rlp_unit_tc_6")


## Scenario 1&2 ## Test 7.2.1, 9.2.1, 9.2.2 ##
@pytest.mark.rlpunit
def test_negative_non_integer_values_and_empty_unit_type(
    page: Page, rlp_screening_unit_list_page: ScreeningUnitListPage
) -> None:
    """Null unit_name, unit_type and days are null & non integer"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    unit_data = {
        "unit_name": "",
        "thu": "",
        **{
            day: "".join(secrets.choice(string.ascii_letters) for _ in range(2))
            for day in ["sun", "mon", "tue", "wed", "fri", "sat"]
        },
    }
    rlp_screening_unit_list_page.add_screening_unit(
        unit_data, unit_type="", unit_status=""
    )
    rlp_screening_unit_list_page.click_add_screening_unit_btn_on_pop_up_window()
    expect(page.get_by_text("Name must be populated")).to_be_visible()
    expect(page.get_by_text("Unit Type must be populated")).to_be_visible()
    for day in ["Sun", "Mon", "Tues", "Wednes", "Thurs", "Fri", "Satur"]:
        expect(
            page.get_by_text(f"{day}day Appointments must be between 0 and 999")
        ).to_be_visible()
    ScreenshotTool(page).take_screenshot("rlp_unit_tc_7_9")


## Scenario 3 ## negative-Test 6.2.1, 6.2.2, 6.2.3, 6.2.4, 6.2.5, 14.2.1, 15.2.1 ##
@pytest.mark.rlpunit
@pytest.mark.parametrize("invalid_name", ["$#%&", "CA", "Batman", "    "])
def test_negative_non_integer_values_and_empty_unit_type(
    page: Page, rlp_screening_unit_list_page: ScreeningUnitListPage, invalid_name
) -> None:
    """Negative test with invalid data for unit_name filed"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")

    unit_name = invalid_name
    rlp_screening_unit_list_page.create_unit(unit_name)
    # Asserting expected error messages for invalid names
    invalid_char_pattern = re.compile("[#$%<>&]")
    if invalid_char_pattern.findall(unit_name):
        expect(page.get_by_text("Name contains invalid characters")).to_be_visible()
    elif len(unit_name) < 3:
        expect(page.get_by_text("The Name you entered is too short")).to_be_visible()
    elif unit_name == "Batman":
        expect(
            page.get_by_text("Name is already in use by another unit")
        ).to_be_visible()
    elif unit_name == "    ":
        expect(page.get_by_text("Unit Type must be populated")).to_be_visible
    ScreenshotTool(page).take_screenshot("rlp_unit_tc_6_14_15")


## Scenario 1 ##Test 10.2.1 ##
@pytest.mark.rlpunit
def test_notes_shows_err_msg_for_invalid_chars(
    page: Page, rlp_screening_unit_list_page: ScreeningUnitListPage
) -> None:
    """Negative test with invalid data for notes filed"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")

    unitname = f"ZZZZZZ-notes-{datetime.now()}"
    unit_data = {"unit_name": unitname, "notes": "#$%&"}
    rlp_screening_unit_list_page.add_screening_unit(unit_data)
    rlp_screening_unit_list_page.click_add_screening_unit_btn_on_pop_up_window()
    expect(
        page.locator(
            "//p[@id='error_notesText' and text()='Notes contains invalid characters']"
        )
    ).to_be_visible()
    ScreenshotTool(page).take_screenshot("rlp_unit_tc_10")


## Scenario 2 ## Test 14.1.1, 14.1.2, 14.1.3, 14.1.4, 14.1.5, 10.1.1, 15.1.1, 15.1.2, 15.1.3, 15.1.4 ##
@pytest.mark.rlpunit
def test_add_screeing_unit_with_defaults(
    page: Page, rlp_screening_unit_list_page: ScreeningUnitListPage
) -> None:
    """Creating screeing unit with defaults and mandatory fields(unit_name, unit_type and days)"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    unit_name = f"Unit_name-{datetime.now()}"
    rlp_screening_unit_list_page.create_unit(unit_name)

    rlp_screening_unit_list_page.verify_screening_unit_by_name(unit_name)
    assert page.wait_for_selector("//tr//td[5]").text_content() == "Mobile"
    assert page.wait_for_selector("//tr//td[6]").text_content() == "Active"
    for col in range(7, 14):
        assert page.wait_for_selector(f"//tr//td[{col}]").text_content() == "0"
    ScreenshotTool(page).take_screenshot("rlp_unit_tc_14_15")


## Test_11 ##
@pytest.mark.rlpunit
def test_another_user_from_another_bso_creates_the_unit(
    page: Page, rlp_screening_unit_list_page: ScreeningUnitListPage, context
) -> None:
    """Added screening unit is not available for another user from different BSO, and creates the unit with the same data"""
    # Logged into BSS_SO1 user1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    unit_name = f"user1-{datetime.now()}"
    rlp_screening_unit_list_page.create_unit(unit_name)
    context.clear_cookies()
    # Logged on as BSS_02 user2
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    rlp_screening_unit_list_page.filter_unit_by_name(unit_name)
    expect(page.get_by_text("No matching records found")).to_be_visible()

    # user2 is creating the unit in BSO2 with the same data used by user1 in BSO1
    rlp_screening_unit_list_page.create_unit(unit_name)
    rlp_screening_unit_list_page.verify_screening_unit_by_name(unit_name)
    ScreenshotTool(page).take_screenshot("rlp_unit_tc_11")


## Test_12 ##
@pytest.mark.rlpunit
def test_user2_from_same_bso_can_access_the_user1_data(
    page: Page, rlp_screening_unit_list_page: ScreeningUnitListPage, context
) -> None:
    """Added screening unit is available for another user from same BSO, and tried to create the unit with the same data, it'll throw an error"""
    # Logged into BSS_SO1 user1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    unit_name = f"user1-{datetime.now()}"
    rlp_screening_unit_list_page.create_unit(unit_name)
    context.clear_cookies()
    # Logged on as BSS_SO1 user2
    UserTools().user_login(page, "BSO User2 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    rlp_screening_unit_list_page.verify_screening_unit_by_name(unit_name)
    # user2 tries to create the unit with existing unit name, it'll display an error msg
    rlp_screening_unit_list_page.create_unit(unit_name)
    ScreenshotTool(page).take_screenshot("rlp_unit_tc_12")
    expect(page.get_by_text("Name is already in use by another unit")).to_be_visible()
