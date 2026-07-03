"""
This file contains tests to test validation on log in.
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
def initial_navigation(page: Page) -> None:
    """
    This fixture (or hook) is used for each test in this file to navigate to this repository before
    each test, to reduce the need for repeated code within the tests directly.

    This specific fixture has been designated to run for every test by setting autouse=True.
    """

    # Navigate to page
    page.goto("/")
    page.get_by_role("button", name="Allow all cookies").click()


def test_invalid_email(page: Page) -> None:
    """
    Test attempts to log in with an invalid email, then asserts the expected message is returned
    """
    page.get_by_role("textbox", name="Email").fill("nhspathways.test")
    page.get_by_role("textbox", name="Password").fill("Test")
    page.get_by_role("button", name="Sign in", exact=True).click()
    expect(
        page.get_by_text("The Email field is not a valid e-mail address.")
    ).to_be_visible()


def test_incorrect_password(page: Page) -> None:
    """
    Test attempts to log in with a valid email but incorrect password, then asserts the expected message is returned
    """
    page.get_by_role("textbox", name="Email").fill("nhspathways.test+pwteammember@nhs.net")
    page.get_by_role("textbox", name="Password").fill("Test")
    page.get_by_role("button", name="Sign in", exact=True).click()
    expect(page.get_by_text("Invalid login attempt - either your credentials are incorrect or you need to Sign in with Care Identity")).to_be_visible()


def test_empty_email(page: Page) -> None:
    """
    Test attempts to log in without entering an email address, then asserts that Im not logged in
    """
    page.get_by_role("textbox", name="Email").fill("")
    page.get_by_role("textbox", name="Password").fill("Test")
    page.get_by_role("button", name="Sign in", exact=True).click()
    expect(page.get_by_role("button", name="Sign in", exact=True)).to_be_visible()
    # expect(page.get_by_text("Please fill in this field.")).to_be_visible()


def test_empty_password(page: Page) -> None:
    """
    Test attempts to log in without entering a password, then asserts that Im not logged in
    """
    page.get_by_role("textbox", name="Email").fill("nhspathways.test+pwteammember@nhs.net")
    page.get_by_role("textbox", name="Password").fill("")
    page.get_by_role("button", name="Sign in", exact=True).click()
    expect(page.get_by_role("button", name="Sign in", exact=True)).to_be_visible()
    # expect(page.get_by_text("Please fill in this field.")).to_be_visible()
