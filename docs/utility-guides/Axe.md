# Utility Guide: Axe

The Axe utility provided by this blueprint allows for the scanning of pages by using [axe-core](https://github.com/dequelabs/axe-core), a JavaScript
library used for scanning for accessibility issues and providing guidance on how to resolve these issues.

## Using the Axe class

You can initialise the Axe class by using the following code in your test file:

    from utils.axe import Axe

This Axe module has been designed as a static class, so you do not need to instantiate it when you want to run a scan on a page you have navigated to
using Playwright.

To conduct a scan, you can just use the following once the page you want to check is at the right location:

    Axe.run(page)

This will inject the axe-core code into the page and then execute the axe.run() command, generating an accessibility report for the page being tested.

By default, the `Axe.run(page)` command will do the following:

* Scan the page passed in to the WCAG 2.2 AA standard (which is the current expectation for NHS services outlined in the [NHS Service Manual](https://service-manual.nhs.uk/accessibility/what-all-NHS-services-need-to-do))
* Generate a HTML and JSON report with the findings in the `axe-reports` directory, regardless of if any violations are found
* Any steps after the `Axe.run()` command will continue to execute, and it will not cause the test in progress to fail (it runs a passive scan of the page)
* Will return the full response from axe-core as a dict object if the call is set to a variable, e.g. `axe_results = Axe.run(page)` will populate `axe_results` to interact with as required

## Required arguments

The following are required for `Axe.run()`:

|Argument|Format|Description|
|--------|------|-----------|
|page|playwright.sync_api.Page|A Playwright Page on the page to be checked.|

## Optional arguments

The `Axe.run(page)` has the following optional arguments that can be passed in:

|Argument|Format|Supported Values|Default Value|Description|
|--------|------|----------------|-------------|-----------|
|`ruleset` |`list[str]`|Any provided by [axe-core](https://www.deque.com/axe/core-documentation/api-documentation/)|`['wcag2a', 'wcag21a', 'wcag2aa', 'wcag21aa', 'wcag22a', 'wcag22aa', 'best-practice']`|The tags that axe-core uses to filter specific checks. Defaulted to rules used for the WCAG 2.2 AA standard.|
|`filename`|`str`|A string valid for a filename (e.g. `test_report`)||If provided, HTML and JSON reports will save with the filename provided. If not provided (default), the URL of the page under test will be used as the filename.|
|`report_on_violation_only`|`bool`|`True`, `False`|`False`|If True, HTML and JSON reports will only be generated if at least one violation is found.|
|`strict_mode`|`bool`|`True`, `False`|`False`|If True, when a violation is found an AxeAccessibilityException is raised, causing a test failure.|
|`html_report_generated`|`bool`|`True`, `False`|`True`|If True, a HTML report will be generated summarising the axe-core findings.|
|`json_report_generated`|`bool`|`True`, `False`|`True`|If True, a JSON report will be generated with the full axe-core findings.|

## Example usage

    from utils.axe import Axe
    from playwright.sync_api import Page

    def test_axe_example(page: Page) -> None:
        page.goto("https://github.com/nhs-england-tools/playwright-python-blueprint")
        Axe.run(page)
