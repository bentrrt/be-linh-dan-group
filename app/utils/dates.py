"""Small date helpers (no external dependencies)."""

from calendar import monthrange
from datetime import date


def add_one_month(value: date) -> date:
    """Return the date one calendar month after `value`.

    Clamps the day to the last valid day of the target month
    (e.g. Jan 31 + 1 month -> Feb 28/29).
    """
    month = value.month + 1
    year = value.year + (month - 1) // 12
    month = (month - 1) % 12 + 1

    days_in_month = monthrange(year, month)[1]
    day = min(value.day, days_in_month)
    return date(year, month, day)
