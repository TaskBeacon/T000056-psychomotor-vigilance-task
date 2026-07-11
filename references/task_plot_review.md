# Task Plot Review

## Evidence Match

- PASS: Task title and construct match `taskbeacon.yaml`, README, and the logic audit.
- PASS: Standard event order is blank 2-10 s interval, red millisecond counter, 500 ms RT feedback, then next event.
- PASS: Exception row correctly shows premature response, `<100 ms` false start, `>500 ms` lapse, and 65 s no-response behavior.
- PASS: Participant-visible screens use a blank black display, centered red counter, and centered red RT value; no fixation, reward, or accuracy content was invented.

## Visual Quality

- PASS: All text is readable at normal preview size.
- PASS: Screen boxes, arrows, row labels, and timing labels are aligned and non-overlapping.
- PASS: The fixed title and `Construct:` subtitle are centered in the reserved header band.
- PASS: The borderless TaskBeacon logo lockup is legible at top right and does not overlap the title.
- PASS: The raw generated image contains no title, logo, watermark, people, devices, or decorative scene.
- PASS: Final output is 24-bit RGB PNG, avoiding inconsistent alpha decoding in browser/image preview paths.

## README Embed

- PASS: `README.md` embeds `![Task Flow](task_flow.png)` immediately under `## 2. Task Flow`.
- PASS: Raw and final assets are saved at the required paths.

## Decision

Accepted after one generation. No regeneration required.

