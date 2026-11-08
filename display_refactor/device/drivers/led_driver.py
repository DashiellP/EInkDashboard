from gpiozero import PWMLED
import threading
from time import sleep

class LedDriver:
    _LED_PIN = 13
    _led = None
    _led_thread = None
    
    _led_mode = None
    _is_led_mode_dirty = False

    def __init__(self):
        self._led = PWMLED(self._LED_PIN)
        self._led_thread = threading.Thread(target=self._hold_led_mode)
        self._led_thread.start()

    def __del__(self):
        self._led_thread.join()

    def set_led_mode(self, new_state) -> None:
        self._led_mode = new_state
        self._is_led_mode_dirty = True

    def _hold_led_mode(self) -> None:
        while (True):
            self._is_led_mode_dirty = False
            if (self._led_mode is not None):
                self._led_mode.apply(self._led)
            while (not self._is_led_mode_dirty):
                sleep(0.25)
