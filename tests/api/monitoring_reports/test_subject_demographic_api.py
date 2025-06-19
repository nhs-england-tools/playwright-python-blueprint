"""
Pending Subject Demographic Changes List report Tests: These tests cover the Pending Subject Demographic Changes List report, accessed from the Monitoring Reports tab.
"""

import pytest
from utils.api_utils import ApiUtils
from playwright.sync_api import BrowserContext


pytestmark = [pytest.mark.subject_demographic, pytest.mark.uiapi]

API_URL = "/bss/report/pendingDemographicChanges/search"


def test_subject_demographic_default(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on all entries on the Pending Subject Demographic Changes List report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSortDirectionWithOrder[0changeReceivedDateTime]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 4
    for nhs in response_data["results"]:
        assert len(nhs["subject"]["nhsNumber"]) == 10


def test_invalid_national_user(api_national_user_session: BrowserContext) -> None:
    """
    API test to check an invaild user (National user) doesn't have access to the Pending Subject Demographic Changes List report, so returns a 403 error.
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSortDirectionWithOrder[0changeReceivedDateTime]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_national_user_session, API_URL).get_request(
        data, False
    )
    assert response_data == 403


def test_invalid_helpdesk_user(api_helpdesk_session: BrowserContext) -> None:
    """
    API test to check an invaild user (Helpdesk user) doesn't have access to thePending Subject Demographic Changes List report, so returns a 403 error.
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSortDirectionWithOrder[0dateOfBirth]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_helpdesk_session, API_URL).get_request(data, False)
    assert response_data == 403


def test_subject_demographic_nhs_number(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on NHS Number on the Pending Subject Demographic Changes List report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[subject.nhsNumber]": "930 000 0002",
        "columnSortDirectionWithOrder[0changeReceivedDateTime]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 1
    for nhs in response_data["results"]:
        assert len(nhs["subject"]["nhsNumber"]) == 10


def test_subject_demographic_family_name(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on Family Name on the Pending Subject Demographic Changes List report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[subject.familyName]": "performance",
        "columnSortDirectionWithOrder[0changeReceivedDateTime]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 2
    for name in response_data["results"]:
        assert str(name["subject"]["familyName"]).startswith("PERFORMANCE")


def test_subjects_never_invited_first_given_name(
    api_bso_user_session: BrowserContext,
) -> None:
    """
    API test to check search on First Given Name "Audrey" on the Pending Subject Demographic Changes List report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[subject.firstNames]": "Audrey",
        "columnSortDirectionWithOrder[0changeReceivedDateTime]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 1
    for name in response_data["results"]:
        assert str(name["subject"]["firstNames"]).startswith("Audrey")
