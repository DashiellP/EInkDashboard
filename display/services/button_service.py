from drivers import ButtonDriver

class ButtonService():
    button_driver : ButtonDriver

    _global_button_press_callbacks      = [None, None, None, None]
    _global_button_hold_callbacks       = [None, None, None, None]
    _global_button_release_callbacks    = [None, None, None, None]

    _local_button_press_callbacks       = [None, None, None, None]
    _local_button_hold_callbacks        = [None, None, None, None]
    _local_button_release_callbacks     = [None, None, None, None]

    def __init__(self, button_driver):
        self.button_driver = button_driver
        self.button_driver.subscribe_to_press(self._handle_button_press)
        self.button_driver.subscribe_to_release(self._handle_button_release)
        self.button_driver.subscribe_to_hold(self._handle_button_hold)

    def _handle_button_press(self, button_index):
        self._handle_button_event("press", button_index)

    def _handle_button_hold(self, button_index):
        self._handle_button_event("hold", button_index)

    def _handle_button_release(self, button_index):
        self._handle_button_event("release", button_index)

    def _handle_button_event(self, event_type, button_index):
        match event_type:
            case "press":
                global_callback_array = self._global_button_press_callbacks
                local_callback_array = self._local_button_press_callbacks
            case "hold":
                global_callback_array = self._global_button_hold_callbacks
                local_callback_array = self._local_button_hold_callbacks
            case "release":
                global_callback_array = self._global_button_release_callbacks
                local_callback_array = self._local_button_release_callbacks
        if (global_callback_array[button_index]):
            global_callback_array[button_index]()
        elif (local_callback_array[button_index]):
            local_callback_array[button_index]()

    def clear_global_callbacks(self):
        self._global_button_press_callbacks      = [None, None, None, None]
        self._global_button_hold_callbacks       = [None, None, None, None]
        self._global_button_release_callbacks    = [None, None, None, None]

    def clear_local_callbacks(self):
        self._local_button_press_callbacks       = [None, None, None, None]
        self._local_button_hold_callbacks        = [None, None, None, None]
        self._local_button_release_callbacks     = [None, None, None, None]

    def register_button_press(self, button_index, trigger_mode, is_global, callback):
        match trigger_mode:
            case "press":
                (self._global_button_press_callbacks if is_global else self._local_button_press_callbacks)[button_index] = callback
            case "hold":
                (self._global_button_hold_callbacks if is_global else self._local_button_hold_callbacks)[button_index] = callback
            case "release":
                (self._global_button_release_callbacks if is_global else self._local_button_release_callbacks)[button_index] = callback
            