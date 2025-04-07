from playwright.sync_api import Page
from pages.base_page import BasePage


class ReportsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        # Reports page main menu links
        self.bureau_reports_page = self.page.get_by_role("link", name="Bureau Reports")
        self.failsafe_reports_page = self.page.get_by_role(
            "link", name="Failsafe Reports"
        )
        self.operational_reports_page = self.page.get_by_role(
            "link", name="Operational Reports"
        )
        self.strategic_reports_page = self.page.get_by_role(
            "link", name="Strategic Reports"
        )
        self.cancer_waiting_times_reports_page = self.page.get_by_role(
            "link", name="Cancer Waiting Times Reports"
        )
        self.dashboard = self.page.get_by_role("link", name="Dashboard")
        self.qa_report_dataset_completion_page = self.page.get_by_role(
            "link", name="QA Report : Dataset Completion"
        )
        # Reports pages shared buttons & links
        self.refresh_page_button = self.page.get_by_role("button", name="Refresh")
        self.generate_report_button = self.page.get_by_role(
            "button", name="Generate Report"
        )
        self.reports_update_button = self.page.get_by_role("button", name="Update")
        self.report_timestamp_element = self.page.locator("b")
        self.set_patients_screening_centre_dropdown = self.page.locator(
            "#cboScreeningCentre"
        )

        # Failsafe Reports menu links
        self.date_report_last_requested_page = self.page.get_by_role(
            "link", name="Date Report Last Requested"
        )
        self.screening_subjects_with_inactive_open_episode_link_page = (
            self.page.get_by_role("link", name="Screening Subjects With")
        )
        self.subjects_ceased_due_to_date_of_birth_changes_page = self.page.get_by_role(
            "link", name="Subjects Ceased Due to Date"
        )
        self.allocate_sc_for_patient_movements_within_hub_boundaries_page = (
            self.page.get_by_role(
                "link", name="Allocate SC for Patient Movements within Hub Boundaries"
            )
        )
        self.allocate_sc_for_patient_movements_into_your_hub_page = (
            self.page.get_by_role(
                "link", name="Allocate SC for Patient Movements into your Hub"
            )
        )
        self.identify_and_link_new_gp_page = self.page.get_by_role(
            "link", name="Identify and link new GP"
        )
        # Operational Reports menu links
        self.appointment_attendance_not_updated_page = self.page.get_by_role(
            "link", name="Appointment Attendance Not"
        )
        self.fobt_kits_logged_but_not_read_page = self.page.get_by_role(
            "link", name="FOBT Kits Logged but Not Read"
        )
        self.demographic_update_inconsistent_with_manual_update_page = (
            self.page.get_by_role("link", name="Demographic Update")
        )
        self.screening_practitioner_6_weeks_availability_not_set_up_report_page = (
            page.get_by_role("link", name="Screening Practitioner 6")
        )
        self.screening_practitioner_appointments_page = self.page.get_by_role(
            "link", name="Screening Practitioner Appointments"
        )

    # Reports page main menu links
    def go_to_failsafe_reports_page(self) -> None:
        self.click(self.failsafe_reports_page)

    def go_to_operational_reports_page(self) -> None:
        self.click(self.operational_reports_page)

    def go_to_strategic_reports_page(self) -> None:
        self.click(self.strategic_reports_page)

    def go_to_cancer_waiting_times_reports_page(self) -> None:
        self.click(self.cancer_waiting_times_reports_page)

    def go_to_dashboard(self) -> None:
        self.click(self.dashboard)

    # Reports pages shared buttons actions
    def click_refresh_button(self) -> None:
        self.click(self.refresh_page_button)

    def click_generate_report_button(self) -> None:
        self.click(self.generate_report_button)

    def click_reports_pages_update_button(self) -> None:
        self.click(self.reports_update_button)

    # Failsafe Reports menu links
    def go_to_date_report_last_requested_page(self) -> None:
        self.click(self.date_report_last_requested_page)

    def go_to_screening_subjects_with_inactive_open_episode_link_page(self) -> None:
        self.click(self.screening_subjects_with_inactive_open_episode_link_page)

    def go_to_subjects_ceased_due_to_date_of_birth_changes_page(self) -> None:
        self.click(self.subjects_ceased_due_to_date_of_birth_changes_page)

    def go_to_allocate_sc_for_patient_movements_within_hub_boundaries_page(
        self,
    ) -> None:
        self.click(self.allocate_sc_for_patient_movements_within_hub_boundaries_page)

    def go_to_allocate_sc_for_patient_movements_into_your_hub_page(self) -> None:
        self.click(self.allocate_sc_for_patient_movements_into_your_hub_page)

    def go_to_identify_and_link_new_gp_page(self) -> None:
        self.click(self.identify_and_link_new_gp_page)

    # Operational Reports menu links
    def go_to_appointment_attendance_not_updated_page(self) -> None:
        self.click(self.appointment_attendance_not_updated_page)

    def go_to_fobt_kits_logged_but_not_read_page(self) -> None:
        self.click(self.fobt_kits_logged_but_not_read_page)

    def go_to_demographic_update_inconsistent_with_manual_update_page(self) -> None:
        self.click(self.demographic_update_inconsistent_with_manual_update_page)

    def go_to_screening_practitioner_6_weeks_availability_not_set_up_report_page(
        self,
    ) -> None:
        self.click(
            self.screening_practitioner_6_weeks_availability_not_set_up_report_page
        )

    def go_to_screening_practitioner_appointments_page(self) -> None:
        self.click(self.screening_practitioner_appointments_page)
