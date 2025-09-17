from utils.oracle.subject_selection_query_builder import SubjectSelectionQueryBuilder
from utils.oracle.oracle import OracleDB
from classes.user.user import User
from classes.subject.subject import Subject
import logging
import pytest


def test_subject_selection_query_builder():
    """
    This function demonstrates how to use the builder to create a query
    based on specified criteria and user/subject objects.
    """

    criteria = {
        "screening status": "Surveillance",
    }
    user = User()
    subject = Subject()
    subject.set_screening_status_id(4006)

    builder = SubjectSelectionQueryBuilder()

    query, bind_vars = builder.build_subject_selection_query(
        criteria=criteria, user=user, subject=subject, subjects_to_retrieve=1
    )

    df = OracleDB().execute_query(query, bind_vars)
    logging.info(f"DataFrame: {df}")
    assert df is not None, "DataFrame should not be None"
    assert df.shape[0] == 1, "DataFrame should contain exactly one row"

    criteria = {
        "nhs number": "9163626810",
    }
    user = User()
    subject = Subject()
    subject.set_nhs_number("9163626810")
    query, bind_vars = builder.build_subject_selection_query(
        criteria=criteria, user=user, subject=subject, subjects_to_retrieve=1
    )

    df = OracleDB().execute_query(query, bind_vars)
    logging.info(f"DataFrame: {df}")
    assert df is not None, "DataFrame should not be None"
    assert df.shape[0] == 1, "DataFrame should contain exactly one row"
    assert (
        df.iloc[0]["subject_nhs_number"] == "9163626810"
    ), "NHS number should match the input"

    criteria = {
        "subject has temporary address": "No",
    }
    user = User()
    subject = Subject()
    query, bind_vars = builder.build_subject_selection_query(
        criteria=criteria, user=user, subject=subject, subjects_to_retrieve=1
    )

    df = OracleDB().execute_query(query, bind_vars)
    logging.info(f"DataFrame: {df}")
    assert df is not None, "DataFrame should not be None"
    assert df.shape[0] == 1, "DataFrame should contain exactly one row"
