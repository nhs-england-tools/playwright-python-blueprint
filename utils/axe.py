import logging
import os
from playwright.sync_api import Page, sync_playwright
from pathlib import Path

logging.basicConfig(level=logging.INFO)

AXE_MIN_PATH = Path(__file__).parent / "resources" / "axe.min.js"
AXE_FULL_PATH = Path(__file__).parent / "resources" / "axe.js"
PATH_FOR_REPORT = Path(__file__).parent.parent / "test-results" / "axe-reports"

class Axe:
    """
    This utility allows for interaction with axe-core, to allow for accessibility scanning of pages
    under test to identify any accessibility concerns.
    """

    @staticmethod
    def run(page: Page, full_analysis: bool = False) -> dict:
        """
        This runs axe-core against the page provided.

        Args:
            page (playwright.sync_api.Page): The page object to execute axe-core against.
            full_analysis (bool): [Optional] If true, use axe.js to scan the page. If false (default), use axe.min.js to scan the page.
        """

        axe = AXE_FULL_PATH if full_analysis else AXE_MIN_PATH
        
        page.evaluate(axe.read_text(encoding="UTF-8"))
        
        #TODO - Add support for different scan levels (e.g. wcag 2.2aa)
        #TODO - Add strict mode (fail test if violations found)
        response = page.evaluate("axe.run().then(results => {return results;})")
        logging.info(f"Axe scan summary of [{response["url"]}]: Passes = {len(response["passes"])}, Violations = {len(response["violations"])}, Inapplicable = {len(response["inapplicable"])}, Incomplete = {len(response["incomplete"])}")

        #TODO - Add option to generate report only if failure found
        Axe._create_report(response)

        return response

    @staticmethod
    def _create_report(data: dict) -> None:
        html = Axe._generate_html(data)

        filename = str(data["url"])
        if filename[-1] == "/":
            filename = filename[:-1]
        for item_to_remove in ["http://", "https://"]:
            filename = filename.replace(item_to_remove, "")
        filename = filename.replace("/", "--")
        filename += ".html"

        if not os.path.exists(PATH_FOR_REPORT):
            os.mkdir(PATH_FOR_REPORT)

        full_path = PATH_FOR_REPORT / filename
        with open(full_path, 'w') as file:
            file.writelines(html)

        #TODO - Output filepath for created report

    @staticmethod
    def _generate_html(data: dict) -> str:
        def styling() -> str:
            style = "body { font-family: Arial, Helvetica, sans-serif; }"
            style += "table, th, td { border: 1px solid; border-collapse: collapse; padding: 5px; } "
            style += "th { background-color: #E8EDEE; }"
            style += ".center { text-align: center; }"
            style += ".details-section { width: 100% }"
            style += ".details-header { column-width: 10% }"
            return style
        
        def details_section(header: str) -> str:
            section = f'<h2 name="{header}">{header.title()}</h2>'

            if len(data[header]) > 0:
                for check in data[header]:
                    section += f'<table class="details-section"><tr><th>ID</th><td>{check["id"]}</td></tr>'
                    section += f'<tr><th class "details-header">Impact</th><td>{check["impact"]}</td></tr>'
                    section += f'<tr><th class "details-header">Tags</th><td>{check["tags"]}</td></tr>'
                    section += f'<tr><th class "details-header">Description</th><td>{str(check["description"]).replace("<", "").replace(">", "")}</td></tr>'
                    section += f'<tr><th class "details-header">Help</th><td>{str(check["help"]).replace("<", "").replace(">", "")}</td></tr>'
                    section += f'<tr><th class "details-header">Help URL</th><td><a href="{check["helpUrl"]}" target="_blank">{check["helpUrl"]}</a></td></tr>'
                    section += "</table><br />"
            else:
                section += f"<p>No {header} results returned.</p>"
            
            return section

        # Head & Body Header
        html = "<!doctype html><html><head>"
        html += f"<style>{styling()}</style>"
        html += "<title>Axe Accessibility Report</title></head>"
        html += "<body><h1>Axe Accessibility Report</h1>"
        html += f"<p>This is an axe-core accessibility summary for: {data["url"]}</p>"

        # Metadata
        html += "<h2>Metadata</h2>"
        html += "<table><tr><th>Key</th><th>Description</th></tr>"
        html += f"<tr><td>Engine version</td><td>{data["testEngine"]["name"]} {data["testEngine"]["version"]}</td></tr>"
        html += "</table><br />"

        # Summary
        html += "<h2>Summary</h2>"
        html += "<table><tr><th>Outcome</th><th>Total Count</th></tr>"
        for outcome in ["violations", "inapplicable", "incomplete", "passes"]:
            html += f'<tr><td><a href="#{outcome}">{outcome.title()}</a></td><td class="center">{len(data[outcome])}</td></tr>'
        html += "</table><br />"

        for section in ["violations", "inapplicable", "incomplete", "passes"]:
            html += details_section(section)

        # Close tags
        html += "</body></html>"

        return html


if __name__ == "__main__":
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto("https://www.nhs.uk")
        results = Axe.run(page)

        # ---------------------
        context.close()
        browser.close()
