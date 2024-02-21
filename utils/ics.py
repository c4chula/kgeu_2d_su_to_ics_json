from icalendar import Calendar, Event
from .schema import EventInfo


class ENERSv2ICalendar:

    def __init__(self, events: list[EventInfo]) -> None:
        self.cal = Calendar()
        self.cal.add("VERSION", "2.0")
        self.cal.add("PRODID", "EnersV2-ics")
        for event in events:
            ical_event = Event()
            ical_event.add("SUMMARY", f"{event.subject}")
            ical_event.add("DTSTART", event.start_datetime)
            ical_event.add("DTEND", event.end_datetime)
            ical_event.add("DESCRIPTION", f"{event.teacher}\n{event.auditory}")
            self.cal.add_component(ical_event)

    def create_ics_file(self) -> None:
        with open("file.ics", "+wb") as f:
            f.write(self.cal.to_ical())
