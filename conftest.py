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
from _pytest.config.argparsing import Parser
from _pytest.fixtures import FixtureRequest
from playwright.sync_api import Page
from utils.oracle.oracle_specific_functions.organisation_parameters import (
    set_org_parameter_value,
    check_parameter,
)
from utils.last_test_run import has_test_run_today
from utils.appointments import setup_appointments

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


# Command-Line Options for Pytest


def pytest_addoption(parser: Parser) -> None:
    """
    Add custom command-line options to pytest.

    Args:
        parser (Parser): The pytest parser object used to define CLI options.

    Adds:
        --subjects-to-run-for (int):
            The number of subjects to run the test setup for.
            Default is 10.

    Example:
        pytest tests/test_setup.py::test_setup_subjects_as_a259 --subjects-to-run-for=5
    """
    parser.addoption(
        "--subjects-to-run-for",
        action="store",
        default="10",
        help="Number of subjects to run the test setup for (default: 10)",
    )


@pytest.fixture
def subjects_to_run_for(request: FixtureRequest) -> int:
    """
    Fixture to retrieve the value of the '--subjects-to-run-for' CLI argument.

    Args:
        request (FixtureRequest): Provides access to the requesting test context.

    Returns:
        int: The number of subjects specified via the CLI or default (10).
    """
    return int(request.config.getoption("--subjects-to-run-for"))  # type: ignore


@pytest.fixture(scope="function")
def setup_org_and_appointments(
    page: Page, request: FixtureRequest, general_properties: dict
) -> None:
    """
    Ensures required org parameters and appointments are set up.
    Only runs once per day per environment, regardless of which test calls it.

    This fixture is designed to be used in tests that require a specific setup of the organisation and appointments.

    Example usage:

    @pytest.mark.usefixtures("setup_org_and_appointments")
    def test_my_function(page: Page):
        # Your test code here

    def test_my_function(page: Page, setup_org_and_appointments):
        # Your test code here
    """
    org_id = general_properties["eng_screening_centre_id"]
    param_12_set_correctly = check_parameter(12, org_id, "10")
    param_28_set_correctly = check_parameter(28, org_id, "07:00")
    param_29_set_correctly = check_parameter(29, org_id, "20:00")
    if not param_12_set_correctly:
        set_org_parameter_value(12, "10", org_id)
    if not param_28_set_correctly:
        set_org_parameter_value(28, "07:00", org_id)
    if not param_29_set_correctly:
        set_org_parameter_value(29, "20:00", org_id)

    base_url = request.config.getoption("--base-url")
    fixture_name = "setup_org_and_appointments"
    if not has_test_run_today(fixture_name, base_url):  # type: ignore
        setup_appointments(page, 0, max=True)
