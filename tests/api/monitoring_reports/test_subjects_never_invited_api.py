"""
Subjects Never Invited for Screening report Tests: These tests cover the Subjects Never Invited for Screening report, accessed from the Monitoring Reports tab.
"""

import pytest
from utils.api_utils import ApiUtils
from playwright.sync_api import BrowserContext


pytestmark = [pytest.mark.subjects_never_invited, pytest.mark.uiapi]

API_URL = "/bss/report/subjectsNeverInvited/search"


def test_subjects_never_invited_default(api_bso_user_session: BrowserContext) -> None:
    """
    API test to check search on all entries on the Subjects Never Invited for Screening report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSortDirectionWithOrder[0dateOfBirth]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 5
    for code in response_data["results"]:
        assert code["bso"]["code"] == "BS1"


def test_invalid_national_user(api_national_user_session: BrowserContext) -> None:
    """
    API test to check an invaild user (National user) doesn't have access to the Subjects Never Invited for Screening report, so returns a 403 error.
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSortDirectionWithOrder[0dateOfBirth]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_national_user_session, API_URL).get_request(
        data, False
    )
    assert response_data == 403


def test_invalid_helpdesk_user(api_helpdesk_session: BrowserContext) -> None:
    """
    API test to check an invaild user (Helpdesk user) doesn't have access to the Subjects Never Invited for Screening report, so returns a 403 error.
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


def test_subjects_never_invited_nhs_number(
    api_bso_user_session: BrowserContext,
) -> None:
    """
    API test to check search on NHS Number on the Subjects Never Invited for Screening report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[nhsNumber]": "930 000 0022",
        "columnSortDirectionWithOrder[0dateOfBirth]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 1
    for nhs in response_data["results"]:
        assert len(nhs["nhsNumber"]) == 10


def test_subjects_never_invited_family_name(
    api_bso_user_session: BrowserContext,
) -> None:
    """
    API test to check search on Family Name on the Subjects Never Invited for Screening report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[familyName]": "AFAKENAME",
        "columnSortDirectionWithOrder[0dateOfBirth]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 1
    for name in response_data["results"]:
        assert str(name["familyName"]).startswith("AFAKENAME")


def test_subjects_never_invited_first_given_name(
    api_bso_user_session: BrowserContext,
) -> None:
    """
    API test to check search on First Given Name "Judy" on the Subjects Never Invited for Screening report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[firstNames]": "Judy",
        "columnSortDirectionWithOrder[0dateOfBirth]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 1
    for name in response_data["results"]:
        assert str(name["firstNames"]).startswith("Judy")


def test_subjects_never_invited_first_given_names(
    api_bso_user_session: BrowserContext,
) -> None:
    """
    API test to check search on First Given Name "Jen" on the Subjects Never Invited for Screening report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[firstNames]": "Jen",
        "columnSortDirectionWithOrder[0dateOfBirth]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 2
    for name in response_data["results"]:
        assert str(name["firstNames"]).startswith("Jen")


def test_subjects_never_invited_gp_practice_code(
    api_bso_user_session: BrowserContext,
) -> None:
    """
    API test to check search on GP Practice Code "GP4" on the Subjects Never Invited for Screening report
    """
    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "searchText": "",
        "columnSearchText[gpPracticeSummary.code]": "gp4",
        "columnSortDirectionWithOrder[0dateOfBirth]": "asc",
        "searchSpecification": "",
    }
    response_data = ApiUtils(api_bso_user_session, API_URL).get_request(data)
    assert response_data["draw"] == 1
    assert len(response_data["results"]) == 4
    for name in response_data["results"]:
        assert str(name["gpPracticeSummary"]["code"]).startswith("GP4")
