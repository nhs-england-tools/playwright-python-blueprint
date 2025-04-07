import pytest
import utils.user_tools
from utils.user_tools import UserTools, UserToolsException
from pathlib import Path

pytestmark = [pytest.mark.utils]


def test_retrieve_user(monkeypatch: object) -> None:
    monkeypatch.setattr(utils.user_tools, "USERS_FILE", Path(__file__).parent / "resources" / "test_users.json")

    test_user = UserTools.retrieve_user("Test User")
    assert test_user["username"] == "TEST_USER1"
    assert test_user["test_key"] == "TEST A"

    test_user2 = UserTools.retrieve_user("Test User 2")
    assert test_user2["username"] == "TEST_USER2"
    assert test_user2["test_key"] == "TEST B"

    with pytest.raises(UserToolsException, match=r'User \[Invalid User\] is not present in users.json'):
        UserTools.retrieve_user("Invalid User")
