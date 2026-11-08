from gpiozero import Button
from blinker import signal
import asyncio
from enum import Enum

class ButtonDriver():
    _button_pins = {
        5: 0,
        6: 1,
        16: 2,
        24: 3,
    }

    _button_states = [0, 0, 0, 0]

    _button_bounce_time = 0.1
    _button_hold_time = 2

    buttons = []

    _on_press = signal("on-press")
    _on_release = signal("on-release")
    _on_hold = signal("on-hold")

    def __init__(self):
        for pin in self._button_pins:
            button = Button(pin=pin, bounce_time=self._button_bounce_time, hold_time=self._button_hold_time)
            self.buttons.append(button)
            button.when_pressed = lambda button : self.handle_button_press(button)
            button.when_held = lambda button : self.handle_button_hold(button)
            button.when_released = lambda button : self.handle_button_release(button)

    def is_down(self, button_index):
        return self._button_states[button_index]

    def subscribe_to_press(self, callback):
        self._on_press.connect(callback)

    def subscribe_to_release(self, callback):
        self._on_release.connect(callback)

    def subscribe_to_hold(self, callback):
        self._on_hold.connect(callback)

    def unsubscribe_from_press(self, callback):
        self._on_press.disconnect(callback)

    def unsubscribe_from_release(self, callback):
        self._on_release.disconnect(callback)

    def unsubscribe_from_hold(self, callback):
        self._on_hold.disconnect(callback)

    def handle_button_press(self, button):
        button_index = self._button_pins[button.pin.number]
        self._button_states[button_index] = ButtonState.DOWN
        self._on_press.send(button_index)
    
    def handle_button_hold(self, button):
        button_index = self._button_pins[button.pin.number]
        self._button_states[button_index] = ButtonState.HOLD
        self._on_hold.send(button_index)

    def handle_button_release(self, button):
        button_index = self._button_pins[button.pin.number]
        if self._button_states[button_index] != ButtonState.HOLD:
            self._on_release.send(button_index)
        self._button_states[button_index] = ButtonState.UP

class ButtonState(Enum):
    UP = 0
    DOWN = 1
    HOLD = 2