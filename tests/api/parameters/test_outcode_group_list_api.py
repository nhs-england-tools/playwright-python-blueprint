"""
Outcode Group List Tests: These tests cover the Outcode Group List, accessed from the Parameters tab.
"""

import pytest
from utils.api_utils import ApiUtils
from playwright.sync_api import BrowserContext


pytestmark = [pytest.mark.outcode_group_list, pytest.mark.uiapi]

API_URL = "/bss/outcodeGroup/search"


def test_outcode_group_list_search_all(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on all Outcode Group List
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[active]": "true",
        "columnSortDirectionWithOrder[0active]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 9
    for name in response_data["results"]:
        assert name["bsoCode"] == "BS1"


def test_invalid_national_user(api_national_user_session: BrowserContext) -> None:
    """
    API test to check an invaild user (National user) doesn't have access to the Outcode Group List, so returns a 403 error.
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[active]": "true",
        "columnSortDirectionWithOrder[0active]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_national_user_session, API_URL).get_request(
        data, False
    )
    assert response_data == 403


def test_invalid_helpdesk_user(api_helpdesk_session: BrowserContext) -> None:
    """
    API test to check an invaild user (Helpdesk user) doesn't have access to the Outcode Group List, so returns a 403 error.
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[active]": "true",
        "columnSortDirectionWithOrder[0active]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_helpdesk_session, API_URL).get_request(data, False)
    assert response_data == 403


def test_outcode_group_list_search_zone(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on "Zone" in the Outcode Group List
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[groupName]": "zone",
        "columnSortDirectionWithOrder[0active]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 3
    for name in response_data["results"]:
        assert str(name["groupName"]).startswith("ZONE")


def test_outcode_group_status_all(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on Status "All"
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[active]": "true",
        "columnSortDirectionWithOrder[0active]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 9
    for name in response_data["results"]:
        assert name["bsoCode"] == "BS1"
