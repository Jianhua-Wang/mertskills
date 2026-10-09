# deck.yaml specification

`scripts/build_deck.py` turns one YAML file into a `.pptx` on the academic
template. The YAML holds **content only**. Position, size, font, colour and
spacing come from the template (`scripts/design.py`), so they never appear in
the spec.

```bash
uv run scripts/build_deck.py deck.yaml               # writes deck.pptx next to it
uv run scripts/build_deck.py deck.yaml -o out/talk.pptx
uv run scripts/build_deck.py --layouts               # every layout, field and slot size
```

Exit code 0 means the build is clean or has warnings only. 1 means there are
errors (overflow, missing headline or file, and so on). 2 means the spec itself
is malformed, for example an unknown layout or field. Relative paths, such as
`image:`, resolve against the folder that holds deck.yaml.

## Top level

```yaml
meta:
  title: Curriculum sampling halves the compute    # file metadata
  author: Presenter Name                           # file metadata
  duration_min: 15                                 # enables the slide-count check
  # notes: true                                    # only when Boss asks for speaker notes

slides:
  - layout: title
    ...
```

## Fields every slide may carry

| Key | Meaning |
|---|---|
| `layout` | Required. One of the 11 layout keys below. |
| `notes` | Speaker notes, plain text. Leave them out unless Boss asks for notes; then set `meta.notes: true` and the builder warns when a content slide has none. |
| `slide_number` | `false` hides the slide number on this slide. There is no footer text. |
| `backup` | `true` keeps the slide out of the slide-count check. Use it for slides after the "Backup" section. |
| `reveal` | `true` turns a `text` or `points` list into one slide per top-level item (progressive reveal). |
| `highlight` | Boxes drawn over the image. See [Highlights](#highlights). |
| `borrowed` | `true` marks a figure taken from a paper. It skips the "export at slot size" warning, and the slide must have a `source`. |
| `id` | A free label for your own reference. It is ignored by the builder. |

## Layouts

Slot sizes are in inches on a 13.333 × 7.5 in (16:9) slide. Export figures at
exactly these sizes (see `slide_figures.py`) so they are placed 1:1.

### Hero layouts

These have no headline. Their slots are stacked and centred vertically, so a
one-line title sits as tight to its subtitle as a two-line one does.

**`title`**: the opening slide.

| Field | Style | Notes |
|---|---|---|
| `kicker` | 14 pt bold blue caps | Event, session, date |
| `title` | 40 pt bold | Up to 3 lines. State the claim if you can. |
| `subtitle` | 22 pt | Optional |
| `authors` | 18 pt | Bold the presenter: `"**Your Name**, Co-author"` |
| `affiliation` | 14 pt | Optional |

**`paper`**: the opening slide of a journal club, or a slide introducing a cited
paper.

| Field | Style | Notes |
|---|---|---|
| `kicker` | 14 pt bold blue caps | "Journal club · date" |
| `title` | 30 pt bold | The paper's title, up to 3 lines |
| `authors` | 16 pt | "First, Second, …, Last" |
| `citation` | 16 pt blue | "Journal · year · doi:…" |
| `presenter` | 14 pt muted | "Presented by …" |
| `image` | 4.23 × 5.70 in | Graphical abstract or key figure (optional, portrait) |

**`section`**: a divider between parts of the talk.

| Field | Style | Notes |
|---|---|---|
| `number` | 48 pt bold blue | Optional. Defaults to "01", "02", … counted over section slides. Give `B` for backup. |
| `title` | 40 pt bold | Up to 2 lines |
| `subtitle` | 20 pt | Optional. One line on what this part shows. |

**`statement`**: one sentence on its own, such as the research question, the key
result, or a provocation.

| Field | Style | Notes |
|---|---|---|
| `kicker` | 14 pt bold blue caps | "The question", "Key result" |
| `text` | 32 pt bold | One sentence. Mark the key phrase with `==…==`. `statement:` is an alias. |
| `source` | 14 pt | Optional citation |

### Content layouts

Every content layout has a `headline`: a full sentence that states the finding,
in at most 2 lines at 30 pt (about 14 words). Write the conclusion, not the
topic: "All 48 samples pass QC", not "QC results". It sits on the template's
headline rule. `title:` is accepted as an alias. All of them except `summary`
also take `source`: a 14 pt line at the bottom for the citation, n, statistical
test, or error-bar definition. It holds two lines at most.

**`figure`**: one full-width figure. This is the default slide for a result.

| Field | Size |
|---|---|
| `image` | 12.13 × 4.75 in. A list of images makes a build (see below). |

**`figure_text`**: a figure plus 2–4 short points.

| Field | Size / style |
|---|---|
| `image` | 7.60 × 4.75 in |
| `text` | 4.13 × 4.75 in, list at 20/18/16 pt |

**`two_figures`**: a side-by-side comparison, such as before/after, two
conditions, or method vs baseline.

```yaml
left:  {label: Clean labels, image: figures/clean.png}
right: {label: 20% label noise, image: figures/noisy.png, highlight: [{box: [...]}]}
```

| Field | Size / style |
|---|---|
| `left.label`, `right.label` | 20 pt bold, one line |
| `left.image`, `right.image` | 5.87 × 4.25 in each |

**`text`**: a short list, used for motivation, methods steps, or caveats.

| Field | Size / style |
|---|---|
| `text` | 9.00 × 4.75 in, list at 24/20/18 pt, at most 5 top-level points |

**`two_columns`**: a comparison in words, such as ours vs theirs, pros vs cons,
or hypothesis vs result.

```yaml
left:  {heading: Uniform (baseline), text: [..., ...]}
right: {heading: Curriculum (ours),  text: [..., ...]}
```

| Field | Size / style |
|---|---|
| `left.heading`, `right.heading` | 20 pt bold |
| `left.text`, `right.text` | 5.87 × 4.20 in, list at 20/18/16 pt |

**`table`**: a booktabs-style table drawn by the builder.

```yaml
table:
  header: [Dataset, Uniform, Curriculum, Δ]
  rows:
    - [A · images, "0.812", "0.861", "+0.049"]
    - [Mean, "0.788", "0.834", "+0.046"]
  widths: [2.2, 1, 1.2, 1]   # optional relative column widths
  width: 9.6                 # optional total width in inches (default max(7.5, 2.4 × columns))
  align: [l, r, r, r]        # optional; numeric columns are right-aligned by default
  highlight: [2]             # optional 1-based body rows: tinted and bold
```

The rules are: top and bottom rules plus one rule under the header, with no
vertical lines and no zebra stripes. Text is 18 pt. The table is centred and
can hold at most 8 body rows. **Quote numbers as strings** (`"0.810"`) so YAML
keeps trailing zeros. The `table` layout is also the blank canvas ("Title Only")
for a diagram you place yourself.

**`summary`**: the closing slide. It takes the place of a "Thank you / Questions?"
slide.

| Field | Size / style |
|---|---|
| `headline` | "Take-home messages" is fine here |
| `points` | Numbered, 24 pt, 2–4 messages |
| `acknowledgements` | 14 pt |
| `contact` | 14 pt blue: email · code · preprint |

## Text

**Lists.** A YAML list gives one bullet per item. A nested list holds the
**previous** item's sub-points:

```yaml
text:
  - Needs per-example loss, which costs memory
  - - About 4 bytes per example        # sub-point of the item above
  - Gains shrink when labels are clean
```

Another way to write a sub-point is a single-key mapping:
`- "Needs per-example loss": [About 4 bytes per example]`. Never type `•` or
`-` into the text yourself, because bullets are automatic. Use two levels at most.

**Inline markup** works in every text field and in table cells:

| Markup | Result | Use |
|---|---|---|
| `**bold**` | bold | Names, terms on first use |
| `*italic*` | italic | Gene names, variables, titles |
| `==accent==` | bold blue | The one phrase the audience must catch. Use it once per slide at most. |
| `^{2}` | superscript | Units, citations: `R^{2}`, `cm^{-1}` |
| `_{i}` | subscript | `x_{i}`, `CO_{2}` |

A `\n` inside a non-list field starts a new paragraph. Chinese text needs no
markup, because CJK runs get the Chinese font (DengXian) automatically.

## Figures

- Use PNG or JPEG at 300 dpi. Convert PDF or SVG first.
- Images are fit inside the slot (never cropped) and centred. The builder warns
  below 150 dpi, and when the image fills less than 85 % of the slot, which
  means the export size is wrong.
- **Builds.** `image: [stage1.png, stage2.png, ...]` makes one slide per stage
  with the same headline. Draw every stage on identical axes so that only the
  new element appears. Highlights show on the last stage only.

### Highlights

```yaml
highlight:
  - box: [0.388, 0.124, 0.503, 0.243]   # x0, y0, x1, y1 as fractions of the image, origin top-left
    label: 47 vs 100 GPU-hours          # optional, 14 pt bold blue, placed above the box
```

Compute boxes from data coordinates with `slide_figures.highlight_box(fig, ax,
x=(x0, x1), y=(y0, y1))` instead of guessing them. Use one box per slide; two
is the maximum.

## What the builder checks

| Level | Check |
|---|---|
| ERROR | Text overflows its slot ("cut words, not font size") |
| ERROR | Headline wraps past 2 lines, or is missing |
| ERROR | Image missing or not a raster format; table has more than 8 rows or is too tall |
| ERROR | A `borrowed` figure has no `source` |
| WARN | Headline names a topic instead of a finding: under 4 words, "Results: …", "Distribution of …", "… results", a short "X vs Y", Chinese ending in 结果/分析/分布/比较/…, or ending in ":". Not checked on `summary` and backup slides. |
| WARN | More than 5 points (4 on `summary`), 3 bullet levels, a point over 12 words, over 40 words of body text on one slide, literal bullet characters. Two CJK characters count as one word. |
| WARN | Figure under 150 dpi, or filling under 85 % of its slot |
| WARN | A table cell wraps |
| WARN | More than 1.2 content slides per minute of `duration_min` |
| WARN | Speaker notes when `meta.notes` is not `true`; content slides without notes when it is |

Fix every ERROR. Fix each WARN as well, or say why it stays.
