from __future__ import annotations
import re
from playwright.sync_api import Page, expect, playwright
import pytest


class ScreeningUnitListPage:

    def __init__(self, page: Page) -> None:
        self.page = page
        self.screening_unit_name_txt_box = page.locator("input#unitNameText")
        self.add_screening_unit_btn_on_pop_up_window = page.locator(
            "#addButtonInAddUnitPopup"
        )
        self.unit_type_inactive_radio_btn = page.locator(
            "//input[@id='statusText' and @type='radio' and @value='INACTIVE']"
        )
        self.unit_type_active_radio_btn = page.locator(
            "//input[@id='statusText' and @type='radio' and @value='ACTIVE']"
        )
        self.status_dropdown = page.locator("#screeningStatusList")
        self.unit_paging_info = page.locator("#screeningUnitList_info")
        self.input_name_filter = page.locator("#nameFilter > input")
        self.add_screening_unit_btn = page.locator("button#addUnitButton")
        self.cancel_btn_on_pop_up = page.locator("#cancelButtonInAddUnitPopup")
        self.no_matching_records_found_msg = page.locator(
            "//td[text()='No matching records found']"
        )
        self.notes_txt_box = page.locator("textarea#notesText")
        self.filterd_unit_name = page.locator("//tr//td[4]")
        self.monday_appointment_value = page.locator("input#mondaySlotsAmendText")

    def enter_screening_unit_name_txt_box(
        self, unit_name: dict
    ) -> ScreeningUnitListPage:
        self.screening_unit_name_txt_box.fill(unit_name)
        return self

    def dbl_click_on_filtered_unit_name(self) -> ScreeningUnitListPage:
        self.filterd_unit_name.dblclick()
        return self

    def select_status_dropdown(self, status_value: str) -> ScreeningUnitListPage:
        self.status_dropdown.select_option(label=status_value)
        return self

    def click_add_screening_unit_btn_on_pop_up_window(self) -> ScreeningUnitListPage:
        self.add_screening_unit_btn_on_pop_up_window.click()
        return self

    def select_unit_status_radio_btn(self, field_value: str) -> ScreeningUnitListPage:
        self.page.wait_for_selector(
            f"//input[@id='statusText' and @type='radio' and @value='{field_value}']"
        ).check()
        return self

    def select_unit_type_radio_btn(self, field_value: str) -> ScreeningUnitListPage:
        self.page.wait_for_selector(
            f"//input[@id='unitTypeText' and @type='radio' and @value='{field_value}']"
        ).check()
        return self

    def select_amend_unit_status_radio_btn(
        self, field_value: str
    ) -> ScreeningUnitListPage:
        self.page.wait_for_selector(
            f"//input[@id='statusAmendText' and @type='radio' and @value='{field_value}']"
        ).check()
        return self

    def select_amend_unit_type_radio_btn(
        self, field_value: str
    ) -> ScreeningUnitListPage:
        self.page.wait_for_selector(
            f"//input[@id='unitTypeAmendText' and @type='radio' and @value='{field_value}']"
        ).check()
        return self

    def select_unit_type_inactive_radio_btn(self) -> ScreeningUnitListPage:
        self.unit_type_inactive_radio_btn.check()
        return self

    def select_unit_type_active_radio_btn(self) -> ScreeningUnitListPage:
        self.unit_type_active_radio_btn.check()
        return self

    def select_status_mobile_radio_btn(self) -> ScreeningUnitListPage:
        self.select_unit_type_radio_btn("MOBILE")
        return self

    def select_status_static_radio_btn(self) -> ScreeningUnitListPage:
        self.select_unit_type_radio_btn("STATIC")
        return self

    def enter_notes_text_box(self, notes: str) -> ScreeningUnitListPage:
        self.notes_txt_box.fill(notes)
        return self

    def click_cancel_btn_on_pop_up_window(self) -> ScreeningUnitListPage:
        self.cancel_btn_on_pop_up.click()
        return self

    def verify_unit_has_no_matching_records_available_in_the_table(
        self, unit_name: str
    ) -> ScreeningUnitListPage:
        self.status_dropdown.select_option(label="All")
        self.input_name_filter.fill(unit_name)
        self.page.wait_for_timeout(3000)
        self.no_matching_records_found_msg.is_visible()
        return self

    def expect_no_matching_records_found_msg(self) -> ScreeningUnitListPage:
        self.no_matching_records_found_msg.is_visible()
        return self

    def get_day_appointment_value(self) -> dict:
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        # Using dictionary comprehension to get values for all days
        return {
            day: self.page.get_by_role("textbox", name=day).input_value()
            for day in days
        }

    def enter_usual_number_of_appontments_text_box(
        self, unit_data: dict
    ) -> ScreeningUnitListPage:
        if "mon" in unit_data:
            self.page.get_by_role("textbox", name="Mon").fill(unit_data["mon"])
        if "tue" in unit_data:
            self.page.get_by_role("textbox", name="Tue").fill(unit_data["tue"])
        if "wed" in unit_data:
            self.page.get_by_role("textbox", name="Wed").fill(unit_data["wed"])
        if "thu" in unit_data:
            self.page.get_by_role("textbox", name="Thu").fill(unit_data["thu"])
        if "fri" in unit_data:
            self.page.get_by_role("textbox", name="Fri").fill(unit_data["fri"])
        if "sat" in unit_data:
            self.page.get_by_role("textbox", name="Sat").fill(unit_data["sat"])
        if "sun" in unit_data:
            self.page.get_by_role("textbox", name="Sun").fill(unit_data["sun"])

    def enter_amend_screening_unit_name(self, text: str) -> ScreeningUnitListPage:
        self.page.locator("input#unitNameAmendText").fill(text)
        return self

    def enter_amend_screening_unit_notes(self, text: str) -> ScreeningUnitListPage:
        self.page.locator("textarea#notesAmendText").fill(text)
        return self

    def clear_name_and_status_filter(self) -> None:
        self.page.wait_for_selector("#screeningStatusList").select_option("")
        self.page.wait_for_selector("#nameFilter input").fill("")

    def click_amend_screening_unit_btn_on_pop_up_window(self) -> None:
        self.page.locator("//span[@id='amendButtonInAmendUnitPopupText']").click()

    def click_cancel_btn_on_amend_screening_unit_pop_up_window(self) -> None:
        self.page.locator("//span[@id='amendButtonInAmendUnitPopupText']").click()

    def filter_unit_by_name(self, unit_name) -> ScreeningUnitListPage:
        self.status_dropdown.select_option(label="All")
        self.input_name_filter.fill(unit_name)
        self.page.wait_for_timeout(5000)
        return self

    def verify_screening_unit_by_name(self, expected_notes) -> ScreeningUnitListPage:
        self.status_dropdown.select_option(label="All")
        self.input_name_filter.fill(expected_notes)
        self.page.wait_for_timeout(3000)
        note_values = self.page.wait_for_selector("//tr//td[4]").text_content()
        self.page.wait_for_timeout(3000)
        assert note_values == expected_notes
        return self

    def click_add_screening_unit_btn(self) -> ScreeningUnitListPage:
        self.add_screening_unit_btn.click()
        return self

    # Method to directly attempt to create the Unit
    def create_unit(self, unit_name: str) -> ScreeningUnitListPage:
        self.click_add_screening_unit_btn()
        self.enter_screening_unit_name_txt_box(unit_name)
        self.select_status_mobile_radio_btn()
        self.click_add_screening_unit_btn_on_pop_up_window()
        self.page.wait_for_timeout(3000)
        return self

    def add_screening_unit(
        self, unit_data: dict, unit_type: str = "MOBILE", unit_status: str = "ACTIVE"
    ):
        # Adds a new screening unit using the provided unit data
        self.add_screening_unit_btn.click()
        self.screening_unit_name_txt_box.fill(unit_data["unit_name"])
        # Unit Type radio button
        if unit_type:
            self.select_unit_type_radio_btn(unit_type)
        if unit_status:
            self.select_unit_status_radio_btn(unit_status)
        self.enter_usual_number_of_appontments_text_box(unit_data)
        if "notes" in unit_data:
            self.page.locator("textarea#notesText").fill(unit_data["notes"])

    def amend_screening_unit(self, unit_data: dict) -> None:
        self.enter_amend_screening_unit_name(unit_data["unit_name"])
        self.enter_amend_usual_number_of_appointments_text_box(unit_data)
        self.enter_amend_screening_unit_notes(unit_data["notes"])
        self.click_amend_screening_unit_btn_on_pop_up_window()

    def screening_unit_list_count_in_db(self, db_util) -> int:
        result = db_util.get_results(
            """select count(1)
                    from rlp_units where bso_organisation_id in(
                            select bso_organisation_id from bso_organisations where bso_organisation_code = 'LAV')
                    """
        )
        return result["count"][0]

    def extract_paging_unit_list_count(self):
        self.input_name_filter.fill("")
        self.status_dropdown.select_option(label="All")
        self.page.wait_for_timeout(4000)
        self.unit_paging_info.scroll_into_view_if_needed()
        paging_info_text = self.unit_paging_info.text_content()
        re_search_result = re.search(r"\b(\d{1,5}) entries\b", paging_info_text)
        return int(re_search_result.group(1))

    def enter_amend_usual_number_of_appointments_text_box(
        self, unit_data: dict
    ) -> ScreeningUnitListPage:
        if "mon" in unit_data:
            self.page.locator("//input[@id='mondaySlotsAmendText']").fill(
                unit_data["mon"]
            )
        if "tue" in unit_data:
            self.page.locator("//input[@id='tuesdaySlotsAmendText']").fill(
                unit_data["tue"]
            )
        if "wed" in unit_data:
            self.page.locator("//input[@id='wednesdaySlotsAmendText']").fill(
                unit_data["wed"]
            )
        if "thu" in unit_data:
            self.page.locator("//input[@id='thursdaySlotsAmendText']").fill(
                unit_data["thu"]
            )
        if "fri" in unit_data:
            self.page.locator("//input[@id='fridaySlotsAmendText']").fill(
                unit_data["fri"]
            )
        if "sat" in unit_data:
            self.page.locator("//input[@id='saturdaySlotsAmendText']").fill(
                unit_data["sat"]
            )
        if "sun" in unit_data:
            self.page.locator("//input[@id='sundaySlotsAmendText']").fill(
                unit_data["sun"]
            )
        return self
