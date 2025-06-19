"""
Outcome List Tests: These tests cover the Outcome List, accessed from the Outcome List tab.
"""

import pytest
from utils.api_utils import ApiUtils
from playwright.sync_api import BrowserContext


pytestmark = [pytest.mark.outcome_list, pytest.mark.uiapi]

API_URL = "/bss/outcome/search"


def test_outcome_list_search_all(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on all Outcome List
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[typeDescription]": "NBR",
        "columnSortDirectionWithOrder[0transferDateTime]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 1
    for description in response_data["results"]:
        assert str(description["typeDescription"]).startswith("NBR")


def test_invalid_national_user(api_national_user_session: BrowserContext) -> None:
    """
    API test to check an invaild user (National user) doesn't have access to the Outcome List, so returns a 403 error.
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSortDirectionWithOrder[0transferDateTime]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_national_user_session, API_URL).get_request(
        data, False
    )
    assert response_data == 403


def test_invalid_helpdesk_user(api_helpdesk_session: BrowserContext) -> None:
    """
    API test to check an invaild user (Helpdesk user) doesn't have access to the Outcome List, so returns a 403 error.
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSortDirectionWithOrder[0transferDateTime]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_helpdesk_session, API_URL).get_request(data, False)
    assert response_data == 403


def test_outcome_list_search_data_type(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on Batch 121 on the Outcome List
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[typeDescription]": "BATCH",
        "columnSortDirectionWithOrder[0transferDateTime]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 2
    for description in response_data["results"]:
        assert str(description["typeDescription"]).startswith("Batch 121")
