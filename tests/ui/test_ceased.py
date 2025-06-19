"""
Ceased Tests: These tests cover the Ceased subject monitoring reports.
"""

import pytest
from pages.main_menu import MainMenuPage
from utils.user_tools import UserTools
from playwright.sync_api import Page, expect
from pages.monitoring_reports.ceased_unceased import CeasedUnceasedPage
from utils.screenshot_tool import ScreenshotTool


pytestmark = [pytest.mark.ceased]

# Fixtures


@pytest.fixture(autouse=True)
def log_in(user_tools: UserTools, page: Page) -> None:
    user_tools.user_login(page, "BSO User - BS1")


@pytest.fixture
def ceased_page(page: Page) -> CeasedUnceasedPage:
    MainMenuPage(page).select_menu_option(
        "Monitoring Reports", "Ceased/Unceased Subject List"
    )
    ceased_page = CeasedUnceasedPage(page)
    ceased_page.verify_header()
    return ceased_page


# Tests


def test_ceased_both_view_subject(page: Page, ceased_page: CeasedUnceasedPage) -> None:
    """
    Search Both on the Ceased/Unceased Subject List report
    """
    ceased_page.search_both()
    expect(page.locator("#subjectCeasingList")).to_be_visible()
    ScreenshotTool(page).take_screenshot("ceased_both_view_subject")


def test_ceased_view_subject(page: Page, ceased_page: CeasedUnceasedPage) -> None:
    """
    Select Ceased on the Ceased/Unceased Subject List report
    """
    ceased_page.search_unceased(False)
    ceased_page.search_ceased()
    expect(page.locator("#subjectCeasingList")).to_be_visible()
    ScreenshotTool(page).take_screenshot("ceased_view_subject")


def test_unceased_view_subject(page: Page, ceased_page: CeasedUnceasedPage) -> None:
    """
    Select Unceased on the Ceased/Unceased Subject List report
    """
    ceased_page.search_unceased()
    expect(page.locator("#subjectCeasingList")).to_be_visible()
    ScreenshotTool(page).take_screenshot("unceased_view_subject")


def test_both_date(page: Page, ceased_page: CeasedUnceasedPage) -> None:
    """
    Select Date from the Date Picker and Both on the Ceased/Unceased Subject List report
    """
    ceased_page.both_date()
    expect(page.locator("#subjectCeasingList")).to_be_visible()
    ScreenshotTool(page).take_screenshot("ceased_both_date")


def test_ceased_only_date(page: Page, ceased_page: CeasedUnceasedPage) -> None:
    """
    Select Date from the Date Picker and Ceased on the Ceased/Unceased Subject List report
    """
    ceased_page.ceased_only_date()
    expect(page.locator("#subjectCeasingList")).to_be_visible()
    ScreenshotTool(page).take_screenshot("ceased_only_date")


def test_unceased_only_date(page: Page, ceased_page: CeasedUnceasedPage) -> None:
    """
    Select Date from the Date Picker and Uneased on the Ceased/Unceased Subject List report
    """
    ceased_page.unceased_only_date()
    expect(page.locator("#subjectCeasingList")).to_be_visible()
    ScreenshotTool(page).take_screenshot("unceased_only_date")


def test_ceased_both_done(page: Page, ceased_page: CeasedUnceasedPage) -> None:
    """
    Select Both and All from the Done drop down menu on the Ceased/Unceased Subject List report
    """
    ceased_page.search_both()
    expect(page.locator("#subjectCeasingList")).to_be_visible()
    ceased_page.set_done_drop_down("All")
    ScreenshotTool(page).take_screenshot("ceased_both_done")


def test_ceased_both_nhs_number(page: Page, ceased_page: CeasedUnceasedPage) -> None:
    """
    Select Both and enter NHS Number in the filter field on the Ceased/Unceased Subject List report
    """
    ceased_page.search_both()
    expect(page.locator("#subjectCeasingList")).to_be_visible()
    nhs_number = page.locator(ceased_page.TABLE_FIRST_NHS_NUMBER).text_content()
    ceased_page.enter_nhs_number(nhs_number)
    expect(page.locator(ceased_page.TABLE_FIRST_NHS_NUMBER)).to_have_text(nhs_number)
    ScreenshotTool(page).take_screenshot("ceased_both_nhs_number")


def test_ceased_both_date_added_to_BSO(
    page: Page, ceased_page: CeasedUnceasedPage
) -> None:
    """
    Select Both and select sorting on Date added to BSO on the Ceased/Unceased Subject List report
    """
    ceased_page.search_both()
    expect(page.locator("#subjectCeasingList")).to_be_visible()
    ceased_page.sort_date_added_to_BSO()
    expect(page.locator("#columnHeaderNhsNumber").nth(1)).to_have_attribute(
        "aria-sort", "ascending"
    )
    ScreenshotTool(page).take_screenshot("ceased_both_date_added_to_BSO")


def test_ceased_both_born(page: Page, ceased_page: CeasedUnceasedPage) -> None:
    """
    Select Both and select sorting on Born on the Ceased/Unceased Subject List report
    """
    ceased_page.search_both()
    expect(page.locator("#subjectCeasingList")).to_be_visible()
    ceased_page.sort_born()
    expect(page.locator("#columnHeaderNhsNumber").nth(2)).to_have_attribute(
        "aria-sort", "ascending"
    )
    ScreenshotTool(page).take_screenshot("ceased_both_born")


