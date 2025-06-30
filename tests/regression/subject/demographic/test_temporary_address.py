import pytest
from playwright.sync_api import Page
from utils.user_tools import UserTools
from classes.user import User
from classes.subject import Subject
from pages.base_page import BasePage
from pages.screening_subject_search.subject_demographic_page import (
    SubjectDemographicPage,
)
from pages.logout.log_out_page import LogoutPage
from utils.screening_subject_page_searcher import (
    search_subject_demographics_by_nhs_number,
)
from utils.oracle.oracle import OracleDB
from utils.oracle.oracle_specific_functions import (
    check_if_subject_has_temporary_address,
)
from utils.oracle.subject_selection_query_builder import SubjectSelectionQueryBuilder
import logging
from faker import Faker
from datetime import datetime, timedelta


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page) -> str:
    """
    Before every test is executed, this fixture:
    - Logs into BCSS as a Screening Centre Manager at BCS001
    - Navigates to the screening subject search page
    """
    nhs_no = obtain_test_data_nhs_no()
    logging.info(f"Selected NHS Number: {nhs_no}")
    UserTools.user_login(page, "Screening Centre Manager at BCS001")
    BasePage(page).go_to_screening_subject_search_page()
    search_subject_demographics_by_nhs_number(page, nhs_no)
    return nhs_no


@pytest.mark.wip
@pytest.mark.regression
@pytest.mark.subject_tests
def test_not_amending_temporary_address(page: Page, before_each) -> None:
    """
    Scenario: If not amending a temporary address, no need to validate it

    This test is checking that if a temporary address is not being amended,
    and the subject's postcode is updated.
    That the subject does not have a temporary address added to them.
    """
    nhs_no = before_each
    fake = Faker("en_GB")
    random_postcode = fake.postcode()
    SubjectDemographicPage(page).fill_postcode_input(random_postcode)
    SubjectDemographicPage(page).postcode_field.press("Tab")
    SubjectDemographicPage(page).click_update_subject_data_button()

    check_subject_has_temporary_address(nhs_no, temporary_address=False)
    LogoutPage(page).log_out()


@pytest.mark.wip
@pytest.mark.regression
@pytest.mark.subject_tests
def test_add_temporary_address_then_delete(page: Page, before_each) -> None:
    """
    Add a temporary address, then delete it.

    This test is checking that a temporary address can be added to a subject,
    and then deleted successfully, ensuring the temporary address icon behaves as expected.
    """
    nhs_no = before_each

    temp_address = {
        "valid_from": datetime.today(),
        "valid_to": datetime.today() + timedelta(days=31),
        "address_line_1": "Temporary Address Line 1",
        "address_line_2": "Temporary Address Line 2",
        "address_line_3": "Temporary Address Line 3",
        "address_line_4": "Temporary Address Line 4",
        "address_line_5": "Temporary Address Line 5",
        "postcode": "AB12 3CD",
    }
    SubjectDemographicPage(page).update_temporary_address(temp_address)
    check_subject_has_temporary_address(nhs_no, temporary_address=True)

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
    SubjectDemographicPage(page).update_temporary_address(temp_address)

    check_subject_has_temporary_address(nhs_no, temporary_address=False)
    LogoutPage(page).log_out()


