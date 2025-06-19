import logging
import boto3
import json

from pandas import DataFrame
import pytest
import time
from dateutil.parser import parse
from playwright.sync_api import expect, Page
from tests.ui.cohort_manager.cohort_manager_util import (
    fetch_subject_column_value,
    subject_count_by_nhs_number,
)
from utils.db_util import DbUtil
from utils.user_tools import UserTools


logging.getLogger("botocore").setLevel(logging.WARNING)

## Run this cmd before running these tests - aws sso login --profile bs-select-rw-user-730319765130


################ CM Lambda Positive tests ####################
# TC-9
@pytest.mark.cm1
def test_status_204(db_util: DbUtil) -> None:
    """
    trigger_lambda_with_python and assert the status of 204
    """
    message_id = "ffffffff-ffff-ffff-ffff-fffffffff204"
    insert_data(db_util, message_id)
    trigger_lambda_and_verify_success(0)


# TC-2,  this test covers TC-4 as well
@pytest.mark.cm2
def test_validate_max_field_length_in_db_pi_changes(db_util: DbUtil) -> None:
    """
    Test to validate cohort_manager max field length in db pi_changes table
    """
    # Insert data
    message_id = "ffffffff-ffff-ffff-ffff-ffffffffffcc"
    insert_data(db_util, message_id)
    trigger_lambda_and_verify_success(1)

    stub_data = {
        "request_id": "6d649f7d-e36f-475e-886b-60ff12d4ddea",
        "nhs_number": "9470082060",
        "name_prefix": "Dr Professor Jonathan WilliamsonXYZ",
        "family_name": "Montgomery Featherstonehaugh ABCXYZ",
        "given_name": "Alexander Jonathan Williamson ABXYZ",
        "other_given_names": "ChristopherEdwardNathanielBenedictAndersonSmithJackson WilliamsRobertJohnsonThompsonSusanLouiseGrogu",
        "previous_family_name": "Montgomery Featherstonehaugh ABC XY",
        "birth_date": "19670101",
        "death_date": "",
        "gender_code": 2,
        "address_line_1": "1234 Greenwood AvenueApartmentSuite 5678",
        "address_line_2": "5678 OakwoodStreetBuilding Number 234567",
        "address_line_3": "91011 MapleLaneResidentialBlock CUnit 56",
        "address_line_4": "1415 PineHillRoadBusinessDistrict Floor7",
        "address_line_5": "1617 CedarGroveDriveLakeviewApartment 3B",
        "postcode": "EU13 9NG",
        "primary_care_provider": "A00002",
        "reason_for_removal": "",
        "reason_removal_eff_from_date": "",
        "superseded_by_nhs_number": "",
        "telephone_number_home": "12345678901234567890123456789012",
        "telephone_number_mobile": "12345678901234567890123456789012",
        "email_address_home": "JonathanWilliamsonAlexanderChristopherEdwardNathanielBenedictSmithWiliamsonJoe@example.com",
        "preferred_language": "En",
        "interpreter_required": "1",
        "usual_address_eff_from_date": "20201201",
        "telephone_number_home_eff_from_date": "20201231",
        "telephone_number_mobile_eff_from_date": "20201231",
        "email_address_home_eff_from_date": "20201231",
    }
    # Retrieve data from the DB using the request_id from stub data
    db_result = get_latest_record_by_request_id(db_util, stub_data["request_id"])
    inserted = db_result.to_dict("records")[0]

    # Assertion to compare stub data and DB data
    assert (
        str(inserted["message_id"]) == stub_data["request_id"]
    ), "field not matched: request_id"
    nhs_number = "9470082060"
    wait_for_assertion(
        lambda: fetch_pi_changes_column_value(db_util, nhs_number, "state")
        == "PROCESSED"
    )
    assert inserted["nhs_number"] == stub_data["nhs_number"]
    assert inserted["name_prefix"] == stub_data["name_prefix"]
    assert inserted["family_name"] == stub_data["family_name"]
    assert inserted["first_name"] == stub_data["given_name"]
    assert inserted["other_names"] == stub_data["other_given_names"]
    assert inserted["previous_family_name"] == stub_data["previous_family_name"]
    assert inserted["date_of_birth"].strftime("%Y%m%d") == stub_data["birth_date"]
    assert inserted["gender_code"] == stub_data["gender_code"]
    assert inserted["address_line_1"] == stub_data["address_line_1"]
    assert inserted["address_line_2"] == stub_data["address_line_2"]
    assert inserted["address_line_3"] == stub_data["address_line_3"]
    assert inserted["address_line_4"] == stub_data["address_line_4"]
    assert inserted["address_line_5"] == stub_data["address_line_5"]
    assert inserted["postcode"] == stub_data["postcode"]
    assert inserted["gp_practice_code"] == stub_data["primary_care_provider"]
    assert inserted["processed_date_time"] == stub_data.get("processed_date_time")
    assert inserted["person_application_feed_id"] == stub_data.get(
        "person_application_feed_id"
    )
    assert inserted["transaction_id"] == stub_data.get("transaction_id")
    assert inserted["transaction_user_org_role_id"] == stub_data.get(
        "transaction_user_org_role_id"
    )
    assert inserted["telephone_number_home"] == stub_data.get("telephone_number_home")
    assert inserted["telephone_number_mobile"] == stub_data.get(
        "telephone_number_mobile"
    )
    assert inserted["email_address_home"] == stub_data.get("email_address_home")
    assert (
        inserted["preferred_language"].upper()
        == stub_data["preferred_language"].upper()
    )
    assert inserted["interpreter_required"] == bool(stub_data["interpreter_required"])
    assert (
        inserted["usual_address_eff_from_date"].strftime("%Y%m%d")
        == stub_data["usual_address_eff_from_date"]
    )
    assert (
        inserted["tel_number_home_eff_from_date"].strftime("%Y%m%d")
        == stub_data["telephone_number_home_eff_from_date"]
    )
    assert (
        inserted["tel_number_mob_eff_from_date"].strftime("%Y%m%d")
        == stub_data["telephone_number_mobile_eff_from_date"]
    )
    assert (
        inserted["email_addr_home_eff_from_date"].strftime("%Y%m%d")
        == stub_data["email_address_home_eff_from_date"]
    )


