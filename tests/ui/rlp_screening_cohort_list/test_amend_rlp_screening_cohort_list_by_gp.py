import playwright
import pytest

# from conftest import db_util
from pages.main_menu import MainMenuPage
from pages.rlp_cohort_list_page import CohortListPage
from playwright.sync_api import expect, Page, Playwright
from datetime import datetime
from pages.rlp_location_list_page import ScreeningLocationListPage
from utils.test_helpers import generate_random_string
from utils import test_helpers
from utils.user_tools import UserTools


# test to create the unit test data
@pytest.mark.amendcohortgp
def test_check_and_create_unit_test_data(
    page: Page, rlp_cohort_list_page: CohortListPage
) -> None:
    """creating unit test data for User2 BS2"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    unit_names = ["Batman", "Captain"]
    for unit_name in unit_names:
        rlp_cohort_list_page.create_unit_if_not_exists(unit_name)


#### Test_15
@pytest.mark.amendcohortgp
def test_try_amend_cohort_by_dblclick_and_invoke_pencil_icon(
    page: Page, rlp_cohort_list_page: CohortListPage
) -> None:
    """User invokes the Edit Cohort functionality by Double click list entry and Invoke Pencil Icon"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")

    # creating cohort using method with hardcoded attendence and screening unit values
    cohort_name = f"cohort_name-{datetime.now()}"
    location_name = "Poundland Car Park - Alberta Retail Park"
    rlp_cohort_list_page.create_cohort(cohort_name, location_name)

    # Filter the newly created cohort and double clicking on the cohort to amend(testing double click)
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    expect(page.get_by_text("Amend Screening Cohort")).to_be_visible()
    # cancelling the amend
    rlp_cohort_list_page.click_amend_cohort_cancel_button()

    # Filter the newly created cohort and clicking on the cohort pencil to amend(testing pencil icon)
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.click_filtered_cohort_pencil_icon()
    expect(page.get_by_text("Amend Screening Cohort")).to_be_visible()


#### Test_16 positive data validation
@pytest.mark.parametrize("input_length", [3, 100])
@pytest.mark.amendcohortgp
def test_amend_cohort_name_with_valid_data(
    page: Page, rlp_cohort_list_page: CohortListPage, input_length
) -> None:
    """User amends data in the Screening Cohort field with valid data"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    # creating cohort
    cohort_name = f"cohort_name-{datetime.now()}"
    location_name = "Poundland Car Park - Alberta Retail Park"
    unit_name = "Batman"
    rlp_cohort_list_page.create_cohort_without_gp(cohort_name, location_name, unit_name)
    # Filter the newly created cohort and double clicking on the cohort to amend(testing double click)
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    # Amending cohort name field
    amend_cohort_name = generate_random_string(input_length)
    rlp_cohort_list_page.enter_amend_screening_cohort_name(amend_cohort_name)
    rlp_cohort_list_page.click_amend_save_btn()
    rlp_cohort_list_page.enter_screening_cohort_name_filter(amend_cohort_name)
    filterd_amend_name = rlp_cohort_list_page.value_of_filtered_cohort_name()
    assert amend_cohort_name == filterd_amend_name


## Test_16 negative field data validation
@pytest.mark.amendcohortgp
@pytest.mark.parametrize(
    "amend_name, expected_message",
    [
        ("$%&@", "Screening Cohort Name contains invalid characters"),
        ("cd", "The Screening Cohort Name you entered is too short"),
        ("     ", "Screening Cohort Name must be populated"),
        ("Hadley", "Screening Cohort Name is already in use by another cohort"),
    ],
)
def test_amend_screening_cohort_with_invalid_data(
    page: Page, rlp_cohort_list_page: CohortListPage, amend_name, expected_message
) -> None:
    """Negative test - User amends data in the Screening Cohort field with inalidv data"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    # creating cohort
    cohort_name = f"cohort_name-{datetime.now()}"
    location_name = "Poundland Car Park - Alberta Retail Park"
    unit_name = "Batman"
    rlp_cohort_list_page.create_cohort_without_gp(cohort_name, location_name, unit_name)
    # Filter the newly created cohort and double clicking on the cohort to amend(testing double click)
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    # Amending cohort name field
    rlp_cohort_list_page.enter_amend_screening_cohort_name(amend_name)
    rlp_cohort_list_page.click_amend_save_btn()
    # Assert that the correct error message is displayed based on invalid_data
    expect(page.get_by_text(expected_message)).to_be_visible()


