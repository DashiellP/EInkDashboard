import led_mode as LedMode
from .app_state import AppState

led_mode_for_states = {
    AppState.IDLE: LedMode.Off,
    AppState.WORKING: LedMode.Pulse
}