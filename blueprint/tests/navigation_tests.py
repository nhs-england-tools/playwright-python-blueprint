import pytest
from playwright.sync_api import Page, expect

@pytest.mark.example
def test_bbc_navigation(page: Page) -> None:

    # Navigate to page
    page.goto("https://bbc.com")
