from oracle.oracle import OracleDB
import pandas as pd


def get_nhs_no_from_batch_id(batch_id: str) -> pd.DataFrame:
    """
    This query returns a dataframe of NHS Numbers of the subjects in a certain batch
    We provide the batch ID e.g. 8812 and then we have a list of NHS Numbers we can verify the statuses

    Args:
        batch_id (str): The batch ID you want to get the subjects from

    Returns:
        nhs_number_df (pd.DataFrame): A pandas DataFrame containing the result of the query
    """
    query = """
        SELECT SUBJECT_NHS_NUMBER
        FROM SCREENING_SUBJECT_T ss
        INNER JOIN sd_contact_t c ON ss.subject_nhs_number = c.nhs_number
        INNER JOIN LETT_BATCH_RECORDS lbr
        ON ss.SCREENING_SUBJECT_ID = lbr.SCREENING_SUBJECT_ID
        WHERE lbr.BATCH_ID IN :batch_id
        AND ss.screening_status_id != 4008
        ORDER BY ss.subject_nhs_number
    """
    params = {"batch_id": batch_id}
    nhs_number_df = OracleDB().execute_query(query, params)
    return nhs_number_df
