import pytest
from utils.oracle.subject_selection_query_builder import (
    SubjectSelectionQueryBuilder,
    SubjectSelectionCriteriaKey,
)
from classes.subject.subject import Subject
from classes.user.user import User


@pytest.fixture
def builder():
    return SubjectSelectionQueryBuilder()


@pytest.fixture
def dummy_subject():
    subject = Subject()
    subject.screening_status_change_date = None
    subject.date_of_death = None
    return subject


@pytest.fixture
def dummy_user():
    return User()


def test_add_criteria_subject_age_y_d(builder, dummy_user, dummy_subject):
    # This format triggers the 'y/d' logic branch
    criteria = {"subject age (y/d)": "60/0"}

    builder._add_variable_selection_criteria(criteria, dummy_user, dummy_subject)
    where_clause = " ".join(builder.sql_where)

    assert "c.date_of_birth" in where_clause
    assert "ADD_MONTHS(TRUNC(TRUNC(SYSDATE))" in where_clause


def test_add_criteria_subject_hub_code_with_enum(builder, dummy_user, dummy_subject):
    criteria = {"subject hub code": "user organisation"}
    builder._add_variable_selection_criteria(criteria, dummy_user, dummy_subject)
    sql = " ".join(builder.sql_where)
    assert "c.hub_id" in sql
    assert "SELECT hub.org_id" in sql


def test_invalid_criteria_key_raises_exception(builder, dummy_user, dummy_subject):
    criteria = {"invalid key": "value"}
    with pytest.raises(Exception):
        builder._add_variable_selection_criteria(criteria, dummy_user, dummy_subject)


def test_preprocess_commented_criterion_skips_processing(builder, dummy_subject):
    result = builder._preprocess_criteria(
        "subject age", "#this is ignored", dummy_subject
    )
    assert result is False


def test_dispatch_known_key_executes(builder, dummy_user, dummy_subject):
    # Arrange
    builder.criteria_key = SubjectSelectionCriteriaKey.SUBJECT_AGE
    builder.criteria_value = "60"
    builder.criteria_comparator = " = "
    builder.criteria_key_name = "subject age"

    # Act
    builder._dispatch_criteria_key(dummy_user, dummy_subject)

    # Assert
    where_clause = " ".join(builder.sql_where)
    assert "c.date_of_birth" in where_clause
    assert "FLOOR(MONTHS_BETWEEN(TRUNC(SYSDATE), c.date_of_birth)/12)" in where_clause
