import playwright
import pytest

# from conftest import db_util
from pages.main_menu import MainMenuPage
from pages.rlp_cohort_list_page import CohortListPage
from playwright.sync_api import expect, Page, Playwright
from datetime import datetime
from pages.rlp_location_list_page import ScreeningLocationListPage
from pages.rlp_unit_list_page import ScreeningUnitListPage
from utils.test_helpers import generate_random_string
from utils import test_helpers
from utils.user_tools import UserTools


# test to create the unit test data
def test_check_and_create_unit_test_data(
    page: Page, rlp_cohort_list_page: CohortListPage
):
    """creating unit test data for User2 BS2"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    unit_names = ["Batman", "Captain"]
    for unit_name in unit_names:
        rlp_cohort_list_page.create_unit_if_not_exists(unit_name)


# test to create the location data
def test_check_and_create_location_test_data_for_outcode(
    page: Page, rlp_cohort_list_page: CohortListPage
):
    """
    Random test to generate location test data for User2 BS2
    """
    # Logged into BSS_SO2 User2
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Location List")
    locations = [
        "Aldi - Caldecott County Retail Park",
        "Poundland Car Park - Alberta Retail Park",
    ]
    for location in locations:
        ScreeningLocationListPage(page).create_location_if_not_exists(location)


#### Test_45
@pytest.mark.cohortoutcode
def test_to_verify_gp_practice_and_outcode_buttons_are_enable(
    page: Page, rlp_cohort_list_page: CohortListPage
):
    """
    Test to verify add By Practice pushbutton is enabled and
    add By Outcode pushbutton is enabled
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    assert page.locator(
        "button:has-text('Create screening cohort by GP practice')"
    ).is_enabled(), "'Create screening cohort by GP practice' button is not enabled"
    assert page.locator(
        "button:has-text('Create screening cohort by outcode')"
    ).is_enabled(), "'Create screening cohort by outcode' button is not enabled"


## Test_24
@pytest.mark.cohortoutcode
def test_for_outcode_defaults_are_set_and_displayed_correctly(
    page: Page, rlp_cohort_list_page: CohortListPage
) -> None:
    """test 'Create Screening Cohort' screen is displayed correctly
    all defaults are set & displayed correctly"""
    # Logged into BSS_SO2 user2
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")

    # Create Screening Cohort screen is displayed
    rlp_cohort_list_page.click_create_screening_cohort_by_outcode_btn()
    page.wait_for_timeout(3000)
    expect(page.get_by_text("Create screening cohort", exact=True)).to_be_visible()

    # All defaults are set & displayed correctly
    expect(page.locator("input#description")).to_be_empty()  # screening cohort name
    expect(
        page.locator("input#uptakePercentage")
    ).to_be_empty()  # Expected Attendance Rate (%)
    assert (
        page.locator("select#defaultLocation").input_value() == ""
    )  # Default Screening Location
    assert (
        page.locator("select#defaultUnit").input_value() == ""
    )  # Default Screening Unit
    expect(page.locator("td.dataTables_empty")).to_be_visible()  # Included GP Practices


# Test_25
@pytest.mark.cohortoutcode
def test_for_outcode_cancel_function(page: Page, rlp_cohort_list_page: CohortListPage):
    """
    User is able to cancel Cohort without saving and able to retuen to cohort home page
    """
    # Logged into BSS_SO2 user2
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    rlp_cohort_list_page.click_create_screening_cohort_by_outcode_btn()
    page.wait_for_timeout(3000)
    rlp_cohort_list_page.click_cancel_cohort_by_outcode_btn()
    page.wait_for_timeout(3000)
    expect(page.get_by_text("Screening cohort list", exact=True)).to_be_visible()


