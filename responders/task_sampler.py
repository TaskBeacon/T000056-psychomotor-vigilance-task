from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


@dataclass
class TaskSamplerResponder:
    """Phase-aware PVT responder covering valid, lapse, false-start, and miss paths."""

    key: str = "space"
    false_start_rate: float = 0.05
    no_response_rate: float = 0.03
    lapse_rate: float = 0.12
    rt_mean_s: float = 0.28
    rt_sd_s: float = 0.04
    lapse_rt_mean_s: float = 0.65
    lapse_rt_sd_s: float = 0.08

    def __post_init__(self) -> None:
        self._rng: Any = None
        for name in ("false_start_rate", "no_response_rate", "lapse_rate"):
            setattr(self, name, max(0.0, min(1.0, float(getattr(self, name)))))

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def on_feedback(self, fb: Feedback) -> None:
        return None

    def end_session(self) -> None:
        self._rng = None

    def _random(self) -> float:
        return float(self._rng.random())

    def _normal(self, mean: float, sd: float) -> float:
        if hasattr(self._rng, "normal"):
            return float(self._rng.normal(mean, sd))
        return float(self._rng.gauss(mean, sd))

    def act(self, obs: Observation) -> Action:
        if self._rng is None or not obs.valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "pvt_sampler", "outcome": "wait"})

        if obs.phase in {"instruction", "goodbye"}:
            return Action(
                key=self.key,
                rt_s=0.1,
                meta={"source": "pvt_sampler", "outcome": "continue"},
            )

        if obs.phase == "isi":
            if self._random() < self.false_start_rate:
                deadline = float(obs.deadline_s or 1.0)
                return Action(
                    key=self.key,
                    rt_s=min(max(0.05, deadline * 0.5), max(0.05, deadline - 0.01)),
                    meta={"source": "pvt_sampler", "outcome": "false_start"},
                )
            return Action(key=None, rt_s=None, meta={"source": "pvt_sampler", "outcome": "wait"})

        if obs.phase != "target" or self._random() < self.no_response_rate:
            return Action(key=None, rt_s=None, meta={"source": "pvt_sampler", "outcome": "no_response"})

        if self._random() < self.lapse_rate:
            rt_s = max(0.501, self._normal(self.lapse_rt_mean_s, self.lapse_rt_sd_s))
            outcome = "lapse"
        else:
            rt_s = max(0.1, self._normal(self.rt_mean_s, self.rt_sd_s))
            outcome = "valid_response"
        return Action(key=self.key, rt_s=rt_s, meta={"source": "pvt_sampler", "outcome": outcome})
