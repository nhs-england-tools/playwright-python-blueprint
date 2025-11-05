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
from pages.screening_subject_search.subject_events_notes_page import (
    NotesOptions,
    NotesStatusOptions,
    SubjectEventsNotesPage,
)
from utils.oracle.oracle_specific_functions.subject_notes import (
    get_subjects_by_note_count,
    get_subjects_with_multiple_notes,
)
from utils.subject_notes import (
    fetch_supporting_notes_from_db,
    verify_note_content_matches_expected,
    verify_note_content_ui_vs_db,
    verify_note_removal_and_obsolete_transition,
)


@pytest.mark.regression
@pytest.mark.note_tests
def test_subject_does_not_have_a_subject_note(
    page: Page, general_properties: dict
) -> None:
    """
    Test to check if I can identify if a subject does not have a Subject note
    """
    logging.info(
        f"Starting test: Verify subject does not have a '{general_properties["subject_note_name"]}'."
    )
    UserTools.user_login(page, "ScreeningAssistant at BCS02")
    BasePage(page).go_to_screening_subject_search_page()

    # Search for the subject by NHS Number.")
    subjects_df = get_subjects_by_note_count(
        general_properties["subject_note_type_value"],
        general_properties["note_status_active"],
        0,
    )
    if subjects_df.empty:
        pytest.fail(
            f"No subjects found without '{general_properties["subject_note_name"]}'."
        )

    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    search_subject_episode_by_nhs_number(page, nhs_no)
    # Verify no subject notes are present
    logging.info(
        f"Verified that no '{general_properties['subject_note_name']}' link is visible for the subject."
    )
    # logging.info("Verifying that no subject  notes are present for the subject.")
    SubjectScreeningSummaryPage(page).verify_note_link_not_present(
        general_properties["subject_note_name"]
    )


@pytest.mark.regression
@pytest.mark.note_tests
def test_add_a_subject_note_for_a_subject_without_a_note(
    page: Page, general_properties: dict
) -> None:
    """
    Test to add a note for a subject without a subject note.
    """
    # User login
    logging.info(
        "Starting test: Add a '{general_properties['subject_note_name']}'  for a subject without a note."
    )
    UserTools.user_login(page, "Team Leader at BCS01")
    BasePage(page).go_to_screening_subject_search_page()

    # Get a subject with no notes of the specified type
    subjects_df = get_subjects_by_note_count(
        general_properties["subject_note_type_value"],
        general_properties["note_status_active"],
        0,
    )
    if subjects_df.empty:
        pytest.fail(
            f"No subjects found for note type {general_properties["subject_note_type_value"]}."
        )
    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    logging.info(f"Searching for subject with NHS Number: {nhs_no}")
    search_subject_episode_by_nhs_number(page, nhs_no)

    # Navigate to Subject Events & Notes
    logging.info("Navigating to 'Subject Events & Notes' for the selected subject.")
    SubjectScreeningSummaryPage(page).click_subjects_events_notes()

    # note type selection
    logging.info(
        f"Selecting note type based on value: '{general_properties["subject_note_type_value"]}'."
    )
    SubjectEventsNotesPage(page).select_subject_note()
    # Set the note status
    note_title = "Subject Note - General observation title"
    logging.info(f"Filling in notes: '{note_title}'.")
    SubjectEventsNotesPage(page).fill_note_title(note_title)
    # Set the note type for verification
    note_text = "Subject Note - General observation"
    logging.info(f"Filling in notes: '{note_text}'.")
    SubjectEventsNotesPage(page).fill_notes(note_text)
    # Dismiss dialog and update notes
    logging.info("Dismissing dialog and clicking 'Update Notes'.")
    SubjectEventsNotesPage(page).accept_dialog_and_update_notes()

    # Get supporting notes for the subject from DB
    _, type_id, notes_df = fetch_supporting_notes_from_db(
        subjects_df, nhs_no, general_properties["note_status_active"]
    )
    # Verify title and note match the provided values
    verify_note_content_matches_expected(notes_df, note_title, note_text, type_id)
    logging.info(
        f"Verification successful: subject note added for the subject with NHS Number: {nhs_no}. "
        f"Title and note matched the provided values. Title: '{note_title}', Note: '{note_text}'."
    )


