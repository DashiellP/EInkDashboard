from gpiozero import Button
from blinker import signal
from dataclasses import dataclass
from enum import Enum

class ButtonEventKind(Enum):
    TAP = 0
    HOLD = 1

@dataclass(frozen=True)
class ButtonEvent():
    kind: ButtonEventKind
    index: int
    held_time: float

class ButtonDriver():
    _button_pins = {
        5: 0,
        6: 1,
        16: 2,
        24: 3,
    }

    _button_bounce_time = 0.1
    _button_hold_time = 2

    buttons = []

    _on_input = signal("on-input")

    def __init__(self):
        for pin in self._button_pins:
            button = Button(pin=pin, bounce_time=self._button_bounce_time, hold_time=self._button_hold_time)
            self.buttons.append(button)
            button.when_held = lambda button : self._handle_button_hold(button)
            button.when_released = lambda button : self._handle_button_release(button)

    def subscribe_to_input(self, callback):
        self._on_input.connect(callback)

    def unsubscribe_from_input(self, callback):
        self._on_input.disconnect(callback)
    
    def _handle_button_hold(self, button):
        button_index = self._button_pins[button.pin.number]
        self._on_input.send(ButtonEvent(ButtonEventKind.HOLD, button_index, button.active_time))

    def _handle_button_release(self, button):
        button_index = self._button_pins[button.pin.number]
        if self.buttons[button_index].active_time is None:
            self._on_input.send(ButtonEvent(ButtonEventKind.TAP, button_index, button.active_time))