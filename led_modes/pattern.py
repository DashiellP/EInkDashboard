from .led_mode import LedMode
from time import sleep

class Pattern(LedMode):
    _pattern = []
    _loop = False

    def __init__(self, pattern, loop=False):
        pattern.append((0,0))
        self._pattern = pattern
        self._loop = loop

    def apply(self, led):
        while (True):
            for state,duration in self._pattern:
                if (state):
                    led.on()
                else:
                    led.off()
                if (duration > 0):
                    sleep(duration)
            if (not self._loop):
                break