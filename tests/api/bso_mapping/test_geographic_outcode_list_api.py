"""
Geographic Outcode List Tests: These tests cover the Geographic Outcode List, accessed from the BSO Mapping tab.
"""

import pytest
from utils.api_utils import ApiUtils
from playwright.sync_api import BrowserContext


pytestmark = [pytest.mark.geographic_outcode_list, pytest.mark.uiapi]

API_URL = "/bss/outcode/search"


def test_geo_outcode_search_all(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on all BSO's
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSortDirectionWithOrder[0bso.code]": "asc",
        "columnSortDirectionWithOrder[1outcode]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 10
    for bso in response_data["results"]:
        assert len(bso["bso"]["code"]) == 3


def test_geo_outcode_search_national_all(
    api_national_user_session: BrowserContext,
) -> None:
    """
    API test logged in as a National user to check search on all BSO's
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSortDirectionWithOrder[0bso.code]": "asc",
        "columnSortDirectionWithOrder[1outcode]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_national_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 10
    for bso in response_data["results"]:
        assert len(bso["bso"]["code"]) == 3


def test_invalid_helpdesk_user(api_helpdesk_session: BrowserContext) -> None:
    """
    API test to check an invaild user (Helpdesk user) doesn't have access to the Geographic Outcode List, so returns a 403 error.
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSortDirectionWithOrder[0bso.code]": "asc",
        "columnSortDirectionWithOrder[1outcode]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_helpdesk_session, API_URL).get_request(data, False)
    assert response_data == 403


def test_geo_outcode_search_bso(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on BSO AGA
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[bso.code]": "aga",
        "columnSortDirectionWithOrder[0bso.code]": "asc",
        "columnSortDirectionWithOrder[1outcode]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 1
    for bso in response_data["results"]:
        assert bso["bso"]["code"] == "AGA"


def test_geo_outcode_search_bso_name(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on BSO Name
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[bso.name]": "New",
        "columnSortDirectionWithOrder[0bso.code]": "asc",
        "columnSortDirectionWithOrder[1outcode]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 1
    for name in response_data["results"]:
        assert str(name["bso"]["name"]).startswith("New")


def test_geo_outcode_search_bso_outcode(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on Outcode "EX4"
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[outcode]": "EX4",
        "columnSortDirectionWithOrder[0bso.code]": "asc",
        "columnSortDirectionWithOrder[1outcode]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 1
    for outcode in response_data["results"]:
        assert outcode["outcode"] == "EX4"
