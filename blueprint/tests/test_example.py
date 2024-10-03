# This file provides a very basic test to confirm the configuration is working

from playwright.sync_api import Page, expect


def test_basic_example(page: Page):
    # Navigate to page
    page.goto("https://github.com/nhs-england-tools/playwright-python-blueprint")

    # Assert repo text is present
    expect(page.get_by_role("article")).to_contain_text("Playwright Python Blueprint")

    # Click license link
    page.get_by_role("link", name="MIT license").click()

    # Assert license text
    expect(page.get_by_role("article")).to_contain_text("MIT Licence")
