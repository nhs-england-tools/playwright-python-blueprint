import pytest
from utils.oracle.subject_creation_util import CreateSubjectSteps
from utils.oracle.subject_selection_query_builder import (
    SubjectSelectionQueryBuilder,
)
from classes.subject.subject import Subject
from classes.user.user import User
from utils.oracle.oracle import OracleDB
import pandas as pd
import logging
from datetime import datetime
from typing import Optional


@pytest.fixture
def subject_steps():
    return CreateSubjectSteps()


pytestmark = [pytest.mark.utils_local]


def test_create_custom_subject_age(subject_steps):
    """
    Test creating a subject with a specific age.
    Verifies that the subject is created with the correct date of birth corresponding to the specified age.
    Args:
        subject_steps: Fixture providing subject creation steps.
    Raises:
        AssertionError: If the created subject's age does not match the expected age.
    """
    expected_age = 30
    requirements = {"age": str(expected_age)}
    nhs_no = subject_steps.create_custom_subject(requirements)
    df = find_subject(nhs_no)
    date_of_birth_str = str(df["date_of_birth"].iloc[0])
    date_of_birth = datetime.strptime(date_of_birth_str[:10], "%Y-%m-%d").date()

    age = (datetime.now().date() - date_of_birth).days // 365
    assert age == expected_age, f"Expected age to be {expected_age}, but got {age}"
    logging.info(
        f"Assertion passed, subject created with the correct age.\nExpected: {expected_age}\nFound: {age}"
    )


def test_create_custom_subject_age_yd(subject_steps):
    """
    Test creating a subject with a specific age in years and days.
    Verifies that the subject is created with the correct date of birth corresponding to the specified age.
    Args:
        subject_steps: Fixture providing subject creation steps.
    Raises:
        AssertionError: If the created subject's age does not match the expected age.
    """
    expected_years = 65
    expected_days = 25
    requirements = {"age (y/d)": f"{expected_years}/{expected_days}"}
    nhs_no = subject_steps.create_custom_subject(requirements)
    df = find_subject(nhs_no)
    date_of_birth_val = df["date_of_birth"].iloc[0]

    # Handle pandas.Timestamp or string
    if hasattr(date_of_birth_val, "to_pydatetime"):
        date_of_birth = date_of_birth_val.to_pydatetime().date()
    elif isinstance(date_of_birth_val, str):
        date_of_birth = datetime.strptime(date_of_birth_val[:10], "%Y-%m-%d").date()
    else:
        date_of_birth = date_of_birth_val

    today = datetime.now().date()
    delta = today - date_of_birth
    actual_years = delta.days // 365
    actual_days = delta.days % 365

    assert actual_years == expected_years and actual_days == expected_days, (
        f"Expected age to be {expected_years} years and {expected_days} days, "
        f"but got {actual_years} years and {actual_days} days"
    )
    logging.info(
        f"Assertion passed, subject created with the correct age.\n"
        f"Expected: {expected_years} years, {expected_days} days\n"
        f"Found: {actual_years} years, {actual_days} days"
    )


def test_create_custom_subject_gp_practice(subject_steps):
    """
    Test creating a subject with a specific GP practice code.
    Verifies that the subject is created with the correct GP practice code.
    Args:
        subject_steps: Fixture providing subject creation steps.
    Raises:
        AssertionError: If the created subject's GP practice code does not match the expected
    """
    expected_gp_practice_code = 13482
    requirements = {"gp practice": "C81014"}
    nhs_no = subject_steps.create_custom_subject(requirements)
    df = find_subject(
        nhs_no,
        " c.gp_practice_id ",
    )
    gp_practice_code = df["gp_practice_id"].iloc[0]
    assert (
        gp_practice_code == expected_gp_practice_code
    ), f"Expected GP practice code to be {expected_gp_practice_code}, but got {gp_practice_code}"
    logging.info(
        f"Assertion passed, subject created with the correct GP practice code.\n"
        f"Expected: {expected_gp_practice_code}\n"
        f"Found: {gp_practice_code}"
    )


def test_create_custom_subject_active_gp_practice(subject_steps):
    """
    Test creating a subject with an active GP practice linked to both hub and screening centre.
    Verifies that the subject is created with the correct GP practice code.
    Args:
        subject_steps: Fixture providing subject creation steps.
    Raises:
        AssertionError: If the created subject's GP practice code does not match the expected
    """
    expected_gp_practice_code = 22414
    requirements = {"active gp practice in hub/sc": "BCS01/BCS001"}
    nhs_no = subject_steps.create_custom_subject(requirements)
    df = find_subject(nhs_no, " c.gp_practice_id ")
    gp_practice_code = df["gp_practice_id"].iloc[0]
    assert (
        gp_practice_code == expected_gp_practice_code
    ), f"Expected GP practice code to be {expected_gp_practice_code}, but got {gp_practice_code}"
    logging.info(
        f"Assertion passed, subject created with the correct GP practice code.\n"
        f"Expected: {expected_gp_practice_code}\n"
        f"Found: {gp_practice_code}"
    )


def test_create_custom_subject_inactive_gp_practice(subject_steps):
    """
    Test creating a subject with an inactive GP practice (not linked to both hub and SC).
    Verifies that the subject is created with an inactive GP practice.
    Args:
        subject_steps: Fixture providing subject creation steps.
    Raises:
        AssertionError: If the created subject does not have an inactive GP practice.
    """
    requirements = {"inactive gp practice": ""}
    nhs_no = subject_steps.create_custom_subject(requirements)
    df = find_subject(nhs_no, inactive_gp_practice=True)
    assert (
        not df.empty
    ), "Expected subject to have an inactive GP practice, but none found"
    logging.info(
        f"Assertion passed, subject created with an inactive GP practice.\nNHS Number: {nhs_no}"
    )


def test_create_custom_subject_invalid_criteria(subject_steps):
    """
    Test creating a subject with an invalid criteria.
    Verifies that a ValueError is raised with the appropriate message.
    Args:
        subject_steps: Fixture providing subject creation steps.
    Raises:
        ValueError: If an invalid criteria is provided.
    """
    requirements = {"invalid_field": "value"}
    with pytest.raises(ValueError) as excinfo:
        subject_steps.create_custom_subject(requirements)
    assert "The criteria provided (invalid_field) is not valid" in str(excinfo.value)


def find_subject(
    nhs_number: str,
    column: Optional[str] = None,
    inactive_gp_practice: Optional[bool] = False,
) -> pd.DataFrame:
    """
    Finds a subject by NHS number, optionally retrieving a specific column and filtering for inactive GP practice.
    Args:
        nhs_number (str): The NHS number of the subject to find.
        column (Optional[str]): Specific column to retrieve. Defaults to None.
        inactive_gp_practice (Optional[bool]): If True, filters for subjects with inactive GP practice. Defaults to False.
    Returns:
        pd.DataFrame: DataFrame containing the subject information.
    """
    criteria = {"nhs number": nhs_number}
    if column:
        criteria["add column to select statement"] = column
    if inactive_gp_practice:
        criteria["has gp practice"] = "Yes - inactive"
    subject = Subject()
    user = User()
    builder = SubjectSelectionQueryBuilder()

    query, bind_vars = builder.build_subject_selection_query(
        criteria=criteria,
        user=user,
        subject=subject,
        subjects_to_retrieve=1,
    )

    df = OracleDB().execute_query(query, bind_vars)
    return df
