import pytest
import utils.date_time_utils
from datetime import datetime, timedelta

pytestmark = [pytest.mark.utils]


def test_current_datetime():
    dtu = utils.date_time_utils.DateTimeUtils()
    current_date = datetime.now()
    assert dtu.current_datetime() == current_date.strftime("%d/%m/%Y %H:%M")
    assert dtu.current_datetime("%Y-%m-%d %H:%M") == current_date.strftime(
        "%Y-%m-%d %H:%M"
    )
    assert dtu.current_datetime("%d %B %Y %H:%M") == current_date.strftime(
        "%d %B %Y %H:%M"
    )


def test_format_date():
    dtu = utils.date_time_utils.DateTimeUtils()
    date = datetime(2022, 12, 31)
    assert dtu.format_date(date, "%d/%m/%Y") == "31/12/2022"
    assert dtu.format_date(date, "%Y/%m/%d") == "2022/12/31"
    assert dtu.format_date(date, "%d %B %Y") == "31 December 2022"


def test_add_days():
    dtu = utils.date_time_utils.DateTimeUtils()
    date = datetime.now()
    new_date = dtu.add_days(date, 5)
    assert new_date == date + timedelta(days=5)


def test_get_day_of_week_for_today():
    dtu = utils.date_time_utils.DateTimeUtils()
    date = datetime.now()
    day_of_week = dtu.get_a_day_of_week(date)
    assert day_of_week in [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]


def test_get_a_day_of_week():
    dtu = utils.date_time_utils.DateTimeUtils()
    date = datetime(2023, 11, 8)
    day_of_week = dtu.get_a_day_of_week(date)
    assert day_of_week in [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
