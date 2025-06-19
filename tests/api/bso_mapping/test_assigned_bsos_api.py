"""
GP Practices Assigned to BSO Tests: These tests cover the GP Practices Assigned to BSO, accessed from the BSO Mapping tab.
"""

import pytest
from utils.api_utils import ApiUtils
from playwright.sync_api import BrowserContext


pytestmark = [pytest.mark.gp_practices_assigned_to_bso, pytest.mark.uiapi]

API_URL = "/bss/assignedGpPractice/search"


def test_gp_practices_assigned_to_bso_search_all(
    api_bso_user_session: BrowserContext,
) -> None:
    """
    API test to check search on all GP Practices
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSortDirectionWithOrder[0lastUpdatedOn]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 10
    assert response_data["results"][0]["code"] == "A12345"


def test_invalid_national_user(api_national_user_session: BrowserContext) -> None:
    """
    API test to check an invaild user (National user) doesn't have access to the GP Practices Assigned to BSO, so returns a 403 error.
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSortDirectionWithOrder[0lastUpdatedOn]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_national_user_session, API_URL).get_request(
        data, False
    )
    assert response_data == 403


def test_invalid_helpdesk_user(api_helpdesk_session: BrowserContext) -> None:
    """
    API test to check an invaild user (Helpdesk user) doesn't have access to the GP Practices Assigned to BSO, so returns a 403 error.
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSortDirectionWithOrder[0lastUpdatedOn]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_helpdesk_session, API_URL).get_request(data, False)
    assert response_data == 403


def test_gp_practices_assigned_to_bso_search_practice(
    api_bso_user_session: BrowserContext,
) -> None:
    """
    API test to check search on a specific GP Practice
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[code]": "EX0007",
        "columnSortDirectionWithOrder[0lastUpdatedOn]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 1
    assert response_data["results"][0]["code"] == "EX0007"


def test_gp_practices_assigned_to_bso_search_name(
    api_bso_user_session: BrowserContext,
) -> None:
    """
    API test to check search on GP Practice Name containing "Gold"
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[name]": "Gold",
        "columnSortDirectionWithOrder[0lastUpdatedOn]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 1
    for name in response_data["results"]:
        assert str(name["name"]).startswith("Gold")
