from ast import List
from ics.icalendar import Calendar
from ics.event import Event
from .schema import EventInfo


class ENERSv2ICalendar:

    def __init__(self, events: list[EventInfo]) -> None:
        self.cal = Calendar()
        for event in events:
            self.cal.events.add(
                Event(
                    name=f"{event.subject}",
                    begin=event.start_datetime.isoformat(),
                    end=event.end_datetime.isoformat(),
                    description=f"{event.teacher}\n{event.auditory}",
                )
            )

    def create_ics_file(self) -> None:
        with open("file.ics", "+w") as f:
            f.writelines(self.cal.serialize_iter())