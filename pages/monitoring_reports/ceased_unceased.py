import logging
from playwright.sync_api import Page, expect
from pages.report_page import ReportPage


class CeasedUnceasedPage(ReportPage):

    # Selectable Options

    HEADER = "Ceased/Unceased Subject List"
    AGE_OPTIONS=["All", "In BSO Age Range"]
    REASON_OPTIONS=["All", "Informed Choice", "Bilateral Mastectomy", "Mental Capacity Act", "Personal Welfare"],
    TABLE_ID="#subjectCeasingList"
    TABLE_FIRST_ROW=f"{TABLE_ID} > tbody > tr:nth-child(1)"
    TABLE_FIRST_NHS_NUMBER=f"{TABLE_FIRST_ROW} > td:nth-child(3)"
    TABLE_FIRST_FAMILY_NAME=f"{TABLE_FIRST_ROW} > td:nth-child(7)"
    TABLE_FIRST_FIRST_NAME=f"{TABLE_FIRST_ROW} > td:nth-child(8)"
    API_REQUEST="**/bss/report/ceasing/search**"

    def __init__(self, page: Page) -> None:
        ReportPage.__init__(self, page)
        self.page = page

    def verify_header(self) -> None:
        super().verify_header(self.HEADER)

    def search_both(self, run_search: bool = True) -> None:
        self.page.get_by_label("Both").check()
        if run_search:
            self.press_search()

    def search_ceased(self, run_search: bool = True) -> None:
        self.page.get_by_label("Ceased Subjects").nth(0).check()
        if run_search:
            self.press_search()

    def search_unceased(self, run_search: bool = True) -> None:
        self.page.get_by_label("Unceased Subjects").check()
        if run_search:
            self.press_search()

    def press_search(self) -> None:
        self.page.get_by_role("button", name=" Search").click()

    def both_date(self) -> None:
        self.page.get_by_label("Both").check()
        self.page.get_by_label("Ceased/Unceased From").click()
        self.page.get_by_label("Ceased/Unceased From").fill("01/01/2015")
        self.page.get_by_label("Ceased/Unceased Until").click()
        self.page.get_by_role("cell", name="14").click()
        self.page.get_by_role("button", name=" Search").click()

    def ceased_only_date(self) -> None:
        self.page.get_by_label("Ceased Subjects", exact=True).check()
        self.page.get_by_label("Ceased From").click()
        self.page.get_by_label("Ceased From").fill("01/01/2015")
        self.page.get_by_label("Ceased Until").click()
        self.page.get_by_role("cell", name="14").click()
        self.page.get_by_role("button", name=" Search").click()

    def unceased_only_date(self) -> None:
        self.page.get_by_label("Unceased Subjects").check()
        self.page.get_by_label("Unceased From").click()
        self.page.get_by_label("Unceased From").fill("01/01/2015")
        self.page.get_by_label("Unceased Until").click()
        self.page.get_by_role("cell", name="14").click()
        self.page.get_by_role("button", name=" Search").click()

    def set_done_drop_down(self, value: str) -> None:
        self.page.locator("#actionList").select_option(value)
        self.page.wait_for_timeout(5000)

    def enter_nhs_number(self, selected_nhs: str) -> None:
        self.page.locator("#nhsNumberFilter").get_by_role("textbox").fill(selected_nhs)
        with self.page.expect_response(self.API_REQUEST) as response:
            pass

    def sort_date_added_to_BSO(self) -> None:
        self.page.locator("#actionList").select_option("")
        self.page.get_by_label("Date Added To BSO: activate").click()
        self.page.wait_for_timeout(5000)

    def sort_born(self) -> None:
        self.page.locator("#actionList").select_option("")
        self.page.get_by_label("Born: activate to sort column").click()
        self.page.wait_for_timeout(5000)

    def table_filtered_by_age(self, selected_age: str) -> None:
        self.page.locator("#ageTodayList").select_option(selected_age)
        with self.page.expect_response(self.API_REQUEST) as response:
            pass

    def enter_family_name(self, selected_family_name: str) -> None:
        self.page.locator("#familyNameFilter").get_by_role("textbox").fill(selected_family_name)
        with self.page.expect_response(self.API_REQUEST) as response:
            pass

    def enter_first_name(self, selected_first_name: str) -> None:
        self.page.locator("#firstGivenNameFilter").get_by_role("textbox").fill(selected_first_name)
        with self.page.expect_response(self.API_REQUEST) as response:
            pass

    def sort_date_ceased(self) -> None:
        self.page.locator("#actionList").select_option("")
        self.page.get_by_label("Date Ceased: activate to sort").click()
        self.page.wait_for_timeout(5000)

    def sort_date_unceased(self) -> None:
        self.page.locator("#actionList").select_option("")
        self.page.get_by_label("Date Unceased: activate to").click()
        self.page.wait_for_timeout(5000)

    def reason_selected(self, selected_reason: str) -> None:
        self.page.locator("#reasonList").select_option(selected_reason)
        with self.page.expect_response(self.API_REQUEST) as response:
            pass
