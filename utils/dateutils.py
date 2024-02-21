from datetime import datetime, timedelta
from pytz import timezone
from calendar import monthrange
from typing import Generator

one_day_delta = timedelta(days=1)
one_week_delta = timedelta(days=7)
one_month_delta = timedelta(days=30)


def get_current_date() -> datetime:
    return datetime.now(tz=timezone("Europe/Moscow"))


def get_current_week_dates(date: datetime) -> Generator[datetime, None, None]:
    days_delta = date.weekday() % 7
    monday = date - timedelta(days=days_delta)
    date = monday
    for _ in range(7):
        yield date
        date += timedelta(days=1)


def get_current_month_dates(date: datetime) -> Generator[datetime, None, None]:
    days_count = monthrange(date.year, date.month)[1]
    current_date = date.replace(day=1)
    for _ in range(days_count):
        yield current_date
        current_date += one_day_delta


if __name__ == "__main__":
    print(
        [
            date.strftime("%Y%m%dZT%H%M%SZ%z")
            for date in get_current_month_dates(get_current_date())
        ]
    )
