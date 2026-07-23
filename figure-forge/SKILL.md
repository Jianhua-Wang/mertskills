---
name: figure-forge
description: Boss's standards and workflow for building publication-quality (high-tier journal) scientific figures with matplotlib — one unified semantic palette across every panel, journal typography, PNG-while-debugging / PDF-only-after-lock discipline, statistical honesty on lattice-valued and length-confounded data, legibility-first panels that must be understandable at a glance, and keeping figure legends + in-text numbers in exact sync with the panel-input data. Use whenever creating, refining, or finalizing any manuscript figure or its legend/results text.
---

# Figure Forge — Boss's requirements

How Boss wants scientific figures built for high-tier journals. The method is
concrete and checkable, so a figure is right by construction, not by taste.

## Operating rules (always)

- **Language:** all figure text, axis labels, code, and docs in **English**;
  talk to Boss in **Chinese**; address him as **Boss**.
- **One shared style module per manuscript.** Every panel of every figure
  imports its palette, typography, and helpers from that one module, so a colour,
  a font size, and a reference-line style mean the same thing everywhere. Start
  from `references/style_template.py`.
- **Data may live on remote compute** and may not be reproducible locally. Use
  the host and project root from the active project context; ask Boss if either
  is missing. Draw figures from **pre-extracted panel-input CSVs** (e.g.
  `02_plotting_data/panel_inputs/`). If a panel needs new data, regenerate it on
  remote compute first; never fabricate or approximate.

## 0. The non-negotiables

These are the standards Boss judges a figure by. Violating any one makes it wrong.

1. **High-tier-journal professional quality** — clean, deliberate, nothing decorative.
2. **Unified palette** — a colour means the *same thing* in every panel of every
   figure. Never recolour a series between panels; never let two semantic families
   share a hue.
3. **Balanced proportions & controlled gaps** — panel sizes, whitespace, and the
   gaps between subplots are designed, not left to defaults.
4. **The key point is highlighted; controls recede** — the subject of the paper
   carries the strongest colour; control/reference series are neutral grey.
5. **Every panel must be understandable at a glance.** If Boss can't read what a
   panel says, it has failed — **redesign it, don't defend it.** (This is how the
   Fig S1b dumbbell replaced an unreadable point array.)
6. **PNG only while iterating; PDF only after the figure is locked.** Do not emit
   PDFs during the debug phase.
7. **Numbers must match the data the figure is drawn from.** Every value in the
   text and legend is verified against the exact panel-input file — never quoted
   from memory or from a stale earlier package.

## 1. Per-figure workflow

Run these in order. Boss expects the logic discussed *before* pixels are polished.

1. **Discuss the logic / story.** What is each panel's job (magnitude, identity,
   polarity, a distance profile, a single headline)? Agree the panel list and what
   each one claims before building. Sometimes the honest answer changes the chart
   type or the statistic.
2. **Design the panels & layout.** Decide the grid, proportions, and which series
   is the subject vs the control.
3. **Regenerate data if needed** (on the server) — some panels need fresh extracts.
4. **Build** with the shared style module.
5. **Iterate in PNG.** Render, *look at it* (label collisions, geometry, overflow),
   adjust. Show Boss PNGs.
6. **Boss locks** ("定稿 / done").
7. **Export PDF** with `save_final` (writes png + pdf side by side).
8. **Sync the docs** — rewrite the legend for the final panel structure and update
   every in-text number and `Fig. Nx` reference (see §6).
9. **Record in botnote** — worklog via `add_comment`, then mark the task `done`.

## 2. The shared style system

### Palette — two semantic families that never share a hue
- Pick colour **last**, after the form. Assign categorical hues in a **fixed
  order, never cycled**.
- Encode the manuscript's subject with the strongest colour; make **control series
  neutral grey (zero chroma)** so they recede.
- Give every series a **non-colour secondary cue** (line style or marker shape) —
  e.g. hue = one factor, dash = another (a 2×2 encoding) — so identity survives
  colour-blindness, grayscale printing, and forced-colours mode.
- **Validate the palette; do not eyeball CVD.** Run the dataviz validator
  (`scripts/validate_palette.js "<hex,…>" --mode light`, then `--mode dark`).
  Fix any FAIL before continuing.

### Ink — text never wears a series colour
- Values, axis labels, tick labels, and legends stay in ink tokens
  (`INK` / `INK_SECONDARY` / `INK_MUTED`); the coloured mark beside them carries
  identity. A number is never printed in a data colour.

