import pytest
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.download.downloads_page import DownloadsPage
from pages.download.individual_download_request_and_retrieval_page import (
    IndividualDownloadRequestAndRetrieval,
)
from pages.download.list_of_individual_downloads_page import ListOfIndividualDownloads
from pages.download.batch_download_request_and_retrieval_page import (
    BatchDownloadRequestAndRetrieval,
)
from utils.user_tools import UserTools


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """
    Before every test is executed, this fixture logs in to BCSS as a test user and navigates to the download page
    """
    # Log in to BCSS
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    # Go to download page
    BasePage(page).go_to_download_page()


@pytest.mark.smoke
def test_download_facility_page_navigation(page: Page) -> None:
    """
    Confirms all menu items are displayed on the downloads page, and that the relevant pages
    are loaded when the links are clicked. Also confirms that the warning header messages are displayed
    on the relevant pages
    """
    # Individual download request and retrieval page loads as expected
    DownloadsPage(page).go_to_individual_download_request_page()
    IndividualDownloadRequestAndRetrieval(
        page
    ).verify_individual_download_request_and_retrieval_title()

    # Individual download request and retrieval page contains warning message
    IndividualDownloadRequestAndRetrieval(page).expect_form_to_have_warning()
    BasePage(page).click_back_button()

    # List of Individual downloads page loads as expected
    DownloadsPage(page).go_to_list_of_individual_downloads_page()
    ListOfIndividualDownloads(page).verify_list_of_individual_downloads_title()
    BasePage(page).click_back_button()

    # Batch download request and retrieval page loads as expected
    DownloadsPage(page).go_to_batch_download_request_and_page()
    BatchDownloadRequestAndRetrieval(
        page
    ).verify_batch_download_request_and_retrieval_title()

    # Batch download request and retrieval page contains warning message
    BatchDownloadRequestAndRetrieval(page).expect_form_to_have_warning()
    BasePage(page).click_back_button()

    # Return to main menu
    BasePage(page).click_main_menu_link()
    BasePage(page).main_menu_header_is_displayed()
