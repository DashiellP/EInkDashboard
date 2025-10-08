from .led_mode import LedMode

class On(LedMode):
    def apply(self, led):
        led.on()