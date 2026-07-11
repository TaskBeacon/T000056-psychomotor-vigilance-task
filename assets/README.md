# Assets

The PVT uses only PsychoPy text stimuli defined in `config/*.yaml`. No external media assets are required.

The target is a config-created monospaced `TextStim`; `src/utils.py` installs a draw hook that updates its five digits while PsyFlow retains ownership of display timing and response capture.
