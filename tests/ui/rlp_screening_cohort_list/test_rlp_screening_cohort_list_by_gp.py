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
@pytest.mark.cohortgp
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
@pytest.mark.cohortgp
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


## Test_01
## Test_02
@pytest.mark.cohortgp
def test_only_default_BSO_Cohort_visible(
    page: Page, rlp_cohort_list_page: CohortListPage
) -> None:
    """
    User Selects 'Screening Cohorts' from the drop down list,
    User has no saved Cohorts,
    'Screening Cohort List' Screen is displayed correctly, with only the default BSO Cohort visible
    """
    # Logged into BSS_SO2_User2 and select screening cohort list from the roundplanning drop down
    UserTools().user_login(page, "Read Only BSO User2 - BS2")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    expect(page.get_by_text("Screening cohort list", exact=True)).to_be_visible()
    paging_info = rlp_cohort_list_page.extract_cohort_paging_info()
    assert paging_info == 1
    cell_data = page.locator("//tbody/tr/td[6]").inner_text()
    assert cell_data == "Default"


## Test_03
@pytest.mark.cohortgp
def test_paging_of_cohort_list(
    page: Page, rlp_cohort_list_page: CohortListPage, db_util
) -> None:
    """
    Test to compare the UI cohort row count and db row count
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    # Checking the paging info
    ui_row_count = rlp_cohort_list_page.extract_cohort_paging_info()
    db_row_count = rlp_cohort_list_page.screening_cohorts_count_in_db(db_util)
    assert db_row_count == int(ui_row_count)


## Test_04
@pytest.mark.cohortgp
def test_defaults_are_set_and_displayed_correctly(
    page: Page, rlp_cohort_list_page: CohortListPage
) -> None:
    """
    Test to verify the cohort defaults are displayed correctly
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")

    # Create Screening Cohort screen is displayed
    rlp_cohort_list_page.click_create_screening_cohort_by_gp_practice_btn()
    page.wait_for_timeout(3000)
    expect(page.get_by_text("Create Screening Cohort")).to_be_visible()

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


## Test_05
@pytest.mark.cohortgp
def test_invoke_cancel_btn_return_to_screening_cohort_list(
    page: Page, rlp_cohort_list_page: CohortListPage
) -> None:
    """
    Test to invoke cancel cohort button and retuen to the screening cohort list page
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")

    # Create Screening Cohort screen is displayed
    rlp_cohort_list_page.click_create_screening_cohort_by_gp_practice_btn()
    page.wait_for_timeout(3000)

    rlp_cohort_list_page.click_on_cancel_creating_screening_cohort()
    page.wait_for_timeout(5000)
    expect(page.get_by_text("Screening cohort list", exact=True)).to_be_visible()


## Test_06
@pytest.mark.cohortgp
@pytest.mark.parametrize("input_length", [3, 100])
def test_create_screening_cohort_valid_data(
    page: Page, rlp_cohort_list_page: CohortListPage, input_length
) -> None:
    """User enters valid data into Screening Cohort field"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    # Test data
    cohort_name = generate_random_string(
        input_length
    )  # this method will generate string between 3 & 100 which will be unique each time
    location_name = "Aldi - Caldecott County Retail Park"
    # checking uniqueness of the name
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    expect(page.locator("td.dataTables_empty")).to_be_visible()
    # creating cohort using create cohort method
    rlp_cohort_list_page.create_cohort(cohort_name, location_name)
    # filtering name and storing in filterd_name
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    filterd_name = page.locator("//tr//td[2]").text_content()
    assert cohort_name == filterd_name


