from drivers import ButtonDriver
from blinker import Signal

class ButtonService():
    button_driver : ButtonDriver

    _last_button_press : int
    _button_press_event : Signal

    def __init__(self, button_driver):
        self.button_driver = button_driver
        self.button_driver.subscribe_to_press(self.handle_button_press)
        self._button_press_event = Signal("button-press")

    def handle_button_press(self, button_index):
        self._last_button_press = button_index
        self._button_press_event.send(button_index)

    def subscribe_to_press(self, callback):
        self._button_press_event.connect(callback)