# TC-3
@pytest.mark.cm3
def test_validate_greater_than_max_field_length_of_nhs_number_in_db_pi_changes(
    db_util: DbUtil,
) -> None:
    """
    Negative test to validate cohort_manager greater than max field length of nhs_number in db pi_changes table
    """
    stub_request_id = "6d649f7d-e36f-475e-846b-60ff12d4bdea"

    # Insert data
    message_id = "ffffffc3-ffff-ffff-ffff-fffffffffff1"
    insert_data(db_util, message_id)
    trigger_lambda_and_verify_error(
        "Invalid response from cohort manager: attribute: nhs_number should be of length 10 but was 11"
    )

    # verify db has the latest request_id
    db_result = get_latest_record_by_request_id(db_util, stub_request_id)
    assert len(db_result) == 0


# TC-3
def test_validate_greater_than_max_field_length_of_family_name_in_db_pi_changes(
    db_util: DbUtil,
) -> None:
    """
    Negative test to validate cohort_manager greater than max field length of family_name in db pi_changes table
    """
    stub_request_id = "6d649f7d-e36f-475e-846b-60cd12d4bdea"

    # Insert data
    message_id = "ffffffc3-ffff-ffff-ffff-fffffffffff2"
    insert_data(db_util, message_id)
    trigger_lambda_and_verify_error(
        "Invalid response from cohort manager: attribute: family_name should be of maximum length 35 but was 37"
    )

    # verify db has the latest request_id
    db_result = get_latest_record_by_request_id(db_util, stub_request_id)
    assert len(db_result) == 0