## Test_26
@pytest.mark.cohortoutcode
@pytest.mark.parametrize("input_length", [3, 100])
def test_create_screening_cohort_outcode_valid_data(
    page: Page, rlp_cohort_list_page: CohortListPage, input_length
) -> None:
    """
    Test for creating screening Cohort outcode using the valid field length of 3 and 100 char,
    asserting created value and the actual value
    """
    # Logged into BSS_SO2 user2
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    # Test data
    cohort_name = generate_random_string(
        input_length
    )  # generate_randon_string method will generate string between 3 & 100 which will be unique each time
    location_name = "Poundland Car Park - Alberta Retail Park"
    unit_name = "Batman"
    attendance_rate = "25"
    # checking uniqueness of the name
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    page.wait_for_timeout(3000)
    expect(page.locator("td.dataTables_empty")).to_be_visible()
    # creating cohort using create cohort method
    rlp_cohort_list_page.create_cohort_outcode_without_gp(
        cohort_name, str(attendance_rate), location_name, unit_name
    )
    # filtering name and storing in filterd_name
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    filterd_name = page.locator("//tr//td[2]").text_content()
    assert cohort_name == filterd_name


# creating cohort for below test
@pytest.mark.cohortoutcode
def test_create_screening_cohort_outcode_test_data(
    page: Page, rlp_cohort_list_page: CohortListPage
) -> None:
    """
    Test to create a test data
    """
    # Logged into BSS_SO2 user2
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    # Test data
    cohort_name = "Hadley"
    attendance_rate = "25"
    location_name = "Poundland Car Park - Alberta Retail Park"
    unit_name = "Batman"
    # creating cohort using create cohort method
    rlp_cohort_list_page.create_cohort_outcode_without_gp(
        cohort_name, str(attendance_rate), location_name, unit_name
    )


## Test_26 negative test
@pytest.mark.cohortoutcode
@pytest.mark.parametrize(
    "cohort_name, expected_message",
    [
        ("$%&@", "Screening Cohort Name contains invalid characters"),
        ("cd", "The Screening Cohort Name you entered is too short"),
        ("     ", "Screening Cohort Name must be populated"),
        ("Hadley", "Screening Cohort Name is already in use by another cohort"),
    ],
)
def test_try_to_create_screening_cohort_outcode_with_invalid_data(
    page: Page, rlp_cohort_list_page: CohortListPage, cohort_name, expected_message
):
    """
    Test for creating screening Cohort outcode using the invalid field values
    capturing the error messages
    """
    # Logged into BSS_SO2 user2
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    # Test data
    attendance_rate = "25"
    location_name = "Poundland Car Park - Alberta Retail Park"
    unit_name = "Batman"
    # try creating cohort using create cohort method
    rlp_cohort_list_page.create_cohort_outcode_without_gp(
        cohort_name, str(attendance_rate), location_name, unit_name
    )
    # Assert that the correct error message is displayed based on invalid_data
    expect(page.get_by_text(expected_message)).to_be_visible()


