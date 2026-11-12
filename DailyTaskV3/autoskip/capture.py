"""
capture.py — Screen-region capture and pixel-level event detection.

``CaptureContext`` is initialised once with the actual screen resolution
and pre-computes every coordinate and byte offset it needs.  The hot-path
method ``grab_and_check()`` therefore does zero arithmetic per call —
just one screen grab and a handful of byte comparisons.
"""

from enum import IntEnum

import mss
import mss.base

from .config import (
    PLAYING_ICON_BGR,
    REF_CUTSCENE_DIAMOND_X,
    REF_CUTSCENE_DIAMOND_Y_END,
    REF_CUTSCENE_DIAMOND_Y_START,
    REF_CUTSCENE_DIAMOND_Y_STEP,
    REF_DIALOGUE_LOWER,
    REF_DIALOGUE_UPPER,
    REF_DIALOGUE_X,
    REF_DIALOGUE_Y_END,
    REF_DIALOGUE_Y_START,
    REF_DIALOGUE_Y_STEP,
    REF_LOADING,
    REF_PLAYING,
)


class Action(IntEnum):
    """Action to execute based on screen detection."""
    NONE = 0
    PRESS_F = 1
    PRESS_SPACE = 2


class CaptureContext:
    """
    Encapsulates all screen-coordinate maths for a given resolution.

    Parameters
    ----------
    screen_w, screen_h:
        Actual display resolution in pixels.  All reference coordinates
        from ``config.py`` (defined for 1920 × 1080) are scaled to this.

    Design notes
    ------------
    * The captured rectangle is the *minimal bounding box* of the four
      anchor points, so mss transfers the smallest possible amount of
      data on each grab.
    * Pixel offsets into the flat BGRA byte buffer are pre-computed in
      ``__init__``, so ``grab_and_check`` never multiplies or adds.
    * Short-circuit order: playing icon → loading guard → dialogue pixels.
      The loading-screen guard prevents false positives during transitions.
    """

    def __init__(self, screen_w: int, screen_h: int) -> None:
        # ------------------------------------------------------------------
        # Scale reference (1920×1080) coordinates to the real resolution
        # ------------------------------------------------------------------
        def sx(x: int) -> int:
            return int(x * screen_w / 1920)

        def sy(y: int) -> int:
            return int(y * screen_h / 1080)

        play_x,    play_y    = sx(REF_PLAYING[0]),        sy(REF_PLAYING[1])
        dial_x,    dial_lo_y = sx(REF_DIALOGUE_LOWER[0]), sy(REF_DIALOGUE_LOWER[1])
        _,         dial_hi_y = sx(REF_DIALOGUE_UPPER[0]), sy(REF_DIALOGUE_UPPER[1])
        dial_y_start         = sy(REF_DIALOGUE_Y_START)
        dial_y_end           = sy(REF_DIALOGUE_Y_END)
        load_x,    load_y    = sx(REF_LOADING[0]),        sy(REF_LOADING[1])
        cutscene_x           = sx(REF_CUTSCENE_DIAMOND_X)
        cutscene_y_hi        = sy(REF_CUTSCENE_DIAMOND_Y_END)

        # ------------------------------------------------------------------
        # Minimal bounding box
        # ------------------------------------------------------------------
        left   = min(play_x, dial_x, load_x, cutscene_x - 30)
        top    = min(play_y, dial_y_start, load_y)
        right  = max(play_x, dial_x, load_x, cutscene_x + 30)
        bottom = max(play_y, dial_y_end, load_y, cutscene_y_hi)
        width  = right - left + 1
        height = bottom - top + 1

        self.monitor_region: dict = {
            "top":    top,
            "left":   left,
            "width":  width,
            "height": height,
        }

        # ------------------------------------------------------------------
        # Relative coordinates inside the captured rectangle
        # ------------------------------------------------------------------
        rel_play_x    = play_x  - left
        rel_play_y    = play_y  - top
        rel_dial_x    = dial_x  - left
        rel_dial_lo_y = dial_lo_y - top
        rel_dial_hi_y = dial_hi_y - top
        rel_load_x    = load_x  - left
        rel_load_y    = load_y  - top

        # ------------------------------------------------------------------
        # Pre-computed BGRA byte offsets:  pixel(y,x) → (y*width + x) * 4
        # ------------------------------------------------------------------
        self._off_play    = (rel_play_y    * width + rel_play_x)    * 4
        self._off_dial_lo = (rel_dial_lo_y * width + rel_dial_x)    * 4
        self._off_dial_hi = (rel_dial_hi_y * width + rel_dial_x)    * 4
        self._off_loading = (rel_load_y    * width + rel_load_x)    * 4

        # Precompute offsets for dynamic dialogue choices across full vertical range
        self._off_dial_choices: list[int] = [
            ((sy(y_ref) - top) * width + (dial_x - left)) * 4
            for y_ref in range(REF_DIALOGUE_Y_START, REF_DIALOGUE_Y_END + 1, REF_DIALOGUE_Y_STEP)
        ]

        # Cutscene prompt offsets: (center_offset, left_offset, right_offset)
        # Verifies the surrounding background to prevent open-world terrain/clothing jumps
        self._off_cutscene_diamond: list[tuple[int, int, int]] = []
        for y_ref in range(REF_CUTSCENE_DIAMOND_Y_START, REF_CUTSCENE_DIAMOND_Y_END + 1, REF_CUTSCENE_DIAMOND_Y_STEP):
            cy_rel = sy(y_ref) - top
            cx_rel = cutscene_x - left
            lx_rel = sx(REF_CUTSCENE_DIAMOND_X - 25) - left
            rx_rel = sx(REF_CUTSCENE_DIAMOND_X + 25) - left
            self._off_cutscene_diamond.append((
                (cy_rel * width + cx_rel) * 4,
                (cy_rel * width + lx_rel) * 4,
                (cy_rel * width + rx_rel) * 4,
            ))

        self._play_b, self._play_g, self._play_r = PLAYING_ICON_BGR

    # ------------------------------------------------------------------
    # Hot-path method
    # ------------------------------------------------------------------

    def grab_and_check(self, sct: mss.base.MSSBase) -> Action:
        """
        Capture ``monitor_region`` and return ``True`` if F should be pressed.

        Pixel tests use pre-computed offsets into the raw BGRA byte string —
        no numpy, no per-frame arithmetic, no extra allocations.

        Short-circuit order
        -------------------
        1. Playing icon matched  → press immediately.
        2. Loading-screen white  → skip (avoids false positive).
        3. Either dialogue pixel → press.
        """
        raw: bytes = sct.grab(self.monitor_region).bgra

        # 1. Loading screen guard
        if (raw[self._off_loading]     == 255 and
                raw[self._off_loading + 1] == 255 and
                raw[self._off_loading + 2] == 255):
            return Action.NONE

        # 2. Dialogue choices (scans full vertical range for any option bubble)
        for off in self._off_dial_choices:
            if (raw[off]     >= 245 and
                    raw[off + 1] >= 245 and
                    raw[off + 2] >= 245):
                return Action.PRESS_F

        # Backward compatibility check for dialogue anchor pixels
        if ((raw[self._off_dial_lo]     == 255 and
             raw[self._off_dial_lo + 1] == 255 and
             raw[self._off_dial_lo + 2] == 255)
            or
            (raw[self._off_dial_hi]     == 255 and
             raw[self._off_dial_hi + 1] == 255 and
             raw[self._off_dial_hi + 2] == 255)):
            return Action.PRESS_F

        # 3. Cutscene / storybook / title card prompt diamond at bottom center
        # Verifies both the amber core AND the cutscene letterbox background contrast
        for c_off, l_off, r_off in self._off_cutscene_diamond:
            b = raw[c_off]
            g = raw[c_off + 1]
            r = raw[c_off + 2]
            if r >= 200 and 140 <= g <= 220 and b <= 75 and (r > g > b):
                lb, lg, lr = raw[l_off], raw[l_off + 1], raw[l_off + 2]
                rb, rg, rr = raw[r_off], raw[r_off + 1], raw[r_off + 2]
                # In cutscene letterbox or title banner, background is cool or dark
                if ((lb >= lr or (lr < 95 and lg < 115)) and
                        (rb >= rr or (rr < 95 and rg < 115))):
                    return Action.PRESS_SPACE

        # 4. Playing icon
        if (raw[self._off_play]     == self._play_b and
                raw[self._off_play + 1] == self._play_g and
                raw[self._off_play + 2] == self._play_r):
            return Action.PRESS_F

        return Action.NONE
