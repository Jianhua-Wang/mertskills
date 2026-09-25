#!/usr/bin/env python3
"""Local diagnostics for English scientific prose.

Flags rhythm and wording patterns that make manuscript text read as
machine-written: uniform sentence lengths, repeated openers, connector-heavy
sentence starts, stock AI vocabulary, em dashes, trailing -ing clauses,
stacked hedges, overclaims, and "significant" without a statistical test.
A separate Language block reports usage errors common in drafts and in
Chinese-L1 English, mixed US/UK or -ize/-ise spelling, and abbreviations used
before their definition, defined twice, or rarely used.

The numbers are diagnostic proxies for revision, not an AI-detector score.
Thresholds are heuristics; judge every flag in context.

Usage:
  prose_check.py FILE            .txt .md .tex .docx .pdf (PDF needs pdftotext; its
                                 paragraph breaks are guessed, so prefer .tex or .docx)
  prose_check.py BEFORE AFTER    compare two versions side by side
  prose_check.py -               read plain text from stdin
Options:
  --max N    flagged sentences to list (default 15; 0 lists all)
  --json     machine-readable output

Standard library only. Nothing leaves the machine.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import statistics
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from pathlib import Path

# Heuristic thresholds (not calibrated against any detector).
SHORT_WORDS = 12            # sentences shorter than this count as short
LONG_WORDS = 30             # sentences longer than this count as long
VERY_LONG_WORDS = 40        # flagged one by one
UNIFORM_BAND = (15, 30)     # a paragraph whose sentences all fall here reads flat
LOW_CV = 0.35               # coefficient of variation of sentence length
HIGH_OPENER_SHARE = 0.25    # one first word starting this share of sentences
HIGH_CONNECTOR_SHARE = 0.30
HIGH_TELL_RATE = 5.0        # AI-vocabulary hits per 1000 words

HEADING = "\x00H"           # marks heading blocks produced during extraction


def _rx(pattern: str, flags: int = re.IGNORECASE) -> re.Pattern:
    return re.compile(pattern, flags)


# ------------------------------------------------------------------ patterns

AI_VOCAB = _rx(
    r"\b(?:delv(?:e|es|ed|ing)|intricate(?:ly)?|intricac(?:y|ies)|pivotal|crucial(?:ly)?|"
    r"vital(?:ly)?|paramount|underscor(?:e|es|ed|ing)|showcas(?:e|es|ed|ing)|"
    r"(?<!high )leverag(?:e|es|ed|ing)(?!\s+(?:scores?|points?|values?|statistics?|plots?))|"
    r"harness(?:es|ed|ing)?|utili[sz](?:e|es|ed|ing|ation)|facilitat(?:e|es|ed|ing)|"
    r"bolster(?:s|ed|ing)?|foster(?:s|ed|ing)?|unlock(?:s|ed|ing)?|unveil(?:s|ed|ing)?|"
    r"elucidat(?:e|es|ed|ing)|realms?|tapestry|interplay|multi-?faceted|nuanced|"
    r"holistic(?:ally)?|seamless(?:ly)?|meticulous(?:ly)?|noteworthy|landscapes?|"
    r"groundbreaking|cutting-edge|game-?changer|synerg(?:y|ies|istic))\b"
)

STOCK = _rx(
    r"\b(?:in recent years|(?:in|over) the (?:past|last) (?:few |two |several )?(?:decades?|years)|"
    r"with the (?:rapid |recent |continuous )?(?:development|advancement|advances?|advent|emergence|"
    r"growth|proliferation) of|in the (?:era|age) of|in today's|ha(?:s|ve) emerged as|"
    r"ha(?:s|ve) (?:garnered|attracted|received|gained) (?:(?:significant|considerable|increasing|"
    r"growing|widespread|much|great|extensive) )?(?:attention|interest)|more and more|"
    r"play(?:s|ed|ing)? (?:an? )?(?:\w+ )?(?:crucial|pivotal|vital|key|critical|important|central|"
    r"essential|significant|major|fundamental) roles?|"
    r"it is (?:worth|important|interesting|noteworthy) (?:to )?not(?:e|ing)|it should be noted|"
    r"a testament to|in the realm of|pav(?:e|es|ed|ing) the way|sh(?:ed|eds|edding) (?:new )?light on|"
    r"opens? (?:up )?new avenues|a deeper understanding of|remains? elusive|gaining traction)\b"
)

ING_TAIL = _rx(
    r",\s+(?:thereby\s+|thus\s+)?(?:highlighting|underscoring|emphasi[sz]ing|showcasing|paving|"
    r"reinforcing|demonstrating|illustrating|reflecting|revealing|offering|providing|ensuring|"
    r"enabling|facilitating|contributing|marking|signal+ing|cementing|solidifying)\b"
)

NEG_PARALLEL = _rx(
    r"\bnot only\b|\bnot (?:just|merely|simply)\b|\brather than (?:merely|simply|just)\b|"
    r"\bit is not\b[^.;]{0,60}\bbut\b|\bno longer just\b"
)

COPULA = _rx(r"\b(?:serv(?:e|es|ed|ing)|stand(?:s|ing)?|stood) as (?:an?|the)\b")

VAGUE = _rx(
    r"\b(?:a (?:wide|broad|diverse|vast) (?:range|array|spectrum|variety) of|"
    r"a (?:plethora|myriad|multitude|host) of|myriad|various|numerous|a number of)\b"
)

INTENSIFIER = _rx(
    r"\b(?:remarkabl[ey]|strikingly|profoundly|truly|undeniably|incredibly|exceptionally|"
    r"tremendous(?:ly)?|immense(?:ly)?|unparalleled|invaluable|indispensable|"
    r"powerful (?:tool|approach|framework|method|technique|strategy|resource)s?)\b"
)

SPOTLIGHT_START = _rx(
    r"^(?:Notably|Importantly|Interestingly|Remarkably|Strikingly|Crucially|Critically|"
    r"Intriguingly|Surprisingly|Significantly)\b",
    0,
)

FILLER = _rx(
    r"\b(?:in order to|(?:due|owing) to the fact that|the fact that|in light of the fact that|"
    r"it is (?:clear|evident|obvious) that|it can be (?:seen|observed|concluded) that|as can be seen|"
    r"needless to say|prior to|subsequent to|in an effort to|for the purpose of)\b"
)

PARAPHRASE = _rx(
    r"\b(?:in other words|that is to say|put (?:differently|simply|another way)|simply put|"
    r"to put it simply)\b|^That is,"
)

SUMMARY_MORAL = _rx(
    r"\b(?:taken together|collectively|in summary|in conclusion|to summari[sz]e|overall),? "
    r"(?:these|our|this|the) (?:results|findings|data|observations|analyses|work|study)\b|"
    r"\bthese (?:results|findings|data|observations) (?:collectively |together )?"
    r"(?:highlight|underscore|emphasi[sz]e|showcase|illustrate|reinforce|reveal)\b"
)

OVERCLAIM = _rx(
    r"\b(?:prov(?:e|es|ed|en|ing)|conclusive(?:ly)?|unprecedented|groundbreaking|"
    r"paradigm[- ]shift\w*|revolutioni[sz]\w*|for the first time|the first (?:study|method|tool|"
    r"approach|framework|report|work|attempt|comprehensive)|superior|definitive(?:ly)?|"
    r"unequivocal(?:ly)?|undoubtedly|clearly (?:shows?|showed|demonstrat(?:e|es|ed))|"
    r"novel(?! (?:loc(?:i|us)|variants?|signals?|associations?|isoforms?|transcripts?|genes?))|"
    r"comprehensive(?:ly)?)\b"
)

CHAT = _rx(
    r"\bcertainly!|\bas an ai\b|\bas a language model\b|\bi hope this helps\b|\blet me know if\b|"
    r"\bhere is (?:a|the|your) (?:revised|rewritten|polished|improved|updated)\b|\bfeel free to\b|"
    r"\bhappy to help\b|\bgreat question\b"
)

SIGNIFICANT = _rx(r"\bsignifican(?:t|tly|ce)\b")
STAT_MARKER = _rx(
    r"\bP\s*[<=≤>≥]|\bP[- ]?values?\b|\bFDR\b|\bq[- ]?values?\b|\bq\s*[<=≤]|\bα\b|\balpha\b|"
    r"\btest(?:s|ed|ing)?\b|Wilcoxon|Mann[–-]Whitney|χ2|χ²|chi-?squared?|ANOVA|Fisher|Bonferroni|"
    r"Benjamini|permutation|\bOR\s*=|\bHR\s*=|\bCI\b|confidence interval|adjusted|"
    r"(?:genome|study|exome|transcriptome)-wide significan|statistical(?:ly)?|\bz\s*=|\bt\s*=|"
    r"\bF\s*=|×\s*10|\de-\d|10\^?[-−]\d|nominal(?:ly)?|threshold"
)

HEDGE = _rx(
    r"\b(?:may|might|could|possibly|potentially|perhaps|presumably|plausibly|conceivably|likely|"
    r"probably|suggests?|suggested|suggesting|appears? to|appeared to|seems? to|seemed to|"
    r"putative(?:ly)?|to some extent|somewhat)\b"
)
HEDGE_PAIR = _rx(
    r"\b(?:may|might|could)\s+(?:possibly|potentially|perhaps|presumably|conceivably|likely)\b|"
    r"\b(?:possibly|potentially|perhaps)\s+(?:suggest|indicate|may|might|could)\w*|"
    r"\b(?:may|might|could)\s+(?:suggest|indicate)\w*"
)

CONNECTOR_START = _rx(
    r"^(?:However|Furthermore|Moreover|Additionally|In addition|Notably|Importantly|Interestingly|"
    r"Consequently|Therefore|Thus|Hence|Overall|Collectively|Taken together|Together|In contrast|"
    r"By contrast|Conversely|Similarly|Likewise|Specifically|Finally|Indeed|Nevertheless|"
    r"Nonetheless|Meanwhile|Subsequently|Accordingly|Crucially|Critically|Remarkably|Strikingly|"
    r"Surprisingly|Ultimately|In particular|In summary|In conclusion|As a result|To this end|"
    r"Beyond|First(?:ly)?|Second(?:ly)?|Third(?:ly)?|Lastly|Next|Also|Besides|Instead|"
    r"Alternatively|Altogether)\b",
    0,
)

EM_DASH = re.compile(r"[\u2014\u2015]|(?<=\w) ?-- ?(?=\w)")

# (label, pattern) pairs counted per sentence; order sets the report order.
CATEGORIES = [
    ("AI vocabulary", AI_VOCAB),
    ("stock phrases", STOCK),
    ("-ing tails", ING_TAIL),
    ("not-only/not-just", NEG_PARALLEL),
    ("serves/stands as", COPULA),
    ("vague quantifiers", VAGUE),
    ("intensifiers", INTENSIFIER),
    ("fillers", FILLER),
    ("paraphrase repeats", PARAPHRASE),
    ("summary morals", SUMMARY_MORAL),
    ("overclaim words", OVERCLAIM),
    ("chat residue", CHAT),
]

# ------------------------------------------------------------------ language
# Usage errors and conventions (references/language.md). Reported apart from AI tells.

USAGE = [   # (label, pattern, advice)
    ("uncountable plural",
     _rx(r"\b(?:evidences|softwares|informations|researches|knowledges|feedbacks|equipments|"
         r"datas|metadatas|advices)\b"),
     "no plural: lines of evidence, software packages, studies"),
    ("data + singular verb",
     _rx(r"\bdata (?:is|was|has|shows|showed|suggests|indicates|reveals)\b"),
     "'data' is plural in most journals"),
    ("compared to", _rx(r"\bcompared to\b"), "'compared with' for measured differences"),
    ("different than/to", _rx(r"\bdifferent (?:than|to)\b"), "'different from'"),
    ("comprised of", _rx(r"\b(?:is|are|was|were|be|been|being) comprised of\b"),
     "'comprises' or 'consists of'"),
    ("paired connector",
     _rx(r"\b(?:although|though)\b[^.;:]{0,150},\s*but\b|\bbecause\b[^.;:]{0,150},\s*so\b|"
         r"\bdespite of\b|\breason (?:\w+ )?is because\b"),
     "one connector only: drop 'but' or 'so'; 'despite'; 'the reason is that'"),
    ("etc. after such as", _rx(r"\bsuch as\b[^.;]{0,150}\betc\b|\band so on\b"),
     "'such as' already implies more items"),
    ("Chinese-English set phrase",
     _rx(r"\b(?:as we all know|it is well[- ]known that|what'?s more|last but not least|in a word|"
         r"nowadays|a lot of|lots of|up to now|discuss(?:es|ed|ing)? about|"
         r"emphasi[sz](?:e|es|ed|ing) on|in this paper)\b|^(?:among them|especially|at last)\b"),
     "see language.md section 4"),
    ("numeral starts sentence", re.compile(r"^\d[\d,.]*%?(?=\s)"), "spell the number out or rephrase"),
    ("E-notation", re.compile(r"(?<![\w.])\d+(?:\.\d+)?[eE][-−+]?\d+\b"),
     "write 3.2 × 10^-8 in text"),
    ("P = 0", re.compile(r"\b[Pp](?:[- ]values?)?\s*=\s*0(?:\.0+)?(?!\.?\d)"),
     "report P < 0.001 or the exact value"),
    ("no space before unit",
     re.compile(r"(?<![\w.])\d+(?:\.\d+)?(?:bp|kb|Mb|Gb|kDa|GB|MB|TB|ms|min|mg|ml|mL|"
                r"[µμ][lLgM]|ng|nM|mM)\b"),
     "space between number and unit: 10 kb"),
    ("et al without full stop", re.compile(r"\bet al\b(?!\.)"), "'et al.'"),
]

# -ize/-ise is its own axis: Oxford spelling pairs -ize with other British forms.
IZE_STEMS = (r"real|recogn|organ|normal|standard|optim|character|util|summar|visual|priorit|"
             r"minim|maxim|general|local|random|stabil|neutral|harmon|parameter|categor|emphas|"
             r"hypothes|synthes|special|final|initial|critic|mobil|polar|regular|token|binar|"
             r"discret|linear|homogen|marginal|central|quant|vector|memor|immun|author|global|"
             r"personal|contextual|conceptual|individual|symbol|capital|operational")
IZE_RE = _rx(rf"\b(?:{IZE_STEMS})i([sz])(?:e|es|ed|ing|ation|ations|er|ers)\b")
SPELLING_PAIRS = [   # (US, UK)
    (r"analy(?:ze|zed|zing|zer|zers|zes)", r"analy(?:se|sed|sing|ser|sers)"),
    (r"model(?:ing|ed|er|ers)", r"modell(?:ing|ed|er|ers)"),
    (r"label(?:ed|ing)", r"labell(?:ed|ing)"),
    (r"signal(?:ed|ing)", r"signall(?:ed|ing)"),
    (r"color(?:s|ed|ing|ation)?", r"colour(?:s|ed|ing|ation)?"),
    (r"behavior(?:s|al|ally)?", r"behaviour(?:s|al|ally)?"),
    (r"favor(?:s|ed|ing|able|ably|ite|ites)?", r"favour(?:s|ed|ing|able|ably|ite|ites)?"),
    (r"tumor(?:s|al)?", r"tumour(?:s|al)?"),
    (r"neighbor(?:s|ing|hood|hoods)?", r"neighbour(?:s|ing|hood|hoods)?"),
    (r"harbor(?:s|ed|ing)?", r"harbour(?:s|ed|ing)?"),
    (r"cent(?:er|ers|ered|ering)", r"cent(?:re|res|red|ring)"),
    (r"fib(?:er|ers)", r"fib(?:re|res)"),
    (r"hem(?:at|og|ol|orr)\w*", r"haem(?:at|og|ol|orr)\w*"),
    (r"fet(?:al|us|uses)", r"foet(?:al|us|uses)"),
    (r"esophag\w*", r"oesophag\w*"),
    (r"estrog\w*", r"oestrog\w*"),
    (r"anemi\w*", r"anaemi\w*"),
    (r"leukemi\w*", r"leukaemi\w*"),
    (r"pediatr\w*", r"paediatr\w*"),
    (r"aging", r"ageing"),
    (r"artifacts?", r"artefacts?"),
    (r"enrollments?", r"enrolments?"),
]
US_RE = _rx(r"\b(?:%s)\b" % "|".join(us for us, _ in SPELLING_PAIRS))
UK_RE = _rx(r"\b(?:%s)\b" % "|".join(uk for _, uk in SPELLING_PAIRS))

# "(GWAS)", "(PCs)", "(eQTLs)", "(scRNA-seq)": a parenthesised token with two or more capitals.
ABBR_DEF_RE = re.compile(r"\((?=[A-Za-z0-9\-]*[A-Z][A-Za-z0-9\-]*[A-Z])([A-Za-z][A-Za-z0-9\-]{1,14})\)")

# ---------------------------------------------------------------- extraction

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def read_input(path: str) -> tuple[str, str]:
    """Return (kind, raw_text); kind is txt, md, tex, docx, or pdf."""
    if path == "-":
        return "txt", sys.stdin.read()
    p = Path(path)
    if not p.exists():
        sys.exit(f"{path}: file not found")
    ext = p.suffix.lower()
    if ext == ".docx":
        return "docx", _docx_text(p)
    if ext == ".pdf":
        return "pdf", _pdf_text(p)
    if ext == ".doc":
        sys.exit(f"{path}: legacy .doc; convert first (macOS: textutil -convert docx '{path}')")
    text = p.read_text(encoding="utf-8", errors="replace")
    if ext in (".tex", ".ltx"):
        return "tex", text
    if ext in (".md", ".markdown", ".rmd", ".qmd"):
        return "md", text
    return "txt", text


def _docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
    blocks = []
    for para in root.iter(W + "p"):
        parts = []
        for node in para.iter():
            if node.tag == W + "t" and node.text:
                parts.append(node.text)
            elif node.tag in (W + "tab", W + "br", W + "cr"):
                parts.append(" ")
        text = "".join(parts).strip()
        if not text:
            continue
        style = para.find(f"{W}pPr/{W}pStyle")
        style_name = (style.get(W + "val") if style is not None else "") or ""
        if style_name.lower().startswith(("heading", "title", "subtitle")):
            text = HEADING + text
        blocks.append(text)
    return "\n\n".join(blocks)


def _pdf_text(path: Path) -> str:
    exe = shutil.which("pdftotext")
    if not exe:
        sys.exit(f"{path}: PDF input needs pdftotext (poppler); or convert to .txt first")
    res = subprocess.run([exe, "-enc", "UTF-8", str(path), "-"],
                         capture_output=True, text=True, check=False)
    if res.returncode != 0:
        sys.exit(f"{path}: pdftotext failed: {res.stderr.strip()}")
    text = res.stdout.replace("\f", "\n\n")
    text = re.sub(r"(?m)^[ \t]*\d{1,4}[ \t]*\n", "", text)   # page and line numbers
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)              # end-of-line hyphenation
    # pdftotext rarely keeps blank lines between paragraphs. A line that ends a sentence
    # and stops well short of the usual line width is taken as a paragraph end.
    lines = text.split("\n")
    widths = sorted(len(ln) for ln in lines if len(ln.strip()) > 20)
    if len(widths) >= 5:
        full = widths[int(0.75 * (len(widths) - 1))]
        lines = [ln + "\n" if ln.rstrip().endswith((".", "!", "?", ":"))
                 and len(ln) < 0.8 * full else ln for ln in lines]
    return "\n".join(lines)


def _md_clean(text: str) -> str:
    text = re.sub(r"(?ms)^(```|~~~).*?^\1[^\n]*$", " ", text)            # fenced code
    text = re.sub(r"(?s)<!--.*?-->", " ", text)                             # comments
    text = re.sub(r"(?m)^\s*\|.*$", "", text)                               # tables
    text = re.sub(r"(?m)^#{1,6}\s+(.*?)\s*#*\s*$",
                  lambda m: "\n\n" + HEADING + m.group(1) + "\n\n", text)  # headings
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)                       # images
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)                    # links
    text = re.sub(r"\[-?@[^\]]+\]", "", text)                               # pandoc citations
    text = re.sub(r"\[\^[^\]]+\]", "", text)                                # footnote refs
    text = re.sub(r"`[^`\n]+`", "X", text)                                  # inline code
    text = re.sub(r"(?m)^[ \t]*(?:[-*+]|\d+[.)])[ \t]+", "\n\n", text)      # list items
    text = re.sub(r"(?m)^[ \t]*>[ \t]?", "", text)                          # block quotes
    text = re.sub(r"(\*\*|__)(?=\S)(.+?)(?<=\S)\1", r"\2", text)            # bold
    return re.sub(r"(?<![\w*])([*_])(?=\S)(.+?)(?<=\S)\1(?![\w*])", r"\2", text)  # italics


TEX_DROP_ENVS = ("equation", "align", "gather", "multline", "eqnarray", "displaymath", "math",
                 "verbatim", "lstlisting", "minted", "tikzpicture", "tabular", "tabularx",
                 "longtable", "algorithmic", "thebibliography", "comment")
TEX_DROP_CMDS = {
    "cite", "citep", "citealp", "citealt", "parencite", "autocite", "footcite", "supercite",
    "nocite", "label", "includegraphics", "bibliography", "bibliographystyle", "footnote",
    "footnotetext", "url", "input", "include", "vspace", "hspace", "vskip", "hskip",
    "setlength", "addtolength", "author", "affil", "affiliation", "address", "email", "date",
    "thanks", "keywords", "orcid", "newcommand", "renewcommand", "providecommand",
    "usepackage", "documentclass", "graphicspath",
}
TEX_REF_CMDS = {"ref", "eqref", "autoref", "cref", "Cref", "pageref", "nameref", "subref"}
TEX_TEXTCITE = {"citet", "Citet", "textcite", "Textcite", "citeauthor"}
TEX_HEADINGS = {"section", "subsection", "subsubsection", "paragraph", "subparagraph",
                "chapter", "part", "title"}
TEX_BLOCK_KEEP = {"caption", "abstract"}
_CMD_RE = re.compile(r"\\([A-Za-z@]+\*?|[^A-Za-z@])")


def _tex_group(s: str, i: int, open_ch: str, close_ch: str) -> tuple[str, int]:
    """s[i] is open_ch; return (inner text, index after the matching close)."""
    depth, j = 0, i
    while j < len(s):
        ch = s[j]
        if ch == "\\":
            j += 2
            continue
        if ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    return s[i + 1:], len(s)


def _tex_command(s: str, i: int) -> tuple[str, list[str], int]:
    m = _CMD_RE.match(s, i)
    if not m:
        return "", [], i + 1
    name, j = m.group(1), m.end()
    args: list[str] = []
    if name[0].isalpha() or name[0] == "@":
        while j < len(s) and s[j] == "[" and not args:     # optional args
            _, j = _tex_group(s, j, "[", "]")
        while True:
            k = j
            while k < len(s) and s[k] in " \t":
                k += 1
            if k >= len(s) or s[k] != "{":
                break
            content, j = _tex_group(s, k, "{", "}")
            args.append(content)
            while name == "begin" and j < len(s) and s[j] == "[":   # \begin{figure}[t]
                _, j = _tex_group(s, j, "[", "]")
    return name, args, j


_MATH_STAT = re.compile(r"(?<![A-Za-z\\])(P|p|q|z|t|F|FDR|OR|HR|\\chi\^?\{?2?\}?|\\alpha)\s*"
                        r"(?:=|<|>|\\le(?:q)?\b|\\ge(?:q)?\b|\\ll\b|\\approx\b)")


def _math_token(content: str) -> str:
    """Inline math becomes 'X', but keep statistics visible (e.g. 'P = X') for the test check."""
    if content.strip() in ("P", "p"):                      # $P$-value
        return "P"
    m = _MATH_STAT.search(content)
    if not m:
        return "X"
    name = m.group(1)
    name = "chi-square" if "chi" in name else "alpha" if "alpha" in name else name
    return f"{name} = X"


def _tex_to_text(s: str) -> str:
    out: list[str] = []
    i, n = 0, len(s)
    while i < n:
        ch = s[i]
        if ch == "\\":
            name, args, j = _tex_command(s, i)
            base = name.rstrip("*")
            last = args[-1] if args else ""
            if name == "(":
                end = s.find("\\)", j)
                out.append(_math_token(s[j:] if end < 0 else s[j:end]))
                j = n if end < 0 else end + 2
            elif name == "[":
                end = s.find("\\]", j)
                out.append(" ")
                j = n if end < 0 else end + 2
            elif name == "\\":
                if j < n and s[j] == "[":
                    _, j = _tex_group(s, j, "[", "]")
                out.append(" ")
            elif name in "%&_#${}":
                out.append(name)
            elif name in ",;: \n\t":
                out.append(" ")
            elif base in TEX_HEADINGS:
                out.append("\n\n" + HEADING + _tex_to_text(last).strip() + "\n\n")
            elif base in TEX_BLOCK_KEEP:
                out.append("\n\n" + _tex_to_text(last) + "\n\n")
            elif base in TEX_REF_CMDS:
                out.append("1")
            elif base in TEX_TEXTCITE:
                out.append("Smith")
            elif base in ("item", "begin", "end", "par"):
                out.append("\n\n")
            elif base in TEX_DROP_CMDS:
                pass
            elif args:
                out.append(_tex_to_text(last))
            i = j                       # other commands, accents included, are dropped
        elif ch == "$":
            if s.startswith("$$", i):
                end = s.find("$$", i + 2)
                out.append(" ")
                i = n if end < 0 else end + 2
            else:
                end = i + 1
                while True:
                    end = s.find("$", end)
                    if end < 0 or s[end - 1] != "\\":
                        break
                    end += 1
                out.append(_math_token(s[i + 1:] if end < 0 else s[i + 1:end]))
                i = n if end < 0 else end + 1
        elif ch in "{}":
            i += 1
        elif ch == "~":
            out.append(" ")
            i += 1
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def _tex_clean(src: str) -> str:
    src = re.sub(r"(?<!\\)%.*", "", src)                                     # comments
    body = re.search(r"\\begin\{document\}(.*?)(?:\\end\{document\}|\Z)", src, re.S)
    if body:
        src = body.group(1)
    src = re.split(r"\\begin\{thebibliography\}|\\bibliography\{|\\printbibliography", src)[0]
    for env in TEX_DROP_ENVS:
        src = re.sub(r"\\begin\{%s\*?\}.*?\\end\{%s\*?\}" % (env, env), " ", src, flags=re.S)
    text = _tex_to_text(src)
    text = re.sub(r"[ \t]+([.,;:])", r"\1", text)          # space left by a dropped \cite
    text = text.replace("---", "\u2014").replace("--", "\u2013")
    return text.replace("``", "\u201c").replace("''", "\u201d")


# ------------------------------------------------------------- segmentation

TERMINAL = tuple('.!?:;)"\u201d\u2019]')
REFS_RE = _rx(r"^(?:\d+[.)]?\s*)?(?:references|bibliography|literature cited|works cited|"
              r"reference list)\.?$")
WORD_RE = re.compile(r"[A-Za-z0-9\u00C0-\u024F\u0370-\u03FF]+"
                     r"(?:['\u2019\-\u2013/.\u00B7][A-Za-z0-9\u00C0-\u024F\u0370-\u03FF]+)*")
_DOT = "\u2024"
PROTECT = ["e.g.", "i.e.", "Fig.", "Figs.", "Eq.", "Eqs.", "Ref.", "Refs.", "vs.", "cf.",
           "approx.", "No.", "Nos.", "Chr.", "Suppl.", "Supp.", "Tab.", "Sect.", "Sec.", "ca.",
           "resp.", "Dr.", "Prof.", "Inc.", "Ltd.", "Corp.", "Vol.", "vol.", "pp.", "p.",
           "ed.", "eds.", "Ext.", "St.", "Mr.", "Ms.", "Jr.", "Sr."]
_PROTECT_RE = re.compile(r"(?<![A-Za-z])(?:%s)" % "|".join(
    re.escape(a) for a in sorted(PROTECT, key=len, reverse=True)))
_ETAL_RE = re.compile(r"\bet al\.(?!\s+[A-Z][a-z])")
_SUPER_CITE_RE = re.compile(r"(?<=[a-z)\]][.!?])\d{1,3}(?:[,\u2013-]\d{1,3})*(?=\s+[A-Z])")
_SPLIT_RE = re.compile(r"(?:(?<=[.!?])|(?<=[.!?][)\]\"\u201d\u2019]))\s+"
                       r"(?=[A-Z0-9(\[\"\u201c\u2018])")


def words(s: str) -> list[str]:
    return WORD_RE.findall(s)


def split_blocks(kind: str, text: str) -> list[str]:
    blocks = []
    for block in re.split(r"\n[ \t]*\n", text):
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if not lines:
            continue
        # In plain text one paragraph per line is common; wrapped text is joined.
        if kind in ("txt", "pdf") and len(lines) > 1 and \
                sum(ln.endswith(TERMINAL) for ln in lines) / len(lines) >= 0.6:
            blocks.extend(lines)
        else:
            blocks.append(" ".join(lines))
    return blocks


def split_sentences(par: str) -> list[str]:
    t = _SUPER_CITE_RE.sub("", par)
    t = _ETAL_RE.sub("et al" + _DOT, t)
    t = _PROTECT_RE.sub(lambda m: m.group(0).replace(".", _DOT), t)
    return [p.replace(_DOT, ".").strip() for p in _SPLIT_RE.split(t) if p.strip()]


def segment(kind: str, raw: str) -> tuple[list[list[str]], list[str], str]:
    """Return (paragraphs as sentence lists, headings, cleaned text)."""
    if kind == "tex":
        text = _tex_clean(raw)
    elif kind == "md":
        text = _md_clean(raw)
    else:
        text = raw
    text = text.replace("\r\n", "\n").replace("\u00a0", " ")
    paragraphs, headings = [], []
    for block in split_blocks(kind, text):
        is_heading = block.startswith(HEADING)
        block = block.replace(HEADING, "").strip()
        if not block:
            continue
        if REFS_RE.match(block):
            break
        n = len(words(block))
        if n == 0:
            continue
        if is_heading or (not block.endswith(TERMINAL) and n < 15):
            headings.append(block)
            continue
        if n < 4:
            continue
        paragraphs.append(split_sentences(block))
    return paragraphs, headings, text


# ------------------------------------------------------------------ analysis

def first_word(sentence: str) -> str:
    w = words(sentence)
    return w[0] if w else ""


def is_title_case(heading: str) -> bool:
    small = {"a", "an", "the", "and", "or", "but", "of", "in", "on", "for", "to", "with", "by",
             "at", "from", "as", "vs", "via", "into", "over"}
    ws = [w for w in words(heading) if w.isalpha()]
    if len(ws) < 3:
        return False
    rest = [w for w in ws[1:] if w.lower() not in small]
    return len(rest) >= 2 and all(w[0].isupper() for w in rest)


def _long_form_fits(short: str, before: str) -> bool:
    """Schwartz-Hearst test: the letters of `short` appear, in order, in the words
    just before the parenthesis, the first one at a word start."""
    chars = [c.lower() for c in short if c.isalnum()]
    lf = " ".join(before.split()[-min(len(chars) + 5, 2 * len(chars)):]).lower()
    li = len(lf) - 1
    for si in range(len(chars) - 1, -1, -1):
        while li >= 0 and (lf[li] != chars[si]
                           or (si == 0 and li > 0 and lf[li - 1].isalnum())):
            li -= 1
        if li < 0:
            return False
        li -= 1
    return True


def _short(s: str, n: int = 60) -> str:
    return s if len(s) <= n else s[:n // 2 - 2] + " ... " + s[-(n // 2 - 3):]


def language(sents: list[tuple]) -> dict:
    """Usage errors, spelling consistency, and abbreviation order (references/language.md)."""
    where = lambda pi, si: f"P{pi}.S{si}"
    usage = []
    for pi, si, s, _ in sents:
        for label, rx, advice in USAGE:
            for m in rx.finditer(s):
                usage.append({"where": where(pi, si), "label": label,
                              "match": _short(m.group(0).strip()), "advice": advice})

    ize, usuk = {"z": [], "s": []}, {"US": [], "UK": []}
    for pi, si, s, _ in sents:
        for m in IZE_RE.finditer(s):
            ize[m.group(1).lower()].append((m.group(0), where(pi, si)))
        for key, rx in (("US", US_RE), ("UK", UK_RE)):
            usuk[key] += [(m.group(0), where(pi, si)) for m in rx.finditer(s)]

    def axis(d: dict, names: dict) -> dict:
        a, b = list(d)
        out = {names[k]: len(v) for k, v in d.items()}
        if d[a] and d[b]:
            minority = b if len(d[b]) <= len(d[a]) else a
            out["minority"] = [{"form": f, "where": w} for f, w in d[minority]]
        return out

    spelling = {"ize_ise": axis(ize, {"z": "-ize", "s": "-ise"}),
                "us_uk": axis(usuk, {"US": "US", "UK": "UK"})}
    # Oxford spelling pairs -ize with UK forms; -ise with US forms is no convention.
    spelling["ise_with_us"] = len(ize["s"]) > len(ize["z"]) and len(usuk["US"]) > len(usuk["UK"])

    order = {(pi, si): k for k, (pi, si, _, _) in enumerate(sents)}
    defs: dict[str, list] = {}
    for pi, si, s, _ in sents:
        for m in ABBR_DEF_RE.finditer(s):
            tok = m.group(1)
            if len(tok) > 2 and tok.endswith("s") and tok[-2].isupper():
                tok = tok[:-1]   # (SNPs) defines SNP
            before = s[:m.start()]
            if tok not in before.split()[-2:] and _long_form_fits(tok, before):
                defs.setdefault(tok, []).append((order[(pi, si)], m.start(1), where(pi, si)))
    abbr = {"defined": len(defs), "used_before_definition": [], "defined_more_than_once": [],
            "rarely_used": []}
    for tok, dl in defs.items():
        use_rx = re.compile(rf"(?<![\w-]){re.escape(tok)}(?:s|es)?(?![\w-])")
        def_at = {(k, st) for k, st, _ in dl}
        uses = [(order[(pi, si)], m.start(), where(pi, si))
                for pi, si, s, _ in sents for m in use_rx.finditer(s)
                if (order[(pi, si)], m.start()) not in def_at]
        first = min(dl)
        early = [u for u in uses if u[:2] < first[:2]]
        if early:
            abbr["used_before_definition"].append(
                {"abbr": tok, "first_use": early[0][2], "defined": first[2]})
        if len(dl) > 1:
            abbr["defined_more_than_once"].append({"abbr": tok, "where": [d[2] for d in dl]})
        later = len(uses) - len(early)
        if later < 2:
            abbr["rarely_used"].append({"abbr": tok, "uses_after_definition": later})
    return {"usage": usage, "spelling": spelling, "abbreviations": abbr}


def analyse(path: str) -> dict:
    kind, raw = read_input(path)
    paragraphs, headings, text = segment(kind, raw)

    sents = []   # (paragraph no., sentence no., text, word count)
    for pi, par in enumerate(paragraphs, 1):
        for si, s in enumerate(par, 1):
            n = len(words(s))
            if n:
                sents.append((pi, si, s, n))
    lengths = [n for *_, n in sents]
    total_words = sum(lengths)
    n_sent = len(lengths)
    mean = statistics.mean(lengths) if lengths else 0.0
    sd = statistics.stdev(lengths) if n_sent > 1 else 0.0
    cv = sd / mean if mean else 0.0

    eligible = [pi for pi, par in enumerate(paragraphs, 1) if len(par) >= 3]
    uniform = [pi for pi, par in enumerate(paragraphs, 1)
               if len(par) >= 3 and all(UNIFORM_BAND[0] <= len(words(s)) <= UNIFORM_BAND[1]
                                        for s in par)]

    openers = Counter(first_word(s) for _, _, s, _ in sents)
    openers_ci = Counter(w.lower() for w in openers.elements())
    adjacent_same = sum(
        1 for a, b in zip(sents, sents[1:])
        if a[0] == b[0] and first_word(a[2]).lower() == first_word(b[2]).lower()
    )
    connector_starts = sum(bool(CONNECTOR_START.match(s)) for _, _, s, _ in sents)

    counts = {label: Counter() for label, _ in CATEGORIES}
    counts["spotlight openers"] = Counter()
    em_dashes = hedge_stacks = sig_total = sig_untested = 0
    flagged = []
    for pi, si, s, n in sents:
        flags = []
        for label, rx in CATEGORIES:
            hits = [m.group(0).lower().strip(", ") for m in rx.finditer(s)]
            if hits:
                counts[label].update(hits)
                flags.append(f"{label}: {' | '.join(dict.fromkeys(hits))}")
        m = SPOTLIGHT_START.match(s)
        if m:
            counts["spotlight openers"][m.group(0)] += 1
            flags.append(f"spotlight opener: {m.group(0)}")
        d = len(EM_DASH.findall(s))
        if d:
            em_dashes += d
            flags.append("em dash")
        if len(HEDGE.findall(s)) >= 3 or HEDGE_PAIR.search(s):
            hedge_stacks += 1
            flags.append("stacked hedges")
        if SIGNIFICANT.search(s):
            sig_total += 1
            if not STAT_MARKER.search(s):
                sig_untested += 1
                flags.append('"significant" without a test in the sentence')
        if n > VERY_LONG_WORDS:
            flags.append(f"very long ({n} words)")
        if flags:
            flagged.append({"para": pi, "sent": si, "words": n, "flags": flags, "text": s})

    vocab_hits = sum(counts["AI vocabulary"].values())
    all_hits = sum(sum(c.values()) for c in counts.values()) + em_dashes + hedge_stacks
    per_k = (lambda x: 1000.0 * x / total_words) if total_words else (lambda x: 0.0)

    raw_no_comments = re.sub(r"(?<!\\)%.*", "", raw) if kind == "tex" else raw
    formatting = {
        "markdown_bold": len(re.findall(r"\*\*[^*\n]+\*\*", raw)) if kind in ("txt", "md") else 0,
        "curly_quotes_in_tex": len(re.findall(r"[\u201c\u201d\u2018\u2019]", raw_no_comments))
        if kind == "tex" else 0,
        "title_case_headings": [h for h in headings if is_title_case(h)],
    }

    return {
        "file": path,
        "kind": kind,
        "words": total_words,
        "sentences": n_sent,
        "paragraphs": len(paragraphs),
        "length": {
            "mean": round(mean, 1), "sd": round(sd, 1), "cv": round(cv, 2),
            "median": statistics.median(lengths) if lengths else 0,
            "min": min(lengths) if lengths else 0, "max": max(lengths) if lengths else 0,
            "short_share": round(sum(n < SHORT_WORDS for n in lengths) / n_sent, 3) if n_sent else 0,
            "long_share": round(sum(n > LONG_WORDS for n in lengths) / n_sent, 3) if n_sent else 0,
        },
        "uniform_paragraphs": uniform,
        "eligible_paragraphs": len(eligible),
        "openers": openers_ci.most_common(6),
        "adjacent_same_opener": adjacent_same,
        "connector_start_share": round(connector_starts / n_sent, 3) if n_sent else 0,
        "counts": {k: dict(v.most_common()) for k, v in counts.items()},
        "em_dashes": em_dashes,
        "hedge_stacks": hedge_stacks,
        "significant": {"total": sig_total, "without_test": sig_untested},
        "ai_vocab_per_1000": round(per_k(vocab_hits), 1),
        "all_tells_per_1000": round(per_k(all_hits), 1),
        "formatting": formatting,
        "flagged": flagged,
        **language(sents),
    }


# ------------------------------------------------------------------- report

def _pct(x: float) -> str:
    return f"{100 * x:.0f}%"


def report(r: dict, max_items: int) -> str:
    L = r["length"]
    out = [f"prose_check: {r['file']}  ({r['kind']}; diagnostic proxies, not an AI detector)",
           f"Words {r['words']} | sentences {r['sentences']} | paragraphs {r['paragraphs']}"]
    if not r["sentences"]:
        out.append("No prose sentences found.")
        return "\n".join(out)

    out.append("\nRhythm")
    tag = "  <- uniform" if L["cv"] < LOW_CV and r["sentences"] >= 10 else ""   # noisy below 10
    out.append(f"  Sentence length: mean {L['mean']}, SD {L['sd']}, CV {L['cv']}{tag}; "
               f"median {L['median']}, range {L['min']}-{L['max']}")
    out.append(f"  Short (<{SHORT_WORDS} words) {_pct(L['short_share'])} | "
               f"long (>{LONG_WORDS} words) {_pct(L['long_share'])}")
    if r["eligible_paragraphs"]:
        ids = ", ".join(f"P{p}" for p in r["uniform_paragraphs"][:12])
        out.append(f"  Flat paragraphs (3+ sentences, all {UNIFORM_BAND[0]}-{UNIFORM_BAND[1]} words): "
                   f"{len(r['uniform_paragraphs'])} of {r['eligible_paragraphs']}"
                   + (f"  -> {ids}" if ids else ""))
    top = ", ".join(f"{w} {_pct(c / r['sentences'])}" for w, c in r["openers"][:5])
    lead = r["openers"][0][1] / r["sentences"] if r["openers"] else 0
    tag = "  <- repetitive" if lead > HIGH_OPENER_SHARE and r["sentences"] >= 8 else ""
    out.append(f"  First words: {top}{tag}")
    out.append(f"  Same first word in adjacent sentences: {r['adjacent_same_opener']}")
    tag = "  <- connector-heavy" if r["connector_start_share"] > HIGH_CONNECTOR_SHARE else ""
    out.append(f"  Sentences opening with a connector: {_pct(r['connector_start_share'])}{tag}")

    out.append("\nWording")
    tag = "  <- high" if r["ai_vocab_per_1000"] > HIGH_TELL_RATE else ""
    out.append(f"  AI vocabulary: {r['ai_vocab_per_1000']} per 1000 words{tag}")
    out.append(f"  All pattern hits: {r['all_tells_per_1000']} per 1000 words")
    for label, c in r["counts"].items():
        if c:
            items = "; ".join(f"{k} x{v}" if v > 1 else k for k, v in list(c.items())[:8])
            out.append(f"  {label}: {items}")
    if r["em_dashes"]:
        out.append(f"  em dashes: {r['em_dashes']}")
    if r["hedge_stacks"]:
        out.append(f"  sentences with stacked hedges: {r['hedge_stacks']}")
    sig = r["significant"]
    if sig["total"]:
        out.append(f"  \"significant(ly)\": {sig['total']} sentences, "
                   f"{sig['without_test']} with no test or P value in the same sentence")
    f = r["formatting"]
    if f["markdown_bold"]:
        out.append(f"  Markdown bold in text: {f['markdown_bold']}")
    if f["curly_quotes_in_tex"]:
        out.append(f"  curly quotes in LaTeX source: {f['curly_quotes_in_tex']}")
    if f["title_case_headings"]:
        out.append(f"  Title Case headings (check journal style): "
                   + "; ".join(f['title_case_headings'][:5]))

    out += language_report(r, max_items)

    items = r["flagged"] if max_items == 0 else r["flagged"][:max_items]
    if items:
        more = len(r["flagged"]) - len(items)
        out.append(f"\nFlagged sentences ({len(r['flagged'])}"
                   + (f"; first {len(items)}, use --max 0 for all" if more else "") + ")")
        for it in items:
            text = it["text"] if len(it["text"]) <= 170 else it["text"][:167] + "..."
            out.append(f"  P{it['para']}.S{it['sent']} [{'; '.join(it['flags'])}]")
            out.append(f"      {text}")
    return "\n".join(out)


def _minority(r: dict) -> int:
    return sum(len(r["spelling"][k].get("minority", [])) for k in ("ize_ise", "us_uk"))


def _abbr_problems(r: dict) -> int:
    ab = r["abbreviations"]
    return sum(len(ab[k]) for k in ("used_before_definition", "defined_more_than_once", "rarely_used"))


def language_report(r: dict, max_items: int) -> list[str]:
    out = ["\nLanguage (usage and consistency; not counted in the pattern hits above)"]
    usage = r["usage"]
    shown = usage if max_items == 0 else usage[:max_items]
    out.append(f"  Usage problems: {len(usage)}"
               + (f" (first {len(shown)}, use --max 0 for all)" if len(shown) < len(usage) else ""))
    for u in shown:
        out.append(f"    {u['where']} {u['label']}: \"{u['match']}\" -> {u['advice']}")

    sp = r["spelling"]
    for key, (a, b) in (("ize_ise", ("-ize", "-ise")), ("us_uk", ("US", "UK"))):
        d = sp[key]
        if not d[a] and not d[b]:
            continue
        line = f"  Spelling {a}/{b}: {d[a]}/{d[b]}"
        if "minority" in d:
            forms = ", ".join(f"{m['form']} {m['where']}" for m in d["minority"][:8])
            line += f"  <- mixed; minority forms: {forms}"
        out.append(line)
    if sp["ise_with_us"]:
        out.append("  -ise spellings alongside US forms: choose US (-ize) or UK throughout")

    ab = r["abbreviations"]
    out.append(f"  Abbreviations defined: {ab['defined']}")
    for x in ab["used_before_definition"]:
        out.append(f"    {x['abbr']} used at {x['first_use']} before its definition at {x['defined']}")
    for x in ab["defined_more_than_once"]:
        out.append(f"    {x['abbr']} defined {len(x['where'])} times ({', '.join(x['where'])}); "
                   "fine only as once in the abstract and once in the main text")
    rare = ab["rarely_used"]
    if rare:
        out.append("    used fewer than twice after definition (spell out?): "
                   + ", ".join(f"{x['abbr']} ({x['uses_after_definition']})" for x in rare))
    if any(ab[k] for k in ("used_before_definition", "defined_more_than_once", "rarely_used")):
        out.append("    (on an excerpt, definitions may sit outside the text; judge in context)")
    return out


def compare(a: dict, b: dict) -> str:
    def row(name, x, y):
        return f"  {name:<38}{str(x):>12}{str(y):>12}"

    def top_opener(r):
        if not r["openers"] or not r["sentences"]:
            return "-"
        w, c = r["openers"][0]
        return f"{w} {_pct(c / r['sentences'])}"

    rows = [
        ("words", a["words"], b["words"]),
        ("sentences", a["sentences"], b["sentences"]),
        ("mean words per sentence", a["length"]["mean"], b["length"]["mean"]),
        ("SD of sentence length", a["length"]["sd"], b["length"]["sd"]),
        ("CV of sentence length", a["length"]["cv"], b["length"]["cv"]),
        (f"short sentences (<{SHORT_WORDS})", _pct(a["length"]["short_share"]),
         _pct(b["length"]["short_share"])),
        (f"long sentences (>{LONG_WORDS})", _pct(a["length"]["long_share"]),
         _pct(b["length"]["long_share"])),
        ("flat paragraphs", f"{len(a['uniform_paragraphs'])}/{a['eligible_paragraphs']}",
         f"{len(b['uniform_paragraphs'])}/{b['eligible_paragraphs']}"),
        ("most common first word", top_opener(a), top_opener(b)),
        ("connector-initial sentences", _pct(a["connector_start_share"]),
         _pct(b["connector_start_share"])),
        ("AI vocabulary per 1000 words", a["ai_vocab_per_1000"], b["ai_vocab_per_1000"]),
        ("all pattern hits per 1000 words", a["all_tells_per_1000"], b["all_tells_per_1000"]),
        ("stock phrases", sum(a["counts"]["stock phrases"].values()),
         sum(b["counts"]["stock phrases"].values())),
        ("-ing tails", sum(a["counts"]["-ing tails"].values()),
         sum(b["counts"]["-ing tails"].values())),
        ("overclaim words", sum(a["counts"]["overclaim words"].values()),
         sum(b["counts"]["overclaim words"].values())),
        ("em dashes", a["em_dashes"], b["em_dashes"]),
        ("stacked hedges", a["hedge_stacks"], b["hedge_stacks"]),
        ('"significant" without a test', a["significant"]["without_test"],
         b["significant"]["without_test"]),
        ("usage problems", len(a["usage"]), len(b["usage"])),
        ("minority spellings", _minority(a), _minority(b)),
        ("abbreviation problems", _abbr_problems(a), _abbr_problems(b)),
    ]
    out = ["prose_check comparison (diagnostic proxies, not an AI detector)",
           row("", "before", "after"),
           row("", Path(a["file"]).name[:12], Path(b["file"]).name[:12])]
    out += [row(*r) for r in rows]
    out.append("Run on a single file for the flagged sentences.")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="+", help="one file, or BEFORE AFTER; '-' for stdin")
    ap.add_argument("--max", type=int, default=15, help="flagged sentences to list (0 = all)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()
    if len(args.files) > 2:
        ap.error("give one file, or two files to compare")
    results = [analyse(f) for f in args.files]
    if args.json:
        print(json.dumps(results[0] if len(results) == 1 else
                         {"before": results[0], "after": results[1]}, indent=2, ensure_ascii=False))
    elif len(results) == 1:
        print(report(results[0], args.max))
    else:
        print(compare(*results))


if __name__ == "__main__":
    main()
