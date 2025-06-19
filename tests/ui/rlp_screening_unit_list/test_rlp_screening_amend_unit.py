import random
import secrets
import re
import string
import pytest
from playwright.sync_api import expect, Page, Playwright
from datetime import datetime
from pages.rlp_unit_list_page import ScreeningUnitListPage
from utils.test_helpers import generate_random_string
from utils import test_helpers
from utils.screenshot_tool import ScreenshotTool
from utils.user_tools import UserTools
from pages.main_menu import MainMenuPage


## Scenario 4 - 16.1.3, 18.1.1, 18.1.4, 21.1.2 ##
@pytest.mark.rlpunit
def test_amend_screeing_unit_name_verify_the_paging_count(
    page: Page, rlp_screening_unit_list_page: ScreeningUnitListPage, db_util
) -> None:
    """
    Amend screening unit name and assert the unit list count on the UI and DB
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    rlp_screening_unit_list_page.select_status_dropdown("All")
    page.wait_for_timeout(3000)
    db_row_count = rlp_screening_unit_list_page.screening_unit_list_count_in_db(db_util)
    ui_row_count = rlp_screening_unit_list_page.extract_paging_unit_list_count()
    assert db_row_count == int(ui_row_count)
    unit_name = f"unit_name-{datetime.now()}"
    rlp_screening_unit_list_page.create_unit(unit_name)
    ScreenshotTool(page).take_screenshot("rlp_unit_amend_tc_16_18_21")
    rlp_screening_unit_list_page.filter_unit_by_name(unit_name)
    rlp_screening_unit_list_page.dbl_click_on_filtered_unit_name()
    amend_unit_name = f"amend_name-{datetime.now()}"
    rlp_screening_unit_list_page.enter_amend_screening_unit_name(amend_unit_name)
    rlp_screening_unit_list_page.click_amend_screening_unit_btn_on_pop_up_window()
    page.wait_for_timeout(3000)
    ScreenshotTool(page).take_screenshot("rlp_unit_amend_tc_16_18_21.1")
    amend_db_row_count = rlp_screening_unit_list_page.screening_unit_list_count_in_db(
        db_util
    )
    amend_ui_row_count = rlp_screening_unit_list_page.extract_paging_unit_list_count()
    assert amend_db_row_count == int(amend_ui_row_count)


## Scenario 4 - 18.1.2, 18.1.3, 19.1.1, 20.1.2 ##
@pytest.mark.rlpunit
@pytest.mark.parametrize("input_length", [3, 50])
def test_amend_screeing_unit_name_using_min_max_char_length(
    page: Page, rlp_screening_unit_list_page: ScreeningUnitListPage, input_length
) -> None:
    """Amend screening unit name, unit_status and unt_type and assert the values in the table"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    rlp_screening_unit_list_page.select_status_dropdown("All")
    page.wait_for_timeout(3000)
    unit_name = f"unit_name-{datetime.now()}"
    rlp_screening_unit_list_page.create_unit(unit_name)
    ScreenshotTool(page).take_screenshot("rlp_unit_amend_tc_18_19_20")
    rlp_screening_unit_list_page.filter_unit_by_name(unit_name)
    rlp_screening_unit_list_page.dbl_click_on_filtered_unit_name()
    amend_unit_name = generate_random_string(input_length)
    # Amended the unit name, status and type
    rlp_screening_unit_list_page.enter_amend_screening_unit_name(amend_unit_name)
    rlp_screening_unit_list_page.select_amend_unit_status_radio_btn("INACTIVE")
    rlp_screening_unit_list_page.select_amend_unit_type_radio_btn("STATIC")
    rlp_screening_unit_list_page.click_amend_screening_unit_btn_on_pop_up_window()
    page.wait_for_timeout(3000)
    rlp_screening_unit_list_page.filter_unit_by_name(amend_unit_name)
    ScreenshotTool(page).take_screenshot("rlp_unit_amend_tc_18_19_20.1")
    assert page.wait_for_selector("//tr//td[4]").text_content() == amend_unit_name
    assert page.wait_for_selector("//tr//td[5]").text_content() == "Static"
    assert page.wait_for_selector("//tr//td[6]").text_content() == "Inactive"
    # verify_screening_unit_by_name() - will assert the actual amend_unit_name and created value in the table
    rlp_screening_unit_list_page.verify_screening_unit_by_name(amend_unit_name)


