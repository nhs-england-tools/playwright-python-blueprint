import pytest
import os
from pathlib import Path
from utils.jira_confluence_util import JiraConfluenceUtil


pytestmark = [pytest.mark.utils]

TEST_RESULTS_DIR = (
    Path(__file__).parent.joinpath("resources").joinpath("jira-util-test-dir")
)


@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch) -> None:
    monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **kw: None)
    applicable_vars = [
        "JIRA_URL",
        "JIRA_PROJECT_KEY",
        "JIRA_API_KEY",
        "CONFLUENCE_URL",
        "CONFLUENCE_API_KEY",
    ]
    for var in applicable_vars:
        os.environ[var] = "test"


def test_check_init() -> None:
    """Check initialization works as intended"""
    test_init = JiraConfluenceUtil(TEST_RESULTS_DIR)
    assert isinstance(test_init, JiraConfluenceUtil)

    with pytest.raises(ValueError):
        JiraConfluenceUtil("a/fake/directory")


def test_can_complete_jira_actions_check(monkeypatch: object) -> None:
    """Test that errors occur when env values not set for Jira"""
    applicable_vars = ["JIRA_URL", "JIRA_PROJECT_KEY", "JIRA_API_KEY"]
    # monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **kw: None)

    for expected_var in applicable_vars:
        test_util = JiraConfluenceUtil(TEST_RESULTS_DIR)
        for var in applicable_vars:
            os.environ[var] = "test"
        os.environ.pop(expected_var, None)
        with pytest.raises(ValueError) as e:
            test_util._can_complete_jira_actions_check()
        assert (
            str(e.value)
            == f"The [{expected_var}] os environment variable is required to complete any Jira actions"
        )


def test_can_complete_confluence_actions_check(monkeypatch: object) -> None:
    """Test that errors occur when env values not set for Confluence"""
    applicable_vars = ["CONFLUENCE_URL", "CONFLUENCE_API_KEY"]
    # monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **kw: None)

    for expected_var in applicable_vars:
        test_util = JiraConfluenceUtil(TEST_RESULTS_DIR)
        for var in applicable_vars:
            os.environ[var] = "test"
        os.environ.pop(expected_var, None)
        with pytest.raises(ValueError) as e:
            test_util._can_complete_confluence_actions_check()
        assert (
            str(e.value)
            == f"The [{expected_var}] os environment variable is required to complete any Confluence actions"
        )


def test_get_files_to_upload_to_jira() -> None:
    """Test that valid Jira reference checks work"""
    test_util = JiraConfluenceUtil(TEST_RESULTS_DIR)
    results_list = test_util._get_files_to_upload_to_jira(True, True, True, True)
    # Get all paths
    path_list = []
    for item in results_list:
        path_list.append(item["path"])
    # Get all test files
    test_files = [
        TEST_RESULTS_DIR.joinpath("report.html"),
        TEST_RESULTS_DIR.joinpath("test_image.png"),
        TEST_RESULTS_DIR.joinpath("csv_test.csv"),
        TEST_RESULTS_DIR.joinpath("screenshot/test_image_b.png"),
        TEST_RESULTS_DIR.joinpath("test-sub-dir/trace.zip"),
    ]
    assert len(path_list) == len(test_files)
    for test_file in test_files:
        assert test_file in path_list
