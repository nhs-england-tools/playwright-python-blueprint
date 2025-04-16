import logging
import pytest
from playwright.sync_api import Page, expect
from pages.logout.log_out_page import Logout
from pages.base_page import BasePage
from utils.user_tools import UserTools
from utils.load_properties_file import PropertiesFile
from utils.calendar_picker import CalendarPicker
from utils.batch_processing import batch_processing
from datetime import datetime


@pytest.fixture
def smokescreen_properties() -> dict:
    return PropertiesFile().get_smokescreen_properties()


@pytest.mark.smokescreen
@pytest.mark.compartment4
def test_compartment_4(page: Page, smokescreen_properties: dict) -> None:
    """
    This is the main compartment 4 method
    First it obtains the necessary test data from the DB
    Then it logs on as a Screening Centre Manager and sets the availablity of a practitioner from 09:00 to 17:15 from todays date for the next 6 weeks
    After It logs out an logs back in as a Hub Manager
    Once logging back in it books appointments for the subjects retrieved earlier
    Finally it processes the necessary batches to send out the letters and checks the subjects satus has been updated to what is expected
    """

    # Add method of getting test data using the query below. To remove once subject retrieval logic is created
    """select tk.kitid, ss.subject_nhs_number, se.screening_subject_id
    from tk_items_t tk
    inner join ep_subject_episode_t se on se.screening_subject_id = tk.screening_subject_id
    inner join screening_subject_t ss on ss.screening_subject_id = se.screening_subject_id
    inner join sd_contact_t c on c.nhs_number = ss.subject_nhs_number
    where se.latest_event_status_id = 11132
    and tk.logged_in_flag = 'Y'
    and se.episode_status_id = 11352
    and ss.screening_status_id != 4008
    and tk.logged_in_at = 23159
    and c.hub_id = 23159
    and tk.tk_type_id = 2
    and tk.datestamp > add_months(sysdate,-24)
    order by ss.subject_nhs_number desc"""

    UserTools.user_login(page, "Screening Centre Manager at BCS001")
    BasePage(page).go_to_screening_practitioner_appointments_page()
    page.get_by_role("link", name="Set Availability").click()
    page.get_by_role("link", name="Practitioner Availability -").click()
    page.locator("#UI_SITE_ID").select_option(index=1)
    page.locator("#UI_PRACTITIONER_ID").select_option(index=1)
    page.get_by_role("button", name="Calendar").click()
    CalendarPicker(page).select_day(
        datetime.today()
    )  # This will make it so that we can only run this test once a day, or we need to restore the DB back to the snapshot
    page.get_by_role("button", name="Show").dblclick()
    page.get_by_role("textbox", name="From:").click()
    page.get_by_role("textbox", name="From:").fill("09:00")
    page.get_by_role("textbox", name="To:").click()
    page.get_by_role("textbox", name="To:").fill("17:15")
    page.get_by_role("button", name="Calculate Slots").click()
    page.locator("#FOR_WEEKS").click()
    page.locator("#FOR_WEEKS").fill("6")
    page.locator("#FOR_WEEKS").press("Enter")
    page.get_by_role("button", name="Save").click()
    expect(page.get_by_text("Slots Updated for 6 Weeks")).to_be_visible()
    Logout(page).log_out()

    page.get_by_role("button", name="Log in").click()
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")
    BasePage(page).go_to_screening_practitioner_appointments_page()
    page.get_by_role("link", name="Patients that Require").click()
    # Add for loop to loop x times (depends on how many we want to run it for) 70 - 79
    page.locator("#nhsNumberFilter").click()
    page.locator("#nhsNumberFilter").fill("9991406131")
    page.locator("#nhsNumberFilter").press("Enter")
    page.get_by_role("link", name="999 140 6131").click()
    page.get_by_label("Screening Centre ( All)").select_option("23162")
    page.locator("#UI_NEW_SITE").select_option("42808")
    page.locator('input[name="fri2"]').click()  # Todays date if available
    page.locator("#UI_NEW_SLOT_SELECTION_ID_359119").check()
    page.get_by_role("button", name="Save").click()
    expect(page.get_by_text("Appointment booked")).to_be_visible()

    batch_processing(
        page,
        "A183",
        "Practitioner Clinic 1st Appointment",
        "A25 - 1st Colonoscopy Assessment Appointment Booked, letter sent",
    )

    batch_processing(
        page,
        "A183",
        "GP Result (Abnormal)",
        "A25 - 1st Colonoscopy Assessment Appointment Booked, letter sent",
    )
    page.locator("#ID_LINK_EPISODES_img").click()
    page.get_by_role("link", name="FOBT Screening").click()
    expect(
        page.get_by_role("cell", name="A167 - GP Abnormal FOBT Result Sent", exact=True)
    ).to_be_visible()
    Logout(page).log_out()
