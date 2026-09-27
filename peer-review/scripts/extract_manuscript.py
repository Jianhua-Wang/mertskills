#!/usr/bin/env python3
"""Extract a manuscript folder (or a single file) into plain text for peer review.

What it handles:
  DOCX/DOCM   Body text with headings, list numbers and tables. Tracked changes are
              shown as {+[author] inserted+} and {-[author] deleted-}. Word comments
              are listed with their anchored text, author, date, reply links and
              resolved state. Footnotes, endnotes and embedded media are listed too.
  PDF         Page-by-page text. On pages with a line-number margin (journal reviewer
              PDFs), each visual line keeps its line number so comments can cite
              "Line 131". Annotations are listed: highlights with the highlighted text,
              sticky notes and replies. Pages that look like figures are flagged, and
              pages can be rendered to PNG.
  DOC/RTF/ODT/HTML/XLS
              Converted with macOS textutil, pandoc, antiword or LibreOffice,
              whichever is available.
  PPTX        Slide text and speaker notes.
  XLSX        Cell values, via openpyxl or a zip fallback.
  Text/code   CSV, TSV, TXT, MD, TeX, R, Python and similar files, plus notebooks.
  Images      Listed with their pixel size. --figures-to-png converts them (TIFF, BMP,
              GIF, WebP, ...) to downscaled PNGs that can be viewed.
  Archives    ZIP/TAR files are listed; --unzip extracts and processes them.

File metadata (author names in document properties) is printed only with --meta, to
respect double-blind review.

Examples:
  extract_manuscript.py "2025-04-30 Journal" --outdir /tmp/review/extract --figures-to-png
  extract_manuscript.py reviewer.pdf --outdir /tmp/review/extract --render-figure-pages
  extract_manuscript.py reviewer.pdf --outdir /tmp/review/extract --render-pages 12,14-15
  extract_manuscript.py comments.docx          # print to stdout
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import warnings
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "w15": "http://schemas.microsoft.com/office/word/2012/wordml",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "ss": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "ep": "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties",
}


def _q(prefix: str, tag: str) -> str:
    return "{%s}%s" % (NS[prefix], tag)


def W(tag: str) -> str:
    return _q("w", tag)


DOCX_EXT = {".docx", ".docm", ".dotx", ".dotm"}
PDF_EXT = {".pdf"}
CONVERT_EXT = {".doc", ".rtf", ".odt", ".html", ".htm", ".webarchive", ".wordml", ".xls", ".ppt"}
PPTX_EXT = {".pptx", ".pptm"}
XLSX_EXT = {".xlsx", ".xlsm"}
TABLE_TEXT_EXT = {".csv", ".tsv"}
TEXT_EXT = {
    ".txt", ".md", ".markdown", ".tex", ".bib", ".json", ".yaml", ".yml", ".toml", ".ini",
    ".cfg", ".log", ".xml", ".r", ".rmd", ".qmd", ".py", ".sh", ".pl", ".c", ".cc", ".cpp",
    ".h", ".hpp", ".java", ".js", ".ts", ".m", ".jl", ".sql", ".sas", ".do", ".stan", ".nf",
    ".smk", ".wdl", ".go", ".rs", ".scala", ".f90",
}
IMAGE_EXT = {
    ".tif", ".tiff", ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".jp2", ".heic",
    ".eps", ".svg", ".emf", ".wmf", ".ai", ".psd",
}
ARCHIVE_EXT = {".zip", ".tar", ".tgz", ".gz", ".bz2", ".xz"}
SKIP_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini", "Icon\r"}
SKIP_DIRS = {"__MACOSX", ".git", ".svn", "__pycache__", ".ipynb_checkpoints"}

# Word's "Symbol" font maps Latin code points to Greek letters and math signs.
SYMBOL_MAP = {
    0x61: "α", 0x62: "β", 0x63: "χ", 0x64: "δ", 0x65: "ε", 0x66: "φ", 0x67: "γ", 0x68: "η",
    0x69: "ι", 0x6A: "ϕ", 0x6B: "κ", 0x6C: "λ", 0x6D: "μ", 0x6E: "ν", 0x6F: "ο", 0x70: "π",
    0x71: "θ", 0x72: "ρ", 0x73: "σ", 0x74: "τ", 0x75: "υ", 0x77: "ω", 0x78: "ξ", 0x79: "ψ",
    0x7A: "ζ", 0x41: "Α", 0x42: "Β", 0x43: "Χ", 0x44: "Δ", 0x45: "Ε", 0x46: "Φ", 0x47: "Γ",
    0x48: "Η", 0x49: "Ι", 0x4B: "Κ", 0x4C: "Λ", 0x4D: "Μ", 0x4E: "Ν", 0x4F: "Ο", 0x50: "Π",
    0x51: "Θ", 0x52: "Ρ", 0x53: "Σ", 0x54: "Τ", 0x55: "Υ", 0x57: "Ω", 0x58: "Ξ", 0x59: "Ψ",
    0x5A: "Ζ", 0xA3: "≤", 0xB3: "≥", 0xB1: "±", 0xB4: "×", 0xB8: "÷", 0xB0: "°", 0xAE: "→",
    0xAC: "←", 0xAD: "↑", 0xAF: "↓", 0xB9: "≠", 0xBB: "≈", 0xA5: "∞", 0xD6: "√", 0xE5: "∑",
    0xB6: "∂", 0xB7: "•", 0x2D: "−", 0xBA: "≡", 0xA2: "′", 0xB2: "″", 0xC6: "∅", 0xCE: "∈",
}

LINE_NUMBER_RE = re.compile(r"^\d{1,5}$")


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def natural_key(s: str):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", str(s))]


def safe_name(rel: str, limit: int = 120) -> str:
    s = re.sub(r"[\\/]+", "__", rel)
    s = re.sub(r"[^\w.\-]+", "_", s, flags=re.UNICODE).strip("._")
    return s[:limit] or "file"


def fmt_ranges(nums) -> str:
    nums = sorted(set(nums))
    out, start, prev = [], None, None
    for n in nums:
        if start is None:
            start = prev = n
        elif n == prev + 1:
            prev = n
        else:
            out.append(str(start) if start == prev else "%d-%d" % (start, prev))
            start = prev = n
    if start is not None:
        out.append(str(start) if start == prev else "%d-%d" % (start, prev))
    return ", ".join(out)


def parse_ranges(spec: str, n_pages: int) -> list[int]:
    if spec.strip().lower() == "all":
        return list(range(1, n_pages + 1))
    pages = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            a = int(a) if a.strip() else 1
            b = int(b) if b.strip() else n_pages
            pages.update(range(max(1, a), min(n_pages, b) + 1))
        else:
            p = int(part)
            if 1 <= p <= n_pages:
                pages.add(p)
    return sorted(pages)


def count_words(text: str) -> int:
    text = re.sub(r"\{[+-]\[[^\]]*\] ?|[+-]\}|\[\[C\d+>|<C\d+\]\]", " ", text)
    return len(re.findall(r"\w+", text))


def truncate(text: str, max_chars: int | None) -> str:
    if max_chars and len(text) > max_chars:
        return text[:max_chars] + "\n... [truncated at %d of %d characters; use --max-chars or --outdir]\n" % (
            max_chars, len(text))
    return text


def import_fitz():
    try:
        import pymupdf as fitz  # PyMuPDF >= 1.24
        return fitz
    except ImportError:
        pass
    try:
        import fitz  # older PyMuPDF
        return fitz
    except ImportError:
        return None


def run_cmd(cmd: list[str], timeout: int = 180) -> tuple[int, bytes, bytes]:
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, b"", str(e).encode()


class Result:
    """What one extractor returns: the text to save, a one-line summary, extra files."""

    def __init__(self, text: str, summary: str, extras: list[str] | None = None):
        self.text = text
        self.summary = summary
        self.extras = extras or []


# ---------------------------------------------------------------------------
# DOCX
# ---------------------------------------------------------------------------

SKIP_TAGS = {
    W("rPr"), W("pPr"), W("instrText"), W("delInstrText"), W("sectPr"), W("tblPr"),
    W("tblGrid"), W("trPr"), W("tcPr"), W("fldData"), _q("mc", "Fallback"),
}


def _val(el, attr="val"):
    return el.get(W(attr)) if el is not None else None


def _symbol_text(s: str) -> str:
    out = []
    for ch in s:
        code = ord(ch)
        if code >= 0xF000:
            code -= 0xF000
        out.append(SYMBOL_MAP.get(code, chr(code) if code >= 0x20 else ""))
    return "".join(out)


def _to_letters(v: int) -> str:
    v = max(1, v)
    return chr(ord("A") + (v - 1) % 26) * ((v - 1) // 26 + 1)


def _to_roman(v: int) -> str:
    vals = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
            (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    out = []
    for n, s in vals:
        while v >= n:
            out.append(s)
            v -= n
    return "".join(out) or str(v)


def _to_chinese(v: int) -> str:
    digits = "零一二三四五六七八九"
    if v <= 0 or v >= 100:
        return str(v)
    if v < 10:
        return digits[v]
    tens, ones = divmod(v, 10)
    return ("" if tens == 1 else digits[tens]) + "十" + (digits[ones] if ones else "")


def _fmt_num(v: int, fmt: str) -> str:
    if fmt == "decimalZero":
        return "%02d" % v
    if fmt == "lowerLetter":
        return _to_letters(v).lower()
    if fmt == "upperLetter":
        return _to_letters(v)
    if fmt == "lowerRoman":
        return _to_roman(v).lower()
    if fmt == "upperRoman":
        return _to_roman(v)
    if fmt.startswith(("chinese", "ideograph", "japanese", "taiwanese")):
        return _to_chinese(v)
    if fmt.startswith("decimalEnclosedCircle") and 1 <= v <= 20:
        return chr(0x2460 + v - 1)
    return str(v)


class DocxReader:
    def __init__(self, path: Path, changes: str = "markup", max_rows: int = 200):
        self.z = zipfile.ZipFile(path)
        self.names = set(self.z.namelist())
        self.changes = changes
        self.max_rows = max_rows
        self.track: dict[str, list[int]] = {}
        self.counting = False
        self.counters: dict = {}
        self.doc_part = self._main_part()
        self.rels = self._rels_for(self.doc_part)
        self.styles: dict = {}
        self.nums: dict = {}
        self.absnums: dict = {}
        self._load_styles()
        self._load_numbering()

    # -- package plumbing
    def xml(self, name):
        if name and name in self.names:
            return ET.fromstring(self.z.read(name))
        return None

    def _main_part(self) -> str:
        root = self.xml("_rels/.rels")
        if root is not None:
            for rel in root.findall("rel:Relationship", NS):
                if rel.get("Type", "").endswith("/officeDocument"):
                    return rel.get("Target", "word/document.xml").lstrip("/")
        return "word/document.xml"

    def _rels_for(self, part: str) -> dict:
        base = posixpath.dirname(part)
        rels_name = posixpath.join(base, "_rels", posixpath.basename(part) + ".rels")
        out = {}
        root = self.xml(rels_name)
        if root is None:
            return out
        for rel in root.findall("rel:Relationship", NS):
            target = rel.get("Target", "")
            if rel.get("TargetMode") == "External":
                continue
            path = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join(base, target))
            out.setdefault(rel.get("Type", "").rsplit("/", 1)[-1], path)
        return out

    def part(self, rel_type: str, default: str) -> str:
        return self.rels.get(rel_type, default)

    # -- styles and numbering
    def _load_styles(self):
        root = self.xml(self.part("styles", "word/styles.xml"))
        if root is None:
            return
        for s in root.findall("w:style", NS):
            sid = s.get(W("styleId"))
            ppr = s.find("w:pPr", NS)
            outline = ppr.find("w:outlineLvl", NS) if ppr is not None else None
            self.styles[sid] = {
                "name": (_val(s.find("w:name", NS)) or sid or ""),
                "based": _val(s.find("w:basedOn", NS)),
                "numpr": ppr.find("w:numPr", NS) if ppr is not None else None,
                "outline": int(_val(outline)) if outline is not None and _val(outline, "val") else None,
            }

    def _load_numbering(self):
        root = self.xml(self.part("numbering", "word/numbering.xml"))
        if root is None:
            return
        for an in root.findall("w:abstractNum", NS):
            lvls = {}
            for lvl in an.findall("w:lvl", NS):
                il = int(lvl.get(W("ilvl"), "0"))
                lvls[il] = (
                    _val(lvl.find("w:numFmt", NS)) or "decimal",
                    _val(lvl.find("w:lvlText", NS)) if lvl.find("w:lvlText", NS) is not None else "%%%d." % (il + 1),
                    int(_val(lvl.find("w:start", NS)) or 1),
                )
            self.absnums[an.get(W("abstractNumId"))] = lvls
        for n in root.findall("w:num", NS):
            overrides = {}
            for ov in n.findall("w:lvlOverride", NS):
                so = ov.find("w:startOverride", NS)
                if so is not None:
                    overrides[int(ov.get(W("ilvl"), "0"))] = int(_val(so) or 1)
            self.nums[n.get(W("numId"))] = (_val(n.find("w:abstractNumId", NS)), overrides)

    def _style_chain(self, sid):
        seen = 0
        while sid and sid in self.styles and seen < 12:
            yield sid, self.styles[sid]
            sid = self.styles[sid]["based"]
            seen += 1

    def heading_level(self, sid, ppr) -> int:
        if ppr is not None:
            ol = ppr.find("w:outlineLvl", NS)
            if ol is not None and (_val(ol) or "9").isdigit() and int(_val(ol)) < 9:
                return int(_val(ol)) + 1
        for _, st in self._style_chain(sid):
            name = st["name"].lower()
            m = re.match(r"heading\s*(\d)", name)
            if m:
                return int(m.group(1))
            if name == "title":
                return 1
            if st["outline"] is not None and st["outline"] < 9:
                return st["outline"] + 1
        if sid:
            m = re.match(r"(?i)heading(\d)$", sid)
            if m:
                return int(m.group(1))
        return 0

    def list_label(self, ppr, sid):
        numpr = ppr.find("w:numPr", NS) if ppr is not None else None
        style_numpr = None
        for _, st in self._style_chain(sid):
            if st["numpr"] is not None:
                style_numpr = st["numpr"]
                break
        if numpr is None and style_numpr is None:
            return None
        nid = _val(numpr.find("w:numId", NS)) if numpr is not None else None
        il = _val(numpr.find("w:ilvl", NS)) if numpr is not None else None
        if nid is None and style_numpr is not None:
            nid = _val(style_numpr.find("w:numId", NS))
        if il is None and style_numpr is not None:
            il = _val(style_numpr.find("w:ilvl", NS))
        if not nid or nid == "0" or nid not in self.nums:
            return None
        il = int(il or 0)
        aid, overrides = self.nums[nid]
        lvls = self.absnums.get(aid, {})

        def start_of(level):
            return overrides.get(level, lvls.get(level, ("decimal", "", 1))[2])

        key = ("num", nid) if overrides else ("abs", aid)
        cnt = self.counters.setdefault(key, [None] * 10)
        cnt[il] = start_of(il) if cnt[il] is None else cnt[il] + 1
        for deeper in range(il + 1, 10):
            cnt[deeper] = None
        fmt, text, _ = lvls.get(il, ("decimal", "%%%d." % (il + 1), 1))
        indent = "  " * il
        if fmt == "bullet":
            return indent + "- "
        if fmt == "none":
            return indent

        def repl(m):
            level = int(m.group(1)) - 1
            v = cnt[level] if cnt[level] is not None else start_of(level)
            return _fmt_num(v, lvls.get(level, ("decimal",))[0])

        return indent + re.sub(r"%([1-9])", repl, text or "") + " "

    # -- text
    def inline(self, el, symbol: bool = False) -> str:
        out = []
        for c in el:
            t = c.tag
            if t in SKIP_TAGS:
                continue
            if t in (W("t"), W("delText"), _q("m", "t")):
                s = c.text or ""
                out.append(_symbol_text(s) if symbol else s)
            elif t == W("r"):
                rfonts = c.find("w:rPr/w:rFonts", NS)
                is_symbol = rfonts is not None and "symbol" in (
                    (rfonts.get(W("ascii")) or "") + (rfonts.get(W("hAnsi")) or "")).lower()
                out.append(self.inline(c, is_symbol))
            elif t in (W("tab"), W("ptab")):
                out.append("\t")
            elif t in (W("br"), W("cr")):
                out.append("\n")
            elif t == W("noBreakHyphen"):
                out.append("-")
            elif t == W("sym"):
                code = int(c.get(W("char"), "3F"), 16)
                font = (c.get(W("font")) or "").lower()
                if code >= 0xF000:
                    code -= 0xF000
                out.append(SYMBOL_MAP.get(code, "?") if font == "symbol" else (chr(code) if code >= 0x20 else ""))
            elif t in (W("ins"), W("moveTo")):
                out.append(self._change(c, "+"))
            elif t in (W("del"), W("moveFrom")):
                out.append(self._change(c, "-"))
            elif t == W("commentRangeStart"):
                out.append("[[C%s>" % c.get(W("id")))
            elif t == W("commentRangeEnd"):
                out.append("<C%s]]" % c.get(W("id")))
            elif t == W("footnoteReference"):
                out.append("[^%s]" % c.get(W("id")))
            elif t == W("endnoteReference"):
                out.append("[^e%s]" % c.get(W("id")))
            elif t == W("txbxContent"):
                parts = [ln.strip() for ln in self.blocks(c) if ln.strip()]
                if parts:
                    out.append(" [text box: %s] " % " / ".join(parts))
            else:
                out.append(self.inline(c, symbol))
        return "".join(out)

    def _change(self, el, kind: str) -> str:
        author = el.get(W("author"), "?")
        if self.counting:
            rec = self.track.setdefault(author, [0, 0])
            rec[0 if kind == "+" else 1] += 1
        text = self.inline(el)
        if not text:
            return ""
        if self.changes == "accept":
            return text if kind == "+" else ""
        if self.changes == "reject":
            return "" if kind == "+" else text
        return "{%s[%s] %s%s}" % (kind, author, text, kind)

    def paragraph(self, p) -> str:
        ppr = p.find("w:pPr", NS)
        sid = _val(ppr.find("w:pStyle", NS)) if ppr is not None else None
        text = self.inline(p)
        label = self.list_label(ppr, sid)
        level = self.heading_level(sid, ppr)
        if level and text.strip():
            number = label.strip() if label and label.strip() not in ("-", "") else ""
            return "\n" + "#" * min(level, 6) + " " + (number + " " if number else "") + text.strip()
        if label is not None:
            return label + text
        return text

    def _children(self, el, tag):
        for c in el:
            if c.tag == tag:
                yield c
            elif c.tag in (W("sdt"), W("sdtContent"), W("customXml")):
                yield from self._children(c, tag)

    def table(self, tbl) -> list[str]:
        rows = []
        for tr in self._children(tbl, W("tr")):
            cells = []
            for tc in self._children(tr, W("tc")):
                parts = [ln.strip() for ln in self.blocks(tc) if ln.strip()]
                cells.append(" / ".join(parts).replace("\n", " ").replace("|", "¦"))
            rows.append("| " + " | ".join(cells) + " |")
        if self.max_rows and len(rows) > self.max_rows:
            extra = len(rows) - self.max_rows
            rows = rows[: self.max_rows] + ["| ... %d more rows (use --max-rows) |" % extra]
        return [""] + rows + [""]

    def blocks(self, container) -> list[str]:
        lines = []
        for c in container:
            t = c.tag
            if t == W("p"):
                lines.append(self.paragraph(c))
            elif t == W("tbl"):
                lines.extend(self.table(c))
            elif t == W("sdt"):
                content = c.find("w:sdtContent", NS)
                if content is not None:
                    lines.extend(self.blocks(content))
            elif t in (W("customXml"), W("sdtContent"), _q("mc", "AlternateContent"), _q("mc", "Choice")):
                lines.extend(self.blocks(c))
        return lines

    # -- comments and notes
    def comments(self, body_text: str) -> list[dict]:
        root = self.xml(self.part("comments", "word/comments.xml"))
        if root is None:
            return []
        ext = {}
        ext_root = self.xml(self.part("commentsExtended", "word/commentsExtended.xml"))
        if ext_root is not None:
            for ce in ext_root.iter(_q("w15", "commentEx")):
                ext[ce.get(_q("w15", "paraId"))] = (
                    ce.get(_q("w15", "done")) == "1", ce.get(_q("w15", "paraIdParent")))
        items, para_owner = [], {}
        for c in root.findall("w:comment", NS):
            cid = c.get(W("id"))
            paras = c.findall(".//w:p", NS)
            for p in paras:
                pid = p.get(_q("w14", "paraId"))
                if pid:
                    para_owner[pid] = cid
            text = "\n".join(self.inline(p) for p in paras).strip()
            last = paras[-1].get(_q("w14", "paraId")) if paras else None
            items.append({"id": cid, "author": c.get(W("author"), "?"), "date": c.get(W("date"), ""),
                          "text": text, "para": last})
        for it in items:
            done, parent = ext.get(it["para"], (False, None))
            it["resolved"] = done
            it["parent"] = para_owner.get(parent) if parent else None
            start = body_text.find("[[C%s>" % it["id"])
            end = body_text.find("<C%s]]" % it["id"])
            anchor = ""
            if start != -1 and end > start:
                anchor = body_text[start + len("[[C%s>" % it["id"]):end]
                anchor = re.sub(r"\[\[C\d+>|<C\d+\]\]", "", anchor)
                anchor = re.sub(r"\s+", " ", anchor).strip()
                if len(anchor) > 400:
                    anchor = anchor[:400] + " ..."
            it["anchor"] = anchor
        return items

    def notes(self, part: str, tag: str) -> list[tuple[str, str]]:
        root = self.xml(part)
        if root is None:
            return []
        out = []
        for fn in root.findall("w:%s" % tag, NS):
            if fn.get(W("type")) in ("separator", "continuationSeparator", "continuationNotice"):
                continue
            text = " ".join(self.inline(p) for p in fn.findall(".//w:p", NS)).strip()
            if text:
                out.append((fn.get(W("id")), text))
        return out

    def meta(self) -> dict:
        out = {}
        core = self.xml("docProps/core.xml")
        if core is not None:
            for key, tag in (("title", _q("dc", "title")), ("creator", _q("dc", "creator")),
                             ("lastModifiedBy", _q("cp", "lastModifiedBy")),
                             ("created", _q("dcterms", "created")), ("modified", _q("dcterms", "modified"))):
                el = core.find(tag)
                if el is not None and el.text:
                    out[key] = el.text
        app = self.xml("docProps/app.xml")
        if app is not None:
            for key in ("Application", "Company", "Pages", "Words"):
                el = app.find(_q("ep", key))
                if el is not None and el.text:
                    out[key] = el.text
        return out


def extract_docx(path: Path, rel: str, args, ctx) -> Result:
    d = DocxReader(path, changes=args.changes, max_rows=args.max_rows)
    doc = d.xml(d.doc_part)
    if doc is None:
        raise RuntimeError("no main document part found")
    body = doc.find("w:body", NS)
    d.counting = True
    text = "\n".join(d.blocks(body))
    d.counting = False
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    comments = d.comments(text)
    footnotes = d.notes(d.part("footnotes", "word/footnotes.xml"), "footnote")
    endnotes = d.notes(d.part("endnotes", "word/endnotes.xml"), "endnote")
    fmt_changes: dict[str, int] = {}
    for tag in ("rPrChange", "pPrChange"):
        for el in body.iter(W(tag)):
            a = el.get(W("author"), "?")
            fmt_changes[a] = fmt_changes.get(a, 0) + 1
    line_numbering = any(True for _ in body.iter(W("lnNumType")))
    media = sorted((n for n in d.names if n.startswith("word/media/")), key=natural_key)
    n_ins = sum(v[0] for v in d.track.values())
    n_del = sum(v[1] for v in d.track.values())
    words = count_words(text)

    out = ["=== FILE: %s" % rel,
           "=== TYPE: docx | words: %s | comments: %d | tracked changes: %d insertions, %d deletions%s" % (
               format(words, ","), len(comments), n_ins, n_del,
               "" if args.changes == "markup" else " (shown as: %s all)" % args.changes)]
    if args.meta:
        out.append("=== META: " + json.dumps(d.meta(), ensure_ascii=False))
    if line_numbering:
        out.append("=== NOTE: Word line numbering is on, but line numbers are not stored in the text. "
                   "Use the journal PDF for line anchors, or anchor by section and paragraph.")
    out += ["=== BODY:", text]
    if comments:
        out.append("\n=== COMMENTS (%d):" % len(comments))
        for c in comments:
            flags = (" [resolved]" if c["resolved"] else "") + (" [reply to C%s]" % c["parent"] if c["parent"] else "")
            out.append("--- C%s | %s | %s%s" % (c["id"], c["author"], c["date"], flags))
            out.append("    ANCHOR: %s" % (c["anchor"] or ("(same as parent)" if c["parent"] else "(none)")))
            out.append("    COMMENT: %s" % c["text"].replace("\n", "\n             "))
    if footnotes:
        out.append("\n=== FOOTNOTES (%d):" % len(footnotes))
        out += ["[^%s] %s" % (i, t) for i, t in footnotes]
    if endnotes:
        out.append("\n=== ENDNOTES (%d):" % len(endnotes))
        out += ["[^e%s] %s" % (i, t) for i, t in endnotes]
    if d.track:
        out.append("\n=== TRACKED CHANGES by author: " + "; ".join(
            "%s: %d ins, %d del" % (a, v[0], v[1]) for a, v in sorted(d.track.items())))
    if fmt_changes:
        out.append("=== FORMATTING CHANGES by author: " + "; ".join(
            "%s: %d" % (a, n) for a, n in sorted(fmt_changes.items())))
    extras = []
    if media:
        out.append("\n=== EMBEDDED MEDIA (%d): %s" % (len(media), ", ".join(posixpath.basename(m) for m in media)))
        if args.figures_to_png:
            fig_dir = ctx.work_dir() / "figures"
            with tempfile.TemporaryDirectory() as td:
                for m in media:
                    ext = posixpath.splitext(m)[1].lower()
                    if ext in (".emf", ".wmf", ".svg"):
                        out.append("    %s: not converted (%s)" % (posixpath.basename(m), ext[1:].upper()))
                        continue
                    src = Path(td) / posixpath.basename(m)
                    src.write_bytes(d.z.read(m))
                    dest = fig_dir / ("%s_%s.png" % (ctx.prefix, safe_name(Path(m).stem, 60)))
                    try:
                        for o in to_png(src, dest, args.max_px):
                            extras.append(str(o))
                    except Exception as e:  # noqa: BLE001
                        out.append("    %s: conversion failed (%s)" % (posixpath.basename(m), e))
    summary = "docx, %s words, %d comments, %d tracked changes%s" % (
        format(words, ","), len(comments), n_ins + n_del, ", %d media" % len(media) if media else "")
    return Result("\n".join(out) + "\n", summary, extras)


# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------

def _pdf_flags(fitz, kind: str) -> int:
    try:
        if kind == "dict":
            return fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_LIGATURES & ~fitz.TEXT_PRESERVE_IMAGES
        return fitz.TEXTFLAGS_TEXT & ~fitz.TEXT_PRESERVE_LIGATURES
    except AttributeError:
        return 0


def pdf_page_text(page, fitz) -> tuple[str, bool]:
    """Return the page text; keep visual lines (with line numbers) on line-numbered pages."""
    width = page.rect.width
    try:
        d = page.get_text("dict", flags=_pdf_flags(fitz, "dict"))
    except Exception:  # noqa: BLE001
        d = {"blocks": []}
    rows = []
    for b in d.get("blocks", []):
        if b.get("type", 0) != 0:
            continue
        for ln in b.get("lines", []):
            t = "".join(s.get("text", "") for s in ln.get("spans", [])).strip()
            if not t:
                continue
            x0, y0, x1, y1 = ln["bbox"]
            horizontal = abs(ln.get("dir", (1, 0))[0] - 1) < 1e-3
            rows.append(((y0 + y1) / 2, x0, max(1.0, y1 - y0), t, horizontal))
    margin_numbers = [r for r in rows if LINE_NUMBER_RE.match(r[3]) and r[1] < 0.2 * width]
    if len(margin_numbers) < 5:
        return page.get_text("text", flags=_pdf_flags(fitz, "text")), False
    horiz = sorted((r for r in rows if r[4]), key=lambda r: (r[0], r[1]))
    heights = sorted(r[2] for r in horiz)
    tol = max(2.0, 0.45 * heights[len(heights) // 2])
    lines: list[list] = []
    for r in horiz:
        if lines and abs(r[0] - lines[-1][0]) <= tol:
            lines[-1][1].append(r)
        else:
            lines.append([r[0], [r]])
    out = []
    for _, items in lines:
        items.sort(key=lambda r: r[1])
        first = items[0]
        if LINE_NUMBER_RE.match(first[3]) and first[1] < 0.2 * width and len(items) > 1:
            out.append(first[3] + "  " + " ".join(i[3] for i in items[1:]))
        else:
            out.append(" ".join(i[3] for i in items))
    rotated = [r[3] for r in rows if not r[4]]
    if rotated:
        out.append("[rotated text: %s]" % " / ".join(rotated))
    return "\n".join(out), True


def pdf_annotations(doc, fitz) -> list[dict]:
    items, by_xref = [], {}
    for pno, page in enumerate(doc, 1):
        words = None
        for a in page.annots() or []:
            typ = a.type[1]
            if typ in ("Link", "Popup", "Widget"):
                continue
            info = a.info or {}
            marked = ""
            if typ in ("Highlight", "Underline", "StrikeOut", "Squiggly"):
                if words is None:
                    words = page.get_text("words")
                rects = []
                v = a.vertices or []
                for k in range(0, len(v) - 3, 4):
                    try:
                        rects.append(fitz.Quad(v[k:k + 4]).rect + (-1, -1, 1, 1))
                    except Exception:  # noqa: BLE001
                        pass
                if not rects:
                    rects = [a.rect]
                sel = [w for w in words
                       if any(fitz.Point((w[0] + w[2]) / 2, (w[1] + w[3]) / 2) in r for r in rects)]
                marked = " ".join(w[4] for w in sel)
            item = {"page": pno, "type": typ, "author": info.get("title", ""),
                    "date": info.get("modDate") or info.get("creationDate") or "",
                    "content": (info.get("content") or "").strip(), "marked": marked,
                    "irt": getattr(a, "irt_xref", 0) or 0}
            items.append(item)
            by_xref[a.xref] = len(items)
    for it in items:
        it["reply_to"] = by_xref.get(it["irt"]) if it["irt"] else None
    return items


def extract_pdf(path: Path, rel: str, args, ctx) -> Result:
    fitz = import_fitz()
    if fitz is None:
        if shutil.which("pdftotext"):
            code, out, err = run_cmd(["pdftotext", "-layout", str(path), "-"])
            if code == 0:
                text = out.decode("utf-8", "replace")
                return Result("=== FILE: %s\n=== TYPE: pdf (pdftotext; install PyMuPDF for annotations)\n"
                              "=== BODY:\n%s" % (rel, text), "pdf via pdftotext")
        raise RuntimeError("PyMuPDF is not installed (pip install pymupdf)")
    doc = fitz.open(str(path))
    if doc.needs_pass and not doc.authenticate(""):
        return Result("=== FILE: %s\n=== TYPE: pdf (encrypted; cannot read)\n" % rel, "pdf, encrypted")
    body, numbered, image_pages, vector_pages = [], [], [], []
    for i, page in enumerate(doc, 1):
        text, has_numbers = pdf_page_text(page, fitz)
        if has_numbers:
            numbered.append(i)
        body.append("--- page %d ---\n%s" % (i, text.replace("\x00", "").rstrip()))
        area = max(1.0, page.rect.width * page.rect.height)
        try:
            infos = page.get_image_info()
        except Exception:  # noqa: BLE001
            infos = []
        big = 0.0
        for inf in infos:
            r = fitz.Rect(inf.get("bbox", (0, 0, 0, 0))) & page.rect
            if not r.is_empty:
                big = max(big, r.width * r.height / area)
        if big >= 0.15:
            image_pages.append(i)
        else:
            try:
                n_draw = len(page.get_cdrawings())
            except Exception:  # noqa: BLE001
                n_draw = 0
            if n_draw >= 500:
                vector_pages.append(i)
    annots = pdf_annotations(doc, fitz)
    figure_pages = sorted(set(image_pages) | set(vector_pages))

    header = ["=== FILE: %s" % rel,
              "=== TYPE: pdf | pages: %d | annotations: %d%s" % (
                  doc.page_count, len(annots),
                  " | line-numbered pages: %s" % fmt_ranges(numbered) if numbered else "")]
    if args.meta:
        header.append("=== META: " + json.dumps({k: v for k, v in (doc.metadata or {}).items() if v},
                                                 ensure_ascii=False))
    if figure_pages:
        header.append("=== FIGURE-LIKE PAGES: %s (view with --render-pages or --render-figure-pages)" %
                      fmt_ranges(figure_pages))
    out = header + ["=== BODY:"] + body
    if annots:
        out.append("\n=== ANNOTATIONS (%d):" % len(annots))
        for n, a in enumerate(annots, 1):
            parts = ["#%d p%d %s" % (n, a["page"], a["type"])]
            if a["author"]:
                parts.append(a["author"])
            if a["date"]:
                parts.append(a["date"])
            if a["reply_to"]:
                parts.append("reply to #%d" % a["reply_to"])
            line = " | ".join(parts)
            if a["marked"]:
                line += '\n    MARKED: "%s"' % a["marked"]
            if a["content"]:
                line += '\n    NOTE: "%s"' % a["content"].replace("\n", " ")
            out.append(line)

    extras = []
    pages_to_render = set()
    if args.render_pages:
        pages_to_render.update(parse_ranges(args.render_pages, doc.page_count))
    if args.render_figure_pages:
        pages_to_render.update(figure_pages)
    if pages_to_render:
        page_dir = ctx.work_dir() / "pages"
        page_dir.mkdir(parents=True, exist_ok=True)
        for p in sorted(pages_to_render):
            dest = page_dir / ("%s_p%03d.png" % (ctx.prefix, p))
            doc[p - 1].get_pixmap(dpi=args.dpi).save(str(dest))
            extras.append(str(dest))
        out.append("\n=== RENDERED PAGES: %s -> %s" % (fmt_ranges(pages_to_render), page_dir))

    summary = "pdf, %d pages%s, %d annotations%s" % (
        doc.page_count, " (line numbers on %s)" % fmt_ranges(numbered) if numbered else "", len(annots),
        ", figure-like pages %s" % fmt_ranges(figure_pages) if figure_pages else "")
    doc.close()
    return Result("\n".join(out) + "\n", summary, extras)


# ---------------------------------------------------------------------------
# Other formats
# ---------------------------------------------------------------------------

def extract_converted(path: Path, rel: str, args, ctx) -> Result:
    ext = path.suffix.lower()
    attempts = []
    if shutil.which("textutil") and ext in {".doc", ".rtf", ".odt", ".html", ".htm", ".webarchive", ".wordml"}:
        attempts.append(("textutil", ["textutil", "-convert", "txt", "-encoding", "UTF-8", "-stdout", str(path)]))
    if shutil.which("pandoc") and ext in {".rtf", ".odt", ".html", ".htm"}:
        attempts.append(("pandoc", ["pandoc", str(path), "-t", "plain", "--wrap=none"]))
    if ext == ".doc":
        if shutil.which("antiword"):
            attempts.append(("antiword", ["antiword", str(path)]))
        if shutil.which("catdoc"):
            attempts.append(("catdoc", ["catdoc", "-w", str(path)]))
    for name, cmd in attempts:
        code, out, _ = run_cmd(cmd)
        if code == 0 and out.strip():
            text = out.decode("utf-8", "replace")
            return Result("=== FILE: %s\n=== TYPE: %s (via %s) | words: %s\n=== BODY:\n%s\n" % (
                rel, ext[1:], name, format(count_words(text), ","), text), "%s via %s" % (ext[1:], name))
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice and Path("/Applications/LibreOffice.app/Contents/MacOS/soffice").exists():
        soffice = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    if soffice:
        target = "csv" if ext == ".xls" else "txt:Text"
        with tempfile.TemporaryDirectory() as td:
            code, _, _ = run_cmd([soffice, "--headless", "--convert-to", target, "--outdir", td, str(path)], 300)
            produced = sorted(Path(td).iterdir())
            if code == 0 and produced:
                text = produced[0].read_text("utf-8", "replace")
                return Result("=== FILE: %s\n=== TYPE: %s (via LibreOffice)\n=== BODY:\n%s\n" % (rel, ext[1:], text),
                              "%s via LibreOffice" % ext[1:])
    if ext in {".html", ".htm"}:
        raw = path.read_text("utf-8", "replace")
        raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
        text = re.sub(r"\s+\n", "\n", re.sub(r"<[^>]+>", " ", raw))
        return Result("=== FILE: %s\n=== TYPE: html (tags stripped)\n=== BODY:\n%s\n" % (rel, text), "html")
    raise RuntimeError("no converter for %s (install pandoc or LibreOffice, or save as .docx/.pdf)" % ext)


def extract_pptx(path: Path, rel: str, args, ctx) -> Result:
    z = zipfile.ZipFile(path)
    names = set(z.namelist())

    def rels(part):
        base = posixpath.dirname(part)
        name = posixpath.join(base, "_rels", posixpath.basename(part) + ".rels")
        out = {}
        if name in names:
            for r in ET.fromstring(z.read(name)).findall("rel:Relationship", NS):
                tgt = r.get("Target", "")
                out[r.get("Id")] = (r.get("Type", ""), tgt.lstrip("/") if tgt.startswith("/")
                                    else posixpath.normpath(posixpath.join(base, tgt)))
        return out

    slides = []
    if "ppt/presentation.xml" in names:
        pres_rels = rels("ppt/presentation.xml")
        pres = ET.fromstring(z.read("ppt/presentation.xml"))
        for sid in pres.iter(_q("p", "sldId")):
            rid = sid.get(_q("r", "id"))
            if rid in pres_rels:
                slides.append(pres_rels[rid][1])
    if not slides:
        slides = sorted((n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)), key=natural_key)

    def paras(xml_bytes):
        root = ET.fromstring(xml_bytes)
        out = []
        for p in root.iter(_q("a", "p")):
            t = "".join(x.text or "" for x in p.iter(_q("a", "t"))).strip()
            if t:
                out.append(t)
        return out

    out = ["=== FILE: %s" % rel, "=== TYPE: pptx | slides: %d" % len(slides), "=== BODY:"]
    for n, s in enumerate(slides, 1):
        if s not in names:
            continue
        out.append("--- slide %d ---" % n)
        out += paras(z.read(s))
        for typ, tgt in rels(s).values():
            if typ.endswith("/notesSlide") and tgt in names:
                notes = [t for t in paras(z.read(tgt)) if not t.isdigit()]
                if notes:
                    out.append("[notes] " + " / ".join(notes))
    return Result("\n".join(out) + "\n", "pptx, %d slides" % len(slides))


def _col_index(ref: str) -> int:
    m = re.match(r"([A-Z]+)", ref or "")
    if not m:
        return 0
    n = 0
    for ch in m.group(1):
        n = n * 26 + ord(ch) - 64
    return n - 1


def extract_xlsx(path: Path, rel: str, args, ctx) -> Result:
    out = ["=== FILE: %s" % rel]
    sheets_out = []
    try:
        import openpyxl  # noqa: F401
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
            for ws in wb.worksheets:
                rows, n = [], 0
                for row in ws.iter_rows(values_only=True):
                    vals = ["" if v is None else str(v) for v in row]
                    while vals and vals[-1] == "":
                        vals.pop()
                    if not vals:
                        continue
                    n += 1
                    if n > args.max_rows:
                        rows.append("... (truncated at %d rows; use --max-rows)" % args.max_rows)
                        break
                    rows.append(" | ".join(v.replace("\n", " ") for v in vals))
                sheets_out.append((ws.title, rows))
            wb.close()
    except ImportError:
        z = zipfile.ZipFile(path)
        names = set(z.namelist())
        shared = []
        if "xl/sharedStrings.xml" in names:
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("ss:si", NS):
                shared.append("".join(t.text or "" for t in si.iter(_q("ss", "t"))))
        wb_rels = {}
        if "xl/_rels/workbook.xml.rels" in names:
            for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels")).findall("rel:Relationship", NS):
                tgt = r.get("Target", "")
                wb_rels[r.get("Id")] = tgt.lstrip("/") if tgt.startswith("/") else posixpath.normpath(
                    posixpath.join("xl", tgt))
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        for s in wb.iter(_q("ss", "sheet")):
            part = wb_rels.get(s.get(_q("r", "id")))
            if not part or part not in names:
                continue
            rows, n = [], 0
            for row in ET.fromstring(z.read(part)).iter(_q("ss", "row")):
                cells = {}
                for c in row.findall("ss:c", NS):
                    t, v = c.get("t"), c.find("ss:v", NS)
                    if t == "s" and v is not None:
                        val = shared[int(v.text)]
                    elif t == "inlineStr":
                        val = "".join(x.text or "" for x in c.iter(_q("ss", "t")))
                    elif t == "b" and v is not None:
                        val = "TRUE" if v.text == "1" else "FALSE"
                    else:
                        val = v.text if v is not None and v.text else ""
                    cells[_col_index(c.get("r"))] = val
                if not any(cells.values()):
                    continue
                n += 1
                if n > args.max_rows:
                    rows.append("... (truncated at %d rows; use --max-rows)" % args.max_rows)
                    break
                width = max(cells) + 1
                rows.append(" | ".join(cells.get(i, "") for i in range(width)))
            sheets_out.append((s.get("name"), rows))
    out.append("=== TYPE: xlsx | sheets: %d" % len(sheets_out))
    out.append("=== BODY:")
    for name, rows in sheets_out:
        out.append("--- sheet: %s ---" % name)
        out += rows
    return Result("\n".join(out) + "\n", "xlsx, %d sheets" % len(sheets_out))


def extract_text(path: Path, rel: str, args, ctx, gz: bool = False) -> Result:
    opener = (lambda: gzip.open(path, "rt", encoding="utf-8", errors="replace")) if gz else (
        lambda: open(path, "r", encoding="utf-8", errors="replace"))
    suffixes = [s.lower() for s in path.suffixes]
    tabular = any(s in TABLE_TEXT_EXT for s in suffixes) or gz
    lines = []
    with opener() as fh:
        for n, line in enumerate(fh, 1):
            if tabular and n > args.max_rows:
                lines.append("... (truncated at %d lines; use --max-rows)\n" % args.max_rows)
                break
            lines.append(line)
    text = "".join(lines)
    if path.suffix.lower() == ".ipynb":
        try:
            nb = json.loads(text)
            cells = []
            for c in nb.get("cells", []):
                src = "".join(c.get("source", []))
                cells.append("[%s]\n%s" % (c.get("cell_type", "cell"), src))
            text = "\n\n".join(cells)
        except ValueError:
            pass
    kind = "gzip text" if gz else (path.suffix.lower()[1:] or "text")
    return Result("=== FILE: %s\n=== TYPE: %s\n=== BODY:\n%s\n" % (rel, kind, text), kind)


def _normalize_image(im):
    from PIL import Image
    if im.mode in ("I;16", "I;16B", "I;16L", "I", "F"):
        im = im.convert("I") if im.mode != "F" else im
        lo, hi = im.getextrema()
        scale = 255.0 / (hi - lo) if hi > lo else 1.0
        im = im.point(lambda v: v * scale - lo * scale).convert("L")
    elif im.mode == "CMYK":
        im = im.convert("RGB")
    elif im.mode in ("P", "PA"):
        im = im.convert("RGBA")
    elif im.mode == "1":
        im = im.convert("L")
    elif im.mode not in ("RGB", "RGBA", "L", "LA"):
        im = im.convert("RGB")
    if im.mode in ("RGBA", "LA"):
        background = Image.new("RGB", im.size, (255, 255, 255))
        background.paste(im.convert("RGBA"), mask=im.convert("RGBA").split()[-1])
        im = background
    return im


def to_png(src: Path, dest: Path, max_px: int) -> list[Path]:
    """Convert an image to PNG (every frame of a multi-page TIFF, up to 10), downscaled to max_px."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    errors = []
    try:
        from PIL import Image, ImageSequence
        Image.MAX_IMAGE_PIXELS = 400_000_000
        outs = []
        with Image.open(src) as im:
            for i, frame in enumerate(ImageSequence.Iterator(im)):
                if i >= 10:
                    break
                f = _normalize_image(frame.copy())
                f.thumbnail((max_px, max_px), Image.LANCZOS)
                target = dest if i == 0 else dest.with_name("%s_f%d.png" % (dest.stem, i + 1))
                f.save(target, "PNG", optimize=True)
                outs.append(target)
        if outs:
            return outs
    except Exception as e:  # noqa: BLE001
        errors.append("Pillow: %s" % e)
    fitz = import_fitz()
    if fitz is not None:
        try:
            pix = fitz.Pixmap(str(src))
            if pix.colorspace is None or pix.colorspace.n not in (1, 3) or pix.alpha:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            while max(pix.width, pix.height) > max_px:
                pix.shrink(1)
            pix.save(str(dest))
            return [dest]
        except Exception as e:  # noqa: BLE001
            errors.append("PyMuPDF: %s" % e)
    if shutil.which("sips"):
        code, _, err = run_cmd(["sips", "-s", "format", "png", "-Z", str(max_px), str(src), "--out", str(dest)])
        if code == 0 and dest.exists():
            return [dest]
        errors.append("sips: %s" % err.decode("utf-8", "replace").strip()[:200])
    raise RuntimeError("; ".join(errors) or "no image converter available")