## Test_27
@pytest.mark.cohortoutcode
@pytest.mark.parametrize("attendance_rate", [0, 100])
def test_outcode_expected_attendance_rate_valid_data(
    page: Page, rlp_cohort_list_page: CohortListPage, attendance_rate
) -> None:
    """User enters valid data into Expected Attendance Rate (%) field"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    cohort_name = f"cohort_name-{datetime.now()}"
    location_name = "Poundland Car Park - Alberta Retail Park"
    unit_name = "Batman"
    rlp_cohort_list_page.create_cohort_outcode_without_gp(
        cohort_name, str(attendance_rate), location_name, unit_name
    )
    # filtering name and storing in filterd_name
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    assert (
        float(page.locator("input#uptakePercentage").input_value()) == attendance_rate
    )


## Test_27 negative test for Expected Attendance Rate field
@pytest.mark.cohortoutcode
@pytest.mark.parametrize(
    "attendance_rate, expected_message",
    [
        ("cd", "Invalid value"),
        ("     ", "Expected Attendance Rate must be between 0 and 100"),
    ],
)
def test_outcode_expected_attendance_rate_invalid_data(
    page: Page, rlp_cohort_list_page: CohortListPage, attendance_rate, expected_message
):
    """Negative test - User enters inalid data into Expected Attendance Rate (%) field"""
    # Logged into BSS_SO2 user2
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    # try to create cohort using invalid attendance rate
    cohort_name = f"cohort_name-{datetime.now()}"
    location_name = "Poundland Car Park - Alberta Retail Park"
    unit_name = "Batman"
    rlp_cohort_list_page.create_cohort_outcode_without_gp(
        cohort_name, attendance_rate, location_name, unit_name
    )
    # Assert that the correct error message is displayed based on invalid_data
    expect(page.get_by_text(expected_message)).to_be_visible()


## Test_28
@pytest.mark.cohortoutcode
def test_outcode_default_location_dropdown(
    page: Page, rlp_cohort_list_page: CohortListPage
):
    """The correct list of Locations available to this user in this BSO are displayed correctly"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")

    rlp_cohort_list_page.click_create_screening_cohort_by_outcode_btn()
    page.wait_for_timeout(3000)
    # extracting the drop down location count
    rlp_cohort_list_page.select_default_screening_location_dropdown(None)
    dropdown_count = rlp_cohort_list_page.number_of_location_dropdown_count()

    MainMenuPage(page).select_menu_option("Round Planning", "Screening Location List")
    # extracting the location count
    location_list_count = rlp_cohort_list_page.extract_location_paging_list_count()
    assert dropdown_count == location_list_count


## Test_29
@pytest.mark.cohortoutcode
def test_outcode_default_unit_dropdown(
    page: Page, rlp_cohort_list_page: CohortListPage
):
    """Test the correct list of Active only Units available to this user in this BSO are displayed correctly"""
    # Logged into BSS_SO2 user2
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")

    rlp_cohort_list_page.click_create_screening_cohort_by_outcode_btn()
    page.wait_for_timeout(3000)
    rlp_cohort_list_page.select_default_screening_unit_dropdown(None)
    dropdown_count = rlp_cohort_list_page.number_of_unit_dropdown_count()

    # Logged into BSS_SO2 location list
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    # extracting the location count
    unit_list_count = rlp_cohort_list_page.extract_paging_unit_list_count()
    assert dropdown_count == unit_list_count


## Test_30
@pytest.mark.cohortoutcode
def test_outcode_added_gp_practices_are_visible(
    page: Page, rlp_cohort_list_page: CohortListPage
):
    """1. Selects Outcode from the 'All available Outcodes' List, the correct Outcodes details are now visible in the Included Outcodes List
    Negative test - 2. Attempt to add same Outcode"""
    # Logged into BSS_SO2 user2
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")

    rlp_cohort_list_page.click_create_screening_cohort_by_outcode_btn()
    page.wait_for_timeout(3000)
    # including outcode
    rlp_cohort_list_page.click_select_outcodes_btn()
    rlp_cohort_list_page.enter_outcode_filter("EX1")
    rlp_cohort_list_page.click_add_btn_to_select_outcode("EX1")
    rlp_cohort_list_page.click_done_btn_gp_practices_include_popup()
    page.wait_for_timeout(3000)
    included_outcodes = page.locator(
        "//table[@id='practicesToIncludeList']//tr//td[2]"
    ).count()
    assert included_outcodes == 1

    # attempt to add the same outcode the add btn is not present 2nd time - negative test
    rlp_cohort_list_page.click_select_outcodes_btn()
    rlp_cohort_list_page.enter_outcode_filter("EX1")
    expect(
        page.locator("//tr[td[1][normalize-space()='EX1']]//button[text()='Add']")
    ).not_to_be_visible()


