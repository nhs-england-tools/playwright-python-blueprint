from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class FITTestKitsPage(BasePage):
    """FIT Test Kits Page locators, and methods for interacting with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Downloads Page
        self.fit_rollout_summary_page = self.page.get_by_role(
            "link", name="FIT Rollout Summary"
        )
        self.log_devices_page = self.page.get_by_role("link", name="Log Devices")
        self.view_fit_kit_result_page = self.page.get_by_role(
            "link", name="View FIT Kit Result"
        )
        self.kit_service_management_page = self.page.get_by_role(
            "link", name="Kit Service Management"
        )
        self.kit_result_audit_page = self.page.get_by_role(
            "link", name="Kit Result Audit"
        )
        self.view_algorithm_page = self.page.get_by_role("link", name="View Algorithm")
        self.view_screening_centre_fit_page = self.page.get_by_role(
            "link", name="View Screening Centre FIT"
        )
        self.screening_incidents_list_page = self.page.get_by_role(
            "link", name="Screening Incidents List"
        )
        self.manage_qc_products_page = self.page.get_by_role(
            "link", name="Manage QC Products"
        )
        self.maintain_analysers_page = self.page.get_by_role(
            "link", name="Maintain Analysers"
        )
        self.fit_device_id = self.page.get_by_role("textbox", name="FIT Device ID")
        self.fit_test_kits_title = self.page.locator("#ntshPageTitle")

        self.sc_fit_configuration_page_screening_centre_dropdown = page.locator(
            "#screeningCentres"
        )

    def verify_fit_test_kits_title(self) -> None:
        """Verifies that the FIT Test Kits page title is displayed correctly."""
        expect(self.fit_test_kits_title).to_contain_text("FIT Test Kits")

    def go_to_fit_rollout_summary_page(self) -> None:
        """Navigates to the FIT Rollout Summary page."""
        self.click(self.fit_rollout_summary_page)

    def go_to_log_devices_page(self) -> None:
        """Navigates to the Log Devices page."""
        self.click(self.log_devices_page)

    def go_to_view_fit_kit_result(self) -> None:
        """Navigates to the View FIT Kit Result page."""
        self.click(self.view_fit_kit_result_page)

    def go_to_kit_service_management(self) -> None:
        """Navigates to the Kit Service Management page."""
        self.click(self.kit_service_management_page)

    def go_to_kit_result_audit(self) -> None:
        """Navigates to the Kit Result Audit page."""
        self.click(self.kit_result_audit_page)

    def go_to_view_algorithm(self) -> None:
        """Navigates to the View Algorithm page."""
        self.click(self.view_algorithm_page)

    def go_to_view_screening_centre_fit(self) -> None:
        """Navigates to the View Screening Centre FIT page."""
        self.click(self.view_screening_centre_fit_page)

    def go_to_screening_incidents_list(self) -> None:
        """Navigates to the Screening Incidents List page."""
        self.click(self.screening_incidents_list_page)

    def go_to_manage_qc_products(self) -> None:
        """Navigates to the Manage QC Products page."""
        self.click(self.manage_qc_products_page)

    def go_to_maintain_analysers(self) -> None:
        """Navigates to the Maintain Analysers page."""
        self.click(self.maintain_analysers_page)

    def go_to_fit_device_id(self) -> None:
        """Navigates to the FIT Device ID field."""
        self.click(self.fit_device_id)
