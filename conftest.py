"""
This is a conftest.py file for pytest, which is used to set up fixtures and hooks for testing.
This file is used to define fixtures that can be used across multiple test files.
It is also used to define hooks that can be used to modify the behavior of pytest.
"""

import pytest
import os
import typing
from dotenv import load_dotenv
from pathlib import Path
from _pytest.python import Function
from pytest_html.report_data import ReportData

from pages.ni_ri_sp_batch_page import NiRiSpBatchPage

# from utils.db_util import DbUtil
import logging
from playwright.sync_api import sync_playwright

# from utils.db_restore import DbRestore
from utils.user_tools import UserTools

logger = logging.getLogger(__name__)
from playwright.sync_api import Page
from pages.rlp_cohort_list_page import CohortListPage
from pages.rlp_location_list_page import ScreeningLocationListPage
from pages.rlp_unit_list_page import ScreeningUnitListPage
from pages.main_menu import MainMenuPage


LOCAL_ENV_PATH = Path(os.getcwd()) / "local.env"


@pytest.fixture(autouse=True, scope="session")
def import_local_env_file() -> None:
    """
    This fixture is used to import the local.env file into the test environment (if the file is present),
    and will populate the environment variables prior to any tests running.
    If environment variables are set in a different way when running (e.g. via cli), this will
    prioritise those values over the local.env file.

    NOTE: You should not use this logic to read a .env file in a pipeline or workflow to set sensitive values.
    """
    if Path.is_file(LOCAL_ENV_PATH):
        load_dotenv(LOCAL_ENV_PATH, override=False)


@pytest.fixture(scope="session")
def user_tools() -> UserTools:
    return UserTools()


@pytest.fixture
def main_menu(page: Page) -> MainMenuPage:
    return MainMenuPage(page)


@pytest.fixture
def rlp_location_list_page(page: Page) -> ScreeningLocationListPage:
    return ScreeningLocationListPage(page)


@pytest.fixture
def rlp_cohort_list_page(page: Page) -> CohortListPage:
    return CohortListPage(page)


@pytest.fixture
def rlp_unit_list_page(page: Page) -> ScreeningUnitListPage:
    return ScreeningUnitListPage(page)


@pytest.fixture
def ni_ri_sp_batch_page(page: Page) -> NiRiSpBatchPage:
    return NiRiSpBatchPage(page)


# ## Fixture for ci-infra
# @pytest.fixture
# def db_util():
#     db = DbUtil(host = os.getenv("CI_INFRA_DB_HOST"),
#                 port=os.getenv("CI_INFRA_DB_PORT"),
#                 dbname=os.getenv("CI_INFRA_DBNAME"),
#                 user=os.getenv("CI_INFRA_DB_USER"),
#                 password=os.getenv("CI_INFRA_DB_PASSWORD"))
#     return db

# ## Fixture is for VM local database
# @pytest.fixture
# def db_util_local():
#     db = DbUtil(host = os.getenv("LOCAL_DB_HOST"),
#                 port=os.getenv("LOCAL_DB_PORT"),
#                 dbname=os.getenv("LOCAL_DBNAME"),
#                 user=os.getenv("LOCAL_DB_USER"),
#                 password=os.getenv("LOCAL_DB_PASSWORD"))
#     return db

# # @pytest.fixture(scope="session", autouse=True)
# def db_restore():
#     DbRestore().full_db_restore()

# This variable is used for JSON reporting only
ENVIRONMENT_DATA = None


@pytest.fixture(autouse=True, scope="session")
def environment_info(metadata: object, base_url: str) -> None:

    def filter_result(results: dict, key: str) -> str:
        """This is for tidying up the response for the HTML report"""
        string_to_return = ""
        for item in results[key]:
            if string_to_return != "":
                string_to_return += "<br />"
            string_to_return += f"{item}: {results[key][item]}"
        return string_to_return

    if base_url is not None:
        try:  # Try to get metadata first using a playwright object, but don't fail if it can't retrieve it
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                context = browser.new_context(base_url=base_url)
                result = context.request.get(
                    "/bss/info",
                    headers={
                        "Host": f"{base_url}".replace("https://", "").replace("/", ""),
                        "Accept": "*/*",
                        "Accept-Encoding": "gzip, deflate, br",
                    },
                    ignore_https_errors=True,
                )
                metadata["Application Details"] = filter_result(
                    result.json(), "Application Details"
                )
                metadata["Database Details"] = filter_result(
                    result.json(), "Database Details"
                )
                global ENVIRONMENT_DATA
                ENVIRONMENT_DATA = result.json()
                context.close()
                browser.close()

        except Exception as ex:
            logger.warning("Not been able to capture environment data for this run.")
            logger.warning(f"Exception: {ex}")
            metadata["Application Details"] = "Unable to retrieve"
            metadata["Database Details"] = "Unable to retrieve"


# --- JSON Report Generation ---


@pytest.hookimpl(optionalhook=True)
def pytest_json_runtest_metadata(item: object) -> dict:
    formatted_description = str(item.function.__doc__).replace("\n", "")
    return {"description": " ".join(formatted_description.split())}


@pytest.hookimpl(optionalhook=True)
def pytest_json_modifyreport(json_report: object) -> None:
    # Add env data to json report if present
    if ENVIRONMENT_DATA != None:
        json_report["environment_data"] = ENVIRONMENT_DATA


# --- HTML Report Generation ---


def pytest_html_report_title(report: ReportData) -> None:
    report.title = "Test Automation Report"


def pytest_html_results_table_header(cells: list) -> None:
    cells.insert(2, "<th>Description</th>")


def pytest_html_results_table_row(report: object, cells: list) -> None:
    description = getattr(report, "description", "N/A")
    cells.insert(2, f"<td>{description}</td>")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Function) -> typing.Generator[None, None, None]:
    outcome = yield
    if outcome is not None:
        report = outcome.get_result()
        report.description = str(item.function.__doc__)
