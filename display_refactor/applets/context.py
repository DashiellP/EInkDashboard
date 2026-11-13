from typing import Callable

class AppletContext():
    request_redraw: Callable[[], None]