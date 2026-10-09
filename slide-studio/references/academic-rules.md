# Rules for academic slides

These are the standards a deck is judged by. Most are enforced by the template
or the builder. The rest are checked by eye in the QA pass
(`qa-checklist.md`).

## 1. One slide, one message

- Each content slide makes **one claim**. If you need "and" to state it, you
  have two slides.
- The **headline is the finding**: the conclusion the slide proves, written as
  a full sentence with a verb, at most 2 lines. It never just names the topic,
  the method or the content.

  | Topic (don't) | Finding (do) |
  |---|---|
  | QC results / Distribution of QC metrics | All 48 samples pass QC (median RIN 8.7) |
  | Accuracy vs compute | Curriculum sampling reaches baseline accuracy with 2× less compute |
  | Comparison of model A and model B | Model A beats B on 5 of 6 datasets |
  | Method overview | A two-stage filter removes 90 % of false positives |
  | 质控结果 | 所有样本均通过质控 |

  When the result is negative or mixed, say so: "QC fails on 3 of 48 samples,
  all from batch 2".
  - Exceptions where a label headline is fine: `summary` ("Take-home
    messages"), section dividers, and backup slides titled for lookup.
- The body is the **evidence** for the headline: a figure, a table, or a few
  points. Most slides should be figures. A talk made of `text` slides is a
  paper read aloud.
- Someone who reads only the headlines in order should get the whole argument.
  Check this before building (step 2 of the workflow).

## 2. Words

- **As few words as possible.** Keep each point to 12 words or fewer (two
  Chinese characters count as one word), 2–4 points per slide (5 maximum), about
  40 words of body text per slide, and two bullet levels at most.
- Write phrases, not paragraphs. Leave out articles and filler; the speaker
  supplies the full sentences.
- Before adding a point, ask whether the figure already shows it. If it does,
  drop the point.
- Never shrink the font to fit more text. **Cut words**, split the slide, or move
  detail to backup.
- Use one accent (`==…==`) per slide at most. If everything is emphasised,
  nothing is.
- Define every abbreviation the first time it is spoken, and on the slide when
  the audience is mixed.
- Write equations only when the audience needs them to follow the next slide.
  Show at most one per slide, defining each symbol on the slide, as an image
  rendered at slide-scale font size.

## 3. Type

The template fixes all type sizes, and these minimums hold for every slide:

| Element | Size |
|---|---|
| Headline | 30 pt bold |
| Body text | 24 pt (20 pt in two-column and figure + text layouts) |
| Figure text (ticks, labels, legends) | 16 pt minimum, 18 pt axis labels |
| Source line, slide number | 14 pt. Nothing on a slide is smaller. |

Use Arial for Latin text and DengXian for Chinese, both set in the theme. Never
set a font by hand.

## 4. Figures

- **Redraw figures for the slide; don't paste journal panels.** A panel built
  for print (7–8 pt text, six subpanels) is unreadable at the back of a room.
  Use `slide_figures.new_figure(layout)`, which sizes the figure to its slot
  with 16–18 pt text, and keep one idea per figure. Split multi-panel figures
  across slides or builds.
- **Colour has meaning.** The subject of the talk is vermillion (`SUBJECT`) and
  baselines are neutral grey (`BASELINE`). Every series also carries a
  non-colour cue: a line style, marker, or hatch. A colour keeps its meaning
  across all slides. These are the figure-forge rules applied at slide scale.
- **The accent is the slide's colour, not the data's.** Klein blue marks chrome,
  emphasis and highlight boxes, so a blue box always means "look here".
- **Label directly.** Put series names next to the lines rather than in a legend
  when there is room. Name axes in words with units, such as "Compute
  (GPU-hours)".
- **Show uncertainty** (error bars, bands, or n), and say what it is in the
  `source` line, for example "mean ± s.d., 5 seeds".
- **Builds.** When a figure has several elements, reveal them in the order you
  will talk about them: axes and baseline first, then the result. Draw every
  stage on identical axes.
- **Borrowed figures** (from papers, which is common in journal club) are fine
  if they are cited in `source` and `borrowed: true` is set. Crop to the one
  panel you discuss. Render from PDF at 300 dpi or more, never from a
  screenshot.

## 5. Tables

- A table belongs on a slide only when exact numbers matter. Otherwise plot it.
- Use at most 8 rows and 5–6 columns. Keep the rows that carry the message and
  move the full table to backup.
- Use the booktabs style: three rules, no vertical lines, numbers right-aligned,
  and the same decimals within a column. Highlight the one row that is the
  point.

## 6. Citations and integrity

- Every figure, number or claim from someone else's work gets a short citation
  in `source`, for example "Author et al., *Journal* 2025".
- Never invent numbers, p-values or citations. If a value is not in the
  material you were given, leave a visible `[TODO: value]` and tell Boss.
- Label synthetic, illustrative or preliminary data as such in `source`.
- Report results honestly: say what was compared, how many runs, and what
  failed. A `text` slide of limitations or caveats builds trust.

## 7. Structure and timing

- Plan **one content slide per minute** and leave time for questions. A
  15-minute slot means about 12 content slides plus title and summary.
- Use section dividers when the talk has 3 or more parts. Short talks may skip
  them.
- Close on `summary` (2–4 numbered take-home messages plus contact), not on
  "Thank you" or "Questions?". The summary stays up during questions.
- Put backup slides after a "Backup" section (`number: B`, `backup: true`):
  extra results, full tables, method details, and answers to likely questions.
- Don't write speaker notes unless Boss asks for them. When Boss does, set
  `meta.notes: true` and give every content slide notes: what to say first,
  where to point, and the transition to the next slide.

## 8. Accessibility

- Use only the template's colours. Text contrast is at least 4.5:1, and the
  palette is colour-blind safe (Okabe-Ito).
- Never encode meaning by colour alone. Pair it with a line style, a marker, or
  a word.
- Don't use animations or transitions, except that progressive reveal and
  builds are separate slides, so they survive PDF export.

## 9. The template is fixed

- Every slide uses one of the 11 layouts. Don't move placeholders, recolour
  text, add logos, backgrounds, gradients, shadows, clip art or decorative
  shapes.
- If content does not fit any layout, change the content: split it, plot it, or
  move it to backup. If a layout is genuinely missing, add it to
  `scripts/design.py` and regenerate the template. Don't hand-place one-off
  boxes on a slide.
