# Talk recipes

Starting structures for the three talks Boss gives. Adjust the number of slides
to the time slot, about one content slide per minute. Each line is
`layout: what goes on it`.

## Conference talk (12–20 min)

The audience is smart but outside your sub-field, and they decide in the first
two minutes whether to listen. Lead with the question and the answer, then earn
the answer.

```
title        claim-style title; venue/session in kicker
statement    the question (or the gap), one sentence
figure       why it matters: the problem, shown, not told
section      01 · <the problem / setting>          (skip if < 15 min)
figure_text  the key observation that motivates the method
section      02 · <the method>
two_columns  ours vs the standard approach, in 3 points each
figure       method schematic (one diagram, built in stages if complex)
section      03 · <results>
figure       main result (build: baseline first, then ours) + highlight
two_figures  where it holds / where it breaks (conditions, ablation)
table        the numbers reviewers will ask about (≤ 8 rows)
text         limitations / caveats (reveal)
summary      2–4 take-home messages + contact
section      B · Backup slides
...          backup: ablations, full tables, method details, likely questions
```

- A 12-minute talk has about 10 content slides. Drop the section dividers and
  merge setup into one slide.
- A 20-minute talk can add a second main result and a related-work slide
  (`two_columns`: prior approach vs ours).
- The title, the statement and the first headline of results should each say
  the main claim. Repetition is the point.

## Lab meeting / 组会 progress report (10–20 min)

The audience knows the project. They want to know what changed, what it means,
and where you are stuck. Feedback is the goal, so show problems openly.

```
title        "<project>: <one-line status>"; kicker = "Lab meeting · date"
text         last time → this week: goals set last meeting, and whether each was met
figure       result 1 (headline = what it shows, not "Experiment 1")
figure       result 2 / figure_text with interpretation
two_figures  comparison or sanity check
statement    the open problem / decision needed ("Should we ... or ...?")
text         plan for next week (3 concrete items, owner/date if relevant)
summary      take-home + the specific feedback you want
section      B · Backup
...          raw numbers, setups, extra plots
```

- Lab meeting slides may be more detailed than a conference talk: more points,
  smaller tables. But every headline must still be a claim.
- A QC or sanity-check slide still states its result: "All 48 samples pass QC
  (median RIN 8.7)" or "Batch 2 fails QC on 3 samples", never "QC results".
- Mark preliminary or uncertain results in the headline or source: "Preliminary:
  …", "n = 2 seeds".
- Chinese headlines and points are fine for an internal audience. Keep figure
  text in English so figures can be reused.

## Journal club (20–45 min)

The goal is to make the room understand **and judge** someone else's paper. The
paper's figures are the evidence, and your job is to explain and critique them.

```
paper        title, authors, journal · year · doi, "Presented by", teaser figure
statement    the question the paper asks, in one sentence
text         background: what was known / the gap (3 points)
figure_text  key concept or method overview (paper Fig. 1, borrowed: true)
section      01 · Main results
figure       Fig. 2a — headline = what the panel shows, in your words
figure       Fig. 2b … one panel or claim per slide, with builds if needed
two_figures  control vs experiment, side by side
section      02 · Critique
two_columns  strengths vs weaknesses / concerns
text         open questions for discussion (reveal, one at a time)
summary      the paper's claim, whether you believe it, and why
```

- **One figure panel per slide.** Crop single panels from the paper and render
  them at 300 dpi or more from the PDF. Mark them `borrowed: true` and cite them in
  `source` ("Author et al., *Journal* 2025, Fig. 2b").
- The headline gives your reading of the panel ("Knockout cells lose polarity
  within 2 h"), not the paper's figure title.
- Separate what the authors claim from what the data shows. The critique
  section is the reason for journal club, so don't skip it.
- To extract a panel, render the PDF page with pymupdf and crop it with a clip
  rectangle:

  ```python
  import pymupdf
  doc = pymupdf.open("paper.pdf")
  page = doc[3]                                  # 0-based page index
  clip = pymupdf.Rect(50, 80, 300, 260)          # points, from page.rect / a quick render
  page.get_pixmap(dpi=300, clip=clip).save("figures/fig2b.png")
  ```

## Choosing a layout for a slide

| You want to show | Layout |
|---|---|
| A result (plot, image, diagram) | `figure` |
| A result that needs 2–4 points of interpretation | `figure_text` |
| Two conditions, before/after, method vs baseline | `two_figures` |
| A comparison in words | `two_columns` |
| Exact numbers that matter | `table` |
| Motivation, steps, caveats, next steps | `text` (use `reveal: true` when discussing items one by one) |
| The question, the key claim, a decision needed | `statement` |
| A transition between parts | `section` |
| A paper being discussed | `paper` |
| The end | `summary` |

If you reach for `text` three times in a row, find a figure instead.
