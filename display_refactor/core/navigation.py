from applets.base import Applet

class Navigation():
    _current_applet: Applet | None = None

    def handle_button_event(self, button_event):
        if (not self.is_home() and button_event.kind == ButtonEventKind.HOLD):
            self.go_home()
        elif (self.is_home() and button_event.kind == ButtonEventKind.TAP):
            self.open_applet("test")

    def go_home(self):
        print("home")

    def open_applet(self, applet_id: str):
        print(applet_id)

    def is_home(self):
        return self._current_applet is not None