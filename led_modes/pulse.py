from .led_mode import LedMode

class Pulse(LedMode):
    _led_args = None

    def __init__(self, **kwargs):
        self._led_args = kwargs

    def apply(self, led):
        led.pulse(**self._led_args)