## Scenario 4 - 16.2.3 ##
@pytest.mark.rlpunit
def test_cancel_amend_screeing_unit(
    page: Page, rlp_screening_unit_list_page: ScreeningUnitListPage, db_util
) -> None:
    """Cancel amend screening unit  and assert the unit list count on the UI and DB should be the same"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    rlp_screening_unit_list_page.select_status_dropdown("All")
    page.wait_for_timeout(3000)
    db_row_count = rlp_screening_unit_list_page.screening_unit_list_count_in_db(db_util)
    ui_row_count = rlp_screening_unit_list_page.extract_paging_unit_list_count()
    assert db_row_count == int(ui_row_count)
    unit_name = f"unit_name-{datetime.now()}"
    rlp_screening_unit_list_page.create_unit(unit_name)
    rlp_screening_unit_list_page.filter_unit_by_name(unit_name)
    rlp_screening_unit_list_page.dbl_click_on_filtered_unit_name()
    amend_unit_name = f"amend_name-{datetime.now()}"
    rlp_screening_unit_list_page.enter_amend_screening_unit_name(amend_unit_name)
    rlp_screening_unit_list_page.click_cancel_btn_on_amend_screening_unit_pop_up_window()
    page.wait_for_timeout(3000)
    ScreenshotTool(page).take_screenshot("rlp_unit_amend_tc_16")
    amend_db_row_count = rlp_screening_unit_list_page.screening_unit_list_count_in_db(
        db_util
    )
    amend_ui_row_count = rlp_screening_unit_list_page.extract_paging_unit_list_count()
    assert amend_db_row_count == int(amend_ui_row_count)


## Scenario 4, 21.1.1, 24.1.2, 24.1.3, 29.1.5 ##
@pytest.mark.rlpunit
def test_amend_screeing_unit_days_and_notes(
    page: Page, rlp_screening_unit_list_page: ScreeningUnitListPage
) -> None:
    """Amend screening unit name and usual no of appointments and notes"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    unit_name = f"unit_name-{datetime.now()}"
    rlp_screening_unit_list_page.create_unit(unit_name)
    rlp_screening_unit_list_page.filter_unit_by_name(unit_name)
    rlp_screening_unit_list_page.dbl_click_on_filtered_unit_name()
    amend_unit_name = f"amend_name-{datetime.now()}"
    amend_notes = generate_random_string(250)
    unit_data = {
        "amend_unit_name": amend_unit_name,
        "amend_unit_notes": amend_notes,
        **{
            day: str(secrets.randbelow(999))
            for day in ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
        },
    }
    rlp_screening_unit_list_page.enter_amend_screening_unit_name(amend_unit_name)
    rlp_screening_unit_list_page.enter_amend_usual_number_of_appointments_text_box(
        unit_data
    )
    rlp_screening_unit_list_page.enter_amend_screening_unit_notes(amend_notes)
    rlp_screening_unit_list_page.click_amend_screening_unit_btn_on_pop_up_window()
    page.wait_for_timeout(3000)
    rlp_screening_unit_list_page.filter_unit_by_name(amend_unit_name)
    rlp_screening_unit_list_page.dbl_click_on_filtered_unit_name()
    amended_day_values = rlp_screening_unit_list_page.get_day_appointment_value()
    field_amend_notes = page.locator("textarea#notesAmendText").input_value()
    assert field_amend_notes == amend_notes
    # Assert that the UI data matches the expected data
    for day, expected_value in unit_data.items():
        if not day.startswith("amend_unit"):
            day_value = amended_day_values[day.capitalize()]
            assert (
                day_value == expected_value
            ), f"Mismatch for {day}: expected {expected_value}, got {day_value}"


