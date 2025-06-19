"""
SSPI Tests: These tests cover the SSPI warning reports.
"""

import pytest
import csv
from pages.main_menu import MainMenuPage
from utils.nhs_number_tools import NHSNumberTools
from utils.user_tools import UserTools
from utils.table_utils import TableUtils
from playwright.sync_api import Page, expect
from pages.monitoring_reports.sspi_update_warnings_action import (
    SSPIUpdateWarningsActionPage,
)
from pages.monitoring_reports.sspi_update_warnings_information import (
    SSPIUpdateWarningsInformationPage,
)
from utils.screenshot_tool import ScreenshotTool


pytestmark = [pytest.mark.sspi]

# Fixtures


@pytest.fixture(autouse=True)
def log_in(user_tools: UserTools, page: Page) -> None:
    user_tools.user_login(page, "BSO User - BS1")


@pytest.fixture
def action_page(page: Page) -> SSPIUpdateWarningsActionPage:
    MainMenuPage(page).select_menu_option(
        "Monitoring Reports", "SSPI Update Warnings - Action"
    )
    action_page = SSPIUpdateWarningsActionPage(page)
    action_page.verify_header()
    return action_page


@pytest.fixture
def information_page(page: Page) -> SSPIUpdateWarningsInformationPage:
    MainMenuPage(page).select_menu_option(
        "Monitoring Reports", "SSPI Update Warnings - Information"
    )
    information_page = SSPIUpdateWarningsInformationPage(page)
    information_page.verify_header()
    return information_page


# Tests


def test_sspi_update_warnings_action_csv_download(
    page: Page, action_page: SSPIUpdateWarningsActionPage
) -> None:
    """
    Select Done from the drop down menu on the SSPI Update Warnings Action report and click the Download to CSV button to download the file
    """
    action_page.set_done_drop_down("All")
    downloaded_file = action_page.download_csv()
    warning_table = TableUtils(page, action_page.TABLE_ID)
    row_number = 0
    with open(downloaded_file) as file:
        csv_file = csv.DictReader(file)
        for lines in csv_file:
            expect(warning_table.pick_row(row_number)).to_contain_text(
                NHSNumberTools().spaced_nhs_number(lines["NHS Number"])
            )
            row_number += 1

            if row_number >= warning_table.get_row_count():
                # Stop if we have processed all rows in the table visible on the UI
                break


def test_sspi_update_warnings_action_done(
    page: Page, action_page: SSPIUpdateWarningsActionPage
) -> None:
    """
    Select Done from the drop down menu on the SSPI Update Warnings Action report
    """
    action_page.set_done_drop_down("All")
    ScreenshotTool(page).take_screenshot("sspi_update_warnings_action_done")


def test_sspi_update_warnings_action_nhs_number(
    page: Page, action_page: SSPIUpdateWarningsActionPage
) -> None:
    """
    Enter NHS Number in the filter field on the SSPI Update Warnings Action report
    """
    nhs_number = page.locator(action_page.TABLE_FIRST_NHS_NUMBER).text_content()
    action_page.enter_nhs_number(nhs_number)
    expect(page.locator(action_page.TABLE_FIRST_NHS_NUMBER)).to_have_text(nhs_number)
    ScreenshotTool(page).take_screenshot("sspi_update_warnings_action_nhs_number")


def test_sspi_update_warnings_action_family_name(
    page: Page, action_page: SSPIUpdateWarningsActionPage
) -> None:
    """
    Enter Family Name in the filter field on the SSPI Update Warnings Action report
    """
    family_name = page.locator(action_page.TABLE_FIRST_FAMILY_NAME).text_content()
    action_page.enter_family_name(family_name)
    expect(page.locator(action_page.TABLE_FIRST_FAMILY_NAME)).to_have_text(family_name)
    ScreenshotTool(page).take_screenshot("sspi_update_warnings_action_family_name")


def test_sspi_update_warnings_action_first_name(
    page: Page, action_page: SSPIUpdateWarningsActionPage
) -> None:
    """
    Enter First Given Name in the filter field on the SSPI Update Warnings Action report
    """
    first_name = page.locator(action_page.TABLE_FIRST_FIRST_NAME).text_content()
    action_page.enter_first_name(first_name)
    expect(page.locator(action_page.TABLE_FIRST_FIRST_NAME)).to_have_text(first_name)
    ScreenshotTool(page).take_screenshot("sspi_update_warnings_action_first_name")


