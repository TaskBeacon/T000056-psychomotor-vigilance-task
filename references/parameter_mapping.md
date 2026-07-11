# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| `condition` | `task.conditions` | `[standard]` | `W2008161183` | Original PVT is a repeated simple visual RT protocol without trial classes. | `direct` | One label delegates scheduling to BlockUnit. |
| `blocks` | `task.total_blocks` | `1` | `W2098748797` | PC-PVT runs each assessment as one continuous session. | `direct` | No participant-visible break. |
| `events` | `task.trial_per_block` | `90` | `W2098748797` | The implementation reports 50-100 events in 5- or 10-minute sessions. | `inferred` | Ninety events approximate a 10-minute session under the cited timing. |
| `response_key` | `task.key_list` | `[space]` | `W2098748797` | PC-PVT preserves the simple button-response contract while changing response hardware. | `inferred` | Keyboard-compatible equivalent of a dedicated response button. |
| `isi_range` | `timing.isi_duration` | `[2.0, 10.0] s` | `W2098748797` | Protocol section specifies a randomly delayed stimulus, usually between 2 and 10 s. | `direct` | A response in this interval is a false start. |
| `target_timeout` | `timing.response_window_duration` | `65.0 s` | `W2098748797` | Protocol section classifies failure to respond within 65 s as no-response. | `direct` | Timeout trigger is emitted by StimUnit. |
| `feedback_duration` | `timing.feedback_duration` | `0.5 s` | `W2098748797` | PC-PVT displays RT for 500 ms after a valid response. | `direct` | Feedback is omitted for false starts and no-response events. |
| `false_start_threshold` | `timing.false_start_threshold` | `0.1 s` | `W143922047` | Standardized PVT analyses count anticipatory responses below 100 ms as false starts. | `direct` | Pre-target responses are also false starts. |
| `lapse_threshold` | `timing.lapse_threshold` | `0.5 s` | `W143922047` | The standard lapse metric uses RT greater than 500 ms. | `direct` | Exactly 500 ms is not classified as a lapse. |
| `target_counter` | `stimuli.target_counter` | `red five-digit millisecond counter` | `W2098748797` | PC-PVT uses a five-digit millisecond counter as the visual stimulus. | `direct` | Updated each frame by a task-local draw wrapper. |
| `background` | `window.bg_color` | `black` | `W2098748797` | PC-PVT reproduces a high-contrast LED-style counter display. | `inferred` | Preserves contrast and suppresses irrelevant visual structure. |
| `trigger_codes` | `triggers.map` | `1-40` | `W2098748797` | Literature defines event semantics but not TaskBeacon trigger integers. | `inferred` | Codes uniquely identify experiment, interval, target, response, timeout, and feedback events. |