## Scenario 4 - 18.2.1, 18.2.2, 18.2.4, 18.2.5, 21.2.1, 21.2.2, 24.2.1, 30.2.1, 30.2.3 ##
@pytest.mark.rlpunit
@pytest.mark.parametrize("amend_unit_name", ["#$%&", "CA", "   ", "Batman"])
def test_negative_amend_screeing_unit_name(
    page: Page, rlp_screening_unit_list_page: ScreeningUnitListPage, amend_unit_name
) -> None:
    """
    Amend screening unit name using invalid data and capturing the error messages
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    unit_name = f"unit_name-{datetime.now()}"
    rlp_screening_unit_list_page.create_unit(unit_name)
    rlp_screening_unit_list_page.filter_unit_by_name(unit_name)
    rlp_screening_unit_list_page.dbl_click_on_filtered_unit_name()
    notes = "negative invalid char # % $ & test"
    unit_data = {
        "amend_unit_name": amend_unit_name,
        "thu": "",
        "notes": notes,
        **{
            day: "".join(secrets.choice(string.ascii_letters) for _ in range(2))
            for day in ["sun", "mon", "tue", "wed", "fri", "sat"]
        },
    }
    rlp_screening_unit_list_page.amend_screening_unit(unit_data)

    errors = {
        bool(
            re.search(r"[#$%<>&]", amend_unit_name)
        ): "Name contains invalid characters",
        len(amend_unit_name) < 3: "The Name you entered is too short",
        amend_unit_name == "Batman": "Name is already in use by another unit",
        amend_unit_name.strip() == "": "Unit Type must be populated",
        notes
        == "negative invalid char # % $ & test": "Notes contains invalid characters",
    }

    for condition, message in errors.items():
        if condition:
            expect(page.get_by_text(message)).to_be_visible()
            break


## Scenario 4 - 21.2.1, 21.2.2, 24.2.1, 28.2.1, 30.2.2 ##
@pytest.mark.rlpunit
def test_negative_amend_screeing_unit_name(
    page: Page, rlp_screening_unit_list_page: ScreeningUnitListPage
) -> None:
    """
    Amend screening unit name using invalid data and capturing the error messages
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    unit_name = f"unit_name-{datetime.now()}"
    rlp_screening_unit_list_page.create_unit(unit_name)
    rlp_screening_unit_list_page.filter_unit_by_name(unit_name)
    rlp_screening_unit_list_page.dbl_click_on_filtered_unit_name()
    notes = "negative invalid char # % $ & test"
    unit_data = {
        "unit_name": unit_name,
        "thu": "",
        "notes": notes,
        **{
            day: "".join(secrets.choice(string.ascii_letters) for _ in range(2))
            for day in ["sun", "mon", "tue", "wed", "fri", "sat"]
        },
    }
    rlp_screening_unit_list_page.amend_screening_unit(unit_data)
    for day in [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]:
        expect(
            page.get_by_text(f"{day} Appointments must be between 0 and 999")
        ).to_be_visible()
    expect(page.get_by_text("Notes contains invalid characters")).to_be_visible()
    ScreenshotTool(page).take_screenshot("rlp_unit_amend_tc_21_24_28_30")


## Test_31 ##
@pytest.mark.rlpunit
def test_user2_from_same_bso_can_access_the_user1_amended_data(
    page: Page, rlp_screening_unit_list_page: ScreeningUnitListPage, context
) -> None:
    """
    Amended screening unit is available for another user from same BSO
    """
    # Logged into BSS_SO1 user1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    unit_name = f"user1-{datetime.now()}"
    rlp_screening_unit_list_page.create_unit(unit_name)
    rlp_screening_unit_list_page.filter_unit_by_name(unit_name)
    rlp_screening_unit_list_page.dbl_click_on_filtered_unit_name()
    amend_unit_name = f"amend_name-{datetime.now()}"
    rlp_screening_unit_list_page.enter_amend_screening_unit_name(amend_unit_name)
    rlp_screening_unit_list_page.click_amend_screening_unit_btn_on_pop_up_window()
    context.clear_cookies()
    page.wait_for_timeout(500)
    # Logged on as BSS_SO1 user2
    UserTools().user_login(page, "BSO User2 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    rlp_screening_unit_list_page.filter_unit_by_name(amend_unit_name)
    ScreenshotTool(page).take_screenshot("rlp_unit_amend_tc_31")
    assert page.wait_for_selector(f"//tr//td[4]").text_content() == amend_unit_name
