from __future__ import annotations

from types import MethodType

from psychopy import core


def _draw_elapsed_counter(self, win=None):
    if not self._pvt_started:
        self._pvt_clock.reset()
        self._pvt_started = True
        elapsed_ms = 0
    else:
        elapsed_ms = min(99999, int(round(self._pvt_clock.getTime() * 1000.0)))
    self.text = f"{elapsed_ms:05d}"
    return self._pvt_original_draw(win=win)


def prepare_dynamic_counter(text_stim):
    """Keep a StimBank TextStim while updating its digits on each draw."""
    if not hasattr(text_stim, "_pvt_original_draw"):
        text_stim._pvt_original_draw = text_stim.draw
        text_stim._pvt_clock = core.Clock()
        text_stim.draw = MethodType(_draw_elapsed_counter, text_stim)
        text_stim.autoLog = False
    text_stim._pvt_started = False
    text_stim.text = "00000"
    return text_stim
