import logging

logger = logging.getLogger(__name__)
from playwright.sync_api import Page, expect


class ScreenshotTool:
    """
    A utility class providing functionality for taking a screenshot.
    """

    def __init__(self, page: Page) -> None:
        self.page = page

    def take_screenshot(self, filename: str) -> None:
        """
        This will take a screenshot of the test which is passed into the class.

        Args:
            filename (str): Name given to the screenshot.

        """
        self.page.screenshot(
            path=f"test-results/screenshot/{filename}.png", full_page=True
        )