@pytest.mark.regression
@pytest.mark.note_tests
def test_identify_subject_with_subject_note(
    page: Page, general_properties: dict
) -> None:
    """
    Test to identify if a subject has an subject note.
    """
    logging.info("Starting test: Verify subject has a subject note.")
    UserTools.user_login(page, "ScreeningAssistant at BCS02")
    BasePage(page).go_to_screening_subject_search_page()

    # Search for the subject by NHS Number.")
    subjects_df = get_subjects_by_note_count(
        general_properties["subject_note_type_value"],
        general_properties["note_status_active"],
        1,
    )
    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    search_subject_episode_by_nhs_number(page, nhs_no)
    # Verify subject has subject notes  present
    logging.info("Verified: Subject notes are present for the subject.")
    # logging.info("Verifying that  additional care notes are present for the subject.")
    SubjectScreeningSummaryPage(page).verify_note_link_present(
        general_properties["subject_note_name"]
    )


@pytest.mark.regression
@pytest.mark.note_tests
def test_view_active_subject_note(page: Page, general_properties: dict) -> None:
    """
    Test to verify if an active subject note is visible for a subject.
    """
    logging.info("Starting test: Verify subject has subject  note.")
    UserTools.user_login(page, "ScreeningAssistant at BCS02")
    BasePage(page).go_to_screening_subject_search_page()

    # Search for the subject by NHS Number.")
    subjects_df = get_subjects_by_note_count(
        general_properties["subject_note_type_value"], 1
    )
    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    search_subject_episode_by_nhs_number(page, nhs_no)
    # Verify subject has subject notes  present
    logging.info("Verified: subject notes are present for the subject.")
    # logging.info("Verifying that  subject notes is present for the subject.")
    logging.info(
        f"Verifying that the subject Note is visible for the subject with NHS Number: {nhs_no}."
    )
    SubjectScreeningSummaryPage(page).verify_note_link_present(
        general_properties["subject_note_name"]
    )

    SubjectScreeningSummaryPage(page).click_subjects_events_notes()
    SubjectEventsNotesPage(page).select_note_type(NotesOptions.SUBJECT_NOTE)

    # Get supporting notes for the subject
    _, _, notes_df = fetch_supporting_notes_from_db(
        subjects_df, nhs_no, general_properties["note_status_active"]
    )
    verify_note_content_ui_vs_db(page, notes_df)


@pytest.mark.regression
@pytest.mark.note_tests
def test_update_existing_subject_note(page: Page, general_properties: dict) -> None:
    """
    Test to verify if an existing subject note can be updated successfully.
    """
    logging.info("Starting test: Verify subject has a subject note.")
    UserTools.user_login(page, "Team Leader at BCS01")
    BasePage(page).go_to_screening_subject_search_page()
    # Search for the subject by NHS Number.")
    subjects_df = get_subjects_by_note_count(
        general_properties["subject_note_type_value"],
        general_properties["note_status_active"],
        1,
    )
    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    search_subject_episode_by_nhs_number(page, nhs_no)
    # Verify subject has subject notes  present
    logging.info(
        f"Verifying that the subject Note is visible for the subject with NHS Number: {nhs_no}."
    )
    SubjectScreeningSummaryPage(page).verify_note_link_present(
        general_properties["subject_note_name"]
    )
    SubjectScreeningSummaryPage(page).click_subjects_events_notes()
    SubjectEventsNotesPage(page).select_note_type(NotesOptions.SUBJECT_NOTE)
    BasePage(page).safe_accept_dialog_select_option(
        SubjectEventsNotesPage(page).note_status, NotesStatusOptions.INVALID
    )
    SubjectEventsNotesPage(page).fill_note_title("updated subject title")
    SubjectEventsNotesPage(page).fill_notes("updated subject note")
    SubjectEventsNotesPage(page).accept_dialog_and_add_replacement_note()

    # Get updated supporting notes for the subject
    _, type_id, notes_df = fetch_supporting_notes_from_db(
        subjects_df, nhs_no, general_properties["note_status_active"]
    )
    # Verify title and note match the provided values
    logging.info("Verifying that the updated title and note match the provided values.")

    # Define the expected title and note
    note_title = "updated subject title"
    note_text = "updated subject note"
    # Log the expected title and note
    logging.info(f"Expected title: '{note_title}'")
    logging.info(f"Expected note: '{note_text}'")

    # Ensure the filtered DataFrame is not empty
    if notes_df.empty:
        pytest.fail(
            f"No notes found for type_id: {general_properties["subject_note_type_value"]}. Expected at least one updated note."
        )

    # Verify title and note match the provided values
    verify_note_content_matches_expected(notes_df, note_title, note_text, type_id)

    logging.info(
        f"Verification successful:Subject note added for the subject with NHS Number: {nhs_no}. "
        f"Title and note matched the provided values. Title: '{note_title}', Note: '{note_text}'."
    )


