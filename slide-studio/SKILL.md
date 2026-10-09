---
name: slide-studio
description: Boss's academic slide system. A fixed minimal-white PowerPoint template (Klein-blue accent, figure-first, 16:9) with 11 layouts, a YAML-to-pptx builder that lints every slide (overflow, finding-style headlines, word count, figure resolution, talk length), slot-sized matplotlib figure helpers, a render-and-inspect QA loop, and the rules for good academic talks. Use whenever making, rebuilding or reviewing slides, PPT, PowerPoint or presentation decks — 做 PPT / 幻灯片 / 汇报 / 组会 / journal club / 学术会议报告 / conference talk / defense — and always build them on this template rather than any other.
---

# Slide Studio — Boss's academic slides

Every deck Boss gets is built on **one template**
(`assets/academic-template.pptx`) by **one builder**
(`scripts/build_deck.py`) from a content-only `deck.yaml`. Layout, fonts,
colours and spacing are never decided per deck, so every talk looks like the
same lab made it, and Boss can still edit the result in PowerPoint because
every element sits in a real layout placeholder.

Paths below are relative to this skill's directory. All scripts run with
`uv run` and declare their own dependencies.

## Operating rules (always)

- **Language.** Slide text, code and files are in **English** unless Boss asks
  for Chinese slides. Chinese mixes in freely and renders in DengXian. Talk to
  Boss in **Chinese** and always address the user as **Boss**.
- **Always this template.** Do not use pptxgenjs, python-pptx from scratch, the
  generic pptx skill's design ideas, or another template for Boss's slides. No
  logos, background images, gradients, icons-in-circles or decorative shapes.
- **Content, not styling.** Choose a layout and fill its fields. Never set a
  font, size, colour or position in the spec or on a slide. If something
  doesn't fit, cut or split the content (see `references/academic-rules.md`).
- **Headlines state the finding.** A content slide's headline is the conclusion
  the slide proves, not its topic. Write "All 48 samples pass QC (median RIN
  8.7)" or "Model A beats B on 5 of 6 datasets", never "QC results" or
  "Distribution of QC metrics". The builder warns on topic-style headlines.
- **As few words as possible.** Write phrases, not sentences: at most 12 words
  per point, 2–4 points, and about 40 words of body text per slide. The figure
  carries the evidence and the speaker the explanation. When in doubt, cut.
- **No speaker notes unless Boss asks.** Leave `notes` out of deck.yaml. When
  Boss asks for notes, set `meta.notes: true` and write them for every content
  slide.
- **Never invent data.** Every number, p-value and citation comes from Boss's
  material. When one is missing, write `[TODO: …]` on the slide and list it in
  your report.
- **Look before you deliver.** Render the deck and read every slide image
  (`references/qa-checklist.md`). A clean build alone is not done.

## Files

| Path | What it is |
|---|---|
| `assets/academic-template.pptx` | The template: theme, master, 11 layouts. Generated, so don't edit it by hand. |
| `scripts/design.py` | The single source of truth: colours, type scale, grid, every layout slot. |
| `scripts/make_template.py` | Writes the template from `design.py`. |
| `scripts/build_deck.py` | deck.yaml → .pptx, with lint report. `--layouts` lists fields and slot sizes. |
| `scripts/render_deck.py` | .pptx → PDF, `slide-NN.png`, `contact.png` (PowerPoint on macOS). |
| `scripts/slide_figures.py` | matplotlib at slide scale: `new_figure(layout)`, `save`, `highlight_box`, palette. |
| `references/academic-rules.md` | What makes a good academic slide. Read it before writing content. |
| `references/talk-recipes.md` | Structures for conference talk, lab meeting (组会), journal club. |
| `references/deck-spec.md` | The full YAML format: every layout, field, markup, build, highlight and table. |
| `references/qa-checklist.md` | The checks to run before showing Boss a deck. |
| `assets/example/` | A complete 15-min conference deck: `deck.yaml`, `make_figures.py`, figures. |

## Workflow

1. **Gather and plan the story.** Find out the talk type, time slot and
   audience, and collect the material (paper, results, figures, data). Pick
   the recipe in `references/talk-recipes.md`. Write the **headline of every
   slide** as a list first: one finding per slide, stated as its conclusion,
   and about one content slide per minute. Show Boss this outline before building when the talk is new or
   longer than 10 slides.
