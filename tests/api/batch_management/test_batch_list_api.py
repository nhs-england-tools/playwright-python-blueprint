"""
Batch List Tests: These tests cover the Batch List, accessed from the Batch Management tab.
"""

import pytest
from utils.api_utils import ApiUtils
from playwright.sync_api import BrowserContext


pytestmark = [pytest.mark.batch_list, pytest.mark.uiapi]

API_URL = "/bss/batch/search"


def test_batch_list_search_all(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search Batch List on all batches
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSortDirectionWithOrder[0countDateTime]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 10
    for batch in response_data["results"]:
        # Have to exclude RISP due to test data showing "RISP1" etc
        if batch["description"] != "RISP":
            assert len(batch["bsoBatchId"]) == 10
            assert batch["bsoCode"] == batch["bsoBatchId"][:3]


def test_bso_search_national_all(api_national_user_session: BrowserContext) -> None:
    """
    API test to check search Batch List on all BSO's
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[batchType]": "RISP_AGEX",
        "columnSortDirectionWithOrder[0countDateTime]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_national_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 2
    for batch in response_data["results"]:
        if batch["description"] == "RISP_AGEX":
            assert len(batch["bsoBatchId"]) == 10
            assert batch["bsoCode"] == batch["bsoBatchId"][:3]


def test_invalid_helpdesk_user(api_helpdesk_session: BrowserContext) -> None:
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


def test_batch_list_search_batch_type_risp_agex(
    api_bso_user_session: BrowserContext,
) -> None:
    """
    API test to check search Batch Type on all RISP_AGEX batches
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[batchType]": "RISP_AGEX",
        "columnSortDirectionWithOrder[0countDateTime]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 10
    for batch in response_data["results"]:
        if batch["description"] == "RISP_AGEX":
            assert len(batch["bsoBatchId"]) == 10
            assert batch["bsoCode"] == batch["bsoBatchId"][:3]


def test_batch_list_search_batch_type_ntdd(
    api_bso_user_session: BrowserContext,
) -> None:
    """
    API test to check search Batch Type on all NTDD batches
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[batchType]": "NTDD",
        "columnSortDirectionWithOrder[0countDateTime]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 10
    for batch in response_data["results"]:
        if batch["description"] == "NTDD":
            assert len(batch["bsoBatchId"]) == 10
            assert batch["bsoCode"] == batch["bsoBatchId"][:3]


def test_batch_list_search_batch_type_routine_failsafe(
    api_bso_user_session: BrowserContext,
) -> None:
    """
    API test to check search Batch Type on all NTDD batches
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[batchType]": "FS",
        "columnSortDirectionWithOrder[0countDateTime]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 10
    for batch in response_data["results"]:
        if batch["description"] == "FS":
            assert len(batch["bsoBatchId"]) == 10
            assert batch["bsoCode"] == batch["bsoBatchId"][:3]


def test_batch_list_search_failsafe_flag(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search Failsafe Flag on all batches
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[includeYoungerSubjects]": "NO",
        "columnSortDirectionWithOrder[0countDateTime]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 10
    for batch in response_data["results"]:
        # Have to exclude RISP due to test data showing "RISP1" etc
        if batch["description"] != "RISP":
            assert len(batch["bsoBatchId"]) == 10
            assert batch["bsoCode"] == batch["bsoBatchId"][:3]


def test_batch_list_search_batch_title(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search Batch Title for "Perform" on all batches
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[title]": "Perform",
        "columnSortDirectionWithOrder[0countDateTime]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 10
    for batch in response_data["results"]:
        assert str(batch["title"]).startswith("Perform")
