"""Reusable visual system for publication figures — copy this per manuscript.

Every panel of every figure imports its palette, typography, and helpers from one
module like this, so a colour means the same thing in every panel, text never
wears a series colour, and reference lines look identical everywhere.

WHAT TO CHANGE PER MANUSCRIPT
-----------------------------
Swap ONLY the "Palette" block for your project's semantics, keeping the rules:

  * two semantic families that never share a hue;
  * the subject of the paper gets the strongest colour;
  * control/reference series are neutral grey (zero chroma) so they recede;
  * every series also carries a non-colour cue (line style or marker) so identity
    survives colour-blindness, grayscale printing, and forced-colours mode.

Validate the palette with the dataviz validator before shipping — do not eyeball
CVD separation:  node scripts/validate_palette.js "<hex,hex,...>" --mode light
(then --mode dark). Everything below the Palette block is project-agnostic and can
be reused verbatim.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# ==========================================================================
# Palette  — EXAMPLE (replace per manuscript; keep the rules in the docstring)
# ==========================================================================
# Example of the two-family pattern from a promoter-window study:
#   family 1 (warm)  = the subject: a "downstream" window carries the argument
#                      and gets the strongest colour; "distal" is the control and
#                      is deliberately neutral grey.
#   family 2 (green/violet) = a different factor, with hue = one binary attribute
#                      and line style = a second binary attribute (a 2x2 encoding),
#                      so the colour axis stays on the element the paper is about
#                      and every series has a secondary, non-colour cue.

CAT_COLORS = {          # family 1: categorical subject vs control
    "subject": "#D55E00",   # strongest colour — the thing the paper argues about
    "second": "#E8A33D",
    "control": "#6E6E6E",   # neutral grey, zero chroma — recedes
}
CAT_LABELS = {"subject": "Subject", "second": "Second", "control": "Control"}
CAT_ORDER = ["subject", "second", "control"]

# family 2: hue encodes one factor, dash encodes another (2x2)
FACTOR_COLORS = {True: "#009E73", False: "#9B5DE5"}
ARCH_PROPS = {
    "A":  {"color": FACTOR_COLORS[True],  "linestyle": "-"},
    "A2": {"color": FACTOR_COLORS[True],  "linestyle": (0, (4, 1.6))},
    "B":  {"color": FACTOR_COLORS[False], "linestyle": "-"},
    "B2": {"color": FACTOR_COLORS[False], "linestyle": (0, (4, 1.6))},
}

# ==========================================================================
# Ink and rule tokens  — text NEVER wears a series colour  (reuse verbatim)
# ==========================================================================
INK = "#1A1A1A"            # primary text
INK_SECONDARY = "#4D4D4D"  # secondary text / axis edges
INK_MUTED = "#8A8A8A"      # reference lines, de-emphasised annotation
RULE = "#C8C8C8"           # hairline grid, if ever used
SURFACE = "#FFFFFF"        # figure/axes background


# ==========================================================================
# Typography and rc  (reuse verbatim)
# ==========================================================================
def apply_rc() -> None:
    """Journal-scale typography: 7 pt ticks, 8 pt labels, hairline rules.

    Arial is listed first deliberately: on macOS, Helvetica/Helvetica Neue ship as
    .ttc collections matplotlib cannot select a bold face from, so
    ``fontweight="bold"`` silently renders regular. Arial ships a separate
    "Arial Bold.ttf", so bold panel letters and titles actually render bold.
    ``pdf.fonttype = 42`` embeds text as editable TrueType (journal requirement)
    rather than outlines.
    """
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica Neue", "Helvetica", "DejaVu Sans"],
            "font.size": 8,
            "axes.labelsize": 8,
            "axes.titlesize": 8,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "legend.fontsize": 7,
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "axes.edgecolor": INK_SECONDARY,
            "axes.linewidth": 0.7,
            "xtick.major.width": 0.7,
            "ytick.major.width": 0.7,
            "xtick.major.size": 2.8,
            "ytick.major.size": 2.8,
            "legend.frameon": False,
            "figure.facecolor": SURFACE,
            "axes.facecolor": SURFACE,
            "savefig.facecolor": SURFACE,
            "savefig.dpi": 400,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def clean_axis(ax: plt.Axes, grid_axis: str | None = None) -> None:
    """Drop the top/right box; optionally add a recessive grid behind the marks.

    Default is NO grid (Boss's preference). Pass ``grid_axis="y"`` only when a
    magnitude comparison genuinely needs a reading aid, and it goes *behind* the
    data.
    """
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if grid_axis:
        ax.set_axisbelow(True)
        ax.grid(axis=grid_axis, color=RULE, linewidth=0.5, alpha=0.7)


def reference_line(ax: plt.Axes, y=0.0, *, horizontal: bool = True) -> None:
    """The one house style for a zero-line / threshold: dashed, muted, on top.

    Every guide line in every figure looks identical and sits ABOVE the marks it
    annotates, so it reads as "guide, not data".
    """
    kw = dict(color=INK_MUTED, lw=0.7, ls=(0, (3, 2)), zorder=5)
    (ax.axhline if horizontal else ax.axvline)(y, **kw)


def place_panel_labels(
    fig: plt.Figure,
    groups: list[list[tuple[plt.Axes, str]]],
    fontsize: float = 12,
    dx: float = -1.0,
    dy: float = 2.0,
) -> None:
    """Bold, column-aligned panel letters that hug the top of each panel.

    ``groups`` is a list of column groups; each group is a list of ``(ax, label)``.
    Every letter in a group is placed at the same x — the leftmost tight-bbox edge
    among that group's panels — so panels stacked in a column share one letter
    margin (``a`` lines up with ``c``, ``b`` with ``d``), while each letter still
    sits at the top of its own panel. Keep long y-category labels narrow so the
    shared edge lands where the eye expects it.
    """
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    inv = fig.transFigure.inverted()
    for group in groups:
        left = min(
            inv.transform((ax.get_tightbbox(renderer).x0, 0.0))[0]
            for ax, _ in group
        )
        x = left + dx / 72 / fig.get_figwidth()
        for ax, label in group:
            y1 = ax.get_position().y1
            fig.text(
                x,
                y1 + dy / 72 / fig.get_figheight(),
                label,
                fontsize=fontsize,
                fontweight="bold",
                color=INK,
                ha="left",
                va="bottom",
            )


# ==========================================================================
# Statistics helpers  (reuse verbatim)
# ==========================================================================
def stars(p: float) -> str:
    """Significance marker. Feed an ALREADY-CORRECTED p-value."""
    if not np.isfinite(p):
        return "n.s."
    if p < 1e-3:
        return "***"
    if p < 1e-2:
        return "**"
    if p < 5e-2:
        return "*"
    return "n.s."


def bootstrap_mean_samples(
    values: np.ndarray,
    n_boot: int = 2000,
    seed: int = 20260722,
    batch: int = 250,
) -> np.ndarray:
    """Bootstrap distribution of the mean, batched to bound peak memory.

    Returns the full array of ``n_boot`` resampled means so a caller can draw its
    shape (a box of the bootstrap distribution) rather than only an interval.
    Prefer this over a normal approximation when the data are skewed or
    lattice-valued (e.g. density = k/L), where the median is unreliable.
    """
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    n = values.size
    if n == 0:
        return np.array([])
    rng = np.random.default_rng(seed)
    means = np.empty(n_boot, dtype=float)
    done = 0
    while done < n_boot:
        size = min(batch, n_boot - done)
        idx = rng.integers(0, n, size=(size, n))
        means[done : done + size] = values[idx].mean(axis=1)
        done += size
    return means


def bootstrap_ci(
    values: np.ndarray,
    n_boot: int = 2000,
    ci: float = 95.0,
    seed: int = 20260722,
    batch: int = 250,
) -> tuple[float, float, float]:
    """Mean with a percentile bootstrap CI (see ``bootstrap_mean_samples``)."""
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if values.size == 0:
        return np.nan, np.nan, np.nan
    means = bootstrap_mean_samples(values, n_boot=n_boot, seed=seed, batch=batch)
    lo, hi = np.percentile(means, [(100 - ci) / 2, 100 - (100 - ci) / 2])
    return float(values.mean()), float(lo), float(hi)


def paired_bootstrap_ratio_samples(
    numerator: np.ndarray,
    denominator: np.ndarray,
    n_boot: int = 2000,
    seed: int = 20260722,
    batch: int = 250,
) -> np.ndarray:
    """Bootstrap distribution of the percent difference of two paired means.

    When the same unit is measured in two conditions, resample over UNITS (rows)
    to keep the pairing intact. Returns the full array of ``n_boot`` resampled
    percent differences so a caller can draw its shape, not only its interval.
    """
    num = np.asarray(numerator, dtype=float)
    den = np.asarray(denominator, dtype=float)
    keep = np.isfinite(num) & np.isfinite(den)
    num, den = num[keep], den[keep]
    n = num.size
    if n == 0:
        return np.array([])
    rng = np.random.default_rng(seed)
    out = np.empty(n_boot, dtype=float)
    done = 0
    while done < n_boot:
        size = min(batch, n_boot - done)
        idx = rng.integers(0, n, size=(size, n))
        out[done : done + size] = (
            num[idx].mean(axis=1) / den[idx].mean(axis=1) - 1.0
        ) * 100.0
        done += size
    return out


def paired_bootstrap_ratio_ci(
    numerator: np.ndarray,
    denominator: np.ndarray,
    n_boot: int = 2000,
    ci: float = 95.0,
    seed: int = 20260722,
    batch: int = 250,
) -> tuple[float, float, float]:
    """Percent difference of two paired means, with a paired bootstrap CI.

    Point estimate is the ratio of the full-sample means; the interval is a
    percentile interval of the bootstrap distribution.
    """
    num = np.asarray(numerator, dtype=float)
    den = np.asarray(denominator, dtype=float)
    keep = np.isfinite(num) & np.isfinite(den)
    if not keep.any():
        return np.nan, np.nan, np.nan
    out = paired_bootstrap_ratio_samples(num, den, n_boot=n_boot, seed=seed, batch=batch)
    lo, hi = np.percentile(out, [(100 - ci) / 2, 100 - (100 - ci) / 2])
    point = (num[keep].mean() / den[keep].mean() - 1.0) * 100.0
    return float(point), float(lo), float(hi)


# ==========================================================================
# Output  — PNG while debugging, PDF only after lock  (reuse verbatim)
# ==========================================================================
def save_png(fig: plt.Figure, path, dpi: int = 400) -> None:
    """Iteration-phase output. PDF is emitted only once a figure is locked."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print(f"wrote {path}")


def save_final(fig: plt.Figure, stem, dpi: int = 400) -> None:
    """Locked-figure output: a preview PNG plus a vector PDF.

    ``apply_rc`` sets ``pdf.fonttype = 42`` so text embeds as editable TrueType
    rather than outlines, which is what journals ask for. ``stem`` is a suffix-less
    path; both ``.png`` and ``.pdf`` are written beside each other. Use only once a
    figure is approved — ``save_png`` stays for the iteration phase (Boss's rule:
    PNG while debugging, PDF only after lock).
    """
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    png, pdf = stem.with_suffix(".png"), stem.with_suffix(".pdf")
    fig.savefig(png, dpi=dpi, bbox_inches="tight", facecolor=SURFACE)
    fig.savefig(pdf, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print(f"wrote {png} + {pdf.name}")
