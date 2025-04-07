from playwright.sync_api import Page, expect, Locator
from pages.base_page import BasePage
from enum import Enum


class SubjectScreeningSummary(BasePage):
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

    def verify_result_contains_text(self, text) -> None:
        expect(self.display_rs).to_contain_text(text)

    def verify_subject_search_results_title_subject_screening_summary(self) -> None:
        expect(self.subject_search_results_title).to_contain_text(
            "Subject Screening Summary"
        )

    def verify_subject_search_results_title_subject_search_results(self) -> None:
        expect(self.subject_search_results_title).to_contain_text(
            "Subject Search Results"
        )

    def get_latest_event_status_cell(self, latest_event_status: str) -> Locator:
        return self.page.get_by_role("cell", name=latest_event_status, exact=True)

    def verify_subject_screening_summary(self) -> None:
        expect(self.subject_screening_summary).to_be_visible()

    def verify_latest_event_status_header(self) -> None:
        expect(self.latest_event_status).to_be_visible()

    def verify_latest_event_status_value(self, latest_event_status: str) -> None:
        latest_event_status_cell = self.get_latest_event_status_cell(
            latest_event_status
        )
        expect(latest_event_status_cell).to_be_visible()

    def click_subjects_events_notes(self) -> None:
        self.click(self.subjects_events_notes)

    def click_list_episodes(self) -> None:
        self.click(self.list_episodes)

    def click_subject_demographics(self) -> None:
        self.click(self.subject_demographics)

    def click_datasets(self) -> None:
        self.click(self.datasets)

    def click_individual_letters(self) -> None:
        self.click(self.individual_letters)

    def click_patient_contacts(self) -> None:
        self.click(self.patient_contacts)

    def click_more(self) -> None:
        self.click(self.more)

    def click_update_subject_data(self) -> None:
        self.click(self.update_subject_data)

    def click_close_fobt_screening_episode(self) -> None:
        self.click(self.close_fobt_screening_episode)

    def go_to_a_page_to_advance_the_episode(self) -> None:
        self.click(self.a_page_to_advance_the_episode)

    def go_to_a_page_to_close_the_episode(self) -> None:
        self.click(self.a_page_to_close_the_episode)

    def select_change_screening_status(self, option: str) -> None:
        self.change_screening_status.select_option(option)

    def select_reason(self, option: str) -> None:
        self.reason.select_option(option)


class ChangeScreeningStatusOptions(Enum):
    SEEKING_FURTHER_DATA = "4007"


class ReasonOptions(Enum):
    UNCERTIFIED_DEATH = "11314"
