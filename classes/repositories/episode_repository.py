from typing import Optional
from utils.oracle.oracle import OracleDB


class EpisodeRepository:
    """
    Repository for accessing episode data from the database.
    """

    def get_episode_result(self, episode_id: int) -> str:
        """
        Gets the episode result description for a given episode ID.
        Args:
            episode_id (int): The ID of the episode.
        Returns:
            str: The episode result description.
        """
        sql = """
            SELECT vv.description
            FROM ep_subject_episode_t ep
            INNER JOIN valid_values vv ON vv.valid_value_id = ep.episode_result_id
            WHERE ep.subject_epis_id = :episode_id
        """
        params = {"episode_id": episode_id}
        episode_result_df = OracleDB().execute_query(sql, params)
        episode_result = episode_result_df["description"].iloc[0]
        return episode_result

    def find_episode_id_for_subject(self, nhs_no: str) -> int:
        """
        Finds the latest episode id for a subject.
        Args:
            nhs_no (str): The subject's NHS Number.
        Returns:
            int: The latest episode ID for the subject.
        """
        subject_id = OracleDB().get_subject_id_from_nhs_number(nhs_no)
        sql_query = """
            SELECT
                ep.subject_epis_id,
                ep.screening_subject_id,
                ep.episode_type_id,
                ep.episode_status_id
            FROM ep_subject_episode_t ep
            WHERE ep.screening_subject_id = :subject_id
            ORDER BY ep.subject_epis_id DESC
        """
        params = {"subject_id": subject_id}
        episode_df = OracleDB().execute_query(sql_query, params)
        episode_id = episode_df["subject_epis_id"].iloc[0]
        return int(episode_id)

    def confirm_episode_result(self, nhs_no: str, expected_episode_result: str) -> None:
        """
        Confirms that the episode result for a subject matches the expected value.
        Args:
            nhs_no (str): The subject's NHS Number.
            expected_episode_result (str): The expected episode result description.
        """
        episode_id = self.find_episode_id_for_subject(nhs_no)
        episode_result = self.get_episode_result(episode_id)
        assert (
            episode_result == expected_episode_result
        ), f"Expected episode result to be '{expected_episode_result}' but got '{episode_result}'"
