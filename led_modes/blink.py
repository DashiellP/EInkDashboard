from .led_mode import LedMode

class Blink(LedMode):
    def apply(self, led):
        led.blink()