import playwright
import pytest
from pages.main_menu import MainMenuPage
from playwright.sync_api import expect, Page, Playwright
from pages.ni_ri_sp_batch_page import NiRiSpBatchPage
from utils.user_tools import UserTools
from utils.screenshot_tool import ScreenshotTool


# TC-1
@pytest.mark.ni
def test_ni_bso_user_cannot_create_ri_sp_batch_when_yob_parameter_not_set(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """This test verifies that a BSS NI BSO user is unable to create an RI/SP Batch by Year of Birth
    when the corresponding BSO parameter 'RI/SP Batch by Year of Birth' is not set.
    """
    # Logged into BSO3 as user3(PMA) and select 'Create RI/SP Batch' from the 'batch management' dropdown
    UserTools().user_login(page, "Ni Only BSO User3 - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    ni_ri_sp_batch_page.enter_bso_batch_id("PMA106376K")
    ni_ri_sp_batch_page.enter_date_for_selection(5)
    ni_ri_sp_batch_page.enter_include_year_of_birth_from("")
    ni_ri_sp_batch_page.enter_include_year_of_birth_to("")
    ni_ri_sp_batch_page.click_count_button()
    # Validating the error message
    ni_ri_sp_batch_page.assert_text_visible("Earliest Birth Year must be populated")
    ni_ri_sp_batch_page.assert_text_visible("Latest Birth Year must be populated")
    ScreenshotTool(page).take_screenshot(
        "user_cannot_create_ri_sp_batch_when_yob_parameter_not_set"
    )


# TC-2.1
@pytest.mark.ni
def test_eng_bso_user_cannot_create_ri_sp_batch_by_year_of_birth(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """Verify 'ENG' user attempt to create ri/sp batch by YOB."""
    UserTools().user_login(page, "BSO User1 - BS1")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    ni_ri_sp_batch_page.enter_bso_batch_id("BA1542274F")
    ni_ri_sp_batch_page.enter_date_for_selection(5)
    ni_ri_sp_batch_page.enter_include_year_of_birth_from("1955")
    ni_ri_sp_batch_page.enter_include_year_of_birth_to("1975")
    ni_ri_sp_batch_page.click_count_button()
    ni_ri_sp_batch_page.assert_text_visible("Invalid format for BSO Batch ID")
    ScreenshotTool(page).take_screenshot(
        "eng_bso_user_cannot_create_ri_sp_batch_by_yob"
    )


# TC-2.2
@pytest.mark.ni
def test_ni_bso_user_is_able_to_create_ri_sp_batch_by_year_of_birth(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """Verify ni bso user is able to create ri/sp batch by YOB."""
    UserTools().user_login(page, "Ni Only BSO User3 - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    ni_ri_sp_batch_page.enter_bso_batch_id("PMA106376K")
    ni_ri_sp_batch_page.enter_date_for_selection(5)
    ni_ri_sp_batch_page.click_count_button()
    ni_ri_sp_batch_page.assert_page_header("Amend RI/SP Batch by Year of Birth")
    ScreenshotTool(page).take_screenshot(
        "ni_bso_user_able_to_create_ri_sp_batch_by_yob"
    )
    page.locator("#deleteButton").click()
    page.wait_for_timeout(3000)
    page.locator("#confirmButtonInDeletePopupText").click()


# TC-3.1
@pytest.mark.ni
def test_ni_bso_batch_id_not_unique_warning(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """This test verifies that a BSS NI BSO user sees appropriate warnings
    when entering an invalid BSO Batch ID that is not unique.
    """
    # Logged into BSO3 as user3(PMA) and select 'Create RI/SP Batch' from the 'batch management' dropdown
    UserTools().user_login(page, "Ni Only BSO User3 - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    ni_ri_sp_batch_page.validate_batch_id_error(
        batch_id="PMA999582G",
        expected_error="This Batch ID already exists on the system.",
    )
    ScreenshotTool(page).take_screenshot("batch_id_already_exists_on_the_system")


# TC-3.2
@pytest.mark.ni
def test_ni_bso_batch_id_invalid_format_warning(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """This test verifies that a BSS NI BSO user sees appropriate warnings
    when entering an invalid BSO Batch ID that is incorrect format.
    """
    # Logged into BSO3 as user3(PMA) and select 'Create RI/SP Batch' from the 'batch management' dropdown
    UserTools().user_login(page, "Ni Only BSO User3 - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    ni_ri_sp_batch_page.validate_batch_id_error(
        batch_id="123INVALID", expected_error="Invalid format for BSO Batch ID"
    )
    ScreenshotTool(page).take_screenshot("batch_id_invalid_format_warning")


# TC-3.3
@pytest.mark.ni
def test_ni_bso_batch_id_check_digit_warning(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """This test verifies that a BSS NI BSO user sees appropriate warnings
    when entering an invalid BSO Batch ID that is Check digit is incorrect.
    """
    # Logged into BSO3 as user3(PMA) and select 'Create RI/SP Batch' from the 'batch management' dropdown
    UserTools().user_login(page, "Ni Only BSO User3 - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    ni_ri_sp_batch_page.validate_batch_id_error(
        batch_id="PMA9168656", expected_error="Invalid format for BSO Batch ID"
    )
    ScreenshotTool(page).take_screenshot("batch_id_incorrect_check_digit_warning")


# TC-4.1
@pytest.mark.ni
def test_ni_date_for_selection_today_shows_warning(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """Verifies that a warning is shown when 'Date for Selection' is set to today's date."""
    # Logged into BSO3 as user3(PMA) and select 'Create RI/SP Batch' from the 'batch management' dropdown
    UserTools().user_login(page, "Ni Only BSO User3 - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    ni_ri_sp_batch_page.enter_bso_batch_id("PMA916865R")
    ni_ri_sp_batch_page.enter_date_for_selection(0)
    ni_ri_sp_batch_page.click_count_button()
    ni_ri_sp_batch_page.assert_text_visible("Date for Selection must be in the future")
    ScreenshotTool(page).take_screenshot("batch_id_date_for_selection_today_warning")


# TC-4.2
@pytest.mark.ni
def test_ni_date_for_selection_in_past_shows_warning(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """Verifies that a warning is shown when 'Date for Selection' is set to past date."""
    # Logged into BSO3 as user3(PMA) and select 'Create RI/SP Batch' from the 'batch management' dropdown
    UserTools().user_login(page, "Ni Only BSO User3 - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    ni_ri_sp_batch_page.enter_bso_batch_id("PMA916865R")
    ni_ri_sp_batch_page.enter_date_for_selection(-5)
    ni_ri_sp_batch_page.click_count_button()
    ni_ri_sp_batch_page.assert_text_visible("Date for Selection must be in the future")
    ScreenshotTool(page).take_screenshot(
        "batch_id_date_for_selection_must_be_in_the_future_warning"
    )


# TC-5.1
@pytest.mark.ni
def test_ni_bso_user_receives_warning_for_invalid_yob_range_1954_1975(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """Verify that a warning is shown when YOB From = 1954 and To = 1975 (71 to 50 years ago)."""
    UserTools().user_login(page, "Ni Only BSO User3 - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    ni_ri_sp_batch_page.enter_year_range_and_count("1954", "1975")
    ni_ri_sp_batch_page.assert_text_visible(
        "Earliest Birth Year must be between 1955 and 1975"
    )
    ScreenshotTool(page).take_screenshot(
        "Earliest_warning_for_invalid_yob_range_1954_1975"
    )


# TC-5.2
@pytest.mark.ni
def test_ni_bso_user_receives_warning_for_invalid_yob_range_1954_1974(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """Verify that a warning is shown when YOB From = 1954 and To = 1974 (71 to 51 years ago)."""
    UserTools().user_login(page, "Ni Only BSO User3 - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    ni_ri_sp_batch_page.enter_year_range_and_count("1954", "1974")
    ni_ri_sp_batch_page.assert_text_visible(
        "Earliest Birth Year must be between 1955 and 1975"
    )
    ScreenshotTool(page).take_screenshot(
        "Earliest_warning_for_invalid_yob_range_1954_1974"
    )


# TC-6.1
@pytest.mark.ni
def test_ni_bso_user_receives_warning_for_invalid_yob_range_1955_1976(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """Verify that a warning is shown when YOB From = 1955 and To = 1976 (70 to 49 years ago)."""
    UserTools().user_login(page, "Ni Only BSO User3 - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    ni_ri_sp_batch_page.enter_year_range_and_count("1955", "1976")
    ni_ri_sp_batch_page.assert_text_visible(
        "Latest Birth Year must be between 1955 and 1975"
    )
    ScreenshotTool(page).take_screenshot(
        "Latest_warning_for_invalid_yob_range_1955_1976"
    )


# TC-6.2
@pytest.mark.ni
def test_ni_bso_user_receives_warning_for_invalid_yob_range_1956_1976(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """Verify that a warning is shown when YOB From = 1956 and To = 1976 (69 to 49 years ago)."""
    UserTools().user_login(page, "Ni Only BSO User3 - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    ni_ri_sp_batch_page.enter_year_range_and_count("1956", "1976")
    ni_ri_sp_batch_page.assert_text_visible(
        "Latest Birth Year must be between 1955 and 1975"
    )
    ScreenshotTool(page).take_screenshot(
        "Latest_warning_for_invalid_yob_range_1956_1976"
    )


# TC-7
@pytest.mark.ni
@pytest.mark.nitest
def test_ni_bso_user_receives_warning_for_invalid_yob_range_1955_1954(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """Verify that a warning is shown when YOB From = 1955 and To = 1954 (70 to 69 years ago)."""
    UserTools().user_login(page, "Ni Only BSO User3 - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    ni_ri_sp_batch_page.enter_year_range_and_count("1955", "1954")
    ni_ri_sp_batch_page.assert_text_visible(
        "Earliest Birth Year must not be after the Latest Birth Year"
    )
    ni_ri_sp_batch_page.assert_text_visible(
        "Latest Birth Year must be between 1955 and 1975"
    )
    ScreenshotTool(page).take_screenshot("warning_for_invalid_yob_range_1955_1954")


# TC-8
@pytest.mark.ni
def test_ni_bso_user_receives_warning_for_invalid_month_of_birth_range(
    page: Page, ni_ri_sp_batch_page: NiRiSpBatchPage
) -> None:
    """Verify that a warning is shown when 'Include Month Of Birth' value is set to 13."""
    UserTools().user_login(page, "Ni Only BSO User3 - BS3")
    MainMenuPage(page).select_menu_option("Batch Management", "Create RI/SP Batch")
    ni_ri_sp_batch_page.assert_page_header("Create RI/SP Batch by Year of Birth")
    ni_ri_sp_batch_page.enter_bso_batch_id("PMA916865R")
    ni_ri_sp_batch_page.enter_date_for_selection(5)
    ni_ri_sp_batch_page.enter_include_month_of_birth_to("13")
    ni_ri_sp_batch_page.click_count_button()
    ni_ri_sp_batch_page.assert_text_visible(
        "Latest Birth Month must be between 1 and 12"
    )
    ScreenshotTool(page).take_screenshot("warning_for_invalid_month_of_birth_range")
