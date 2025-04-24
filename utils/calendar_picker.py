from datetime import datetime
from utils.date_time_utils import DateTimeUtils
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from sys import platform


class CalendarPicker(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # V1 Calendar picker locators
        self.v1_prev_year = self.page.get_by_role("cell", name="«").locator("div")
        self.v1_prev_month = self.page.get_by_role("cell", name="‹").locator("div")
        self.v1_next_month = self.page.get_by_role("cell", name="›").locator("div")
        self.v1_next_year = self.page.get_by_role("cell", name="»").locator("div")

    # Calendar Methods
    def calendar_picker_ddmmyyyy(self, date: datetime, locator: Locator) -> None:
        """Enters a date in the format dd/mm/yyyy (e.g. 16/01/2025) into the specified locator
        This is for the older style pages v1

        Args:
            date (datetime): The date we want to enter into the locator
            locator (Locator): The locator of the element in which we want to enter the date
        """
        formatted_date = DateTimeUtils.format_date(date)
        locator.fill(formatted_date)
        locator.press("Enter")

    def calendar_picker_ddmonyy(self, date: datetime, locator: Locator) -> None:
        """Enters a date in the format dd month yy (e.g. 16 Jan 25) into the specified locator
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
        """
        years_to_traverse = int(current_date.strftime("%Y")) - int(date.strftime("%Y"))
        months_to_traverse = int(current_date.strftime("%m")) - int(date.strftime("%m"))
        return years_to_traverse, months_to_traverse

    def traverse_years_in_v1_calendar(self, years_to_traverse: int) -> None:
        """
        This function traverses the years on the v1 calendar picker by the number specified in years_to_traverse
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
        """
        if platform == "win32":  # Windows
            day_to_select = str(date.strftime("%#d"))
        else:  # Linux or Mac
            day_to_select = str(date.strftime("%-d"))
        number_of_cells_with_day = self.page.get_by_role(
            "cell", name=day_to_select
        ).count()

        if int(day_to_select) < 15 and number_of_cells_with_day > 1:
            self.click(self.page.locator(".day", has_text=day_to_select).first)
        elif int(day_to_select) > 15 and number_of_cells_with_day > 1:
            self.click(self.page.locator(".day", has_text=day_to_select).last)
        else:
            self.click(self.page.locator(".day", has_text=day_to_select))

    def v1_calender_picker(self, date: datetime) -> None:
        """
        This is the main method used to traverse the v1 calendar picker (e.g. the one on the subject screening search page)
        You provide it with a date and it will call the necessary functions to calculate how to navigate to the specified date
        """
        current_date = datetime.today()
        years_to_traverse, months_to_traverse = (
            self.calculate_years_and_months_to_traverse(date, current_date)
        )

        self.traverse_years_in_v1_calendar(years_to_traverse)

        self.traverse_months_in_v1_calendar(months_to_traverse)

        self.select_day(date)

    def calculate_v2_calendar_variables(
        self, date: datetime, current_date: datetime
    ) -> tuple[str, str, str, int, int, str, int, int, str, int, int]:
        """
        This function calculates all of the variables needed to traverse through the v2 calendar picker
        Args:
            current_month_long: the current month in long format (e.g. April)
            month_long: the wanted month in long format (e.g. June)
            month_short: the wanted month is short format (e.g. Jun)
            current_year: the current year in yyyy format (e.g. 2025)
            year: the wanted year in yyyy format (e.g. 1983)
            end_of_current_decade: the end of the current decade in yyyy format (e.g. 2029)
            current_decade: the current decade in yyyy format (e.g. 2020)
            decade: the wanted decade in yyyy format (e.g. 1980)
            end_of_current_century: 10 years before the end of the current century in yyyy format (e.g. 2090)
            current_century: the current century in yyyy format (e.g. 2000/2100)
            century: the wanted century in yyyy format (e.g. 1900)
        """
        current_month_long = str(current_date.strftime("%B"))
        current_year = int(current_date.strftime("%Y"))
        current_century = (current_year // 100) * 100
        end_of_current_century = str(current_century + 90)
        current_decade = (
            ((current_year - current_century) // 10) * 10
        ) + current_century
        end_of_current_decade = str(current_decade + 9)

        year = int(date.strftime("%Y"))
        century = (year // 100) * 100
        decade = (((year - century) // 10) * 10) + century
        month_short = str(date.strftime("%b"))
        month_long = str(date.strftime("%B"))

        return (
            current_month_long,
            month_long,
            month_short,
            current_year,
            year,
            end_of_current_decade,
            current_decade,
            decade,
            end_of_current_century,
            current_century,
            century,
        )

    def v2_calendar_picker_traverse_back(
        self,
        current_month_long: str,
        month_long: str,
        current_year: int,
        year: int,
        end_of_current_decade: str,
        current_decade: int,
        decade: int,
        end_of_current_century: str,
        current_century: int,
        century: int,
    ) -> tuple[bool, bool, bool, bool]:
        """
        This function is used to "go back in time" / "expand" on the v2 calendar picker
        By selecting the top locator we can increase the range of dates available to be clicked
        It uses the variables calculated in 'calculate_v2_calendar_variables' to know which locators to select
        """

        click_month = False
        click_year = False
        click_decade = False
        click_century = False

        if current_month_long != month_long:
            self.click(self.page.get_by_role("cell", name=current_month_long))
            click_month = True
        if current_year != year:
            self.click(
                self.page.get_by_role("cell", name=str(current_year), exact=True)
            )
            click_year = True
        if current_decade != decade:
            self.click(
                self.page.get_by_role("cell", name=("-" + str(end_of_current_decade)))
            )
            click_decade = True
        if current_century != century:
            self.click(
                self.page.get_by_role("cell", name=("-" + str(end_of_current_century)))
            )
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
    ):
        """
        This function is used to "go forward" through the v2 calendar picker after the date range has been expanded
        It uses the variables calculated in 'calculate_v2_calendar_variables' to know which locators to select
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
        """
        current_date = datetime.today()
        (
            current_month_long,
            month_long,
            month_short,
            current_year,
            year,
            end_of_current_decade,
            current_decade,
            decade,
            end_of_current_century,
            current_century,
            century,
        ) = self.calculate_v2_calendar_variables(date, current_date)

        click_month, click_year, click_decade, click_century = (
            self.v2_calendar_picker_traverse_back(
                current_month_long,
                month_long,
                current_year,
                year,
                end_of_current_decade,
                current_decade,
                decade,
                end_of_current_century,
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
