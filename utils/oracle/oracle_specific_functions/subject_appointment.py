from oracle.oracle import OracleDB
import pandas as pd
from enums import SqlQueryValues


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
    and tk.logged_in_at = :hub_id
    and tk.algorithm_sc_id = :algorithm_sc_id
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

    hub_id = 23159
    algorithm_sc_id = 23162

    params = {
        "positive_appointment_booked": SqlQueryValues.POSITIVE_APPOINTMENT_BOOKED,
        "open_episode_status_id": SqlQueryValues.OPEN_EPISODE_STATUS_ID,
        "hub_id": hub_id,
        "algorithm_sc_id": algorithm_sc_id,
        "subjects_to_retrieve": subjects_to_retrieve,
    }

    subjects_df = OracleDB().execute_query(query, params)

    return subjects_df
