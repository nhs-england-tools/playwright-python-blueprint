import pytest
from utils.calendar_picker import CalendarPicker
from datetime import datetime
from playwright.sync_api import Page

pytestmark = [pytest.mark.utils_local]


def test_calculate_v2_calendar_variables(page: Page):
    calendar_picker = CalendarPicker(page)
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
    ) = calendar_picker.calculate_v2_calendar_variables(
        datetime(2025, 4, 9), datetime(2020, 6, 9)
    )

    assert current_month_long == "June"
    assert month_long == "April"
    assert month_short == "Apr"
    assert current_year == 2020
    assert year == 2025
    assert current_decade == 2020
    assert decade == 2020
    assert current_century == 2000
    assert century == 2000

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
    ) = calendar_picker.calculate_v2_calendar_variables(
        datetime(1963, 1, 28), datetime(2020, 6, 9)
    )

    assert current_month_long == "June"
    assert month_long == "January"
    assert month_short == "Jan"
    assert current_year == 2020
    assert year == 1963
    assert current_decade == 2020
    assert decade == 1960
    assert current_century == 2000
    assert century == 1900

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
    ) = calendar_picker.calculate_v2_calendar_variables(
        datetime(2356, 12, 18), datetime(2020, 6, 9)
    )

    assert current_month_long == "June"
    assert month_long == "December"
    assert month_short == "Dec"
    assert current_year == 2020
    assert year == 2356
    assert current_decade == 2020
    assert decade == 2350
    assert current_century == 2000
    assert century == 2300


def test_calculate_years_and_months_to_traverse(page: Page):
    calendar_picker = CalendarPicker(page)
    years_to_traverse, months_to_traverse = (
        calendar_picker.calculate_years_and_months_to_traverse(
            datetime(2356, 12, 18), datetime(2020, 6, 9)
        )
    )
    assert years_to_traverse == -336
    assert months_to_traverse == -6

    years_to_traverse, months_to_traverse = (
        calendar_picker.calculate_years_and_months_to_traverse(
            datetime(2020, 12, 1), datetime(2020, 6, 9)
        )
    )
    assert years_to_traverse == 0
    assert months_to_traverse == -6

    years_to_traverse, months_to_traverse = (
        calendar_picker.calculate_years_and_months_to_traverse(
            datetime(1961, 1, 30), datetime(2020, 6, 9)
        )
    )
    assert years_to_traverse == 59
    assert months_to_traverse == 5
