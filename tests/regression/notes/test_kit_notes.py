import logging
import pytest
from playwright.sync_api import Page, expect
from utils.user_tools import UserTools
from pages.base_page import BasePage
from pages.screening_subject_search.subject_screening_search_page import (
    SubjectScreeningPage,
)
from utils.screening_subject_page_searcher import search_subject_episode_by_nhs_number
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from pages.screening_subject_search.subject_events_notes import (
    NotesOptions,
    NotesStatusOptions,
    SubjectEventsNotes,
)
from utils.oracle.oracle_specific_functions import get_subjects_by_note_count
from utils.subject_notes import (
    fetch_supporting_notes_from_db,
    verify_note_content_matches_expected,
    verify_note_content_ui_vs_db,
)


@pytest.mark.regression
@pytest.mark.note_tests
def test_subject_does_not_have_a_kit_note(page: Page, general_properties: dict) -> None:
    """
    Test to check if I can identify if a subject does not have a kit note
    """
    logging.info(
        f"Starting test: Verify subject does not have a '{general_properties["kit_note_name"]}'."
    )
    UserTools.user_login(page, "ScreeningAssistant at BCS02")
    BasePage(page).go_to_screening_subject_search_page()

    # Search for the subject by NHS Number.")
    subjects_df = get_subjects_by_note_count(
        general_properties["kit_note_type_value"],
        general_properties["note_status_active"],
        0,
    )
    if subjects_df.empty:
        pytest.fail(
            f"No subjects found without '{general_properties["kit_note_name"]}'."
        )

    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    search_subject_episode_by_nhs_number(page, nhs_no)
    # Verify no kit notes are present
    logging.info(
        f"Verified that no '{general_properties['kit_note_name']}' link is visible for the subject."
    )
    # logging.info("Verifying that no kit notes are present for the subject.")
    SubjectScreeningSummaryPage(page).verify_note_link_not_present(
        general_properties["kit_note_name"]
    )


@pytest.mark.regression
@pytest.mark.note_tests
def test_add_a_kit_note_for_a_subject_without_a_note(
    page: Page, general_properties: dict
) -> None:
    """
    Test to add a note for a subject without a kit note.
    """
    # User login
    logging.info(
        "Starting test: Add a '{general_properties['kit_note_name']}'  for a subject without a note."
    )
    UserTools.user_login(page, "Team Leader at BCS01")
    BasePage(page).go_to_screening_subject_search_page()

    # Get a subject with no notes of the specified type
    subjects_df = get_subjects_by_note_count(
        general_properties["kit_note_type_value"],
        general_properties["note_status_active"],
        0,
    )
    if subjects_df.empty:
        pytest.fail(
            f"No subjects found for note type {general_properties["kit_note_type_value"]}."
        )
    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    search_subject_episode_by_nhs_number(page, nhs_no)

    # Navigate to Subject Events & Notes
    logging.info("Navigating to 'Subject Events & Notes' for the selected subject.")
    SubjectScreeningSummaryPage(page).click_subjects_events_notes()

    # note type selection
    logging.info(
        f"Selecting note type based on value: '{general_properties["kit_note_type_value"]}'."
    )
    SubjectEventsNotes(page).select_kit_note()
    # Set the note status
    note_title = "kit Note - General observation title"
    logging.info(f"Filling in notes: '{note_title}'.")
    SubjectEventsNotes(page).fill_note_title(note_title)
    # Set the note type for verification
    note_text = "kit Note - General observation"
    logging.info(f"Filling in notes: '{note_text}'.")
    SubjectEventsNotes(page).fill_notes(note_text)
    # Accept dialog and update notes
    logging.info("Accepting dialog and clicking 'Update Notes'.")
    SubjectEventsNotes(page).accept_dialog_and_update_notes()

    # Get supporting notes for the subject from DB
    _, type_id, notes_df = fetch_supporting_notes_from_db(
        subjects_df, nhs_no, general_properties["note_status_active"]
    )
    # Verify title and note match the provided values
    verify_note_content_matches_expected(notes_df, note_title, note_text, type_id)

    logging.info(
        f"Verification successful: Kit note added for the subject with NHS Number: {nhs_no}. "
        f"Title and note matched the provided values. Title: '{note_title}', Note: '{note_text}'."
    )


