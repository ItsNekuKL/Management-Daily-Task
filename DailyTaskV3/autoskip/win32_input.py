"""
win32_input.py — Low-level Win32 key injection and screen metrics.

All ctypes / Windows API calls are isolated here so the rest of the
package never touches platform-specific internals directly.
"""

import ctypes
from ctypes import wintypes
import random
from time import sleep

from .config import KEY_HOLD_S

# ---------------------------------------------------------------------------
# Win32 handle
# ---------------------------------------------------------------------------

user32 = ctypes.windll.user32

# ---------------------------------------------------------------------------
# SendInput constants
# ---------------------------------------------------------------------------

_INPUT_KEYBOARD  = 1
_KEYEVENTF_KEYUP   = 0x0002
_KEYEVENTF_SCANCODE = 0x0008
_SCAN_F: int = 0x21   # hardware scan code for the F key
_VK_F:   int = 0x46   # virtual-key code for F
_SCAN_SPACE: int = 0x39  # hardware scan code for the Space key
_VK_SPACE:   int = 0x20  # virtual-key code for Space

_ULONG_PTR = (
    ctypes.c_ulonglong if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_ulong
)

# ---------------------------------------------------------------------------
# ctypes structures required by SendInput
# ---------------------------------------------------------------------------


class _KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk",         wintypes.WORD),
        ("wScan",       wintypes.WORD),
        ("dwFlags",     wintypes.DWORD),
        ("time",        wintypes.DWORD),
        ("dwExtraInfo", _ULONG_PTR),
    ]


class _MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx",          wintypes.LONG),
        ("dy",          wintypes.LONG),
        ("mouseData",   wintypes.DWORD),
        ("dwFlags",     wintypes.DWORD),
        ("time",        wintypes.DWORD),
        ("dwExtraInfo", _ULONG_PTR),
    ]


class _HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg",    wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    ]


class _INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", _MOUSEINPUT),
        ("ki", _KEYBDINPUT),
        ("hi", _HARDWAREINPUT),
    ]


class _INPUT(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD), ("ii", _INPUT_UNION)]


# ---------------------------------------------------------------------------
# Pre-built INPUT structs — allocated once, reused on every key press
# ---------------------------------------------------------------------------

def _build_f_inputs() -> tuple[_INPUT, _INPUT]:
    down = _INPUT()
    down.type = _INPUT_KEYBOARD
    down.ii.ki = _KEYBDINPUT(_VK_F, _SCAN_F, _KEYEVENTF_SCANCODE, 0, 0)

    up = _INPUT()
    up.type = _INPUT_KEYBOARD
    up.ii.ki = _KEYBDINPUT(_VK_F, _SCAN_F, _KEYEVENTF_SCANCODE | _KEYEVENTF_KEYUP, 0, 0)

    return down, up


def _build_space_inputs() -> tuple[_INPUT, _INPUT]:
    down = _INPUT()
    down.type = _INPUT_KEYBOARD
    down.ii.ki = _KEYBDINPUT(_VK_SPACE, _SCAN_SPACE, _KEYEVENTF_SCANCODE, 0, 0)

    up = _INPUT()
    up.type = _INPUT_KEYBOARD
    up.ii.ki = _KEYBDINPUT(_VK_SPACE, _SCAN_SPACE, _KEYEVENTF_SCANCODE | _KEYEVENTF_KEYUP, 0, 0)

    return down, up


_F_DOWN, _F_UP = _build_f_inputs()
_SPACE_DOWN, _SPACE_UP = _build_space_inputs()
_INPUT_SIZE = ctypes.sizeof(_INPUT)   # cached — avoids a repeated C call


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def press_f() -> None:
    """Send a single F key tap (down + hold + up) via SendInput with humanized timing."""
    user32.SendInput(1, ctypes.byref(_F_DOWN), _INPUT_SIZE)
    # Realistic human hold jitter (15ms to 28ms) avoids bot pattern detection
    sleep(random.uniform(KEY_HOLD_S, KEY_HOLD_S + 0.018))
    user32.SendInput(1, ctypes.byref(_F_UP), _INPUT_SIZE)


def press_space() -> None:
    """Send a single Space key tap (down + hold + up) via SendInput with humanized timing."""
    user32.SendInput(1, ctypes.byref(_SPACE_DOWN), _INPUT_SIZE)
    sleep(random.uniform(KEY_HOLD_S + 0.005, KEY_HOLD_S + 0.022))
    user32.SendInput(1, ctypes.byref(_SPACE_UP), _INPUT_SIZE)


def get_screen_size() -> tuple[int, int]:
    """Return ``(width, height)`` of the primary monitor via GetSystemMetrics."""
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
