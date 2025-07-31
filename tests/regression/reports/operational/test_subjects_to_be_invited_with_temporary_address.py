import logging
import pytest
from playwright.sync_api import Page, expect
from utils.user_tools import UserTools
from classes.user import User
from classes.subject import Subject
from pages.base_page import BasePage
from pages.reports.operational.subjects_to_be_invited_with_temporary_address_page import (
    SubjectsToBeInvitedWithTemporaryAddressPage
)
from pages.reports.reports_page import ReportsPage
from pages.screening_subject_search.subject_demographic_page import (
    SubjectDemographicPage,
)
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from utils.oracle.oracle import OracleDB
from utils.oracle.subject_selection_query_builder import SubjectSelectionQueryBuilder
from utils.screening_subject_page_searcher import search_subject_episode_by_nhs_number
from datetime import datetime, timedelta


@pytest.mark.regression
@pytest.mark.reports_operational
def test_subject_not_on_report_if_not_due(page: Page) -> None:
    """
    Test to check that a subject who is not due for invite is not in the report.
    """
    logging.info(
        "Starting test: Test to check that a subject who is not due for invite is not in the report."
    )

    criteria1 = {
        "subject has temporary address": "current",
        "subject hub code": "BCS01",
        "subject is due for invite": "no"
    }

    nhs_no = _db_search(criteria1)

    UserTools.user_login(page, "Hub Manager at BCS01")
    _go_to_report_page(page)

    report = SubjectsToBeInvitedWithTemporaryAddressPage(page)
    report.filter_by_nhs_number(nhs_no)
    report.assertRecordsVisible(nhs_no, False)

@pytest.mark.wip
@pytest.mark.regression
@pytest.mark.reports_operational
def test_subject_to_be_invited_without_temporary_address_at_this_hub_not_on_report(page: Page) -> None:
    """
    Test to check that a subject who is due to be invited, but does not have a temporary address, and is at this hub, does not appear in the report.
    """
    logging.info(
        "Starting test: Check that a subject who is due to be invited, but does not have a temporary address, and is at this hub, does not appear in the report."
    )

    criteria = {
        "subject has temporary address": "No",
        "subject hub code": "BCS01",
        "subject is due for invite": "yes"
    }

    nhs_no = _db_search(criteria)

    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    BasePage(page).click_main_menu_link()
    _go_to_report_page(page)

    report = SubjectsToBeInvitedWithTemporaryAddressPage(page)
    report.filter_by_nhs_number(nhs_no)
    report.assertRecordsVisible(nhs_no, False)
    report.filter_by_nhs_number("")

    BasePage(page).click_main_menu_link()
    _go_to_demographics_page_for_subject_from_menu(page, nhs_no)
    _add_a_temp_address(page)

    BasePage(page).click_main_menu_link()
    _go_to_report_page(page)

    report.filter_by_nhs_number(nhs_no)
    report.assertRecordsVisible(nhs_no, True)


@pytest.mark.regression
@pytest.mark.reports_operational
def test_subject_to_be_invited_with_temporary_address_at_another_hub_not_on_report(page: Page) -> None:
    """
    Test to check that a subject who is due to be invited, and does have a temporary address but is at another hub, does not appear in the report.
    """
    logging.info(
        "Starting test: Check that a subject who is due to be invited, and does have a temporary address but is at another hub, does not appear in the report."
    )

    criteria = {
        "subject has temporary address": "No",
        "subject hub code": "BCS01",
        "subject is due for invite": "yes"
    }

    nhs_no = _db_search(criteria)

    UserTools.user_login(page, "Hub Manager at BCS02")

    BasePage(page).click_main_menu_link()
    _go_to_report_page(page)

    report = SubjectsToBeInvitedWithTemporaryAddressPage(page)
    report.filter_by_nhs_number(nhs_no)
    report.assertRecordsVisible(nhs_no, False)


@pytest.mark.regression
@pytest.mark.reports_operational
def test_subject_on_report_is_hidden_after_review(page: Page) -> None:
    """
    Test to check that a subject who becomes reviewed is then hidden from the default view in the report.
    """
    logging.info(
        "Starting test: Check that a subject who becomes reviewed is then hidden from the default view in the report."
    )

    criteria = {
        "subject has temporary address": "Current",
        "subject hub code": "BCS01",
        "subject is due for invite": "yes"
    }

    nhs_no = _db_search(criteria)

    UserTools.user_login(page, "Hub Manager State Registered at BCS01")
    _go_to_report_page(page)

    report = SubjectsToBeInvitedWithTemporaryAddressPage(page)

    logging.info("Limit report to show just our subject, make sure starting state is not-reviewed")
    report.filterByReviewed("All")
    report.filter_by_nhs_number(nhs_no)
    report.assertRecordsVisible(nhs_no, True)
    report.reviewSubject(nhs_no, False)

    logging.info("Only show Non-reviewed, review the subject, watch subject disappear")
    report.filterByReviewed("No")
    report.reviewSubject(nhs_no, True)
    report.assertRecordsVisible(nhs_no, False)

    logging.info("Only show Reviewed, watch subject appear")
    report.filterByReviewed("Yes")
    report.assertRecordsVisible(nhs_no, True)

    report.filterByReviewed("All")
    report.assertRecordsVisible(nhs_no, True)

    logging.info("Only show Reviewed, un-review the subject, watch subject disappear")
    report.filterByReviewed("Yes")
    report.reviewSubject(nhs_no, False)
    report.assertRecordsVisible(nhs_no, False)

    logging.info("Only show Non-reviewed, watch subject appear")
    report.filterByReviewed("No")
    report.assertRecordsVisible(nhs_no, True)


