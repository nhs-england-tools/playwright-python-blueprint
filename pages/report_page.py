import logging
from pathlib import Path
from playwright.sync_api import Page, expect
from pages.base_page import BasePage

DOWNLOAD_PATH = Path(__file__).parent.parent / "test-results"


class ReportPage(BasePage):

    def __init__(self, page: Page) -> None:
        BasePage.__init__(self, page)
        self.page = page

    def download_csv(self) -> Path:
        with self.page.expect_download() as download_info:
            # Perform the action that initiates download
            self.page.get_by_text("Download to CSV").click()
        download = download_info.value
        # Wait for the download process to complete and save the downloaded file somewhere
        download.save_as(DOWNLOAD_PATH / download.suggested_filename)
        return DOWNLOAD_PATH / download.suggested_filename
