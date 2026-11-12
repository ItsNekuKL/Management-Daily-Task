"""
state.py — Shared application state for the skipper main loop.

Keeping the Status enum and SharedState in their own module means
neither the hotkey listener nor the main loop need to import each other.
"""

from enum import Enum, auto
from threading import Event


class Status(Enum):
    RUNNING = auto()
    PAUSED  = auto()
    EXIT    = auto()


class SharedState:
    """
    Thread-safe state cell backed by ``threading.Event`` objects.

    Using Events instead of a polled value means the main loop blocks
    with zero CPU while paused and wakes *immediately* when F8 or F12
    is pressed — no spin, no fixed polling interval.
    """

    def __init__(self) -> None:
        self._running: Event = Event()   # set → RUNNING; clear → PAUSED
        self._exit:    Event = Event()

    # ------------------------------------------------------------------
    # Mutators (called from the hotkey thread)
    # ------------------------------------------------------------------

    def set_running(self) -> None:
        self._exit.clear()
        self._running.set()

    def set_paused(self) -> None:
        self._running.clear()

    def set_exit(self) -> None:
        self._exit.set()
        self._running.set()   # unblock any wait() on _running

    # ------------------------------------------------------------------
    # Blocking helper (called from the main thread)
    # ------------------------------------------------------------------

    def wait_until_running(self) -> None:
        """Block the caller until RUNNING or EXIT is signalled."""
        self._running.wait()

    # ------------------------------------------------------------------
    # Read-only properties
    # ------------------------------------------------------------------

    @property
    def is_exit(self) -> bool:
        return self._exit.is_set()

    @property
    def is_running(self) -> bool:
        return self._running.is_set() and not self._exit.is_set()
