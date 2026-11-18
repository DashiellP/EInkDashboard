from applets.base import Applet, View
from datetime import datetime
from time import time
from core.config import config
import requests


class WeatherApplet(Applet):
    id = "weather"
    name = "Weather"

    background_url = f"https://cdns.abclocal.go.com/three/kabc/webcam/web2-1.jpg?w=630&r=16%3A9&t={time()}"

    text_fill_colors = {
        0: "#120088",
        6: "#72002f",
        10: "#ff9100",
        18: "#72002f",
        20: "#5C008B",
    }

    text_stroke_colors = {
        0: "#424242",
        6: "#FFFFFF",
        10: "#FFFFFF",
        18: "#828282",
        20: "#828282",
    }
    
    def on_start(self) -> None:
        self.context.request_redraw()

    def build_view(self):
        template = self.load_template_file("applets/weather/templates/full.html")

        # todo: separate data collection and rendering
        weather_data = self.get_weather_data(config.OPEN_WEATHER_MAP_API_KEY)
        text_colors = self.get_current_text_colors()
        now = datetime.now()
        hour = (now.hour - 1) % 12 + 1
        formatted_time = str(hour) + now.strftime(":%M %p")
        formatted_date = now.strftime("%A, %m/%-d/%Y")
        context = {
            "background_url": self.background_url,
            "weather_icon": weather_data['weather_icon'],
            "temperature": weather_data['temperature'],
            "weather_type": weather_data['weather_type'],
            "formatted_time": formatted_time,
            "formatted_date": formatted_date,
            "text_top_color": text_colors['text_top_color'],
            "text_bottom_color": text_colors['text_bottom_color'],
            "stroke_color": text_colors['stroke_color'],   
            "text_top_color": text_colors['text_top_color'],
            "text_bottom_color": text_colors['text_bottom_color'],
            "stroke_color": text_colors['stroke_color']
        }

        return View(
            template,
            context
        )

    def fetch_data(self):
        pass

    def get_weather_data(self, api_key):
        url = "https://api.openweathermap.org/data/2.5/weather"

        response = requests.get(
            url,
            params={
                "q": "huntington beach,us",
                "units": "imperial",
                "appid": api_key,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        result = {
            "temperature": round(data["main"]["temp"]),
            "weather_icon": (
                "https://openweathermap.org/img/wn/"
                f"{data['weather'][0]['icon']}@2x.png"
            ),
            "weather_type": data["weather"][0]["main"],
        }
        return result


    def get_text_colors(self, current_time):
        times = sorted(self.text_fill_colors)

        prev_time = times[-1]
        next_time = 24

        for hour in times:
            if hour <= current_time:
                prev_time = hour
            elif hour > current_time:
                next_time = hour
                break

        return {
            "text_top_color": self.text_fill_colors[prev_time],
            "text_bottom_color": self.text_fill_colors[
                0 if next_time == 24 else next_time
            ],
            "stroke_color": self.text_stroke_colors[prev_time],
            "prev_time": prev_time,
            "next_time": next_time,
        }


    def interpolate_color(self, color1, color2, t):
        t = max(0.0, min(1.0, t))

        c1 = bytes.fromhex(color1.lstrip("#"))
        c2 = bytes.fromhex(color2.lstrip("#"))

        rgb = [
            round(a + (b - a) * t)
            for a, b in zip(c1, c2)
        ]

        return "#{:02X}{:02X}{:02X}".format(*rgb)


    def get_current_text_colors(self, delta_t=0.07, now=None):
        if now is None:
            now = datetime.now()

        current_hour = now.hour + now.minute / 60

        color_data = self.get_text_colors(current_hour)

        t1 = (
            (current_hour - color_data["prev_time"])
            / (color_data["next_time"] - color_data["prev_time"])
        )
        t2 = t1 + delta_t

        return {
            "text_bottom_color": self.interpolate_color(
                color_data["text_top_color"],
                color_data["text_bottom_color"],
                t1,
            ),
            "text_top_color": self.interpolate_color(
                color_data["text_top_color"],
                color_data["text_bottom_color"],
                t2,
            ),
            "stroke_color": color_data["stroke_color"],
        }