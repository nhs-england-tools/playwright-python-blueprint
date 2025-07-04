import logging
import pytest
from playwright.sync_api import Page, expect
from utils.user_tools import UserTools
from pages.base_page import BasePage
from pages.screening_subject_search.subject_screening_search_page import (
    SubjectScreeningPage,
)
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from pages.screening_subject_search.subject_events_notes import (
    NotesOptions,
    NotesStatusOptions,
    SubjectEventsNotes,
    AdditionalCareNoteTypeOptions,
)
from utils.oracle.oracle_specific_functions import (
    get_subjects_by_note_count,
    get_subjects_with_multiple_notes,
)
from utils.screening_subject_page_searcher import search_subject_episode_by_nhs_number
from utils.subject_notes import (
    fetch_supporting_notes_from_db,
    verify_note_content_matches_expected,
    verify_note_content_ui_vs_db,
    verify_note_removal_and_obsolete_transition,
)


@pytest.mark.regression
@pytest.mark.note_tests
def test_subject_does_not_have_an_additional_care_note(
    page: Page, general_properties: dict
) -> None:
    """
    Test to check if I can identify if a subject does not have a Additional Care note
    """
    logging.info(
        f"Starting test: Verify subject does not have a '{general_properties["additional_care_note_name"]}'."
    )
    UserTools.user_login(page, "ScreeningAssistant at BCS02")
    BasePage(page).go_to_screening_subject_search_page()

    # Search for the subject by NHS Number.")
    subjects_df = get_subjects_by_note_count(
        general_properties["additional_care_note_type_value"],
        general_properties["note_status_active"],
        0,
    )
    if subjects_df.empty:
        pytest.fail(
            f"No subjects found without '{general_properties["additional_care_note_name"]}'."
        )

    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    search_subject_episode_by_nhs_number(page, nhs_no)
    # Verify no additional care notes are present
    logging.info(
        f"Verified that no '{general_properties['additional_care_note_name']}' link is visible for the subject."
    )
    # logging.info("Verifying that no additional care notes are present for the subject.")
    SubjectScreeningSummaryPage(page).verify_note_link_not_present(
        general_properties["additional_care_note_name"]
    )


@pytest.mark.regression
@pytest.mark.note_tests
def test_add_an_additional_care_note_for_a_subject_without_a_note(
    page: Page, general_properties: dict
) -> None:
    """
    Test to add a note for a subject without an additional care note.
    """
    logging.info(
        "Starting test: Add a '{general_properties['additional_care_note_name']}'  for a subject without a note."
    )
    UserTools.user_login(page, "Team Leader at BCS01")
    BasePage(page).go_to_screening_subject_search_page()

    # Get a subject with no notes of the specified type
    subjects_df = get_subjects_by_note_count(
        general_properties["additional_care_note_type_value"],
        general_properties["note_status_active"],
        0,
    )
    if subjects_df.empty:
        pytest.fail(
            f"No subjects found for note type {general_properties["additional_care_note_type_value"]}."
        )
    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    search_subject_episode_by_nhs_number(page, nhs_no)
    # search_subject_by_nhs(page, nhs_no)

    # Navigate to Subject Events & Notes
    logging.info("Navigating to 'Subject Events & Notes' for the selected subject.")
    SubjectScreeningSummaryPage(page).click_subjects_events_notes()

    # note type selection
    logging.info(
        f"Selecting note type based on value: '{general_properties["additional_care_note_type_value"]}'."
    )
    SubjectEventsNotes(page).select_additional_care_note()
    logging.info("Selecting Additional Care Note Type")
    note_title = "Additional Care Need - Learning disability"
    SubjectEventsNotes(page).select_additional_care_note_type(
        AdditionalCareNoteTypeOptions.LEARNING_DISABILITY
    )
    # Fill Notes
    note_text = "adding additional care need notes"
    logging.info(f"Filling in notes: '{note_text}'.")
    SubjectEventsNotes(page).fill_notes(note_text)
    # Dismiss dialog and update notes
    logging.info("Dismissing dialog and clicking 'Update Notes'.")
    SubjectEventsNotes(page).accept_dialog_and_update_notes()

    # Get supporting notes for the subject from DB
    _, type_id, notes_df = fetch_supporting_notes_from_db(
        subjects_df, nhs_no, general_properties["note_status_active"]
    )

    verify_note_content_matches_expected(notes_df, note_title, note_text, type_id)

    logging.info(
        f"Verification successful: Additional care note added for the subject with NHS Number: {nhs_no}. "
        f"Title and note matched the provided values. Title: '{note_title}', Note: '{note_text}'."
    )


