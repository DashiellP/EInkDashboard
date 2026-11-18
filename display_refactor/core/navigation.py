from applets.base import Applet, AppletContext
from applets.weather.applet import WeatherApplet
from drivers.button_driver import ButtonEventKind

class Navigation():
    HOME_BUTTON = 0
    _current_applet: Applet | None = None
    _applet_context: AppletContext

    def __init__(self, applet_context: AppletContext):
        self._applet_context = applet_context

    def handle_button_event(self, button_event):
        print(button_event)
        print(self._current_applet)
        if (not self.is_home() and button_event.index == self.HOME_BUTTON and button_event.kind == ButtonEventKind.HOLD):
            self.go_home()
        elif (self.is_home() and button_event.kind == ButtonEventKind.TAP):
            self.open_applet(f"test_{button_event.index}")

    def go_home(self):
        print("home")
        if self._current_applet is not None:
            self._current_applet.on_stop()
        self._current_applet = None

    def open_applet(self, applet_id: str):
        if self._current_applet is not None:
            self._current_applet.on_stop()
        print(applet_id)
        self._current_applet = WeatherApplet({}, self._applet_context)
        self._current_applet.on_start()

    def is_home(self):
        return self._current_applet is None

    def get_current_view(self):
        if self._current_applet is not None:
            return self._current_applet.build_view()
        