from __future__ import annotations
import re
import playwright
from playwright.sync_api import Page, expect


class ScreeningLocationListPage:

    def __init__(self, page: Page) -> None:

        self.page = page
        self.add_screening_location_btn = page.locator("button#addLocationButton")
        self.screening_location_name_txtbox = page.locator("input#locationNameText")
        self.add_screening_location_btn_on_popup = page.locator(
            "#addButtonInAddLocationPopupText"
        )
        self.cancel_add_screening_location_btn = page.locator(
            "#cancelButtonInAddLocationPopup"
        )
        self.paging_info = page.locator("#screeningLocationList_info")
        self.location_name_filter = page.locator("th#nameFilter > input")
        self.filtered_location = page.locator("//tbody/tr/td[2]")
        self.amend_screening_location_name = page.locator("#locationNameAmendText")
        self.amend_screening_location_btn = page.locator(
            "#amendButtonInAmendLocationPopupText"
        )
        self.cancel_amend_location_btn = page.locator(
            "#cancelButtonInAmendLocationPopup"
        )
        self.log_out_btn = page.locator("#logoutButton")
        self.create_screening_cohort_by_gp_practice_btn = page.locator(
            "#addCohortByPracticeButtonText"
        )
        self.screening_cohort_name_txtbox = page.locator("//input[@id='description']")
        self.default_screening_location_dropdown = page.locator(
            "//select[@id='defaultLocation']"
        )
        self.default_screening_unit_dropdown = page.locator(
            "//select[@id='defaultUnit']"
        )
        self.select_gp_practices_btn = page.locator("button#selectElementsButton.btn")
        self.create_screening_cohort_save_btn = page.locator("#saveButton")
        self.gp_practice_name_field = page.locator("th#nameFilter > input")
        self.gp_code_field = page.locator("th#codeFilter > input")
        self.add_gp_practices_to_include = page.locator("//button[text()='Add']")
        self.expected_attendance_rate = page.locator("input#uptakePercentage")
        self.error_message_locator = page.locator("p#error_locationNameText")

    def click_add_screening_location_btn(self) -> ScreeningLocationListPage:
        self.add_screening_location_btn.click()
        return self

    def enter_screening_location_name(
        self, location_name: str
    ) -> ScreeningLocationListPage:
        self.screening_location_name_txtbox.fill(location_name)
        return self

    def click_add_screening_location_btn_on_popup(self) -> ScreeningLocationListPage:
        self.add_screening_location_btn_on_popup.click()
        self.page.wait_for_timeout(3000)
        return self

    def click_cancel_add_screening_location_btn(self) -> ScreeningLocationListPage:
        self.cancel_add_screening_location_btn.click()
        return self

    def enter_screening_location_filter_txtbox(
        self, location_name: str
    ) -> ScreeningLocationListPage:
        self.location_name_filter.fill(location_name)
        self.page.wait_for_timeout(4000)
        return self

    def extract_paging_info(self) -> int:
        self.paging_info.scroll_into_view_if_needed()
        paging_info_text = self.paging_info.text_content()
        self.page.wait_for_timeout(5000)
        re_search_result = re.search(r"\b(\d{1,5}) entries\b", paging_info_text)
        return int(re_search_result.group(1))

    def invoke_filtered_screening_location(self) -> None:
        self.page.wait_for_timeout(4000)
        self.filtered_location.dblclick()

    def enter_amend_screening_location_name_fn(self) -> ScreeningLocationListPage:
        existing_value = self.amend_screening_location_name.input_value()
        new_name = f"{existing_value}+ Amend"
        self.amend_screening_location_name.fill(new_name)
        return new_name

    def enter_amend_screening_location_name(
        self, amend_name: str
    ) -> ScreeningLocationListPage:
        self.amend_screening_location_name.fill(amend_name)
        return self

    def screening_location_count_in_db(self, db_util) -> int:
        result = db_util.get_results(
            """select count(1)
                    from rlp_locations where bso_organisation_id in(
                            select bso_organisation_id from bso_organisations where bso_organisation_code = 'LAV')
                    """
        )
        return result["count"][0]

    def click_amend_screening_location_btn(self) -> None:
        self.amend_screening_location_btn.click()

    def click_cancel_amend_location_btn(self) -> None:
        self.cancel_amend_location_btn.click()

    def value_of_filterd_location_name(self):
        filterd_value = self.filtered_location.text_content()
        self.page.wait_for_timeout(4000)
        return filterd_value

    def click_log_out_btn(self) -> None:
        self.log_out_btn.click()

    def click_create_screening_cohort_by_gp_practice_btn(
        self,
    ) -> ScreeningLocationListPage:
        self.create_screening_cohort_by_gp_practice_btn.click()
        return self

    def enter_screening_cohort_name_txtbox(
        self, cohort_name: str
    ) -> ScreeningLocationListPage:
        self.screening_cohort_name_txtbox.fill(cohort_name)
        return self

    def select_default_screening_location_dropdown(
        self, location_name: str
    ) -> ScreeningLocationListPage:
        self.default_screening_location_dropdown.select_option(location_name)
        return self

    def select_default_screening_unit_dropdown(
        self, unit_name: str
    ) -> ScreeningLocationListPage:
        self.default_screening_unit_dropdown.select_option(unit_name)
        return self

    def click_select_gp_practices_btn(self) -> ScreeningLocationListPage:
        self.select_gp_practices_btn.click()
        return self

    def click_create_screening_cohort_save_btn(self) -> ScreeningLocationListPage:
        self.create_screening_cohort_save_btn.click()
        return self

    def enter_gp_practice_name_field(self, gp_name: str) -> ScreeningLocationListPage:
        self.gp_practice_name_field.fill(gp_name)
        return self

    def enter_gp_code_filed(self, gp_code: str) -> ScreeningLocationListPage:
        self.gp_code_field.fill(gp_code)
        return self

    def click_add_btn_gp_practices_to_include(self) -> ScreeningLocationListPage:
        self.add_gp_practices_to_include.click()
        return self

    def enter_expected_attendance_rate(self) -> ScreeningLocationListPage:
        self.expected_attendance_rate.click()
        return self

    def create_screening_location(self, location_name) -> None:
        self.click_add_screening_location_btn()
        self.enter_screening_location_name(location_name)
        self.click_add_screening_location_btn_on_popup()

    # Method to directly attempt to create the location
    def create_location_if_not_exists(self, location_name: str):
        self.click_add_screening_location_btn()
        self.enter_screening_location_name(location_name)
        self.click_add_screening_location_btn_on_popup()
        # Check for the error message indicating a duplicate location
        try:
            self.page.wait_for_selector(
                "p#error_locationNameText", timeout=3000
            )  # Adjust timeout as needed
            if (
                "Name is already in use by another location"
                in self.error_message_locator.inner_text()
            ):
                # If the error message appears, click cancel to close the popup
                self.click_cancel_add_screening_location_btn()
        except playwright._impl._errors.TimeoutError:
            # If no error message appears, assume the location was added successfully
            pass
        self.page.wait_for_timeout(500)
