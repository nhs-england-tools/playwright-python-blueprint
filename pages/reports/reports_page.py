from playwright.sync_api import Page
from pages.base_page import BasePage


class ReportsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

        # Reports page main menu links
        self.bureau_reports_link = self.page.get_by_text("Bureau Reports")
        self.failsafe_reports_link = self.page.get_by_role(
            "link", name="Failsafe Reports"
        )
        self.operational_reports_link = self.page.get_by_role(
            "link", name="Operational Reports"
        )
        self.strategic_reports_link = self.page.get_by_role(
            "link", name="Strategic Reports"
        )
        self.cancer_waiting_times_reports_link = self.page.get_by_role(
            "link", name="Cancer Waiting Times Reports"
        )
        self.dashboard_link = self.page.get_by_role("link", name="Dashboard")
        self.qa_report_dataset_completion_link = self.page.get_by_role(
            "link", name="QA Report : Dataset Completion"
        )

        # Reports pages shared buttons, locators & links
        self.refresh_page_button = self.page.get_by_role("button", name="Refresh")
        self.reports_update_button = self.page.get_by_role("button", name="Update")
        self.report_start_date_field = self.page.get_by_role(
            "textbox", name="Report Start Date"
        )
        self.qa_report_dataset_completion_link = self.page.get_by_text(
            "QA Report : Dataset Completion"
        )

        # Generate Report button locators
        self.generate_report_button = self.page.get_by_role(
            "button", name="Generate Report"
        )
        self.operational_reports_sp_appointments_generate_report_button = (
            self.page.locator("#submitThisForm")
        )

        # Set patients screening centre dropdown locators
        self.set_patients_screening_centre_dropdown = self.page.locator(
            "#cboScreeningCentre"
        )
        self.six_weeks_availability_not_set_up_set_patients_screening_centre_dropdown = self.page.get_by_label(
            "Screening Centre"
        )
        self.practitioner_appointments_set_patients_screening_centre_dropdown = (
            page.get_by_label("Screening Centre")
        )
        self.attendance_not_updated_set_patients_screening_centre_dropdown = (
            page.get_by_label("Screening Centre")
        )

        # Select screening practitioner dropdown locators
        self.screening_practitioner_dropdown = self.page.locator("#A_C_NURSE")

        # Report Timestamp locators
        self.common_report_timestamp_element = self.page.locator("b")
        self.subject_ceased_report_timestamp_element = self.page.locator(
            "#displayGenerateDate > tbody > tr > td > b"
        )
        self.fobt_logged_not_read_report_timestamp_element = self.page.locator(
            "#report-generated"
        )
        self.six_weeks_availability_not_set_up_report_timestamp_element = (
            self.page.locator("#displayGenerateDate")
        )

        # Failsafe Reports menu links
        self.date_report_last_requested_link = self.page.get_by_role(
            "link", name="Date Report Last Requested"
        )
        self.screening_subjects_with_inactive_open_episode_link = self.page.get_by_role(
            "link", name="Screening Subjects With"
        )
        self.subjects_ceased_due_to_date_of_birth_changes_link = self.page.get_by_role(
            "link", name="Subjects Ceased Due to Date"
        )
        self.allocate_sc_for_patient_movements_within_hub_boundaries_link = (
            self.page.get_by_role(
                "link", name="Allocate SC for Patient Movements within Hub Boundaries"
            )
        )
        self.allocate_sc_for_patient_movements_into_your_hub_link = (
            self.page.get_by_role(
                "link", name="Allocate SC for Patient Movements into your Hub"
            )
        )
        self.identify_and_link_new_gp_link = self.page.get_by_role(
            "link", name="Identify and link new GP"
        )

        # Operational Reports menu links
        self.appointment_attendance_not_updated_link = self.page.get_by_role(
            "link", name="Appointment Attendance Not"
        )
        self.fobt_kits_logged_but_not_read_link = self.page.get_by_role(
            "link", name="FOBT Kits Logged but Not Read"
        )
        self.demographic_update_inconsistent_with_manual_update_link = (
            self.page.get_by_role("link", name="Demographic Update")
        )
        self.screening_practitioner_6_weeks_availability_not_set_up_report_link = (
            page.get_by_role("link", name="Screening Practitioner 6")
        )
        self.screening_practitioner_appointments_link = self.page.get_by_role(
            "link", name="Screening Practitioner Appointments"
        )

    # Reports page main menu navigation
    def go_to_failsafe_reports_page(self) -> None:
        self.click(self.failsafe_reports_link)

    def go_to_operational_reports_page(self) -> None:
        self.click(self.operational_reports_link)

    def go_to_strategic_reports_page(self) -> None:
        self.click(self.strategic_reports_link)

    def go_to_cancer_waiting_times_reports_page(self) -> None:
        self.click(self.cancer_waiting_times_reports_link)

    def go_to_dashboard(self) -> None:
        self.click(self.dashboard_link)

    # Reports pages shared buttons and actions
    def click_refresh_button(self) -> None:
        self.click(self.refresh_page_button)

    def click_generate_report_button(self) -> None:
        self.click(self.generate_report_button)

    def click_reports_pages_update_button(self) -> None:
        self.click(self.reports_update_button)

    # Failsafe Reports menu links
    def go_to_date_report_last_requested_page(self) -> None:
        self.click(self.date_report_last_requested_link)

    def go_to_screening_subjects_with_inactive_open_episode_link_page(self) -> None:
        self.click(self.screening_subjects_with_inactive_open_episode_link)

    def go_to_subjects_ceased_due_to_date_of_birth_changes_page(self) -> None:
        self.click(self.subjects_ceased_due_to_date_of_birth_changes_link)

    def go_to_allocate_sc_for_patient_movements_within_hub_boundaries_page(
        self,
    ) -> None:
        self.click(self.allocate_sc_for_patient_movements_within_hub_boundaries_link)

    def go_to_allocate_sc_for_patient_movements_into_your_hub_page(self) -> None:
        self.click(self.allocate_sc_for_patient_movements_into_your_hub_link)

    def go_to_identify_and_link_new_gp_page(self) -> None:
        self.click(self.identify_and_link_new_gp_link)

    # Operational Reports menu links
    def go_to_appointment_attendance_not_updated_page(self) -> None:
        self.click(self.appointment_attendance_not_updated_link)

    def go_to_fobt_kits_logged_but_not_read_page(self) -> None:
        self.click(self.fobt_kits_logged_but_not_read_link)

    def go_to_demographic_update_inconsistent_with_manual_update_page(self) -> None:
        self.click(self.demographic_update_inconsistent_with_manual_update_link)

    def go_to_screening_practitioner_6_weeks_availability_not_set_up_report_page(
        self,
    ) -> None:
        self.click(
            self.screening_practitioner_6_weeks_availability_not_set_up_report_link
        )

    def go_to_screening_practitioner_appointments_page(self) -> None:
        self.click(self.screening_practitioner_appointments_link)

    def click_nhs_number_link(self, page: Page) -> None:
        """
        Clicks the first NHS number link present on the screen if any are found.
        """
        # List of locators to check for NHS number links.
        # This implementation is a workaround for the fact that the NHS number
        # links are not using the same locators accross bcss
        # This is a temporary solution until
        # we have a table utility that will allow us to interact with tables across bcss.
        locators = [
            "#listReportDataTable > tbody > tr:nth-child(3) > td:nth-child(1) > a",
            "//*[@id='listReportDataTable']/tbody/tr[3]/td[1]",
            "//*[@id='listReportDataTable']/tbody/tr[3]/td[2]",
            "#listReportDataTable > tbody > tr:nth-child(3) > td:nth-child(1) > a",
            "#subjInactiveOpenEpisodes > tbody > tr:nth-child(1) > td.NHS_NUMBER.dt-type-numeric > a",
        ]

        for locator_string in locators:
            try:
                # Use page.locator to get a locator object
                locator = page.locator(locator_string)
                # Check if the locator is visible
                if locator.is_visible():
                    # Click the locator
                    locator.click()
            except Exception:
                print("No NHS number links found on the page")