@pytest.mark.regression
@pytest.mark.note_tests
def test_remove_existing_subject_note(page: Page, general_properties: dict) -> None:
    """
    Test to verify if an existing Subject note can be removed for a subject with one Subject note.
    """
    logging.info(
        "Starting test: Verify if an existing Subject note can be removed for a subject with one Subject note"
    )
    UserTools.user_login(page, "Team Leader at BCS01")
    BasePage(page).go_to_screening_subject_search_page()

    # Search for the subject by NHS Number.")
    subjects_df = get_subjects_by_note_count(
        general_properties["subject_note_type_value"],
        general_properties["note_status_active"],
        1,
    )
    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    search_subject_episode_by_nhs_number(page, nhs_no)
    # Verify subject has subject notes  present
    logging.info(
        f"Verifying that the Subject Note is visible for the subject with NHS Number: {nhs_no}."
    )
    SubjectScreeningSummaryPage(page).verify_note_link_present(
        general_properties["subject_note_name"]
    )
    SubjectScreeningSummaryPage(page).click_subjects_events_notes()
    SubjectEventsNotesPage(page).select_note_type(NotesOptions.SUBJECT_NOTE)
    logging.info("Selecting the 'Obsolete' option for the existing Subject Note.")
    BasePage(page).safe_accept_dialog_select_option(
        SubjectEventsNotesPage(page).note_status, NotesStatusOptions.OBSOLETE
    )
    logging.info("Verifying that the subject does not have any Subject Notes.")

    _, _, notes_df = fetch_supporting_notes_from_db(
        subjects_df, nhs_no, general_properties["note_status_active"]
    )
    # Verify that the DataFrame is not empty
    if not notes_df.empty:
        pytest.fail(f"Subject has Subject Notes. Expected none, but found: {notes_df}")

    logging.info(
        "Verification successful: Subject does not have any active Subject Notes."
    )


@pytest.mark.regression
@pytest.mark.note_tests
def test_remove_existing_subject_note_for_subject_with_multiple_notes(
    page: Page, general_properties: dict
) -> None:
    """
    Test to verify if an existing subject note can be removed for a subject with multiple Subject notes.
    """
    # User login
    logging.info(
        "Starting test: Remove a subject note for a subject who already has multiple Subject note."
    )
    UserTools.user_login(page, "Team Leader at BCS01")
    BasePage(page).go_to_screening_subject_search_page()

    # Get a subject with multiple subject notes
    subjects_df = get_subjects_with_multiple_notes(
        general_properties["subject_note_type_value"]
    )
    if subjects_df.empty:
        logging.info("No subjects found with multiple Subject Notes.")
        pytest.fail("No subjects found with multiple Subject Notes.")
    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    logging.info(f"Searching for subject with NHS Number: {nhs_no}")
    search_subject_episode_by_nhs_number(page, nhs_no)
    # Navigate to Subject Events & Notes
    logging.info("Navigating to 'Subject Events & Notes' for the selected subject.")
    SubjectScreeningSummaryPage(page).click_subjects_events_notes()

    SubjectEventsNotesPage(page).select_note_type(NotesOptions.SUBJECT_NOTE)
    # Select the first Subject Note from the table for removal
    logging.info("Selecting the first Subject Note from the table for removal.")
    ui_data = SubjectEventsNotesPage(page).get_title_and_note_from_row(2)
    logging.info(
        "Removing one of the existing Subject Note by selecting 'Obsolete' option "
    )
    BasePage(page).safe_accept_dialog_select_option(
        SubjectEventsNotesPage(page).note_status, NotesStatusOptions.OBSOLETE
    )
    logging.info(
        "Verifying that the subject's removed subject note is removed from DB as well "
    )
    verify_note_removal_and_obsolete_transition(
        subjects_df,
        ui_data,
        general_properties,
        note_type_key="subject_note_type_value",
        status_active_key="note_status_active",
        status_obsolete_key="note_status_obsolete",
    )
