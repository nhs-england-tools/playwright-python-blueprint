from oracle.oracle import OracleDB
import pandas as pd


def check_if_subject_has_temporary_address(nhs_no: str) -> pd.DataFrame:
    """
    Checks if the subject has a temporary address in the database.
    Args:
        nhs_no (str): The NHS number of the subject.
    Returns:
        pd.DataFrame: A single-row DataFrame with the address status.
        Either 'Subject has a temporary address' or `Subject doesn't have a temporary address`

    Details:
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
            ELSE 'Subject doesn't have a temporary address'
        END AS address_status
        FROM DUAL
    """
    bind_vars = {"nhs_no": nhs_no}
    df = OracleDB().execute_query(query, bind_vars)
    return df
