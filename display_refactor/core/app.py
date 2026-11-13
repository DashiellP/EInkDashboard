import drivers as Drivers
from navigation import Navigation

class App():
    _led_driver : Drivers.LedDriver
    _display_driver : Drivers.DisplayDriver
    _button_driver : Drivers.ButtonDriver

    _screen_dimensions = (0,0)
    
    def __init__(self):
        self._led_driver = Drivers.LedDriver()
        self._display_driver = Drivers.DisplayDriver()
        self._button_driver = Drivers.ButtonDriver()
        self._navigation = Navigation()

        self._button_driver.subscribe_to_input(self._handle_button_press)

    def _handle_button_press(self, button_event: Drivers.ButtonDriver.ButtonEvent):
        print(button_event)

    def run(self):
        while True:
            pass