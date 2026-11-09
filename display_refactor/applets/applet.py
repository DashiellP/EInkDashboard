from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Mapping, Protocol

class RenderMode(Enum):
    FULL = 0
    PREVIEW = 1

@dataclass(frozen=True)
class View:
    template: str
    context: Mapping[str, object]

class Applet(Protocol):
    id: str
    title: str
    current_view: View

    def build_view(self, render_mode: RenderMode):
        pass