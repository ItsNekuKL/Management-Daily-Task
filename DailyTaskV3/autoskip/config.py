"""
config.py — All tuning knobs and reference pixel coordinates.

Edit this file to adjust timing behaviour or to re-anchor the pixel
detection points when a game update shifts UI elements.
"""

# ---------------------------------------------------------------------------
# Timing knobs
# ---------------------------------------------------------------------------

KEY_HOLD_S: float = 0.01
"""Seconds the F key is held down per press."""

PRESS_INTERVAL_S: float = 0.05
"""Minimum gap (seconds) between consecutive F presses."""

IDLE_SLEEP_MIN_S: float = 0.001
"""Initial sleep duration (seconds) when no event is detected."""

IDLE_SLEEP_MAX_S: float = 0.016
"""Maximum sleep duration (seconds) during idle — roughly 60 fps polling."""

IDLE_BACKOFF_STEPS: int = 50
"""Consecutive idle frames before the sleep duration doubles."""

# ---------------------------------------------------------------------------
# Reference pixel anchor points  (coordinate space: 1920 × 1080)
#
# Each tuple is (x, y).  They are scaled to the actual screen resolution
# at runtime inside CaptureContext.
# ---------------------------------------------------------------------------

REF_PLAYING: tuple[int, int] = (84, 46)
"""Top-left music 'now playing' icon."""

REF_DIALOGUE_LOWER: tuple[int, int] = (1301, 808)
"""Lower anchor of the dialogue-advance arrow (kept for backward compatibility)."""

REF_DIALOGUE_UPPER: tuple[int, int] = (1301, 790)
"""Upper anchor of the dialogue-advance arrow (kept for backward compatibility)."""

REF_DIALOGUE_X: int = 1301
"""Horizontal anchor of the dialogue choice speech bubbles."""

REF_DIALOGUE_Y_START: int = 450
"""Top vertical boundary for dialogue choices (handles 3+ options and multi-line subtitles)."""

REF_DIALOGUE_Y_END: int = 835
"""Bottom vertical boundary for dialogue choices."""

REF_DIALOGUE_Y_STEP: int = 6
"""Vertical scan step size for dialogue choices."""

REF_LOADING: tuple[int, int] = (1200, 700)
"""Point used to detect the white loading-screen overlay."""

# ---------------------------------------------------------------------------
# Expected pixel colour
# ---------------------------------------------------------------------------

PLAYING_ICON_BGR: tuple[int, int, int] = (216, 229, 236)
"""BGR value of the music icon pixel that signals an active cutscene/voiceover."""

# ---------------------------------------------------------------------------
# Cutscene / storybook bottom-center prompt reference (1920 × 1080 space)
# ---------------------------------------------------------------------------

REF_CUTSCENE_DIAMOND_X: int = 960
"""Horizontal center coordinate for the cutscene/storybook diamond advance prompt."""

REF_CUTSCENE_DIAMOND_Y_START: int = 1025
"""Upper boundary of the diamond prompt vertical search range."""

REF_CUTSCENE_DIAMOND_Y_END: int = 1060
"""Lower boundary of the diamond prompt vertical search range."""

REF_CUTSCENE_DIAMOND_Y_STEP: int = 3
"""Step size for vertical sampling of the cutscene prompt."""

