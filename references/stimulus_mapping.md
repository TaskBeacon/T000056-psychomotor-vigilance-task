# Stimulus Mapping

## Mapping Table

| Condition | Stage/Phase | Stimulus IDs | Participant-Facing Content | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Asset References | Notes |
|---|---|---|---|---|---|---|---|---|
| `standard` | `instruction` | `instruction_text` | Chinese instructions to wait for the red counter and respond immediately with Space | `W2098748797` | Protocol describes an unpredictable visual simple-RT response. | `psychopy_builtin` | `config/config.yaml` | SimHei text; response mapping is stated once. |
| `standard` | `isi` | `blank_screen` | Blank black screen for a random 2-10 s interval | `W2098748797` | PC-PVT protocol specifies the random pre-stimulus interval and false-start behavior. | `psychopy_builtin` | `config/config.yaml` | Space remains active to detect premature responses. |
| `standard` | `target` | `target_counter` | Centered red five-digit counter beginning at `00000` and advancing in milliseconds | `W2098748797` | PC-PVT uses a five-digit millisecond counter as the visual target. | `psychopy_builtin_dynamic` | `config/config.yaml`; `src/utils.py` | Config owns appearance; a draw hook updates only elapsed digits. |
| `standard` | `feedback` | `rt_feedback` | Recorded reaction time in integer milliseconds | `W2098748797` | A valid RT is displayed for 500 ms before the next interval. | `psychopy_builtin` | `config/config.yaml` | No extra correctness message is shown. |
| `standard` | `completion` | `good_bye` | Counts of valid responses, lapses, false starts, misses, and mean RT | `W143922047` | These measures are standard PVT summary outcomes. | `psychopy_builtin` | `config/config.yaml` | Summary appears only after the vigilance block. |
