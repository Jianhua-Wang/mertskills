# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Write assets/academic-template.pptx from the tokens in design.py.

Usage:
    uv run scripts/make_template.py [--out PATH]

Every part of the package is written from scratch, so the template is fully
determined by design.py: theme (colours + Arial/DengXian), one master, and the
eleven layouts in ``design.LAYOUTS``. Rerun after any change to design.py.
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))
import design as D  # noqa: E402

NS = (
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
)
XML_DECL = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
OFFICE_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
CT_PML = "application/vnd.openxmlformats-officedocument.presentationml"

MASTER_ID = 2147483648
LAYOUT_ID0 = 2147483649


def emu(inches: float) -> int:
    return int(round(inches * D.EMU_PER_IN))


def color_xml(c: str) -> str:
    if len(c) == 6 and all(ch in "0123456789ABCDEFabcdef" for ch in c):
        return f'<a:srgbClr val="{c.upper()}"/>'
    return f'<a:schemeClr val="{c}"/>'


# ==========================================================================
# Theme
# ==========================================================================

def theme_xml() -> str:
    clr = "".join(f'<a:{k}><a:srgbClr val="{v}"/></a:{k}>' for k, v in D.THEME_COLORS.items())
    font = (
        f'<a:latin typeface="{D.FONT_LATIN}"/><a:ea typeface="{D.FONT_EA}"/><a:cs typeface=""/>'
        f'<a:font script="Hans" typeface="{D.FONT_EA}"/>'
        f'<a:font script="Hant" typeface="{D.FONT_EA}"/>'
    )
    solid = '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    line = lambda w: (  # noqa: E731
        f'<a:ln w="{w}" cap="flat" cmpd="sng" algn="ctr">{solid}'
        '<a:prstDash val="solid"/><a:miter lim="800000"/></a:ln>'
    )
    fmt = (
        '<a:fmtScheme name="Flat">'
        f"<a:fillStyleLst>{solid * 3}</a:fillStyleLst>"
        f"<a:lnStyleLst>{line(9525)}{line(19050)}{line(28575)}</a:lnStyleLst>"
        "<a:effectStyleLst>"
        + "<a:effectStyle><a:effectLst/></a:effectStyle>" * 3
        + "</a:effectStyleLst>"
        f"<a:bgFillStyleLst>{solid * 3}</a:bgFillStyleLst>"
        "</a:fmtScheme>"
    )
    return (
        XML_DECL
        + f'<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="{D.THEME_NAME}">'
        "<a:themeElements>"
        f'<a:clrScheme name="{D.THEME_NAME}">{clr}</a:clrScheme>'
        f'<a:fontScheme name="{D.THEME_NAME}"><a:majorFont>{font}</a:majorFont>'
        f"<a:minorFont>{font}</a:minorFont></a:fontScheme>"
        f"{fmt}</a:themeElements>"
        "<a:objectDefaults>"
        # Shapes a person draws by hand: no fill, accent outline, ink text.
        '<a:spDef><a:spPr><a:noFill/><a:ln w="19050"><a:solidFill><a:schemeClr val="accent1"/>'
        '</a:solidFill></a:ln></a:spPr><a:bodyPr rtlCol="0" anchor="ctr"/><a:lstStyle/>'
        '<a:style><a:lnRef idx="1"><a:schemeClr val="accent1"/></a:lnRef>'
        '<a:fillRef idx="0"><a:schemeClr val="accent1"/></a:fillRef>'
        '<a:effectRef idx="0"><a:schemeClr val="accent1"/></a:effectRef>'
        '<a:fontRef idx="minor"><a:schemeClr val="tx1"/></a:fontRef></a:style></a:spDef>'
        '<a:lnDef><a:spPr><a:ln w="19050"><a:solidFill><a:schemeClr val="accent1"/></a:solidFill>'
        '</a:ln></a:spPr><a:bodyPr/><a:lstStyle/>'
        '<a:style><a:lnRef idx="1"><a:schemeClr val="accent1"/></a:lnRef>'
        '<a:fillRef idx="0"><a:schemeClr val="accent1"/></a:fillRef>'
        '<a:effectRef idx="0"><a:schemeClr val="accent1"/></a:effectRef>'
        '<a:fontRef idx="minor"><a:schemeClr val="tx1"/></a:fontRef></a:style></a:lnDef>'
        '<a:txDef><a:spPr><a:noFill/></a:spPr><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" '
        'bIns="0" rtlCol="0"><a:spAutoFit/></a:bodyPr><a:lstStyle/></a:txDef>'
        "</a:objectDefaults><a:extraClrSchemeLst/></a:theme>"
    )