# TC-8 test covers TC-6 & TC-7
@pytest.mark.tc8
def test_to_add_and_update_participant_in_the_pi_changes(db_util: DbUtil) -> None:
    """
    Test to add and update the participant and assert the added and updaded values
    """
    # Insert data
    nhs_number = "9011000042"
    message_id = "ffffffff-ffff-ffff-ffff-fffffffffc8f"
    insert_data(db_util, message_id)
    trigger_lambda_and_verify_success(1)

    stub_data = {
        "request_id": "2f153e68-b4f3-45fb-a85d-14b0d1eb22bb",
        "nhs_number": "9011000042",
        "name_prefix": "Dr.",
        "family_name": "Bednar",
        "given_name": "Miguelina",
        "other_given_names": "Raul",
        "previous_family_name": "Olson",
        "birth_date": "19700702",
        "death_date": "",
        "gender_code": 2,
        "address_line_1": "Apt. 825",
        "address_line_2": "71354 Monahan Squares",
        "address_line_3": "Lake Jamieside",
        "address_line_4": "Arkansas",
        "address_line_5": "Burundi",
        "postcode": "EU1 8LN",
        "primary_care_provider": "A00001",
        "reason_for_removal": "",
        "reason_removal_eff_from_date": "",
        "superseded_by_nhs_number": "",
        "telephone_number_home": "40846 280 931",
        "telephone_number_mobile": "40103 024 754",
        "email_address_home": "dltlhagqn3229@test.com",
        "preferred_language": "en",
        "interpreter_required": 1,
        "usual_address_eff_from_date": "20000101",
        "telephone_number_home_eff_from_date": "20000101",
        "telephone_number_mobile_eff_from_date": "20000101",
        "email_address_home_eff_from_date": "20000101",
        "primary_care_provider_eff_from_date": "20000101",
    }

    # Retrieve data from the DB using the request_id from stub data
    db_result = get_latest_record_by_request_id(db_util, stub_data["request_id"])
    inserted = db_result.to_dict("records")[0]

    # Perform the assertion to compare stub data and DB data
    assert (
        str(inserted["message_id"]) == stub_data["request_id"]
    ), "field not matched: request_id"
    wait_for_assertion(
        lambda: fetch_pi_changes_column_value(db_util, nhs_number, "state")
        == "PROCESSED"
    )
    assert inserted["address_line_1"] == stub_data["address_line_1"]
    assert inserted["telephone_number_home"] == stub_data.get("telephone_number_home")
    assert inserted["telephone_number_mobile"] == stub_data.get(
        "telephone_number_mobile"
    )
    # Insert data for add and update
    insert_data(db_util, "ffffffff-ffff-ffff-ffff-ffffffffc8ff")
    trigger_lambda_and_verify_success(2)

    stub_data_update = [
        {
            "request_id": "2f153e68-b4f3-45f2-a85d-14b0d1eb22cc",
            "nhs_number": "9000000041",
            "superseded_by_nhs_number": "",
            "primary_care_provider": "A00001",
            "primary_care_provider_eff_from_date": "",
            "name_prefix": "MS",
            "given_name": "ADDIEN",
            "other_given_names": "PADERAU",
            "family_name": "DIMOCK",
            "previous_family_name": "",
            "birth_date": "19801209",
            "gender_code": 2,
            "address_line_1": "1 NEWSTEAD AVENUE",
            "address_line_2": "NEWARK",
            "address_line_3": "NOTTS",
            "address_line_4": "",
            "address_line_5": "",
            "postcode": "NG2 1ND",
            "usual_address_eff_from_date": "20070723",
            "death_date": "",
            "telephone_number_home": "",
            "telephone_number_home_eff_from_date": "",
            "telephone_number_mobile": "",
            "telephone_number_mobile_eff_from_date": "",
            "email_address_home": "",
            "email_address_home_eff_from_date": "",
            "preferred_language": "",
            "interpreter_required": 0,
            "reason_for_removal": "",
            "reason_removal_eff_from_date": "",
        },
        {
            "request_id": "2f153e68-b4f3-45f2-a85d-14b0d1eb22cc",
            "nhs_number": "9011000042",
            "superseded_by_nhs_number": "",
            "primary_care_provider": "A00001",
            "primary_care_provider_eff_from_date": "20000101",
            "name_prefix": "Dr.",
            "given_name": "Miguelina",
            "other_given_names": "Raul",
            "family_name": "Bednar",
            "previous_family_name": "Olson",
            "birth_date": "19700702",
            "gender_code": 2,
            "address_line_1": "825",
            "address_line_2": "71354 Monahan Squares",
            "address_line_3": "Lake Jamieside",
            "address_line_4": "Arkansas",
            "address_line_5": "Burundi",
            "postcode": "EU1 8LN",
            "usual_address_eff_from_date": "20000101",
            "death_date": "",
            "telephone_number_home": "70846 280 941",
            "telephone_number_home_eff_from_date": "20000101",
            "telephone_number_mobile": "70103 024 555",
            "telephone_number_mobile_eff_from_date": "20000101",
            "email_address_home": "dltlhagqn3229@test.com",
            "email_address_home_eff_from_date": "20000101",
            "preferred_language": "en",
            "interpreter_required": 1,
            "reason_for_removal": "",
            "reason_removal_eff_from_date": "",
        },
    ]
    # Retrieve data from the DB using the request_id from stub data
    expected = stub_data_update[1]
    db_result = get_latest_records_by_nhs_number(db_util, expected["nhs_number"], 2)
    updated = db_result.to_dict("records")[0]

    assert (
        str(updated["message_id"]) == expected["request_id"]
    ), "field not matched: request_id"
    wait_for_assertion(
        lambda: fetch_pi_changes_column_value(db_util, nhs_number, "state")
        == "PROCESSED"
    )
    assert updated["address_line_1"] == expected["address_line_1"]
    assert updated["telephone_number_home"] == expected.get("telephone_number_home")
    assert updated["telephone_number_mobile"] == expected.get("telephone_number_mobile")


