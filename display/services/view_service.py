from services import DisplayService
from image_generators import ImageGenerator

class ViewService():
    _display_service: DisplayService
    _registered_views = {}
    _current_view: ImageGenerator

    _screen_dimensions = None

    def __init__(self, display_service: DisplayService):
        self._display_service = display_service

    def set_dimensions(self, screen_dimensions):
        self._screen_dimensions = screen_dimensions

    def register_view(self, view_name: str, view: ImageGenerator):
        self._registered_views[view_name] = view

    def set_view(self, view_name: str):
        self._current_view = self._registered_views[view_name](self._screen_dimensions)

    def render_view(self):
        image = self._current_view.generate()
        self._display_service.update_image(image)