# ==========================================================================
# Text styles -> lstStyle / txStyles
# ==========================================================================

def _bullet_xml(style: D.TextStyle, level: int) -> tuple[str, int, int]:
    """Return (bullet xml, marL emu, indent emu) for one outline level."""
    if style.bullets == "dot":
        ch = D.BULLET_CHARS[min(level, len(D.BULLET_CHARS) - 1)]
        mar = emu(D.BULLET_INDENT * (level + 1))
        clr = '<a:buClr><a:schemeClr val="accent1"/></a:buClr>' if level == 0 else (
            f'<a:buClr><a:srgbClr val="{D.INK_SECONDARY}"/></a:buClr>')
        return (f'{clr}<a:buSzPct val="100000"/><a:buFont typeface="Arial"/>'
                f'<a:buChar char="{ch}"/>', mar, -emu(D.BULLET_INDENT))
    if style.bullets == "number":
        ind = 0.5
        return ('<a:buClr><a:schemeClr val="accent1"/></a:buClr><a:buSzPct val="100000"/>'
                '<a:buFont typeface="+mj-lt"/><a:buAutoNum type="arabicPlain"/>',
                emu(ind), -emu(ind))
    return "<a:buNone/>", 0, 0


def level_ppr(style: D.TextStyle, level: int) -> str:
    sz = style.sizes[min(level, len(style.sizes) - 1)] * 100
    before = style.space_before[min(level, len(style.space_before) - 1)] * 100
    bullet, mar, ind = _bullet_xml(style, level)
    attrs = [f'marL="{mar}"', f'indent="{ind}"', f'algn="{style.align}"', 'defTabSz="457200"',
             'rtl="0"', 'eaLnBrk="1"', 'latinLnBrk="0"', 'hangingPunct="1"']
    rpr = [f'sz="{sz}"', f'b="{1 if style.bold else 0}"', 'kern="1200"']
    if style.caps:
        rpr.append('cap="all"')
    if style.spacing:
        rpr.append(f'spc="{style.spacing}"')
    return (
        f'<a:lvl{level + 1}pPr {" ".join(attrs)}>'
        f'<a:lnSpc><a:spcPct val="{style.line_spacing * 1000}"/></a:lnSpc>'
        f'<a:spcBef><a:spcPts val="{before}"/></a:spcBef><a:spcAft><a:spcPts val="0"/></a:spcAft>'
        f"{bullet}"
        f'<a:defRPr {" ".join(rpr)}><a:solidFill>{color_xml(style.color)}</a:solidFill>'
        '<a:latin typeface="+mn-lt"/><a:ea typeface="+mn-ea"/><a:cs typeface="+mn-cs"/>'
        "</a:defRPr>"
        f"</a:lvl{level + 1}pPr>"
    )


def lst_style(style: D.TextStyle, levels: int = 9) -> str:
    return "".join(level_ppr(style, i) for i in range(levels))


def body_pr(style: D.TextStyle) -> str:
    return ('<a:bodyPr vert="horz" wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" '
            f'rtlCol="0" anchor="{style.anchor}" anchorCtr="0"><a:noAutofit/></a:bodyPr>')


# ==========================================================================
# Shapes
# ==========================================================================

def xfrm(x: float, y: float, w: float, h: float) -> str:
    return (f'<a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/>'
            f'<a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>')


PH_NAMES = {
    "title": "Title", "ctrTitle": "Title", "subTitle": "Subtitle", "body": "Text",
    "pic": "Picture", "sldNum": "Slide Number",
}


def ph_attr(slot: D.Slot, custom_prompt: bool) -> str:
    parts = [f'type="{slot.kind}"']
    if slot.kind == "sldNum":
        parts.append('sz="quarter"')
    if slot.idx is not None:
        parts.append(f'idx="{slot.idx}"')
    if custom_prompt:
        parts.append('hasCustomPrompt="1"')
    return " ".join(parts)