def test_ceased_both_age_today(page: Page, ceased_page: CeasedUnceasedPage) -> None:
    """
    Select Both and select Age "In BSO Age Range" from the drop down menu on the Ceased/Unceased Subject List report
    """
    ceased_page.search_both()
    expect(page.locator("#subjectCeasingList")).to_be_visible()
    selected_age = "In BSO Age Range"
    ceased_page.table_filtered_by_age(selected_age)
    for age in ceased_page.AGE_OPTIONS:
        if age != selected_age:
            expect(page.locator("tbody")).not_to_contain_text(age)
    ScreenshotTool(page).take_screenshot("ceased_both_age_today")


def test_ceased_both_done_age_today(
    page: Page, ceased_page: CeasedUnceasedPage
) -> None:
    """
    Select Both, select All from the Done drop down menu and select Age "In BSO Age Range" from the drop down menu on the Ceased/Unceased Subject List report
    """
    ceased_page.search_both()
    expect(page.locator("#subjectCeasingList")).to_be_visible()
    ceased_page.set_done_drop_down("All")
    selected_age = "In BSO Age Range"
    ceased_page.table_filtered_by_age(selected_age)
    for age in ceased_page.AGE_OPTIONS:
        if age != selected_age:
            expect(page.locator("tbody")).not_to_contain_text(age)
    ScreenshotTool(page).take_screenshot("ceased_both_done_age_today")


def test_ceased_both_done_all_age_today(
    page: Page, ceased_page: CeasedUnceasedPage
) -> None:
    """
    Select Both, select All from the Done drop down menu and select Age "All" from the drop down menu on the Ceased/Unceased Subject List report
    """
    ceased_page.search_both()
    expect(page.locator("#subjectCeasingList")).to_be_visible()
    ceased_page.set_done_drop_down("All")
    selected_age = "In BSO Age Range"
    ceased_page.table_filtered_by_age(selected_age)
    for age in ceased_page.AGE_OPTIONS:
        if age != selected_age:
            expect(page.locator("tbody")).not_to_contain_text(age)
    ScreenshotTool(page).take_screenshot("ceased_both_done_all_age_today")


def test_ceased_both_family_name(page: Page, ceased_page: CeasedUnceasedPage) -> None:
    """
    Select Both and enter Family Name in the filter field on the Ceased/Unceased Subject List report
    """
    ceased_page.search_both()
    expect(page.locator("#subjectCeasingList")).to_be_visible()
    family_name = page.locator(ceased_page.TABLE_FIRST_FAMILY_NAME).text_content()
    ceased_page.enter_family_name(family_name)
    expect(page.locator(ceased_page.TABLE_FIRST_FAMILY_NAME)).to_have_text(family_name)
    ScreenshotTool(page).take_screenshot("ceased_both_family_name")


def test_ceased_first_name(page: Page, ceased_page: CeasedUnceasedPage) -> None:
    """
    Select Both and enter First Given Name in the filter field on the Ceased/Unceased Subject List report
    """
    ceased_page.search_both()
    expect(page.locator("#subjectCeasingList")).to_be_visible()
    first_name = page.locator(ceased_page.TABLE_FIRST_FIRST_NAME).text_content()
    ceased_page.enter_first_name(first_name)
    expect(page.locator(ceased_page.TABLE_FIRST_FIRST_NAME)).to_have_text(first_name)
    ScreenshotTool(page).take_screenshot("ceased_first_name")


def test_ceased_both_date_ceased(page: Page, ceased_page: CeasedUnceasedPage) -> None:
    """
    Select Both, All from the Done drop down menu and select sorting on Date Ceased on the Ceased/Unceased Subject List report
    """
    ceased_page.search_both()
    expect(page.locator("#subjectCeasingList")).to_be_visible()
    ceased_page.set_done_drop_down("All")
    ceased_page.sort_date_ceased()
    expect(page.locator("#columnHeaderDateCeased")).to_have_attribute(
        "aria-sort", "ascending"
    )
    ScreenshotTool(page).take_screenshot("ceased_both_date_ceased")


def test_ceased_both_date_unceased(page: Page, ceased_page: CeasedUnceasedPage) -> None:
    """
    Select Both, All from the Done drop down menu and select sorting on Date Unceased on the Ceased/Unceased Subject List report
    """
    ceased_page.search_both()
    expect(page.locator("#subjectCeasingList")).to_be_visible()
    ceased_page.set_done_drop_down("All")
    ceased_page.sort_date_unceased()
    expect(page.locator("#columnHeaderDateUnceased")).to_have_attribute(
        "aria-sort", "ascending"
    )
    ScreenshotTool(page).take_screenshot("ceased_both_date_unceased")


def test_ceased_both_reason(page: Page, ceased_page: CeasedUnceasedPage) -> None:
    """
    Select Both and Reason "Informed Choice" on the Ceased/Unceased Subject List report
    """
    ceased_page.search_both()
    expect(page.locator("#subjectCeasingList")).to_be_visible()
    selected_reason = "Informed Choice"
    ceased_page.reason_selected(selected_reason)
    for reason in ceased_page.REASON_OPTIONS:
        if reason != selected_reason:
            expect(page.locator("tbody")).not_to_contain_text(reason)
    ScreenshotTool(page).take_screenshot("ceased_both_reason")
