import functools
import operator
from typing import Any, Callable, Generator
from datetime import datetime
from typing import AsyncGenerator
from aiohttp import ClientSession
from contextlib import asynccontextmanager
from .dateutils import (
    get_current_week_dates,
    get_current_date,
    one_week_delta,
    get_current_month_dates,
    one_month_delta,
)
import asyncio
from pprint import pprint
import itertools
from .schema import EnersV2ApiData, EventInfo


@asynccontextmanager
async def get_client_session() -> AsyncGenerator[ClientSession, None]:
    async with ClientSession(
        headers={
            "Content-type": "application/json",
        }
    ) as session:
        yield session


class EnersV2Api:

    api_data: EnersV2ApiData

    current_week_gen: Callable[[], Generator[datetime, None, None]] = functools.partial(
        get_current_week_dates, get_current_date()
    )
    next_week_gen: Callable[[], Generator[datetime, None, None]] = functools.partial(
        get_current_week_dates, get_current_date() + one_week_delta
    )
    current_month_gen: Callable[[], Generator[datetime, None, None]] = (
        functools.partial(get_current_month_dates, get_current_date())
    )
    next_month_gen: Callable[[], Generator[datetime, None, None]] = functools.partial(
        get_current_month_dates, get_current_date() + one_month_delta
    )

    def __init__(self, api_data: EnersV2ApiData) -> None:
        self.api_data = api_data

    async def _get_request(self, session: ClientSession, params: dict) -> str:
        resp = await session.get(
            str(self.api_data),
            params=params,
        )
        return await resp.json(content_type=None)

    async def _request_tasks(
        self, date_gen: Callable[[], Generator[datetime, None, None]]
    ) -> list[dict[str, Any]]:
        async with get_client_session() as session:
            tasks = []
            for date in date_gen():
                tasks.append(
                    self._get_request(
                        session,
                        {
                            "date": str(date.date()),
                            "group": self.api_data.group_name,
                        },
                    )
                )

            data = await asyncio.gather(*tasks)
            pprint(data)
            return data

    def _request_to_model(self, data: list[dict[str, Any]]) -> list[EventInfo]:
        return [
            EventInfo(
                start_datetime=datetime.strptime(
                    f"{date_str} {event['start_time']}",
                    "%Y-%m-%d %H:%M",
                ),
                end_datetime=datetime.strptime(
                    f"{date_str} {event['end_time']}",
                    "%Y-%m-%d %H:%M",
                ),
                subject="%s %s" % (event["type"], event["subject"]),
                teacher=event["teacher"],
                auditory=event["auditory"],
            )
            for event, date_str in [
                (event, list(sublist["schedule"].items())[0][0]) 
                for sublist in data
                if sublist["status"] == "success"
                for event in list(sublist["schedule"].items())[0][1]
            ]
        ]

    async def get_current_week_schedule(self) -> list[EventInfo]:
        data = self._request_to_model(await self._request_tasks(self.current_week_gen))
        return data

    async def get_next_week_schedule(self) -> list[EventInfo]:
        data = self._request_to_model(await self._request_tasks(self.next_week_gen))
        return data

    async def get_current_month_schedule(self) -> list[EventInfo]:
        data = self._request_to_model(await self._request_tasks(self.current_month_gen))
        return data

    async def get_next_month_schedule(self) -> list[EventInfo]:
        data = self._request_to_model(await self._request_tasks(self.next_month_gen))
        return data
