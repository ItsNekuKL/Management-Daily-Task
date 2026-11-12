"""
hotkeys.py — Global hotkey listener for the skipper.

Runs in a dedicated daemon thread and signals the main loop through
``SharedState`` events.  Uses the standard ``logging`` module so that
state transitions appear in the log with timestamps.
"""

import logging
from threading import Event
from typing import Union

from pynput.keyboard import Key, KeyCode, Listener

from .state import SharedState

log = logging.getLogger(__name__)


def listen_for_hotkeys(state: SharedState, stop_event: Event) -> None:
    """
    Listen for F8 / F9 / F12 and update *state* accordingly.

    Blocks on *stop_event* so the thread consumes no CPU while idle.
    Intended to run as a daemon thread started from ``__main__``.

    Hotkeys
    -------
    F8  — resume (RUNNING)
    F9  — pause  (PAUSED)
    F12 — quit   (EXIT)
    """

    def on_press(key: Union[Key, KeyCode, None]) -> None:
        if key == Key.f8:
            state.set_running()
            log.info("RUNNING")
        elif key == Key.f9:
            state.set_paused()
            log.info("PAUSED")
        elif key == Key.f12:
            state.set_exit()
            stop_event.set()
            log.info("EXIT — stopping listener")

    with Listener(on_press=on_press) as listener:
        stop_event.wait()   # block until EXIT is signalled
        listener.stop()
