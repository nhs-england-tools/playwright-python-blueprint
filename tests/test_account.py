"""
This file contains account tests.
"""

import pytest
import os
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
def initial_navigation(page: Page) -> None:
    # Navigate to page
    page.goto("/")
    page.get_by_role("button", name="Allow all cookies").click()


def test_change_password(page: Page) -> None:
    """
    This test logs in and changes the password, then fails to log in with the old password and successfully logs in with the new password.
    It then resets the password.
    """
    # Log in and go to change password
    page.get_by_role("textbox", name="Email").fill(
        "nhspathways.test+pwteammember@nhs.net"
    )
    page.get_by_role("textbox", name="Password").fill(os.getenv("USER_PASS"))
    page.get_by_role("button", name="Sign in").click()
    page.goto("/Account/ChangePassword")
    page.get_by_role("textbox", name="Current password").fill(os.getenv("USER_PASS"))
    page.get_by_role("textbox", name="New password", exact=True).fill(
        os.getenv("CHANGE_PASS")
    )
    page.get_by_role("textbox", name="Confirm new password").fill(
        os.getenv("CHANGE_PASS")
    )
    page.get_by_role("button", name="Change password").click()
    expect(page.locator("body")).to_contain_text("Sign in with Care Identity")

    # log back in
    page.get_by_role("textbox", name="Email").fill(
        "nhspathways.test+pwteammember@nhs.net"
    )
    page.get_by_role("textbox", name="Password").fill(os.getenv("USER_PASS"))
    page.get_by_role("button", name="Sign in").click()
    expect(page.get_by_text("Invalid login attempt - either your credentials are incorrect or you need to Sign in with Care Identity")).to_be_visible()
    page.get_by_role("textbox", name="Password").fill(os.getenv("CHANGE_PASS"))
    page.get_by_role("button", name="Sign in").click()
    page.goto("/Account/ChangePassword")
    page.get_by_role("textbox", name="Current password").fill(os.getenv("CHANGE_PASS"))
    page.get_by_role("textbox", name="New password", exact=True).fill(
        os.getenv("USER_PASS")
    )
    page.get_by_role("textbox", name="Confirm new password").fill(
        os.getenv("USER_PASS")
    )
    page.get_by_role("button", name="Change password").click()
    expect(page.locator("body")).to_contain_text("Sign in with Care Identity")

