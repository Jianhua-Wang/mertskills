# QA checklist

Run this before showing a deck to Boss. The builder catches the mechanical
problems, and the render pass catches what only eyes can see.

## 1. Build is clean

```bash
uv run scripts/build_deck.py deck.yaml
```

- [ ] 0 errors.
- [ ] Every warning is fixed, or you can say why it stays (for example, a table
      cell that has to wrap).

## 2. Render and look at every slide

```bash
uv run scripts/render_deck.py deck.pptx          # PowerPoint on macOS; LibreOffice fallback
```

Open `contact.png` for the overview, then **read each `slide-NN.png` at full
size**. Thumbnails hide collisions.

Per slide:

- [ ] The headline states the finding ("All 48 samples pass QC"), not the topic
      ("QC results"). It is at most 2 lines, and the evidence below supports
      exactly that claim.
- [ ] The slide has as few words as it can. Delete any point the figure already
      shows.
- [ ] Nothing overlaps: figure labels against curves, highlight labels against
      data, and long words in table cells.
- [ ] Figure text is readable. Ticks and labels look the same size as the
      slide's 16–18 pt text, not smaller.
- [ ] The figure fills its slot, with no large white margins (export at slot size).
- [ ] Colours carry their meaning: subject vermillion, baseline grey, and the
      Klein-blue accent only for chrome and highlights. Colour is the same
      across slides.
- [ ] A highlight box sits on the feature the headline names.
- [ ] `source` gives n, error-bar meaning and citations where needed.
- [ ] The accent (`==…==`) appears at most once.
- [ ] Builds: every stage uses identical axes, so nothing jumps between stages.
- [ ] Chinese text renders in DengXian (not a fallback font) and does not break
      in the middle of a term.

Whole deck:

- [ ] Reading only the headlines tells the full story in order.
- [ ] The slide count fits the time (about 1 content slide per minute) and the
      backup slides come after the Backup section.
- [ ] No speaker notes unless Boss asked for them. If so, every content
      slide has them.
- [ ] No `[TODO]`, placeholder prompt text ("Headline: one full sentence…") or
      lorem ipsum is left.
- [ ] Every number on the slides matches the source data or paper. Spot-check
      at least the headline numbers.
- [ ] The summary slide restates the 2–4 messages the talk actually supported.

## 3. Deliver

- [ ] Give Boss the `.pptx` path and the contact sheet.
- [ ] List what you could not verify: missing values marked `[TODO]`, figures
      you could not redraw, and claims that need Boss's judgement.
- [ ] If Boss will present from PDF, the render pass already made `<deck>.pdf`.
