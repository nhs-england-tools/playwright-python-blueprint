"""
This file provides a very basic test to confirm how to get started with test execution, and also
a way to prove that the blueprint has been copied and built correctly for teams getting stated.

You can invoke this test once the blueprint has been installed by using the following command
to see the test executing and producing a trace report:
    pytest --tracing on --headed
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.example
def test_basic_example(page: Page) -> None:
    '''
    This test demonstrates how to quickly get started using Playwright Python.

    This example starts with @pytest.mark.example, which indicates this test has been tagged
    with the term "example", to demonstrate how tests can be independently tagged.

    When running via the command line, Playwright automatically instantiates certain objects
    available for use, including the Page object (which is how Playwright interacts with the
    system under test).

    This test does the following:
    1) Navigates to this repository
    2) Asserts that the README contents rendered by GitHub includes the text "Playwright Python Blueprint"
    3) Clicks the MIT license link
    4) Asserts that the LICENCE contents rendered by GitHub includes the text "MIT Licence"
    '''

    # Navigate to page
    page.goto("https://github.com/nhs-england-tools/playwright-python-blueprint")

    # Assert repo text is present
    expect(page.get_by_role("article")).to_contain_text("Playwright Python Blueprint")

    # Click license link
    page.get_by_role("link", name="MIT license", exact=True).click()

    # Assert license text
    expect(page.get_by_role("article")).to_contain_text("MIT Licence")


@pytest.mark.example
def test_textbox_example(page: Page) -> None:
    """
    This test demonstrates another example of quickly getting started using Playwright Python.

    This is specifically designed to outline some of the principals that Playwright uses, for
    example when looking for a specific textbox to enter information into, rather than using a
    direct HTML or CSS reference, you can use attributes of the field (in this case the placeholder
    text) to find the element as a user would navigating your application. You can also use
    locators to find specific HTML or CSS elements as required (in this case the locator for the
    assertion).

    This test does the following:
    1) Navigates to this repository
    2) Uses the "Go to file" textbox and searches for this file, "text_example.py"
    3) Selects the label for the dropdown element presented for the search results and clicks
    4) Asserts that the filename for the now selected file is "test_example.py"
    """

    # Navigate to page
    page.goto("https://github.com/nhs-england-tools/playwright-python-blueprint")

    # Select the "Go to file" textbox and search for this file
    page.get_by_placeholder("Go to file").fill("test_example.py")

    # Click the file name presented in the dropdown
    page.get_by_label("blueprint/tests/test_example.").click()

    # Confirm we are viewing the correct file
    expect(page.locator("#file-name-id-wide")).to_contain_text("test_example.py")
