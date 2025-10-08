import led_modes as LedMode

class LedService():
    _led_driver = None

    def __init__(self, led_driver):
        self._led_driver = led_driver

    def update_led(self, led_mode):
        self._led_driver.set_led_mode(led_mode)

    def show_idle(self):
        self._led_driver.set_led_mode(LedMode.Off())

    def show_working(self):
        self._led_driver.set_led_mode(LedMode.Pulse(fade_in_time=1, fade_out_time=0.33))

    def show_ready(self):
        pattern = [(0,0.15),(1,0.15),(0,0.15),(1,0.15),(0,0.15),(1,0.15)]
        self._led_driver.set_led_mode(LedMode.Pattern(pattern))

    def show_error(self):
        pattern = [(0,0.15),(1,0.15),(0,0.15),(1,0.15),(0,0.15),(1,0.15)]
        self._led_driver.set_led_mode(LedMode.Pattern(pattern))