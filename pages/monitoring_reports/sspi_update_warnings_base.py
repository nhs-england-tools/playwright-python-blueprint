import logging
from playwright.sync_api import Page
from pages.report_page import ReportPage


class SSPIUpdateWarningsBasePage(ReportPage):

    def __init__(self, page: Page) -> None:
        ReportPage.__init__(self, page)
        self.action_list = page.locator("#actionList")
        self.API_REQUEST = ""  # This is set by specific action or information page
        self.HEADER = ""  # This is set by specific action or information page

    def verify_header(self) -> None:
        super().verify_header(self.HEADER)

    def set_done_drop_down(self, value: str) -> None:
        self.action_list.select_option(value)
        self.page.wait_for_timeout(5000)

    def enter_nhs_number(self, selected_nhs: str) -> None:
        self.page.locator("#nhsNumberFilter").get_by_role("textbox").fill(selected_nhs)
        self.await_api_response()

    def enter_family_name(self, selected_family_name: str) -> None:
        self.page.locator("#familyNameFilter").get_by_role("textbox").fill(
            selected_family_name
        )
        self.await_api_response()

    def enter_first_name(self, selected_first_name: str) -> None:
        self.page.locator("#firstGivenNameFilter").get_by_role("textbox").fill(
            selected_first_name
        )
        self.await_api_response()

    def sort_received(self) -> None:
        self.action_list.select_option("")
        self.page.get_by_label("Received: activate to sort").click()
        self.page.wait_for_timeout(5000)

    def table_filtered_by_age(self, selected_age: str) -> None:
        self.page.locator("#ageTodayList").select_option(selected_age)
        self.await_api_response()

    def event_selected(self, selected_reason: str) -> None:
        self.page.locator("#eventList").select_option(selected_reason)
        self.await_api_response()

    def warning_selected(self, selected_warning: str) -> None:
        self.page.locator("#reasonList").select_option(selected_warning)
        self.await_api_response()

    def sort_add_info(self) -> None:
        self.action_list.select_option("")
        self.page.get_by_label("Additional Info: activate to").click()
        self.page.wait_for_timeout(5000)

    def await_api_response(self) -> None:
        """
        This method waits for the API response to complete after a filter or action is applied.
        It is useful to ensure that the page has updated before proceeding with further actions.
        """
        with self.page.expect_response(self.API_REQUEST) as response:
            # Response captured here is not used, but we wait for the request to complete
            logging.debug(
                "response received from {} = {}".format(
                    self.API_REQUEST, response.value
                )
            )
