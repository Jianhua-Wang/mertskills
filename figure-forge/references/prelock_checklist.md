# Pre-lock checklist

A figure clears every line before it is locked and exported to PDF. Any FAIL sends
it back to the PNG-iteration phase.

## Story & correctness
- [ ] Each panel has one clear job, agreed with Boss, and reads at a glance.
- [ ] The statistic does not misrepresent the data (lattice → bootstrap means +
      paired t-test, not medians/Wilcoxon; unequal lengths → normalized per bp or
      % vs reference; multiple comparisons → Bonferroni, stars from corrected p).
- [ ] Every number that will appear in text/legend is verified against the exact
      panel-input file, and the N is the right subset (watch for panels that use
      different filters and therefore different N).

## Palette & ink
- [ ] One shared style module; no colour redefined inside a figure script.
- [ ] Two semantic families, no shared hue; subject = strongest colour, control =
      neutral grey.
- [ ] Every series has a non-colour secondary cue (line style / marker).
- [ ] Palette passed the dataviz validator in BOTH `--mode light` and `--mode dark`.
- [ ] No text (value, label, legend) wears a series colour — ink tokens only.

## Typography & axes
- [ ] Arial-first stack; 8 pt labels/titles, 7 pt ticks, 0.7 pt spines.
- [ ] Top and right spines removed; no gridlines unless a magnitude read genuinely
      needs one (then behind the data).
- [ ] Panel letters bold, lowercase, column-aligned; each hugs its own panel top.
- [ ] Bold actually renders bold (check the letters — not silently regular).

## Reference lines & labels
- [ ] All guide/zero/threshold lines use the house style: dashed `(0,(3,2))`,
      `lw=0.7`, `INK_MUTED`, high `zorder` (drawn on top).
- [ ] Labels are the shortest unambiguous form; a row of small multiples shares one
      centered axis label.
- [ ] A relative-% axis uses `PercentFormatter` so it is not read as absolute.

## Layout
- [ ] Proportions and inter-panel gaps are deliberate (subgridspec where a pair
      needs isolated spacing).
- [ ] Rendered and eyeballed: no label collisions, no clipping, no overflow.

## Export & housekeeping
- [ ] `save_final` used (png + pdf); `pdf.fonttype = 42` in effect.
- [ ] Draft written to `draft/`; original packaged figures NOT overwritten without
      Boss's explicit go-ahead.

## Docs & tracking (part of "done")
- [ ] Legend rewritten for the final panel structure (letters, content, statistic,
      N, table links).
- [ ] Every `Fig. Nx` reference in the results text re-mapped after panels moved.
- [ ] botnote: worklog added via `add_comment`; task set to `done`.
