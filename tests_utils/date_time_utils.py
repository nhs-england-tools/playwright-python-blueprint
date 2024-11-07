from datetime import datetime

class DateTimeUtils:
    def __init__(self):
        pass

    @staticmethod
    def current_datetime(format_date="%d/%m/%Y %H:%M"):
        """Gets the current datetime in the specified format."""
        return datetime.now().strftime(format_date)

    @staticmethod
    def format_date(date, format_date="%Y/%m/%d"):
        """Formats a given date object."""
        return date.strftime(format_date)

    @staticmethod
    def add_days(date, days):
        """Adds a specified number of days to the given date."""
        return date + datetime.timedelta(days=days)

    @staticmethod
    def get_day_of_week(date):
        """Gets the day of the week (e.g., Monday, Tuesday) from the given date."""
        return date.strftime("%A")
