from oracle.oracle import OracleDB
import pandas as pd


def get_subjects_by_note_count(
    type_id: int, note_status: int, note_count: int = 0
) -> pd.DataFrame:
    """
    Retrieves subjects based on the number of additional care notes of the specified type.

    Args:
        type_id (int): The type ID of the additional care note to check for.
        note_count (int): The number of notes to check for. Defaults to 0.
        note_status (int): The status ID of the notes.
    Returns:
        pd.DataFrame: A pandas DataFrame containing the result of the query.
    """
    query = """
    SELECT ss.screening_subject_id, ss.subject_nhs_number, :type_id AS type_id, :status_id AS note_status
    FROM screening_subject_t ss
    INNER JOIN sd_contact_t c ON ss.subject_nhs_number = c.nhs_number
    WHERE (
    (:note_count = 0 AND NOT EXISTS (
        SELECT 1
        FROM supporting_notes_t sn
        WHERE sn.screening_subject_id = ss.screening_subject_id
        AND (sn.type_id = :type_id OR sn.promote_pio_id IS NOT NULL)
        AND sn.status_id = :status_id
    ))
    OR
    (:note_count > 0 AND :note_count = (
        SELECT COUNT(sn.screening_subject_id)
        FROM supporting_notes_t sn
        WHERE sn.screening_subject_id = ss.screening_subject_id
        AND sn.type_id = :type_id
        AND sn.status_id = :status_id
        GROUP BY sn.screening_subject_id
    ))
    )
    AND ss.number_of_invitations > 0
    AND ROWNUM = 1
    """

    params = {"type_id": type_id, "note_count": note_count, "status_id": note_status}
    subjects_df = OracleDB().execute_query(query, params)

    return subjects_df


def get_supporting_notes(
    screening_subject_id: int, type_id: int, note_status: int
) -> pd.DataFrame:
    """
    Retrieves supporting notes for a given screening subject ID and type ID.

    Args:
        screening_subject_id (int): The ID of the screening subject.
        type_id (int): The type ID of the supporting note.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the result of the query.
    """
    query = """
    SELECT *
    FROM supporting_notes_t sn
    WHERE sn.screening_subject_id = :screening_subject_id
    AND sn.type_id = :type_id
    AND sn.status_id = :note_status
    ORDER BY NVL(sn.updated_datestamp, sn.created_datestamp) DESC
    """
    params = {
        "screening_subject_id": screening_subject_id,
        "type_id": type_id,
        "note_status": note_status,
    }
    notes_df = OracleDB().execute_query(query, params)
    return notes_df


def get_subjects_with_multiple_notes(note_type: int) -> pd.DataFrame:
    """
    Retrieves subjects with a multiple note counts for a specific note type.

    Args:
        note_type (int): The type ID of the note.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the result of the query.
    """
    query = """
    SELECT ss.*
    FROM screening_subject_t ss
    INNER JOIN sd_contact_t c ON ss.subject_nhs_number = c.nhs_number
    WHERE 1 < (
        SELECT COUNT(sn.screening_subject_id)
        FROM supporting_notes_t sn
        WHERE sn.screening_subject_id = ss.screening_subject_id
        AND sn.type_id = :note_type
        AND sn.status_id = 4100
        GROUP BY sn.screening_subject_id
    )
    AND 200 > (SELECT COUNT(sn.screening_subject_id)
        FROM supporting_notes_t sn
        WHERE sn.screening_subject_id = ss.screening_subject_id
        AND sn.type_id = :note_type
        AND sn.status_id = 4100
        GROUP BY sn.screening_subject_id
    )
    AND ROWNUM = 1
    """

    params = {"note_type": note_type}
    subjects_df = OracleDB().execute_query(query, params)

    return subjects_df
