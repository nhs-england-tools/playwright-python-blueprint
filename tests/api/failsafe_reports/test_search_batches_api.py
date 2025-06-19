"""
Search Batches Tests: These tests cover the Search Batches, accessed from the Failsafe Reports tab.
"""

import pytest
from utils.api_utils import ApiUtils
from playwright.sync_api import BrowserContext


pytestmark = [pytest.mark.search_batches, pytest.mark.uiapi]

API_URL = "/bss/selectedBatch/search"


def test_invalid_national_user(api_national_user_session: BrowserContext) -> None:
    """
    API test to check an invaild user (National user) doesn't have access to the Search Batches, so returns a 403 error.
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSortDirectionWithOrder[0selectDateTime]": "desc",
        "searchSpecification[gpPracticeCode]": "",
        "searchSpecification[gpPracticeGroupName]": "",
        "searchSpecification[outcode]": "",
        "searchSpecification[outcodeGroupName]": "",
        "searchSpecification[startDate]": "25-Jul-2016",
        "searchSpecification[endDate]": "27-May-2025",
    }
    response_data = ApiUtils(api_national_user_session, API_URL).get_request(
        data, False
    )
    assert response_data == 403


def test_invalid_helpdesk_user(api_helpdesk_session: BrowserContext) -> None:
    """
    API test to check an invaild user (Helpdesk user) doesn't have access to the Search Batches, so returns a 403 error.
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSortDirectionWithOrder[0selectDateTime]": "desc",
        "searchSpecification[gpPracticeCode]": "",
        "searchSpecification[gpPracticeGroupName]": "",
        "searchSpecification[outcode]": "",
        "searchSpecification[outcodeGroupName]": "",
        "searchSpecification[startDate]": "25-Jul-2016",
        "searchSpecification[endDate]": "27-May-2025",
    }
    response_data = ApiUtils(api_helpdesk_session, API_URL).get_request(data, False)
    assert response_data == 403


def test_search_batches_all(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on All entries on Search Batches
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSortDirectionWithOrder[0selectDateTime]": "desc",
        "searchSpecification[gpPracticeCode]": "",
        "searchSpecification[gpPracticeGroupName]": "",
        "searchSpecification[outcode]": "",
        "searchSpecification[outcodeGroupName]": "",
        "searchSpecification[startDate]": "25-Jul-2016",
        "searchSpecification[endDate]": "27-May-2025",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 5
    for name in response_data["results"]:
        assert name["bsoCode"] == "BS1"
