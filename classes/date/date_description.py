from enum import Enum
from typing import Optional
from datetime import date, timedelta
import random


class DateDescription(Enum):
    """
    Enum representing various date descriptions and their associated logic.

    Each member contains:
        - description (str): A human-readable description of the date logic.
        - number_of_months (int): The number of months relevant to the date logic.
        - suitable_date (Optional[date]): A calculated or representative date, if applicable.

    Example members:
        AFTER_TODAY: A date after today, randomly chosen up to 1000 days in the future.
        BEFORE_TODAY: A date before today, randomly chosen up to 1000 days in the past.
        TODAY: Today's date.
        YESTERDAY: Yesterday's date.
        NULL: Represents a null value.
        NOT_NULL: Represents a non-null value.
    """

    AFTER_TODAY = (
        "after today",
        0,
        date.today() + timedelta(days=random.randint(1, 1000)),
    )
    AS_AT_EPISODE_START = ("as at episode start", 0, None)
    BEFORE_TODAY = (
        "before today",
        0,
        date.today() - timedelta(days=random.randint(1, 1000)),
    )
    CALCULATED_FOBT_DUE_DATE = ("calculated fobt due date", 0, None)
    CALCULATED_LYNCH_DUE_DATE = ("calculated lynch due date", 0, None)
    CALCULATED_SCREENING_DUE_DATE = ("calculated screening due date", 0, None)
    CALCULATED_SURVEILLANCE_DUE_DATE = ("calculated surveillance due date", 0, None)
    CSDD = ("csdd", 0, None)
    CSSDD = ("cssdd", 0, None)
    GREATER_THAN_TODAY = (
        "> today",
        0,
        date.today() + timedelta(days=random.randint(1, 1000)),
    )
    LAST_BIRTHDAY = ("last birthday", 0, None)
    LESS_THAN_2_YEARS_AGO = (
        "less than 2 years ago",
        24,
        date.today() - timedelta(days=random.randint(1, 730)),
    )
    LESS_THAN_TODAY = (
        "< today",
        0,
        date.today() - timedelta(days=random.randint(1, 1000)),
    )
    LESS_THAN_OR_EQUAL_TO_6_MONTHS_AGO = (
        "<= 6 months ago",
        6,
        date.today() - timedelta(days=random.randint(0, 182)),
    )
    LYNCH_DIAGNOSIS_DATE = ("lynch diagnosis date", 0, None)
    MORE_THAN_2_YEARS_AGO = (
        "more than 2 years ago",
        24,
        date.today() - timedelta(days=730 + random.randint(1, 1000)),
    )
    MORE_THAN_3_YEARS_AGO = (
        "more than 3 years ago",
        36,
        date.today() - timedelta(days=1095 + random.randint(1, 1000)),
    )
    MORE_THAN_6_MONTHS_AGO = (
        "more than 6 months ago",
        6,
        date.today() - timedelta(days=182 + random.randint(1, 1000)),
    )
    MORE_THAN_10_DAYS_AGO = (
        "> 10 days ago",
        0,
        date.today() - timedelta(days=random.randint(11, 1010)),
    )
    MORE_THAN_20_DAYS_AGO = (
        "> 20 days ago",
        0,
        date.today() - timedelta(days=random.randint(21, 1020)),
    )
    NOT_NULL = ("not null", 0, None)
    NULL = ("null", 0, None)
    ONE_YEAR_FROM_DIAGNOSTIC_TEST = ("1 year from diagnostic test", 12, None)
    ONE_YEAR_FROM_EPISODE_END = ("1 year from episode end", 12, None)
    ONE_YEAR_FROM_SYMPTOMATIC_PROCEDURE = (
        "1 year from symptomatic procedure",
        12,
        None,
    )
    THREE_YEARS_FROM_DIAGNOSTIC_TEST = ("3 years from diagnostic test", 36, None)
    THREE_YEARS_FROM_EPISODE_END = ("3 years from episode end", 36, None)
    THREE_YEARS_FROM_SYMPTOMATIC_PROCEDURE = (
        "3 years from symptomatic procedure",
        36,
        None,
    )
    TODAY = ("today", 0, date.today())
    TOMORROW = ("tomorrow", 0, date.today() + timedelta(days=1))
    TWO_YEARS_FROM_DIAGNOSTIC_TEST = ("2 years from diagnostic test", 24, None)
    TWO_YEARS_FROM_EPISODE_END = ("2 years from episode end", 24, None)
    TWO_YEARS_FROM_LAST_LYNCH_COLONOSCOPY_DATE = (
        "2 years from last lynch colonoscopy date",
        24,
        None,
    )
    TWO_YEARS_FROM_LATEST_A37_EVENT = ("2 years from latest A37 event", 24, None)
    TWO_YEARS_FROM_LATEST_J8_EVENT = ("2 years from latest J8 event", 24, None)
    TWO_YEARS_FROM_LATEST_J15_EVENT = ("2 years from latest J15 event", 24, None)
    TWO_YEARS_FROM_LATEST_J16_EVENT = ("2 years from latest J16 event", 24, None)
    TWO_YEARS_FROM_LATEST_J25_EVENT = ("2 years from latest J25 event", 24, None)
    TWO_YEARS_FROM_EARLIEST_S10_EVENT = ("2 years from earliest S10 event", 24, None)
    TWO_YEARS_FROM_LATEST_S158_EVENT = ("2 years from latest S158 event", 24, None)
    TWO_YEARS_FROM_SYMPTOMATIC_PROCEDURE = (
        "2 years from symptomatic procedure",
        24,
        None,
    )
    UNCHANGED = ("unchanged", 0, None)
    UNCHANGED_NULL = ("unchanged (null)", 0, None)
    WITHIN_THE_LAST_2_YEARS = (
        "within the last 2 years",
        24,
        date.today() - timedelta(days=random.randint(0, 730)),
    )
    WITHIN_THE_LAST_4_YEARS = (
        "within the last 4 years",
        48,
        date.today() - timedelta(days=random.randint(0, 1460)),
    )
    WITHIN_THE_LAST_6_MONTHS = (
        "within the last 6 months",
        6,
        date.today() - timedelta(days=random.randint(0, 182)),
    )
    YESTERDAY = ("yesterday", 0, date.today() - timedelta(days=1))

    def __init__(
        self, description: str, number_of_months: int, suitable_date: Optional[date]
    ):
        """
        Initialize a DateDescription enum member.

        Args:
            description (str): The human-readable description of the date logic.
            number_of_months (int): The number of months relevant to the date logic.
            suitable_date (Optional[date]): A calculated or representative date, if applicable.
        """
        self._description = description
        self._number_of_months = number_of_months
        self._suitable_date = suitable_date

    @property
    def description(self) -> str:
        """
        Returns the human-readable description of the date logic.

        Returns:
            str: The description.
        """
        return self._description

    @property
    def number_of_months(self) -> int:
        """
        Returns the number of months relevant to the date logic.

        Returns:
            int: The number of months.
        """
        return self._number_of_months

    @property
    def suitable_date(self) -> Optional[date]:
        """
        Returns a calculated or representative date, if applicable.

        Returns:
            Optional[date]: The suitable date, or None if not applicable.
        """
        return self._suitable_date

    @classmethod
    def by_description(cls, desc: str) -> Optional["DateDescription"]:
        """
        Returns the enum member matching the given description.

        Args:
            desc (str): The description to search for.

        Returns:
            Optional[DateDescription]: The matching enum member, or None if not found.
        """
        return next((d for d in cls if d.description == desc), None)

    @classmethod
    def by_description_case_insensitive(cls, desc: str) -> Optional["DateDescription"]:
        """
        Returns the enum member matching the given description (case-insensitive).

        Args:
            desc (str): The description to search for.

        Returns:
            Optional[DateDescription]: The matching enum member, or None if not found.
        """
        return next((d for d in cls if d.description.lower() == desc.lower()), None)
