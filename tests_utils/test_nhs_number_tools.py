import pytest
from utils.nhs_number_tools import NHSNumberTools, NHSNumberToolsException

pytestmark = [pytest.mark.utils]


def test_nhs_number_checks() -> None:
    assert NHSNumberTools._nhs_number_checks("1234567890") == None

    with pytest.raises(
        Exception, match=r"The NHS number provided \(A234567890\) is not numeric."
    ):
        NHSNumberTools._nhs_number_checks("A234567890")

    with pytest.raises(
        NHSNumberToolsException,
        match=r"The NHS number provided \(123\) is not 10 digits",
    ):
        NHSNumberTools._nhs_number_checks("123")


def test_spaced_nhs_number() -> None:
    assert NHSNumberTools.spaced_nhs_number("1234567890") == "123 456 7890"
    assert NHSNumberTools.spaced_nhs_number(3216549870) == "321 654 9870"
