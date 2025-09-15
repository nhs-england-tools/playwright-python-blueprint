import logging
import os
from playwright.sync_api import Page
from pathlib import Path
import pytest_playwright_axe


logger = logging.getLogger(__name__)
PATH_FOR_REPORT = str(Path(os.getcwd()) / "axe-reports")


class Axe():
    """
    This utility allows for interaction with axe-core, to allow for accessibility scanning of pages
    under test to identify any accessibility concerns.
    """

    @staticmethod
    def run(
        page: Page,
        filename: str = "",
        output_directory: str = PATH_FOR_REPORT,
        context: str = "",
        options: str = pytest_playwright_axe.OPTIONS_WCAG_22AA,
        report_on_violation_only: bool = False,
        strict_mode: bool = False,
        html_report_generated: bool = True,
        json_report_generated: bool = True,
    ) -> dict:
        """
        This runs axe-core against the page provided.

        Args:
            page (playwright.sync_api.Page): The page object to execute axe-core against.
            filename (str): [Optional] The filename to use for the outputted reports. If not provided, defaults to the URL under test.
            output_directory (str): [Optional] The directory to output the reports to. If not provided, defaults to /axe-reports directory.
            context (str): [Optional] If provided, a stringified JavaScript object to denote the context axe-core should use.
            options (str): [Optional] If provided, a stringified JavaScript object to denote the options axe-core should use. If not provided, defaults to WCAG 2.2 AA standard.
            report_on_violation_only (bool): [Optional] If true, only generates an Axe report if a violation is detected. If false (default), always generate a report.
            strict_mode (bool): [Optional] If true, raise an exception if a violation is detected. If false (default), proceed with test execution.
            html_report_generated (bool): [Optional] If true (default), generates a html report for the page scanned. If false, no html report is generated.
            json_report_generated (bool): [Optional] If true (default), generates a json report for the page scanned. If false, no json report is generated.

        Returns:
            dict: A Python dictionary with the axe-core output of the page scanned.
        """
        return pytest_playwright_axe.Axe.run(
            page=page,
            filename=filename,
            output_directory=output_directory,
            context=context,
            options=options,
            report_on_violation_only=report_on_violation_only,
            strict_mode=strict_mode,
            html_report_generated=html_report_generated,
            json_report_generated=json_report_generated,
        )

    @staticmethod
    def run_list(
        page: Page,
        page_list: list[str],
        use_list_for_filename: bool = True,
        output_directory: str = PATH_FOR_REPORT,
        context: str = "",
        options: str = pytest_playwright_axe.OPTIONS_WCAG_22AA,
        report_on_violation_only: bool = False,
        strict_mode: bool = False,
        html_report_generated: bool = True,
        json_report_generated: bool = True,
    ) -> dict:
        """
        This runs axe-core against a list of pages provided.

        NOTE: It is recommended to set a --base-url value when running Playwright using this functionality, so you only need to pass in a partial URL within the page_list.

        Args:
            page (playwright.sync_api.Page): The page object to execute axe-core against.
            page_list (list[playwright.sync_api.Page): A list of URLs to execute against.
            use_list_for_filename (bool): If true, based filenames off the list provided. If false, use the full URL under test for the filename.
            output_directory (str): [Optional] The directory to output the reports to. If not provided, defaults to /axe-reports directory.
            context (str): [Optional] If provided, a stringified JavaScript object to denote the context axe-core should use.
            options (str): [Optional] If provided, a stringified JavaScript object to denote the options axe-core should use.
            report_on_violation_only (bool): [Optional] If true, only generates an Axe report if a violation is detected. If false (default), always generate a report.
            strict_mode (bool): [Optional] If true, raise an exception if a violation is detected. If false (default), proceed with test execution.
            html_report_generated (bool): [Optional] If true (default), generates a html report for the page scanned. If false, no html report is generated.
            json_report_generated (bool): [Optional] If true (default), generates a json report for the page scanned. If false, no json report is generated.

        Returns:
            dict: A Python dictionary with the axe-core output of all the pages scanned, with the page list used as the key for each report.
        """
        return pytest_playwright_axe.Axe.run_list(
            page=page,
            page_list=page_list,
            use_list_for_filename=use_list_for_filename,
            output_directory=output_directory,
            context=context,
            options=options,
            report_on_violation_only=report_on_violation_only,
            strict_mode=strict_mode,
            html_report_generated=html_report_generated,
            json_report_generated=json_report_generated,
        )
