from playwright.sync_api import Page, expect, Locator
from pages.base_page import BasePage
from enum import Enum
import logging
import pytest


class SubjectScreeningSummaryPage(BasePage):
    """Subject Screening Summary Page locators, and methods for interacting with the page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Subject Screening Summary - page filters
        self.subject_screening_summary = self.page.get_by_role(
            "cell", name="Subject Screening Summary", exact=True
        )
        self.latest_event_status = self.page.get_by_role(
            "cell", name="Latest Event Status", exact=True
        )
        self.subjects_events_notes = self.page.get_by_role(
            "link", name="Subject Events & Notes"
        )
        self.list_episodes = self.page.get_by_role("link", name="List Episodes")
        self.episodes_list_expander_icon = self.page.locator("#ID_LINK_EPISODES_img")
        self.subject_demographics = self.page.get_by_role(
            "link", name="Subject Demographics"
        )
        self.datasets = self.page.get_by_role("link", name="Datasets")
        self.individual_letters = self.page.get_by_role(
            "link", name="Individual Letters"
        )
        self.patient_contacts = self.page.get_by_role("link", name="Patient Contacts")
        self.more = self.page.get_by_role("link", name="more")
        self.change_screening_status = self.page.get_by_label("Change Screening Status")
        self.reason = self.page.get_by_label("Reason", exact=True)
        self.update_subject_data = self.page.get_by_role(
            "button", name="Update Subject Data"
        )
        self.close_fobt_screening_episode = self.page.get_by_role(
            "button", name="Close FOBT Screening Episode"
        )
        self.a_page_to_advance_the_episode = self.page.get_by_text(
            "go to a page to Advance the"
        )
        self.a_page_to_close_the_episode = self.page.get_by_text(
            "go to a page to Close the"
        )
        self.subject_search_results_title = self.page.locator("#ntshPageTitle")
        self.display_rs = self.page.locator("#displayRS")
        self.first_fobt_episode_link = page.get_by_role(
            "link", name="FOBT Screening"
        ).first
        self.datasets_link = self.page.get_by_role("link", name="Datasets")
        self.advance_fobt_screening_episode_button = self.page.get_by_role(
            "button", name="Advance FOBT Screening Episode"
        )

    def verify_result_contains_text(self, text) -> None:
        """Verify that the result contains the given text."""
        expect(self.display_rs).to_contain_text(text)

    def verify_subject_search_results_title_subject_screening_summary(self) -> None:
        """Verify that the subject search results title contains 'Subject Screening Summary'."""
        expect(self.subject_search_results_title).to_contain_text(
            "Subject Screening Summary"
        )

    def verify_subject_search_results_title_subject_search_results(self) -> None:
        """Verify that the subject search results title contains 'Subject Search Results'."""
        expect(self.subject_search_results_title).to_contain_text(
            "Subject Search Results"
        )

    def get_latest_event_status_cell(self, latest_event_status: str) -> Locator:
        """Get the latest event status cell by its name."""
        return self.page.get_by_role("cell", name=latest_event_status, exact=True)

    def verify_subject_screening_summary(self) -> None:
        """Verify that the subject screening summary is visible."""
        expect(self.subject_screening_summary).to_be_visible()

    def verify_latest_event_status_header(self) -> None:
        """Verify that the latest event status header is visible."""
        expect(self.latest_event_status).to_be_visible()

    def verify_latest_event_status_value(self, latest_event_status: str | list) -> None:
        """Verify that the latest event status value is visible."""
        latest_event_status_locator = self.get_visible_status_from_list(
            latest_event_status
        )
        status = latest_event_status_locator.inner_text()
        logging.info(f"Verifying subject has the status: {status}")
        try:
            expect(latest_event_status_locator).to_be_visible()
            logging.info(f"Subject has the status: {status}")
        except Exception:
            pytest.fail(f"Subject does not have the status: {status}")

    def get_visible_status_from_list(self, latest_event_status) -> Locator:
        """
        Get the first visible status from the latest event status string or list.

        Args:
            latest_event_status (str | list): The latest event status to check.

        Returns:
            Locator: The locator for the first visible status.
        """
        if isinstance(latest_event_status, str):
            latest_event_status = [latest_event_status]
        for status in latest_event_status:
            locator = self.page.get_by_role("cell", name=status, exact=True)
            if locator.is_visible():
                return locator
        logging.error("Unable to find any of the listed statuses")

    def click_subjects_events_notes(self) -> None:
        """Click on the 'Subject Events & Notes' link."""
        self.click(self.subjects_events_notes)

    def click_list_episodes(self) -> None:
        """Click on the 'List Episodes' link."""
        self.click(self.list_episodes)

    def click_subject_demographics(self) -> None:
        """Click on the 'Subject Demographics' link."""
        self.click(self.subject_demographics)

    def click_datasets(self) -> None:
        """Click on the 'Datasets' link."""
        self.click(self.datasets)

    def click_individual_letters(self) -> None:
        """Click on the 'Individual Letters' link."""
        self.click(self.individual_letters)

    def click_patient_contacts(self) -> None:
        """Click on the 'Patient Contacts' link."""
        self.click(self.patient_contacts)

    def click_more(self) -> None:
        """Click on the 'More' link."""
        self.click(self.more)

    def click_update_subject_data(self) -> None:
        """Click on the 'Update Subject Data' button."""
        self.click(self.update_subject_data)

    def click_close_fobt_screening_episode(self) -> None:
        """Click on the 'Close FOBT Screening Episode' button."""
        self.click(self.close_fobt_screening_episode)

    def go_to_a_page_to_advance_the_episode(self) -> None:
        """Click on the link to go to a page to advance the episode."""
        self.click(self.a_page_to_advance_the_episode)

    def go_to_a_page_to_close_the_episode(self) -> None:
        """Click on the link to go to a page to close the episode."""
        self.click(self.a_page_to_close_the_episode)

    def select_change_screening_status(self, option: str) -> None:
        """Select the given 'change screening status' option."""
        self.change_screening_status.select_option(option)

    def select_reason(self, option: str) -> None:
        """Select the given 'reason' option."""
        self.reason.select_option(option)

    def expand_episodes_list(self) -> None:
        """Click on the episodes list expander icon."""
        self.click(self.episodes_list_expander_icon)

    def click_first_fobt_episode_link(self) -> None:
        """Click on the first FOBT episode link."""
        self.click(self.first_fobt_episode_link)

    def click_datasets_link(self) -> None:
        """Click on the 'Datasets' link."""
        self.click(self.datasets_link)

    def click_advance_fobt_screening_episode_button(self) -> None:
        """Click on the 'Advance FOBT Screening Episode' button."""
        logging.info("Advancing the episode")
        try:
            self.click(self.advance_fobt_screening_episode_button)
            logging.info("Episode successfully advanced")
        except Exception as e:
            pytest.fail(f"Unable to advance the episode: {e}")


class ChangeScreeningStatusOptions(Enum):
    """Enum for Change Screening Status options."""

    SEEKING_FURTHER_DATA = "4007"


class ReasonOptions(Enum):
    """Enum for Reason options."""

    UNCERTIFIED_DEATH = "11314"
