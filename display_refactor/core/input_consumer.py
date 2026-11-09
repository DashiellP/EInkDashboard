import abc

class InputConsumer(abc.ABC):
    event_bindings: dict[(str, int), callable]

    @abc.abstractmethod
    def handle_input(self, input_event):
        return True