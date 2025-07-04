from oracle.oracle import OracleDB
import logging
import pandas as pd
from datetime import datetime
from enum import IntEnum


class SqlQueryValues(IntEnum):
    S10_EVENT_STATUS = 11198
    S19_EVENT_STATUS = 11213
    S43_EVENT_STATUS = 11223
    OPEN_EPISODE_STATUS_ID = 11352
    A8_EVENT_STATUS = 11132
    POSITIVE_APPOINTMENT_BOOKED = 11119
    POST_INVESTIGATION_APPOINTMENT_NOT_REQUIRED = 160182


def get_kit_id_from_db(
    tk_type_id: int, hub_id: int, no_of_kits_to_retrieve: int
) -> pd.DataFrame:
    """
    This query is used to obtain test kits used in compartment 2

    Args:
        tk_type_id (int): The id of the kit type
        hub_id (int): The hub ID of the screening center
        no_of_kits_to_retrieve (int): The amount of kits you want to retrieve

    Returns:
        kit_id_df (pd.DataFrame): A pandas DataFrame containing the result of the query
    """
    logging.info("Retrieving useable test kit ids")
    query = """select tk.kitid, tk.screening_subject_id, sst.subject_nhs_number
    from tk_items_t tk
    inner join ep_subject_episode_t se on se.screening_subject_id = tk.screening_subject_id
    inner join screening_subject_t sst on (sst.screening_subject_id = tk.screening_subject_id)
    inner join sd_contact_t sdc on (sdc.nhs_number = sst.subject_nhs_number)
    where tk.tk_type_id = :tk_type_id
    and tk.logged_in_flag = 'N'
    and sdc.hub_id = :hub_id
    and device_id is null
    and tk.invalidated_date is null
    and se.latest_event_status_id in (:s10_event_status, :s19_event_status)
    order by tk.kitid DESC
    fetch first :subjects_to_retrieve rows only"""

    params = {
        "s10_event_status": SqlQueryValues.S10_EVENT_STATUS,
        "s19_event_status": SqlQueryValues.S19_EVENT_STATUS,
        "tk_type_id": tk_type_id,
        "hub_id": hub_id,
        "subjects_to_retrieve": no_of_kits_to_retrieve,
    }

    kit_id_df = OracleDB().execute_query(query, params)

    return kit_id_df


def get_nhs_no_from_batch_id(batch_id: str) -> pd.DataFrame:
    """
    This query returns a dataframe of NHS Numbers of the subjects in a certain batch
    We provide the batch ID e.g. 8812 and then we have a list of NHS Numbers we can verify the statuses

    Args:
        batch_id (str): The batch ID you want to get the subjects from

    Returns:
        nhs_number_df (pd.DataFrame): A pandas DataFrame containing the result of the query
    """
    nhs_number_df = OracleDB().execute_query(
        f"""
    SELECT SUBJECT_NHS_NUMBER
    FROM SCREENING_SUBJECT_T ss
    INNER JOIN sd_contact_t c ON ss.subject_nhs_number = c.nhs_number
    INNER JOIN LETT_BATCH_RECORDS lbr
    ON ss.SCREENING_SUBJECT_ID = lbr.SCREENING_SUBJECT_ID
    WHERE lbr.BATCH_ID IN {batch_id}
    AND ss.screening_status_id != 4008
    ORDER BY ss.subject_nhs_number
    """
    )
    return nhs_number_df