# TC-11
@pytest.mark.tc11
def test_where_nhs_num_exists_superseded_nhs_num_does_not_exists(
    db_util: DbUtil, page: Page, user_tools: UserTools
) -> None:
    """
    Test to when the subjects record for the NHS number is updated with the superseded NHS number received within the message,
    No new subject record is created
    """
    nhs_number_before = "9007007228"
    superseded_nhs_number = "9011100042"
    assert subject_count_by_nhs_number(db_util, nhs_number_before, "subjects") == 1
    assert subject_count_by_nhs_number(db_util, superseded_nhs_number, "subjects") == 0
    prev_subject_audit_count = subject_count_by_nhs_number(
        db_util, superseded_nhs_number, "audit_subjects"
    )

    # Insert data
    message_id = "ffffffff-ffff-ffff-ffff-ffffffffff11"
    insert_data(db_util, message_id)

    trigger_lambda_and_verify_success(1)

    stub_data = {
        "request_id": "33ccaa03-9e8e-4aad-a14d-f25d697dcb3a",
        "participant_id": 11,
        "nhs_number": "9007007228",
        "superseded_by_nhs_number": "9011100042",
        "primary_care_provider": "A00020",
        "primary_care_provider_eff_from_date": "",
        "name_prefix": "Mrs",
        "given_name": "Harriet",
        "other_given_names": "",
        "family_name": "COLE",
        "previous_family_name": "",
        "birth_date": "19491003",
        "gender_code": 2,
        "address_line_1": "56",
        "address_line_2": "Eastcliffe Road",
        "address_line_3": "Eastcliffe Crescent",
        "address_line_4": "Bristol",
        "address_line_5": "Avon",
        "postcode": "BR20 4RD",
        "usual_address_eff_from_date": "20070723",
        "death_date": "",
        "telephone_number_home": "",
        "telephone_number_home_eff_from_date": "",
        "telephone_number_mobile": "",
        "telephone_number_mobile_eff_from_date": "",
        "email_address_home": "",
        "email_address_home_eff_from_date": "",
        "preferred_language": "",
        "interpreter_required": 0,
        "reason_for_removal": "",
        "reason_removal_eff_from_date": "",
    }

    db_result = get_latest_record_by_request_id(db_util, stub_data["request_id"])
    inserted = db_result.to_dict("records")[0]
    # Perform the assertion to compare stub data and DB data
    assert (
        str(inserted["message_id"]) == stub_data["request_id"]
    ), "field not matched: request_id"
    wait_for_assertion(
        lambda: fetch_pi_changes_column_value(db_util, nhs_number_before, "state")
        == "PROCESSED"
    )
    wait_for_assertion(
        lambda: subject_count_by_nhs_number(db_util, nhs_number_before, "subjects") == 0
    )
    wait_for_assertion(
        lambda: subject_count_by_nhs_number(db_util, superseded_nhs_number, "subjects")
        == 1
    )
    wait_for_assertion(
        lambda: subject_count_by_nhs_number(
            db_util, superseded_nhs_number, "audit_subjects"
        )
        == prev_subject_audit_count + 1
    )
    # UI assertions
    # Logged into BSS_SO1
    user_tools.user_login(page, "BSO User1 - BS1")
    page.goto("/bss/subjects", wait_until="domcontentloaded")
    page.locator("//a[text()='Subject Search']").click()
    page.locator("#nhsNumberFilter input").fill(nhs_number_before)
    page.locator("#nhsNumberFilter input").press("Enter")
    expect(page.locator("text=No matching records found")).to_be_visible()
    page.locator("#nhsNumberFilter input").fill(superseded_nhs_number)
    page.locator("#nhsNumberFilter input").press("Enter")
    expect(page.locator("//td[text()='901 110 0042']")).to_be_visible()