def extract_image(path: Path, rel: str, args, ctx) -> Result:
    info = ""
    try:
        from PIL import Image
        Image.MAX_IMAGE_PIXELS = 400_000_000
        with Image.open(path) as im:
            frames = getattr(im, "n_frames", 1)
            info = "%dx%d px, mode %s%s" % (im.size[0], im.size[1], im.mode,
                                            ", %d frames" % frames if frames > 1 else "")
    except Exception:  # noqa: BLE001
        info = "%s bytes" % format(path.stat().st_size, ",")
    out = ["=== FILE: %s" % rel, "=== TYPE: image | %s" % info]
    extras = []
    if args.figures_to_png and path.suffix.lower() not in (".svg", ".emf", ".wmf", ".ai", ".eps"):
        dest = ctx.work_dir() / "figures" / ("%s_%s.png" % (ctx.prefix, safe_name(path.stem, 80)))
        try:
            extras = [str(p) for p in to_png(path, dest, args.max_px)]
            out.append("=== PNG: " + ", ".join(extras))
        except Exception as e:  # noqa: BLE001
            out.append("=== PNG: conversion failed (%s)" % e)
    elif args.figures_to_png:
        out.append("=== PNG: not converted (%s is a vector format; open it directly or export to PNG)" %
                   path.suffix.lower())
    return Result("\n".join(out) + "\n", "image, %s" % info, extras)