def get_kit_id_logged_from_db(smokescreen_properties: dict) -> pd.DataFrame:
    """
    This query is used to obtain test data used in compartment 3

    Args:
        smokescreen_properties(): A dictionary containing all values needed to run the query

    Returns:
        return kit_id_df (pd.DataFrame): A pandas DataFrame containing the result of the query
    """
    query = """SELECT tk.kitid,tk.device_id,tk.screening_subject_id
    FROM tk_items_t tk
    INNER JOIN kit_queue kq ON kq.device_id = tk.device_id
    INNER JOIN ep_subject_episode_t se ON se.screening_subject_id = tk.screening_subject_id
    WHERE tk.logged_in_flag = 'Y'
    AND kq.test_kit_status IN ('LOGGED', 'POSTED')
    AND se.episode_status_id = :open_episode_status_id
    AND tk.tk_type_id = 2
    AND se.latest_event_status_id = :s43_event_status
    AND tk.logged_in_at = :logged_in_at
    AND tk.reading_flag = 'N'
    AND tk.test_results IS NULL
    fetch first :subjects_to_retrieve rows only
    """

    params = {
        "s43_event_status": SqlQueryValues.S43_EVENT_STATUS,
        "logged_in_at": smokescreen_properties["c3_fit_kit_results_test_org_id"],
        "open_episode_status_id": SqlQueryValues.OPEN_EPISODE_STATUS_ID,
        "subjects_to_retrieve": smokescreen_properties["c3_total_fit_kits_to_retrieve"],
    }

    kit_id_df = OracleDB().execute_query(query, params)

    return kit_id_df


def get_service_management_by_device_id(device_id: str) -> pd.DataFrame:
    """
    This SQL is similar to the one used in pkg_test_kit_queue.p_get_fit_monitor_details, but adapted to allow us to pick out sub-sets of records

    Args:
        device_id (str): The device ID

    Returns:
        get_service_management_df (pd.DataFrame): A pandas DataFrame containing the result of the query
    """

    query = """SELECT kq.device_id, kq.test_kit_name, kq.test_kit_type, kq.test_kit_status,
    CASE WHEN tki.logged_in_flag = 'Y' THEN kq.logged_by_hub END AS logged_by_hub,
    CASE WHEN tki.logged_in_flag = 'Y' THEN kq.date_time_logged END AS date_time_logged,
    tki.logged_in_on AS tk_logged_date_time, kq.test_result, kq.calculated_result,
    kq.error_code,
    (SELECT vvt.description
    FROM tk_analyser_t tka
    INNER JOIN tk_analyser_type_error tkate ON tkate.tk_analyser_type_id = tka.tk_analyser_type_id
    INNER JOIN valid_values vvt ON tkate.tk_analyser_error_type_id = vvt.valid_value_id
    WHERE tka.analyser_code = kq.analyser_code AND tkate.error_code = kq.error_code)
    AS analyser_error_description, kq.analyser_code, kq.date_time_authorised,
    kq.authoriser_user_code, kq.datestamp, kq.bcss_error_id,
    REPLACE(mt.description, 'ERROR - ', '') AS error_type,
    NVL(mta.allowed_value, 'N') AS error_ok_to_archive,
    kq.post_response, kq.post_attempts, kq.put_response,
    kq.put_attempts, kq.date_time_error_archived,
    kq.error_archived_user_code, sst.screening_subject_id,
    sst.subject_nhs_number, tki.test_results, tki.issue_date,
    o.org_code AS issued_by_hub
    FROM kit_queue kq
    LEFT OUTER JOIN tk_items_t tki ON tki.device_id = kq.device_id
    OR (tki.device_id IS NULL AND tki.kitid = pkg_test_kit.f_get_kit_id_from_device_id(kq.device_id))
    LEFT OUTER JOIN screening_subject_t sst ON sst.screening_subject_id = tki.screening_subject_id
    LEFT OUTER JOIN ep_subject_episode_t ep ON ep.subject_epis_id = tki.subject_epis_id
    LEFT OUTER JOIN message_types mt ON kq.bcss_error_id = mt.message_type_id
    LEFT OUTER JOIN valid_values mta ON mta.valid_value_id = mt.message_attribute_id AND mta.valid_value_id = 305482
    LEFT OUTER JOIN ORG o ON ep.start_hub_id = o.org_id
    LEFT OUTER JOIN ORG lo ON lo.org_code = kq.logged_by_hub
    WHERE kq.test_kit_type = 'FIT' AND kq.device_id = :device_id
    """
    params = {"device_id": device_id}
    get_service_management_df = OracleDB().execute_query(query, params)
    return get_service_management_df


