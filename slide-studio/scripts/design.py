"""Design tokens and layout geometry for the slide-studio academic template.

This module is the single source of truth for the template's look.
``make_template.py`` writes ``assets/academic-template.pptx`` from these values,
and ``build_deck.py`` uses the same values to measure text and place figures.
To change the design, edit this file and rerun ``make_template.py``; never
hand-edit the template.

Style "A, minimal white": white background on every slide, near-black ink, one
accent colour used sparingly (kickers, section numbers, bullets, emphasis, the
headline rule and the bottom bar). Slide chrome never uses a data colour, so the
semantic palette of the figures (see the figure-forge skill) is the only colour
story inside a content slide's body. There is no footer text: the only chrome
text is the slide number, at the same 14 pt minimum as every other text.

All geometry is in inches on a 13.333 x 7.5 in (16:9) canvas.
"""

from __future__ import annotations

from dataclasses import dataclass, field

EMU_PER_IN = 914400
EMU_PER_PT = 12700

SLIDE_W = 13.333
SLIDE_H = 7.5

# ==========================================================================
# Colour tokens (hex, no '#')
# ==========================================================================
INK = "1A1A1A"            # primary text (same ink as figure-forge)
INK_SECONDARY = "4D4D4D"  # subtitles, secondary text
INK_MUTED = "767676"      # sources, slide number; 4.5:1 on white (WCAG AA)
RULE = "8C8C8C"           # table rules
HAIRLINE = "D9D9D9"       # the headline divider
SURFACE = "FFFFFF"        # slide background
ACCENT = "002FA7"         # Klein blue: kickers, numbers, bullets, emphasis, highlight boxes, rule mark, bar
ACCENT_TINT = "E6EAF6"    # quiet accent wash: highlighted table rows

# Theme slots. accent2-6 are Okabe-Ito hues, so PowerPoint-native charts and
# tables a person adds by hand start from a colour-blind-safe palette.
THEME_NAME = "slide-studio academic"
THEME_COLORS = {
    "dk1": INK,
    "lt1": SURFACE,
    "dk2": INK_SECONDARY,
    "lt2": "F2F2F2",
    "accent1": ACCENT,
    "accent2": "D55E00",
    "accent3": "009E73",
    "accent4": "E69F00",
    "accent5": "56B4E9",
    "accent6": "CC79A7",
    "hlink": ACCENT,
    "folHlink": "6B4C9A",
}

# ==========================================================================
# Typography
# ==========================================================================
# Arial ships with every Office install and renders bold faithfully. DengXian
# (等线) ships with Office on both macOS and Windows, so Chinese text renders the
# same on any machine that has PowerPoint.
FONT_LATIN = "Arial"
FONT_EA = "DengXian"

# Line box used by the fit checks: Arial ascent + descent is ~1.12 em; 1.17
# leaves a little slack so the check errs toward "overflow".
LINE_HEIGHT = 1.17

@dataclass(frozen=True)
class TextStyle:
    """How one placeholder's text looks. ``sizes`` lists pt per outline level."""

    sizes: tuple[int, ...]
    bold: bool = False
    color: str = "tx1"            # scheme name ("tx1", "accent1") or hex
    caps: bool = False
    spacing: int = 0              # character spacing, 1/100 pt
    anchor: str = "t"             # t | ctr | b
    align: str = "l"              # l | ctr | r
    bullets: str = "none"         # none | dot | number
    space_before: tuple[int, ...] = (0,)   # pt before each paragraph, per level
    line_spacing: int = 100       # percent


