from datetime import datetime, timedelta, tzinfo
from zoneinfo import ZoneInfo


class DateTimeUtils:
    UTC_TIMEZONE = "UTC"
    DST_TIMEZONE = "Europe/London"
    """
    A utility class for doing common actions with datetimes.
    """

    @staticmethod
    def current_datetime(format_date: str = "%d/%m/%Y %H:%M") -> str:
        """Gets the current datetime in the specified format.

        Args:
            format_date (str): [Optional] The format to return the current datetime in. Defaults to dd/mm/yyyy hh:mm if not provided.

        Returns:
            str: The current datetime in the specified format.
        """
        return datetime.now().strftime(format_date)

    @staticmethod
    def format_date(date: datetime, format_date: str = "%d/%m/%Y") -> str:
        """Formats a specified datetime object.

        Args:
            date (datetime): The date to be formatted.
            format_date (str): [Optional] The format to return the datetime in. Defaults to dd/mm/yyyy if not provided.

        Returns:
            str: The formatted date in the specified format.
        """
        return date.strftime(format_date)

    @staticmethod
    def add_days(date: datetime, days: float) -> datetime:
        """Adds a specified number of days to a specified date.

        Args:
            date (datetime): The date to which the days will be added.
            days (float): The number of days to add to the specified date.

        Returns:
            datetime: The specified date plus the number of specified days (year, month, day, hour, minute, second, microsecond).
        """
        return date + timedelta(days=days)

    @staticmethod
    def get_day_of_week_for_today(date: datetime) -> str:
        """Gets the day of the week (e.g., Monday, Tuesday) from the specified date.

        Args:
            date (datetime): The current date using the now function

        Returns:
            str: The day of the week relating to the specified date.
        """
        return date.strftime("%A")

    @staticmethod
    def get_a_day_of_week(date: datetime) -> str:
        """Gets the day of the week (e.g., Monday, Tuesday) from the specified date.

        Args:
            date (datetime): The date for which the day of the week will be returned.

        Returns:
            str: The day of the week relating to the specified date.
        """
        return date.strftime("%A")

    @staticmethod
    def report_timestamp_date_format(use_utc: bool = True) -> str:
        """Gets the current datetime in the timestamp format used on the report pages.
        Based on the value of `use_utc`, it chooses the appropriate timezone.
        """

        if use_utc:
            return DateTimeUtils.format_date(
                datetime.now(ZoneInfo(DateTimeUtils.UTC_TIMEZONE)),
                "%d/%m/%Y at %H:%M:%S",
            )
        else:
            return DateTimeUtils.format_date(
                datetime.now(ZoneInfo(DateTimeUtils.DST_TIMEZONE)),
                "%d/%m/%Y at %H:%M:%S",
            )

    @staticmethod
    def fobt_kits_logged_but_not_read_report_timestamp_date_format(
        use_utc: bool = False,
    ) -> str:
        """Gets the current datetime in the format used for FOBT Kits Logged but Not Read report.
        Based on the value of `use_utc`, it chooses the appropriate timezone.
        """

        if use_utc:
            return DateTimeUtils.format_date(
                datetime.now(ZoneInfo(DateTimeUtils.UTC_TIMEZONE)), "%d %b %Y %H:%M:%S"
            )
        else:
            return DateTimeUtils.format_date(
                datetime.now(ZoneInfo(DateTimeUtils.DST_TIMEZONE)), "%d %b %Y %H:%M:%S"
            )

    @staticmethod
    def screening_practitioner_appointments_report_timestamp_date_format(
        use_utc: bool = True,
    ) -> str:
        """Gets the current datetime in the format used for Screening Practitioner Appointments report.
        Based on the value of `use_utc`, it chooses the appropriate timezone.
        """

        if use_utc:
            return DateTimeUtils.format_date(
                datetime.now(ZoneInfo(DateTimeUtils.UTC_TIMEZONE)),
                "%d.%m.%Y at %H:%M:%S",
            )
        else:
            return DateTimeUtils.format_date(
                datetime.now(ZoneInfo(DateTimeUtils.DST_TIMEZONE)),
                "%d.%m.%Y at %H:%M:%S",
            )