# TC-12
# @pytest.mark.tc12
def test_where_nhs_num_and_superseded_nhs_num_both_does_exists(
    db_util: DbUtil, page: Page, user_tools: UserTools
) -> None:
    """
    Test for when nhs_number and superseded_by_nhs number both exists in the Subjects table
    """
    nhs_number_before = "9007007227"
    assert subject_count_by_nhs_number(db_util, nhs_number_before, "subjects") == 1

    superseded_nhs_number = "9100070464"
    assert subject_count_by_nhs_number(db_util, superseded_nhs_number, "subjects") == 1
    prev_subject_audit_count = subject_count_by_nhs_number(
        db_util, superseded_nhs_number, "audit_subjects"
    )
    prev_subject = fetch_latest_record_by_nhs_number(
        db_util, superseded_nhs_number, "subjects", "transaction_db_date_time"
    )

    # Insert data
    message_id = "ffffffff-ffff-ffff-ffff-ffffffffff12"
    insert_data(db_util, message_id)
    trigger_lambda_and_verify_success(1)

    stub_data = {
        "request_id": "33ccaa03-9e8e-4abd-a14d-f25d697dbb3b",
        "participant_id": 12,
        "nhs_number": "9007007227",
        "superseded_by_nhs_number": "9100070464",
        "primary_care_provider": "A00020",
        "primary_care_provider_eff_from_date": "20000101",
        "name_prefix": "Mrs",
        "given_name": "Felicity ",
        "other_given_names": "",
        "family_name": "COLE",
        "previous_family_name": "",
        "birth_date": "19500403",
        "gender_code": 2,
        "address_line_1": "55",
        "address_line_2": "Eastcliffe Road",
        "address_line_3": "Eastcliffe Crescent",
        "address_line_4": "Bristol",
        "address_line_5": "Avon",
        "postcode": "BR20 4RD",
        "usual_address_eff_from_date": "",
        "death_date": "",
        "telephone_number_home": "",
        "telephone_number_home_eff_from_date": "",
        "telephone_number_mobile": "",
        "telephone_number_mobile_eff_from_date": "",
        "email_address_home": "",
        "email_address_home_eff_from_date": "",
        "preferred_language": "en",
        "interpreter_required": 1,
        "reason_for_removal": "",
        "reason_removal_eff_from_date": "",
    }

    db_result = get_latest_record_by_request_id(db_util, stub_data["request_id"])
    inserted = db_result.to_dict("records")[0]
    # Perform the assertion to compare stub data and DB data
    assert (
        str(inserted["message_id"]) == stub_data["request_id"]
    ), "field not matched: request_id"
    wait_for_assertion(
        lambda: fetch_pi_changes_column_value(db_util, nhs_number_before, "state")
        == "PROCESSED"
    )
    wait_for_assertion(
        lambda: subject_count_by_nhs_number(db_util, nhs_number_before, "subjects") == 1
    )
    wait_for_assertion(
        lambda: fetch_latest_removal_reason(db_util, nhs_number_before, "subjects")
        == "NOT_PROVIDED"
    )
    wait_for_assertion(
        lambda: fetch_latest_removal_reason(db_util, superseded_nhs_number, "subjects")
        is None
    )
    wait_for_assertion(
        lambda: subject_count_by_nhs_number(db_util, superseded_nhs_number, "subjects")
        == 1
    )
    wait_for_assertion(
        lambda: subject_count_by_nhs_number(
            db_util, superseded_nhs_number, "audit_subjects"
        )
        == prev_subject_audit_count
    )
    # Assering no change in the superseded_nhs participant data
    after_subject = fetch_latest_record_by_nhs_number(
        db_util, superseded_nhs_number, "subjects", "transaction_db_date_time"
    )
    assert after_subject.equals(prev_subject)
    # UI assertions
    # Logged into BSS_SO1
    user_tools.user_login(page, "BSO User1 - BS1")
    page.goto("/bss/subjects", wait_until="domcontentloaded")
    page.locator("//a[text()='Subject Search']").click()
    page.locator("#nhsNumberFilter input").fill(nhs_number_before)
    page.locator("#nhsNumberFilter input").press("Enter")
    expect(page.locator("//td[text()='900 700 7227']")).to_be_visible()
    page.locator("#nhsNumberFilter input").fill(superseded_nhs_number)
    page.locator('//th[@id="bsoFilter"]//input').fill("")
    page.locator("#nhsNumberFilter input").press("Enter")
    expect(page.locator("//td[text()='910 007 0464']")).to_be_visible()


# TC-13
@pytest.mark.tc13
def test_where_nhs_num_and_superseded_nhs_num_both_does_not_exists(
    db_util: DbUtil, page: Page, user_tools: UserTools
) -> None:
    """
    Test for when nhs_number and superseded_by_nhs number both does NOT exists in the Subjects table
    """
    nhs_number_before = "9007117227"
    assert subject_count_by_nhs_number(db_util, nhs_number_before, "subjects") == 0

    superseded_nhs_number = "9006116227"
    assert subject_count_by_nhs_number(db_util, superseded_nhs_number, "subjects") == 0
    prev_subject_audit_count = subject_count_by_nhs_number(
        db_util, superseded_nhs_number, "audit_subjects"
    )

    # Insert data
    message_id = "ffffffff-ffff-ffff-ffff-ffffffffff13"
    insert_data(db_util, message_id)
    trigger_lambda_and_verify_success(1)

    stub_data = {
        "request_id": "33ccaa03-9e8e-4bbd-a14d-f25d697dbb3c",
        "participant_id": 13,
        "nhs_number": "9007117227",
        "superseded_by_nhs_number": "9006116227",
        "primary_care_provider": "A00002",
        "primary_care_provider_eff_from_date": "",
        "name_prefix": "Mrs",
        "given_name": "Tina",
        "other_given_names": "",
        "family_name": "Test",
        "previous_family_name": "",
        "birth_date": "19701201",
        "gender_code": 2,
        "address_line_1": "The House",
        "address_line_2": "Bakerstreet",
        "address_line_3": "London",
        "address_line_4": "UK",
        "address_line_5": "",
        "postcode": "EX8 1AA",
        "usual_address_eff_from_date": "20070723",
        "death_date": "",
        "telephone_number_home": "",
        "telephone_number_home_eff_from_date": "",
        "telephone_number_mobile": "",
        "telephone_number_mobile_eff_from_date": "",
        "email_address_home": "",
        "email_address_home_eff_from_date": "",
        "preferred_language": "",
        "interpreter_required": 0,
        "reason_for_removal": "",
        "reason_removal_eff_from_date": "",
    }

    db_result = get_latest_record_by_request_id(db_util, stub_data["request_id"])
    inserted = db_result.to_dict("records")[0]
    # Perform the assertion to compare stub data and DB data
    assert (
        str(inserted["message_id"]) == stub_data["request_id"]
    ), "field not matched: request_id"
    wait_for_assertion(
        lambda: fetch_pi_changes_column_value(db_util, nhs_number_before, "state")
        == "PROCESSED"
    )
    wait_for_assertion(
        lambda: subject_count_by_nhs_number(db_util, nhs_number_before, "subjects") == 0
    )
    wait_for_assertion(
        lambda: subject_count_by_nhs_number(db_util, superseded_nhs_number, "subjects")
        == 1
    )
    wait_for_assertion(
        lambda: subject_count_by_nhs_number(
            db_util, superseded_nhs_number, "audit_subjects"
        )
        == prev_subject_audit_count + 1
    )
    # UI assertions
    # Logged into BSS_SO1
    user_tools.user_login(page, "BSO User1 - BS1")
    page.goto("/bss/subjects", wait_until="domcontentloaded")
    page.locator("//a[text()='Subject Search']").click()
    page.locator("#nhsNumberFilter input").fill(nhs_number_before)
    page.locator("#nhsNumberFilter input").press("Enter")
    expect(page.locator("text=No matching records found")).to_be_visible()
    page.locator("#nhsNumberFilter input").fill(superseded_nhs_number)
    page.locator("#nhsNumberFilter input").press("Enter")
    expect(page.locator("//td[text()='900 611 6227']")).to_be_visible()


