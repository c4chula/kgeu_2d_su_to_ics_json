from datetime import datetime, timedelta
from calendar import monthrange
from typing import Generator

one_week_delta = timedelta(days=7)
one_month_delta = timedelta(days=30)


def get_current_date() -> datetime:
    return datetime.today()


def get_current_week_dates(date: datetime) -> Generator[datetime, None, None]:
    days_delta = date.weekday() % 7
    monday = date - timedelta(days=days_delta)
    date = monday
    for _ in range(7):
        yield date
        date += timedelta(days=1)


def get_current_month_dates(date: datetime) -> Generator[datetime, None, None]:
    days_count = monthrange(date.year, date.month)[1]
    current_date = date
    for _ in range(1, days_count + 1):
        yield current_date
