import pytest
from playwright.sync_api import Page, expect
from utils.user_tools import UserTools


@pytest.mark.smoke
def test_successful_login_to_bcss(page: Page) -> None:
    """
    Confirms that a user with valid credentials can log in to bcss
    """
    # Enter a valid username and password and click 'sign in' button
    UserTools.user_login(page, "Hub Manager State Registered")
    # Confirm user has successfully signed in and is viewing the bcss homepage
    expect(page.locator("#ntshAppTitle")).to_contain_text(
        "Bowel Cancer Screening System"
    )
