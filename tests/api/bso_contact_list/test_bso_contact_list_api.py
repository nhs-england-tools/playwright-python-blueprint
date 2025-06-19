"""
BSO Contact List Tests: These tests cover the BSO Contact List, accessed from the BSO Contact List tab.
"""

import pytest
from utils.api_utils import ApiUtils
from playwright.sync_api import BrowserContext


pytestmark = [pytest.mark.bso_contact_list, pytest.mark.uiapi]

API_URL = "/bss/bso/search"


def test_bso_search_all(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on all BSO's
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSortDirectionWithOrder[0code]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 10
    for bso in response_data["results"]:
        assert len(bso["code"]) == 3


def test_bso_search_national_all(api_national_user_session: BrowserContext) -> None:
    """
    API test to check search on all BSO's
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSortDirectionWithOrder[0code]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_national_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 10
    for bso in response_data["results"]:
        assert len(bso["code"]) == 3


def test_invalid_user(api_helpdesk_session: BrowserContext) -> None:
    """
    API test to check an invaild user doesn't have access to the BSO Contact List, so returns a 403 error.
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[code]": "BS1",
        "columnSortDirectionWithOrder[0code]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_helpdesk_session, API_URL).get_request(data, False)
    assert response_data == 403


def test_bso_search_bso(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on BSO AGA
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[code]": "AGA",
        "columnSortDirectionWithOrder[0code]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 1
    for bso in response_data["results"]:
        assert bso["code"] == "AGA"


def test_bso_search_bso_name(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on BSO Name containing "BSO"
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "2",
        "searchText": "",
        "columnSearchText[name]": "BSO",
        "columnSortDirectionWithOrder[0code]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 2
    for name in response_data["results"]:
        assert str(name["name"]).startswith("BSO")


def test_bso_search_sqas_region_north(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on SQAS Region "North"
    """
    data = {
        "draw": "5",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[bsoRegionName]": "NORTH",
        "columnSortDirectionWithOrder[0code]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 5
    assert len(response_data["results"]) == 10
    assert response_data["results"][0]["code"] == "BYO"


def test_bso_search_sqas_region_south(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on SQAS Region "South"
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[bsoRegionName]": "SOUTH",
        "columnSortDirectionWithOrder[0code]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 10
    assert response_data["results"][0]["code"] == "BS2"


def test_bso_search_status_active(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on Status "Active"
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[active]": "true",
        "columnSortDirectionWithOrder[0code]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 2
    assert response_data["results"][0]["code"] == "BS1"


def test_bso_search_status_inactive(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on Status "Inactive"
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[active]": "false",
        "columnSortDirectionWithOrder[0code]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 10
    assert response_data["results"][0]["code"] == "AGA"
