import logging
import pytest
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from typing import Dict

class SubjectEpisodeEventsAndNotesPage(BasePage):
    """Episode Events and Notes Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # List of episode events and notes - page locators
        self.latest_event_status_cell = self.page.locator(
            "table >> td.epihdr_data"
        ).nth(
            0
        )  # if it's the first one
        self.latest_event_cell = self.page.get_by_role(
            "cell", name="Record Diagnosis Date", exact=True
        )
        self.latest_diagnosis_cell = self.page.locator(
            "td[align='center']:has-text('Diag Date :')"
        )

        # Episode details (Replace with actual selectors only for scenario 17)
        self.latest_episode_status = self.page.locator("#latestEpisodeStatus")
        self.latest_episode_has_diagnosis_date = self.page.locator(
            "#latestEpisodeHasDiagnosisDate"
        )
        self.latest_episode_diagnosis_reason = self.page.locator(
            "#latestEpisodeDiagnosisDateReason"
        )
        self.process_sspi_update_button = self.page.get_by_text("Process SSPI Update")
        self.deduction_reason_dropdown = self.page.locator("#deductionReason")
        self.confirm_sspi_update_button = self.page.get_by_text("Confirm")

    def expected_episode_event_is_displayed(self, event_description: str) -> None:
        """Check if the expected episode event is displayed on the page."""
        expect(
            self.page.get_by_role("cell", name=event_description, exact=True)
        ).to_be_visible()

    def get_latest_event_details(self) -> dict:
        """
        Retrieves key details for the latest episode entry from the UI.

        Returns:
        dict: A dictionary containing the following keys:
            - "latest_event_status" (str): The current status text of the latest event.
            - "event" (str): A description or name of the latest event.
            - "item" (str): Details related to the latest diagnosis item.

        Raises:
        pytest.fail: If any of the UI elements cannot be read, the test fails immediately.
        """
        try:
            status_text = self.latest_event_status_cell.inner_text()
            event_text = self.latest_event_cell.inner_text()
            diagnosis_text = self.latest_diagnosis_cell.first.inner_text()
            logging.debug(f"DEBUG: {event_text}, {status_text}, {diagnosis_text}")
        except Exception as e:
            pytest.fail(f"Failed to read latest episode event details from UI: {e}")
        return {
            "latest_event_status": status_text,
            "event": event_text,
            "item": diagnosis_text,
        }

    def validate_event_status_is_not_A50(self, event_details: dict) -> None:
        """Validates that latest_event_status does not contain 'A50'."""
        latest_status = event_details.get("latest_event_status")
        logging.info(f"Validating Latest Event Status: {latest_status}")

        if latest_status is None:
            pytest.fail("Missing 'latest_event_status' in event_details.")
        elif "A50" in str(latest_status):
            pytest.fail(
                f"Invalid status detected: 'A50' is not allowed. Received: '{latest_status}'"
            )
        logging.info(f"Status '{latest_status}' is allowed.")

    def is_record_diagnosis_date_option_available(self) -> bool:
        """
        Check if the 'Record Diagnosis Date' option is available on the page

        Returns:
            bool: True if the option is available, False otherwise.
        """
        try:
            return self.page.get_by_role(
                "button", name="Record Diagnosis Date"
            ).is_visible()
        except Exception as e:
            logging.error(f"Record Diagnosis Date option not found: {e}")
            return False

    def is_amend_diagnosis_date_option_available(self) -> bool:
        """
        Check if the 'Amend Diagnosis Date' option is available on the page.

        Returns:
            bool: True if the option is available, False otherwise.
        """
        try:
            return self.page.get_by_role(
                "button", name="Amend Diagnosis Date"
            ).is_visible()
        except Exception as e:
            logging.error(f"Error checking for 'Amend Diagnosis Date' option: {e}")
            return False

    def process_sspi_update_for_death(self, deduction_reason: str) -> None:
        """
        Submits an SSPI update for a death-related deduction reason through the UI workflow.

        Args:
        deduction_reason (str): The label of the deduction reason to select from the dropdown.

        Steps:
        - Clicks the SSPI update button.
        - Selects the specified deduction reason from the dropdown.
        - Confirms the SSPI update by clicking the confirmation button.
        """
        self.process_sspi_update_button.click()
        self.deduction_reason_dropdown.select_option(label=deduction_reason)
        self.confirm_sspi_update_button.click()

    def get_latest_episode_details(self) -> Dict[str, str]:
        """
        Retrieve details of the latest episode from the UI elements.

        Returns:
            Dict[str, str]: A dictionary containing:
                - 'latest_episode_status': The status text of the latest episode.
                - 'latest_episode_has_diagnosis_date': Indicator of whether a diagnosis date is present.
                - 'latest_episode_diagnosis_date_reason': Reason explaining the diagnosis date status.
        """
        return {
            "latest_episode_status": self.latest_episode_status.inner_text(),
            "latest_episode_has_diagnosis_date": self.latest_episode_has_diagnosis_date.inner_text(),
            "latest_episode_diagnosis_date_reason": self.latest_episode_diagnosis_reason.inner_text(),
        }