def update_kit_service_management_entity(
    device_id: str, normal: bool, smokescreen_properties: dict
) -> str:
    """
    This method is used to update the KIT_QUEUE table on the DB
    This is done so that we can then run two stored procedures to update the subjects and kits status to either normal or abnormal

    Args:
        device_id (str): The device ID
        normal (bool): Whether the device should be marked as normal or abnormal
        smokescreen_properties(): A dictionary containing all values needed to run the query

    Returns:
        subject_nhs_number (str): The NHS Number of the affected subject
    """
    get_service_management_df = get_service_management_by_device_id(device_id)

    # Extract the NHS number from the DataFrame
    subject_nhs_number = get_service_management_df["subject_nhs_number"].iloc[0]
    test_kit_name = get_service_management_df["test_kit_name"].iloc[0]
    test_kit_type = get_service_management_df["test_kit_type"].iloc[0]
    logged_by_hub = get_service_management_df["logged_by_hub"].iloc[0]
    date_time_logged = get_service_management_df["date_time_logged"].iloc[0]
    calculated_result = get_service_management_df["calculated_result"].iloc[0]
    post_response = get_service_management_df["post_response"].iloc[0]
    post_attempts = get_service_management_df["post_attempts"].iloc[0]
    put_response = get_service_management_df["put_response"].iloc[0]
    put_attempts = get_service_management_df["put_attempts"].iloc[0]
    # format date
    date_time_authorised = (
        datetime.now().strftime("%d-%b-%y %H.%M.%S.")
        + f"{datetime.now().microsecond:06d}000"
    )
    if normal:
        test_result = int(smokescreen_properties["c3_fit_kit_normal_result"])
    else:
        test_result = int(smokescreen_properties["c3_fit_kit_abnormal_result"])
        # Parameterized query
    update_query = """
    UPDATE kit_queue kq
    SET kq.test_kit_name = :test_kit_name,
    kq.test_kit_type = :test_kit_type,
    kq.test_kit_status =:test_kit_status,
    kq.logged_by_hub = :logged_by_hub,
    kq.date_time_logged = :date_time_logged,
    kq.test_result = :test_result,
    kq.calculated_result = :calculated_result,
    kq.error_code = NULL,
    kq.analyser_code = :analyser_code,
    kq.date_time_authorised = TO_TIMESTAMP(:date_time_authorised, 'DD-Mon-YY HH24.MI.SS.FF9'),
    kq.authoriser_user_code = :authoriser_user_code,
    kq.post_response = :post_response,
    kq.post_attempts = :post_attempts,
    kq.put_response = :put_response,
    kq.put_attempts = :put_attempts
    WHERE kq.device_id = :device_id
    """

    # Parameters dictionary
    params = {
        "test_kit_name": test_kit_name,
        "test_kit_type": test_kit_type,
        "test_kit_status": "BCSS_READY",
        "logged_by_hub": logged_by_hub,
        "date_time_logged": date_time_logged,
        "test_result": int(test_result),
        "calculated_result": calculated_result,
        "analyser_code": smokescreen_properties["c3_fit_kit_analyser_code"],
        "date_time_authorised": str(date_time_authorised),
        "authoriser_user_code": smokescreen_properties["c3_fit_kit_authorised_user"],
        "post_response": int(post_response) if post_response is not None else 0,
        "post_attempts": int(post_attempts) if post_attempts is not None else 0,
        "put_response": put_response,
        "put_attempts": put_attempts,
        "device_id": device_id,
    }

    # Execute query
    rows_affected = OracleDB().update_or_insert_data_to_table(update_query, params)
    logging.info(f"Rows affected: {rows_affected}")
    # Return the subject NHS number
    return subject_nhs_number


def execute_fit_kit_stored_procedures() -> None:
    """
    This method executes two stored procedures:
    - PKG_TEST_KIT_QUEUE.p_validate_kit_queue
    - PKG_TEST_KIT_QUEUE.p_calculate_result
    This is needed for compartment 3 after we update the KIT_QUEUE table on the DB
    """
    db_instance = OracleDB()  # Create an instance of the OracleDB class
    logging.info("start: oracle.OracleDB.execute_stored_procedure")
    db_instance.execute_stored_procedure(
        "PKG_TEST_KIT_QUEUE.p_validate_kit_queue"
    )  # Run stored procedure - validate kit queue
    db_instance.execute_stored_procedure(
        "PKG_TEST_KIT_QUEUE.p_calculate_result"
    )  # Run stored procedure - calculate result
    logging.info("exit: oracle.OracleDB.execute_stored_procedure")


