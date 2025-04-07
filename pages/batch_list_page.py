from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class BatchList(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Batch List - page filters
        self.id_filter = self.page.locator("#batchIdFilter")
        self.type_filter = self.page.locator("#batchTypeFilter")
        self.original_filter = self.page.locator("#originalBatchIdFilter")
        self.event_code_filter = self.page.locator("#eventCodeFilter")
        self.description_filter = self.page.locator("#eventDescriptionFilter")
        self.batch_split_by_filter = self.page.locator("#splitByFilter")
        self.screening_centre_filter = self.page.locator("#screeningCentreFilter")
        self.count_filter = self.page.locator("#countFilter")
        self.table_data = self.page.locator("td")
        self.batch_successfully_archived_msg = self.page.locator(
            'text="Batch Successfully Archived and Printed"'
        )
        self.batch_list_page_title = self.page.locator("#page-title")

    def verify_batch_list_page_title(self, text) -> None:
        expect(self.batch_list_page_title).to_contain_text(text)

    def verify_table_data(self, value) -> None:
        expect(self.table_data.filter(has_text=value)).to_be_visible()

    def enter_id_filter(self, search_text: str) -> None:
        self.id_filter.fill(search_text)
        self.id_filter.press("Enter")

    def enter_type_filter(self, search_text: str) -> None:
        self.type_filter.fill(search_text)
        self.type_filter.press("Enter")

    def enter_original_filter(self, search_text: str) -> None:
        self.original_filter.fill(search_text)
        self.original_filter.press("Enter")

    def enter_event_code_filter(self, search_text: str) -> None:
        self.event_code_filter.fill(search_text)
        self.event_code_filter.press("Enter")

    def enter_description_filter(self, search_text: str) -> None:
        self.description_filter.fill(search_text)
        self.description_filter.press("Enter")

    def enter_batch_split_by_filter(self, search_text: str) -> None:
        self.batch_split_by_filter.fill(search_text)
        self.batch_split_by_filter.press("Enter")

    def enter_screening_centre_filter(self, search_text: str) -> None:
        self.screening_centre_filter.fill(search_text)
        self.screening_centre_filter.press("Enter")

    def enter_count_filter(self, search_text: str) -> None:
        self.count_filter.fill(search_text)
        self.count_filter.press("Enter")


class ActiveBatchList(BatchList):
    def __init__(self, page):
        super().__init__(page)


class ArchivedBatchList(BatchList):
    def __init__(self, page):
        super().__init__(page)
