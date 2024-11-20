import pytest
from utils.user_tools import UserTools, UserToolsException


pytestmark = [pytest.mark.utils]

def test_nhs_number_checks() -> None:
    assert UserTools().retrieve_user("Example User 1")
