import requests
import json
import urllib.parse

from config import config
from image_generators.image_generator import ImageGenerator

class CalendarGenerator(ImageGenerator):
    _screenshot_endpoint = config.SERVER_URL + "node/calendar?key=" + config.SECRET_KEY
    _calendar_service = None

    def __init__(self, calendar_service):
        self._calendar_service = calendar_service

    def generate(self):
        event_data = self._calendar_service.get_calendar_data()
        event_string = urllib.parse.quote(json.dumps(event_data))
        return super().get_image_from_uri(self._screenshot_endpoint + "&events=" + event_string)