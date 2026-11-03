from drivers import ButtonDriver
from blinker import Signal

class ButtonService():
    button_driver : ButtonDriver

    _last_button_press : int
    _button_release_event : Signal
    _button_hold_event : Signal
    _button_release_event : Signal

    def __init__(self, button_driver):
        self.button_driver = button_driver
        self.button_driver.subscribe_to_release(self._handle_button_release)
        self.button_driver.subscribe_to_hold(self._handle_button_hold)
        self._button_release_event = Signal("button-release")
        self._button_hold_event = Signal("button-hold")

    def _handle_button_release(self, button_index):
        self._last_button_press = button_index
        self._button_release_event.send(button_index)

    def _handle_button_hold(self, button_index):
        self._button_hold_event.send(button_index)

    def subscribe_to_press(self, callback):
        self._button_press_event.connect(callback)

    def subscribe_to_release(self, callback):
        self._button_release_event.connect(callback)

    def subscribe_to_hold(self, callback):
        self._button_hold_event.connect(callback)