# TC-14
# @pytest.mark.tc14
def test_where_nhs_num_does_not_exists_superseded_nhs_num_exists(
    db_util: DbUtil, page: Page, user_tools: UserTools
) -> None:
    """
    Test for when nhs_number does NOT and superseded_by_nhs number both exists in the Subjects table
    """
    nhs_number_before = "9005114227"
    assert subject_count_by_nhs_number(db_util, nhs_number_before, "subjects") == 0

    superseded_nhs_number = "9007007226"
    assert subject_count_by_nhs_number(db_util, superseded_nhs_number, "subjects") == 1
    prev_subject_audit_count = subject_count_by_nhs_number(
        db_util, superseded_nhs_number, "audit_subjects"
    )

    # Insert data
    message_id = "ffffffff-ffff-ffff-ffff-ffffffffff14"
    insert_data(db_util, message_id)
    trigger_lambda_and_verify_success(1)

    stub_data = {
        "request_id": "33ccaa03-9e8e-4aad-a14d-f25d697dbb3d",
        "participant_id": 14,
        "nhs_number": "9005114227",
        "superseded_by_nhs_number": "9007007226",
        "primary_care_provider": "A00002",
        "primary_care_provider_eff_from_date": "",
        "name_prefix": "Mrs",
        "given_name": "Emily",
        "other_given_names": "",
        "family_name": "Test",
        "previous_family_name": "",
        "birth_date": "19771111",
        "gender_code": 2,
        "address_line_1": "Emily's House",
        "address_line_2": "Bakerstreet",
        "address_line_3": "London",
        "address_line_4": "UK",
        "address_line_5": "",
        "postcode": "EX8 1AA",
        "usual_address_eff_from_date": "20070723",
        "death_date": "",
        "telephone_number_home": "",
        "telephone_number_home_eff_from_date": "",
        "telephone_number_mobile": "",
        "telephone_number_mobile_eff_from_date": "",
        "email_address_home": "",
        "email_address_home_eff_from_date": "",
        "preferred_language": "",
        "interpreter_required": 0,
        "reason_for_removal": "",
        "reason_removal_eff_from_date": "",
    }

    db_result = get_latest_record_by_request_id(db_util, stub_data["request_id"])
    inserted = db_result.to_dict("records")[0]
    # Perform the assertion to compare stub data and DB data
    assert (
        str(inserted["message_id"]) == stub_data["request_id"]
    ), "field not matched: request_id"
    wait_for_assertion(
        lambda: fetch_pi_changes_column_value(db_util, nhs_number_before, "state")
        == "PROCESSED"
    )
    wait_for_assertion(
        lambda: subject_count_by_nhs_number(db_util, nhs_number_before, "subjects") == 0
    )
    wait_for_assertion(
        lambda: subject_count_by_nhs_number(db_util, superseded_nhs_number, "subjects")
        == 1
    )
    wait_for_assertion(
        lambda: subject_count_by_nhs_number(
            db_util, superseded_nhs_number, "audit_subjects"
        )
        == prev_subject_audit_count
    )
    # UI assertions
    # Logged into BSS_SO1
    user_tools.user_login(page, "BSO User1 - BS1")
    page.goto("/bss/subjects", wait_until="domcontentloaded")
    page.locator("//a[text()='Subject Search']").click()
    page.locator("#nhsNumberFilter input").fill(nhs_number_before)
    page.locator("#nhsNumberFilter input").press("Enter")
    expect(page.locator("text=No matching records found")).to_be_visible()
    page.locator("#nhsNumberFilter input").fill(superseded_nhs_number)
    page.locator("#nhsNumberFilter input").press("Enter")
    expect(page.locator("//td[text()='900 700 7226']")).to_be_visible()


