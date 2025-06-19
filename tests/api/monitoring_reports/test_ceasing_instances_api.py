"""
Ceasing Instances with No Documentation report Tests: These tests cover the Ceasing Instances with No Documentation report, accessed from the Monitoring Reports tab.
"""

import pytest
from utils.api_utils import ApiUtils
from playwright.sync_api import BrowserContext


pytestmark = [pytest.mark.ceasing_instances, pytest.mark.uiapi]

API_URL = "/bss/report/outstandingCeasingDocumentation/search"


def test_ceasing_instances_current(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on current entries on the Ceasing Instances with No Documentation report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[subject.ageInYears]": "73",
        "columnSearchText[dateTimeOfUnceasing]": "open",
        "columnSortDirectionWithOrder[0dateTimeOfCeasing]": "asc",
        "columnSortDirectionWithOrder[1subject.nhsNumber]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 3
    for code in response_data["results"]:
        assert code["subject"]["bso"]["code"] == "BS1"


def test_ceasing_instances_all(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on all entries on the Ceasing Instances with No Documentation report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[subject.ageInYears]": "73",
        "columnSortDirectionWithOrder[0dateTimeOfCeasing]": "asc",
        "columnSortDirectionWithOrder[1subject.nhsNumber]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 5
    for code in response_data["results"]:
        assert code["subject"]["bso"]["code"] == "BS1"


def test_ceasing_instances_historic(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on all entries on the Ceasing Instances with No Documentation report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[subject.ageInYears]": "73",
        "columnSearchText[dateTimeOfUnceasing]": "closed",
        "columnSortDirectionWithOrder[0dateTimeOfCeasing]": "asc",
        "columnSortDirectionWithOrder[1subject.nhsNumber]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 2
    for code in response_data["results"]:
        assert code["subject"]["bso"]["code"] == "BS1"


def test_invalid_national_user(api_national_user_session: BrowserContext) -> None:
    """
    API test to check an invaild user (National user) doesn't have access to the Ceasing Instances with No Documentation report, so returns a 403 error.
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[subject.ageInYears]": "73",
        "columnSearchText[dateTimeOfUnceasing]": "open",
        "columnSortDirectionWithOrder[0dateTimeOfCeasing]": "asc",
        "columnSortDirectionWithOrder[1subject.nhsNumber]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_national_user_session, API_URL).get_request(
        data, False
    )
    assert response_data == 403


def test_invalid_helpdesk_user(api_helpdesk_session: BrowserContext) -> None:
    """
    API test to check an invaild user (Helpdesk user) doesn't have access to the Ceasing Instances with No Documentation report, so returns a 403 error.
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[subject.ageInYears]": "73",
        "columnSearchText[dateTimeOfUnceasing]": "open",
        "columnSortDirectionWithOrder[0dateTimeOfCeasing]": "asc",
        "columnSortDirectionWithOrder[1subject.nhsNumber]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_helpdesk_session, API_URL).get_request(data, False)
    assert response_data == 403


def test_ceasing_instances_nhs_number(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on NHS Number on the Ceasing Instances with No Documentation report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[subject.nhsNumber]": "930 000 0015",
        "columnSearchText[subject.ageInYears]": "73",
        "columnSearchText[dateTimeOfUnceasing]": "open",
        "columnSortDirectionWithOrder[0dateTimeOfCeasing]": "asc",
        "columnSortDirectionWithOrder[1subject.nhsNumber]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 1
    for nhs in response_data["results"]:
        assert len(nhs["subject"]["nhsNumber"]) == 10


def test_ceasing_instances_family_name(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on Family Name on the Ceasing Instances with No Documentation report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[subject.ageInYears]": "73",
        "columnSearchText[subject.familyName]": "PERFORMANCE",
        "columnSearchText[dateTimeOfUnceasing]": "open",
        "columnSortDirectionWithOrder[0dateTimeOfCeasing]": "asc",
        "columnSortDirectionWithOrder[1subject.nhsNumber]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 2
    for name in response_data["results"]:
        assert str(name["subject"]["familyName"]).startswith("PERFORMANCE")


def test_ceasing_instances_first_given_name(
    api_bso_user_session: BrowserContext,
) -> None:
    """
    API test to check search on First Given Name "India" on the Ceasing Instances with No Documentation report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[subject.ageInYears]": "73",
        "columnSearchText[subject.firstNames]": "India",
        "columnSearchText[dateTimeOfUnceasing]": "open",
        "columnSortDirectionWithOrder[0dateTimeOfCeasing]": "asc",
        "columnSortDirectionWithOrder[1subject.nhsNumber]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 2
    for name in response_data["results"]:
        assert str(name["subject"]["firstNames"]).startswith("India")