#### Test_17 positive field data validation for amend Expected Attendance Rate
@pytest.mark.amendcohortgp
@pytest.mark.parametrize("input_value", ["0.0", "100.0"])
def test_amend_expected_attendance_rate_valid_data(
    page: Page, rlp_cohort_list_page: CohortListPage, input_value
) -> None:
    """Positive test - The User is able to select and commit a change to Expected Attendance Rate - integer values 0.00 - 100.0"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    cohort_name = f"amend_attendance-{datetime.now()}"
    location_name = "Poundland Car Park - Alberta Retail Park"
    rlp_cohort_list_page.create_cohort(cohort_name, location_name)
    # Filter the newly created cohort and double clicking on the cohort to amend(testing double click)
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    # Test data
    rlp_cohort_list_page.enter_amend_expected_attendance_rate(input_value)
    rlp_cohort_list_page.click_amend_save_btn()
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    filtered_amend_attendance = rlp_cohort_list_page.value_of_filtered_attendance()
    assert input_value == filtered_amend_attendance


#### Test_17 negative test for amend Expected Attendance Rate field
@pytest.mark.amendcohortgp
@pytest.mark.parametrize(
    "amend_attendance_rate, expected_message",
    [
        ("cd", "Invalid value"),
        ("     ", "Expected Attendance Rate must be between 0 and 100"),
    ],
)
def test_amend_expected_attendance_rate_invalid_data(
    page: Page,
    rlp_cohort_list_page: CohortListPage,
    amend_attendance_rate,
    expected_message,
) -> None:
    """Negative test - User amends data in the Expected Attendance Rate (%) field - Non integer value and Null"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    cohort_name = f"amend_attendance-{datetime.now()}"
    location_name = "Poundland Car Park - Alberta Retail Park"
    rlp_cohort_list_page.create_cohort(cohort_name, location_name)
    # Filter the newly created cohort and double clicking on the cohort to amend(testing double click)
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    rlp_cohort_list_page.enter_amend_expected_attendance_rate(amend_attendance_rate)
    rlp_cohort_list_page.click_amend_save_btn()
    # Assert that the correct error message is displayed based on invalid_data
    expect(page.get_by_text(expected_message)).to_be_visible()


#### Test_18
@pytest.mark.amendcohortgp
def test_amend_cohort_location(
    page: Page, rlp_cohort_list_page: CohortListPage
) -> None:
    """The correct list of Locations available to this user in this BSO, are displayed correctly,
    The User is able to select and commit a change to Location"""
    # Logged into BSS_SO1 location_list to create location data

    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Location List")
    location_name = f"cohort_location-{datetime.now()}"
    ScreeningLocationListPage(page).create_screening_location(location_name)

    # extracting the location count
    location_list_count = rlp_cohort_list_page.extract_location_paging_list_count()

    # Logged into BSS_SO1
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    cohort_name = f"cohort_name-{datetime.now()}"
    unit_name = "Batman"
    rlp_cohort_list_page.create_cohort_without_gp(cohort_name, location_name, unit_name)
    page.wait_for_timeout(3000)
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()

    # extracting the drop down location count
    dropdown_count = rlp_cohort_list_page.number_of_location_dropdown_count()
    assert location_list_count == dropdown_count
    amend_location_name = "Aldi - Caldecott County Retail Park"
    rlp_cohort_list_page.select_amend_screening_location_dropdown(amend_location_name)
    rlp_cohort_list_page.click_amend_save_btn()
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    expect(page.get_by_text("Aldi - Caldecott County Retail Park")).to_be_visible()


