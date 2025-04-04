from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class IndividualDownloadRequestAndRetrieval(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        #Individual Download Request And Retrieval - page locators
        self.individual_download_request_and_retrieval_title = self.page.locator("#ntshPageTitle")
        self.page_form = self.page.locator("form[name=\"frm\"]")

    def verify_individual_download_request_and_retrieval_title(self) -> None:
        expect(self.individual_download_request_and_retrieval_title).to_contain_text("Individual Download Request and Retrieval")

    def expect_form_to_have_warning(self) -> None:
        expect(self.page_form).to_contain_text("Warning - FS Screening data will not be downloaded")
