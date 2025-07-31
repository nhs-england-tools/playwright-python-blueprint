from enum import Enum
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from datetime import datetime
from utils.calendar_picker import CalendarPicker
from utils.nhs_number_tools import NHSNumberTools
from utils.table_util import TableUtils
import logging


class SubjectsToBeInvitedWithTemporaryAddressPage(BasePage):
    """Subjects To Be Invited with Temporary Address Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self.title = "Subjects To Be Invited with Temporary Address";
        self.nhs_filter = self.page.locator("#nhsNumberFilter")

        self.subjects_to_be_invited_with_temporary_address_report_page = self.page.get_by_role("link", name="Subjects To Be Invited with Temporary Address")
        self.report_table = TableUtils(page, "#tobeinvitedtemporaryaddress")

    def go_to_page(self) -> None:
        logging.info(f"Go to '{self.title}'")
        ""f"Click the '{self.title}' link."""
        self.click(self.subjects_to_be_invited_with_temporary_address_report_page)

    def verify_page_title(self) -> None:
        logging.info(f"Verify title as '{self.title}'")
        ""f"Verifies that the {self.title} page title is displayed correctly."""
        self.page_title_contains_text(self.title)

    def filter_by_nhs_number(self, search_text: str) -> None:
        logging.info(f"filter_by_nhs_number : {search_text}")
        """Enter text in the NHS Number filter and press Enter"""
        self.nhs_filter.fill(search_text)
        self.nhs_filter.press("Enter")

    def assertRecordsVisible(self, nhs_no: str, expectedVisible: bool) -> None:
        logging.info(f"Attempting to check if records for {nhs_no} are visible : {expectedVisible}")

        subject_summary_link = self.page.get_by_role(
            "link", name = NHSNumberTools().spaced_nhs_number(nhs_no)
        )

        logging.info(f"subject_summary_link.is_visible() : {subject_summary_link.is_visible()}")
        if (
            expectedVisible != subject_summary_link.is_visible()
        ):
            raise ValueError(
                f"Record for {NHSNumberTools().spaced_nhs_number(nhs_no)} does not have expected visibility : {expectedVisible}.  Was in fact {subject_summary_link.is_visible()}."
            )

    def filterByReviewed(self, filterValue: str) -> None:
        logging.info(f"Filter reviewed column by : {filterValue}")

        filterBox = self.page.locator("#reviewedFilter")
        filterBox.click()
        filterBox.select_option(filterValue)

    def reviewSubject(self, nhs_no: str, reviewed: bool) -> None:
        logging.info(f"Mark subject {nhs_no} as reviewed: {reviewed}")

        row = self.page.locator(f'tr:has-text("{NHSNumberTools().spaced_nhs_number(nhs_no)}")')
        lastCell = row.get_by_role("cell").nth(-1)
        checkbox = lastCell.get_by_role("checkbox")
        checkbox.set_checked(reviewed)

    def click_subject_link(self, nhs_no: str) -> None:
        subject_summary_link = self.page.get_by_role(
            "link", name = NHSNumberTools().spaced_nhs_number(nhs_no)
        )
        subject_summary_link.click()
