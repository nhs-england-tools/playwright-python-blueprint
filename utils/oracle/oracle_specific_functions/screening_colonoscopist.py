from oracle.oracle import OracleDB
import pandas as pd


def build_accredited_screening_colonoscopist_query(query_type: str) -> pd.DataFrame:
    """
    Builds a SQL query for either 'Current' or 'Expiring soon' accreditations.

    Args:
        query_type (str): Either "Current" or "Expiring soon".

    Returns:
        pd.DataFrame: A DataFrame containing accredited colonoscopist records.

    Raises:
        ValueError: If query_type is invalid.
    """
    base_query = """
    SELECT
        prs.prs_id,
        prs.person_family_name,
        prs.person_given_name,
        prs.gmc_code,
        pio305730.pio_id
    FROM person prs
    LEFT OUTER JOIN person_in_org pio305730 ON pio305730.prs_id = prs.prs_id
        AND NOT EXISTS (
            SELECT 1
            FROM person_in_org pio305730_2
            WHERE pio305730.prs_id = pio305730_2.prs_id
            AND pio305730.role_id = pio305730_2.role_id
            AND pio305730.pio_id != pio305730_2.pio_id
        )
        AND pio305730.role_id = 305730
        AND TRUNC(SYSDATE) BETWEEN pio305730.start_date AND NVL(pio305730.end_date, TO_DATE('31/12/3999','DD/MM/YYYY'))
        AND pio305730.org_id IN (
            SELECT oio305730.org_id
            FROM org oio305730
            WHERE oio305730.org_code = 'BCS001'
        )
    INNER JOIN person_accreditation pa ON pa.prs_id = prs.prs_id
        AND pa.accreditation_id = (
            SELECT pax.accreditation_id
            FROM person_accreditation pax
            WHERE pax.prs_id = prs.prs_id
            AND pax.accreditation_type_id = 305730
            ORDER BY pax.start_date DESC
            FETCH FIRST 1 ROW ONLY
        )
        AND pa.accreditation_type_id = 305730
        AND pa.start_date <= TRUNC(SYSDATE)
    """

    # condition for accreditation end date
    if query_type == "Expiring soon":
        condition = """    AND pa.end_date > TRUNC(SYSDATE)
    AND pa.end_date <= ADD_MONTHS(TRUNC(SYSDATE), 5)"""
    elif query_type == "Current":
        condition = """    AND pa.end_date > ADD_MONTHS(TRUNC(SYSDATE), 5)"""
    else:
        raise ValueError("query_type must be either 'Current' or 'Expiring soon'")

    full_query = f"""{base_query}
        {condition}
        WHERE 1=1
        AND pio305730.pio_id IS NOT NULL
        FETCH FIRST 1 ROWS ONLY"""

    df = OracleDB().execute_query(full_query)
    return df


def get_accredited_screening_colonoscopist_in_bcs001() -> pd.DataFrame:
    """
    Retrieves a list of accredited screening colonoscopists in the BCS001 organization.
    The query filters based on the role ID, accreditation type, and organization code.
    """
    query = """
        SELECT
            prs.prs_id,
            prs.person_family_name,
            prs.person_given_name,
            prs.gmc_code,
            pio305730.pio_id
        FROM person prs
        LEFT OUTER JOIN person_in_org pio305730 ON pio305730.prs_id = prs.prs_id
            AND NOT EXISTS (
                SELECT 1
                FROM person_in_org pio305730_2
                WHERE pio305730.prs_id = pio305730_2.prs_id
                AND pio305730.role_id = pio305730_2.role_id
                AND pio305730.pio_id != pio305730_2.pio_id
            )
            AND pio305730.role_id = 305730
            AND TRUNC(SYSDATE) BETWEEN pio305730.start_date AND NVL(pio305730.end_date, TO_DATE('31/12/3999','DD/MM/YYYY'))
            AND pio305730.org_id IN (
                SELECT oio305730.org_id
                FROM org oio305730
                WHERE oio305730.org_code = 'BCS001'
            )
        INNER JOIN person_accreditation pa ON pa.prs_id = prs.prs_id
            AND pa.accreditation_id = (
                SELECT pax.accreditation_id
                FROM person_accreditation pax
                WHERE pax.prs_id = prs.prs_id
                AND pax.accreditation_type_id = 305730
                ORDER BY pax.start_date DESC
                FETCH FIRST 1 ROW ONLY
            )
    """
    df = OracleDB().execute_query(query)
    return df
