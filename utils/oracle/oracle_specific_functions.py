from oracle.oracle import OracleDB
import logging
import pandas as pd
from datetime import datetime


def get_kit_id_from_db() -> pd.DataFrame:
    """
    This query is used to obtain test kits used in compartment 2
    It searches for kits that have not been logged and meet the following criteria:
    - tk.tk_type_id = 2 (Only FIT Kits)
    - sdc.hub_id = 23159 (Hub ID that the compartments are running in)
    - se.latest_event_status_id is 11198 or 11213 (Only kits at the status we want S10/S19 are retrieved)
    """
    logging.info("Retrieving useable test kit ids")
    kit_id_df = OracleDB().execute_query(
        """select tk.kitid, tk.screening_subject_id, sst.subject_nhs_number
    from tk_items_t tk
    inner join ep_subject_episode_t se on se.screening_subject_id = tk.screening_subject_id
    inner join screening_subject_t sst on (sst.screening_subject_id = tk.screening_subject_id)
    inner join sd_contact_t sdc on (sdc.nhs_number = sst.subject_nhs_number)
    where tk.tk_type_id = 2
    and tk.logged_in_flag = 'N'
    and sdc.hub_id = 23159
    and device_id is null
    and tk.invalidated_date is null
    and se.latest_event_status_id in (11198, 11213)
    order by tk.kitid DESC
    fetch first 10 rows only"""
    )
    return kit_id_df


def get_nhs_no_from_batch_id(batch_id) -> pd.DataFrame:
    """
    This query returns a dataframe of NHS Numbers of the subjects in a certain batch
    We provide the batch ID e.g. 8812 and then we have a list of NHS Numbers we can verify the statuses
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
    It searches for kits that have not been logged and meet the following criteria:
    - tk.tk_type_id = 2 (Only FIT Kits)
    - tk.logged_in_at = 23159 (Hub ID that the compartments are running in)
    """
    kit_id_df = OracleDB().execute_query(
        f"""SELECT tk.kitid,tk.device_id,tk.screening_subject_id
    FROM tk_items_t tk
    INNER JOIN kit_queue kq ON kq.device_id = tk.device_id
    INNER JOIN ep_subject_episode_t se ON se.screening_subject_id = tk.screening_subject_id
    WHERE tk.logged_in_flag = 'Y'
    AND kq.test_kit_status IN ('LOGGED', 'POSTED')
    AND se.episode_status_id = 11352
    AND tk.tk_type_id = 2
    AND se.latest_event_status_id = 11223
    AND tk.logged_in_at = {smokescreen_properties["c3_fit_kit_results_test_org_id"]}
    AND tk.reading_flag = 'N'
    AND tk.test_results IS NULL
    fetch first 9 rows only
    """
    )

    return kit_id_df


def get_service_management_by_device_id(device_id: str) -> pd.DataFrame:
    """
    This SQL is similar to the one used in pkg_test_kit_queue.p_get_fit_monitor_details, but adapted to allow us to pick out sub-sets of records
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
    params = {
        "device_id": device_id
    }
    get_service_management_df = OracleDB().execute_query(query, params)
    return get_service_management_df


def update_kit_service_management_entity(
    device_id: str, normal: bool, smokescreen_properties: dict
) -> str:
    """
    This method is used to update the KIT_QUEUE table on the DB
    This is done so that we can then run two stored procedures to update the subjects and kits status to either normal or abnormal
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
    kq.analyser_code = 'UU2_tdH3',
    kq.date_time_authorised = TO_TIMESTAMP(:date_time_authorised, 'DD-Mon-YY HH24.MI.SS.FF9'),
    kq.authoriser_user_code = 'AUTO1',
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
        "date_time_authorised": str(date_time_authorised),
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
    This is needed for compartment 3 after we update the KIT_QUE table on the DB
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