# TC-15, 16, 17
@pytest.mark.tc15
def test_death_date_and_reason_for_reamoval_populated_using_dummy_GP_practice_code_pi_changes_gp_practice_code_is_Null_with_reason_for_removal(
    db_util: DbUtil,
) -> None:
    """
    15 = Test to verify death_date and reason_for_reamoval is populated
    16 = Test using dummy GP_practice_code = ZZZLED
    17 = Test with where pi_changes.gp_practice_code = Null and with a reason_for_removal
    """
    nhs_number_15 = "9000019463"
    nhs_number_16 = "9007007216"
    nhs_number_17 = "9000018196"

    assert fetch_subject_column_value(db_util, nhs_number_15, "removal_reason") is None
    assert fetch_subject_column_value(db_util, nhs_number_16, "gp_practice_id") == 20
    assert fetch_subject_column_value(db_util, nhs_number_17, "removal_reason") is None

    # Inserted reason_for_removal data
    message_id = "ffffff15-ff16-ff17-ffff-fffffffffff2"
    insert_data(db_util, message_id)
    trigger_lambda_and_verify_success(3)

    stub_data_with_reasons = [
        {
            "request_id": "24fec7a0-98eb-4cf1-a4bd-a9bc60105f51",
            "participant_id": 15,
            "nhs_number": nhs_number_15,
            "death_date": "20090909",
            "reason_for_removal": "D",
            "reason_removal_eff_from_date": "20090909",
        },
        {
            "request_id": "24fec7a0-98eb-4cf1-a4bd-a9bc60105f51",
            "participant_id": 16,
            "nhs_number": nhs_number_16,
            "primary_care_provider": "ZZZLED",
        },
        {
            "request_id": "24fec7a0-98eb-4cf1-a4bd-a9bc60105f51",
            "participant_id": 17,
            "nhs_number": nhs_number_17,
            "primary_care_provider": "",
            "reason_for_removal": "R",
        },
    ]
    db_result = get_latest_record_by_request_id(
        db_util, stub_data_with_reasons[0]["request_id"]
    )
    inserted_data = db_result.to_dict("records")[0]
    # Perform the assertion to compare stub data and DB data
    assert (
        str(inserted_data["message_id"]) == stub_data_with_reasons[0]["request_id"]
    ), "field not matched: request_id"
    wait_for_assertion(
        lambda: fetch_pi_changes_column_value(db_util, nhs_number_15, "state")
        == "PROCESSED"
    )
    wait_for_assertion(
        lambda: fetch_pi_changes_column_value(db_util, nhs_number_16, "state")
        == "PROCESSED"
    )
    wait_for_assertion(
        lambda: fetch_pi_changes_column_value(db_util, nhs_number_17, "state")
        == "PROCESSED"
    )

    assert (
        fetch_subject_column_value(db_util, nhs_number_15, "removal_reason") == "DEATH"
    )
    assert (
        fetch_subject_column_value(db_util, nhs_number_16, "gp_practice_id") == 100032
    )  # todo add UI assertions
    assert (
        fetch_subject_column_value(db_util, nhs_number_17, "removal_reason")
        == "REMOVAL"
    )
    assert fetch_subject_column_value(db_util, nhs_number_17, "gp_practice_id") is None


#################### CM Lambda Neagtive/NFR tests ####################
# TC-16
def test_status_401(db_util: DbUtil) -> None:
    """
    trigger_lambda_with_python and assert the status of 401
    """
    # Insert data & verify the error message(lambda response)
    message_id = "ffffffff-ffff-ffff-ffff-fffffffff401"
    insert_data(db_util, message_id)
    trigger_lambda_and_verify_error(
        "The request to https://bss2-1381.nonprod.breast-screening-select.nhs.uk/bss/cohortManager had a HTTP error: 401 Client Error:  for url: https://bss2-1381.nonprod.breast-screening-select.nhs.uk/bss/cohortManager?screeningServiceId=1&rowCount=500&requestId=ffffffff-ffff-ffff-ffff-fffffffff401"
    )


# TC-17
def test_status_403(db_util: DbUtil) -> None:
    """
    trigger_lambda_with_python and assert the status of 403
    """
    # Insert data & verify the error message(lambda response)
    message_id = "ffffffff-ffff-ffff-ffff-fffffffff403"
    insert_data(db_util, message_id)
    trigger_lambda_and_verify_error(
        "The request to https://bss2-1381.nonprod.breast-screening-select.nhs.uk/bss/cohortManager had a HTTP error: 403 Client Error:  for url: https://bss2-1381.nonprod.breast-screening-select.nhs.uk/bss/cohortManager?screeningServiceId=1&rowCount=500&requestId=ffffffff-ffff-ffff-ffff-fffffffff403"
    )


# TC-18
def test_status_404(db_util: DbUtil) -> None:
    """
    trigger_lambda_with_python and assert the status of 404
    """
    # Insert data & verify the error message(lambda response)
    message_id = "ffffffff-ffff-ffff-ffff-fffffffff404"
    insert_data(db_util, message_id)
    trigger_lambda_and_verify_error(
        "The request to https://bss2-1381.nonprod.breast-screening-select.nhs.uk/bss/cohortManager had a HTTP error: 404 Client Error:  for url: https://bss2-1381.nonprod.breast-screening-select.nhs.uk/bss/cohortManager?screeningServiceId=1&rowCount=500&requestId=ffffffff-ffff-ffff-ffff-fffffffff404"
    )


