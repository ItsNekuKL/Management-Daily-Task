"""
__main__.py — Entry point for ``python -m autoskip``.

This is the *only* module that has side effects (console I/O, .env reads,
screen grabs, threads).  Every other module in the package is pure logic
that can be imported freely without triggering anything.
"""

import logging
import os
import random
import sys
from threading import Event, Thread
from time import sleep

import mss
from dotenv import find_dotenv, load_dotenv, set_key

from .capture import Action, CaptureContext
from .config import (
    IDLE_BACKOFF_STEPS,
    IDLE_SLEEP_MAX_S,
    IDLE_SLEEP_MIN_S,
    PRESS_INTERVAL_S,
)
from .hotkeys import listen_for_hotkeys
from .state import SharedState
from .win32_input import get_screen_size, press_f, press_space

# ---------------------------------------------------------------------------
# Logging — simple timestamped format, INFO level by default
# ---------------------------------------------------------------------------

logging.basicConfig(
    format="%(asctime)s  %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Resolution setup
# ---------------------------------------------------------------------------

def _setup_resolution() -> tuple[int, int]:
    """
    Return ``(screen_width, screen_height)`` for the primary monitor.

    Resolution is persisted to ``.env`` after the first interactive
    confirmation so subsequent launches skip the prompt entirely.
    """
    load_dotenv()
    cached_w = os.getenv("WIDTH",  "")
    cached_h = os.getenv("HEIGHT", "")

    if cached_w and cached_h:
        return int(cached_w), int(cached_h)

    sw, sh = get_screen_size()
    print(f"Detected resolution: {sw}x{sh}")

    if input("Is the resolution correct? (y/n): ").strip().lower() == "n":
        sw = int(input("Enter resolution width:  ").strip())
        sh = int(input("Enter resolution height: ").strip())
        print(f"New resolution set to {sw}x{sh}\n")

    dotenv_file = find_dotenv()
    set_key(dotenv_file, "WIDTH",  str(sw), quote_mode="never")
    set_key(dotenv_file, "HEIGHT", str(sh), quote_mode="never")
    return sw, sh


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def main() -> None:
    os.system("cls")
    print("Welcome to Genshin Impact Dialogue Skipper\n")

    screen_w, screen_h = _setup_resolution()
    capture = CaptureContext(screen_w, screen_h)

    state      = SharedState()
    stop_event = Event()

    print(
        "-------------\n"
        "F8  to start\n"
        "F9  to pause\n"
        "F12 to quit\n"
        "-------------"
    )

    hotkey_thread = Thread(
        target=listen_for_hotkeys,
        args=(state, stop_event),
        daemon=True,
        name="HotkeyListener",
    )
    hotkey_thread.start()

    # Adaptive idle sleep: starts at IDLE_SLEEP_MIN_S for fast response,
    # doubles every IDLE_BACKOFF_STEPS idle frames up to IDLE_SLEEP_MAX_S,
    # and resets to minimum the moment a press event is detected.
    idle_count = 0
    idle_sleep = IDLE_SLEEP_MIN_S

    with mss.mss() as sct:
        while True:
            if state.is_exit:
                log.info("Closing…")
                break

            if not state.is_running:
                # Zero-CPU wait — unblocked instantly by F8 or F12.
                idle_count = 0
                idle_sleep = IDLE_SLEEP_MIN_S
                state.wait_until_running()
                continue

            # --- RUNNING ---
            action = capture.grab_and_check(sct)
            if action == Action.PRESS_SPACE:
                idle_count = 0
                idle_sleep = IDLE_SLEEP_MIN_S
                press_space()
                sleep(random.uniform(PRESS_INTERVAL_S, PRESS_INTERVAL_S + 0.035))
            elif action == Action.PRESS_F:
                idle_count = 0
                idle_sleep = IDLE_SLEEP_MIN_S
                press_f()
                sleep(random.uniform(PRESS_INTERVAL_S, PRESS_INTERVAL_S + 0.025))
            else:
                idle_count += 1
                if idle_count >= IDLE_BACKOFF_STEPS:
                    idle_sleep = min(idle_sleep * 2, IDLE_SLEEP_MAX_S)
                    idle_count = 0
                sleep(idle_sleep)

    hotkey_thread.join(timeout=1.0)
    sys.exit(0)


if __name__ == "__main__":
    main()
