from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from typing import Optional
import logging
from classes.date.date_description import DateDescription


class DateDescriptionUtils:
    """
    Utility class for interpreting and converting date descriptions to Python date objects or formatted strings.
    """

    DATE_FORMAT_YYYY_MM_DD = "%Y-%m-%d"
    DATE_FORMAT_DD_MM_YYYY = "%d/%m/%Y"

    # string constants
    NULL_STRING = "NULL"
    NOT_NULL_STRING_UNDERSCORE = "NOT_NULL"
    NOT_NULL_STRING = "NOT NULL"

    @staticmethod
    def interpret_date(date_field_name: str, date_value: str) -> str:
        """
        Interprets a date description and returns a formatted date string (dd/MM/yyyy).
        If the date cannot be interpreted, returns the original value.
        Args:
            date_field_name (str): The name of the date field (for logging purposes).
            date_value (str): The date description to interpret. E.g., "2 years ago", "NULL", "15/08/2020".
        """
        logging.debug(f"interpret_date: {date_field_name}, {date_value}")
        try:
            return DateDescriptionUtils.convert_description_to_string_date(
                date_field_name, date_value, DateDescriptionUtils.DATE_FORMAT_DD_MM_YYYY
            )
        except Exception as e:
            logging.error(f"Could not interpret date: {e}")
            return date_value

    @staticmethod
    def convert_description_to_sql_date(
        which_date: str, date_description: str
    ) -> Optional[str]:
        """
        Converts a date description to an Oracle TO_DATE SQL string.
        Returns None if the date cannot be interpreted.
        Args:
            which_date (str): A label for the date being converted (for logging purposes). E.g., "start_date", "end_date".
            date_description (str): The date description to convert. E.g., "2 years ago", "NULL", "15/08/2020".
        """
        logging.debug(
            f"convert_description_to_sql_date: {which_date}, {date_description}"
        )
        return_date_string = None
        return_date = None

        date_description_words = date_description.split(" ")

        # First handle actual dates
        if DateDescriptionUtils.is_valid_date(
            date_description, DateDescriptionUtils.DATE_FORMAT_DD_MM_YYYY
        ):
            return_date_string = DateDescriptionUtils.oracle_to_date_function(
                date_description, "dd/mm/yyyy"
            )
        elif DateDescriptionUtils.is_valid_date(
            date_description, DateDescriptionUtils.DATE_FORMAT_YYYY_MM_DD
        ):
            return_date_string = DateDescriptionUtils.oracle_to_date_function(
                date_description, "yyyy-mm-dd"
            )
        elif date_description.endswith(" ago") and len(date_description_words) == 3:
            return_date = DateDescriptionUtils.convert_description_to_local_date(
                which_date, date_description
            )
        else:
            # If the date description is in the enum, use the suggested suitable date, plus allow for NULL and NOT NULL
            enum_val = DateDescription.by_description_case_insensitive(date_description)
            if enum_val is not None:
                if enum_val.name == DateDescriptionUtils.NULL_STRING:
                    return_date_string = DateDescriptionUtils.NULL_STRING
                elif enum_val.name == DateDescriptionUtils.NOT_NULL_STRING_UNDERSCORE:
                    return_date_string = DateDescriptionUtils.NOT_NULL_STRING
                else:
                    return_date = enum_val.suitable_date

        if return_date is not None and return_date_string is None:
            return_date_string = DateDescriptionUtils.oracle_to_date_function(
                return_date.strftime(DateDescriptionUtils.DATE_FORMAT_DD_MM_YYYY),
                "dd/mm/yyyy",
            )

        return return_date_string

    @staticmethod
    def convert_description_to_local_date(
        which_date: str, date_description: str
    ) -> date:
        """
        Converts a date description to a Python date object.
        Raises ValueError if the description cannot be interpreted.
        Args:
            which_date (str): A label for the date being converted (for logging purposes). E.g., "start_date", "end_date".
            date_description (str): The date description to convert. E.g., "2 years ago", "NULL", "15/08/2020".
        """
        logging.debug(
            f"convert_description_to_local_date: {which_date}, {date_description}"
        )
        date_description_words = date_description.split(" ")

        # Handle actual dates
        if DateDescriptionUtils.is_valid_date(
            date_description, DateDescriptionUtils.DATE_FORMAT_DD_MM_YYYY
        ):
            return datetime.strptime(
                date_description, DateDescriptionUtils.DATE_FORMAT_DD_MM_YYYY
            ).date()
        if DateDescriptionUtils.is_valid_date(
            date_description, DateDescriptionUtils.DATE_FORMAT_YYYY_MM_DD
        ):
            return datetime.strptime(
                date_description, DateDescriptionUtils.DATE_FORMAT_YYYY_MM_DD
            ).date()

        # Handle relative dates ("ago" or "ahead")
        if DateDescriptionUtils._is_relative_date(
            date_description, date_description_words, "ago"
        ):
            return DateDescriptionUtils._calculate_relative_date(
                date_description_words, is_ago=True
            )
        if DateDescriptionUtils._is_relative_date(
            date_description, date_description_words, "ahead"
        ):
            return DateDescriptionUtils._calculate_relative_date(
                date_description_words, is_ago=False
            )

        # Handle enum-based descriptions
        enum_val = DateDescription.by_description_case_insensitive(date_description)
        if enum_val is not None:
            if enum_val.name in [
                DateDescriptionUtils.NULL_STRING,
                DateDescriptionUtils.NOT_NULL_STRING_UNDERSCORE,
            ]:
                raise ValueError(f"Cannot convert '{date_description}' to a date.")
            if enum_val.suitable_date is not None:
                return enum_val.suitable_date

        raise ValueError(f"Cannot interpret date description '{date_description}'.")

    @staticmethod
    def _is_relative_date(date_description, words, suffix):
        """Checks if the date description is a relative date ending with the specified suffix.
        Args:
            date_description (str): The full date description string.
            words (list): The split words of the date description.
            suffix (str): The suffix to check for ("ago" or "ahead").
        """
        return date_description.endswith(f" {suffix}") and len(words) == 3

    @staticmethod
    def _calculate_relative_date(words, is_ago):
        """Calculates the date based on the relative description.
        Args:
            words (list): The split words of the date description. E.g., ["2", "years", "ago"].
            is_ago (bool): Whether the date is in the past (True) or future (False).
        """
        if not words[0].isdigit():
            raise ValueError(f"Invalid period number in '{' '.join(words)}'")
        number_of_periods = int(words[0])
        period_type = words[1]
        today = date.today()
        delta_days = DateDescriptionUtils._get_delta_days(
            number_of_periods, period_type
        )
        if is_ago:
            return today - timedelta(days=delta_days)
        else:
            return today + timedelta(days=delta_days)

    @staticmethod
    def _get_delta_days(number_of_periods, period_type):
        """Returns the number of days corresponding to the given period type and number.
        Args:
            number_of_periods (int): The number of periods (e.g., 2).
            period_type (str): The type of period (e.g., "years", "months", "weeks", "days").
        """
        if period_type in ["year", "years"]:
            return number_of_periods * 365
        if period_type in ["month", "months"]:
            return number_of_periods * 30
        if period_type in ["week", "weeks"]:
            return number_of_periods * 7
        if period_type in ["day", "days"]:
            return number_of_periods
        raise ValueError(f"Unknown period type '{period_type}'")

    @staticmethod
    def convert_description_to_string_date(
        which_date: str, date_description: str, date_format: str
    ) -> str:
        """
        Converts a date description to a formatted date string.
        Raises ValueError if the description cannot be interpreted.
        Args:
            which_date (str): A label for the date being converted (for logging purposes). E.g., "start_date", "end_date".
            date_description (str): The date description to convert. E.g., "2 years ago", "NULL", "15/08/2020".
            date_format (str): The desired output date format. E.g., "%d/%m/%Y".
        Returns:
            str: The formatted date string.
        """
        logging.debug(
            f"convert_description_to_string_date: {which_date}, {date_description}, {date_format}"
        )
        local_date = DateDescriptionUtils.convert_description_to_local_date(
            which_date, date_description
        )
        return local_date.strftime(date_format)

    @staticmethod
    def is_valid_date(date_str: str, date_format: str) -> bool:
        """
        Checks if the given string is a valid date in the specified format.
        Args:
            date_str (str): The date string to validate.
            date_format (str): The format to validate against. E.g., "%d/%m/%Y".
        Returns:
            bool: True if the string is a valid date, False otherwise.
        """
        try:
            datetime.strptime(date_str, date_format)
            return True
        except ValueError:
            return False

    @staticmethod
    def oracle_to_date_function(date_str: str, oracle_format: str) -> str:
        """
        Constructs a safe Oracle TO_DATE() expression from a Python date string.
        Args:
            date_str (str): The date string to be converted (e.g., '06/10/1950').
            oracle_format (str): The Oracle format mask (e.g., 'dd/mm/yyyy').
        Returns:
            str: The SQL-safe TO_DATE(...) expression, or 'NULL' if date_str is None/empty.
        """
        if not date_str or str(date_str).strip().lower() == "none":
            return "NULL"

        clean = str(date_str).strip().replace("\u00a0", "")
        py_fmt = (
            oracle_format.lower()
            .replace("dd", "%d")
            .replace("mm", "%m")
            .replace("yyyy", "%Y")
        )

        # Validate in Python before sending to Oracle
        datetime.strptime(clean, py_fmt)

        return f"TO_DATE('{clean}', '{oracle_format}')"

    @staticmethod
    def convert_description_to_python_date(
        which_date: str, date_description: str
    ) -> Optional[date]:
        """
        Converts a date description (e.g. '2 years ago', '15/08/2020', 'NULL')
        into a Python datetime.date object or None.
        Args:
            which_date (str): Label for logging.
            date_description (str): Human-readable or exact date description.
        Returns:
            Optional[date]: The corresponding date object, or None if not applicable.
        """
        logging.debug(
            f"convert_description_to_python_date: {which_date}, {date_description}"
        )

        if not date_description or date_description.strip().upper() in (
            DateDescriptionUtils.NULL_STRING,
            "NONE",
        ):
            return None

        date_description = date_description.strip()
        today = datetime.today().date()

        # Try direct date formats
        abs_date = _parse_absolute_date(date_description)
        if abs_date:
            return abs_date

        # Try relative phrases like "3 years ago"
        rel_date = _parse_relative_date(date_description, today)
        if rel_date:
            return rel_date

        # Try enum-based descriptions
        enum_date = _parse_enum_date(date_description, today)
        if enum_date is not None:
            return enum_date

        return None


