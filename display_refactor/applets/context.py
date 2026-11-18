from typing import Callable
from dataclasses import dataclass

@dataclass
class AppletContext():
    request_redraw: Callable[[], None]