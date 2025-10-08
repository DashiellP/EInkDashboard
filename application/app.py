import services as Services
import drivers as Drivers
from utils.state_manager import StateManager
from utils.app_state import AppState
import image_generators as ImageGenerators
import datetime
from time import sleep

class App():
    _led_service : Services.LedService
    _display_service : Services.DisplayService
    _button_service : Services.ButtonService
    
    _led_driver : Drivers.LedDriver
    _display_driver : Drivers.DisplayDriver
    _button_driver : Drivers.ButtonDriver

    state_manager : StateManager

    _screen_dimensions = (0,0)

    _last_update = 0
    _time_between_updates = 600
    
    def __init__(self):
        self.state_manager = StateManager()

        self._led_driver = Drivers.LedDriver()
        self._display_driver = Drivers.DisplayDriver()
        self._button_driver = Drivers.ButtonDriver()

        self._led_service = Services.LedService(self._led_driver)
        self._display_service = Services.DisplayService(self._display_driver)
        self._button_service = Services.ButtonService(self._button_driver)

        self._screen_dimensions = self._display_driver.get_display_info()["dimensions"]

        self.state_manager.add_child(self._display_service.state_manager)
        self.state_manager.subscribe_to_state_change(self._handle_state_change)

        self._init_event_listeners()

    def _init_event_listeners(self):
        self._button_service.subscribe_to_press(self._handle_button_press)
        
    def _handle_button_press(self, button_index):
        match button_index:
            case 0:
                self._update_image(ImageGenerators.RandomScreenshotGenerator())
            case 1:
                self._update_image(ImageGenerators.WeatherGenerator())
            case 2:
                self._update_image(ImageGenerators.TestPageGenerator())
            case 3:
                self._update_image(ImageGenerators.CalendarGenerator(Services.CalendarService()))

    def _handle_state_change(self, new_state):
        match new_state:
            case AppState.WORKING:
                self._led_service.show_working()
            case AppState.IDLE:
                self._led_service.show_ready()

    def _update_image(self, image_generator):
        try:
            self.state_manager.set_state_to_working()
            self._display_service.update_image(image_generator.generate())
            self.state_manager.set_state_to_idle()
        except Exception as exception:
            self.state_manager.set_state_to_working()
            self._display_service.update_image(ImageGenerators.ErrorPageGenerator(self._screen_dimensions).generate(exception))
            self.state_manager.set_state_to_idle()

    def run(self):
        try:
            while True:
                current_datetime = datetime.datetime.now()
                if (current_datetime.timestamp() >= self._last_update + self._time_between_updates):
                    self._last_update = current_datetime.timestamp()
                    self._update_image(ImageGenerators.RandomScreenshotGenerator())
                sleep(10)
                
        except Exception as e:
            exception_name = type(e).__name__
            exception_description = str(e)  
            self.state_manager.set_state_to_working()
            self._display_service.update_image(ImageGenerators.ErrorPageGenerator((800,480)).generate(e))
            self.state_manager.set_state_to_idle()