def placeholder_sp(slot: D.Slot, shape_id: int, on_master: bool = False) -> str:
    style = D.TEXT_STYLES[slot.style]
    name = f"{PH_NAMES.get(slot.kind, 'Text')} {shape_id - 1} ({slot.role})"
    custom = bool(slot.prompt) and not on_master
    if slot.kind == "sldNum":
        para = ('<a:p><a:fld id="{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}" type="slidenum">'
                '<a:rPr lang="en-US"/><a:t>&lt;#&gt;</a:t></a:fld><a:endParaRPr lang="en-US"/></a:p>')
    else:
        text = slot.prompt or "Text"
        para = f'<a:p><a:r><a:rPr lang="en-US"/><a:t>{escape(text)}</a:t></a:r></a:p>'
    levels = 3 if style.bullets == "dot" else 1
    lst = lst_style(style, levels)
    # No outline on picture placeholders: a picture that fills one inherits the
    # placeholder's line, so any frame drawn here would end up around the figure.
    sp_extra = '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
    if slot.kind == "pic":
        sp_extra += '<a:noFill/><a:ln><a:noFill/></a:ln>'
    lock = '<a:spLocks noGrp="1"/>'
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{shape_id}" name="{escape(name)}"/>'
        f'<p:cNvSpPr>{lock}</p:cNvSpPr><p:nvPr><p:ph {ph_attr(slot, custom)}/></p:nvPr></p:nvSpPr>'
        f'<p:spPr>{xfrm(slot.x, slot.y, slot.w, slot.h)}{sp_extra}</p:spPr>'
        f'<p:txBody>{body_pr(style)}<a:lstStyle>{lst}</a:lstStyle>{para}</p:txBody></p:sp>'
    )


def rect_sp(shape_id: int, name: str, x: float, y: float, w: float, h: float, fill: str) -> str:
    """A plain filled rectangle (template chrome): no outline, no text, not editable on slides."""
    color = (f'<a:schemeClr val="{fill}"/>' if fill.startswith("accent")
             else f'<a:srgbClr val="{fill}"/>')
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{shape_id}" name="{escape(name)}"/>'
        '<p:cNvSpPr><a:spLocks noGrp="1" noSelect="1" noMove="1" noResize="1"/></p:cNvSpPr>'
        f'<p:nvPr userDrawn="1"/></p:nvSpPr>'
        f'<p:spPr>{xfrm(x, y, w, h)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f'<a:solidFill>{color}</a:solidFill><a:ln><a:noFill/></a:ln></p:spPr>'
        '<p:txBody><a:bodyPr rtlCol="0" anchor="ctr"/><a:lstStyle/><a:p><a:endParaRPr lang="en-US"/></a:p>'
        '</p:txBody></p:sp>'
    )


def headline_rule(first_id: int) -> list[str]:
    """The divider under a content slide's headline: grey hairline + accent mark."""
    pt = 1 / 72
    line_h, mark_h = D.HEAD_RULE_PT * pt, D.HEAD_MARK_PT * pt
    return [
        rect_sp(first_id, "Headline rule", D.M, D.HEAD_RULE_Y - line_h / 2, D.CONTENT_W, line_h,
                D.HAIRLINE),
        rect_sp(first_id + 1, "Headline mark", D.M, D.HEAD_RULE_Y - mark_h / 2, D.HEAD_MARK_W,
                mark_h, "accent1"),
    ]


def sp_tree(shapes: list[str]) -> str:
    return (
        '<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
        '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
        '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
        + "".join(shapes) + "</p:spTree>"
    )


CLR_MAP = ('bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" '
           'accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" '
           'hlink="hlink" folHlink="folHlink"')


# ==========================================================================
# Master
# ==========================================================================

def master_xml() -> str:
    head = D.Slot("headline", "title", None, D.M, D.HEAD_Y, D.CONTENT_W, D.HEAD_H, "headline",
                  "Headline")
    body = D.Slot("text", "body", 1, D.M, D.BODY_Y, D.CONTENT_W, D.BODY_H, "body", "Text")
    num = D._slide_number()
    shapes = [placeholder_sp(s, i + 2, on_master=True) for i, s in enumerate((head, body, num))]
    # The bottom bar sits on the master, so every slide (hero slides included) carries it.
    shapes.append(rect_sp(len(shapes) + 2, "Bottom bar", 0, D.BAR_Y, D.SLIDE_W, D.BAR_H, "accent1"))
    ids = "".join(
        f'<p:sldLayoutId id="{LAYOUT_ID0 + i}" r:id="rId{i + 1}"/>' for i in range(len(D.LAYOUTS))
    )
    title_style = lst_style(D.TEXT_STYLES["headline"], 1)
    body_style = lst_style(D.TEXT_STYLES["body"], 9)
    other = lst_style(D.TextStyle((18,)), 9)
    return (
        XML_DECL + f"<p:sldMaster {NS}>"
        '<p:cSld><p:bg><p:bgPr><a:solidFill><a:schemeClr val="bg1"/></a:solidFill>'
        "<a:effectLst/></p:bgPr></p:bg>"
        f"{sp_tree(shapes)}</p:cSld>"
        f"<p:clrMap {CLR_MAP}/>"
        f"<p:sldLayoutIdLst>{ids}</p:sldLayoutIdLst>"
        '<p:hf hdr="0" ftr="0" dt="0"/>'
        f"<p:txStyles><p:titleStyle>{title_style}</p:titleStyle>"
        f"<p:bodyStyle>{body_style}</p:bodyStyle>"
        f"<p:otherStyle>{other}</p:otherStyle></p:txStyles>"
        "</p:sldMaster>"
    )


