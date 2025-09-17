from oracle.oracle import OracleDB
import logging
import pandas as pd


def set_org_parameter_value(param_id: int, param_value: str, org_id: str) -> None:
    """
    Updates the value of an organisation parameter in the database.

    This function first ends any existing values for the given parameter and organisation by updating their effective dates and audit information.
    It then inserts a new value for the parameter with the provided value and sets the audit fields accordingly.

    Args:
        param_id (int): The ID of the parameter to update.
        param_value (str): The new value to set for the parameter.
        org_id (str): The organisation ID for which the parameter should be set.
    """
    # End any old values
    sql_update = (
        "UPDATE org_parameters op "
        "SET op.effective_from = op.effective_from - 1, "
        "op.effective_to = CASE WHEN op.effective_to IS NULL THEN TRUNC(SYSDATE)-1 ELSE op.effective_to - 1 END, "
        "op.audit_reason = 'AUTOMATED TESTING - END', "
        "op.datestamp = SYSTIMESTAMP "
        "WHERE op.org_id = :org_id "
        "AND param_id = :param_id"
    )
    params = {"org_id": org_id, "param_id": param_id}
    logging.info(f"executing query to end any old values: {sql_update}")
    OracleDB().update_or_insert_data_to_table(sql_update, params)

    # Insert new value
    sql_insert = """
        INSERT INTO org_parameters (
        org_param_id, org_code, org_id, param_id, val,
        effective_from, pio_id, audit_reason, datestamp
        )
        VALUES (
        seq_org_param.NEXTVAL,
        (SELECT org_code FROM org WHERE org_id = :org_id),
        :org_id,
        :param_id,
        :param_value,
        TRUNC(SYSDATE),
        1,
        'AUTOMATED TESTING - ADD',
        SYSTIMESTAMP
        )
        """
    params = {"org_id": org_id, "param_id": param_id, "param_value": param_value}
    logging.info(f"executing query to set new value: {sql_insert}")
    OracleDB().update_or_insert_data_to_table(sql_insert, params)


def get_org_parameter_value(param_id: int, org_id: str) -> pd.DataFrame:
    """
    Retrieves the value of an organisation parameter from the database.

    Args:
        param_id (int): The ID of the parameter to retrieve.
        org_id (str): The organisation ID for which the parameter value should be retrieved.

    Returns:
        pd.DataFrame: A DataFrame containing the parameter value and its effective date.
    """
    query = """
        SELECT val, effective_from, audit_reason
        FROM org_parameters
        WHERE param_id = :param_id
        AND org_id = :org_id
    """
    bind_vars = {"param_id": param_id, "org_id": org_id}
    logging.debug(f"Fetching parameter {param_id} for org_id={org_id}")
    df = OracleDB().execute_query(query, bind_vars)
    return df


def check_parameter(param_id: int, org_id: str, expected_param_value: str) -> bool:
    """
    Check if the organization parameter is set correctly.
    Args:
        param_id (int): The ID of the parameter to check.
        org_id (str): The ID of the organization.
        expected_param_value (str): The expected value of the parameter.

    Returns:
        bool: True if the parameter is set correctly, False otherwise.
    """
    df = get_org_parameter_value(param_id, org_id)
    for _, row in df.iterrows():
        val_matches = str(row["val"]) == expected_param_value
        audit_reason_matches = row["audit_reason"] == "AUTOMATED TESTING - ADD"

        if val_matches and audit_reason_matches:
            logging.info(f"Parameter {param_id} is set correctly: {row['val']}")
            return True

    logging.warning(f"Parameter {param_id} is not set correctly, updating parameter.")
    return False