@pytest.mark.regression
@pytest.mark.note_tests
def test_add_additional_care_note_for_subject_with_existing_note(
    page: Page, general_properties: dict
) -> None:
    """
    Test to add an additional care note for a subject who already has an existing note.
    """
    # User login
    logging.info(
        "Starting test: Add an additional care note for a subject who already has additional care note."
    )
    UserTools.user_login(page, "Team Leader at BCS01")
    BasePage(page).go_to_screening_subject_search_page()

    # Get a subject with existing additional care notes
    subjects_df = get_subjects_by_note_count(
        general_properties["additional_care_note_type_value"],
        general_properties["note_status_active"],
        1,
    )
    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    search_subject_episode_by_nhs_number(page, nhs_no)
    # Navigate to Subject Events & Notes
    logging.info("Navigating to 'Subject Events & Notes' for the selected subject.")
    SubjectScreeningSummaryPage(page).click_subjects_events_notes()

    # add an Additional Care Note if the subject already has one
    logging.info("Selecting 'Additional Care Needs Note'.")
    SubjectEventsNotes(page).select_additional_care_note()

    # Select Additional Care Note Type
    note_title = "Additional Care Need - Learning disability"
    logging.info(f"Selecting Additional Care Note Type: '{note_title}'.")
    SubjectEventsNotes(page).select_additional_care_note_type(
        AdditionalCareNoteTypeOptions.LEARNING_DISABILITY
    )

    # Fill Notes
    note_text = "adding additional care need notes2"
    logging.info(f"Filling in notes: '{note_text}'.")
    SubjectEventsNotes(page).fill_notes(note_text)

    # Accept dialog and update notes
    logging.info("Accept dialog and clicking 'Update Notes'.")
    SubjectEventsNotes(page).accept_dialog_and_update_notes()
    # Get supporting notes for the subject
    _, type_id, notes_df = fetch_supporting_notes_from_db(
        subjects_df, nhs_no, general_properties["note_status_active"]
    )

    verify_note_content_matches_expected(notes_df, note_title, note_text, type_id)

    logging.info(
        f"Verification successful: Additional care note added for the subject with NHS Number: {nhs_no}. "
        f"Title and note matched the provided values. Title: '{note_title}', Note: '{note_text}'."
    )


@pytest.mark.regression
@pytest.mark.note_tests
def test_identify_subject_with_additional_care_note(
    page: Page, general_properties: dict
) -> None:
    """
    Test to identify if a subject has an Additional Care note.
    """
    logging.info("Starting test: Verify subject has an additional care note.")
    UserTools.user_login(page, "ScreeningAssistant at BCS02")
    BasePage(page).go_to_screening_subject_search_page()

    # Search for the subject by NHS Number.")
    subjects_df = get_subjects_by_note_count(
        general_properties["additional_care_note_type_value"],
        general_properties["note_status_active"],
        1,
    )
    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    search_subject_episode_by_nhs_number(page, nhs_no)
    # Verify subject has additional care notes  present
    logging.info("Verified: Additional care notes are present for the subject.")
    # logging.info("Verifying that  additional care notes are present for the subject.")
    SubjectScreeningSummaryPage(page).verify_note_link_present(
        general_properties["additional_care_note_name"]
    )


