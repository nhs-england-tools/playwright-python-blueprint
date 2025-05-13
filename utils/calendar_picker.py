from datetime import datetime
from utils.date_time_utils import DateTimeUtils
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from sys import platform
import pytest


class CalendarPicker(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # V1 Calendar picker locators
        self.v1_prev_year = self.page.get_by_role("cell", name="«").locator("div")
        self.v1_prev_month = self.page.get_by_role("cell", name="‹").locator("div")
        self.v1_next_month = self.page.get_by_role("cell", name="›").locator("div")
        self.v1_next_year = self.page.get_by_role("cell", name="»").locator("div")
        self.v1_calendar_current_date = self.page.locator(
            'td.title[colspan="5"][style="cursor: move;"]'
        )
        self.v1_today_button = self.page.get_by_text("Today", exact=True)
        # V2 Calendar picker locators
        self.v2date_picker_switch = self.page.locator(
            'th.datepicker-switch[colspan="5"]:visible'
        )
        # Book Appointment picker locators
        self.appointments_prev_month = self.page.get_by_role(
            "link", name="<-", exact=True
        )
        self.appointments_next_month = self.page.get_by_role(
            "link", name="->", exact=True
        )

    # Calendar Methods
    def calendar_picker_ddmmyyyy(self, date: datetime, locator: Locator) -> None:
        """
        Enters a date in the format dd/mm/yyyy (e.g. 16/01/2025) into the specified locator
        This is for the older style pages v1

        Args:
            date (datetime): The date we want to enter into the locator
            locator (Locator): The locator of the element in which we want to enter the date
        """
        formatted_date = DateTimeUtils.format_date(date)
        locator.fill(formatted_date)
        locator.press("Enter")

    def calendar_picker_ddmonyy(self, date: datetime, locator: Locator) -> None:
        """
        Enters a date in the format dd month yy (e.g. 16 Jan 25) into the specified locator
        This is for the more modern style pages v2

        Args:
            date (datetime): The date we want to enter into the locator
            locator (Locator): The locator of the element in which we want to enter the date
        """
        if platform == "win32":  # Windows
            formatted_date = DateTimeUtils.format_date(date, "%#d %b %Y")
        else:  # Linux or Mac
            formatted_date = DateTimeUtils.format_date(date, "%-d %b %Y")
        locator.fill(formatted_date)
        locator.press("Enter")

    def calculate_years_and_months_to_traverse(
        self, date: datetime, current_date: datetime
    ) -> tuple[int, int]:
        """
        This function is used when using the v1 calendar picker
        It calculates how many years and months it needs to traverse

        Args:
            date (datetime): The date we want to go to
            current_date (datetime): The current date

        Returns:
            years_to_traverse (int): The number of years we need to traverse
            years_to_traverse (int): The number of months we need to traverse
        """
        years_to_traverse = int(DateTimeUtils.format_date(current_date, "%Y")) - int(
            DateTimeUtils.format_date(date, "%Y")
        )
        months_to_traverse = int(DateTimeUtils.format_date(current_date, "%m")) - int(
            DateTimeUtils.format_date(date, "%m")
        )
        return years_to_traverse, months_to_traverse

    def traverse_years_in_v1_calendar(self, years_to_traverse: int) -> None:
        """
        This function traverses the years on the v1 calendar picker by the number specified in years_to_traverse

        Args:
            years_to_traverse (int): The number of years we need to traverse
        """
        if years_to_traverse > 0:
            for _ in range(years_to_traverse):
                self.click(self.v1_prev_year)
        elif years_to_traverse < 0:
            for _ in range(years_to_traverse * -1):
                self.click(self.v1_next_year)

    def traverse_months_in_v1_calendar(self, months_to_traverse: int) -> None:
        """
        This function traverses the months on the v1 calendar picker by the number specified in months_to_traverse

        Args:
            months_to_traverse (int): The number of months we need to traverse
        """
        if months_to_traverse > 0:
            for _ in range(months_to_traverse):
                self.click(self.v1_prev_month)
        elif months_to_traverse < 0:
            for _ in range(months_to_traverse * -1):
                self.click(self.v1_next_month)

    def select_day(self, date: datetime) -> None:
        """
        This function is used by both the v1 and v2 calendar picker
        It extracts the day from the date and then selects that value in the calendar picker

        Args:
            date (datetime): The date we want to select
        """
        if platform == "win32":  # Windows
            day_to_select = DateTimeUtils.format_date(date, "%#d")
        else:  # Linux or Mac
            day_to_select = DateTimeUtils.format_date(date, "%-d")
        number_of_cells_with_day = self.page.get_by_role(
            "cell", name=day_to_select
        ).count()

        all_matching_days = self.page.get_by_role(
            "cell", name=day_to_select, exact=True
        ).all()

        matching_days = [
            day
            for day in all_matching_days
            if day.evaluate("el => el.textContent.trim()") == day_to_select
        ]

        if int(day_to_select) < 15 and number_of_cells_with_day > 1:
            self.click(matching_days[0].first)
        elif int(day_to_select) > 15 and number_of_cells_with_day > 1:
            self.click(matching_days[-1].last)
        else:
            self.click(matching_days[0])

    def v1_calender_picker(self, date: datetime) -> None:
        """
        This is the main method used to traverse the v1 calendar picker (e.g. the one on the subject screening search page)
        You provide it with a date and it will call the necessary functions to calculate how to navigate to the specified date

        Args:
            date (datetime): The date we want to select
        """

        if DateTimeUtils.format_date(date, "%d/%m/%Y") == DateTimeUtils.format_date(
            datetime.today(), "%d/%m/%Y"
        ):
            self.click(self.v1_today_button)
            return

        current_date = datetime.strptime(
            self.v1_calendar_current_date.inner_text(), "%B, %Y"
        )
        years_to_traverse, months_to_traverse = (
            self.calculate_years_and_months_to_traverse(date, current_date)
        )
        self.traverse_years_in_v1_calendar(years_to_traverse)

        self.traverse_months_in_v1_calendar(months_to_traverse)

        self.select_day(date)

    def calculate_v2_calendar_variables(
        self, date: datetime, current_date: datetime
    ) -> tuple[str, str, str, int, int, int, int, int, int]:
        """
        This function calculates all of the variables needed to traverse through the v2 calendar picker

        Args:
            date (datetime): The date we want to select
            current_date (datetime): The current date

        Returns:
            current_month_long (str): The current month in long format (e.g. April)
            month_long (str): The wanted month in long format (e.g. June)
            month_short (str): The wanted month is short format (e.g. Jun)
            current_year (int): The current year in yyyy format (e.g. 2025)
            year (int): The wanted year in yyyy format (e.g. 1983)
            current_decade (int): The current decade in yyyy format (e.g. 2020)
            decade (int): The wanted decade in yyyy format (e.g. 1980)
            current_century (int): The current century in yyyy format (e.g. 2000/2100)
            century (int): The wanted century in yyyy format (e.g. 1900)
        """
        current_month_long = DateTimeUtils.format_date(current_date, "%B")
        current_year = int(DateTimeUtils.format_date(current_date, "%Y"))
        current_century = (current_year // 100) * 100
        current_decade = (
            ((current_year - current_century) // 10) * 10
        ) + current_century

        year = int(DateTimeUtils.format_date(date, "%Y"))
        century = (year // 100) * 100
        decade = (((year - century) // 10) * 10) + century
        month_short = DateTimeUtils.format_date(date, "%b")
        month_long = DateTimeUtils.format_date(date, "%B")

        return (
            current_month_long,
            month_long,
            month_short,
            current_year,
            year,
            current_decade,
            decade,
            current_century,
            century,
        )

    def v2_calendar_picker_traverse_back(
        self,
        current_month_long: str,
        month_long: str,
        current_year: int,
        year: int,
        current_decade: int,
        decade: int,
        current_century: int,
        century: int,
    ) -> tuple[bool, bool, bool, bool]:
        """
        This function is used to "go back in time" / "expand" on the v2 calendar picker
        By selecting the top locator we can increase the range of dates available to be clicked
        It uses the variables calculated in 'calculate_v2_calendar_variables' to know which locators to select

        Args:
            current_month_long (str): The current month in long format (e.g. April)
            month_long (str): The wanted month in long format (e.g. June)
            current_year (int): The current year in yyyy format (e.g. 2025)
            year (int): The wanted year in yyyy format (e.g. 1983)
            current_decade (int): The current decade in yyyy format (e.g. 2020)
            decade (int): The wanted decade in yyyy format (e.g. 1980)
            current_century (int): The current century in yyyy format (e.g. 2000/2100)
            century (int): The wanted century in yyyy format (e.g. 1900)

        Returns:
            click_month (bool): True/False depending on if we clicked on the month
            click_year (bool): True/False depending on if we clicked on the year
            click_decade (bool): True/False depending on if we clicked on the decade
            click_century (bool): True/False depending on if we clicked on the century
        """

        click_month = False
        click_year = False
        click_decade = False
        click_century = False

        if current_month_long != month_long:
            self.click(self.v2date_picker_switch)
            click_month = True
        if current_year != year:
            self.click(self.v2date_picker_switch)
            click_year = True
        if current_decade != decade:
            self.click(self.v2date_picker_switch)
            click_decade = True
        if current_century != century:
            self.click(self.v2date_picker_switch)
            click_century = True

        return click_month, click_year, click_decade, click_century

    def v2_calendar_picker_traverse_forward(
        self,
        click_month: bool,
        click_year: bool,
        click_decade: bool,
        click_century: bool,
        century: str,
        decade: str,
        year: str,
        month_short: str,
    ) -> None:
        """
        This function is used to "go forward" through the v2 calendar picker after the date range has been expanded
        It uses the variables calculated in 'calculate_v2_calendar_variables' to know which locators to select

        Args:
            click_month (bool): True/False depending on if we need to click on the month
            click_year (bool): True/False depending on if we need to click on the year
            click_decade (bool): True/False depending on if we need to click on the decade
            click_century (bool): True/False depending on if we need to click on the century
            century (str): The century of the date we want to select
            decade (str): The decade of the date we want to select
            year (str): The year of the date we want to select
            month_short (str): The month of the date we want to select
        """

        if click_century:
            self.click(self.page.get_by_text(str(century), exact=True).first)
        if click_decade:
            self.click(self.page.get_by_text(str(decade), exact=True).first)
        if click_year:
            self.click(self.page.get_by_text(str(year), exact=True))
        if click_month:
            self.click(self.page.get_by_text(str(month_short)))

    def v2_calendar_picker(self, date: datetime) -> None:
        """
        This is the main method to navigate the v2 calendar picker (like the one on the Active Batch List page)
        This calls all the relevant functions in order to know how to traverse the picker

        Args:
            date (datetime): The date we want to select
        """
        current_date = datetime.today()
        (
            current_month_long,
            month_long,
            month_short,
            current_year,
            year,
            current_decade,
            decade,
            current_century,
            century,
        ) = self.calculate_v2_calendar_variables(date, current_date)

        click_month, click_year, click_decade, click_century = (
            self.v2_calendar_picker_traverse_back(
                current_month_long,
                month_long,
                current_year,
                year,
                current_decade,
                decade,
                current_century,
                century,
            )
        )

        self.v2_calendar_picker_traverse_forward(
            click_month,
            click_year,
            click_decade,
            click_century,
            century,
            decade,
            year,
            month_short,
        )

        self.select_day(date)

    def book_first_eligible_appointment(
        self,
        current_month_displayed: str,
        locator: Locator,
        bg_colours: list,
    ) -> None:
        """
        This is used to select the first eligible appointment date
        It first sets the calendar to the current month
        Then gets all available dates, and then clicks on the first one starting from today's date
        If no available dates are found it moves onto the next month and repeats this 2 more times
        If in the end no available dates are found the test will fail.

        Args:
            current_month_displayed (str): The current month that is displayed by the calendar
            locator (Locator): The locator of the cells containing the days
            bg_colours (list): A list containing all of the background colours of cells we would like to select
        """
        current_month_displayed_int = DateTimeUtils().month_string_to_number(
            current_month_displayed
        )
        if platform == "win32":  # Windows
            current_month_int = int(DateTimeUtils.format_date(datetime.now(), "%#m"))
        else:  # Linux or Mac
            current_month_int = int(DateTimeUtils.format_date(datetime.now(), "%-m"))

        self.book_appointments_go_to_month(
            current_month_displayed_int, current_month_int
        )

        months_looped = 0
        appointment_clicked = False
        while (
            months_looped < 3 and not appointment_clicked
        ):  # This loops through this month + next two months to find available appointments. If none found it has failed
            appointment_clicked = self.check_for_eligible_appointment_dates(
                locator, bg_colours
            )

            if not appointment_clicked:
                self.click(self.appointments_next_month)
                months_looped += 1

        if not appointment_clicked:
            pytest.fail("No available appointments found for the current month")

    def book_appointments_go_to_month(
        self, current_displayed_month: int, wanted_month: int
    ):
        """
        This is used to move the calendar on the appointments page to the wanted month

        Args:
            current_displayed_month (int): The current month shown as an integer
            wanted_month (int): The month we want to go to as an integer
        """
        month_difference = current_displayed_month - wanted_month
        if month_difference > 0:
            for _ in range(month_difference):
                self.click(self.appointments_prev_month)
        elif month_difference < 0:
            for _ in range(month_difference * -1):
                self.click(self.appointments_next_month)

    def check_for_eligible_appointment_dates(
        self, locator: Locator, bg_colours: list
    ) -> bool:
        """
        This function loops through all of the appointment date cells and if the background colour matches
        It then checks that the length of the name is less than 5.
        This is done the name length is the only differentiating factor between the two calendar tables on the page
        - 1st table has a length of 4 (e.g. wed2, fri5) and the 2nd table has a length of 5 (e.g. wed11, fri14)

        Args:
            locator (Locator): The locator of the cells containing the days
            bg_colours (list): A list containing all of the background colours of cells we would like to select

        Returns:
            True
        """

        locator_count = locator.count()

        for i in range(locator_count):
            locator_element = locator.nth(i)
            background_colour = locator_element.evaluate(
                "el => window.getComputedStyle(el).backgroundColor"
            )

            if background_colour in bg_colours:
                value = locator_element.get_attribute("name")
                if len(value) < 5:
                    self.click(locator.nth(i))
                    return True