def test_sspi_update_warnings_action_age(
    page: Page, action_page: SSPIUpdateWarningsActionPage
) -> None:
    """
    Select Age "Under 80" from the drop down menu on the SSPI Update Warnings Action report
    """
    selected_age = "Under 80"
    action_page.table_filtered_by_age(selected_age)
    for age in action_page.AGE_OPTIONS:
        if age != selected_age:
            expect(page.locator("tbody")).not_to_contain_text(age)
    ScreenshotTool(page).take_screenshot("sspi_update_warnings_action_age")


def test_sspi_update_warnings_action_received(
    page: Page, action_page: SSPIUpdateWarningsActionPage
) -> None:
    """
    Select the sorting Received on the SSPI Update Warnings Action report
    """
    action_page.sort_received()
    expect(page.locator("#columnHeaderReceived")).to_have_attribute(
        "aria-sort", "ascending"
    )
    ScreenshotTool(page).take_screenshot("sspi_update_warnings_action_received")


def test_sspi_update_warnings_action_event(
    page: Page, action_page: SSPIUpdateWarningsActionPage
) -> None:
    """
    Select Event "Date of death set" on the SSPI Update Warnings Action report
    """
    selected_reason = "Date of death set"
    action_page.event_selected(selected_reason)
    for reason in action_page.REASON_OPTIONS:
        if reason != selected_reason:
            expect(page.locator("tbody")).not_to_contain_text(reason)
    ScreenshotTool(page).take_screenshot("sspi_update_warnings_action_event")


def test_sspi_update_warnings_action_warning(
    page: Page, action_page: SSPIUpdateWarningsActionPage
) -> None:
    """
    Select Warning "Subject has open episode" on the SSPI Update Warnings Action report
    """
    selected_warning = "Subject has open episode"
    action_page.warning_selected(selected_warning)
    for warning in action_page.WARNING_OPTIONS:
        if warning != selected_warning:
            expect(page.locator("tbody")).not_to_contain_text(warning)
    ScreenshotTool(page).take_screenshot("sspi_update_warnings_action_warning")


def test_sspi_update_warnings_action_add_info(
    page: Page, action_page: SSPIUpdateWarningsActionPage
) -> None:
    """
    Select the sorting Add Information on the SSPI Update Warnings Action report
    """
    action_page.sort_add_info()
    expect(page.locator("#columnHeaderAdditionalInfo")).to_have_attribute(
        "aria-sort", "ascending"
    )
    ScreenshotTool(page).take_screenshot("sspi_update_warnings_action_add_info")


def test_sspi_update_warnings_information_csv_download(
    page: Page, information_page: SSPIUpdateWarningsInformationPage
) -> None:
    """
    Select Done from the drop down menu on the SSPI Update Warnings Information report and click the Download to CSV button to download the file
    """
    information_page.set_done_drop_down("All")
    downloaded_file = information_page.download_csv()
    warning_table = TableUtils(page, information_page.TABLE_ID)
    row_number = 0
    with open(downloaded_file) as file:
        csv_file = csv.DictReader(file)
        for lines in csv_file:
            expect(warning_table.pick_row(row_number)).to_contain_text(
                NHSNumberTools().spaced_nhs_number(lines["NHS Number"])
            )
            row_number += 1

            if row_number >= warning_table.get_row_count():
                # Stop if we have processed all rows in the table visible on the UI
                break


def test_sspi_update_warnings_information_done(
    page: Page, information_page: SSPIUpdateWarningsInformationPage
) -> None:
    """
    Select Done from the drop down menu on the SSPI Update Warnings Information report
    """
    information_page.set_done_drop_down("All")
    ScreenshotTool(page).take_screenshot("sspi_update_warnings_information_done")


