import pytest
from playwright.sync_api import Page
from pages.logout.log_out_page import LogoutPage
from pages.base_page import BasePage
from pages.screening_practitioner_appointments.screening_practitioner_appointments_page import (
    ScreeningPractitionerAppointmentsPage,
)
from pages.screening_practitioner_appointments.set_availability_page import (
    SetAvailabilityPage,
)
from pages.screening_practitioner_appointments.practitioner_availability_page import (
    PractitionerAvailabilityPage,
)
from pages.screening_practitioner_appointments.colonoscopy_assessment_appointments_page import (
    ColonoscopyAssessmentAppointmentsPage,
)
from pages.screening_practitioner_appointments.book_appointment_page import (
    BookAppointmentPage,
)
from pages.screening_subject_search.subject_screening_summary_page import (
    SubjectScreeningSummaryPage,
)
from pages.screening_subject_search.episode_events_and_notes_page import (
    EpisodeEventsAndNotesPage,
)
from utils.user_tools import UserTools
from utils.load_properties_file import PropertiesFile
from utils.calendar_picker import CalendarPicker
from utils.batch_processing import batch_processing
from datetime import datetime
from utils.oracle.oracle_specific_functions import get_subjects_for_appointments
from utils.nhs_number_tools import NHSNumberTools
import logging


@pytest.fixture
def smokescreen_properties() -> dict:
    return PropertiesFile().get_smokescreen_properties()


@pytest.mark.vpn_required
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

    subjects_df = get_subjects_for_appointments(
        smokescreen_properties["c4_eng_number_of_appointments_to_book"]
    )

    logging.info(
        f"Compartment 4 - Setting up appointments for {smokescreen_properties["c4_eng_weeks_to_make_available"]} Weeks"
    )
    UserTools.user_login(page, "Screening Centre Manager at BCS001")
    BasePage(page).go_to_screening_practitioner_appointments_page()
    ScreeningPractitionerAppointmentsPage(page).go_to_set_availability_page()
    SetAvailabilityPage(page).go_to_practitioner_availability_page()
    PractitionerAvailabilityPage(page).select_site_dropdown_option(
        smokescreen_properties["c4_eng_site_name1"]
    )
    PractitionerAvailabilityPage(page).select_practitioner_dropdown_option(
        smokescreen_properties["c4_eng_practitioner_name"]
    )
    PractitionerAvailabilityPage(page).click_calendar_button()
    CalendarPicker(page).select_day(datetime.today())
    PractitionerAvailabilityPage(page).click_show_button()
    PractitionerAvailabilityPage(page).enter_start_time("09:00")
    PractitionerAvailabilityPage(page).enter_end_time("17:15")
    PractitionerAvailabilityPage(page).click_calculate_slots_button()
    PractitionerAvailabilityPage(page).enter_number_of_weeks(
        smokescreen_properties["c4_eng_weeks_to_make_available"]
    )
    PractitionerAvailabilityPage(page).click_save_button()
    PractitionerAvailabilityPage(page).slots_updated_message_is_displayed(
        f"Slots Updated for {smokescreen_properties["c4_eng_weeks_to_make_available"]} Weeks"
    )
    LogoutPage(page).log_out(close_page=False)

    logging.info(
        f"Compartment 4 - Booking {smokescreen_properties["c4_eng_number_of_appointments_to_book"]} subjects to appointments"
    )
    ScreeningPractitionerAppointmentsPage(page).go_to_log_in_page()
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")

    BasePage(page).go_to_screening_practitioner_appointments_page()
    ScreeningPractitionerAppointmentsPage(page).go_to_patients_that_require_page()

    for subject_num in range(
        int(smokescreen_properties["c4_eng_number_of_appointments_to_book"])
    ):
        nhs_number = subjects_df["subject_nhs_number"].iloc[subject_num]
        logging.info(f"Booking appointment for: {nhs_number}")

        nhs_number_spaced = NHSNumberTools().spaced_nhs_number(nhs_number)
        ColonoscopyAssessmentAppointmentsPage(page).filter_by_nhs_number(nhs_number)
        ColonoscopyAssessmentAppointmentsPage(page).click_nhs_number_link(
            nhs_number_spaced
        )
        BookAppointmentPage(page).select_screening_centre_dropdown_option(
            smokescreen_properties["c4_eng_centre_name"]
        )
        BookAppointmentPage(page).select_site_dropdown_option(
            [
                f"{smokescreen_properties["c4_eng_site_name2"]} (? km)",
                f"{smokescreen_properties["c4_eng_site_name2"]} (? km) (attended)",
            ]
        )

        current_month_displayed = BookAppointmentPage(
            page
        ).get_current_month_displayed()
        CalendarPicker(page).book_first_eligble_appointment(
            current_month_displayed,
            BookAppointmentPage(page).appointment_cell_locators,
            [
                BookAppointmentPage(page).available_background_colour,
                BookAppointmentPage(page).some_available_background_colour,
            ],
        )
        BookAppointmentPage(page).appointments_table.click_first_input_in_column(
            "Appt/Slot Time"
        )
        BasePage(page).safe_accept_dialog(BookAppointmentPage(page).save_button)
        try:
            BookAppointmentPage(page).appointment_booked_confirmation_is_displayed(
                "Appointment booked"
            )
            logging.info(f"Appointment successfully booked for: {nhs_number}")
        except Exception as e:
            pytest.fail(f"Appointment not booked successfully: {e}")
        BasePage(page).click_back_button()
    ColonoscopyAssessmentAppointmentsPage(page).wait_for_page_header()

    logging.info("Compartment 4 - Sending out appointment invitations")
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

    SubjectScreeningSummaryPage(page).expand_episodes_list()
    SubjectScreeningSummaryPage(page).click_first_fobt_episode_link()
    EpisodeEventsAndNotesPage(page).expected_episode_event_is_displayed(
        "A167 - GP Abnormal FOBT Result Sent"
    )
    LogoutPage(page).log_out()
