from playwright.sync_api import Page, expect


def click(page: Page, locator) -> None:
    try:
        page.wait_for_load_state('load')
        page.wait_for_load_state('domcontentloaded')
        locator.wait_for("attached")
        locator.wait_for("visible")
        locator.click()

    except Exception as locatorClickError:
        print(f"Failed to click element with error: {locatorClickError}, trying again...")
        locator.click()