@pytest.mark.wip
@pytest.mark.regression
@pytest.mark.subject_tests
def test_validation_regarding_dates(page: Page) -> None:
    """
    Checks the validation regarding the temporary address date fields works as expected.

    This test is checking that the validation for the temporary address date fields
    works correctly when the user tries to enter a temporary address with invalid dates.
    It ensures that the user is prompted with appropriate error messages when the dates are not valid.
    """

    temp_address = {
        "valid_from": None,
        "valid_to": None,
        "address_line_1": "Line 1",
        "address_line_2": "Line 2",
        "address_line_3": "Line 3",
        "address_line_4": "Line 4",
        "address_line_5": "Line 5",
        "postcode": "EX2 5SE",
    }
    subject_page = SubjectDemographicPage(page)

    subject_page.assert_dialog_text(
        "If entering a temporary address, please specify the From-date"
    )
    subject_page.update_temporary_address(temp_address)
    dialog_error = getattr(subject_page, "_dialog_assertion_error", None)
    if dialog_error is not None:
        raise dialog_error
    logging.info("Temporary address validation for 'From-date' passed.")

    temp_address["valid_from"] = datetime(1900, 1, 1)
    subject_page.assert_dialog_text(
        "If entering a temporary address, please specify the To-date"
    )
    subject_page.update_temporary_address(temp_address)
    dialog_error = getattr(subject_page, "_dialog_assertion_error", None)
    if dialog_error is not None:
        raise dialog_error
    logging.info("Temporary address validation for 'To-date' passed.")

    temp_address["valid_to"] = datetime(1900, 1, 2)
    subject_page.assert_dialog_text(
        "The From-date of the Subject's temporary address must not be before the Date of Birth"
    )
    subject_page.update_temporary_address(temp_address)
    dialog_error = getattr(subject_page, "_dialog_assertion_error", None)
    if dialog_error is not None:
        raise dialog_error
    logging.info("Temporary address validation for 'From-date before DOB' passed.")

    # Reset to valid state before next test
    temp_address["valid_from"] = datetime.today()
    temp_address["valid_to"] = datetime.today() + timedelta(days=1)
    subject_page.update_temporary_address(temp_address)

    temp_address["valid_from"] = datetime.today() + timedelta(days=1)
    temp_address["valid_to"] = datetime.today()
    subject_page.assert_dialog_text(
        "The From-date of the Subject's temporary address must not be after the To-date"
    )
    subject_page.update_temporary_address(temp_address)
    dialog_error = getattr(subject_page, "_dialog_assertion_error", None)
    if dialog_error is not None:
        raise dialog_error
    logging.info("Temporary address validation for 'From-date after To-date' passed.")

    LogoutPage(page).log_out()


@pytest.mark.wip
@pytest.mark.regression
@pytest.mark.subject_tests
def test_ammending_temporary_address(page: Page, before_each) -> None:
    """
    Scenario: If amending a temporary address, it should be validated.

    This test checks that if a temporary address is being amended,
    and the subject's postcode is updated.
    That the subject has a temporary address added to them.
    """
    nhs_no = before_each

    temp_address = {
        "valid_from": datetime(2000, 1, 1),
        "valid_to": datetime(2000, 1, 2),
        "address_line_1": "Line 1",
        "address_line_2": "Line 2",
        "address_line_3": "Line 3",
        "address_line_4": "Line 4",
        "address_line_5": "Line 5",
        "postcode": "EX2 5SE",
    }
    SubjectDemographicPage(page).update_temporary_address(temp_address)
    check_subject_has_temporary_address(nhs_no, temporary_address=True)

    temp_address = {
        "valid_from": datetime(3000, 1, 1),
        "valid_to": datetime(3000, 1, 2),
        "address_line_1": "Line 1.1",
        "address_line_2": "Line 2.1",
        "address_line_3": "Line 3.1",
        "address_line_4": "Line 4.1",
        "address_line_5": "Line 5.1",
        "postcode": "EX2 5SE",
    }
    SubjectDemographicPage(page).update_temporary_address(temp_address)
    check_subject_has_temporary_address(nhs_no, temporary_address=True)

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
    SubjectDemographicPage(page).update_temporary_address(temp_address)
    check_subject_has_temporary_address(nhs_no, temporary_address=False)

    LogoutPage(page).log_out()


