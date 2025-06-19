from __future__ import annotations
import re
import playwright
from playwright.sync_api import Page, expect


class CohortListPage:

    def __init__(self, page: Page) -> None:
        self.page = page

        self.create_screening_cohort_by_gp_practice_btn = page.locator(
            "#addCohortByPracticeButtonText"
        )
        self.screening_cohort_name_txtbox = page.locator("//input[@id='description']")
        self.default_screening_location_dropdown = page.locator(
            "select#defaultLocation"
        )
        self.default_screening_unit_dropdown = page.locator("select#defaultUnit")
        self.select_gp_practices_btn = page.locator("button#selectElementsButton.btn")
        self.create_screening_cohort_save_btn = page.locator("#saveButton")
        self.gp_practice_name_field = page.locator("th#nameFilter > input")
        self.gp_code_field = page.locator("th#codeFilter > input")
        self.add_gp_practices_to_include = page.locator("//button[text()='Add']")
        self.cancel_creating_screening_cohort = page.locator("a#cancelButton")
        self.expected_attendance_rate = page.locator("input#uptakePercentage")
        self.done_btn_gp_practices_incluse_popup = page.locator(
            "button#cancelButtonInAmendCohortPopup"
        )
        self.screening_cohort_name_filter = page.locator("th#descriptionFilter > input")
        self.screening_location_filter = page.locator(
            "th#defaultLocationFilter > input"
        )
        self.screening_unit_filter = page.locator("th#defaultUnitFilter> input")
        self.location_paging_info = page.locator("#screeningLocationList_info")
        self.unit_paging_info = page.locator("#screeningUnitList_info")
        self.cohort_paging_info = page.locator("#screeningCohortList_info")
        self.remove_btn_included_gp_practices = page.locator("button#deleteBtn_301")
        self.filtered_cohort_name = page.locator("//tbody/tr/td[2]")
        self.filtered_cohort_pencil_icon = page.locator("tbody tr td .glyphicon-pencil")
        self.amend_cohort_cancel_button = page.locator("a#cancelButton")
        self.amend_screening_cohort_name_txtbox = page.locator("input#description")
        self.amend_attendance_rate_txtbox = page.locator("input#uptakePercentage")
        self.amend_screening_location_dropdown = page.locator("select#defaultLocation")
        self.amend_screening_unit_dropdown = page.locator("select#defaultUnit")
        self.amend_select_gp_practices_btn = page.locator(
            "span#selectElementsButtonText"
        )
        self.amend_save_btn = page.locator("span#saveButtonText")
        self.amend_gp_code_field = page.locator("th#codeFilter > input")
        self.amend_add_btn_select_gp_practices = page.get_by_role("button", name="Add")
        self.amend_done_btn_gp_practices = page.locator(
            "button#cancelButtonInAmendCohortPopup"
        )
        self.location_dropdown_count = page.locator("select#defaultLocation option")
        self.unit_dropdown_count = page.locator("select#defaultUnit option")
        self.error_message_locator = page.locator("p#error_unitNameText")
        self.create_screening_cohort_by_outcode_btn = page.locator(
            "button#addCohortByOutcodeButton"
        )
        self.cancel_cohort_by_outcode_btn = page.locator("a#cancelButton")
        self.save_cohort_by_outcode_btn = page.locator("button#saveButton")
        self.select_outcodes_btn = page.locator("button#selectElementsButton")
        self.outcode_filter = page.locator("#nameFilter > input")

    def click_create_screening_cohort_by_gp_practice_btn(self) -> CohortListPage:
        self.create_screening_cohort_by_gp_practice_btn.click()
        return self

    def click_create_screening_cohort_by_outcode_btn(self) -> CohortListPage:
        self.create_screening_cohort_by_outcode_btn.click()
        return self

    def enter_outcode_filter(self, out_code: str) -> CohortListPage:
        self.outcode_filter.fill(out_code)
        return self

    def click_cancel_cohort_by_outcode_btn(self) -> CohortListPage:
        self.cancel_cohort_by_outcode_btn.click()
        return self

    def click_save_cohort_by_outcode_btn(self) -> CohortListPage:
        self.save_cohort_by_outcode_btn.click()
        return self

    def click_select_outcodes_btn(self) -> CohortListPage:
        self.select_outcodes_btn.click()
        return self

    def number_of_location_dropdown_count(self) -> CohortListPage:
        self.page.wait_for_timeout(5000)
        return self.location_dropdown_count.count() - 1  # excluding empty option

    def number_of_unit_dropdown_count(self) -> CohortListPage:
        return self.unit_dropdown_count.count() - 1  # excluding empty option

    def select_amend_screening_location_dropdown(
        self, location_name: str
    ) -> CohortListPage:
        self.amend_screening_location_dropdown.select_option(location_name)
        return self

    def select_amend_screening_unit_dropdown(self, unit_name: str) -> CohortListPage:
        self.amend_screening_unit_dropdown.select_option(unit_name)
        return self

    def enter_amend_gp_code_field(self, gp_code: str) -> CohortListPage:
        self.amend_gp_code_field.fill(gp_code)
        return self

    def click_amend_select_gp_practices_btn(self) -> CohortListPage:
        self.amend_select_gp_practices_btn.click()
        return self

    def click_amend_save_btn(self) -> CohortListPage:
        self.amend_save_btn.click()
        return self

    def click_amend_add_btn_select_gp_practices(self) -> CohortListPage:
        self.amend_add_btn_select_gp_practices.click()
        return self

    def click_amend_done_btn_gp_practices(self) -> CohortListPage:
        self.amend_done_btn_gp_practices.click()
        return self

    def enter_amend_expected_attendance_rate(
        self, attendance_rate: int
    ) -> CohortListPage:
        self.amend_attendance_rate_txtbox.fill(attendance_rate)
        return self

    def enter_amend_screening_cohort_name(self, amend_name: str) -> CohortListPage:
        self.amend_screening_cohort_name_txtbox.fill(amend_name)
        return self

    def click_filtered_cohort_pencil_icon(self) -> CohortListPage:
        self.filtered_cohort_pencil_icon.click()
        return self

    def click_amend_cohort_cancel_button(self) -> CohortListPage:
        self.amend_cohort_cancel_button.click()
        return self

    def enter_screening_cohort_name_field(self, cohort_name: str) -> CohortListPage:
        self.screening_cohort_name_txtbox.fill(cohort_name)
        return self

    def select_default_screening_location_dropdown(
        self, location_name: str
    ) -> CohortListPage:
        self.default_screening_location_dropdown.select_option(location_name)
        return self

    def select_default_screening_unit_dropdown(self, unit_name: str) -> CohortListPage:
        self.default_screening_unit_dropdown.select_option(unit_name)
        return self

    def click_select_gp_practices_btn(self) -> CohortListPage:
        self.select_gp_practices_btn.click()
        return self

    def click_create_screening_cohort_save_btn(self) -> CohortListPage:
        self.create_screening_cohort_save_btn.click()
        return self

    def enter_gp_practice_name_field(self, gp_name: str) -> CohortListPage:
        self.gp_practice_name_field.fill(gp_name)
        return self

    def enter_gp_code_field(self, gp_code: str) -> CohortListPage:
        self.gp_code_field.fill(gp_code)
        return self

    def click_on_cancel_creating_screening_cohort(self) -> CohortListPage:
        self.cancel_creating_screening_cohort.click()
        return self

    def click_add_btn_gp_practices_to_include(self) -> CohortListPage:
        self.add_gp_practices_to_include.click()
        return self

    def verify_add_btn_gp_practices_not_to_be_present(self) -> CohortListPage:
        expect(self.add_gp_practices_to_include).not_to_be_visible()
        return self

    def enter_expected_attendance_rate(self, attendance_rate: int) -> CohortListPage:
        self.expected_attendance_rate.fill(attendance_rate)
        return self

    def click_add_btn_to_select_outcode(self, outcode) -> CohortListPage:
        outcode_add_btn = self.page.locator(
            f"//tr[td[1][normalize-space()='{outcode}']]//button[text()='Add']"
        )
        outcode_add_btn.click()
        return self

    def click_remove_button_by_gp_code(self, gp_code) -> CohortListPage:
        # Use an XPath selector to find the "Remove" button in the same row where the first column text matches the gp_code
        remove_button = self.page.locator(
            f"//table[@id='practicesToIncludeList']//tr[td[normalize-space()='{gp_code}']]//button[text()='Remove']"
        )
        remove_button.click()
        return self

    def create_cohort_user2_bso2(self, cohort_name, location_name) -> CohortListPage:
        self.click_create_screening_cohort_by_gp_practice_btn()
        self.enter_screening_cohort_name_field(
            cohort_name
        ).enter_expected_attendance_rate("25")
        self.select_default_screening_location_dropdown(
            location_name
        ).select_default_screening_unit_dropdown("Batman")
        self.click_select_gp_practices_btn().enter_gp_code_field(
            "A00009"
        ).click_add_btn_gp_practices_to_include().click_done_btn_gp_practices_include_popup()
        self.click_create_screening_cohort_save_btn()
        self.page.wait_for_timeout(3000)
        return self

    def create_cohort(self, cohort_name, location_name) -> CohortListPage:
        self.click_create_screening_cohort_by_gp_practice_btn()
        self.enter_screening_cohort_name_field(
            cohort_name
        ).enter_expected_attendance_rate("25")
        self.select_default_screening_location_dropdown(
            location_name
        ).select_default_screening_unit_dropdown("Batman")
        self.click_select_gp_practices_btn().enter_gp_code_field(
            "A00005"
        ).click_add_btn_gp_practices_to_include().click_done_btn_gp_practices_include_popup()
        self.click_create_screening_cohort_save_btn()
        self.page.wait_for_timeout(3000)
        return self

    def create_cohort_without_gp(
        self, cohort_name, location_name, unit_name
    ) -> CohortListPage:
        self.click_create_screening_cohort_by_gp_practice_btn()
        self.enter_screening_cohort_name_field(
            cohort_name
        ).enter_expected_attendance_rate("25")
        self.select_default_screening_location_dropdown(
            location_name
        ).select_default_screening_unit_dropdown(unit_name)
        self.click_create_screening_cohort_save_btn()
        self.page.wait_for_timeout(3000)
        return self

    def create_cohort_outcode_without_gp(
        self, cohort_name, attendance_rate, location_name, unit_name
    ) -> CohortListPage:
        self.click_create_screening_cohort_by_outcode_btn()
        self.enter_screening_cohort_name_field(
            cohort_name
        ).enter_expected_attendance_rate(attendance_rate)
        self.select_default_screening_location_dropdown(
            location_name
        ).select_default_screening_unit_dropdown(unit_name)
        self.click_save_cohort_by_outcode_btn()
        self.page.wait_for_timeout(3000)
        return self

    def value_of_filtered_cohort_name(self):
        filterd_value = self.filtered_cohort_name.text_content()
        self.page.wait_for_timeout(4000)
        return filterd_value

    def value_of_filtered_attendance(self):
        filtered_value = self.amend_attendance_rate_txtbox.input_value()
        self.page.wait_for_timeout(4000)
        return filtered_value

    def click_done_btn_gp_practices_include_popup(self) -> CohortListPage:
        self.done_btn_gp_practices_incluse_popup.click()
        return self

    def enter_screening_cohort_name_filter(self, cohort_name: str) -> CohortListPage:
        self.screening_cohort_name_filter.fill(cohort_name)
        self.page.wait_for_timeout(4000)
        return self

    def enter_screening_location_filter(self, location_name: str) -> CohortListPage:
        self.screening_location_filter.fill(location_name)
        self.page.wait_for_timeout(3000)
        return self

    def enter_screening_unit_filter(self, unit_name: str) -> CohortListPage:
        self.screening_unit_filter.fill(unit_name)
        self.page.wait_for_timeout(3000)
        return self

    def select_cohort_type_dropdown(self, cohort_type: str) -> CohortListPage:
        self.page.locator("select#cohortTypeList").select_option(label=cohort_type)
        self.page.wait_for_timeout(3000)
        return self

    def dbl_click_on_filtered_cohort(self) -> CohortListPage:
        self.filtered_cohort_name.dblclick()
        return self

    def extract_cohort_paging_info(self) -> int:
        self.cohort_paging_info.scroll_into_view_if_needed()
        paging_info_text = self.cohort_paging_info.text_content()
        self.page.wait_for_timeout(3000)
        re_search_result = re.search(
            "Showing (\d+) to (\d+) of (\d+) entries", paging_info_text
        )
        return int(re_search_result.group(3))

    def screening_cohorts_count_in_db(self, db_util) -> int:
        result = db_util.get_results(
            """select count(1)
                    from rlp_cohorts where bso_organisation_id in(
                            select bso_organisation_id from bso_organisations where bso_organisation_code = 'LAV')
                    """
        )
        return result["count"][0]

    def extract_location_paging_list_count(self) -> int:
        self.location_paging_info.scroll_into_view_if_needed()
        paging_info_text = self.location_paging_info.text_content()
        self.page.wait_for_timeout(5000)
        re_search_result = re.search(
            "Showing (\d+) to (\d+) of (\d+) entries", paging_info_text
        )
        return int(re_search_result.group(3))

    def extract_paging_unit_list_count(self) -> int:
        self.page.locator("#screeningStatusList").select_option(label="All")
        self.unit_paging_info.scroll_into_view_if_needed()
        paging_info_text = self.unit_paging_info.text_content()
        self.page.wait_for_timeout(5000)
        re_search_result = re.search(
            "Showing (\d+) to (\d+) of (\d+) entries", paging_info_text
        )
        return int(re_search_result.group(3))

    def extract_paging_unit_list_count_active_only(self) -> int:
        self.page.locator("#screeningStatusList").select_option(label="Active")
        self.unit_paging_info.scroll_into_view_if_needed()
        paging_info_text = self.unit_paging_info.text_content()
        self.page.wait_for_timeout(5000)
        re_search_result = re.search(
            "Showing (\d+) to (\d+) of (\d+) entries", paging_info_text
        )
        return int(re_search_result.group(3))

    # Method to directly attempt to create the unit
    def create_unit_if_not_exists(self, unit_name: str) -> None:
        self.page.get_by_role("button", name="Add Screening Unit").click()
        self.page.locator("//input[@id='unitNameText']").fill(unit_name)
        self.page.wait_for_selector(
            f"//input[@id='unitTypeText' and @type='radio' and @value='MOBILE']"
        ).check()
        self.page.locator("#addButtonInAddUnitPopup").click()
        # Check for the error message indicating a duplicate unit
        try:
            self.page.wait_for_selector("p#error_unitNameText", timeout=3000)
            if (
                "Name is already in use by another unit"
                in self.error_message_locator.inner_text()
            ):
                # If the error message appears, click cancel to close the popup
                self.page.wait_for_selector("#cancelButtonInAddUnitPopup").click()
        except playwright._impl._errors.TimeoutError:
            # If no error message appears, assume the Unit was added successfully
            pass
        self.page.wait_for_timeout(5000)

    def create_unit_for_test_data(self, unit_name: str) -> None:
        self.page.get_by_role("button", name="Add Screening Unit").click()
        self.page.locator("//input[@id='unitNameText']").fill(unit_name)
        self.page.wait_for_selector(
            f"//input[@id='unitTypeText' and @type='radio' and @value='MOBILE']"
        ).check()
        self.page.locator("#addButtonInAddUnitPopup").click()