## Test_31
@pytest.mark.cohortoutcode
def test_selects_to_remove_outcodes(page: Page, rlp_cohort_list_page: CohortListPage):
    """User selects to Remove Outcodes - Removes 1 Outcode, Removes 2 Outcode, Removes all Outcodes"""
    # Logged into BSS_SO2 user2
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")

    rlp_cohort_list_page.click_create_screening_cohort_by_outcode_btn()
    page.wait_for_timeout(3000)
    # including outcodes
    rlp_cohort_list_page.click_select_outcodes_btn()
    rlp_cohort_list_page.enter_outcode_filter("EX1")
    rlp_cohort_list_page.click_add_btn_to_select_outcode("EX1")
    rlp_cohort_list_page.click_done_btn_gp_practices_include_popup()
    rlp_cohort_list_page.click_select_outcodes_btn()
    rlp_cohort_list_page.enter_outcode_filter("EX2")
    rlp_cohort_list_page.click_add_btn_to_select_outcode("EX2")
    rlp_cohort_list_page.click_done_btn_gp_practices_include_popup()
    rlp_cohort_list_page.click_select_outcodes_btn()
    rlp_cohort_list_page.enter_outcode_filter("EX3")
    rlp_cohort_list_page.click_add_btn_to_select_outcode("EX3")
    rlp_cohort_list_page.click_done_btn_gp_practices_include_popup()
    included_outcodes = page.locator(
        "//table[@id='practicesToIncludeList']//tr//td[2]"
    ).count()
    assert included_outcodes == 3
    # removing one included gp practice
    rlp_cohort_list_page.click_remove_button_by_gp_code("EX1")
    removed_included_outcodes = page.locator(
        "//table[@id='practicesToIncludeList']//tr//td[2]"
    ).count()
    assert removed_included_outcodes == 2
    # removing one included gp practice
    rlp_cohort_list_page.click_remove_button_by_gp_code("EX2")
    removed_included_outcodes = page.locator(
        "//table[@id='practicesToIncludeList']//tr//td[2]"
    ).count()
    assert removed_included_outcodes == 1
    # removing last of the included gp practice
    rlp_cohort_list_page.click_remove_button_by_gp_code("EX3")
    removed_included_outcodes = page.locator(
        "//table[@id='practicesToIncludeList']//tr//td[2]"
    ).count()
    assert removed_included_outcodes == 0


## Test_32
@pytest.mark.cohortoutcode
def test_outcode_click_save_without_filling_all_mandatory_fields(
    page: Page, rlp_cohort_list_page: CohortListPage
):
    """Invoke add button without filling out all the mandatory fiels and validate the error messages"""
    # Logged into BSS_SO2 user2
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    rlp_cohort_list_page.click_create_screening_cohort_by_outcode_btn()
    page.wait_for_timeout(3000)
    rlp_cohort_list_page.click_create_screening_cohort_save_btn()
    # expected error messages to be visible
    expect(page.get_by_text("Screening Cohort Name must be populated")).to_be_visible
    expect(
        page.get_by_text("Expected Attendance Rate must be between 0 and 100")
    ).to_be_visible
    expect(
        page.get_by_text("Default Screening Location must be populated")
    ).to_be_visible
    expect(page.get_by_text("Default Screening Unit must be populated")).to_be_visible


#### Test_44.1.1
@pytest.mark.cohortoutcode
@pytest.mark.parametrize("search_term", ["Cohort", "had"])
def test_outcode_search_feature_using_description(
    page: Page, rlp_cohort_list_page: CohortListPage, search_term: str
):
    """
    Test to validate the search feature using description
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    # search by description
    rlp_cohort_list_page.enter_screening_cohort_name_filter(search_term)
    filtered_values = page.locator("//tbody/tr/td[2]").all_text_contents()
    # Assert that each value contains "cohort"
    for text in filtered_values:
        assert (
            search_term.lower() in text.lower()
        ), f"Value '{text}' does not contain '{search_term}'."


#### Test_44.1.2
@pytest.mark.cohortoutcode
@pytest.mark.parametrize("search_term", ["Pound", "Park"])
def test_outcode_search_feature_using_location(
    page: Page, rlp_cohort_list_page: CohortListPage, search_term: str
):
    """
    Test to validate the search feature using location
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    # search by description
    rlp_cohort_list_page.enter_screening_location_filter(search_term)
    filtered_values = page.locator("//tbody/tr/td[4]").all_text_contents()
    # Assert that each value contains "cohort"
    for text in filtered_values:
        assert (
            search_term.lower() in text.lower()
        ), f"Value '{text}' does not contain '{search_term}'."