@pytest.mark.regression
@pytest.mark.note_tests
def test_view_active_additional_care_note(page: Page, general_properties: dict) -> None:
    """
    Test to verify if an active Additional Care note is visible for a subject.
    """
    logging.info("Starting test: Verify subject has an additional care note.")
    UserTools.user_login(page, "ScreeningAssistant at BCS02")
    BasePage(page).go_to_screening_subject_search_page()

    # Search for the subject by NHS Number.")
    subjects_df = get_subjects_by_note_count(
        general_properties["additional_care_note_type_value"], 1
    )
    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    search_subject_episode_by_nhs_number(page, nhs_no)
    # Verify subject has additional care notes  present
    logging.info("Verified: Additional care notes are present for the subject.")
    # logging.info("Verifying that  additional care notes are present for the subject.")
    logging.info(
        f"Verifying that the Additional Care Note is visible for the subject with NHS Number: {nhs_no}."
    )
    SubjectScreeningSummaryPage(page).verify_note_link_present(
        general_properties["additional_care_note_name"]
    )
    logging.info(
        f"Clicking on the 'Additional Care Note' link for the subject with NHS Number: {nhs_no}."
    )

    SubjectScreeningSummaryPage(page).click_subjects_events_notes()
    SubjectEventsNotes(page).select_note_type(NotesOptions.ADDITIONAL_CARE_NOTE)

    # Get supporting notes for the subject
    _, _, notes_df = fetch_supporting_notes_from_db(
        subjects_df, nhs_no, general_properties["note_status_active"]
    )

    verify_note_content_ui_vs_db(page, notes_df)


@pytest.mark.regression
@pytest.mark.note_tests
def test_update_existing_additional_care_note(
    page: Page, general_properties: dict
) -> None:
    """
    Test to verify if an existing Additional Care note can be updated successfully.
    """
    logging.info("Starting test: Verify subject has an additional care note.")
    UserTools.user_login(page, "Team Leader at BCS01")
    BasePage(page).go_to_screening_subject_search_page()
    # Search for the subject by NHS Number.")
    subjects_df = get_subjects_by_note_count(
        general_properties["additional_care_note_type_value"],
        general_properties["note_status_active"],
        1,
    )
    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    search_subject_episode_by_nhs_number(page, nhs_no)
    # Verify subject has additional care notes  present
    logging.info(
        f"Verifying that the Additional Care Note is visible for the subject with NHS Number: {nhs_no}."
    )
    SubjectScreeningSummaryPage(page).verify_note_link_present(
        general_properties["additional_care_note_name"]
    )
    SubjectScreeningSummaryPage(page).click_subjects_events_notes()
    SubjectEventsNotes(page).select_note_type(NotesOptions.ADDITIONAL_CARE_NOTE)
    BasePage(page).safe_accept_dialog_select_option(
        SubjectEventsNotes(page).note_status, NotesStatusOptions.INVALID
    )
    SubjectEventsNotes(page).select_additional_care_note()
    SubjectEventsNotes(page).select_additional_care_note_type(
        AdditionalCareNoteTypeOptions.HEARING_DISABILITY
    )
    SubjectEventsNotes(page).fill_notes("updated additional care note")
    SubjectEventsNotes(page).accept_dialog_and_add_replacement_note()

    # Get updated supporting notes for the subject
    _, type_id, notes_df = fetch_supporting_notes_from_db(
        subjects_df, nhs_no, general_properties["note_status_active"]
    )
    # Verify title and note match the provided values
    logging.info("Verifying that the updated title and note match the provided values.")

    # Define the expected title and note
    note_title = "Additional Care Need - Hearing disability"
    note_text = "updated additional care note"
    # Log the expected title and note
    logging.info(f"Expected title: '{note_title}'")
    logging.info(f"Expected note: '{note_text}'")

    # Ensure the filtered DataFrame is not empty
    if notes_df.empty:
        pytest.fail(
            f"No notes found for type_id: {general_properties["additional_care_note_type_value"]}. Expected at least one updated note."
        )

    # Verify title and note match the provided values
    verify_note_content_matches_expected(notes_df, note_title, note_text, type_id)

    logging.info(
        f"Verification successful: Additional care note added for the subject with NHS Number: {nhs_no}. "
        f"Title and note matched the provided values. Title: '{note_title}', Note: '{note_text}'."
    )


