import pytest
from pages.main_menu import MainMenuPage
from pages.rlp_location_list_page import ScreeningLocationListPage
from pages.rlp_cohort_list_page import CohortListPage
from playwright.sync_api import expect, Page
from datetime import datetime
from pages.rlp_unit_list_page import ScreeningUnitListPage
from utils.test_helpers import generate_random_string
from utils.screenshot_tool import ScreenshotTool
from utils.user_tools import UserTools


#### Test_01
#### Test_03
@pytest.mark.locationlist
def test_paging_of_screening_location_list(
    page: Page, rlp_location_list_page: ScreeningLocationListPage, db_util
) -> None:
    """
    Test to check the paging of the location list
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Location List")
    # Expected to see the screening location page
    expect(page.get_by_text("Screening location list", exact=True)).to_be_visible()
    # Checking the paging info
    db_row_count = rlp_location_list_page.screening_location_count_in_db(db_util)
    ui_row_count = rlp_location_list_page.extract_paging_info()
    assert db_row_count == int(ui_row_count)


#### Test_04
@pytest.mark.locationlist
def test_add_screening_location(
    page: Page, rlp_location_list_page: ScreeningLocationListPage
) -> None:
    """
    Test to add location to the location list
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Location List")
    # Adding new screening location
    location_name = f"Location_name-{datetime.now()}"
    rlp_location_list_page.click_add_screening_location_btn()
    rlp_location_list_page.enter_screening_location_name(location_name)
    rlp_location_list_page.click_add_screening_location_btn_on_popup()
    # Entering the newly added location name in the search box
    rlp_location_list_page.enter_screening_location_filter_txtbox(location_name)
    # Capturing the search value and stored it in the search_value
    search_value = page.locator("//tbody/tr/td[2]").text_content()
    page.wait_for_timeout(4000)
    ScreenshotTool(page).take_screenshot("rlp_unit_tc_4")
    # asserting the location_name and search_value
    assert location_name == search_value


#### Test_04 Negative test
@pytest.mark.locationlist
def test_cancel_screening_location(
    page: Page, rlp_location_list_page: ScreeningLocationListPage
) -> None:
    """
    Test to cancel the screening location and asserting the values of before and after the cancellation,
    both values should be the same
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Location List")
    # Extracting page_info before cancellation
    before_cancellation = rlp_location_list_page.extract_paging_info()
    # Cancel add screening location
    location_name = f"Location_name-{datetime.now()}"
    rlp_location_list_page.click_add_screening_location_btn()
    rlp_location_list_page.enter_screening_location_name(location_name)
    rlp_location_list_page.click_cancel_add_screening_location_btn()
    # Extracting page_info after cancellation
    after_cancellation = rlp_location_list_page.extract_paging_info()
    # Assering page number before and after the cancellation
    assert before_cancellation == after_cancellation


#### Test_05
@pytest.mark.locationlist
def test_default_screening_location_values(
    page: Page, rlp_location_list_page: ScreeningLocationListPage
) -> None:
    """
    Test to verify the default location field, field should be empty
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Location List")
    # Expected default values should be empty
    rlp_location_list_page.click_add_screening_location_btn()
    expect(page.locator("#locationNameText")).to_be_empty()


#### Test_06  valid_data
@pytest.mark.locationlist
@pytest.mark.parametrize("input_length", [3, 100])
def test_create_location_valid_data_positive(
    page: Page, rlp_location_list_page: ScreeningLocationListPage, input_length
) -> None:
    """
    Test for creating screening location using the valid field length of 3 and 100 char,
    asserting created value and the actual value
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Location List")
    location_name = generate_random_string(input_length)
    rlp_location_list_page.click_add_screening_location_btn()
    rlp_location_list_page.enter_screening_location_name(location_name)
    rlp_location_list_page.click_add_screening_location_btn_on_popup()
    rlp_location_list_page.enter_screening_location_filter_txtbox(location_name)
    page.wait_for_timeout(4000)
    # Capturing the search value and stored it in the search_value
    search_value = page.locator("//tbody/tr/td[2]").text_content()
    # asserting the location_name and search_value
    assert location_name == search_value


#### Test_06 negative invalid_data
@pytest.mark.locationlist
@pytest.mark.parametrize(
    "invalid_data, expected_message",
    [
        ("$%&@", "Name contains invalid characters"),
        ("cd", "The Name you entered is too short"),
        ("     ", "Name must be populated"),
        (
            "Aldi - Caldecott County Retail Park",
            "Name is already in use by another location",
        ),
    ],
)
def test_create_location_invalid_data_negative(
    page: Page,
    rlp_location_list_page: ScreeningLocationListPage,
    invalid_data,
    expected_message,
) -> None:
    """
    Test for try creating the screening location with invalid data "$%&@","cd", "  ", already existing name
    and expecting the error values
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Location List")
    # Enter invalid_data in the location name txt box
    rlp_location_list_page.click_add_screening_location_btn()
    rlp_location_list_page.enter_screening_location_name(invalid_data)
    rlp_location_list_page.click_add_screening_location_btn_on_popup()
    # Assert that the correct error message is displayed based on invalid_data
    expect(page.get_by_text(expected_message)).to_be_visible()