def _parse_absolute_date(date_description: str) -> Optional[date]:
    """
    Tries to parse an absolute date from the description.
    Args:
        date_description (str): The date description to parse.
    Returns:
        Optional[date]: The parsed absolute date or None if parsing failed.
    """
    for fmt in (
        DateDescriptionUtils.DATE_FORMAT_DD_MM_YYYY,
        DateDescriptionUtils.DATE_FORMAT_YYYY_MM_DD,
    ):
        if DateDescriptionUtils.is_valid_date(date_description, fmt):
            return datetime.strptime(date_description, fmt).date()
    return None


def _parse_relative_date(date_description: str, today: date) -> Optional[date]:
    """
    Tries to parse a relative date from the description (e.g., "3 years ago").
    Args:
        date_description (str): The date description to parse.
        today (date): The reference date for relative calculations.
    Returns:
        Optional[date]: The parsed relative date or None if parsing failed.
    """
    words = date_description.split(" ")
    if date_description.endswith(" ago") and len(words) == 3:
        try:
            number = int(words[0])
            unit = words[1]
            if "year" in unit:
                return today - relativedelta(years=number)
            if "month" in unit:
                return today - relativedelta(months=number)
            if "day" in unit:
                return today - timedelta(days=number)
        except Exception as e:
            logging.warning(f"Could not parse relative date '{date_description}': {e}")
    return None


def _parse_enum_date(date_description: str, today: date) -> Optional[date]:
    """
    Tries to parse a date from the DateDescription enum.
    Args:
        date_description (str): The date description to parse.
        today (date): The reference date for special cases.
    Returns:
        Optional[date]: The parsed enum date or None if parsing failed.
    """
    enum_val = DateDescription.by_description_case_insensitive(date_description)
    if enum_val is not None:
        if enum_val.name == DateDescriptionUtils.NULL_STRING:
            return None
        if enum_val.name == DateDescriptionUtils.NOT_NULL_STRING_UNDERSCORE:
            return today
        return enum_val.suitable_date
    return None
