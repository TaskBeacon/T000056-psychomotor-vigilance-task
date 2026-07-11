Use case: infographic-diagram
Asset type: TaskBeacon task flow diagram
Primary request: Create a clean, publication-ready task flow diagram as a timeline collection for the behavioral task described below.

Task: Psychomotor Vigilance Task
Construct: sustained attention / behavioral alertness
Rows/conditions:
- Standard event: the normal wait, target response, and RT feedback sequence.
- Recorded exceptions: premature response, lapse, and no-response branches.

Timeline phases:
- Standard event: Blank black screen (random 2-10 s; SPACE is monitored; no visible content) -> Red counter (65 s max; press SPACE; centered red five-digit `00000` counter on black) -> RT feedback (500 ms; centered red value such as `284 ms` on black) -> Next event
- Recorded exceptions: Blank black screen (SPACE before target = False start) -> Red counter (`RT < 100 ms` = False start; `RT > 500 ms` = Lapse) -> No response (65 s = No response; event ends without feedback)

Visual requirements:
- White background, landscape orientation, crisp dark text, restrained condition accent colors.
- One horizontal row per condition or representative trial type.
- Each row contains 3-7 participant-screen snapshots connected by a subtle arrow.
- Each screen snapshot shows the visible stimulus or feedback, not internal variable names.
- Use gray participant-screen boxes, thin black arrows, consistent row spacing, and subtle row separators.
- Place timing labels under each screen in compact text.
- Place condition labels at the left of each row.
- Use short labels only; avoid paragraphs inside the image.
- Make all text legible at normal document preview size.
- Leave a clean blank header band across the top 15-18% of the image. This band is reserved for a fixed title, `Construct: ...` subtitle, and TaskBeacon logo lockup that will be added after generation.

Accuracy constraints:
- Do not invent phases, stimuli, condition names, keys, rewards, or timings.
- Do not add people, lab equipment, decorative scenes, logos, or unrelated icons.
- Do not draw the task title, construct subtitle, any logo, watermark, brand mark, or `TaskBeacon` text inside the generated image.
- Draw only the timeline content below the blank header band.
- If a detail is unknown, omit it rather than guessing.
- Preserve these exact terms where used: Standard event, Recorded exceptions, Blank, Red counter, RT feedback, False start, Lapse, No response, SPACE, 2-10 s, 65 s max, 500 ms, RT < 100 ms, RT > 500 ms, 00000, 284 ms

Style:
TaskBeacon scientific infographic style: clean vector-like raster image, organized spacing, gray screen boxes, restrained color accents, and a blank header-safe area.

