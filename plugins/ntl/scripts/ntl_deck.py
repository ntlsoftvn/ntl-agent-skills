"""NTL deck library for python-pptx: NTL cover/content layouts and the components of NTL proposal decks.

Canvas 13.333" x 7.5" (1280x720 px at 96 px/in). Colours are hex values from references/brand.md, so the deck needs
no theme post-processing. Needs python-pptx: run `sh scripts/setup_python.sh` once, then run the build script with python3.

    import sys; sys.path.insert(0, "<PLUGIN>/scripts")
    import ntl_deck as ntl
    d = ntl.create_deck(project="RoadVision VN Distribution", doc_type="Proposal", version="2.0", date="10/2026", total=11)
    d.cover(title="RoadVision VN Distribution", subtitle="From AWS to VN Cloud: challenges, solution, roadmap and cost")
    s = d.content("Intro", "Agenda"); ...
    d.save("RoadVision_VN_Distribution_Proposal_v2.0.pptx")

Text content (`d.txt`, `d.box`, `d.table` cells) is a str, or a list of paragraphs. A paragraph is a str, a run dict
(`{"text": ..., "bold": True, "color": H["navy"]}`) or a list of those (several runs in one paragraph).
`d.lead()` and `d.bullets()` return ready-made paragraph lists.
"""
import os
import sys
import uuid

try:
    import pptx  # noqa: F401
except ImportError:  # installed by scripts/setup_python.sh into a cache folder
    for _c in (os.environ.get("NTL_PY_CACHE"),
               os.path.join(os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"), "ntl-agent-skills", "python"),
               os.path.join(os.environ.get("TMPDIR", "/tmp"), "ntl-agent-skills", "python")):
        if _c and os.path.isdir(_c):
            sys.path.insert(0, _c)
    try:
        import pptx  # noqa: F401,F811
    except ImportError:
        sys.exit("python-pptx not found: run  sh <PLUGIN>/scripts/setup_python.sh")

from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.dml import MSO_LINE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE, PP_PLACEHOLDER as PH
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

H = dict(
    navy="14264A", navy2="1F396D", navy3="3B5690", orange="F16D22", orange_text="C9520F",
    bg="F1F4FA", border="D5DBE7", text="1E2637", muted="667085", orange_tint="FDE7D9", note_bg="E9EEF7",
    white="FFFFFF", cover_text="C9D3E6", cover_sub="DCE3F0", grid="B8C2D6", grid_minor="E3E8F1",
)
FONT = "Verdana"  # stand-in for DejaVu Sans (same Bitstream Vera design, ships with Office)
W, HT = 13.333, 7.5
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"

_ALIGN = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}
_VALIGN = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}


def px(v):
    """Template px -> inches."""
    return v / 96


def pt(v):
    """Template px -> points."""
    return v * 0.75


def _in(v):
    return Emu(int(round(v * 914400)))


def _rgb(hex_):
    return RGBColor.from_string(hex_)


def _xml(s):
    return etree.fromstring(s)


# ---------------------------------------------------------------- text

def _norm_runs(p):
    """A paragraph spec -> (list of run dicts, paragraph options)."""
    opts = {}
    if isinstance(p, dict) and "runs" in p:
        opts = {k: v for k, v in p.items() if k != "runs"}
        p = p["runs"]
    if isinstance(p, (str, dict)):
        p = [p]
    return [{"text": r} if isinstance(r, str) else r for r in p], opts


def _fill_text(tf, content, *, size, color, bold=False, font=FONT, align="left", valign="top", space_after=None,
               char_spacing=None, in_cell=False):
    """Write `content` into a text frame with zero margins, no autofit, wrapped."""
    if not in_cell:  # table cells take their margins and anchor from the cell
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.auto_size = MSO_AUTO_SIZE.NONE
        tf.vertical_anchor = _VALIGN[valign]
    tf.word_wrap = True
    paras = [content] if isinstance(content, (dict,)) else content
    if isinstance(paras, str):
        paras = paras.split("\n")
    for i, spec in enumerate(paras):
        runs, popts = _norm_runs(spec)
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = _ALIGN[popts.get("align", align)]
        sa = popts.get("space_after", space_after)
        if sa is not None:
            para.space_after = Pt(sa)
        if popts.get("bullet"):
            ppr = para._p.get_or_add_pPr()
            ppr.set("marL", str(27 * 12700))
            ppr.set("indent", str(-27 * 12700))
            ppr.append(_xml(f'<a:buFont xmlns:a="{NS_A}" typeface="Arial"/>'))
            ppr.append(_xml(f'<a:buChar xmlns:a="{NS_A}" char="●"/>'))
        for r in runs:
            run = para.add_run()
            run.text = r["text"]
            f = run.font
            f.name = r.get("font", font)
            f.size = Pt(r.get("size", size))
            f.bold = r.get("bold", bold)
            f.color.rgb = _rgb(r.get("color", color))
            if char_spacing:
                run._r.get_or_add_rPr().set("spc", str(int(char_spacing * 100)))