def test_sspi_update_warnings_information_nhs_number(
    page: Page, information_page: SSPIUpdateWarningsInformationPage
) -> None:
    """
    Enter NHS Number in the filter field on the SSPI Update Warnings Information report
    """
    nhs_number = page.locator(information_page.TABLE_FIRST_NHS_NUMBER).text_content()
    information_page.enter_nhs_number(nhs_number)
    expect(page.locator(information_page.TABLE_FIRST_NHS_NUMBER)).to_have_text(
        nhs_number
    )
    ScreenshotTool(page).take_screenshot("sspi_update_warnings_information_nhs_number")


def test_sspi_update_warnings_information_family_name(
    page: Page, information_page: SSPIUpdateWarningsInformationPage
) -> None:
    """
    Enter Family Name in the filter field on the SSPI Update Warnings Information report
    """
    family_name = page.locator(information_page.TABLE_FIRST_FAMILY_NAME).text_content()
    information_page.enter_family_name(family_name)
    expect(page.locator(information_page.TABLE_FIRST_FAMILY_NAME)).to_have_text(
        family_name
    )
    ScreenshotTool(page).take_screenshot("sspi_update_warnings_information_family_name")


def test_sspi_update_warnings_information_first_name(
    page: Page, information_page: SSPIUpdateWarningsInformationPage
) -> None:
    """
    Enter First Name in the filter field on the SSPI Update Warnings Information report
    """
    first_name = page.locator(information_page.TABLE_FIRST_FIRST_NAME).text_content()
    information_page.enter_first_name(first_name)
    expect(page.locator(information_page.TABLE_FIRST_FIRST_NAME)).to_have_text(
        first_name
    )
    ScreenshotTool(page).take_screenshot("sspi_update_warnings_information_first_name")


def test_sspi_update_warnings_information_age(
    page: Page, information_page: SSPIUpdateWarningsInformationPage
) -> None:
    """
    Select Age "Under 80" from the drop down menu on the SSPI Update Warnings Information report
    """
    selected_age = "Under 80"
    information_page.table_filtered_by_age(selected_age)
    for age in information_page.AGE_OPTIONS:
        if age != selected_age:
            expect(page.locator("tbody")).not_to_contain_text(age)
    ScreenshotTool(page).take_screenshot("sspi_update_warnings_information_age")


def test_sspi_update_warnings_information_received(
    page: Page, information_page: SSPIUpdateWarningsInformationPage
) -> None:
    """
    Select the sorting Received on the SSPI Update Warnings Information report
    """
    information_page.sort_received()
    expect(page.locator("#columnHeaderReceived")).to_have_attribute(
        "aria-sort", "ascending"
    )
    ScreenshotTool(page).take_screenshot("sspi_update_warnings_information_received")


def test_sspi_update_warnings_information_event(
    page: Page, information_page: SSPIUpdateWarningsInformationPage
) -> None:
    """
    Select Event "Subject joined BSO" on the SSPI Update Warnings Information report
    """
    selected_reason = "Subject joined BSO"
    information_page.event_selected(selected_reason)
    for reason in information_page.REASONI_OPTIONS:
        if reason != selected_reason:
            expect(page.locator("tbody")).not_to_contain_text(reason)
    ScreenshotTool(page).take_screenshot("sspi_update_warnings_information_event")


def test_sspi_update_warnings_information_warning(
    page: Page, information_page: SSPIUpdateWarningsInformationPage
) -> None:
    """
    Select Warning "No open episodes" on the SSPI Update Warnings Information report
    """
    selected_warning = "No open episodes"
    information_page.warning_selected(selected_warning)
    for warning in information_page.WARNINGI_OPTIONS:
        if warning != selected_warning:
            expect(page.locator("tbody")).not_to_contain_text(warning)
    ScreenshotTool(page).take_screenshot("sspi_update_warnings_information_warning")


def test_sspi_update_warnings_information_add_info(
    page: Page, information_page: SSPIUpdateWarningsInformationPage
) -> None:
    """
    Select the sorting Add Information on the SSPI Update Warnings Information report
    """
    information_page.sort_add_info()
    expect(page.locator("#columnHeaderAdditionalInfo")).to_have_attribute(
        "aria-sort", "ascending"
    )
    ScreenshotTool(page).take_screenshot("sspi_update_warnings_information_add_info")