#### Test_07
@pytest.mark.locationlist
def test_check_availability_of_locations_different_user_same_bso(
    page: Page, rlp_location_list_page: ScreeningLocationListPage, context
) -> None:
    """
    under same bso, location was created by user_1 and user_2 from same bso can have access to the location
    """
    # Logged into BSS_SO1_User1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Location List")
    # Adding new screening location
    location_name = f"location_name-{datetime.now()}"
    rlp_location_list_page.click_add_screening_location_btn()
    rlp_location_list_page.enter_screening_location_name(location_name)
    rlp_location_list_page.click_add_screening_location_btn_on_popup()
    context.clear_cookies()
    # Logged into BSS_SO1_User2
    UserTools().user_login(page, "BSO User2 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Location List")
    # Searching for the screening_location created by User 1 while logged in as User 2
    rlp_location_list_page.enter_screening_location_filter_txtbox(location_name)
    # storing the User_2 filterd location_name in filterd_name
    filterd_name = rlp_location_list_page.value_of_filterd_location_name()
    # assering the the location name created by User_1 and filterd by User_2
    assert location_name == filterd_name
    # User_2 is trying to create a location already created by User_1
    rlp_location_list_page.click_add_screening_location_btn()
    rlp_location_list_page.enter_screening_location_name(location_name)
    rlp_location_list_page.click_add_screening_location_btn_on_popup()
    # Test should throw an error message
    expect(
        page.get_by_text("Name is already in use by another location")
    ).to_be_visible()


#### Test_08
@pytest.mark.locationlist
def test_check_availability_of_locations_different_user_different_bso(
    page: Page, rlp_location_list_page: ScreeningLocationListPage, context
) -> None:
    """
    Location was created by user_1, user_2 from different bso can't have access to the location
    user 2 from different bso try to search for the location created by user 1 will get a response as "No matching records found"
    """
    # Logged into BSS_SO1_User1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Location List")
    # Adding new screening location
    location_name = f"Location_name-{datetime.now()}"
    rlp_location_list_page.click_add_screening_location_btn()
    rlp_location_list_page.enter_screening_location_name(location_name)
    rlp_location_list_page.click_add_screening_location_btn_on_popup()
    rlp_location_list_page.click_log_out_btn()
    context.clear_cookies()
    # Logged into BSS_SO2_User2
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Location List")
    # BSO specific Locations are not available to other Users within other BSOs
    rlp_location_list_page.enter_screening_location_filter_txtbox(location_name)
    expect(page.get_by_text("No matching records found")).to_be_visible()
    rlp_location_list_page.click_add_screening_location_btn()
    rlp_location_list_page.enter_screening_location_name(location_name)
    rlp_location_list_page.click_add_screening_location_btn_on_popup()
    # storing the User_2 created and filterd location_name in filterd_name
    rlp_location_list_page.enter_screening_location_filter_txtbox(location_name)
    filterd_name = rlp_location_list_page.value_of_filterd_location_name()
    # assering the the location name created and filterd by User_2
    assert location_name == filterd_name


