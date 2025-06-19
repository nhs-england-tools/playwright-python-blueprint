"""
Subject Search Tests: These tests cover the Subject Search, accessed from the Subject Search tab.
"""

import pytest
from utils.api_utils import ApiUtils
from playwright.sync_api import BrowserContext


pytestmark = [pytest.mark.subject_search, pytest.mark.uiapi]

API_URL = "/bss/subject/search"


@pytest.mark.only
def test_subject_search_all(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check Subject Search
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "50",
        "searchText": "",
        "columnSearchText[familyName]": "performance",
        "columnSearchText[bso.code]": "BS1",
        "columnSortDirectionWithOrder[0familyName]": "asc",
        "columnSortDirectionWithOrder[1firstNames]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 16
    for bso in response_data["results"]:
        assert len(bso["code"]) == 3
