import pytest
from utils.subject_assertion import subject_assertion

pytestmark = [pytest.mark.utils_local]

nhs_number = "9233639266"


def test_subject_assertion_true():
    criteria = {"screening status": "Inactive", "subject age": "> 28"}
    assert subject_assertion(nhs_number, criteria) is True


def test_subject_assertion_false():
    criteria = {"screening status": "Call", "subject age": "< 28"}
    assert subject_assertion(nhs_number, criteria) is False


def test_subject_assertion_false_with_some_true():
    criteria = {
        "screening status": "Inactive",
        "subject age": "> 28",
        "latest episode type": "FOBT",
        "latest episode status": "Open",
        "latest episode has referral date": "Past",
        "latest episode has diagnosis date": "No",
        "latest episode diagnosis date reason": "NULL",
    }
    assert subject_assertion(nhs_number, criteria) is False
