"""
This file provides a very basic test to confirm how to get started with test execution, and also
a way to prove that the blueprint has been copied and built correctly for teams getting stated.

You can invoke this test once the blueprint has been installed by using the following command
to see the test executing and producing a trace report:
    pytest --tracing on --headed
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
def initial_navigation(page: Page) -> None:
    '''
    This fixture (or hook) is used for each test in this file to navigate to this repository before
    each test, to reduce the need for repeated code within the tests directly.

    This specific fixture has been designated to run for every test by setting autouse=True.
    '''

    # Navigate to page
    page.goto("https://github.com/nhs-england-tools/playwright-python-blueprint")


@pytest.mark.example
def test_basic_example(page: Page) -> None:
    '''
    This test demonstrates how to quickly get started using Playwright Python, which runs using pytest.

    This example starts with @pytest.mark.example, which indicates this test has been tagged
    with the term "example", to demonstrate how tests can be independently tagged.

    When running using the pytest command, Playwright automatically instantiates certain objects
    available for use, including the Page object (which is how Playwright interacts with the
    system under test).

    This test does the following:
    1) Navigates to this repository (via the initial_navigation fixture above)
    2) Asserts that the README contents rendered by GitHub contains the text "Playwright Python Blueprint"
    3) Asserts that the main section of the page contains the topic label "playwright-python"
    '''

    # Assert repo text is present
    expect(page.get_by_role("article")).to_contain_text("Playwright Python Blueprint")

    # Assert the page loaded contains a reference to the playwright-python topic page
    expect(page.get_by_role("main")).to_contain_text("playwright-python")


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
    1) Navigates to this repository (via the initial_navigation fixture above)
    2) Uses the "Go to file" textbox and searches for this file, "text_example.py"
    3) Selects the label for the dropdown element presented for the search results and clicks
    4) Asserts that the filename for the now selected file is "test_example.py"
    """

    # Select the "Go to file" textbox and search for this file
    page.get_by_placeholder("Go to file").fill("test_example.py")

    # Click the file name presented in the dropdown
    page.get_by_label("tests/test_example.").click()

    # Confirm we are viewing the correct file
    expect(page.locator("#file-name-id-wide")).to_contain_text("test_example.py")
