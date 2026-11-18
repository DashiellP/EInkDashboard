import drivers as Drivers
from core.navigation import Navigation
from applets.context import AppletContext
from core.renderer import Renderer

class App():
    _led_driver: Drivers.LedDriver
    _display_driver: Drivers.DisplayDriver
    _button_driver: Drivers.ButtonDriver

    _renderer: Renderer
    
    def __init__(self):
        self._led_driver = Drivers.LedDriver()
        self._display_driver = Drivers.DisplayDriver()
        self._button_driver = Drivers.ButtonDriver()
        self._navigation = Navigation(AppletContext(request_redraw=self.request_redraw))
        
        self._renderer = Renderer(self._display_driver)
        self._button_driver.subscribe_to_input(self._handle_button_press)

    def _handle_button_press(self, button_event: Drivers.button_driver.ButtonEvent):
        self._navigation.handle_button_event(button_event)

    def run(self):
        while True:
            pass

    def request_redraw(self):
        view = self._navigation.get_current_view()
        self._renderer.render_view(view)