TEXT_STYLES: dict[str, TextStyle] = {
    # hero slides
    "kicker": TextStyle((14,), bold=True, color="accent1", caps=True, spacing=100),
    "hero_title": TextStyle((40,), bold=True, line_spacing=95),
    "paper_title": TextStyle((30,), bold=True, line_spacing=95),
    "section_number": TextStyle((48,), bold=True, color="accent1"),
    "section_title": TextStyle((40,), bold=True, line_spacing=95),
    "statement": TextStyle((32,), bold=True, line_spacing=100, space_before=(0, 12)),
    "subtitle": TextStyle((22,), color=INK_SECONDARY),
    "section_subtitle": TextStyle((20,), color=INK_SECONDARY),
    "authors": TextStyle((18,)),
    "paper_authors": TextStyle((16,), color=INK_SECONDARY),
    "citation": TextStyle((16,), color="accent1"),
    "affiliation": TextStyle((14,), color=INK_SECONDARY),
    "presenter": TextStyle((14,), color=INK_MUTED),
    # content slides
    "headline": TextStyle((30,), bold=True, line_spacing=95, anchor="b"),
    "label": TextStyle((20,), bold=True),
    "body": TextStyle((24, 20, 18), bullets="dot", space_before=(14, 4, 2)),
    "body_compact": TextStyle((20, 18, 16), bullets="dot", space_before=(12, 4, 2)),
    "numbered": TextStyle((24,), bullets="number", space_before=(18,)),
    "small": TextStyle((14,), color=INK_SECONDARY, space_before=(4,)),
    "contact": TextStyle((14,), color="accent1", anchor="b"),
    "source": TextStyle((14,), color=INK_MUTED, anchor="b"),
    "slide_number": TextStyle((14,), color=INK_MUTED, anchor="b", align="r"),
    "figure_prompt": TextStyle((14,), color=INK_MUTED, anchor="ctr", align="ctr"),
    # tables (drawn by build_deck.py, not a placeholder)
    "table_header": TextStyle((18,), bold=True),
    "table_body": TextStyle((18,)),
}

# Bullet glyphs per level for the "dot" style; level 1 carries the accent.
BULLET_CHARS = ("•", "–", "•")
BULLET_INDENT = 0.28  # in, hanging indent per level

# ==========================================================================
# Grid
# ==========================================================================
M = 0.6                       # side margin of content slides
CONTENT_W = SLIDE_W - 2 * M   # 12.133
GAP = 0.4                     # gutter between columns
HERO_X = 0.9                  # left inset of title / section / statement slides
HERO_W = SLIDE_W - 2 * HERO_X

HEAD_Y, HEAD_H = 0.4, 1.0     # headline: two lines of 30 pt, sits on the rule
BODY_Y, BODY_H = 1.75, 4.75   # content region: 1.75 -> 6.5
SOURCE_Y, SOURCE_H = 6.55, 0.5   # two lines of 14 pt, bottom-anchored
NUM_W, NUM_H = 0.8, 0.3       # slide number, bottom-right, on the source baseline
NUM_X = SLIDE_W - M - NUM_W
NUM_Y = SOURCE_Y + SOURCE_H - NUM_H
SOURCE_W = NUM_X - 0.3 - M    # the source line stops short of the slide number

# Headline divider (content layouts): a full-width hairline with a short accent
# mark at its left end, both centred on HEAD_RULE_Y.
HEAD_RULE_Y = 1.55
HEAD_RULE_PT = 0.75
HEAD_MARK_W, HEAD_MARK_PT = 1.0, 4.0
# Bottom bar (every slide, from the master): a thin full-width accent band.
BAR_H = 0.12
BAR_Y = SLIDE_H - BAR_H

COL2_W = (CONTENT_W - GAP) / 2           # 5.867
COL2_X = M + COL2_W + GAP                # right column x
FIGTEXT_FIG_W = 7.6
FIGTEXT_TEXT_X = M + FIGTEXT_FIG_W + GAP
FIGTEXT_TEXT_W = SLIDE_W - M - FIGTEXT_TEXT_X
LABEL_H = 0.45


@dataclass(frozen=True)
class Slot:
    """One placeholder on a layout.

    ``role`` is the name build_deck.py fills; ``kind`` is the OOXML placeholder
    type; ``idx`` is the placeholder index (None for title-type placeholders).
    """

    role: str
    kind: str
    idx: int | None
    x: float
    y: float
    w: float
    h: float
    style: str
    prompt: str = ""
    max_h: float | None = None   # tallest the text may grow on a stacked layout

    @property
    def limit_h(self) -> float:
        return self.max_h or self.h


