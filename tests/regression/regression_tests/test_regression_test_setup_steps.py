import pytest
import logging
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.contacts_list.contacts_list_page import ContactsListPage
from pages.contacts_list.maintain_contacts_page import MaintainContactsPage
from pages.contacts_list.edit_contact_page import EditContactPage
from pages.contacts_list.resect_and_discard_accreditation_history_page import (
    ResectAndDiscardAccreditationHistoryPage,
)
from pages.logout.log_out_page import LogoutPage
from utils.user_tools import UserTools
from utils.oracle.oracle_specific_functions import (
    set_org_parameter_value,
    check_parameter,
    build_accredited_screening_colonoscopist_query,
    get_accredited_screening_colonoscopist_in_bcs001,
)


def test_allow_10_minute_colonsocopy_assessment_appointments(
    page: Page, general_properties: dict
) -> None:
    """
    Scenario: 1: Allow 10 minute colonoscopy assessment appointments between 7am and 8pm at BCS001

    Given I log in to BCSS "England" as user role "Screening Centre Manager"
        And I set the value of parameter 12 to "10" for my organisation with immediate effect
        And I set the value of parameter 28 to "07:00" for my organisation with immediate effect
        And I set the value of parameter 29 to "20:00" for my organisation with immediate effect
    """
    UserTools.user_login(page, "Screening Centre Manager at BCS001")
    org_id = general_properties["eng_screening_centre_id"]
    param_12_set_correctly = check_parameter(12, org_id, "10")
    param_28_set_correctly = check_parameter(28, org_id, "07:00")
    param_29_set_correctly = check_parameter(29, org_id, "20:00")
    if not param_12_set_correctly:
        set_org_parameter_value(12, "10", org_id)
    if not param_28_set_correctly:
        set_org_parameter_value(28, "07:00", org_id)
    if not param_29_set_correctly:
        set_org_parameter_value(29, "20:00", org_id)

    LogoutPage(page).log_out()


def test_asc_with_current_resect_and_discard_accreditation(
    page: Page,
) -> None:
    """
    Scenario: 2: Ensure there is an Accredited Screening Colonoscopist with current Resect & Discard accreditation
    """
    UserTools.user_login(page, "BCSS Bureau Staff at X26")

    current_df = build_accredited_screening_colonoscopist_query("Current")
    if current_df.empty:
        pytest.skip(
            "No Accredited Screening Colonoscopist with current Resect & Discard accreditation found."
        )
    expired_df = build_accredited_screening_colonoscopist_query("Expiring soon")
    if expired_df.empty:
        pytest.skip(
            "No Accredited Screening Colonoscopist with expiring Resect & Discard accreditation found."
        )
    person_df = get_accredited_screening_colonoscopist_in_bcs001()
    if person_df.empty:
        pytest.fail("No Accredited Screening Colonoscopist found in the database.")

    BasePage(page).go_to_contacts_list_page()
    ContactsListPage(page).go_to_maintain_contacts_page()

    surname = person_df.iloc[0]["person_family_name"]
    forename = person_df.iloc[0]["person_given_name"]
    MaintainContactsPage(page).fill_surname_input_field(surname)
    MaintainContactsPage(page).fill_forenames_input_field(forename)
    MaintainContactsPage(page).click_search_button()
    MaintainContactsPage(page).click_person_link_from_surname(surname)

    EditContactPage(page).click_view_resect_and_discard_link()
    ResectAndDiscardAccreditationHistoryPage(page).verify_heading_is_correct()
    ResectAndDiscardAccreditationHistoryPage(
        page
    ).verify_add_accreditation_button_exists()
    yesterday = datetime.today() - timedelta(days=1)
    ResectAndDiscardAccreditationHistoryPage(
        page
    ).add_new_period_of_resect_and_discard_accerditation(date=yesterday)

    BasePage(page).click_back_button()
    end_date = yesterday + relativedelta(years=2)
    EditContactPage(page).assert_value_for_label_in_edit_contact_table(
        "Resect & Discard Accreditation?",
        f"Current: ends {end_date.strftime('%d/%m/%Y')}",
    )
    logging.info(f"Test person used in this scenario is: {forename} {surname}")