## Test_06 negative field data validation
@pytest.mark.cohortgp
@pytest.mark.parametrize(
    "cohort_name, expected_message",
    [
        ("$%&@", "Screening Cohort Name contains invalid characters"),
        ("cd", "The Screening Cohort Name you entered is too short"),
        ("     ", "Screening Cohort Name must be populated"),
        ("Hadley", "Screening Cohort Name is already in use by another cohort"),
    ],
)
def test_try_to_create_screening_cohort_with_invalid_data(
    page: Page, rlp_cohort_list_page: CohortListPage, cohort_name, expected_message
):
    """
    Negative test - User enters invalid data into Screening Cohort field
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    # try to create cohort using create cohort method with invalid data
    rlp_cohort_list_page.click_create_screening_cohort_by_gp_practice_btn()
    page.wait_for_timeout(3000)
    rlp_cohort_list_page.enter_screening_cohort_name_field(cohort_name)
    rlp_cohort_list_page.enter_expected_attendance_rate("25")
    rlp_cohort_list_page.select_default_screening_location_dropdown(
        "Aldi - Caldecott County Retail Park"
    )
    rlp_cohort_list_page.select_default_screening_unit_dropdown("Batman")
    rlp_cohort_list_page.click_create_screening_cohort_save_btn()

    # Assert that the correct error message is displayed based on invalid_data
    expect(page.get_by_text(expected_message)).to_be_visible()


## Test_07 positive field data validation for Expected Attendance Rate
@pytest.mark.cohortgp
@pytest.mark.parametrize("input_value", [0, 100])
def test_expected_attendance_rate_valid_data(
    page: Page, rlp_cohort_list_page: CohortListPage, input_value
) -> None:
    """
    User enters valid data in the Expected Attendance Rate (%) field
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    cohort_name = f"cohort_name-{datetime.now()}"
    rlp_cohort_list_page.click_create_screening_cohort_by_gp_practice_btn()
    page.wait_for_timeout(3000)
    rlp_cohort_list_page.enter_screening_cohort_name_field(cohort_name)
    rlp_cohort_list_page.enter_expected_attendance_rate(str(input_value))
    rlp_cohort_list_page.select_default_screening_location_dropdown(
        "Aldi - Caldecott County Retail Park"
    )
    rlp_cohort_list_page.select_default_screening_unit_dropdown("Batman")
    rlp_cohort_list_page.click_create_screening_cohort_save_btn()

    # filtering name and storing in filterd_name
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    assert float(page.locator("input#uptakePercentage").input_value()) == input_value


#### Test_07 negative test for Expected Attendance Rate field
@pytest.mark.cohortgp
@pytest.mark.parametrize(
    "attendance_rate, expected_message",
    [
        ("cd", "Invalid value"),
        ("     ", "Expected Attendance Rate must be between 0 and 100"),
    ],
)
def test_expected_attendance_rate_invalid_data(
    page: Page, rlp_cohort_list_page: CohortListPage, attendance_rate, expected_message
):
    """Negative test - User enters data in the Expected Attendance Rate (%) field - Non integer value and Null"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")

    # try to create cohort using invalid attendance rate
    cohort_name = f"cohort_name-{datetime.now()}"
    rlp_cohort_list_page.click_create_screening_cohort_by_gp_practice_btn()
    page.wait_for_timeout(3000)
    rlp_cohort_list_page.enter_screening_cohort_name_field(cohort_name)
    rlp_cohort_list_page.enter_expected_attendance_rate(attendance_rate)
    rlp_cohort_list_page.select_default_screening_location_dropdown(
        "Aldi - Caldecott County Retail Park"
    )
    rlp_cohort_list_page.select_default_screening_unit_dropdown("Batman")
    rlp_cohort_list_page.click_create_screening_cohort_save_btn()
    # Assert that the correct error message is displayed based on invalid_data
    expect(page.get_by_text(expected_message)).to_be_visible()


#### Test_08
@pytest.mark.cohortgp
def test_default_location_dropdown(page: Page, rlp_cohort_list_page: CohortListPage):
    """
    The correct list of Locations available to this user in this BSO, are displayed correctly
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    rlp_cohort_list_page.click_create_screening_cohort_by_gp_practice_btn()
    page.wait_for_timeout(3000)
    # extracting the drop down location count
    rlp_cohort_list_page.select_default_screening_location_dropdown(None)
    dropdown_count = rlp_cohort_list_page.number_of_location_dropdown_count()

    MainMenuPage(page).select_menu_option("Round Planning", "Screening Location List")
    # extracting the location count
    location_list_count = rlp_cohort_list_page.extract_location_paging_list_count()
    assert dropdown_count == location_list_count