### Typography & axes
- **Arial-first** font stack. On macOS this matters: Helvetica ships as `.ttc`
  collections matplotlib can't pull a bold face from, so `fontweight="bold"`
  silently renders regular; Arial ships a real `Arial Bold.ttf`.
- Journal scale: **8 pt labels/titles, 7 pt ticks**, hairline **0.7 pt** spines.
- **Drop the top and right spines. No gridlines by default** (`clean_axis`).
- **Panel letters:** bold lowercase (`a`, `b`, …), column-aligned to the group's
  true left edge (outer edge of tick labels/titles), each hugging the top of its
  own panel.

### Reference / guide lines — dashed, muted, thin, on top
Every zero-line, threshold, or reference marker uses the **same** convention so it
reads as "guide, not data", and sits *above* the marks it annotates:
```python
ax.axhline(0, color=S.INK_MUTED, lw=0.7, ls=(0, (3, 2)), zorder=5)
```

## 3. Statistical honesty

The statistic must not lie about the data. Recurring traps and the fixes Boss expects:

- **Lattice-valued per-unit metrics** (density = k/L, counts over a fixed length):
  values snap to a coarse per-unit lattice, and the **median locks to a lattice
  point and can invert or wrong-sign the true ordering**. Use **bootstrap means +
  paired t-test**, not boxplot medians / Wilcoxon. If the artifact is important,
  *show* it in a supplementary panel (mean vs median dumbbell) and justify the
  method in the legend.
- **Unequal interval lengths** (windows of 50 vs 51 vs 101 bp): a raw per-unit
  total is confounded by length and can hide or flip the trend. **Normalize
  (per bp, or % vs a reference window) before comparing**; keep the raw view in a
  supplement to show why normalization was needed.
- **Multiple comparisons:** Bonferroni-correct, and draw significance stars from
  the **corrected** p-value.
- **Draw the uncertainty, don't just summarize it.** A bootstrap distribution can
  be rendered as a box (its shape), not only as an interval.
- **Pairing:** when the same unit is measured in several conditions, resample over
  units (rows) to keep the pairing intact.

## 4. Legibility & labels

- **Shortest unambiguous label wins.** "Fold enrichment" not "Fold enrichment vs.
  genome background"; "Distance from TSS (bp)" not "…from corrected TSS (bp)";
  "Density" (with a `PercentFormatter` on the ticks) rather than a verbose unit.
- A **relative-% axis gets `PercentFormatter`** so a reader never mistakes a
  relative-% scale for an absolute quantity.
- A row of small multiples shares **one centered axis label**, not three copies.
- **Design the gaps.** Use a `subgridspec` to control the spacing of one pair of
  panels in isolation when a global `hspace`/`wspace` would disturb the rest.

## 5. Export discipline

- `save_png(fig, path)` during the debug phase; **`save_final(fig, stem)`** once
  locked — it writes both `.png` (preview) and `.pdf` (vector) beside each other.
- `apply_rc` sets **`pdf.fonttype = 42`** so text embeds as editable TrueType
  (what journals ask for), not outlines.
- **Never overwrite the original packaged figures without asking.** Drafts go to a
  `draft/` directory; promoting them over `main/` / `supplementary/` is Boss's call.

## 6. Keep the docs in sync

After a figure is locked, the prose must follow it — this is part of "done":

- **Rewrite the legend** for the final panel structure (panel letters, what each
  shows, the statistic, the N, the table links).
- **Re-map every `Fig. Nx` reference** in the results text when panels move
  (e.g. old B–C → B, D → C, E–G → D–F).
- **Verify every quoted number against the panel-input file**, with a small stats
  script. Watch for the trap where two panels use **different subsets/filters and
  therefore different N** (e.g. density from 16,249 transcripts vs cancer burden
  from 17,079) — quoting the wrong N is a real error caught this way.

## 7. Before locking

Run through `references/prelock_checklist.md`.

## Files

- `references/style_template.py` — reusable matplotlib style module (palette
  rationale, ink tokens, `apply_rc`, `clean_axis`, `place_panel_labels`, the
  bootstrap/paired-test helpers, `save_png`, `save_final`). Copy per manuscript and
  swap only the palette block.
- `references/prelock_checklist.md` — the pass/fail list a figure must clear.
