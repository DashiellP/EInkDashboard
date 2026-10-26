from gpiozero import Button
from blinker import signal

class ButtonDriver():
    _button_pins = {
        5: 0,
        6: 1,
        16: 2,
        24: 3,
    }

    _button_bounce_time = 0.1

    buttons = []

    _on_press = signal("on-press")
    _on_release = signal("on-release")

    def __init__(self):
        for pin in self._button_pins:
            button = Button(pin=pin, bounce_time=self._button_bounce_time)
            self.buttons.append(button)
            button.when_pressed = lambda button : self.handle_button_event(button, True)
            button.when_released = lambda button : self.handle_button_event(button, False)

    def subscribe_to_press(self, callback):
        self._on_press.connect(callback)

    def subscribe_to_release(self, callback):
        self._on_release.connect(callback)

    def handle_button_event(self, button, is_press):
        button_index = self._button_pins[button.pin.number]
        if (is_press):
            print("BUTTON PRESS")
            self._on_press.send(button_index)
        else:
            self._on_release.send(button_index)