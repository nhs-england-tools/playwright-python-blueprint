from oracle.oracle import OracleDB
import pandas as pd
from utils.oracle.oracle_specific_functions.enums import SqlQueryValues
from typing import Optional


def get_subjects_for_investigation_dataset_updates(
    number_of_subjects: int, hub_id: str
) -> pd.DataFrame:
    """
    This is used to get subjects for compartment 6
    It finds subjects who:
        - Have the latest event status of A323 - Post-investigation Appointment
        - Have a single episode with an incomplete colonoscopy dataset
        - Have a valid GP practice linked and are associated  with the specified hub

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


def get_investigation_dataset_polyp_category(
    dataset_id: int, polyp_number: int
) -> Optional[str]:
    """
    Retrieves the polyp category for a given dataset ID and polyp number.

    Args:
        dataset_id (int): The ID of the dataset.
        polyp_number (int): The number of the polyp.

    Returns:
        Optional[str]: The polyp category description if found, otherwise None.
    """
    query = """
    select polyp_category
    from (
    select
    rank () over (order by p.polyp_id) as polyp_number,
    pc.description as polyp_category
    from ds_polyp_t p
    left outer join valid_values pc
    on pc.valid_value_id = p.polyp_category_id
    where ext_test_id = :ext_test_id
    and p.deleted_flag = 'N'
    )
    where polyp_number = :polyp_number
    """
    bind_vars = {
        "ext_test_id": dataset_id,
        "polyp_number": polyp_number,
    }
    df = OracleDB().execute_query(query, bind_vars)
    polyp_category = df["polyp_category"].iloc[0] if not df.empty else None
    return polyp_category


def get_investigation_dataset_polyp_algorithm_size(
    dataset_id: int, polyp_number: int
) -> Optional[str]:
    """
    Retrieves the polyp algorithm size for a given dataset ID and polyp number.

    Args:
        dataset_id (int): The ID of the dataset.
        polyp_number (int): The number of the polyp.

    Returns:
        Optional[str]: The polyp algorithm size if found, otherwise None.
    """
    query = """
    select polyp_algorithm_size
    from (
    select
    rank () over (order by p.polyp_id) as polyp_number,
    p.polyp_algorithm_size
    from ds_polyp_t p
    where ext_test_id = :ext_test_id
    and p.deleted_flag = 'N'
    )
    where polyp_number = :polyp_number
    """
    bind_vars = {
        "ext_test_id": dataset_id,
        "polyp_number": polyp_number,
    }
    df = OracleDB().execute_query(query, bind_vars)
    polyp_algorithm_size = df["polyp_algorithm_size"].iloc[0] if not df.empty else None
    return polyp_algorithm_size
