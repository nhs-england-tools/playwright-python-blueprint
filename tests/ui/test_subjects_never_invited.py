"""
Subjects Never Invited For Screening Tests: These tests cover the Subjects Never Invited For Screening report.
"""

import pytest
import csv
from pages.main_menu import MainMenuPage
from utils.nhs_number_tools import NHSNumberTools
from utils.user_tools import UserTools
from utils.table_utils import TableUtils
from playwright.sync_api import Page, expect
from pages.monitoring_reports.subjects_never_invited import SubjectsNeverInvitedPage


pytestmark = [pytest.mark.invited]

# Fixtures


@pytest.fixture(autouse=True)
def log_in(user_tools: UserTools, page: Page) -> None:
    user_tools.user_login(page, "BSO User - BS1")


@pytest.fixture
def subjectsnotinvited_page(page: Page) -> SubjectsNeverInvitedPage:
    MainMenuPage(page).select_menu_option(
        "Monitoring Reports", "Subjects Never Invited For Screening"
    )
    neverinvited_page = SubjectsNeverInvitedPage(page)
    neverinvited_page.verify_header()
    return neverinvited_page


# Tests


def test_subjects_never_invited_csv_download(
    page: Page, neverinvited_page: SubjectsNeverInvitedPage
) -> None:
    """
    Click the Download to CSV button to download the file
    """
    downloaded_file = neverinvited_page.download_csv()
    warning_table = TableUtils(page, neverinvited_page.TABLE_ID)
    row_number = 0
    with open(downloaded_file) as file:
        csv_file = csv.DictReader(file)
        for lines in csv_file:
            expect(warning_table.pick_row(row_number)).to_contain_text(
                NHSNumberTools().spaced_nhs_number(lines["NHS Number"])
            )
            row_number += 1