@pytest.mark.regression
@pytest.mark.note_tests
def test_remove_existing_additional_care_note(
    page: Page, general_properties: dict
) -> None:
    """
    Test to verify if an existing Additional Care note can be removed for a subject with one Additional Care note.
    """
    logging.info(
        "Starting test: Verify if an existing Additional Care note can be removed for a subject with one Additional Care note"
    )
    UserTools.user_login(page, "Team Leader at BCS01")
    BasePage(page).go_to_screening_subject_search_page()

    # Search for the subject by NHS Number.")
    subjects_df = get_subjects_by_note_count(
        general_properties["additional_care_note_type_value"],
        general_properties["note_status_active"],
        1,
    )
    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    search_subject_episode_by_nhs_number(page, nhs_no)
    # Verify subject has additional care notes  present
    logging.info(
        f"Verifying that the Additional Care Note is visible for the subject with NHS Number: {nhs_no}."
    )
    SubjectScreeningSummaryPage(page).verify_note_link_present(
        general_properties["additional_care_note_name"]
    )

    SubjectScreeningSummaryPage(page).click_subjects_events_notes()
    SubjectEventsNotes(page).select_note_type(NotesOptions.ADDITIONAL_CARE_NOTE)
    logging.info(
        "Selecting the 'Obsolete' option for the existing Additional Care Note."
    )
    BasePage(page).safe_accept_dialog_select_option(
        SubjectEventsNotes(page).note_status, NotesStatusOptions.OBSOLETE
    )
    logging.info("Verifying that the subject does not have any Additional Care Notes.")

    _, _, notes_df = fetch_supporting_notes_from_db(
        subjects_df, nhs_no, general_properties["note_status_active"]
    )
    # Verify that the DataFrame is not empty
    if not notes_df.empty:
        pytest.fail(
            f"Subject has Additional Care Notes. Expected none, but found: {notes_df}"
        )

    logging.info(
        "Verification successful: Subject does not have any active Additional Care Notes."
    )


@pytest.mark.regression
@pytest.mark.note_tests
def test_remove_existing_additional_care_note_for_subject_with_multiple_notes(
    page: Page, general_properties: dict
) -> None:
    """
    Test to verify if an existing Additional Care note can be removed for a subject with multiple Additional Care notes.
    """
    # User login
    logging.info(
        "Starting test: Remove an additional care note for a subject who already has multiple additional care note."
    )
    UserTools.user_login(page, "Team Leader at BCS01")
    BasePage(page).go_to_screening_subject_search_page()

    # Get a subject with multiple additional care notes
    subjects_df = get_subjects_with_multiple_notes(
        general_properties["additional_care_note_type_value"]
    )
    if subjects_df.empty:
        logging.info("No subjects found with multiple Additional Care Notes.")
        pytest.fail("No subjects found with multiple Additional Care Notes.")
    nhs_no = subjects_df["subject_nhs_number"].iloc[0]
    logging.info(f"Searching for subject with NHS Number: {nhs_no}")
    search_subject_episode_by_nhs_number(page, nhs_no)
    # Navigate to Subject Events & Notes
    logging.info("Navigating to 'Subject Events & Notes' for the selected subject.")
    SubjectScreeningSummaryPage(page).click_subjects_events_notes()

    SubjectEventsNotes(page).select_note_type(NotesOptions.ADDITIONAL_CARE_NOTE)
    # Select the first Additional Care Note from the table for removal
    logging.info("Selecting the first Additional Care Note from the table for removal.")
    ui_data = SubjectEventsNotes(page).get_title_and_note_from_row(2)
    logging.info(
        "Removing one of the existing Additional Care Note by selecting 'Obsolete' option "
    )
    BasePage(page).safe_accept_dialog_select_option(
        SubjectEventsNotes(page).note_status, NotesStatusOptions.OBSOLETE
    )
    logging.info(
        "Verifying that the subject's removed additional care note is removed from DB as well "
    )

    verify_note_removal_and_obsolete_transition(
        subjects_df,
        ui_data,
        general_properties,
        note_type_key="additional_care_note_type_value",
        status_active_key="note_status_active",
        status_obsolete_key="note_status_obsolete",
    )
