from dataclasses import dataclass
from abc import abstractmethod, ABC
from typing import Any
from applets.context import AppletContext
from drivers.button_driver import ButtonEvent

@dataclass
class View:
    template: str
    context: dict[str, Any]

class Applet(ABC):
    id: str
    name: str

    def __init__(self, config: dict, context: AppletContext):
        self.config = config
        self.context = context

    def on_start(self) -> None:
        pass

    def on_activate(self) -> None:
        pass

    def on_deactivate(self) -> None:
        pass

    def on_stop(self) -> None:
        pass

    def on_button(self, press_event: ButtonEvent) -> None:
        pass

    def refresh(self) -> None:
        pass

    @abstractmethod
    def build_view(self) -> View:
        pass

    def build_preview(self) -> View | None:
        pass

    def load_template_file(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            file.close()
        return content