#### Test_19
@pytest.mark.amendcohortgp
def test_amend_cohort_unit_list(
    page: Page, rlp_cohort_list_page: CohortListPage
) -> None:
    """The correct list of Active only Units available to this user in this BSO, are displayed correctly,
    The User is able to select and commit a change to Default Unit"""
    # Logged into BSS_SO1 unit_list to create unit data
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    unit_name = f"cohort_unit-{datetime.now()}"
    rlp_cohort_list_page.create_unit_for_test_data(unit_name)
    # extracting the unit count
    unit_list_count = rlp_cohort_list_page.extract_paging_unit_list_count_active_only()

    # Logged into BSS_SO1
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    cohort_name = f"cohort_name-{datetime.now()}"
    location_name = "Aldi - Caldecott County Retail Park"
    rlp_cohort_list_page.create_cohort_without_gp(cohort_name, location_name, unit_name)
    page.wait_for_timeout(3000)
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()

    # extracting the drop down location count
    dropdown_count = rlp_cohort_list_page.number_of_unit_dropdown_count()
    assert unit_list_count == dropdown_count
    amend_unit_name = "Batman"
    rlp_cohort_list_page.select_amend_screening_unit_dropdown(amend_unit_name)
    rlp_cohort_list_page.click_amend_save_btn()
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    expect(page.get_by_text("Batman")).to_be_visible()


#### Test_20
@pytest.mark.amendcohortgp
def test_amend_added_gp_practices_are_visible(
    page: Page, rlp_cohort_list_page: CohortListPage
) -> None:
    """Amend test - User Selects another GP Practice from the 'All available GP Practices' List by invoking the 'Add' PB"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")

    cohort_name = f"cohort_name-{datetime.now()}"
    location_name = "Aldi - Caldecott County Retail Park"
    rlp_cohort_list_page.create_cohort(cohort_name, location_name)

    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    page.wait_for_timeout(3000)
    # including gp practice
    rlp_cohort_list_page.click_select_gp_practices_btn()
    rlp_cohort_list_page.enter_gp_code_field("A00002")
    rlp_cohort_list_page.click_add_btn_gp_practices_to_include()
    rlp_cohort_list_page.click_done_btn_gp_practices_include_popup()
    rlp_cohort_list_page.click_select_gp_practices_btn()
    rlp_cohort_list_page.enter_gp_code_field("A00003")
    rlp_cohort_list_page.click_add_btn_gp_practices_to_include()
    rlp_cohort_list_page.click_done_btn_gp_practices_include_popup()
    rlp_cohort_list_page.click_create_screening_cohort_save_btn()
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    included_gp_practices = page.locator(
        "//table[@id='practicesToIncludeList']//tr//td[2]"
    ).count()
    assert included_gp_practices == 3
    # Locate all GP practice codes in the table
    gp_practice_codes = page.locator(
        "//div[@id='practicesToIncludeList_wrapper']//tr//td[2]"
    ).all_inner_texts()
    # Assert that "A00002" and "A00003" are in the list of GP practice codes
    assert (
        "A00002" in gp_practice_codes
    ), "A00002 was not found in the included GP practices."
    assert (
        "A00003" in gp_practice_codes
    ), "A00002 was not found in the included GP practices."
    assert (
        "A00005" in gp_practice_codes
    ), "A00003 was not found in the included GP practices."


#### Test_21
@pytest.mark.amendcohortgp
def test_amend_remove_gp_practices(
    page: Page, rlp_cohort_list_page: CohortListPage
) -> None:
    """
    The 'Amend Screening Cohort' screen is displayed for the correct Cohort
    Cohort has GP Practices selected in the 'Included GP Practices List'
    User then selects to Remove GP Practices by invoking the 'Remove' button
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")

    cohort_name = f"cohort_name-{datetime.now()}"
    location_name = "Aldi - Caldecott County Retail Park"
    rlp_cohort_list_page.create_cohort(cohort_name, location_name)

    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    page.wait_for_timeout(3000)
    # including gp practice
    rlp_cohort_list_page.click_select_gp_practices_btn()
    rlp_cohort_list_page.enter_gp_code_field("A00002")
    rlp_cohort_list_page.click_add_btn_gp_practices_to_include()
    rlp_cohort_list_page.click_done_btn_gp_practices_include_popup()
    rlp_cohort_list_page.click_select_gp_practices_btn()
    rlp_cohort_list_page.enter_gp_code_field("A00003")
    rlp_cohort_list_page.click_add_btn_gp_practices_to_include()
    rlp_cohort_list_page.click_done_btn_gp_practices_include_popup()
    rlp_cohort_list_page.click_create_screening_cohort_save_btn()
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    included_gp_practices = page.locator(
        "//table[@id='practicesToIncludeList']//tr//td[2]"
    ).count()
    assert included_gp_practices == 3

    # removing one included gp practice
    rlp_cohort_list_page.click_remove_button_by_gp_code("A00002")
    removed_included_gp_practices = page.locator(
        "//table[@id='practicesToIncludeList']//tr//td[2]"
    ).count()
    assert removed_included_gp_practices == 2

    # removing one included gp practice
    rlp_cohort_list_page.click_remove_button_by_gp_code("A00003")
    removed_included_gp_practices = page.locator(
        "//table[@id='practicesToIncludeList']//tr//td[2]"
    ).count()
    assert removed_included_gp_practices == 1

    # removing last of the included gp practice
    rlp_cohort_list_page.click_remove_button_by_gp_code("A00005")
    removed_included_gp_practices = page.locator(
        "//table[@id='practicesToIncludeList']//tr//td[2]"
    ).count()
    assert removed_included_gp_practices == 0


