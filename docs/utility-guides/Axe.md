# Utility Guide: Axe

The Axe utility provided by this blueprint allows for the scanning of pages by using [axe-core](https://github.com/dequelabs/axe-core), a JavaScript
library used for scanning for accessibility issues and providing guidance on how to resolve these issues.

> NOTE: This is now a direct extension of the [pytest-playwright-axe](https://github.com/davethepunkyone/pytest-playwright-axe) plugin with logic to apply WCAG 2.2 AA rules by default.

## Table of Contents

- [Utility Guide: Axe](#utility-guide-axe)
  - [Table of Contents](#table-of-contents)
  - [Using the Axe class](#using-the-axe-class)
  - [.run(): Single page scan](#run-single-page-scan)
    - [Further reading](#further-reading)
    - [Example usage](#example-usage)
  - [.run\_list(): Multiple page scan](#run_list-multiple-page-scan)
    - [Further reading](#further-reading-1)
    - [Example usage](#example-usage-1)

## Using the Axe class

You can initialise the Axe class by using the following code in your test file:

    from utils.axe import Axe

This Axe module has been designed as a static class, so you do not need to instantiate it when you want to run a scan on a page you have navigated to
using Playwright.

## .run(): Single page scan

To conduct a scan, you can just use the following once the page you want to check is at the right location:

    Axe.run(page)

This will inject the axe-core code into the page and then execute the axe.run() command, generating an accessibility report for the page being tested.

By default, the `Axe.run(page)` command will do the following:

- Scan the page passed in to the WCAG 2.2 AA standard (which is the current expectation for NHS services outlined in the [NHS Service Manual](https://service-manual.nhs.uk/accessibility/what-all-NHS-services-need-to-do))
- Generate a HTML and JSON report with the findings in the `axe-reports` directory, regardless of if any violations are found
- Any steps after the `Axe.run()` command will continue to execute, and it will not cause the test in progress to fail (it runs a passive scan of the page)
- Will return the full response from axe-core as a dict object if the call is set to a variable, e.g. `axe_results = Axe.run(page)` will populate `axe_results` to interact with as required

### Further reading

This class directly extends the pytest-playwright-axe plugin version of this function, so please see the [single page scan documentation](https://github.com/davethepunkyone/pytest-playwright-axe?tab=readme-ov-file#run-single-page-scan) for additional arguments that can be used.

### Example usage

    from utils.axe import Axe
    from playwright.sync_api import Page

    def test_axe_example(page: Page) -> None:
        page.goto("https://github.com/nhs-england-tools/playwright-python-blueprint")
        Axe.run(page)

## .run_list(): Multiple page scan

To scan multiple URLs within your application, you can use the following method:

    Axe.run_list(page, page_list)

This runs the `Axe.run()` function noted above against each URL provided in the `page_list` argument, and will generate reports as required.

### Further reading

This class directly extends the pytest-playwright-axe plugin version of this function, so please see the [multiple page scan documentation](https://github.com/davethepunkyone/pytest-playwright-axe?tab=readme-ov-file#run_list-multiple-page-scan) for additional arguments that can be used.

### Example usage

When using the following command: `pytest --base-url https://www.github.com`:

    from utils.axe import Axe
    from playwright.sync_api import Page

    def test_accessibility(page: Page) -> None:
        # A list of URLs to loop through
        urls_to_check = [
            "nhs-england-tools/playwright-python-blueprint",
            "nhs-england-tools/playwright-python-blueprint/wiki"
            ]

        Axe.run_list(page, urls_to_check)
