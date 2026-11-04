from services import DisplayService
from image_generators import ImageGenerator, ErrorPageGenerator
from utils.state_manager import StateManager

class ViewService():
    _display_service: DisplayService
    _state_manager: StateManager
    
    _registered_views = {}
    _current_view: ImageGenerator

    _screen_dimensions = None

    def __init__(self, display_service: DisplayService, state_manager: StateManager):
        self._display_service = display_service
        self._state_manager = state_manager

    def set_dimensions(self, screen_dimensions):
        self._screen_dimensions = screen_dimensions

    def register_view(self, view_name: str, view: ImageGenerator):
        self._registered_views[view_name] = view

    def set_view(self, view_name: str):
        try:
            self._state_manager.set_state_to_working()
            self._current_view = self._registered_views[view_name](self._screen_dimensions)
            self.render_view()
            self._state_manager.set_state_to_idle()
        except Exception as exception:
            self.show_error(exception)

    def render_view(self):
        image = self._current_view.generate()
        self._display_service.update_image(image)

    def show_error(self, exception):
        self.state_manager.set_state_to_working()
        self._display_service.update_image(ErrorPageGenerator(self._screen_dimensions).generate(exception))
        self.state_manager.set_state_to_idle()