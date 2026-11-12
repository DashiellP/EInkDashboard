from applets.base import Applet

class Navigation():
    _current_applet: Applet | None = None

    def go_home(self):
        pass

    def open_applet(self, applet_id: str):
        pass

    def is_home(self):
        return self._current_applet is not None