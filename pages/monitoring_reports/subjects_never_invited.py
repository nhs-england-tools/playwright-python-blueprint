import logging
from playwright.sync_api import Page, expect
from pages.report_page import ReportPage


class SubjectsNeverInvitedPage(ReportPage):

    # Selectable Options

    HEADER = "Subjects Never Invited For Screening"
    TABLE_ID = "#subjectsNeverInvitedList"
    TABLE_FIRST_ROW = f"{TABLE_ID} > tbody > tr:nth-child(1)"
    TABLE_FIRST_NHS_NUMBER = f"{TABLE_FIRST_ROW} > td:nth-child(2)"

    def __init__(self, page: Page) -> None:
        ReportPage.__init__(self, page)
        self.page = page

    def verify_header(self) -> None:
        super().verify_header(self.HEADER)
