import pandas as pd
from oracle.oracle import OracleDB
import logging
from utils.oracle.subject_selection_query_builder import SubjectSelectionQueryBuilder
from utils.user_tools import UserTools
from classes.subject.subject import Subject

SUBJECT_HUB_CODE_KEY = "subject hub code"
DEFAULT_HUB_CODE = "BCS02"


class SubjectSelector:
    """
    Provides helper methods for selecting screening subjects based on preconditions
    required by specific scenarios.
    """

    @staticmethod
    def get_subject_for_manual_cease(criteria: dict) -> str:
        """
        Retrieves a subject NHS number suitable for manual cease,
        based on dynamically provided selection criteria.

        Args:
            criteria (dict): Dictionary of filtering conditions to select a subject.
                Example criteria:
                    {
                        "subject age": "75",
                        "screening status": "Inactive",
                        "subject hub code": "BCS02",
                    }

        Returns:
            str: The NHS number of the selected subject.

        Raises:
            ValueError: If no subject is found matching the criteria.
        """
        logging.info(
            f"[SUBJECT SELECTOR] Searching for subject using criteria: {criteria}"
        )

        hub_code = criteria.get(SUBJECT_HUB_CODE_KEY, DEFAULT_HUB_CODE)
        user_details = UserTools.retrieve_user(f"Hub Manager at {hub_code}")
        user = UserTools.get_user_object(user_details)
        subject = Subject()

        query_builder = SubjectSelectionQueryBuilder()
        query, bind_vars = query_builder.build_subject_selection_query(
            criteria=criteria,
            user=user,
            subject=subject,
        )

        logging.debug(
            f"[SUBJECT SELECTOR] Executing query:\n{query}\nWith bind variables: {bind_vars}"
        )
        result_df = OracleDB().execute_query(query, bind_vars)

        if result_df.empty:
            raise ValueError("No subject found for manual cease.")

        nhs_number = result_df["subject_nhs_number"].iloc[0]
        logging.info(f"[SUBJECT SELECTOR] Found subject NHS number: {nhs_number}")
        return nhs_number

    @staticmethod
    def get_subject_for_pre_invitation(criteria: dict) -> str:
        """
        Retrieves a subject NHS number suitable for pre-invitation scenarios,
        based on dynamically provided selection criteria.

        Args:
            criteria (dict): Dictionary of filtering conditions to select a subject.
                Example criteria:
                    {
                        "subject age": "75",
                        "screening status": "Pre-invitation",
                        "subject hub code": "BCS02",
                    }

        Returns:
            str: The NHS number of the selected subject.

        Raises:
            ValueError: If no subject is found matching the criteria.
        """
        logging.info(
            f"[SUBJECT SELECTOR] Searching for pre-invitation subject using criteria: {criteria}"
        )

        hub_code = criteria.get(SUBJECT_HUB_CODE_KEY, DEFAULT_HUB_CODE)
        user_details = UserTools.retrieve_user(f"Hub Manager at {hub_code}")
        user = UserTools.get_user_object(user_details)
        subject = Subject()

        query_builder = SubjectSelectionQueryBuilder()
        query, bind_vars = query_builder.build_subject_selection_query(
            criteria=criteria,
            user=user,
            subject=subject,
        )

        logging.debug(
            f"[SUBJECT SELECTOR] Executing query:\n{query}\nWith bind variables: {bind_vars}"
        )
        result_df = OracleDB().execute_query(query, bind_vars)

        if result_df.empty:
            raise ValueError("No subject found for pre-invitation scenario.")

        nhs_number = result_df["subject_nhs_number"].iloc[0]
        logging.info(f"[SUBJECT SELECTOR] Found subject NHS number: {nhs_number}")
        return nhs_number