@pytest.mark.regression
@pytest.mark.note_tests
def test_identify_subject_with_kit_note(page: Page, general_properties: dict) -> None:
    """
    Test to identify if a subject has a kit note.
    """
    logging.info("Starting test: Verify subject has a kit note.")
    UserTools.user_login(page, "ScreeningAssistant at BCS02")
    BasePage(page).go_to_screening_subject_search_page()

    # Search for the subject by NHS Number.")
    subjects_df = get_subjects_by_note_count(
        general_properties["kit_note_type_value"],
        general_properties["note_status_active"],
        1,
    )
    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    search_subject_episode_by_nhs_number(page, nhs_no)
    # Verify subject has kit notes  present
    logging.info("Verified: kit notes are present for the subject.")
    # logging.info("Verifying that  kit notes are present for the subject.")
    SubjectScreeningSummaryPage(page).verify_note_link_present(
        general_properties["kit_note_name"]
    )


@pytest.mark.regression
@pytest.mark.note_tests
def test_view_active_kit_note(page: Page, general_properties: dict) -> None:
    """
    Test to verify if an active kit note is visible for a subject.
    """
    logging.info("Starting test: Verify subject has kit care note.")
    UserTools.user_login(page, "ScreeningAssistant at BCS02")
    BasePage(page).go_to_screening_subject_search_page()

    # Search for the subject by NHS Number.")
    subjects_df = get_subjects_by_note_count(
        general_properties["kit_note_type_value"], 1
    )
    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    search_subject_episode_by_nhs_number(page, nhs_no)
    # Verify subject has kit notes  present
    logging.info("Verified: kit notes are present for the subject.")
    # logging.info("Verifying that  kit notes are present for the subject.")
    logging.info(
        f"Verifying that the kit Note is visible for the subject with NHS Number: {nhs_no}."
    )
    SubjectScreeningSummaryPage(page).verify_note_link_present(
        general_properties["kit_note_name"]
    )

    SubjectScreeningSummaryPage(page).click_subjects_events_notes()
    SubjectEventsNotes(page).select_note_type(NotesOptions.KIT_NOTE)

    # Get supporting notes for the subject
    _, _, notes_df = fetch_supporting_notes_from_db(
        subjects_df, nhs_no, general_properties["note_status_active"]
    )
    verify_note_content_ui_vs_db(
        page, notes_df, title_prefix_to_strip="Subject Kit Note -"
    )


@pytest.mark.regression
@pytest.mark.note_tests
def test_update_existing_kit_note(page: Page, general_properties: dict) -> None:
    """
    Test to verify if an existing kit note can be updated successfully.
    """
    logging.info("Starting test: Verify subject has a kit note.")
    UserTools.user_login(page, "Team Leader at BCS01")
    BasePage(page).go_to_screening_subject_search_page()
    # Search for the subject by NHS Number.")
    subjects_df = get_subjects_by_note_count(
        general_properties["kit_note_type_value"],
        general_properties["note_status_active"],
        1,
    )
    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    search_subject_episode_by_nhs_number(page, nhs_no)
    # Verify subject has additional care notes  present
    logging.info(
        f"Verifying that the kit Note is visible for the subject with NHS Number: {nhs_no}."
    )
    SubjectScreeningSummaryPage(page).verify_note_link_present(
        general_properties["kit_note_name"]
    )
    SubjectScreeningSummaryPage(page).click_subjects_events_notes()
    SubjectEventsNotes(page).select_note_type(NotesOptions.KIT_NOTE)
    BasePage(page).safe_accept_dialog_select_option(
        SubjectEventsNotes(page).note_status, NotesStatusOptions.INVALID
    )
    SubjectEventsNotes(page).fill_note_title("updated kit title")
    SubjectEventsNotes(page).fill_notes("updated kit note")
    SubjectEventsNotes(page).accept_dialog_and_add_replacement_note()

    # Get updated supporting notes for the subject
    _, type_id, notes_df = fetch_supporting_notes_from_db(
        subjects_df, nhs_no, general_properties["note_status_active"]
    )
    # Verify title and note match the provided values
    logging.info("Verifying that the updated title and note match the provided values.")

    # Define the expected title and note
    note_title = "updated kit title"
    note_text = "updated kit note"
    # Log the expected title and note
    logging.info(f"Expected title: '{note_title}'")
    logging.info(f"Expected note: '{note_text}'")

    # Ensure the filtered DataFrame is not empty
    if notes_df.empty:
        pytest.fail(
            f"No notes found for type_id: {general_properties["kit_note_type_value"]}. Expected at least one updated note."
        )

    # Verify title and note match the provided values
    verify_note_content_matches_expected(notes_df, note_title, note_text, type_id)

    logging.info(
        f"Verification successful:Kit note added for the subject with NHS Number: {nhs_no}. "
        f"Title and note matched the provided values. Title: '{note_title}', Note: '{note_text}'."
    )
