from blinker import signal
from utils.app_state import AppState

class StateManager():
    _state = AppState.IDLE
    _state_change_event = signal("state-change")

    _children = []

    def set_state(self, new_state):
        print(self.__class__.__name__ + " became " + new_state.name)
        if (self._state != new_state):
            self._state = new_state
            self._state_change_event.send(self._state)

    def set_state_to_idle(self):
        self.set_state(AppState.IDLE)

    def set_state_to_working(self):
        self.set_state(AppState.WORKING)

    def set_state_to_error(self):
        self.set_state(AppState.ERROR)

    def get_state(self):
        if (len(self._children) == 0):
            return self._state
        return self._get_state_from_children()

    def subscribe_to_state_change(self, callback):
        self._state_change_event.connect(callback)

    def add_child(self, state_manager):
        self._children.append(state_manager)

    def _get_state_from_children(self):
        overall_state = AppState(max(self._state.value, (child.get_state().value for child in self._children)))
        return overall_state