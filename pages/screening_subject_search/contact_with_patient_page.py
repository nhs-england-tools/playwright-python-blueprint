from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.calendar_picker import CalendarPicker
from datetime import datetime


class ContactWithPatientPage(BasePage):
    """
    ContactWithPatientPage class for interacting with 'Contact With Patient' page elements.
    """

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # Contact With Patient - Page Locators
        self.contact_direction_dropdown = self.page.locator("#UI_DIRECTION")
        self.contact_made_between_patient_and_dropdown = self.page.locator(
            "#UI_CALLER_ID"
        )
        self.calendar_button = self.page.get_by_role("button", name="Calendar")
        self.start_time_field = self.page.locator("#UI_START_TIME")
        self.end_time_field = self.page.locator("#UI_END_TIME")
        self.discussion_record_text_field = self.page.locator("#UI_COMMENT_ID")
        self.outcome_dropdown = self.page.locator("#UI_OUTCOME")
        self.save_button = self.page.get_by_role("button", name="Save")
        self.patient_contacted_dropdown = self.page.locator("#UI_PATIENT_CONTACTED")

    def select_direction_dropdown_option(self, direction: str) -> None:
        """
        Select an option from the 'Direction' dropdown by its label.

        Args:
        direction (str): The label of the direction option to select.
        """
        self.contact_direction_dropdown.select_option(label=direction)

    def select_caller_id_dropdown_index_option(self, index_value: int) -> None:
        """
        Select an option from the 'Caller ID' dropdown by its index.

        Args:
        index_value (int): The index of the caller ID option to select.
        """
        self.contact_made_between_patient_and_dropdown.select_option(index=index_value)

    def click_calendar_button(self) -> None:
        """Click the 'Calendar' button to open the calendar picker."""
        self.click(self.calendar_button)

    def enter_start_time(self, start_time: str) -> None:
        """
        Enter a value into the 'Start Time' field.

        Args:
        start_time (str): The start time to enter into the field.
        """
        self.start_time_field.fill(start_time)

    def enter_end_time(self, end_time: str) -> None:
        """
        Enter a value into the 'End Time' field.

        Args:
        end_time (str): The end time to enter into the field.
        """
        self.end_time_field.fill(end_time)

    def enter_discussion_record_text(self, value: str) -> None:
        """
        Enter text into the 'Discussion Record' field.

        Args:
        value (str): The text to enter into the discussion record field.
        """
        self.discussion_record_text_field.fill(value)

    def select_outcome_dropdown_option(self, outcome: str) -> None:
        """
        Select an option from the 'Outcome' dropdown by its label.

        Args:
            outcome (str): The label of the outcome option to select.
            Can be one of the following:
            - 'Suitable for Endoscopic Test'
            - 'Suitable for Radiological Test'
            - 'Close Episode - Patient Choice'
            - 'SSP Appointment Required'
        """
        self.outcome_dropdown.select_option(label=outcome)

    def click_save_button(self) -> None:
        """Click the 'Save' button to save the contact with patient form."""
        self.click(self.save_button)

    def record_post_investigation_appointment_not_required(self) -> None:
        """
        Record a post-investigation appointment not required contact.
        """
        self.select_direction_dropdown_option("To patient")
        self.select_caller_id_dropdown_index_option(1)
        self.click_calendar_button()
        CalendarPicker(self.page).v1_calender_picker(datetime.today())
        self.enter_start_time("11:00")
        self.enter_end_time("12:00")
        self.enter_discussion_record_text("Test Automation")
        self.select_outcome_dropdown_option(
            "Post-investigation Appointment Not Required"
        )
        self.click_save_button()

    def select_patient_contacted_dropdown_option(self, option: str) -> None:
        """
        Select an option from the 'Patient Contacted' dropdown by its label.

        Args:
            option (str): The label of the patient contacted option to select.
            Options can be 'Yes' or 'No'.
        """
        self.patient_contacted_dropdown.select_option(label=option)

    def record_contact(self, outcome: str, patient_contacted: str = "Yes") -> None:
        """
        Records contact with the patient.
        Args:
            outcome (str): The outcome of the contact. Options include:
                - 'Suitable for Endoscopic Test'
                - 'Suitable for Radiological Test'
                - 'Close Episode - Patient Choice'
                - 'SSP Appointment Required'
            patient_contacted (str): Indicates if the patient was contacted. Default is 'Yes'. Options include:
                - 'Yes'
                - 'No'
        """
        self.select_direction_dropdown_option("To patient")
        self.select_caller_id_dropdown_index_option(1)
        self.click_calendar_button()
        CalendarPicker(self.page).v1_calender_picker(datetime.today())
        self.enter_start_time("11:00")
        self.enter_end_time("12:00")
        self.enter_discussion_record_text("TEST AUTOMATION")
        self.select_patient_contacted_dropdown_option(patient_contacted)
        self.select_outcome_dropdown_option(outcome)
        self.click_save_button()

    def verify_contact_with_patient_page_is_displayed(self) -> None:
        """Verify that the 'Contact With Patient' page is displayed."""
        expect(self.bowel_cancer_screening_ntsh_page_title).to_have_text(
            "Contact with Patient", timeout=10000
        )

    def verify_outcome_select_options(self, options: list) -> None:
        """
        Verifies that the 'Outcome' dropdown contains the expected options.
        Args:
            options (list): A list containing all of the expected options in the dropdown.
        Raises:
            AssertionError: If any of the expected options are missing.
        """
        actual_options = self.outcome_dropdown.locator("option").all_text_contents()
        missing = [val for val in options if val not in actual_options]

        assert not missing, (
            f"Missing expected dropdown values in the outcome options: {missing}."
            f"Actual options: {actual_options}"
        )