@pytest.mark.regression
@pytest.mark.reports_operational
def test_subject_to_be_invited_with_temporary_address_at_this_hub_is_on_report(page: Page) -> None:
    """
    Test to check that a subject who is due to be invited, and does have a temporary address, and is at this hub, does appear in the report.
    """
    logging.info(
        "Starting test: Check that a subject who is due to be invited, and does have a temporary address, and is at this hub, does appear in the report."
    )

    criteria = {
        "subject has temporary address": "current",
        "subject hub code": "BCS01",
        "subject is due for invite": "yes"
    }

    nhs_no = _db_search(criteria)

    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    BasePage(page).click_main_menu_link()
    _go_to_report_page(page)

    report = SubjectsToBeInvitedWithTemporaryAddressPage(page)
    report.filter_by_nhs_number(nhs_no)
    report.assertRecordsVisible(nhs_no, True)
    _go_to_demographics_page_for_subject_from_report(page, nhs_no)
    _remove_a_temp_address(page)

    BasePage(page).click_main_menu_link()
    _go_to_report_page(page)

    report.filter_by_nhs_number(nhs_no)
    report.assertRecordsVisible(nhs_no, False)


def _db_search(criteria) -> None:
    logging.info(
        f"Starting _db_search: {criteria}"
    )
    user = User()
    subject = Subject()

    builder = SubjectSelectionQueryBuilder()

    query, bind_vars = builder.build_subject_selection_query(
        criteria=criteria, user=user, subject=subject, subjects_to_retrieve=1
    )

    df = OracleDB().execute_query(query, bind_vars)
    nhs_no = df.iloc[0]["subject_nhs_number"]

    logging.info(
        f"Identified {nhs_no}."
    )
    return nhs_no

def _go_to_report_page(page: Page) -> None:
    BasePage(page).go_to_reports_page()
    ReportsPage(page).go_to_operational_reports_page()
    SubjectsToBeInvitedWithTemporaryAddressPage(page).go_to_page()

    SubjectsToBeInvitedWithTemporaryAddressPage(page).verify_page_title()

def _go_to_demographics_page_for_subject_from_menu(page: Page, nhs_no: str) -> None:
    BasePage(page).go_to_screening_subject_search_page()
    search_subject_episode_by_nhs_number(page, nhs_no)
    _go_to_demographics_page_for_subject(page)

def _go_to_demographics_page_for_subject_from_report(page: Page, nhs_no: str) -> None:
    SubjectsToBeInvitedWithTemporaryAddressPage(page).click_subject_link(nhs_no)
    _go_to_demographics_page_for_subject(page)

def _go_to_demographics_page_for_subject(page: Page) -> None:
    SubjectScreeningSummaryPage(page).click_subject_demographics()

    SubjectDemographicPage(page).verify_page_title()

def _add_a_temp_address(page: Page) -> None:
    temp_address = {
        "valid_from": datetime.today(),
        "valid_to": datetime.today() + timedelta(days=100),
        "address_line_1": "add line 1",
        "address_line_2": "add line 2",
        "address_line_3": "add line 3",
        "address_line_4": "add line 4",
        "address_line_5": "add line 5",
        "postcode": "EX2 5SE",
    }
    _update_temp_address(page, temp_address)

def _remove_a_temp_address(page: Page) -> None:
    temp_address = {
        "valid_from": None,
        "valid_to": None,
        "address_line_1": "",
        "address_line_2": "",
        "address_line_3": "",
        "address_line_4": "",
        "address_line_5": "",
        "postcode": "",
    }
    _update_temp_address(page, temp_address)

def _update_temp_address(page: Page, temp_address) -> None:
    logging.info(f"Updating Temporary address : {temp_address}.")
    demographic_page = SubjectDemographicPage(page)

    logging.info("Updating postcode as sometimes the existing address has a bad or blank value which might break the save")
    demographic_page.fill_postcode_input("EX11AA")
    demographic_page.update_temporary_address(temp_address)