@dataclass(frozen=True)
class Stack:
    """Vertical packing for hero slides.

    The layout's slot positions are the defaults a person sees in PowerPoint.
    When build_deck.py fills a hero slide it measures each filled slot, stacks
    them top to bottom with ``gaps`` (gap before each role; empty roles are
    skipped), and centres the block between ``top`` and ``bottom``. A one-line
    title then sits as close to its subtitle as a two-line one does.
    """

    roles: tuple[str, ...]
    gaps: tuple[float, ...]
    top: float
    bottom: float
    lift: float = 0.25   # raise the block above true centre (optical centre)


@dataclass(frozen=True)
class Layout:
    key: str        # name used in deck.yaml
    name: str       # name shown in PowerPoint's layout gallery
    ooxml_type: str
    slots: tuple[Slot, ...] = field(default_factory=tuple)
    stack: Stack | None = None

    def slot(self, role: str) -> Slot | None:
        for s in self.slots:
            if s.role == role:
                return s
        return None


def _headline() -> Slot:
    return Slot("headline", "title", None, M, HEAD_Y, CONTENT_W, HEAD_H, "headline",
                "Headline: one full sentence that states the finding")


def _source(idx: int, x: float = M, w: float = SOURCE_W) -> Slot:
    return Slot("source", "body", idx, x, SOURCE_Y, w, SOURCE_H, "source",
                "Source or note: citation, n, test, error bars")


def _slide_number() -> Slot:
    return Slot("slide_number", "sldNum", 12, NUM_X, NUM_Y, NUM_W, NUM_H, "slide_number")


def _fig_prompt(w: float, h: float) -> str:
    return f"Figure · export at {w:.2f} × {h:.2f} in"