def list_archive(path: Path) -> list[tuple[str, int]]:
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as z:
            return [(i.filename, i.file_size) for i in z.infolist() if not i.is_dir()]
    with tarfile.open(path) as t:
        return [(m.name, m.size) for m in t.getmembers() if m.isfile()]


def unpack_archive(path: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    root = dest.resolve()
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as z:
            for info in z.infolist():
                target = (dest / info.filename).resolve()
                if info.is_dir() or not str(target).startswith(str(root) + os.sep):
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                with z.open(info) as src, open(target, "wb") as dst:
                    shutil.copyfileobj(src, dst)
    else:
        with tarfile.open(path) as t:
            try:
                t.extractall(dest, filter="data")
            except TypeError:  # Python < 3.12 without extraction filters
                safe = [m for m in t.getmembers() if m.isfile() and
                        str((dest / m.name).resolve()).startswith(str(root) + os.sep)]
                t.extractall(dest, members=safe)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

class Context:
    def __init__(self, outdir: Path | None):
        self.outdir = outdir
        self._tmp = None
        self.prefix = "00"

    def work_dir(self) -> Path:
        if self.outdir is not None:
            return self.outdir
        if self._tmp is None:
            self._tmp = Path(tempfile.mkdtemp(prefix="manuscript_extract_"))
            print("[note] no --outdir given; images and rendered pages go to %s" % self._tmp, file=sys.stderr)
        return self._tmp


def skip_file(name: str) -> bool:
    return (name in SKIP_NAMES or name.startswith(("~$", "._", ".~lock", ".")))


def collect(root: Path, exclude: set[Path]) -> list[Path]:
    if root.is_file():
        return [root]
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dp = Path(dirpath)
        dirnames[:] = sorted((d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")
                              and (dp / d).resolve() not in exclude), key=natural_key)
        files += [dp / f for f in sorted(filenames, key=natural_key) if not skip_file(f)]
    return files


def classify(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in DOCX_EXT:
        return "docx"
    if ext in PDF_EXT:
        return "pdf"
    if ext in PPTX_EXT:
        return "pptx"
    if ext in XLSX_EXT:
        return "xlsx"
    if ext in CONVERT_EXT:
        return "convert"
    if ext in IMAGE_EXT:
        return "image"
    if ext in TEXT_EXT or ext in TABLE_TEXT_EXT or ext == ".ipynb":
        return "text"
    if ext in ARCHIVE_EXT:
        if ext == ".gz" and not tarfile.is_tarfile(path):
            return "gztext"
        return "archive"
    return "other"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="manuscript folder or file")
    ap.add_argument("--outdir", help="write one text file per input here (plus figures/ and pages/)")
    ap.add_argument("--max-chars", type=int, default=None,
                    help="truncate each file's text (default: no limit with --outdir, 60000 on stdout)")
    ap.add_argument("--max-rows", type=int, default=200, help="rows per table, sheet or CSV (default 200)")
    ap.add_argument("--render-pages", help="PDF pages to render as PNG, e.g. '3,5-7' or 'all' (every PDF processed)")
    ap.add_argument("--render-figure-pages", action="store_true",
                    help="render PDF pages that look like figures (large images or dense vector graphics)")
    ap.add_argument("--dpi", type=int, default=110, help="resolution for rendered pages (default 110)")
    ap.add_argument("--figures-to-png", action="store_true",
                    help="convert image files and DOCX-embedded images to downscaled PNGs")
    ap.add_argument("--max-px", type=int, default=2000, help="longest side of converted PNGs (default 2000)")
    ap.add_argument("--changes", choices=["markup", "accept", "reject"], default="markup",
                    help="how to show DOCX tracked changes (default: markup)")
    ap.add_argument("--unzip", action="store_true", help="extract ZIP/TAR archives and process their contents")
    ap.add_argument("--meta", action="store_true",
                    help="print document metadata such as author names (off by default for double-blind review)")
    args = ap.parse_args(argv)

    root = Path(args.path).expanduser()
    if not root.exists():
        print("error: %s does not exist" % root, file=sys.stderr)
        return 1
    outdir = Path(args.outdir).expanduser() if args.outdir else None
    if outdir:
        outdir.mkdir(parents=True, exist_ok=True)
    ctx = Context(outdir)
    exclude = {outdir.resolve()} if outdir else set()
    base = root if root.is_dir() else root.parent
    queue = [(p, str(p.relative_to(base))) for p in collect(root, exclude)]
    width = 3 if len(queue) > 99 else 2
    max_chars = args.max_chars if (args.max_chars or outdir) else 60000
    manifest, ok, failed, index = [], 0, 0, 0

    while queue:
        path, rel = queue.pop(0)
        index += 1
        ctx.prefix = str(index).zfill(width)
        kind = classify(path)
        try:
            if kind == "docx":
                res = extract_docx(path, rel, args, ctx)
            elif kind == "pdf":
                res = extract_pdf(path, rel, args, ctx)
            elif kind == "pptx":
                res = extract_pptx(path, rel, args, ctx)
            elif kind == "xlsx":
                res = extract_xlsx(path, rel, args, ctx)
            elif kind == "convert":
                res = extract_converted(path, rel, args, ctx)
            elif kind == "image":
                res = extract_image(path, rel, args, ctx)
            elif kind in ("text", "gztext"):
                res = extract_text(path, rel, args, ctx, gz=(kind == "gztext"))
            elif kind == "archive":
                members = list_archive(path)
                lines = ["=== FILE: %s" % rel, "=== TYPE: archive | files: %d" % len(members)]
                lines += ["  %s (%s bytes)" % (n, format(s, ",")) for n, s in members[:500]]
                if args.unzip:
                    dest = ctx.work_dir() / "unzipped" / ("%s_%s" % (ctx.prefix, safe_name(path.stem, 60)))
                    unpack_archive(path, dest)
                    new = collect(dest, set())
                    queue = [(p, "%s!/%s" % (rel, p.relative_to(dest))) for p in new] + queue
                    lines.append("=== UNPACKED to %s (%d files queued)" % (dest, len(new)))
                else:
                    lines.append("=== NOTE: use --unzip to extract and process these files")
                res = Result("\n".join(lines) + "\n", "archive, %d files" % len(members))
            else:
                res = Result("=== FILE: %s\n=== TYPE: unsupported (%s, %s bytes)\n" % (
                    rel, path.suffix or "no extension", format(path.stat().st_size, ",")),
                    "unsupported %s" % (path.suffix or "file"))
            ok += 1
        except Exception as e:  # noqa: BLE001
            failed += 1
            res = Result("=== FILE: %s\n=== ERROR: %s: %s\n" % (rel, type(e).__name__, e),
                         "ERROR %s: %s" % (type(e).__name__, e))

        text = truncate(res.text, max_chars)
        if outdir:
            target = outdir / ("%s_%s.txt" % (ctx.prefix, safe_name(rel)))
            target.write_text(text, encoding="utf-8")
            where = " -> %s" % target.name
        else:
            sys.stdout.write(text + "\n")
            where = ""
        entry = "[%s] %s | %s%s" % (ctx.prefix, rel, res.summary, where)
        if res.extras:
            entry += "\n      images: %d file(s) in %s" % (len(res.extras), Path(res.extras[0]).parent)
        manifest.append(entry)

    header = "=== MANIFEST: %d file(s) from %s%s" % (index, root, " -> %s" % outdir if outdir else "")
    summary = "\n".join([header] + manifest) + "\n"
    if outdir:
        (outdir / "MANIFEST.txt").write_text(summary, encoding="utf-8")
    sys.stdout.write(summary)
    return 0 if ok or not index else 2


if __name__ == "__main__":
    sys.exit(main())
