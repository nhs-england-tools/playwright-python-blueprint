import logging
from playwright.sync_api import Page
from pages.monitoring_reports.sspi_update_warnings_base import (
    SSPIUpdateWarningsBasePage,
)


class SSPIUpdateWarningsActionPage(SSPIUpdateWarningsBasePage):

    # Selectable Options

    AGE_OPTIONS = ["All", "Under 80", "80 and over"]
    REASON_OPTIONS = [
        "Date of birth changed",
        "Date of death set",
        "Date of death cleared",
        "Gender changed",
        "NHS number changed",
        "NHS number superseded",
        "Subject joined BSO",
        "Subject left BSO",
    ]
    WARNING_OPTIONS = [
        "Age now inside programme",
        "Age now inside programme - Open episode",
        "Age now outside programme",
        "Age now outside programme - Open episode",
        "Date of death cleared",
        "Gender is Indeterminate",
        "Male with SC end code",
        "Male with no history",
        "Male with screening events",
        "No open episodes",
        "Open episode closed",
        "Subject has open episode",
        "Subject has HR status",
        "Subject has screening events",
        "Subject is ceased",
        "Under 44 with batch episodes",
        "Was below age limit now above",
        "Was below age limit now above - Open episode",
        "Was previously male",
    ]
    TABLE_ID = "#sspiUpdateWarningList"
    TABLE_FIRST_ROW = f"{TABLE_ID} > tbody > tr:nth-child(1)"
    TABLE_FIRST_NHS_NUMBER = f"{TABLE_FIRST_ROW} > td:nth-child(3)"
    TABLE_FIRST_FAMILY_NAME = f"{TABLE_FIRST_ROW} > td:nth-child(4)"
    TABLE_FIRST_FIRST_NAME = f"{TABLE_FIRST_ROW} > td:nth-child(5)"

    def __init__(self, page: Page) -> None:
        SSPIUpdateWarningsBasePage.__init__(self, page)
        self.API_REQUEST = "**/bss/report/sspiUpdateWarnings/action/search**"
        self.HEADER = "SSPI Update Warnings - Action"
        # self.page = page

    # def verify_header(self) -> None:
    #     super().verify_header(self.HEADER)

    # def set_done_drop_down(self, value: str) -> None:
    #     self.page.locator("#actionList").select_option(value)
    #     self.page.wait_for_timeout(5000)

    # def enter_nhs_number(self, selected_nhs: str) -> None:
    #     self.page.locator("#nhsNumberFilter").get_by_role("textbox").fill(selected_nhs)
    #     with self.page.expect_response(self.API_REQUEST) as response:
    #         pass

    # def enter_family_name(self, selected_family_name: str) -> None:
    #     self.page.locator("#familyNameFilter").get_by_role("textbox").fill(
    #         selected_family_name
    #     )
    #     with self.page.expect_response(self.API_REQUEST) as response:
    #         pass

    # def enter_first_name(self, selected_first_name: str) -> None:
    #     self.page.locator("#firstGivenNameFilter").get_by_role("textbox").fill(
    #         selected_first_name
    #     )
    #     with self.page.expect_response(self.API_REQUEST) as response:
    #         pass

    # def sort_received(self) -> None:
    #     self.page.locator("#actionList").select_option("")
    #     self.page.get_by_label("Received: activate to sort").click()
    #     self.page.wait_for_timeout(5000)

    # def table_filtered_by_age(self, selected_age: str) -> None:
    #     self.page.locator("#ageTodayList").select_option(selected_age)
    #     with self.page.expect_response(self.API_REQUEST) as response:
    #         pass

    # def event_selected(self, selected_reason: str) -> None:
    #     self.page.locator("#eventList").select_option(selected_reason)
    #     with self.page.expect_response(self.API_REQUEST) as response:
    #         pass

    # def warning_selected(self, selected_warning: str) -> None:
    #     self.page.locator("#reasonList").select_option(selected_warning)
    #     with self.page.expect_response(self.API_REQUEST) as response:
    #         pass

    # def sort_add_info(self) -> None:
    #     self.page.locator("#actionList").select_option("")
    #     self.page.get_by_label("Additional Info: activate to").click()
    #     self.page.wait_for_timeout(5000)
