from utils.oracle.subject_selection_query_builder import SubjectSelectionQueryBuilder
from utils.oracle.oracle import OracleDB
from classes.subject import Subject
from classes.user import User
from classes.user_role_type import UserRoleType
from typing import Optional
import logging


def subject_assertion(
    nhs_number: str, criteria: dict, user_role: Optional[UserRoleType] = None
) -> None:
    """
    Asserts that a subject with the given NHS number exists in the database and matches the provided criteria.
    Args:
        nhs_number (str): The NHS number of the subject to find.
        criteria (dict): A dictionary of criteria to match against the subject's attributes.
    """
    logging.info("[DB ASSERTIONS] Starting subject_assertion method")
    nhs_number_string = "nhs number"
    subject_nhs_number_string = "subject_nhs_number"
    if user_role:
        user = User.from_user_role_type(user_role)
    else:
        user = User()
    builder = SubjectSelectionQueryBuilder()

    logging.debug(
        "[SUBJECT ASSERTIONS] Executing base query to populate subject object"
    )
    subject = Subject().populate_subject_object_from_nhs_no(nhs_number)

    criteria[nhs_number_string] = nhs_number

    # Check all criteria together first
    logging.info(
        "[SUBJECT ASSERTIONS] Running query to check subject matches criteria:"
    )
    query, bind_vars = builder.build_subject_selection_query(
        criteria=criteria,
        user=user,
        subject=subject,
        subjects_to_retrieve=1,
    )
    df = OracleDB().execute_query(query, bind_vars)
    if nhs_number in df[subject_nhs_number_string].values:
        logging.info("[DB ASSERTIONS COMPLETE] Subject matches the expected criteria")
        return

    # Check each criterion independently
    failed_criteria = []
    criteria_keys = [key for key in criteria if key != nhs_number_string]
    for key in criteria_keys:
        single_criteria = {nhs_number_string: nhs_number, key: criteria[key]}
        query, bind_vars = builder.build_subject_selection_query(
            criteria=single_criteria,
            user=user,
            subject=subject,
            subjects_to_retrieve=1,
            enable_logging=False,
        )
        df = OracleDB().execute_query(query, bind_vars)
        if (
            subject_nhs_number_string not in df.columns
            or nhs_number not in df[subject_nhs_number_string].values
        ):
            failed_criteria.append((key, criteria[key]))

    if failed_criteria:
        log_message = (
            "[DB ASSERTIONS FAILED] Subject Assertion Failed\nFailed criteria:\n"
            + "\n".join(
                [
                    f"Criteria key: {key}, Criteria Value: {value}"
                    for key, value in failed_criteria
                ]
            )
        )
        raise AssertionError(log_message)
    else:
        raise AssertionError(
            "[DB ASSERTIONS FAILED] Subject Assertion Failed: Criteria combination is invalid or conflicting."
        )
