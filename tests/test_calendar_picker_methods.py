from pages.screening_subject_search.subject_screening_search_page import (
    SubjectScreeningPage,
)
from pages.communication_production.communications_production_page import (
    CommunicationsProductionPage,
)
from pages.communication_production.batch_list_page import ActiveBatchListPage
import pytest
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.user_tools import UserTools
from datetime import datetime


@pytest.mark.smoke
def test_calender_picker_v1(page: Page) -> None:
    """
    This test is used to verify that the v1 calendar picker in utils/calendar_picker.py works as intended
    This uses the subject screening search page in order to do so
    NOTE: currently there is no validation that it has selected the correct date.
        This should be implemented after each date is selected however the locators on BCSS make this task difficult
    """
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")
    BasePage(page).go_to_screening_subject_search_page()
    SubjectScreeningPage(page).select_dob_using_calendar_picker(datetime(2021, 12, 1))
    SubjectScreeningPage(page).click_clear_filters_button()
    SubjectScreeningPage(page).select_dob_using_calendar_picker(datetime(2020, 3, 30))
    SubjectScreeningPage(page).click_clear_filters_button()
    SubjectScreeningPage(page).select_dob_using_calendar_picker(datetime(2020, 6, 15))
    SubjectScreeningPage(page).click_clear_filters_button()
    SubjectScreeningPage(page).select_dob_using_calendar_picker(datetime.today())


@pytest.mark.smoke
def test_calender_picker_v2(page: Page) -> None:
    """
    This test is used to verify that the v2 calendar picker in utils/calendar_picker.py works as intended
    This uses the active batch list page in order to do so
    NOTE: currently there is no validation that it has selected the correct date.
        This should be implemented after each date is selected however the locators on BCSS make this task difficult
    """
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")
    BasePage(page).go_to_communications_production_page()
    CommunicationsProductionPage(page).go_to_active_batch_list_page()
    ActiveBatchListPage(page).enter_deadline_date_filter(datetime(1961, 12, 30))
    ActiveBatchListPage(page).clear_deadline_filter_date()
    ActiveBatchListPage(page).enter_deadline_date_filter(datetime(2026, 12, 1))
    ActiveBatchListPage(page).clear_deadline_filter_date()
    ActiveBatchListPage(page).enter_deadline_date_filter(datetime(1989, 6, 15))
    ActiveBatchListPage(page).clear_deadline_filter_date()
    ActiveBatchListPage(page).enter_deadline_date_filter(datetime.today())
