"""
GP Practice List Tests: These tests cover the GP Practice List, accessed from the BSO Mapping tab.
"""

import csv
import pytest
from pages.main_menu import MainMenuPage
from utils.nhs_number_tools import NHSNumberTools
from utils.user_tools import UserTools
from utils.table_utils import TableUtils
from playwright.sync_api import Page, expect
from pages.bso_mapping.gp_practice_list import GPListPage
from utils.screenshot_tool import ScreenshotTool


pytestmark = [pytest.mark.gppracticelist]

# Fixtures


@pytest.fixture(autouse=True)
def log_in(user_tools: UserTools, page: Page) -> None:
    user_tools.user_login(page, "BSO User - BS1")


@pytest.fixture
def gplist_page(page: Page) -> GPListPage:
    MainMenuPage(page).select_menu_option("BSO Mapping", "GP Practice List")
    gplist_page = GPListPage(page)
    gplist_page.verify_header()
    return gplist_page