#### Test_09
@pytest.mark.cohortgp
def test_default_unit_dropdown(page: Page, rlp_cohort_list_page: CohortListPage):
    """
    The correct list of units available to this user in this BSO, are displayed correctly
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    rlp_cohort_list_page.click_create_screening_cohort_by_gp_practice_btn()
    page.wait_for_timeout(3000)
    # extracting the drop down location count
    rlp_cohort_list_page.select_default_screening_unit_dropdown(None)
    dropdown_count = rlp_cohort_list_page.number_of_unit_dropdown_count()

    # Logged into BSS_SO1 location list
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Unit List")
    # extracting the location count
    unit_list_count = rlp_cohort_list_page.extract_paging_unit_list_count_active_only()
    assert dropdown_count == unit_list_count


#### Test_10.1.2, 10.2.1
@pytest.mark.cohortgp
def test_added_gp_practices_are_visible(
    page: Page, rlp_cohort_list_page: CohortListPage
):
    """
    Test to add gp practices and covers negative test of adding the same gp practice
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    rlp_cohort_list_page.click_create_screening_cohort_by_gp_practice_btn()
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
    included_gp_practices = page.locator(
        "//table[@id='practicesToIncludeList']//tr//td[2]"
    ).count()
    assert included_gp_practices == 2
    # try including the already added gp_practices - negative test
    rlp_cohort_list_page.click_select_gp_practices_btn()
    rlp_cohort_list_page.enter_gp_code_field("A00002")
    rlp_cohort_list_page.verify_add_btn_gp_practices_not_to_be_present()


#### Test_11
@pytest.mark.cohortgp
def test_gp_practices_removed_from_included_gp_practices(
    page: Page, rlp_cohort_list_page: CohortListPage
):
    """
    User add and remove the gp practices
    """
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    rlp_cohort_list_page.click_create_screening_cohort_by_gp_practice_btn()
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
    rlp_cohort_list_page.click_select_gp_practices_btn()
    rlp_cohort_list_page.enter_gp_code_field("A00004")
    rlp_cohort_list_page.click_add_btn_gp_practices_to_include()
    rlp_cohort_list_page.click_done_btn_gp_practices_include_popup()
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
    rlp_cohort_list_page.click_remove_button_by_gp_code("A00004")
    removed_included_gp_practices = page.locator(
        "//table[@id='practicesToIncludeList']//tr//td[2]"
    ).count()
    assert removed_included_gp_practices == 0


#### Test_12
@pytest.mark.cohortgp
def test_click_save_without_filling_all_mandatory_fields(
    page: Page, rlp_cohort_list_page: CohortListPage
):
    """User invoke save button without filling all the mandatory fields and validate the response"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")

    rlp_cohort_list_page.click_create_screening_cohort_by_gp_practice_btn()
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


#### Test_13
@pytest.mark.cohortgp
def test_another_user_logs_into_BS_select(
    page: Page, rlp_cohort_list_page: CohortListPage, context
):
    """Other Users are not able to create Cohort with same details of other existing Cohort within the same BSO, failing validation"""
    # Logged into BSS_SO1
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    # creating cohort using method with hardcoded attendence and screening unit
    cohort_name = f"cohort_name-{datetime.now()}"
    location_name = "Poundland Car Park - Alberta Retail Park"
    rlp_cohort_list_page.create_cohort(cohort_name, location_name)
    context.clear_cookies()

    # Logged into BSS_SO1_User2
    UserTools().user_login(page, "BSO User2 - BS1")
    MainMenuPage(page).select_menu_option("Round Planning", "Screening Cohort List")
    # User2 is filtering the cohort by name which is creatd by User1
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    filterd_name = rlp_cohort_list_page.value_of_filtered_cohort_name()
    assert cohort_name == filterd_name
    # User2 tries to create cohort with same detailes test should fail
    rlp_cohort_list_page.create_cohort(cohort_name, location_name)
    expect(
        page.get_by_text("Screening Cohort Name is already in use by another cohort")
    ).to_be_visible()


## Test_47
@pytest.mark.cohortgp
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
@pytest.mark.cohortgp
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
