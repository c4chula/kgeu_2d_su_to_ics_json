from dataclasses import dataclass
from typing import Annotated, Literal
from datetime import datetime
from pydantic import BaseModel, AliasPath, ConfigDict


@dataclass(slots=True)
class EnersV2ApiData:

    domain: str
    route: str
    group_name: str

    def __str__(self) -> str:
        return f"{self.domain}{self.route}"


@dataclass(slots=True)
class DayInfo:
    status: Literal["success", "error"]
    events: list["EventInfo"]


@dataclass(slots=True)
class EventInfo:
    start_datetime: datetime
    end_datetime: datetime
    subject: str
    teacher: str
    auditory: str