LAYOUTS: tuple[Layout, ...] = (
    Layout("title", "Title", "title", (
        Slot("kicker", "body", 13, HERO_X, 1.85, HERO_W, 0.3, "kicker", "Event \u00b7 date"),
        Slot("title", "ctrTitle", None, HERO_X, 2.25, HERO_W, 1.3, "hero_title", "Talk title",
             max_h=1.85),
        Slot("subtitle", "subTitle", 1, HERO_X, 3.75, HERO_W, 0.75, "subtitle", "Subtitle"),
        Slot("authors", "body", 14, HERO_X, 4.95, HERO_W, 0.6, "authors", "Presenter, co-authors"),
        Slot("affiliation", "body", 15, HERO_X, 5.6, HERO_W, 0.5, "affiliation", "Affiliation"),
    ), Stack(("kicker", "title", "subtitle", "authors", "affiliation"),
             (0, 0.14, 0.22, 0.5, 0.08), 0.6, 6.9)),
    Layout("paper", "Paper", "obj", (
        Slot("kicker", "body", 13, HERO_X, 1.5, 7.2, 0.3, "kicker", "Journal club \u00b7 date"),
        Slot("title", "title", None, HERO_X, 1.95, 7.2, 1.85, "paper_title", "Paper title"),
        Slot("authors", "body", 14, HERO_X, 3.95, 7.2, 0.8, "paper_authors",
             "First author, \u2026, last author"),
        Slot("citation", "body", 15, HERO_X, 4.85, 7.2, 0.55, "citation", "Journal \u00b7 year \u00b7 DOI"),
        Slot("presenter", "body", 16, HERO_X, 5.75, 7.2, 0.35, "presenter", "Presented by \u2026"),
        Slot("image", "pic", 17, 8.5, 0.9, SLIDE_W - M - 8.5, 5.7, "figure_prompt",
             _fig_prompt(SLIDE_W - M - 8.5, 5.7)),
    ), Stack(("kicker", "title", "authors", "citation", "presenter"),
             (0, 0.14, 0.3, 0.12, 0.5), 0.6, 6.9)),
    Layout("section", "Section", "secHead", (
        Slot("number", "body", 13, HERO_X, 2.3, HERO_W, 0.8, "section_number", "01"),
        Slot("title", "title", None, HERO_X, 3.15, HERO_W, 1.3, "section_title", "Section title"),
        Slot("subtitle", "body", 14, HERO_X, 4.6, HERO_W, 0.7, "section_subtitle",
             "One line on what this part shows"),
    ), Stack(("number", "title", "subtitle"), (0, 0.06, 0.3), 0.6, 6.9)),
    Layout("statement", "Statement", "obj", (
        Slot("kicker", "body", 13, HERO_X, 2.35, HERO_W, 0.3, "kicker", "Key question"),
        Slot("text", "title", None, HERO_X, 2.9, HERO_W, 2.6, "statement",
             "One sentence the audience must remember"),
        _source(14, HERO_X, NUM_X - 0.3 - HERO_X),
        _slide_number(),
    ), Stack(("kicker", "text"), (0, 0.25), 0.6, 6.4)),
    Layout("figure", "Figure", "picTx", (
        _headline(),
        Slot("image", "pic", 13, M, BODY_Y, CONTENT_W, BODY_H, "figure_prompt",
             _fig_prompt(CONTENT_W, BODY_H)),
        _source(14),
        _slide_number(),
    )),
    Layout("figure_text", "Figure + Text", "picTx", (
        _headline(),
        Slot("image", "pic", 13, M, BODY_Y, FIGTEXT_FIG_W, BODY_H, "figure_prompt",
             _fig_prompt(FIGTEXT_FIG_W, BODY_H)),
        Slot("text", "body", 14, FIGTEXT_TEXT_X, BODY_Y, FIGTEXT_TEXT_W, BODY_H, "body_compact",
             "Two to four short points"),
        _source(15),
        _slide_number(),
    )),
    Layout("two_figures", "Two Figures", "twoObj", (
        _headline(),
        Slot("left_label", "body", 15, M, BODY_Y, COL2_W, LABEL_H, "label", "Left panel label"),
        Slot("left_image", "pic", 13, M, BODY_Y + LABEL_H + 0.05, COL2_W, BODY_H - LABEL_H - 0.05,
             "figure_prompt", _fig_prompt(COL2_W, BODY_H - LABEL_H - 0.05)),
        Slot("right_label", "body", 16, COL2_X, BODY_Y, COL2_W, LABEL_H, "label", "Right panel label"),
        Slot("right_image", "pic", 14, COL2_X, BODY_Y + LABEL_H + 0.05, COL2_W, BODY_H - LABEL_H - 0.05,
             "figure_prompt", _fig_prompt(COL2_W, BODY_H - LABEL_H - 0.05)),
        _source(17),
        _slide_number(),
    )),
    Layout("text", "Text", "obj", (
        _headline(),
        Slot("text", "body", 1, M, BODY_Y, 9.0, BODY_H, "body", "Three to five short points"),
        _source(14),
        _slide_number(),
    )),
    Layout("two_columns", "Two Columns", "twoTxTwoObj", (
        _headline(),
        Slot("left_heading", "body", 13, M, BODY_Y, COL2_W, LABEL_H, "label", "Left heading"),
        Slot("left_text", "body", 14, M, BODY_Y + LABEL_H + 0.1, COL2_W, BODY_H - LABEL_H - 0.1, "body_compact",
             "Points"),
        Slot("right_heading", "body", 15, COL2_X, BODY_Y, COL2_W, LABEL_H, "label", "Right heading"),
        Slot("right_text", "body", 16, COL2_X, BODY_Y + LABEL_H + 0.1, COL2_W, BODY_H - LABEL_H - 0.1,
             "body_compact", "Points"),
        _source(17),
        _slide_number(),
    )),
    Layout("table", "Title Only", "titleOnly", (
        _headline(),
        _source(13),
        _slide_number(),
    )),
    Layout("summary", "Summary", "obj", (
        _headline(),
        Slot("points", "body", 13, M, BODY_Y, 10.0, 3.65, "numbered", "Two to four take-home messages"),
        Slot("acknowledgements", "body", 14, M, 5.5, SOURCE_W, 0.75, "small", "Acknowledgements"),
        Slot("contact", "body", 15, M, 6.65, SOURCE_W, 0.4, "contact", "Email · code · preprint"),
        _slide_number(),
    )),
)

LAYOUT_BY_KEY = {lay.key: lay for lay in LAYOUTS}

# Region the table layout fills (below the headline, above the source line).
TABLE_REGION = (M, BODY_Y, CONTENT_W, BODY_H)
TABLE_ROW_H = 0.5
TABLE_MAX_ROWS = 9    # header + 8 body rows
TABLE_RULE_PT = (1.25, 0.75, 1.25)   # top, below header, bottom (booktabs)