2. **Make the figures at slot size.** In a `make_figures.py` next to the deck:

   ```python
   import sys; sys.path.insert(0, "<skill>/scripts")
   from slide_figures import new_figure, save, highlight_box, SUBJECT, BASELINE
   fig, ax = new_figure("figure")            # 12.13 x 4.75 in, 16-18 pt text
   ax.plot(x, base, color=BASELINE, ls="--"); ax.plot(x, ours, color=SUBJECT)
   print(highlight_box(fig, ax, x=(40, 54), y=(0.82, 0.92)))   # -> deck.yaml highlight
   save(fig, "figures/main.png")
   ```

   - Use one idea per figure and label lines directly.
   - Give the subject vermillion and baselines grey, and give every series a
     line style or marker too.
   - For builds, draw stage 1 and stage 2 on identical axes.
   - Borrowed paper figures: crop single panels from the PDF at 300 dpi and set
     `borrowed: true` plus a `source` citation.
3. **Write `deck.yaml`.** Follow `references/deck-spec.md`, or copy
   `assets/example/deck.yaml` as a start. Add no speaker notes unless Boss
   asked for them.
4. **Build and fix until clean.**
   `uv run <skill>/scripts/build_deck.py deck.yaml` gives 0 errors, and every
   warning is fixed or explained.
5. **Render and inspect.** Run `uv run <skill>/scripts/render_deck.py deck.pptx`,
   then open `deck-render/contact.png` and **every** `slide-NN.png`.
   - Fix collisions, unreadable figure text, wrong highlights and weak
     headlines.
   - Rebuild and re-render until the checklist passes.
6. **Deliver.** Send Boss the contact sheet (SendUserFile) and give the
   `.pptx` path. List the open `[TODO]`s and anything you could not verify.

Keep each talk in its own folder, e.g. `talks/2026-10-lab-meeting/` holding
`deck.yaml`, `make_figures.py`, `figures/`, `deck.pptx`, `deck-render/`.

## The template at a glance

Minimal white, with Klein blue `#002FA7` for chrome and emphasis only. Text is
near-black `#1A1A1A`. Data uses Okabe-Ito with vermillion `#D55E00` for the
subject. The fonts are Arial with DengXian for CJK. The slide is 13.333 × 7.5 in.

The chrome is fixed by the template, so never draw it yourself:

- **Headline rule.** Every content-slide headline sits on a light grey hairline
  with a short blue mark at its left end.
- **Bottom bar.** A thin blue bar runs along the bottom edge of every slide.
- **Slide number.** It sits at the bottom right of content slides. There is no
  footer text.

| Key | Use | Main fields |
|---|---|---|
| `title` | Opening | kicker, title, subtitle, authors, affiliation |
| `paper` | Journal-club opener / cited paper | kicker, title, authors, citation, presenter, image |
| `section` | Part divider (auto-numbered 01, 02, …) | number, title, subtitle |
| `statement` | The question / key claim, alone | kicker, text, source |
| `figure` | One result, full width (default) | headline, image, source |
| `figure_text` | Figure + 2–4 points | headline, image, text, source |
| `two_figures` | Side-by-side comparison | headline, left/right {label, image}, source |
| `text` | Motivation, steps, caveats | headline, text, source |
| `two_columns` | Comparison in words | headline, left/right {heading, text}, source |
| `table` | Exact numbers (booktabs, centred) | headline, table, source |
| `summary` | Closing take-homes + contact | headline, points, acknowledgements, contact |

The type scale is headline 30 pt bold, body 24 pt (20 pt in split layouts),
figure text 16–18 pt, and source 14 pt. Nothing on a slide is smaller than
14 pt.

## Changing the template

The template is a design decision Boss owns. Change it only when Boss asks, and
only in one place:

1. Edit `scripts/design.py`: colours, `TEXT_STYLES`, grid constants, or a new
   `Layout`.
2. `uv run scripts/make_template.py` regenerates `assets/academic-template.pptx`.
3. Rebuild and render `assets/example/deck.yaml` and check that every layout
   still looks right.

Never patch a single deck's slides by hand to work around the template. If a
layout is missing, add it to `design.py`.

## Editing and converting

- **Revise a deck:** edit `deck.yaml` and rebuild. Don't edit the generated
  `.pptx`, because the next build overwrites it.
- **Boss edited the .pptx in PowerPoint:** that file is now the source of truth.
  Make further small changes there with python-pptx (fill placeholders, keep
  the layouts) or ask whether to port those edits back into `deck.yaml`.
- **Someone else's deck → Boss's style:** extract its text and figures
  (python-pptx or markitdown; export pictures from `ppt/media/`), rewrite the
  headlines as claims, and rebuild it as a new `deck.yaml` on this template.