#### Test_22
@pytest.mark.amendcohortgp
def test_amend_cancel_adding_gp_practices(
    page: Page, rlp_cohort_list_page: CohortListPage
) -> None:
    """
    Screening Cohort List is displayed,
    User invokes 'Add by Practice' pb and invokes 'Cancel' pb
    User is returned to the 'Screening Cohort List' Screen
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")

    cohort_name = f"cohort_name-{datetime.now()}"
    location_name = "Aldi - Caldecott County Retail Park"
    unit_name = "Batman"
    rlp_cohort_list_page.create_cohort_without_gp(cohort_name, location_name, unit_name)

    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    page.wait_for_timeout(3000)
    # clicking on amend page cancel button
    rlp_cohort_list_page.click_amend_cohort_cancel_button()
    expect(page.get_by_text("Screening cohort list", exact=True)).to_be_visible()


#### Test_23
@pytest.mark.amendcohortgp
def test_amend_cohort_name_avilable_for_user2(
    page: Page, rlp_cohort_list_page: CohortListPage, context
) -> None:
    """BSO specific GP Practice Cohort amendments are available to the other Users within the same BSO"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")

    # creating cohort using method with hardcoded attendence
    cohort_name = f"cohort_name-{datetime.now()}"
    location_name = "Poundland Car Park - Alberta Retail Park"
    unit_name = "Batman"
    rlp_cohort_list_page.create_cohort_without_gp(cohort_name, location_name, unit_name)
    # Filter the newly created cohort and double clicking on the cohort to amend(testing double click)
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()

    # Test data to amend cohort name
    amend_cohort_name = f"amend_user2-{datetime.now()}"
    rlp_cohort_list_page.enter_amend_screening_cohort_name(amend_cohort_name)
    rlp_cohort_list_page.click_amend_save_btn()
    context.clear_cookies()
    # Logged into BSS_SO1 as user2
    UserTools().user_login(page, "BSO User2 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    rlp_cohort_list_page.enter_screening_cohort_name_filter(amend_cohort_name)
    filterd_amend_name = rlp_cohort_list_page.value_of_filtered_cohort_name()
    assert amend_cohort_name == filterd_amend_name