def master_rels() -> str:
    rels = "".join(
        f'<Relationship Id="rId{i + 1}" Type="{OFFICE_REL}/slideLayout" '
        f'Target="../slideLayouts/slideLayout{i + 1}.xml"/>'
        for i in range(len(D.LAYOUTS))
    )
    rels += (f'<Relationship Id="rId{len(D.LAYOUTS) + 1}" Type="{OFFICE_REL}/theme" '
             'Target="../theme/theme1.xml"/>')
    return XML_DECL + f'<Relationships xmlns="{REL_NS}">{rels}</Relationships>'


# ==========================================================================
# Layouts
# ==========================================================================

def layout_xml(layout: D.Layout) -> str:
    shapes = [placeholder_sp(s, i + 2) for i, s in enumerate(layout.slots)]
    if layout.slot("headline") is not None:
        shapes += headline_rule(len(shapes) + 2)
    has_number = layout.slot("slide_number") is not None
    hf = ('<p:hf hdr="0" ftr="0" dt="0"/>' if has_number
          else '<p:hf sldNum="0" hdr="0" ftr="0" dt="0"/>')
    return (
        XML_DECL
        + f'<p:sldLayout {NS} type="{layout.ooxml_type}" preserve="1" userDrawn="1">'
        f'<p:cSld name="{escape(layout.name)}">{sp_tree(shapes)}</p:cSld>'
        f"<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>{hf}</p:sldLayout>"
    )


def layout_rels() -> str:
    return (XML_DECL + f'<Relationships xmlns="{REL_NS}"><Relationship Id="rId1" '
            f'Type="{OFFICE_REL}/slideMaster" Target="../slideMasters/slideMaster1.xml"/>'
            "</Relationships>")


# ==========================================================================
# Package parts
# ==========================================================================

def presentation_xml() -> str:
    default_text = lst_style(D.TextStyle((18,)), 9)
    return (
        XML_DECL + f'<p:presentation {NS} saveSubsetFonts="1" autoCompressPictures="0">'
        f'<p:sldMasterIdLst><p:sldMasterId id="{MASTER_ID}" r:id="rId1"/></p:sldMasterIdLst>'
        f'<p:sldSz cx="{emu(D.SLIDE_W)}" cy="{emu(D.SLIDE_H)}"/>'
        '<p:notesSz cx="6858000" cy="9144000"/>'
        f'<p:defaultTextStyle><a:defPPr><a:defRPr lang="en-US"/></a:defPPr>{default_text}'
        "</p:defaultTextStyle></p:presentation>"
    )


def presentation_rels() -> str:
    rels = [
        ("rId1", "slideMaster", "slideMasters/slideMaster1.xml"),
        ("rId2", "presProps", "presProps.xml"),
        ("rId3", "viewProps", "viewProps.xml"),
        ("rId4", "theme", "theme/theme1.xml"),
        ("rId5", "tableStyles", "tableStyles.xml"),
    ]
    body = "".join(
        f'<Relationship Id="{i}" Type="{OFFICE_REL}/{t}" Target="{p}"/>' for i, t, p in rels
    )
    return XML_DECL + f'<Relationships xmlns="{REL_NS}">{body}</Relationships>'


