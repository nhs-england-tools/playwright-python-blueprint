import pytest
import os
from pathlib import Path
from utils.axe import Axe


pytestmark = [pytest.mark.utils]

AXE_REPORTS_DIR = Path(__file__).parent.parent / "axe-reports"
TEST_JSON_DEFAULT_FILENAME = "www_test_com__1.json"
TEST_JSON_CUSTOM_FILENAME = "test_json_file.json"
TEST_HTML_DEFAULT_FILENAME = "www_test_com__1.html"
TEST_HTML_CUSTOM_FILENAME = "test_html_file.html"

@pytest.fixture(scope="session", autouse=True)
def remove_files_before_test() -> None:
    for file in [TEST_JSON_DEFAULT_FILENAME, TEST_JSON_CUSTOM_FILENAME, TEST_HTML_DEFAULT_FILENAME, TEST_HTML_CUSTOM_FILENAME]:
        if os.path.isfile(AXE_REPORTS_DIR / file):
            os.remove(AXE_REPORTS_DIR / file)

def test_build_run_command() -> None:
    assert Axe._build_run_command(['test']) == "run({runOnly: { type: 'tag', values: ['test'] }})"

def test_modify_filename_for_report() -> None:
    assert Axe._modify_filename_for_report('https://www.test.com/1/2\\3/') == "www_test_com__1__2__3"

def test_create_path_for_report() -> None:
    assert Axe._create_path_for_report('test123.html') == Path(__file__).parent.parent / "axe-reports" / "test123.html"

def test_create_json_report() -> None:
    test_data = {"url": "https://www.test.com/1"}

    # Default generation
    Axe._create_json_report(test_data)
    with open(AXE_REPORTS_DIR / TEST_JSON_DEFAULT_FILENAME, 'r') as file:
        assert file.read() == '{"url": "https://www.test.com/1"}'

    # With custom filename
    Axe._create_json_report(test_data, TEST_JSON_CUSTOM_FILENAME.replace(".json", ""))
    with open(AXE_REPORTS_DIR / TEST_JSON_CUSTOM_FILENAME, 'r') as file:
        assert file.read() == '{"url": "https://www.test.com/1"}'

def test_create_html_report() -> None:
    test_data = {"testEngine":
                {"name": "axe-core", "version": "4.10.2"},
                "testRunner": {"name": "axe"},
                "testEnvironment": {"userAgent": "test browser"},
                "timestamp": "2024-11-04T16:14:57.934Z",
                "url": "https://www.test.com/1",
                "toolOptions": {"runOnly": {"type": "tag", "values": ["wcag2a", "wcag21a", "wcag2aa", "wcag21aa", "best-practice"]}, "reporter": "v1"},
                "inapplicable": [{"id": "test", "impact": None, "tags": ["cat.keyboard", "best-practice"], "description": "test", "help": "test", "helpUrl": "test", "nodes": []}],
                "passes": [{"id": "test", "impact": None, "tags": ["cat.keyboard", "best-practice"], "description": "test", "help": "test", "helpUrl": "test", "nodes": []}],
                "incomplete": [],
                "violations": [{"id": "test", "impact": None, "tags": ["cat.keyboard", "best-practice"], "description": "test", "help": "test", "helpUrl": "test", "nodes": []}]
    }
    expected_file_data = Axe._generate_html(test_data)

    # Default generation
    Axe._create_html_report(test_data)
    with open(AXE_REPORTS_DIR / TEST_HTML_DEFAULT_FILENAME, 'r') as file:
        assert file.read() == expected_file_data

    # With custom filename
    Axe._create_html_report(test_data, TEST_HTML_CUSTOM_FILENAME.replace(".html", ""))
    with open(AXE_REPORTS_DIR / TEST_HTML_CUSTOM_FILENAME, 'r') as file:
        assert file.read() == expected_file_data

def test_generate_html() -> None:
    test_data = {"testEngine":
                {"name": "axe-core", "version": "4.10.2"},
                "testRunner": {"name": "axe"},
                "testEnvironment": {"userAgent": "test browser"},
                "timestamp": "2024-11-04T16:14:57.934Z",
                "url": "https://www.test.com/2",
                "toolOptions": {"runOnly": {"type": "tag", "values": ["wcag2a", "wcag21a", "wcag2aa", "wcag21aa", "best-practice"]}, "reporter": "v1"},
                "inapplicable": [{"id": "test1", "impact": None, "tags": ["cat.keyboard", "best-practice"], "description": "test", "help": "test", "helpUrl": "test", "nodes": []}],
                "passes": [{"id": "test2", "impact": None, "tags": ["cat.keyboard", "best-practice"], "description": "test", "help": "test", "helpUrl": "test", "nodes": []}],
                "incomplete": [],
                "violations": [{"id": "test3", "impact": "high", "tags": ["cat.keyboard", "best-test"], "description": "test", "help": "test", "helpUrl": "test url", "nodes": []}]
    }
    results = Axe._generate_html(test_data)

    for text_to_assert in ["axe", "test browser", "https://www.test.com/2", "test1", "test2", "test3", "high", "best-test", "test url"]:
        assert text_to_assert in results
