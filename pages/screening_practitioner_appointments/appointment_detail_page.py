from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from enum import StrEnum


class AppointmentDetailPage(BasePage):
    """Appointment Detail Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Appointment Detail - page filters
        self.attendance_radio = self.page.get_by_role("radio", name="Attendance")
        self.attended_check_box = self.page.locator("#UI_ATTENDED")
        self.calendar_button = self.page.get_by_role("button", name="Calendar")
        self.save_button = self.page.get_by_role("button", name="Save")
        self.cancel_radio = self.page.get_by_role("radio", name="Cancel")
        self.reason_for_cancellation_dropdown = self.page.get_by_label(
            "Reason for Cancellation"
        )

    def check_attendance_radio(self) -> None:
        """Checks the attendance radio button."""
        self.attendance_radio.check()

    def check_attended_check_box(self) -> None:
        """Checks the attended check box."""
        self.attended_check_box.check()

    def click_calendar_button(self) -> None:
        """Clicks the calendar button."""
        self.click(self.calendar_button)

    def click_save_button(self, accept_dialog: bool = False) -> None:
        """
        Clicks the save button.
        Args:
            accept_dialog (bool): Whether to accept the dialog.
        """
        if accept_dialog:
            self.safe_accept_dialog(self.save_button)
        else:
            self.click(self.save_button)

    def verify_text_visible(self, text: str) -> None:
        """Verifies that the specified text is visible on the page."""
        expect(self.page.get_by_text(text)).to_be_visible()

    def wait_for_attendance_radio(self, timeout_duration: float = 30000) -> None:
        """
        Waits for the attendance radio to be visible. Refreshes the page every minute if not visible.
        Default timeout is 30 seconds but this can be changed.

        Args:
            timeout_duration (float): How long to wait in milliseconds.
        """
        elapsed = 0
        refresh_interval = 60000  # 1 minute in milliseconds
        while elapsed < timeout_duration:
            try:
                self.attendance_radio.wait_for(
                    timeout=min(refresh_interval, timeout_duration - elapsed)
                )
                return
            except Exception:
                elapsed += refresh_interval
                if elapsed < timeout_duration:
                    self.page.reload()
        # Final attempt, will raise if not found
        self.attendance_radio.wait_for(
            timeout=(
                timeout_duration - elapsed if timeout_duration - elapsed > 0 else 1000
            )
        )

    def check_cancel_radio(self) -> None:
        """Checks the cancel radio button."""
        self.cancel_radio.check()

    def select_reason_for_cancellation_option(self, option: str) -> None:
        """
        Selects the reason for cancellation from the dropdown.
        Args:
            option: The reason for cancellation to select.
            The options are in the ReasonForCancellationOptions class
        """
        self.reason_for_cancellation_dropdown.select_option(value=option)


class ReasonForCancellationOptions(StrEnum):
    """Enum for cancellation reason options"""

    PATIENT_REQUESTS_DISCHARGE_FROM_SCREENING = "6008"
    PATIENT_UNSUITABLE_RECENTLY_SCREENED = "6007"
    PATIENT_UNSUITABLE_CURRENTLY_UNDERGOING_TREATMENT = "6006"
    PATIENT_CANCELLED_TO_CONSIDER = "6005"
    PATIENT_CANCELLED_MOVED_OUT_OF_AREA = "6003"
    SCREENING_CENTRE_CANCELLED_OTHER_REASON = "6002"
    CLINIC_UNAVAILABLE = "6001"
    PRACTITIONER_UNAVAILABLE = "6000"
    PATIENT_CANCELLED_OTHER_REASON = "6004"
