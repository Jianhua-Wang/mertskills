# /// script
# requires-python = ">=3.10"
# dependencies = ["pymupdf>=1.24", "pillow>=10"]
# ///
"""Render a .pptx to PDF, one PNG per slide, and a contact sheet for review.

Usage:
    uv run scripts/render_deck.py deck.pptx [--out DIR] [--dpi 110] [--engine auto|powerpoint|soffice]

Writes DIR/deck.pdf, DIR/slide-01.png ..., and DIR/contact.png (default DIR is
"<deck>-render" next to the deck). PowerPoint (macOS, via AppleScript) renders
exactly what the audience will see, so it is preferred; LibreOffice is the
fallback and may substitute fonts.
"""

from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pymupdf as fitz
from PIL import Image, ImageDraw, ImageFont

POWERPOINT_APP = Path("/Applications/Microsoft PowerPoint.app")


def export_powerpoint(pptx: Path, pdf: Path) -> None:
    script = f'''
    tell application "Microsoft PowerPoint"
        open (POSIX file "{pptx}")
        delay 1
        set pres to active presentation
        save pres in (POSIX file "{pdf}") as save as PDF
        close pres saving no
    end tell
    '''
    subprocess.run(["osascript", "-e", script], check=True, capture_output=True, text=True,
                   timeout=300)


def export_soffice(pptx: Path, pdf: Path) -> None:
    exe = shutil.which("soffice") or shutil.which("libreoffice")
    if exe is None:
        raise RuntimeError("neither PowerPoint nor LibreOffice is available")
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([exe, "--headless", "--convert-to", "pdf", "--outdir", tmp, str(pptx)],
                       check=True, capture_output=True, timeout=300)
        shutil.move(str(Path(tmp) / (pptx.stem + ".pdf")), pdf)


def to_pdf(pptx: Path, pdf: Path, engine: str) -> str:
    if pdf.exists():
        pdf.unlink()
    use_ppt = engine == "powerpoint" or (
        engine == "auto" and platform.system() == "Darwin" and POWERPOINT_APP.exists())
    if use_ppt:
        try:
            export_powerpoint(pptx, pdf)
            if pdf.exists():
                return "powerpoint"
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            if engine == "powerpoint":
                raise RuntimeError(f"PowerPoint export failed: {getattr(e, 'stderr', e)}") from e
            print(f"PowerPoint export failed, trying LibreOffice: {getattr(e, 'stderr', e)}",
                  file=sys.stderr)
    export_soffice(pptx, pdf)
    return "soffice"


def rasterize(pdf: Path, out: Path, dpi: int) -> list[Path]:
    for old in out.glob("slide-*.png"):
        old.unlink()
    paths = []
    with fitz.open(pdf) as doc:
        for i, page in enumerate(doc, 1):
            pix = page.get_pixmap(dpi=dpi)
            p = out / f"slide-{i:02d}.png"
            pix.save(p)
            paths.append(p)
    return paths


def contact_sheet(pngs: list[Path], out: Path, cols: int = 3, thumb_w: int = 560) -> Path:
    thumbs = []
    for p in pngs:
        im = Image.open(p).convert("RGB")
        im.thumbnail((thumb_w, thumb_w))
        thumbs.append(im)
    th = thumbs[0].height
    pad, label_h = 24, 26
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (pad + cols * (thumb_w + pad), pad + rows * (th + label_h + pad)),
                      (236, 236, 236))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("Arial.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
    for i, im in enumerate(thumbs):
        r, c = divmod(i, cols)
        x, y = pad + c * (thumb_w + pad), pad + r * (th + label_h + pad)
        draw.text((x, y), str(i + 1), fill=(90, 90, 90), font=font)
        sheet.paste(im, (x, y + label_h))
        draw.rectangle([x - 1, y + label_h - 1, x + im.width, y + label_h + im.height],
                       outline=(200, 200, 200))
    path = out / "contact.png"
    sheet.save(path)
    return path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("deck", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--dpi", type=int, default=110)
    ap.add_argument("--engine", choices=["auto", "powerpoint", "soffice"], default="auto")
    ap.add_argument("--cols", type=int, default=3)
    args = ap.parse_args()

    deck = args.deck.resolve()
    out = (args.out or deck.with_name(deck.stem + "-render")).resolve()
    out.mkdir(parents=True, exist_ok=True)
    pdf = out / (deck.stem + ".pdf")
    engine = to_pdf(deck, pdf, args.engine)
    pngs = rasterize(pdf, out, args.dpi)
    sheet = contact_sheet(pngs, out, args.cols)
    print(f"rendered {len(pngs)} slides with {engine}")
    print(f"pdf:     {pdf}")
    print(f"slides:  {out}/slide-NN.png")
    print(f"contact: {sheet}")


if __name__ == "__main__":
    main()
