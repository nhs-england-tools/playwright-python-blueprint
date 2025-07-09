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
from utils.load_properties_file import PropertiesFile

# Environment Variable Handling

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


@pytest.fixture
def smokescreen_properties() -> dict:
    return PropertiesFile().get_smokescreen_properties()


@pytest.fixture
def general_properties() -> dict:
    return PropertiesFile().get_general_properties()


# HTML Report Customization


def pytest_html_report_title(report: ReportData) -> None:
    report.title = "BCSS Test Automation Report"


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
