from playwright.sync_api import Page
from datetime import datetime
from faker import Faker
from dateutil.relativedelta import relativedelta
import logging
from pages.base_page import BasePage
from pages.screening_subject_search.subject_screening_search_page import (
    SubjectScreeningPage,
    SearchAreaSearchOptions,
)
from pages.screening_subject_search.subject_demographic_page import (
    SubjectDemographicPage,
)


class SubjectDemographicUtil:
    """The class for holding all the util methods to be used on the subject demographic page"""

    def __init__(self, page: Page):
        self.page = page

    def update_subject_dob(self, nhs_no: str, younger_subject: bool) -> None:
        """
        Navigates to the subject demographics page and updates a subject's date of birth.

        Args:
            nhs_no (str): The NHS number of the subject you want to update.
            younger_subject (bool): Whether you want the subject to be younger (50-70) or older (75-100).
        """
        if younger_subject:
            end_date = datetime.today() - relativedelta(years=50)
            start_date = datetime.today() - relativedelta(years=70)
            date = self.random_datetime(start_date, end_date)
        else:
            end_date = datetime.today() - relativedelta(years=75)
            start_date = datetime.today() - relativedelta(years=100)
            date = self.random_datetime(start_date, end_date)

        logging.info(f"Navigating to subject demographic page for: {nhs_no}")
        BasePage(self.page).click_main_menu_link()
        BasePage(self.page).go_to_screening_subject_search_page()
        SubjectScreeningPage(self.page).click_demographics_filter()
        SubjectScreeningPage(self.page).click_nhs_number_filter()
        SubjectScreeningPage(self.page).nhs_number_filter.fill(nhs_no)
        SubjectScreeningPage(self.page).nhs_number_filter.press("Tab")
        SubjectScreeningPage(self.page).select_search_area_option(
            SearchAreaSearchOptions.SEARCH_AREA_WHOLE_DATABASE.value
        )
        SubjectScreeningPage(self.page).click_search_button()
        postcode_filled = SubjectDemographicPage(self.page).is_postcode_filled()
        if not postcode_filled:
            fake = Faker("en_GB")
            random_postcode = fake.postcode()
            SubjectDemographicPage(self.page).fill_postcode_input(random_postcode)

        current_dob = SubjectDemographicPage(self.page).get_dob_field_value()
        logging.info(f"Current DOB: {current_dob}")
        SubjectDemographicPage(self.page).fill_dob_input(date)
        SubjectDemographicPage(self.page).click_update_subject_data_button()
        updated_dob = SubjectDemographicPage(self.page).get_dob_field_value()
        logging.info(f"Updated DOB: {updated_dob}")

    def random_datetime(self, start: datetime, end: datetime) -> datetime:
        """
        Generate a random datetime between two datetime objects.

        Args:
            start (datetime): the starting date
            end (datetime): The end date

        Returns:
            datetime: the newly generated date
        """
        fake = Faker()
        return fake.date_time_between(start, end)
