# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib>=3.8", "numpy>=1.26"]
# ///
"""Draw the example deck's figures at their slot sizes (synthetic data).

Usage:
    uv run assets/example/make_figures.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from slide_figures import (  # noqa: E402
    BASELINE, INK, INK_MUTED, INK_SECONDARY, SECOND, SUBJECT, highlight_box, new_figure,
    save,
)

OUT = HERE / "figures"
rng = np.random.default_rng(7)


def acc_curve(steps, rate, ceiling=0.9, noise=0.004):
    return ceiling * (1 - np.exp(-steps / rate)) + rng.normal(0, noise, steps.size)


def learning_curves(stage: int) -> None:
    """Accuracy vs compute; stage 1 shows the baseline only (for a build)."""
    fig, ax = new_figure("figure")
    steps = np.linspace(0, 100, 200)
    base = acc_curve(steps, 30)
    ours = acc_curve(steps, 14)
    target = 0.9 * (1 - np.exp(-100 / 30))      # the baseline's final accuracy
    ax.axhline(target, color=INK_MUTED, lw=1.5, ls=(0, (2, 2)))
    ax.text(101, target, "baseline final\naccuracy", va="center", ha="left",
            color=INK_SECONDARY, fontsize=16)
    ax.plot(steps, base, color=BASELINE, ls=(0, (6, 2)), label="Uniform sampling")
    ax.text(70, 0.74, "Uniform", color=INK, ha="left", va="top", fontsize=16)
    if stage == 2:
        ax.plot(steps, ours, color=SUBJECT, label="Curriculum sampling")
        ax.text(14, 0.64, "Curriculum", color=INK, ha="right", va="bottom",
                fontsize=16, fontweight="bold")
    ax.set_xlim(0, 100)
    ax.set_ylim(0.3, 1.0)
    ax.set_xlabel("Compute (GPU-hours)")
    ax.set_ylabel("Validation accuracy")
    if stage == 2:
        cross = 14 * np.log(1 / (1 - target / 0.9))
        print(f"curriculum reaches target at {cross:.0f} GPU-hours; highlight box:",
              highlight_box(fig, ax, x=(cross - 7, cross + 7), y=(target - 0.05, target + 0.05)))
    save(fig, OUT / f"curves_stage{stage}.png")


def wasted_steps() -> None:
    fig, ax = new_figure("figure_text")
    epochs = np.arange(1, 21)
    learned = 1 - np.exp(-epochs / 4.5)
    ax.fill_between(epochs, 0, learned * 100, color=BASELINE, alpha=0.35, lw=0)
    ax.plot(epochs, learned * 100, color=BASELINE, lw=2.5)
    ax.fill_between(epochs, learned * 100, 100, color=SUBJECT, alpha=0.18, lw=0)
    ax.text(15, 45, "already learned\n(revisited anyway)", ha="center", color=INK_SECONDARY,
            fontsize=16)
    ax.text(3.2, 88, "still\nlearning", ha="center", color=INK_SECONDARY, fontsize=16)
    ax.set_xlim(1, 20)
    ax.set_xticks([1, 5, 10, 15, 20])
    ax.set_ylim(0, 100)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Steps on learned examples (%)")
    save(fig, OUT / "wasted_steps.png")


def noise_panels() -> None:
    for name, gap in (("clean", 0.012), ("noisy", 0.06)):
        fig, ax = new_figure("two_figures", "left_image")
        x = np.arange(5)
        base = np.array([0.81, 0.77, 0.84, 0.72, 0.79])
        ours = base + gap + rng.normal(0, 0.006, 5)
        w = 0.36
        ax.bar(x - w / 2, base, w, color=BASELINE, label="Uniform")
        ax.bar(x + w / 2, ours, w, color=SUBJECT, label="Curriculum", hatch="//",
               edgecolor="white")
        ax.set_xticks(x, ["A", "B", "C", "D", "E"])
        ax.set_ylim(0.6, 1.0)
        ax.set_xlabel("Dataset")
        ax.set_ylabel("Accuracy")
        ax.legend(loc="upper left", ncols=2)
        save(fig, OUT / f"bars_{name}.png")


def paper_teaser() -> None:
    fig, ax = new_figure("paper")
    n = 160
    diff = rng.uniform(0, 1, n)
    weight = np.clip(0.15 + 0.9 * diff + rng.normal(0, 0.08, n), 0, None)
    ax.scatter(diff, weight, s=28, color=SECOND, alpha=0.75, lw=0)
    ax.set_xlabel("Example difficulty")
    ax.set_ylabel("Sampling weight")
    ax.set_title("Weight tracks difficulty")
    save(fig, OUT / "paper_teaser.png")


if __name__ == "__main__":
    learning_curves(1)
    learning_curves(2)
    wasted_steps()
    noise_panels()
    paper_teaser()
    print(f"figures written to {OUT}")
