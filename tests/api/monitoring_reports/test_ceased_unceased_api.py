"""
Ceased/Unceased Subjects report Tests: These tests cover the Ceased/Unceased Subjects report, accessed from the Monitoring Reports tab.
"""

import pytest
from utils.api_utils import ApiUtils
from playwright.sync_api import BrowserContext


pytestmark = [pytest.mark.ceased_unceased, pytest.mark.uiapi]

API_URL = "/bss/report/ceasing/search"


def test_ceased_unceased_default(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on all entries on the Ceased/Unceased Subjects report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[actioned]": "NOT_ACTIONED",
        "searchSpecification[searchFor]": "CEASED",
        "searchSpecification[startDate]": "",
        "searchSpecification[endDate]": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 0
    for code in response_data["results"]:
        assert code["bso"]["code"] == "BS1"


def test_invalid_national_user(api_national_user_session: BrowserContext) -> None:
    """
    API test to check an invaild user (National user) doesn't have access to the Ceased/Unceased Subjects report, so returns a 403 error.
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[actioned]": "NOT_ACTIONED",
        "searchSpecification[searchFor]": "CEASED",
        "searchSpecification[startDate]": "",
        "searchSpecification[endDate]": "",
    }
    response_data = ApiUtils(api_national_user_session, API_URL).get_request(
        data, False
    )
    assert response_data == 403


def test_invalid_helpdesk_user(api_helpdesk_session: BrowserContext) -> None:
    """
    API test to check an invaild user (Helpdesk user) doesn't have access to the Ceased/Unceased Subjects report, so returns a 403 error.
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[actioned]": "NOT_ACTIONED",
        "searchSpecification[searchFor]": "CEASED",
        "searchSpecification[startDate]": "",
        "searchSpecification[endDate]": "",
    }
    response_data = ApiUtils(api_helpdesk_session, API_URL).get_request(data, False)
    assert response_data == 403


def test_ceased_unceased_both(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on Both selected on the Ceased/Unceased Subjects report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[actioned]": "NOT_ACTIONED",
        "searchSpecification[searchFor]": "BOTH",
        "searchSpecification[startDate]": "",
        "searchSpecification[endDate]": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 1
    for code in response_data["results"]:
        assert code["subject"]["bso"]["code"] == "BS1"