def get_subjects_for_appointments(subjects_to_retrieve: int) -> pd.DataFrame:
    """
    This is used to get subjects for compartment 4
    It finds subjects with open episodes and the event status A8
    It also checks that the episode is less than 2 years old

    Args:
        subjects_to_retrieve (int): The number of subjects to retrieve

    Returns:
        subjects_df (pd.DataFrame): A pandas DataFrame containing the result of the query
    """

    query = """select tk.kitid, ss.subject_nhs_number, se.screening_subject_id
    from tk_items_t tk
    inner join ep_subject_episode_t se on se.screening_subject_id = tk.screening_subject_id
    inner join screening_subject_t ss on ss.screening_subject_id = se.screening_subject_id
    inner join sd_contact_t c on c.nhs_number = ss.subject_nhs_number
    where se.latest_event_status_id = :a8_event_status
    and tk.logged_in_flag = 'Y'
    and se.episode_status_id = :open_episode_status_id
    and ss.screening_status_id != 4008
    and tk.logged_in_at = 23159
    and c.hub_id = 23159
    and tk.tk_type_id = 2
    and tk.datestamp > add_months(sysdate,-24)
    order by ss.subject_nhs_number desc
    fetch first :subjects_to_retrieve rows only
    """
    params = {
        "a8_event_status": SqlQueryValues.A8_EVENT_STATUS,
        "open_episode_status_id": SqlQueryValues.OPEN_EPISODE_STATUS_ID,
        "subjects_to_retrieve": subjects_to_retrieve,
    }

    subjects_df = OracleDB().execute_query(query, params)

    return subjects_df


def get_subjects_with_booked_appointments(subjects_to_retrieve: int) -> pd.DataFrame:
    """
    This is used to get subjects for compartment 5
    It finds subjects with appointments book and letters sent
    and makes sure appointments are prior to todays date

    Args:
        subjects_to_retrieve (int): The number of subjects to retrieve

    Returns:
        subjects_df (pd.DataFrame): A pandas DataFrame containing the result of the query
    """

    query = """select distinct(s.subject_nhs_number), a.appointment_date, c.person_family_name, c.person_given_name
    from
    (select count(*), ds.screening_subject_id
    from
    (
    select ep.screening_subject_id, ep.subject_epis_id
    from  ep_subject_episode_t ep
    inner join ds_patient_assessment_t pa
    on pa.episode_id = ep.subject_epis_id
    ) ds
    group by ds.screening_subject_id
    having count(*) = 1
    ) ss
    inner join tk_items_t tk on tk.screening_subject_id = ss.screening_subject_id
    inner join ep_subject_episode_t se on se.screening_subject_id = tk.screening_subject_id
    and se.subject_epis_id = tk.logged_subject_epis_id
    inner join screening_subject_t s on s.screening_subject_id = se.screening_subject_id
    inner join sd_contact_t c on c.nhs_number = s.subject_nhs_number
    inner join appointment_t a on se.subject_epis_id = a.subject_epis_id
    where se.latest_event_status_id = :positive_appointment_booked
    and tk.logged_in_flag = 'Y'
    and se.episode_status_id = :open_episode_status_id
    and tk.logged_in_at = 23159
    and tk.algorithm_sc_id = 23162
    --and a.appointment_date > sysdate-27
    and a.cancel_date is null
    and a.attend_info_id is null and a.attend_date is null
    and a.cancel_dna_reason_id is null
    and a.appointment_date <= sysdate
    and tk.tk_type_id = 2
    --and tk.datestamp > add_months(sysdate,-24)
    order by a.appointment_date desc
    fetch first :subjects_to_retrieve rows only
    """

    params = {
        "positive_appointment_booked": SqlQueryValues.POSITIVE_APPOINTMENT_BOOKED,
        "open_episode_status_id": SqlQueryValues.OPEN_EPISODE_STATUS_ID,
        "subjects_to_retrieve": subjects_to_retrieve,
    }

    subjects_df = OracleDB().execute_query(query, params)

    return subjects_df