def _plain(shape, fill=None, line=None, line_w=0.75, dash=None):
    """Drop the theme style reference (it adds shadows), then set fill and outline explicitly."""
    st = shape._element.find(qn("p:style"))
    if st is not None:
        shape._element.remove(st)
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = _rgb(fill)
    else:
        shape.fill.background()
    if line:
        shape.line.color.rgb = _rgb(line)
        shape.line.width = Pt(line_w)
        if dash:
            shape.line.dash_style = dash
    else:
        shape.line.fill.background()


# ---------------------------------------------------------------- layouts

def _lst_style(size, color, bold, align="l", extra_ppr=""):
    return _xml(
        f'<a:lstStyle xmlns:a="{NS_A}"><a:lvl1pPr marL="0" indent="0" algn="{align}"{extra_ppr}><a:lnSpc><a:spcPct val="100000"/></a:lnSpc>'
        f'<a:spcBef><a:spcPts val="0"/></a:spcBef><a:buNone/>'
        f'<a:defRPr sz="{int(round(size * 100))}" b="{1 if bold else 0}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
        f'<a:latin typeface="+mj-lt"/></a:defRPr></a:lvl1pPr></a:lstStyle>')


def _style_placeholder(sp, x, y, w, h, size, color, bold, anchor):
    """Position a layout placeholder and give it NTL text defaults."""
    sp.left, sp.top, sp.width, sp.height = _in(x), _in(y), _in(w), _in(h)
    tx = sp._element.txBody
    body = tx.find(qn("a:bodyPr"))
    for k, v in dict(lIns="0", tIns="0", rIns="0", bIns="0", anchor=anchor).items():
        body.set(k, v)
    for c in list(body):
        body.remove(c)
    body.append(_xml(f'<a:noAutofit xmlns:a="{NS_A}"/>'))
    old = tx.find(qn("a:lstStyle"))
    new = _lst_style(size, color, bold)
    if old is not None:
        tx.replace(old, new)
    else:
        body.addnext(new)


def _layout_shape_xml(shape_id, name, x, y, w, h, fill=None, text=None):
    geom = '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
    fill_xml = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else "<a:noFill/>"
    body = ""
    if text:
        body = (f'<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0"><a:noAutofit/></a:bodyPr><a:lstStyle/>'
                f'<a:p><a:r><a:rPr lang="en-US" sz="{int(round(pt(13) * 100))}"><a:solidFill><a:srgbClr val="{H["muted"]}"/></a:solidFill>'
                f'<a:latin typeface="{FONT}"/></a:rPr><a:t>{text}</a:t></a:r></a:p></p:txBody>')
    return _xml(
        f'<p:sp xmlns:p="{NS_P}" xmlns:a="{NS_A}"><p:nvSpPr><p:cNvPr id="{shape_id}" name="{name}"/><p:cNvSpPr/><p:nvPr userDrawn="1"/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{_in(x)}" y="{_in(y)}"/><a:ext cx="{_in(w)}" cy="{_in(h)}"/></a:xfrm>{geom}{fill_xml}<a:ln><a:noFill/></a:ln></p:spPr>{body}</p:sp>')


def _scale_to_wide(prs):
    k = W / 10.0
    for holder in [prs.slide_master] + list(prs.slide_layouts):
        for sh in holder.shapes:
            if sh.left is not None:
                sh.left, sh.width = int(sh.left * k), int(sh.width * k)