#### Test coveres Test_09, Test_10 and Test_11(valid_data_set)
@pytest.mark.locationlist
@pytest.mark.parametrize("input_length", [3, 100])
def test_amend_screening_location(
    page: Page, rlp_location_list_page: ScreeningLocationListPage, input_length
) -> None:
    """
    Test for amending screening location, in here I created the location and amended the location using the valid field length of 3 and 100 char,
    asserting the amend_name vs actual amended value
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Location List")
    # Adding new screening location
    location_name = f"location_name-{datetime.now()}"
    rlp_location_list_page.click_add_screening_location_btn()
    rlp_location_list_page.enter_screening_location_name(location_name)
    rlp_location_list_page.click_add_screening_location_btn_on_popup()
    # Edit the newly added location
    rlp_location_list_page.enter_screening_location_filter_txtbox(location_name)
    rlp_location_list_page.invoke_filtered_screening_location()
    expect(
        page.locator("#amendButtonInAmendLocationPopupText")
    ).to_be_visible()  # Test 9 verification
    # Amending the newly added location using generate_randon string method and storing in the "amend_name" and clicking amend_button on the pop_up window
    amend_name = generate_random_string(input_length)
    rlp_location_list_page.enter_amend_screening_location_name(amend_name)
    rlp_location_list_page.click_amend_screening_location_btn()
    # entering Amend_name in the search box
    rlp_location_list_page.enter_screening_location_filter_txtbox(amend_name)
    # storing the filterd location value in the "filterd_amend_name"
    filterd_amend_name = rlp_location_list_page.value_of_filterd_location_name()
    # assering the amend_value and filterd_amend_value
    assert amend_name == filterd_amend_name


## Test_11 negatie test with invalid_data
@pytest.mark.locationlist
@pytest.mark.parametrize(
    "invalid_data, expected_message",
    [
        ("$%&@", "Name contains invalid characters"),
        ("cd", "The Name you entered is too short"),
        ("     ", "Name must be populated"),
        (
            "Aldi - Caldecott County Retail Park",
            "Name is already in use by another location",
        ),
    ],
)
def test_invalid_amend_screening_location(
    page: Page,
    rlp_location_list_page: ScreeningLocationListPage,
    invalid_data,
    expected_message,
) -> None:
    """
    Test for amending screening location with invalid data "$%&@","cd", "  ", already existing name
    and expecting the error values
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Location List")
    # Adding new screening location
    location_name = f"location_name-{datetime.now()}"
    rlp_location_list_page.click_add_screening_location_btn()
    rlp_location_list_page.enter_screening_location_name(location_name)
    rlp_location_list_page.click_add_screening_location_btn_on_popup()
    # Edit the pre exising location
    rlp_location_list_page.enter_screening_location_filter_txtbox(location_name)
    rlp_location_list_page.invoke_filtered_screening_location()
    # Enter the invalid amend data
    rlp_location_list_page.enter_amend_screening_location_name(invalid_data)
    rlp_location_list_page.click_amend_screening_location_btn()
    # Assert that the correct error message is displayed based on invalid_data
    expect(page.get_by_text(expected_message)).to_be_visible()


## Test_12
@pytest.mark.locationlist
def test_amend_screening_location_availabale_for_other_user_within_same_bso(
    page: Page, rlp_location_list_page: ScreeningLocationListPage, context
) -> None:
    """
    Test for amending screening location by user2 with in the same bso which is created by user1
    asserting the amended value vs actual amended value
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Location List")
    # Adding new screening location
    location_name = f"Location_name-{datetime.now()}"
    rlp_location_list_page.click_add_screening_location_btn()
    rlp_location_list_page.enter_screening_location_name(location_name)
    rlp_location_list_page.click_add_screening_location_btn_on_popup()
    # Edit the newly added location
    rlp_location_list_page.enter_screening_location_filter_txtbox(location_name)
    rlp_location_list_page.invoke_filtered_screening_location()

    # Amending the newly added location using generate_randon string method and storing in the "amend_name" and clicking amend_button on the pop_up window
    amend_name = f"amend_location-{datetime.now()}"
    rlp_location_list_page.enter_amend_screening_location_name(amend_name)
    rlp_location_list_page.click_amend_screening_location_btn()
    rlp_location_list_page.click_log_out_btn()
    context.clear_cookies()

    # Logged into BSS_SO1_User2
    UserTools().user_login(page, "BSO User2 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Location List")
    # Searching for the screening_location created by User 1 while logged in as User 2
    rlp_location_list_page.enter_screening_location_filter_txtbox(amend_name)
    # storing the User_2 filterd location_name in filterd_name
    filterd_name = rlp_location_list_page.value_of_filterd_location_name()
    # assering the the location name created by User_1 and filterd by User_2
    assert amend_name == filterd_name


## Test_13
@pytest.mark.locationlist
def test_location_linked_to_multiple_cohorts(
    page: Page, rlp_cohort_list_page: CohortListPage, context
) -> None:
    """
    created 2 cohorts and 1 location, linked 2 cohorts to 1 location
    """
    # create unit for test data
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    ScreeningUnitListPage(page).create_unit("Batman")
    context.clear_cookies()
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")

    # create cohort inner function
    def create_cohort(location_name, cohort_name):
        rlp_cohort_list_page.click_create_screening_cohort_by_gp_practice_btn()
        rlp_cohort_list_page.enter_screening_cohort_name_field(cohort_name)
        rlp_cohort_list_page.enter_expected_attendance_rate("25")
        rlp_cohort_list_page.select_default_screening_location_dropdown(location_name)
        rlp_cohort_list_page.select_default_screening_unit_dropdown("Batman")
        rlp_cohort_list_page.click_create_screening_cohort_save_btn()
        page.wait_for_timeout(3000)

    location_name = "Aldi - Caldecott County Retail Park"
    cohort_name = f"Multiple_cohorts-{datetime.now()}"
    input_names = [f"{cohort_name} - Test 1", f"{cohort_name} - Test 2"]

    # creating multiple(2) cohorts in a loop
    for name in input_names:
        create_cohort(location_name, name)

    # filtering name and location
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.enter_screening_location_filter(location_name)
    filterd_names = page.locator("//tr//td[2]").all_text_contents()
    assert input_names == filterd_names
