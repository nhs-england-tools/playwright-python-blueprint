"""
SSPI Update Warnings Information report Tests: These tests cover the SSPI Update Warnings Information report, accessed from the Monitoring Reports tab.
"""

import pytest
from utils.api_utils import ApiUtils
from playwright.sync_api import BrowserContext


pytestmark = [pytest.mark.sspi_information, pytest.mark.uiapi]

API_URL = "/bss/report/sspiUpdateWarnings/information/search"


def test_sspi_information_default(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on all entries on the SSPI Update Warnings Information report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[actioned]": "NOT_ACTIONED",
        "columnSortDirectionWithOrder[0receivedDateTime]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 2
    for name in response_data["results"]:
        assert name["bsoCode"] == "BS1"


def test_invalid_national_user(api_national_user_session: BrowserContext) -> None:
    """
    API test to check an invaild user (National user) doesn't have access to the SSPI Information Warnings Action report, so returns a 403 error.
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[actioned]": "NOT_ACTIONED",
        "columnSortDirectionWithOrder[0receivedDateTime]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_national_user_session, API_URL).get_request(
        data, False
    )
    assert response_data == 403


def test_invalid_helpdesk_user(api_helpdesk_session: BrowserContext) -> None:
    """
    API test to check an invaild user (Helpdesk user) doesn't have access to the SSPI Update Warnings Information report, so returns a 403 error.
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[actioned]": "NOT_ACTIONED",
        "columnSortDirectionWithOrder[0receivedDateTime]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_helpdesk_session, API_URL).get_request(data, False)
    assert response_data == 403


def test_sspi_information_all(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on All entries on the SSPI Update Warnings Information report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSortDirectionWithOrder[0receivedDateTime]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 4
    for name in response_data["results"]:
        assert name["bsoCode"] == "BS1"


def test_sspi_information_nhs_number(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on NHS Number on the SSPI Update Warnings Information report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[actioned]": "NOT_ACTIONED",
        "columnSearchText[nhsNumber]": "930 000 0020",
        "columnSortDirectionWithOrder[0receivedDateTime]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 1
    for nhs in response_data["results"]:
        assert len(nhs["nhsNumber"]) == 10


def test_sspi_information_first_given_name(
    api_bso_user_session: BrowserContext,
) -> None:
    """
    API test to check search on First Given Name "Priscilla" entries on the SSPI Update Warnings Information report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[actioned]": "NOT_ACTIONED",
        "columnSearchText[firstNames]": "priscilla",
        "columnSortDirectionWithOrder[0receivedDateTime]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 1
    for name in response_data["results"]:
        assert str(name["firstNames"]).startswith("Priscilla")


def test_sspi_information_family_name(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on Family Name "Jones" entries on the SSPI Update Warnings Information report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[actioned]": "NOT_ACTIONED",
        "columnSearchText[familyName]": "jones",
        "columnSortDirectionWithOrder[0receivedDateTime]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 1
    for name in response_data["results"]:
        assert str(name["familyName"]).startswith("JONES")


def test_sspi_information_age_today(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on Age Today "Under 80" entries on the SSPI Update Warnings Information report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[actioned]": "NOT_ACTIONED",
        "columnSearchText[ageInYears]": "under80",
        "columnSortDirectionWithOrder[0receivedDateTime]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 2
    for age in response_data["results"]:
        assert age["bsoCode"] == "BS1"


def test_sspi_information_event(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on Event entries on the SSPI Update Warnings Information report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[actioned]": "NOT_ACTIONED",
        "columnSearchText[event]": "REMOVAL",
        "columnSortDirectionWithOrder[0nhsNumber]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 1
    for event in response_data["results"]:
        assert event["event"]["description"] == "Removal"


def test_sspi_information_warning(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on Warning entries on the SSPI Update Warnings Information report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[actioned]": "NOT_ACTIONED",
        "columnSearchText[reason]": "NO_OPEN_EPISODES",
        "columnSortDirectionWithOrder[0receivedDateTime]": "desc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 1
    for warning in response_data["results"]:
        assert warning["reason"]["description"] == "No open episodes"