def _set_theme_fonts(prs):
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT
    theme = prs.slide_master.part.part_related_by(RT.THEME)
    root = etree.fromstring(theme.blob)
    for tag in ("majorFont", "minorFont"):
        el = root.find(f".//{{{NS_A}}}{tag}/{{{NS_A}}}latin")
        if el is not None:
            el.set("typeface", FONT)
    theme._blob = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def _build_layouts(prs, footer):
    """Keep two layouts, NTL_COVER and NTL_CONTENT, with their title/subtitle placeholders, rule and footer."""
    _scale_to_wide(prs)
    keep = {0: "NTL_COVER", 5: "NTL_CONTENT"}
    layouts = list(prs.slide_layouts)
    for i, lay in enumerate(layouts):
        if i not in keep:
            prs.slide_layouts.remove(lay)
    cover, content = [prs.slide_layouts[0], prs.slide_layouts[1]]
    cover._element.cSld.set("name", "NTL_COVER")
    content._element.cSld.set("name", "NTL_CONTENT")
    for lay in (cover, content):  # date / footer / slide-number placeholders are not used
        for sh in list(lay.placeholders):
            if sh.placeholder_format.type in (PH.DATE, PH.FOOTER, PH.SLIDE_NUMBER):
                sh._element.getparent().remove(sh._element)
    # cover: navy background, title + subtitle placeholders
    cover._element.cSld.insert(0, _xml(f'<p:bg xmlns:p="{NS_P}" xmlns:a="{NS_A}"><p:bgPr><a:solidFill><a:srgbClr val="{H["navy"]}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>'))
    for sh in cover.placeholders:
        t = sh.placeholder_format.type
        if t == PH.CENTER_TITLE:
            _style_placeholder(sh, px(96), 2.15, px(960), 1.55, pt(54), H["white"], True, "b")
        elif t == PH.SUBTITLE:
            _style_placeholder(sh, px(96), 4.15, px(1060), 0.9, pt(28), H["cover_sub"], False, "t")
    # content: title, orange rule, footer
    for sh in content.placeholders:
        if sh.placeholder_format.type == PH.TITLE:
            _style_placeholder(sh, px(80), px(56), px(1120), 0.6, pt(38), H["navy2"], True, "b")
    tree = content.shapes._spTree
    tree.append(_layout_shape_xml(90, "title-rule", px(80), px(56) + 0.68, px(84), px(4), fill=H["orange"]))
    tree.append(_layout_shape_xml(91, "footer", px(80), HT - px(26) - 0.2, 8, 0.2, text=footer))
    return cover, content


# ---------------------------------------------------------------- deck

