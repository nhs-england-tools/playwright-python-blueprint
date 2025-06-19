"""
GP Practice List Tests: These tests cover the GP Practice List, accessed from the BSO Mapping tab.
"""

import pytest
from utils.api_utils import ApiUtils
from playwright.sync_api import BrowserContext


pytestmark = [pytest.mark.gp_practice_list, pytest.mark.uiapi]

API_URL = "/bss/gpPractice/search"


def test_gp_practice_search_BS1(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on BSO Code BS1
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[bso.code]": "BS1",
        "columnSortDirectionWithOrder[0bso.code]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 10
    for bso in response_data["results"]:
        assert bso["bso"]["code"] == "BS1"


def test_gp_practice_search_national_BS1(
    api_national_user_session: BrowserContext,
) -> None:
    """
    API test logged in as a National user to check search on BSO Code BS1
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[bso.code]": "BS1",
        "columnSortDirectionWithOrder[0bso.code]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_national_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 10
    for bso in response_data["results"]:
        assert bso["bso"]["code"] == "BS1"


def test_invalid_user(api_helpdesk_session: BrowserContext) -> None:
    """
    API test to check an invaild user (Helpdesk user) doesn't have access to the GP Practice List, so returns a 403 error.
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[bso.code]": "BS1",
        "columnSortDirectionWithOrder[0bso.code]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_helpdesk_session, API_URL).get_request(data, False)
    assert response_data == 403


def test_gp_practice_search_A12345(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on GP Practice A12345
    """
    data = {
        "draw": "2",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[bso.code]": "BS1",
        "columnSearchText[code]": "A12345",
        "columnSearchText[name]": "MEGA",
        "columnSortDirectionWithOrder[0bso.code]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 2
    assert len(response_data["results"]) == 1
    assert response_data["results"][0]["bso"]["code"] == "BS1"
    assert response_data["results"][0]["name"] == "Mega Practice"
    assert response_data["results"][0]["code"] == "A12345"


def test_gp_practice_search_A82(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check GP Practice search on A82
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "3",
        "searchText": "",
        "columnSearchText[code]": "A82",
        "columnSortDirectionWithOrder[0bso.code]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 3
    for practice in response_data["results"]:
        assert str(practice["code"]).startswith("A82")


def test_gp_practice_search_included_in_group_yes(
    api_bso_user_session: BrowserContext,
) -> None:
    """
    API test to check search on Included in Group status is "Yes"
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[bso.code]": "BS1",
        "columnSearchText[includedInGroup]": "YES",
        "columnSortDirectionWithOrder[0bso.code]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 10
    assert response_data["results"][0]["bso"]["code"] == "BS1"


def test_gp_practice_search_included_in_group_no(
    api_bso_user_session: BrowserContext,
) -> None:
    """
    API test to check search on Included in Group status is "No"
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[bso.code]": "BS1",
        "columnSearchText[includedInGroup]": "NO",
        "columnSortDirectionWithOrder[0bso.code]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 7
    assert response_data["results"][0]["bso"]["code"] == "BS1"
