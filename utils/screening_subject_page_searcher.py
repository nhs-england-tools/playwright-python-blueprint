from pages.base_page import BasePage
from pages.screening_subject_search.subject_screening_search_page import (
    SubjectScreeningPage,
    SearchAreaSearchOptions,
)
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from playwright.sync_api import Page, expect


def verify_subject_event_status_by_nhs_no(
    page: Page, nhs_no: str, latest_event_status: str | list
) -> None:
    """
    This is used to check that the latest event status of a subject has been updated to what is expected
    We provide the NHS Number for the subject and the expected latest event status and it navigates to the correct page
    From here it searches for that subject against the whole database and verifies the latest event status is as expected

    Args:
        page (Page): This is the playwright page object
        nhs_no (str): The screening subject's nhs number
        latest_event_status (str | list): the screening subjects's latest event status
    """
    BasePage(page).click_main_menu_link()
    BasePage(page).go_to_screening_subject_search_page()
    SubjectScreeningPage(page).click_nhs_number_filter()
    SubjectScreeningPage(page).nhs_number_filter.fill(nhs_no)
    SubjectScreeningPage(page).nhs_number_filter.press("Tab")
    SubjectScreeningPage(page).select_search_area_option(
        SearchAreaSearchOptions.SEARCH_AREA_WHOLE_DATABASE.value
    )
    SubjectScreeningPage(page).click_search_button()
    SubjectScreeningSummaryPage(page).verify_subject_screening_summary()
    SubjectScreeningSummaryPage(page).verify_latest_event_status_header()
    SubjectScreeningSummaryPage(page).verify_latest_event_status_value(
        latest_event_status
    )


def search_subject_by_nhs_number(page: Page, nhs_number: str) -> None:
    """
    This searches for a subject by their NHS Number and checks the page has redirected accordingly

    Args:
        page (Page): This is the playwright page object
        nhs_no (str): The screening subject's nhs number
    """
    SubjectScreeningPage(page).click_clear_filters_button()
    SubjectScreeningPage(page).nhs_number_filter.fill(nhs_number)
    SubjectScreeningPage(page).nhs_number_filter.press("Tab")
    SubjectScreeningPage(page).click_search_button()


def search_subject_by_surname(page: Page, surname: str) -> None:
    """
    This searches for a subject by their surname and checks the page has redirected accordingly

    Args:
        page (Page): This is the playwright page object
        surname (str): The screening subject's surname
    """
    SubjectScreeningPage(page).click_clear_filters_button()
    SubjectScreeningPage(page).surname_filter.fill(surname)
    SubjectScreeningPage(page).surname_filter.press("Tab")
    SubjectScreeningPage(page).click_search_button()


def search_subject_by_forename(page: Page, forename: str) -> None:
    """
    This searches for a subject by their forename and checks the page has redirected accordingly

    Args:
        page (Page): This is the playwright page object
        forename (str): The screening subject's forename
    """
    SubjectScreeningPage(page).click_clear_filters_button()
    SubjectScreeningPage(page).forename_filter.fill(forename)
    SubjectScreeningPage(page).forename_filter.press("Tab")
    SubjectScreeningPage(page).click_search_button()


def search_subject_by_dob(page: Page, dob: str) -> None:
    """
    This searches for a subject by their date of birth and checks the page has redirected accordingly

    Args:
        page (Page): This is the playwright page object
        dob (str): The screening subject's date of birth
    """
    SubjectScreeningPage(page).click_clear_filters_button()
    SubjectScreeningPage(page).date_of_birth_filter.fill(dob)
    SubjectScreeningPage(page).date_of_birth_filter.press("Tab")
    SubjectScreeningPage(page).click_search_button()


def search_subject_by_postcode(page: Page, postcode: str) -> None:
    """
    This searches for a subject by their postcode and checks the page has redirected accordingly

    Args:
        page (Page): This is the playwright page object
        postcode (str): The screening subject's postcode
    """
    SubjectScreeningPage(page).click_clear_filters_button()
    SubjectScreeningPage(page).postcode_filter.fill(postcode)
    SubjectScreeningPage(page).postcode_filter.press("Tab")
    SubjectScreeningPage(page).click_search_button()


def search_subject_by_episode_closed_date(page: Page, episode_closed_date: str) -> None:
    """
    This searches for a subject by their episode closed date and checks the page has redirected accordingly

    Args:
        page (Page): This is the playwright page object
        episode_closed_date (str): The screening subject's episode closed date
    """
    SubjectScreeningPage(page).click_clear_filters_button()
    SubjectScreeningPage(page).episode_closed_date_filter.fill(episode_closed_date)
    SubjectScreeningPage(page).episode_closed_date_filter.press("Tab")
    SubjectScreeningPage(page).click_search_button()


def search_subject_by_status(page: Page, status: str) -> None:
    """
    This searches for a subject by their screening status and checks the page has redirected accordingly

    Args:
        page (Page): This is the playwright page object
        status (str): The screening subject's screening status
    """
    SubjectScreeningPage(page).click_clear_filters_button()
    SubjectScreeningPage(page).select_screening_status_options(status)
    SubjectScreeningPage(page).select_screening_status.press("Tab")
    SubjectScreeningPage(page).click_search_button()


def search_subject_by_latest_event_status(page: Page, status: str) -> None:
    """
    This searches for a subject by their latest event status and checks the page has redirected accordingly

    Args:
        page (Page): This is the playwright page object
        status (str): The screening subject's latest event status
    """
    SubjectScreeningPage(page).click_clear_filters_button()
    SubjectScreeningPage(page).select_episode_status_option(status)
    SubjectScreeningPage(page).select_episode_status.press("Tab")
    SubjectScreeningPage(page).click_search_button()


def search_subject_by_search_area(
    page: Page, status: str, search_area: str, code: str=None, gp_practice_code: str=None
) -> None:
    """
    This searches for a subject by the search area, populating necessary fields were needed, and checks that the page has redirected accordingly

    Args:
        page (Page): This is the playwright page object
        status (str): The screening subject's screening status
        search_area (str): This is the search area option to use
        code (str): If provided, the code parameter is used to fill the appropriate code filter field
        gp_practice_code (str): If provided, the GP practice code parameter is used to fill the GP Practice in CCG filter field
    """
    SubjectScreeningPage(page).click_clear_filters_button()
    SubjectScreeningPage(page).select_screening_status_options(status)
    SubjectScreeningPage(page).select_screening_status.press("Tab")
    SubjectScreeningPage(page).select_search_area_option(search_area)
    SubjectScreeningPage(page).select_search_area.press("Tab")
    if code != None:
        SubjectScreeningPage(page).appropriate_code_filter.fill(code)
        SubjectScreeningPage(page).appropriate_code_filter.press("Tab")
    if gp_practice_code != None:
        SubjectScreeningPage(page).gp_practice_in_ccg_filter.fill(gp_practice_code)
        SubjectScreeningPage(page).gp_practice_in_ccg_filter.press("Tab")
    SubjectScreeningPage(page).click_search_button()


def check_clear_filters_button_works(page: Page, nhs_number: str) -> None:
    """
    This checks that the "clear filter" button works as intended

    Args:
        page (Page): This is the playwright page object
        nhs_number (str): The screening subject's nhs number
    """
    SubjectScreeningPage(page).nhs_number_filter.fill(nhs_number)
    expect(SubjectScreeningPage(page).nhs_number_filter).to_have_value(nhs_number)
    SubjectScreeningPage(page).click_clear_filters_button()
    expect(SubjectScreeningPage(page).nhs_number_filter).to_be_empty()