class Deck:
    def __init__(self, project, doc_type, version, date, total, author, footer):
        self.project, self.doc_type, self.version, self.date, self.total = project, doc_type, version, date, total
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = _in(W), _in(HT)
        _set_theme_fonts(self.prs)
        cp = self.prs.core_properties
        cp.title, cp.author, cp.last_modified_by = project or "NTL document", author, author
        self.footer = footer or f"NTL Software  ·  {project}  ·  {doc_type}"
        self.cover_layout, self.content_layout = _build_layouts(self.prs, self.footer)
        self.H, self.FONT, self.W, self.HT = H, FONT, W, HT
        self.X0, self.XW, self.Y0 = px(80), W - 2 * px(80), 1.5  # content box
        self.px, self.pt = px, pt
        self._page = 0
        self._section = None
        self._sections = []  # [(title, [slide ids])]

    # ---- primitives

    def shape(self, s, kind, x, y, w, h, *, fill=None, line=None, line_w=0.75, dash=None, name=None, radius=None, rotate=0, flip_h=False):
        sh = s.shapes.add_shape(kind, _in(x), _in(y), _in(w), _in(h))
        _plain(sh, fill, line, line_w, dash)
        if radius is not None:
            sh.adjustments[0] = min(radius / min(w, h), 0.5)
        if rotate:
            sh.rotation = rotate
        if flip_h:
            sh._element.spPr.find(qn("a:xfrm")).set("flipH", "1")
        if name:
            sh.name = name
        return sh

    def rect(self, s, x, y, w, h, **o):
        return self.shape(s, MSO_SHAPE.RECTANGLE, x, y, w, h, **o)

    def rounded(self, s, x, y, w, h, radius, **o):
        return self.shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, radius=radius, **o)

    def oval(self, s, x, y, w, h, **o):
        return self.shape(s, MSO_SHAPE.OVAL, x, y, w, h, **o)

    def hline(self, s, x, y, w, color, width=0.75, dash=None, name=None):
        return self.line(s, x, y, x + w, y, color, width, dash, name)

    def line(self, s, x1, y1, x2, y2, color, width=0.75, dash=None, name=None):
        c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, _in(x1), _in(y1), _in(x2), _in(y2))
        st = c._element.find(qn("p:style"))
        if st is not None:
            c._element.remove(st)
        c.line.color.rgb = _rgb(color)
        c.line.width = Pt(width)
        if dash:
            c.line.dash_style = dash
        if name:
            c.name = name
        return c

    def txt(self, s, text, *, x, y, w, h, size=14, color=H["text"], bold=False, align="left", valign="top",
            space_after=None, char_spacing=None, name=None):
        tb = s.shapes.add_textbox(_in(x), _in(y), _in(w), _in(h))
        _fill_text(tb.text_frame, text, size=size, color=color, bold=bold, align=align, valign=valign,
                   space_after=space_after, char_spacing=char_spacing)
        if name:
            tb.name = name
        return tb

    # ---- NTL components

    def card(self, s, x, y, w, h, name, top=H["navy2"], bg=H["bg"]):
        """Light background, 1px border, 6px top bar (navy, or orange for emphasis), radius 12px."""
        self.rounded(s, x, y, w, h, px(12), fill=bg, line=H["border"], name=name)
        self.rounded(s, x, y, w, px(14), px(6), fill=top, line=top, name=name + "-top")
        self.rect(s, x, y + px(6), w, px(8), fill=bg, line=bg, name=name + "-mask")

    def box(self, s, x, y, w, h, kind, name, text=None, **o):
        """Note (blue) / callout (orange): tinted box with a 6px left bar. Pass text to fill it."""
        bg, bar = (H["orange_tint"], H["orange"]) if kind == "callout" else (H["note_bg"], H["navy2"])
        self.rect(s, x, y, w, h, fill=bg, line=bg, name=name)
        self.rect(s, x, y, px(6), h, fill=bar, line=bar, name=name + "-bar")
        if text is not None:
            o = {"size": pt(19), "valign": "middle", **o}
            self.txt(s, text, x=x + 0.25, y=y, w=w - 0.4, h=h, **o)

    @staticmethod
    def lead(label, rest, color=H["orange_text"]):
        """Bold coloured label + normal text in one paragraph: d.lead("Reference cost: ", "public price lists...")"""
        return [[{"text": label, "bold": True, "color": color}, {"text": rest}]]

    @staticmethod
    def bullets(items):
        return [{"runs": [t], "bullet": True} for t in items]

    def page_no(self, s, n):
        self.txt(s, f"{n} / {self.total}", x=W - px(80) - 1.0, y=HT - px(24) - 0.22, w=1.0, h=0.22, size=pt(15), bold=True,
                 color=H["orange"], align="right", name="page-number")

    def section(self, title):
        self._section = title
        self._sections.append((title, []))

    def _new_slide(self, layout):
        s = self.prs.slides.add_slide(layout)
        if self._sections:
            self._sections[-1][1].append(s.slide_id)
        return s

    def content(self, sec, title):
        """Title + orange rule + footer (from the layout) + "N / total"."""
        if sec and sec != self._section:
            self.section(sec)
        s = self._new_slide(self.content_layout)
        s.shapes.title.text_frame.text = title
        self._page += 1
        self.page_no(s, self._page + 1)
        return s

    def cover(self, title=None, subtitle=None, kicker=None, version_label="Version", logo=True, section_title="Intro"):
        self.section(section_title)
        s = self._new_slide(self.cover_layout)
        kicker = kicker or f"NTL SOFTWARE  ·  {self.doc_type.upper()}"
        self.shape(s, MSO_SHAPE.RIGHT_TRIANGLE, W - px(360), 0, px(360), px(360), fill=H["orange"], line=H["orange"], rotate=180, name="tri-orange")
        self.shape(s, MSO_SHAPE.RIGHT_TRIANGLE, W - px(260), HT - px(260), px(260), px(260), fill=H["navy3"], line=H["navy3"], flip_h=True, name="tri-navy")
        if logo:
            lw = 1.4
            s.shapes.add_picture(os.path.join(ASSETS, "logo-white.png"), _in(px(96)), _in(0.55), _in(lw), _in(lw * 474 / 738)).name = "logo"
        self.txt(s, kicker, x=px(96), y=1.7, w=8, h=0.3, size=pt(16), color=H["cover_text"], char_spacing=4)
        s.shapes.title.text_frame.text = title or self.project
        self.rect(s, px(96), 3.85, px(110), px(4), fill=H["orange"], line=H["orange"], name="cover-rule")
        sub = [p for p in s.placeholders if p.placeholder_format.idx == 1][0]
        if subtitle:
            sub.text_frame.text = subtitle
        else:
            sub._element.getparent().remove(sub._element)
        runs = [{"text": f"{version_label} {self.version}", "bold": True, "color": H["white"]}]
        if self.date:
            runs.append({"text": f"  ·  {self.date}", "color": H["cover_text"]})
        self.txt(s, [runs], x=px(96), y=HT - px(56) - 0.25, w=6, h=0.25, size=pt(16))
        return s

    def agenda(self, items, title="Agenda", sec="Intro"):
        """Numbered agenda: [[title, page], ...]"""
        s = self.content(sec, title)
        X0, XW = self.X0, self.XW
        for i, (t, p) in enumerate(items):
            y = self.Y0 + 0.1 + i * 0.68
            self.txt(s, str(i + 1).zfill(2), x=X0, y=y, w=0.9, h=0.55, size=pt(34), bold=True, color=H["orange"], valign="middle")
            self.txt(s, t, x=X0 + 1.0, y=y, w=8.0, h=0.55, size=pt(26), bold=True, color=H["navy2"], valign="middle")
            self.txt(s, f"p. {p}", x=10.9, y=y, w=1.6, h=0.55, size=pt(20), color=H["muted"], align="right", valign="middle")
            if i < len(items) - 1:
                self.hline(s, X0, y + 0.62, XW, H["border"], name=f"agenda-line-{i}")
        return s

    def numbered(self, s, items, *, x=9.35, y=None, w=3.0, step=1.27, color=H["navy2"], title_size=pt(19), text_size=pt(17)):
        """Numbered points beside a diagram: [[title, text], ...]"""
        y = self.Y0 if y is None else y
        for i, (t, body) in enumerate(items):
            yy = y + i * step
            self.oval(s, x, yy + 0.05, 0.38, 0.38, fill=color, line=color, name=f"num-{i}")
            self.txt(s, str(i + 1), x=x, y=yy + 0.05, w=0.38, h=0.38, size=12, bold=True, color=H["white"], align="center", valign="middle")
            self.txt(s, t, x=x + 0.52, y=yy, w=w, h=0.45, size=title_size, bold=True, color=H["navy2"], valign="middle")
            self.txt(s, body, x=x + 0.52, y=yy + 0.48, w=w, h=step - 0.52, size=text_size)

    def image(self, s, file, *, x=None, y=None, w=8.2, h=5.06, name="image"):
        """Image, or a labelled placeholder box when the file is missing (so the example deck builds anywhere)."""
        x = self.X0 if x is None else x
        y = self.Y0 if y is None else y
        if file and os.path.exists(file):
            s.shapes.add_picture(file, _in(x), _in(y), _in(w), _in(h)).name = name
            return
        self.rect(s, x, y, w, h, fill=H["bg"], line=H["border"], line_w=1, dash=MSO_LINE.DASH, name=name + "-placeholder")
        self.txt(s, f"Diagram: {os.path.basename(file) if file else name}", x=x, y=y, w=w, h=h, align="center", valign="middle",
                 color=H["muted"], size=14)

    def table(self, s, header, rows, *, x=None, y=None, w=None, col_w=None, row_h=0.72, head_h=0.5, size=pt(19), name="table"):
        """Table with a navy header row and thin row rules; first column bold navy."""
        x = self.X0 if x is None else x
        y = self.Y0 if y is None else y
        w = self.XW if w is None else w
        nr, nc = len(rows) + 1, len(header)
        total_h = head_h + row_h * len(rows)
        gf = s.shapes.add_table(nr, nc, _in(x), _in(y), _in(w), _in(total_h))
        gf.name = name
        tbl = gf.table
        tblPr = tbl._tbl.tblPr
        for a in ("firstRow", "bandRow"):
            tblPr.set(a, "0")
        sid = tblPr.find(qn("a:tableStyleId"))
        if sid is not None:
            tblPr.remove(sid)
        col_w = col_w or [w / nc] * nc
        for i, cw in enumerate(col_w):
            tbl.columns[i].width = _in(cw)
        tbl.rows[0].height = _in(head_h)
        for r in range(1, nr):
            tbl.rows[r].height = _in(row_h)

        def put(cell, text, *, bold, color, fsize, fill=None, rule=True):
            cell.margin_left = cell.margin_right = _in(0.15)
            cell.margin_top = cell.margin_bottom = _in(0.08)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            _fill_text(cell.text_frame, text, size=fsize, color=color, bold=bold, in_cell=True)
            tcPr = cell._tc.get_or_add_tcPr()
            for side in ("lnL", "lnR", "lnT"):
                tcPr.append(_xml(f'<a:{side} xmlns:a="{NS_A}" w="0"><a:noFill/></a:{side}>'))
            tcPr.append(_xml(f'<a:lnB xmlns:a="{NS_A}" w="9525"><a:solidFill><a:srgbClr val="{H["border"]}"/></a:solidFill></a:lnB>'))
            if fill:
                tcPr.append(_xml(f'<a:solidFill xmlns:a="{NS_A}"><a:srgbClr val="{fill}"/></a:solidFill>'))
            else:
                tcPr.append(_xml(f'<a:noFill xmlns:a="{NS_A}"/>'))

        for c, t in enumerate(header):
            put(tbl.cell(0, c), t, bold=True, color=H["white"], fsize=pt(20), fill=H["navy2"])
        for r, row in enumerate(rows, start=1):
            for c, t in enumerate(row):
                put(tbl.cell(r, c), t, bold=c == 0, color=H["navy2"] if c == 0 else H["text"], fsize=size)
        return gf

    def stats(self, s, items, *, y=4.85, x=None, w=None, gap=px(24)):
        """Big stats: [[value, label], ...] in equal columns."""
        x = self.X0 if x is None else x
        w = self.XW if w is None else w
        cw = (w - (len(items) - 1) * gap) / len(items)
        for i, (v, label) in enumerate(items):
            xx = x + i * (cw + gap)
            self.txt(s, v, x=xx, y=y, w=cw, h=0.85, size=pt(48), bold=True, color=H["orange"], valign="bottom")
            self.txt(s, label, x=xx, y=y + 0.9, w=cw, h=0.4, size=pt(20), color=H["navy3"])

    def gantt(self, s, *, weeks=20, block=4, phases=(), x=None, y=None, tx=6.6, tw=5.0, row_h=0.56):
        """Roadmap Gantt: phases [[name, team, from_week, to_week, md, color?, optional?]]; vertical week grid, strong line
        every `block` weeks (labelled W1, W5, ...), MD column on the right. Returns the y below the last row."""
        x = self.X0 if x is None else x
        y = self.Y0 if y is None else y
        wk = tw / weeks
        self.txt(s, "Phase", x=x, y=y, w=2.9, h=0.3, size=11, bold=True, color=H["muted"])
        self.txt(s, "Proposed team", x=3.85, y=y, w=2.7, h=0.3, size=11, bold=True, color=H["muted"])
        self.txt(s, "MD", x=11.75, y=y, w=0.75, h=0.3, size=11, bold=True, color=H["muted"], align="right")
        for wi in range(1, weeks + 1, block):
            self.txt(s, f"W{wi}", x=tx + (wi - 1) * wk, y=y, w=0.5, h=0.3, size=10, color=H["muted"])
        top, bottom = y + 0.32, y + 0.4 + len(phases) * row_h - 0.04
        for wi in range(weeks + 1):
            major = wi % block == 0
            self.line(s, tx + wi * wk, top, tx + wi * wk, bottom, H["grid"] if major else H["grid_minor"],
                      0.75 if major else 0.5, None if major else MSO_LINE.DASH, name=f"week-grid-{wi}")
        for i, ph in enumerate(phases):
            name, team, a, b, md = ph[:5]
            color = ph[5] if len(ph) > 5 else None
            optional = ph[6] if len(ph) > 6 else False
            yy = y + 0.4 + i * row_h
            c = color or ("F7B48A" if optional else H["navy2"])
            self.hline(s, x, yy + row_h - 0.04, self.XW, H["border"], name=f"row-line-{i}")
            self.txt(s, name, x=x, y=yy, w=3.0, h=0.5, size=pt(18), bold=not optional, valign="middle", color=H["muted"] if optional else H["navy2"])
            self.txt(s, team, x=3.85, y=yy, w=2.7, h=0.5, size=pt(17), valign="middle")
            self.rounded(s, tx + (a - 1) * wk, yy + 0.11, (b - a + 1) * wk, 0.28, 0.05, fill=c, line=c, name=f"bar-{i}")
            self.txt(s, str(md), x=11.75, y=yy, w=0.75, h=0.5, size=pt(18), bold=True, align="right", valign="middle",
                     color=H["muted"] if optional else H["navy2"])
        return y + 0.4 + len(phases) * row_h

    def bar_chart(self, s, *, labels, values, title=None, x=7.15, y=None, w=5.35, h=5.05, fmt="0.0", name="chart"):
        """Horizontal bar chart (native, single series)."""
        y = self.Y0 if y is None else y
        cd = CategoryChartData()
        cd.categories = labels
        cd.add_series(title or "values", values)
        gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, _in(x), _in(y), _in(w), _in(h), cd)
        gf.name = name
        ch = gf.chart
        ch.has_legend = False
        ch.font.name, ch.font.size, ch.font.color.rgb = FONT, Pt(11), _rgb(H["text"])
        if title:
            ch.has_title = True
            tf = ch.chart_title.text_frame
            tf.text = title
            r = tf.paragraphs[0].runs[0]
            r.font.name, r.font.size, r.font.bold, r.font.color.rgb = FONT, Pt(13), False, _rgb(H["navy2"])
            ch.chart_title.include_in_layout = False
        else:
            ch.has_title = False
        plot = ch.plots[0]
        plot.gap_width = 60
        plot.vary_by_categories = False
        ser = plot.series[0]
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = _rgb(H["navy2"])
        plot.has_data_labels = True
        dl = plot.data_labels
        dl.show_value = True
        dl.number_format, dl.number_format_is_linked = fmt, False
        dl.position = XL_LABEL_POSITION.OUTSIDE_END
        dl.font.name, dl.font.size, dl.font.color.rgb = FONT, Pt(11), _rgb(H["text"])
        cat, val = ch.category_axis, ch.value_axis
        cat.reverse_order = True
        cat.has_major_gridlines = False
        cat.format.line.fill.background()
        cat.tick_labels.font.size = Pt(11)
        val.visible = False
        val._element.find(qn("c:delete")).set("val", "1")
        val.has_major_gridlines = False
        return gf

    def icon_circle(self, s, png, x, y, dia, fill=H["navy2"], name="icon"):
        """Icon (a PNG with a transparent background, e.g. a white glyph) in a filled circle."""
        self.oval(s, x, y, dia, dia, fill=fill, line=fill, name=name + "-c")
        p = dia * 0.25
        s.shapes.add_picture(png, _in(x + p), _in(y + p), _in(dia - 2 * p), _in(dia - 2 * p)).name = name + "-i"

    def page_count(self):
        return self._page + 1

    def _write_sections(self):
        pres = self.prs.part._element
        ids = ",".join(f'<p14:section name="{t}" id="{{{str(uuid.uuid4()).upper()}}}"><p14:sldIdLst>'
                       + "".join(f'<p14:sldId id="{i}"/>' for i in ids_) + "</p14:sldIdLst></p14:section>"
                       for t, ids_ in self._sections if ids_).replace("</p14:section>,", "</p14:section>")
        ext = _xml(f'<p:ext xmlns:p="{NS_P}" uri="{{521415D9-36F7-43E2-AB2F-B90AF26B5E84}}"><p14:sectionLst xmlns:p14="{NS_P14}">{ids}</p14:sectionLst></p:ext>')
        lst = pres.find(qn("p:extLst"))
        if lst is None:
            lst = etree.SubElement(pres, qn("p:extLst"))
        lst.append(ext)

    def save(self, out):
        if self.total and self.page_count() != self.total:
            print(f'! total is {self.total} but the deck has {self.page_count()} slides: fix "N / total"')
        self._write_sections()
        self.prs.save(out)
        print("written", out)


def create_deck(project="", doc_type="Proposal", version="1.0", date="", total=None, author="NTL Software", footer=None):
    return Deck(project, doc_type, version, date, total, author, footer)
