# CHANGELOG

## [v0.1.0] - 2026-07-11

### Added

- Added a literature-aligned visual Psychomotor Vigilance Task.
- Added random 2-10 s response-stimulus intervals with premature-response detection.
- Added a five-digit dynamic millisecond counter, 65 s no-response rule, and 500 ms RT feedback.
- Added false-start, lapse, no-response, valid-response, and RT outcome fields.
- Added Chinese participant instructions, trigger mappings, QA, scripted simulation, and sampled simulation profiles.
- Added curated reference, parameter, stimulus, and paradigm-logic audit artifacts.

### Changed

- Replaced the generated generic trial scaffold with the PVT-specific state machine.
- Kept condition generation, response capture, triggers, timing windows, and phase data on PsyFlow public APIs.

### Fixed

- Removed template conditions, prompts, feedback, and controller logic that did not belong to PVT.

