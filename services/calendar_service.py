import requests
from caldav import DAVClient
from icalendar import Calendar, Event
from datetime import datetime, timedelta
from config import config

class CalendarService():
    _user : str
    _password : str

    _icloud_calendar_endpoint = "https://caldav.icloud.com/"
    _additional_calendar_endpoints = ["https://ics.calendarlabs.com/76/38c3b14f/US_Holidays.ics"]

    def __init__(self):
        self._user = config.ICLOUD_USER
        self._password = config.ICLOUD_PASSWORD

    def get_calendar_data(self):
        return self.get_icloud_calendar_data() + self.get_additional_calendar_data()

    def get_icloud_calendar_data(self):
        client = DAVClient(
            url=self._icloud_calendar_endpoint,
            username=self._user,
            password=self._password
        )
        principal = client.principal()
        calendars = principal.calendars()
        today = datetime.now()
        start = today - timedelta(days=31)
        end = today + timedelta(days=31)
        formatted_events = []
        for calendar in calendars:
            events = calendar.date_search(start, end)
            for event in events:
                ical = event.icalendar_component
                summary = ical.get('SUMMARY')
                dtstart = ical.get('DTSTART').dt
                dtend = ical.get('DTEND').dt
                formatted_events.append({
                    "title": "".join(summary),
                    "start": dtstart.isoformat(),
                    "end": dtend.isoformat()
                })
        return formatted_events

    def get_additional_calendar_data(self):
        events = []
        for endpoint in self._additional_calendar_endpoints:
            response = requests.get(endpoint)
            if (200 <= response.status_code < 300):
                calendar = Calendar.from_ical(response.text)
                for component in calendar.walk():
                    if component.name == "VEVENT":
                        events.append({
                            "title": "".join(component.get('summary')),
                            "start": component.get('dtstart').dt.isoformat(),
                            "end": component.get('dtend').dt.isoformat()
                        })
        return events

