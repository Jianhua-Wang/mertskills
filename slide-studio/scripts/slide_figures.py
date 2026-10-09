"""Matplotlib helpers for figures that go on slide-studio slides.

A slide figure is drawn at the exact size of the slot it fills, with fonts at
slide scale, so the figure is placed 1:1: no scaling, no cropping, and text in
the figure matches the slide's type scale (16 pt ticks, 18 pt labels).

    import sys; sys.path.insert(0, "<skill>/scripts")
    from slide_figures import new_figure, save, SUBJECT, BASELINE

    fig, ax = new_figure("figure_text")          # 7.60 x 4.75 in
    ax.plot(x, y_base, color=BASELINE, ls="--", label="Baseline")
    ax.plot(x, y_ours, color=SUBJECT, label="Ours")
    save(fig, "figures/curves.png")

Colour rules are those of the figure-forge skill: the subject of the talk gets
the strongest colour, baselines are neutral grey, every series also has a
non-colour cue (line style or marker), and text never wears a series colour.
The Klein-blue accent belongs to the slide chrome and highlight boxes; keep it
out of the data.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
import design as D  # noqa: E402

INK = "#" + D.INK
INK_SECONDARY = "#" + D.INK_SECONDARY
INK_MUTED = "#" + D.INK_MUTED
GRID = "#E3E3E3"

# Data palette (Okabe-Ito, colour-blind safe). SUBJECT is the thing the talk is about.
SUBJECT = "#D55E00"     # vermillion
BASELINE = "#6E6E6E"    # neutral grey
SECOND = "#0072B2"      # blue, a second method or condition
THIRD = "#009E73"       # bluish green
FOURTH = "#E69F00"      # orange
SERIES = [SUBJECT, SECOND, THIRD, FOURTH, "#CC79A7", "#56B4E9"]

SLIDE_RC = {
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"],
    "font.size": 16,
    "axes.titlesize": 18,
    "axes.titleweight": "bold",
    "axes.titlelocation": "left",
    "axes.labelsize": 18,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "legend.fontsize": 16,
    "legend.frameon": False,
    "text.color": INK,
    "axes.labelcolor": INK,
    "axes.edgecolor": INK_SECONDARY,
    "axes.linewidth": 1.2,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
    "grid.color": GRID,
    "grid.linewidth": 0.8,
    "xtick.color": INK_SECONDARY,
    "ytick.color": INK_SECONDARY,
    "xtick.major.width": 1.2,
    "ytick.major.width": 1.2,
    "xtick.major.size": 5,
    "ytick.major.size": 5,
    "lines.linewidth": 3.0,
    "lines.markersize": 8,
    "patch.linewidth": 0,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.dpi": 300,
    "pdf.fonttype": 42,
    "svg.fonttype": "none",
}


def apply_rc() -> None:
    mpl.rcParams.update(SLIDE_RC)


def slot_size(layout: str, role: str = "image") -> tuple[float, float]:
    """(width, height) in inches of an image slot, e.g. slot_size("two_figures", "left_image")."""
    lay = D.LAYOUT_BY_KEY[layout]
    slot = lay.slot(role)
    if slot is None or slot.kind != "pic":
        pics = [s.role for s in lay.slots if s.kind == "pic"]
        raise KeyError(f"{layout} has no image slot {role!r}; image slots: {pics}")
    return slot.w, slot.h


def new_figure(layout: str, role: str = "image", nrows: int = 1, ncols: int = 1, **kw):
    """A figure exactly the size of the slot, with constrained layout."""
    apply_rc()
    if role == "image" and layout == "two_figures":
        role = "left_image"
    w, h = slot_size(layout, role)
    fig, ax = plt.subplots(nrows, ncols, figsize=(w, h), layout="constrained", **kw)
    return fig, ax


def highlight_box(fig, ax, x: tuple[float, float], y: tuple[float, float],
                  digits: int = 3) -> list[float]:
    """A data-space rectangle as the [x0, y0, x1, y1] image fractions deck.yaml wants.

    Call after plotting and before save(); the result is exact because save()
    does not trim the figure. Paste it into the slide's ``highlight: - box:``.

        box = highlight_box(fig, ax, x=(38, 56), y=(0.82, 0.92))
    """
    fig.canvas.draw()   # settle the constrained layout first
    to_fig = ax.transData + fig.transFigure.inverted()
    (fx0, fy0), (fx1, fy1) = to_fig.transform([(x[0], y[0]), (x[1], y[1])])
    left, right = sorted((fx0, fx1))
    bottom, top = sorted((fy0, fy1))
    return [round(float(v), digits) for v in (left, 1 - top, right, 1 - bottom)]


def save(fig, path: str | Path) -> Path:
    """Save at 300 dpi without trimming, so the PNG keeps the slot's aspect ratio."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=300)
    plt.close(fig)
    return path