def get_subjects_for_investigation_dataset_updates(
    number_of_subjects: int, hub_id: str
) -> pd.DataFrame:
    """
    This is used to get subjects for compartment 6
    It finds subjects with latest envent status of A323 - Post-investigation Appointment

    Args:
        number_of_subjects (int): The number of subjects to retrieve
        hub_id (str): hub id to use

    Returns:
        subjects_df (pd.DataFrame): A pandas DataFrame containing the result of the query
    """

    query = """SELECT distinct(ss.subject_nhs_number)
    from
    (
    select count(*), eset.screening_subject_id
    from ep_subject_episode_t eset
    inner join screening_subject_t sst on (eset.screening_subject_id = sst.screening_subject_id)
    inner join external_tests_t ext on (eset.subject_epis_id = ext.subject_epis_id)
    inner join ds_colonoscopy_t dct on (ext.ext_test_id = dct.ext_test_id)
    where dct.dataset_completed_date is null
    and dct.deleted_flag ='N'
    and ext.void = 'N'
    group by eset.screening_subject_id
    having
    count(*)= 1 ) sst
    inner join ep_subject_episode_t eset on ( sst.screening_subject_id = eset.screening_subject_id )
    inner join screening_subject_t ss on (eset.screening_subject_id = ss.screening_subject_id)
    inner join sd_contact_t c ON ss.subject_nhs_number = c.nhs_number
    inner join EXTERNAL_TESTS_T ext on (eset.subject_epis_id = ext.subject_epis_id)
    inner join DS_COLONOSCOPY_T dct on (ext.ext_test_id = dct.ext_test_id)
    inner join sd_contact_t sd on (ss.subject_nhs_number = sd.nhs_number)
    inner join sd_address_t sda on (sd.contact_id = sda.address_id)
    inner join org on (sd.gp_practice_id = org.org_id)
    where eset.latest_event_status_id = :latest_event_status_id -- A323 - Post-investigation Appointment NOT Required
    and ext.void = 'N'
    and dct.dataset_new_flag = 'Y'
    and dct.deleted_flag = 'N'
    and sd.GP_PRACTICE_ID is not null
    and eset.start_hub_id = :start_hub_id
    fetch first :subjects_to_retrieve rows only
    """

    params = {
        "latest_event_status_id": SqlQueryValues.POST_INVESTIGATION_APPOINTMENT_NOT_REQUIRED,
        "start_hub_id": hub_id,
        "subjects_to_retrieve": number_of_subjects,
    }

    subjects_df = OracleDB().execute_query(query, params)
    return subjects_df


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
    Retrieves subjects with a multiple note counts for a specific note type and status.

    Args:
        note_type (int): The type ID of the note.
        note_status (int): The status ID of the note.

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


def check_if_subject_has_temporary_address(nhs_no: str) -> pd.DataFrame:
    """
    Checks if the subject has a temporary address in the database.
    Args:
        nhs_no (str): The NHS number of the subject.
    This function queries the database to determine if the subject has a temporary address
    and asserts the result against the expected value.
    The query checks for the existence of a temporary address by looking for a record
    in the screening_subject_t, sd_contact_t, and sd_address_t tables where the address
    type is 13043 (temporary address) and the effective_from date is not null.
    """

    query = """
        SELECT
        CASE
            WHEN EXISTS (
            SELECT 1
            FROM screening_subject_t ss
            INNER JOIN sd_contact_t c ON c.nhs_number = ss.subject_nhs_number
            INNER JOIN sd_address_t a ON a.contact_id = c.contact_id
            WHERE ss.subject_nhs_number = :nhs_no
                AND a.address_type = 13043
                AND a.effective_from IS NOT NULL
            )
            THEN 'Subject has a temporary address'
            ELSE 'Subject doesn''t have a temporary address'
        END AS address_status
        FROM DUAL
    """
    bind_vars = {"nhs_no": nhs_no}
    df = OracleDB().execute_query(query, bind_vars)
    return df