@pytest.mark.wip
@pytest.mark.regression
@pytest.mark.subject_tests
def test_validating_minimum_information(page: Page, before_each) -> None:
    """
    Scenario: Validation regarding minimum information
    This test checks that the validation for the temporary address fields
    works correctly when the user tries to enter a temporary address with minimum information.
    It ensures that the user is prompted with appropriate error messages when the minimum information is not provided
    """
    nhs_no = before_each

    temp_address = {
        "valid_from": datetime.today(),
        "valid_to": datetime.today() + timedelta(days=1),
        "address_line_1": "",
        "address_line_2": "",
        "address_line_3": "",
        "address_line_4": "",
        "address_line_5": "",
        "postcode": "",
    }

    subject_page = SubjectDemographicPage(page)
    subject_page.assert_dialog_text(
        "If entering a temporary address, please specify at least the first two lines and the postcode"
    )
    subject_page.update_temporary_address(temp_address)
    dialog_error = getattr(subject_page, "_dialog_assertion_error", None)
    if dialog_error is not None:
        raise dialog_error
    logging.info("Temporary address validation for minimum information passed.")

    temp_address["address_line_1"] = "min1"
    temp_address["address_line_2"] = "min2"
    subject_page.assert_dialog_text(
        "If entering a temporary address, please specify at least the first two lines and the postcode"
    )
    subject_page.update_temporary_address(temp_address)
    dialog_error = getattr(subject_page, "_dialog_assertion_error", None)
    if dialog_error is not None:
        raise dialog_error
    logging.info("Temporary address validation for minimum information passed.")

    temp_address["address_line_1"] = "min1"
    temp_address["address_line_2"] = ""
    temp_address["postcode"] = "pc"
    subject_page.assert_dialog_text(
        "If entering a temporary address, please specify at least the first two lines and the postcode"
    )
    subject_page.update_temporary_address(temp_address)
    dialog_error = getattr(subject_page, "_dialog_assertion_error", None)
    if dialog_error is not None:
        raise dialog_error
    logging.info("Temporary address validation for minimum information passed.")

    temp_address["address_line_1"] = ""
    temp_address["address_line_2"] = "min2"
    subject_page.assert_dialog_text(
        "If entering a temporary address, please specify at least the first two lines and the postcode"
    )
    subject_page.update_temporary_address(temp_address)
    dialog_error = getattr(subject_page, "_dialog_assertion_error", None)
    if dialog_error is not None:
        raise dialog_error
    logging.info("Temporary address validation for minimum information passed.")

    temp_address["address_line_1"] = "min1"
    temp_address["address_line_2"] = "min2"
    temp_address["postcode"] = "pc"
    subject_page.update_temporary_address(temp_address)
    check_subject_has_temporary_address(nhs_no, temporary_address=True)

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
    subject_page = SubjectDemographicPage(page)
    subject_page.update_temporary_address(temp_address)
    check_subject_has_temporary_address(nhs_no, temporary_address=False)


def check_subject_has_temporary_address(nhs_no: str, temporary_address: bool) -> None:
    """
    Checks if the subject has a temporary address in the database.
    Args:
        nhs_no (str): The NHS number of the subject.
        temporary_address (bool): True if checking for a temporary address, False otherwise.
    Raises:
        AssertionError: If the expected address status does not match the actual status in the database.
    This function queries the database to determine if the subject has a temporary address
    and asserts the result against the expected value.
    The result is then compared to the expected status, and an assertion is raised if they do not match.
    """

    df = check_if_subject_has_temporary_address(nhs_no)

    if temporary_address:
        logging.info(
            "Checking if the subject has an active temporary address in the database."
        )
        assert (
            df.iloc[0]["address_status"] == "Subject has a temporary address"
        ), "Temporary address not found in the database."
        logging.info(
            "Assertion passed: Active temporary address found in the database."
        )
    else:
        logging.info(
            "Checking if the subject does not have an active temporary address in the database."
        )
        assert (
            df.iloc[0]["address_status"] == "Subject doesn't have a temporary address"
        ), "Temporary address found in the database when it shouldn't be."
        logging.info(
            "Assertion passed: No active temporary address found in the database."
        )


def obtain_test_data_nhs_no() -> str:
    """
    Obtain a test subject's NHS number that matches the following criteria:
    | Subject age                   | <= 80 |
        | Subject has temporary address | No    |

    This is obtained using the Subject Selection Query Builder.

    Returns:
        str: The NHS number of the subject that matches the criteria.
    """
    criteria = {
        "subject age": "<= 80",
        "subject has temporary address": "no",
    }
    user = User()
    subject = Subject()

    builder = SubjectSelectionQueryBuilder()

    query, bind_vars = builder.build_subject_selection_query(
        criteria=criteria, user=user, subject=subject, subjects_to_retrieve=1
    )

    df = OracleDB().execute_query(query, bind_vars)
    nhs_no = df.iloc[0]["subject_nhs_number"]
    return nhs_no
