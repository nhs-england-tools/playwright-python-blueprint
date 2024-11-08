from datetime import datetime, timedelta


class DateTimeUtils:
    def __init__(self):
        pass

    @staticmethod
    def current_datetime(format_date: str = "%d/%m/%Y %H:%M"):
        """Gets the current datetime in the specified format.

        Args:
            format_date (str): [Optional] The format to return the current datetime in. Defaults to dd/mm/yyyy hh:mm if not provided.

        Returns:
            current_date (str): The current datetime in the specified format.

        """
        return datetime.now().strftime(format_date)

    @staticmethod
    def format_date(date, format_date: str = "%d/%m/%Y"):
        """Formats a specified datetime object.

        Args:
            date (datetime): The date to be formatted.
            format_date (str): [Optional] The format to return the datetime in. Defaults to dd/mm/yyyy if not provided.

        Returns:
            format_date (str): The formatted date in the specified format.

            """
        return date.strftime(format_date)

    @staticmethod
    def add_days(date: datetime, days: float):
        """Adds a specified number of days to a specified date.

        Args:
            date (datetime): The date to which the days will be added.
            days (float): The number of days to add to the specified date.

        Returns:
            new_date (str): The specified date plus the number of specified days (year, month, day, hour, minute, second, microsecond).

            """
        return date + timedelta(days=days)

    @staticmethod
    def get_day_of_week_for_today(date: datetime):
        """Gets the day of the week (e.g., Monday, Tuesday) from the specified date.

        Args:
            date (datetime): The current date using the now function

        Returns:
            day_of_week (str): The day of the week relating to the specified date.

            """
        return date.strftime("%A")

    @staticmethod
    def get_a_day_of_week(date: datetime):
        """Gets the day of the week (e.g., Monday, Tuesday) from the specified date.

        Args:
            date (datetime): The date for which the day of the week will be returned.

        Returns:
            day_of_week (str): The day of the week relating to the specified date.

            """
        return date.strftime("%A")