# TC-20
def test_status_500(db_util: DbUtil) -> None:
    """
    trigger_lambda_with_python and assert the status of 500
    """
    # Insert data & verify the error message(lambda response)
    message_id = "ffffffff-ffff-ffff-ffff-fffffffff500"
    insert_data(db_util, message_id)
    trigger_lambda_and_verify_error(
        "The request to https://bss2-1381.nonprod.breast-screening-select.nhs.uk/bss/cohortManager had a HTTP error: 500 Server Error:  for url: https://bss2-1381.nonprod.breast-screening-select.nhs.uk/bss/cohortManager?screeningServiceId=1&rowCount=500&requestId=ffffffff-ffff-ffff-ffff-fffffffff500"
    )


#####################################################

# Methods #


#####################################################
# Function to invoke AWS Lambda
def invoke_lambda(function_name, payload, region="eu-west-2") -> dict:
    """
    Invokes an AWS Lambda function and validates the response.
    """
    # Initialize the Lambda
    session = boto3.Session(profile_name="bs-select-rw-user-730319765130")
    lambda_client = session.client("lambda", region_name=region)
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )
    response_payload = json.loads(response["Payload"].read())
    return response_payload


def insert_data(db_util, message_id) -> None:
    insert_query = """INSERT INTO pi_changes (inserted_date_time, message_id) values (current_timestamp, %s)"""
    params = (message_id,)
    db_util.insert(insert_query, params)


def trigger_lambda_and_verify_success(inserted) -> None:
    trigger_lambda_and_verify_status("success", str(inserted))


def trigger_lambda_and_verify_error(message) -> None:
    trigger_lambda_and_verify_status("error", status_message=message)


def trigger_lambda_and_verify_status(
    status_text, inserted="", status_message=""
) -> None:
    lambda_function_name = "bs-select-cohort-bss-cm-integration"  # Lambda function name
    lambda_payload = {}
    response = invoke_lambda(lambda_function_name, lambda_payload)
    assert (
        response.get("status") == status_text
    ), "Lambda did not return expected status!"
    if inserted:
        assert (
            str(response.get("inserted")) == inserted
        ), "Lambda did not return expected inserted count!"
    if status_message:
        assert (
            str(response.get("message")) == status_message
        ), "Lambda did not return expected status!"


# Retrieve data from the DB based on the request_id
def get_latest_record_by_request_id(db_conn, message_id) -> DataFrame | None:
    query = """SELECT message_id, nhs_number, state, name_prefix, family_name, first_name, other_names, previous_family_name, date_of_birth, date_of_death,
        gender_code, address_line_1, address_line_2, address_line_3, address_line_4, address_line_5, postcode, gp_practice_code, nhais_cipher,
        nhais_deduction_reason, nhais_deduction_date, replaced_nhs_number, superseded_by_nhs_number, processed_date_time, person_application_feed_id,
        transaction_id, transaction_app_date_time, transaction_user_org_role_id, telephone_number_home, telephone_number_mobile,
        email_address_home, preferred_language, interpreter_required, usual_address_eff_from_date, tel_number_home_eff_from_date, tel_number_mob_eff_from_date,
        email_addr_home_eff_from_date FROM pi_changes WHERE message_id = %s ORDER BY inserted_date_time DESC limit 1"""
    return db_conn.get_results(query, [message_id])


def get_latest_records_by_nhs_number(db_conn, nhs_number, limit) -> DataFrame | None:
    query = """SELECT * FROM pi_changes WHERE nhs_number=%s ORDER BY inserted_date_time DESC limit %s"""
    return db_conn.get_results(query, [nhs_number, limit])


def wait_for_assertion(assert_func, timeout=90, interval=3):
    end_time = time.time() + timeout

    counter = 0
    while time.time() < end_time:
        counter += 1
        if assert_func():
            return
        time.sleep(interval)

    result = assert_func()
    assert result, "Expected TRUE"


def fetch_latest_removal_reason(db_util, nhs_number, table_name):
    return fetch_latest_record_by_nhs_number(
        db_util, nhs_number, table_name, "transaction_db_date_time"
    )["removal_reason"][0]


def fetch_latest_record_by_nhs_number(
    db_util, nhs_number, table_name, order_by_field
) -> DataFrame:
    query = f"""SELECT * FROM {table_name} WHERE nhs_number = %s order by {order_by_field} desc limit 1"""
    df = db_util.get_results(query, [nhs_number])
    return df


def fetch_pi_changes_column_value(db_util, nhs_number, table_column):
    query = f"""SELECT {table_column} FROM pi_changes WHERE nhs_number = %s order by inserted_date_time desc limit 1"""
    df = db_util.get_results(query, [nhs_number])
    # Extract the column value
    column_value = df[table_column][0]
    return column_value