def content_types() -> str:
    over = [
        ("/ppt/presentation.xml", f"{CT_PML}.presentation.main+xml"),
        ("/ppt/slideMasters/slideMaster1.xml", f"{CT_PML}.slideMaster+xml"),
        ("/ppt/presProps.xml", f"{CT_PML}.presProps+xml"),
        ("/ppt/viewProps.xml", f"{CT_PML}.viewProps+xml"),
        ("/ppt/theme/theme1.xml", "application/vnd.openxmlformats-officedocument.theme+xml"),
        ("/ppt/tableStyles.xml", f"{CT_PML}.tableStyles+xml"),
        ("/docProps/core.xml", "application/vnd.openxmlformats-package.core-properties+xml"),
        ("/docProps/app.xml",
         "application/vnd.openxmlformats-officedocument.extended-properties+xml"),
    ]
    over += [(f"/ppt/slideLayouts/slideLayout{i + 1}.xml", f"{CT_PML}.slideLayout+xml")
             for i in range(len(D.LAYOUTS))]
    body = "".join(f'<Override PartName="{p}" ContentType="{c}"/>' for p, c in over)
    return (
        XML_DECL
        + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Default Extension="png" ContentType="image/png"/>'
        '<Default Extension="jpeg" ContentType="image/jpeg"/>'
        f"{body}</Types>"
    )


ROOT_RELS = (
    XML_DECL + f'<Relationships xmlns="{REL_NS}">'
    f'<Relationship Id="rId1" Type="{OFFICE_REL}/officeDocument" Target="ppt/presentation.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/'
    'metadata/core-properties" Target="docProps/core.xml"/>'
    f'<Relationship Id="rId3" Type="{OFFICE_REL}/extended-properties" Target="docProps/app.xml"/>'
    "</Relationships>"
)

CORE = (
    XML_DECL
    + '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
    'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
    'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
    "<dc:title>Academic template</dc:title><dc:creator>slide-studio</dc:creator>"
    "<cp:lastModifiedBy>slide-studio</cp:lastModifiedBy><cp:revision>1</cp:revision>"
    '<dcterms:created xsi:type="dcterms:W3CDTF">2026-01-01T00:00:00Z</dcterms:created>'
    '<dcterms:modified xsi:type="dcterms:W3CDTF">2026-01-01T00:00:00Z</dcterms:modified>'
    "</cp:coreProperties>"
)

APP = (
    XML_DECL
    + '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
    'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
    "<Application>Microsoft Office PowerPoint</Application>"
    "<PresentationFormat>Widescreen</PresentationFormat><Slides>0</Slides>"
    "<AppVersion>16.0000</AppVersion></Properties>"
)

PRES_PROPS = (XML_DECL + f"<p:presentationPr {NS}/>")

VIEW_PROPS = (
    XML_DECL + f'<p:viewPr {NS} lastView="sldThumbnailView"><p:normalViewPr>'
    '<p:restoredLeft sz="15620"/><p:restoredTop sz="94660"/></p:normalViewPr>'
    '<p:gridSpacing cx="76200" cy="76200"/></p:viewPr>'
)

# Default table style "No Style, No Grid": tables start bare, rules are drawn per cell.
TABLE_STYLES = (
    XML_DECL + '<a:tblStyleLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'def="{2D5ABB26-0587-4C30-8999-92F81FD0307C}"/>'
)


def build(out: Path) -> None:
    parts: dict[str, str] = {
        "[Content_Types].xml": content_types(),
        "_rels/.rels": ROOT_RELS,
        "docProps/core.xml": CORE,
        "docProps/app.xml": APP,
        "ppt/presentation.xml": presentation_xml(),
        "ppt/_rels/presentation.xml.rels": presentation_rels(),
        "ppt/presProps.xml": PRES_PROPS,
        "ppt/viewProps.xml": VIEW_PROPS,
        "ppt/tableStyles.xml": TABLE_STYLES,
        "ppt/theme/theme1.xml": theme_xml(),
        "ppt/slideMasters/slideMaster1.xml": master_xml(),
        "ppt/slideMasters/_rels/slideMaster1.xml.rels": master_rels(),
    }
    for i, lay in enumerate(D.LAYOUTS):
        parts[f"ppt/slideLayouts/slideLayout{i + 1}.xml"] = layout_xml(lay)
        parts[f"ppt/slideLayouts/_rels/slideLayout{i + 1}.xml.rels"] = layout_rels()

    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        # [Content_Types].xml first, as Office writes it.
        for name, data in parts.items():
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data.encode("utf-8"))
    print(f"wrote {out} ({len(D.LAYOUTS)} layouts)")


def main() -> None:
    here = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=here / "assets" / "academic-template.pptx")
    args = ap.parse_args()
    build(args.out)


if __name__ == "__main__":
    main()
