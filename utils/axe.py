import logging
import os
import json
from datetime import datetime
from playwright.sync_api import Page
from pathlib import Path


logger = logging.getLogger(__name__)
AXE_PATH = Path(__file__).parent / "resources" / "axe.js"
PATH_FOR_REPORT = Path(__file__).parent.parent / "axe-reports"
DEFAULT_WCAG_RULESET = ['wcag2a', 'wcag21a', 'wcag2aa', 'wcag21aa', 'wcag22a', 'wcag22aa', 'best-practice']


class Axe:
    """
    This utility allows for interaction with axe-core, to allow for accessibility scanning of pages
    under test to identify any accessibility concerns.
    """

    @staticmethod
    def run(page: Page,
            filename: str = "",
            ruleset: list[str] = DEFAULT_WCAG_RULESET,
            report_on_violation_only: bool = False,
            strict_mode: bool = False,
            html_report_generated: bool = True,
            json_report_generated: bool = True) -> dict:
        """
        This runs axe-core against the page provided.

        Args:
            page (playwright.sync_api.Page): The page object to execute axe-core against.
            filename (str): The filename to use for the outputted reports. If not provided, defaults to the URL under test.
            ruleset (list[str]): [Optional] If provided, a list of strings to denote the ruleset tags axe-core should use. If not provided, defaults to the WCAG 2.2 AA standard (uses tags: 'wcag2a', 'wcag21a', 'wcag2aa', 'wcag21aa', 'wcag22a', 'wcag22aa', 'best-practice').
            report_on_violation_only (bool): [Optional] If true, only generates an Axe report if a violation is detected. If false (default), always generate a report.
            strict_mode (bool): [Optional] If true, raise an exception if a violation is detected. If false (default), proceed with test execution.
            html_report_generated (bool): [Optional] If true (default), generates a html report for the page scanned. If false, no html report is generated.
            json_report_generated (bool): [Optional] If true (default), generates a json report for the page scanned. If false, no json report is generated.

        Returns:
            dict: A Python dictionary with the axe-core output of the page scanned.
        """

        page.evaluate(AXE_PATH.read_text(encoding="UTF-8"))

        response = page.evaluate("axe." + Axe._build_run_command(ruleset) + ".then(results => {return results;})")

        logger.info(f"""Axe scan summary of [{response["url"]}]: Passes = {len(response["passes"])},
                    Violations = {len(response["violations"])}, Inapplicable = {len(response["inapplicable"])},
                    Incomplete = {len(response["incomplete"])}""")

        violations_detected = len(response["violations"]) > 0
        if not report_on_violation_only or (report_on_violation_only and violations_detected):
            if html_report_generated:
                Axe._create_html_report(response, filename)
            if json_report_generated:
                Axe._create_json_report(response, filename)

        if violations_detected and strict_mode:
            raise AxeAccessibilityException(f"Axe Accessibility Violation detected on page: {response["url"]}")

        return response

    @staticmethod
    def run_list(page: Page,
            page_list: list[str],
            use_list_for_filename: bool = True,
            ruleset: list = DEFAULT_WCAG_RULESET,
            report_on_violation_only: bool = False,
            strict_mode: bool = False,
            html_report_generated: bool = True,
            json_report_generated: bool = True) -> dict:
        """
        This runs axe-core against a list of pages provided.

        NOTE: It is recommended to set a --base-url value when running Playwright using this functionality, so you only need to pass in a partial URL within the page_list.

        Args:
            page (playwright.sync_api.Page): The page object to execute axe-core against.
            page_list (list[playwright.sync_api.Page): A list of URLs to execute against.
            use_list_for_filename (bool): If true, based filenames off the list provided. If false, use the full URL under test for the filename.
            ruleset (list[str]): [Optional] If provided, a list of strings to denote the ruleset tags axe-core should use. If not provided, defaults to the WCAG 2.2 AA standard (uses tags: 'wcag2a', 'wcag21a', 'wcag2aa', 'wcag21aa', 'wcag22a', 'wcag22aa', 'best-practice').
            report_on_violation_only (bool): [Optional] If true, only generates an Axe report if a violation is detected. If false (default), always generate a report.
            strict_mode (bool): [Optional] If true, raise an exception if a violation is detected. If false (default), proceed with test execution.
            html_report_generated (bool): [Optional] If true (default), generates a html report for the page scanned. If false, no html report is generated.
            json_report_generated (bool): [Optional] If true (default), generates a json report for the page scanned. If false, no json report is generated.

        Returns:
            dict: A Python dictionary with the axe-core output of all the pages scanned, with the page list used as the key for each report.
        """
        results = {}
        for selected_page in page_list:
            page.goto(selected_page)
            filename = Axe._modify_filename_for_report(selected_page) if use_list_for_filename else ""
            results[selected_page] = Axe.run(
                page,
                filename=filename,
                ruleset=ruleset,
                report_on_violation_only=report_on_violation_only,
                strict_mode=strict_mode,
                html_report_generated=html_report_generated,
                json_report_generated=json_report_generated
                )
        return results


    @staticmethod
    def _build_run_command(ruleset: list[str]) -> str:
        return "run({runOnly: { type: 'tag', values: " + str(ruleset) + " }})"

    @staticmethod
    def _modify_filename_for_report(filename_to_modify: str) -> str:
        if filename_to_modify[-1] == "/":
            filename_to_modify = filename_to_modify[:-1]
        for item_to_remove in ["http://", "https://"]:
            filename_to_modify = filename_to_modify.replace(item_to_remove, "")
        filename_to_modify = filename_to_modify.replace("/", "__").replace('\\', "__").replace(".", "_")

        return filename_to_modify

    @staticmethod
    def _create_path_for_report(filename: str) -> Path:
        if not os.path.exists(PATH_FOR_REPORT):
            os.mkdir(PATH_FOR_REPORT)

        return PATH_FOR_REPORT / filename

    @staticmethod
    def _create_json_report(data: dict, filename_override: str = "") -> None:
        filename = f"{Axe._modify_filename_for_report(data["url"])}.json" if filename_override == "" else f"{filename_override}.json"
        full_path = Axe._create_path_for_report(filename)

        with open(full_path, 'w') as file:
            file.writelines(json.dumps(data))

        logger.info(f"JSON report generated: {full_path}")

    @staticmethod
    def _create_html_report(data: dict, filename_override: str = "") -> None:
        filename = f"{Axe._modify_filename_for_report(data["url"])}.html" if filename_override == "" else f"{filename_override}.html"
        full_path = Axe._create_path_for_report(filename)

        with open(full_path, 'w') as file:
            file.writelines(Axe._generate_html(data))

        logger.info(f"HTML report generated: {full_path}")

    @staticmethod
    def _generate_html(data: dict) -> str:
        def styling() -> str:
            style = '''body { font-family: Arial, Helvetica, sans-serif; }
                    table, th, td { border: 1px solid; border-collapse: collapse; padding: 5px; }
                    th { background-color: #E8EDEE; }
                    .center { text-align: center; }
                    .details-section { width: 100% }
                    .details-header { column-width: 10% }'''
            return style

        def details_section(header: str) -> str:
            section = f'<h2 name="{header}">{header.title()}</h2>'

            if len(data[header]) > 0:
                for check in data[header]:
                    section += f'''<table class="details-section"><tr><th>ID</th><td>{check["id"]}</td></tr>
                                <tr><th class "details-header">Impact</th><td>{check["impact"]}</td></tr>
                                <tr><th class "details-header">Tags</th><td>{check["tags"]}</td></tr>
                                <tr><th class "details-header">Description</th><td>{str(check["description"]).replace("<", "&lt;").replace(">", "&rt;")}</td></tr>
                                <tr><th class "details-header">Help</th><td>{str(check["help"]).replace("<", "&lt;").replace(">", "&rt;")}</td></tr>
                                <tr><th class "details-header">Help URL</th><td><a href="{check["helpUrl"]}" target="_blank">{check["helpUrl"]}</a></td></tr>'''

                    if 'nodes' in check:
                        for node in check['nodes']:
                            section += f'''<tr><th class "details-header">Affected Node</th><td><code>{str(node).replace("<", "&lt;").replace(">", "&rt;")}</code></td></tr>'''

                    section += '</table><br />'
            else:
                section += f'<p>No {header} results returned.</p>'

            return section


        html = f'''<!doctype html><html><head>
                <style>{styling()}</style>
                <title>Axe Accessibility Report</title></head>
                <body><h1>Axe Accessibility Report</h1>
                <p>This is an axe-core accessibility summary for: <strong>{data["url"]}</strong></p>'''

        # Metadata
        html += f'''<h2>Metadata</h2>
                <table><tr><th>Key</th><th>Description</th></tr>
                <tr><td>Date/Time Executed</td><td>{datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d/%m/%Y %H:%M")}</td></tr>
                <tr><td>Engine Version</td><td>{data["testEngine"]["name"]} {data["testEngine"]["version"]}</td></tr>
                <tr><td>User Agent</td><td>{data["testEnvironment"]["userAgent"]}</td></tr>
                <tr><td>Tags Used</td><td>{data["toolOptions"]["runOnly"]["values"]}</td></tr>
                </table><br />'''

        # Summary
        html += '''<h2>Summary</h2>
                <table><tr><th>Outcome</th><th>Total Count</th></tr>'''
        for outcome in ["violations", "incomplete", "passes", "inapplicable"]:
            html += f'<tr><td>{outcome.title()}</td><td class="center">{len(data[outcome])}</td></tr>'
        html += '</table><br />'

        for section in ["violations", "incomplete", "passes", "inapplicable"]:
            html += details_section(section)

        # Close tags
        html += '</body></html>'

        return html


class AxeAccessibilityException(Exception):
    pass
