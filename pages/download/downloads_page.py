from playwright.sync_api import Page
from pages.base_page import BasePage


class DownloadsPage(BasePage):
    """Downloads Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Downloads Page
        self.individual_download_request_page = self.page.get_by_role(
            "link", name="Individual Download Request"
        )
        self.list_of_individual_downloads_page = self.page.get_by_role(
            "link", name="List of Individual Downloads"
        )
        self.batch_download_request_and_page = self.page.get_by_role(
            "link", name="Batch Download Request and"
        )
        self.list_of_batch_downloads_page = self.page.get_by_role(
            "cell", name="List of Batch Downloads", exact=True
        )

    def go_to_individual_download_request_page(self) -> None:
        """Clicks on the 'Individual Download Request' link on the Downloads page."""
        self.click(self.individual_download_request_page)

    def go_to_list_of_individual_downloads_page(self) -> None:
        """Clicks on the 'List of Individual Downloads' link on the Downloads page."""
        self.click(self.list_of_individual_downloads_page)

    def go_to_batch_download_request_and_page(self) -> None:
        """Clicks on the 'Batch Download Request and Retrieval' link on the Downloads page."""
        self.click(self.batch_download_request_and_page)

    def go_to_list_of_batch_downloads_page(self) -> None:
        """Clicks on the 'List of Batch Downloads' link on the Downloads page."""
        self.click(self.list_of_batch_downloads_page)