#### Test_44.1.3
@pytest.mark.cohortoutcode
@pytest.mark.parametrize("search_term", ["Bat", "Cap"])
def test_outcode_search_feature_using_unit_name(
    page: Page, rlp_cohort_list_page: CohortListPage, search_term: str
):
    """
    Test to validate the search feature using unit name
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    # search by description
    rlp_cohort_list_page.enter_screening_unit_filter(search_term)
    filtered_values = page.locator("//tbody/tr/td[5]").all_text_contents()
    # Assert that each value contains "cohort"
    for text in filtered_values:
        assert (
            search_term.lower() in text.lower()
        ), f"Value '{text}' does not contain '{search_term}'."


#### Test_44.1.4
@pytest.mark.cohortoutcode
@pytest.mark.parametrize("search_term", ["All", "Outcode", "Default"])
def test_outcode_search_feature_using_cohort_type(
    page: Page, rlp_cohort_list_page: CohortListPage, search_term: str
):
    """
    Test to validate the search feature using cohort type
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    # search by description
    ui_row_count_before = rlp_cohort_list_page.extract_cohort_paging_info()
    rlp_cohort_list_page.select_cohort_type_dropdown(search_term)
    filtered_values = page.locator("//tbody/tr/td[6]").all_text_contents()
    # Assert that each value contains "cohort"
    if search_term is "All":
        ui_row_count_after = rlp_cohort_list_page.extract_cohort_paging_info()
        assert ui_row_count_before == ui_row_count_after
    else:
        for text in filtered_values:
            assert (
                search_term.lower() in text.lower()
            ), f"Value '{text}' does not contain '{search_term}'."


## Test_47
@pytest.mark.cohortoutcode
def test_gp_practice_exist_outcode_does_not_exist(
    page: Page, rlp_cohort_list_page: CohortListPage
):
    """
    Test to verify when GP practice exists the outcode will be disabled
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    assert page.locator(
        "button:has-text('Create screening cohort by GP practice')"
    ).is_enabled(), "'Create screening cohort by GP practice' button is not enabled"
    assert page.locator(
        "button:has-text('Create screening cohort by outcode')"
    ).is_disabled(), "'Create screening cohort by outcode' button is enabled"

    info_icon = page.locator("button#addCohortByOutcodeButton + span")
    assert info_icon.get_attribute("data-toggle") == "tooltip"
    tooltip_text = info_icon.get_attribute("data-original-title")
    expected_text = "Cohorts have already been defined by GP practice/Sub practice, defining more cohorts by outcode is not permitted.<br>This is to prevent subjects from being included in the demand figures for multiple cohort types."
    assert tooltip_text == expected_text


#### Test_48
@pytest.mark.cohortoutcode
def test_gp_practice_does_not_exist_outcode_exist(
    page: Page, rlp_cohort_list_page: CohortListPage
):
    """
    Test to verify when outcode exists the GP practice will be disabled
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    assert page.locator(
        "button:has-text('Create screening cohort by GP practice')"
    ).is_disabled(), "'Create screening cohort by GP practice' button is enabled"
    assert page.locator(
        "button:has-text('Create screening cohort by outcode')"
    ).is_enabled(), "'Create screening cohort by outcode' button is not enabled"

    info_icon = page.locator("button#addCohortByPracticeButton + span")
    assert info_icon.get_attribute("data-toggle") == "tooltip"
    tooltip_text = info_icon.get_attribute("data-original-title")
    expected_text = "Cohorts have already been defined by outcode, defining more cohorts by GP practice/sub practice is not permitted.<br>This is to prevent subjects from being included in the demand figures for multiple cohort types."
    assert tooltip_text == expected_text
