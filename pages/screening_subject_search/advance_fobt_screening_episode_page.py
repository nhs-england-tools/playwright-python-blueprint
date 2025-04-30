from playwright.sync_api import Page, expect, Locator
from pages.base_page import BasePage


class AdvanceFOBTScreeningEpisode(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Advance FOBT Screening Episode - page locators
        self.suitable_for_endoscopic_test_button = self.page.get_by_role(
            "button", name="Suitable for Endoscopic Test"
        )
        self.calendar_button = self.page.get_by_role("button", name="Calendar")
        self.test_type_dropdown = self.page.locator("#UI_EXT_TEST_TYPE_2233")
        self.invite_for_diagnostic_test_button = self.page.get_by_role(
            "button", name="Invite for Diagnostic Test >>"
        )
        self.attend_diagnostic_test_button = self.page.get_by_role(
            "button", name="Attend Diagnostic Test"
        )
        self.other_post_investigation_button = self.page.get_by_role(
            "button", name="Other Post-investigation"
        )
        self.record_other_post_investigation_contact_button = self.page.get_by_role(
            "button", name="Record other post-"
        )

    def click_suitable_for_endoscopic_test_button(self) -> None:
        AdvanceFOBTScreeningEpisode(self.page).safe_accept_dialog(
            self.suitable_for_endoscopic_test_button
        )

    def click_calendar_button(self) -> None:
        self.click(self.calendar_button)

    def select_test_type_dropdown_option(self, text: str) -> None:
        self.test_type_dropdown.select_option(label=text)

    def click_invite_for_diagnostic_test_button(self) -> None:
        AdvanceFOBTScreeningEpisode(self.page).safe_accept_dialog(
            self.invite_for_diagnostic_test_button
        )

    def click_attend_diagnostic_test_button(self) -> None:
        self.click(self.attend_diagnostic_test_button)

    def click_other_post_investigation_button(self) -> None:
        AdvanceFOBTScreeningEpisode(self.page).safe_accept_dialog(
            self.other_post_investigation_button
        )

    def get_latest_event_status_cell(self, latest_event_status: str) -> Locator:
        return self.page.get_by_role("cell", name=latest_event_status, exact=True)

    def verify_latest_event_status_value(self, latest_event_status: str) -> None:
        latest_event_status_cell = self.get_latest_event_status_cell(
            latest_event_status
        )
        expect(latest_event_status_cell).to_be_visible()

    def click_record_other_post_investigation_contact_button(self) -> None:
        self.click(self.record_other_post_investigation_contact_button)
