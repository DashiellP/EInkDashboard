from .led_mode import LedMode

class Off(LedMode):
    def apply(self, led):
        led.off()