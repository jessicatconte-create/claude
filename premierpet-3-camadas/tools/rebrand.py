"""Rebrand PremieRpet_3_Camadas_v14 with the visual identity of
[PremieRpet] Piloto [Revisão] v2.

usage: python rebrand.py <target_unpacked_dir> <reference_unpacked_dir>
Works in place on the target dir.
"""
import os
import re
import shutil
import sys
import subprocess
from copy import deepcopy

from lxml import etree
from PIL import ImageFont

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PR = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"a": A, "p": P, "r": R}
EMU = 914400
IMG_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"

TGT, REF = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
MEDIA = os.path.join(TGT, "ppt", "media")
SLIDES = os.path.join(TGT, "ppt", "slides")

# ---------------------------------------------------------------- palette
INK = "14171F"
BLUE = "1A56DB"
NAVY_DEEP = "0A1D5C"
BG = "F5F5F3"
CARD_LINE = "E5E7EB"
GREY_TXT = "888D97"
HEAD_TXT = "9CA3AF"
RULE = "D1D5DB"
ROW_RULE = "EEF0F2"

FILL_MAP = {
    "1F3864": BLUE, "203965": BLUE, "2A4470": BLUE, "30466D": BLUE,
    "3F6FB5": "7BA0EA", "2F5A9E": "4F7FE3", "4776B8": "5F8BE6",
    "8FB4DC": "C3D3F5", "8FA9CF": "C3D3F5", "9CB4D8": "C3D3F5",
    "EAF1FA": "E8EEFB", "EAF1F8": "E8EEFB", "E3ECF8": "E8EEFB", "D6E2F5": "DBE6FB",
    "F7F9FC": "F4F5F7", "F3F5F9": "F4F5F7", "F1F5FA": "F4F5F7", "F3F7FB": "F4F5F7",
    "E3E9F2": ROW_RULE, "E3E7EE": ROW_RULE, "D5DBE6": RULE, "D0D7E2": RULE, "B8BFCC": "C7CBD1",
    "7A2018": "C62828", "B3372B": "C62828",
}
TEXT_MAP = {
    "1F3864": INK, "203965": INK, "2A4470": INK,
    "3F6FB5": BLUE,
    "8C8C8C": GREY_TXT, "7B8089": GREY_TXT, "7F7F7F": GREY_TXT, "A6A6A6": HEAD_TXT,
    "595959": "5B6472", "3A4558": "5B6472", "4A5A75": "5B6472", "5A6B85": "5B6472",
    "404040": INK,
    "7A2018": "C62828", "B3372B": "C62828",
}
LIGHT_CARD_FILLS = {"F7F9FC", "F3F5F9", "EAF1FA", "EAF1F8", "F1F5FA", "E3ECF8"}
ORANGE_CARD_FILLS = {"FFF4EC", "FFF1E3", "FFF6F0"}
WHITE_TXT = {"FFFFFF", "DCE6F4"}
NAVY = {"1F3864", "203965", "2A4470"}
ORANGE = {"FF6E08", "E07B1A", "C55A11"}

CHART_PNGS = {f"image{n}.png" for n in range(7, 22) if n not in (6,)}
LOGO_PNGS = {"image1.png", "image2.png", "image3.png", "image4.png", "image5.png"}

FONT_B = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 1000)

HIDDEN_SLIDES = set()


def q(tag):
    pre, t = tag.split(":")
    return "{%s}%s" % (NS[pre], t)


def emu(inches):
    return int(round(inches * EMU))


# ---------------------------------------------------------------- shapes
def xfrm(el):
    x = el.find("./p:spPr/a:xfrm", NS)
    if x is None:
        x = el.find("./p:xfrm", NS)
    return x


def geom(el):
    x = xfrm(el)
    if x is None:
        return None
    o, e = x.find("a:off", NS), x.find("a:ext", NS)
    return [int(o.get("x")) / EMU, int(o.get("y")) / EMU, int(e.get("cx")) / EMU, int(e.get("cy")) / EMU]


def set_geom(el, g):
    x = xfrm(el)
    o, e = x.find("a:off", NS), x.find("a:ext", NS)
    o.set("x", str(emu(g[0])))
    o.set("y", str(emu(g[1])))
    e.set("cx", str(emu(g[2])))
    e.set("cy", str(emu(g[3])))


def text_of(el):
    return "".join(el.xpath(".//a:t/text()", namespaces=NS))


def runs(el):
    return el.xpath(".//a:r/a:rPr", namespaces=NS)


def max_sz(el):
    s = [int(r.get("sz")) for r in el.xpath(".//a:rPr[@sz]", namespaces=NS)]
    return max(s) if s else 0


def fill_of(el):
    c = el.find("./p:spPr/a:solidFill/a:srgbClr", NS)
    return c.get("val").upper() if c is not None else None


def set_solid_fill(sppr, val, after=("a:prstGeom", "a:custGeom")):
    for tag in ("a:solidFill", "a:noFill", "a:gradFill"):
        for f in sppr.findall(tag, NS):
            sppr.remove(f)
    new = etree.SubElement(sppr, q("a:noFill") if val is None else q("a:solidFill"))
    if val is not None:
        etree.SubElement(new, q("a:srgbClr")).set("val", val)
    # position right after geometry
    sppr.remove(new)
    idx = 0
    for i, ch in enumerate(sppr):
        if etree.QName(ch).localname in ("xfrm", "prstGeom", "custGeom"):
            idx = i + 1
    sppr.insert(idx, new)


def set_line(sppr, val, w=9525):
    for ln in sppr.findall("a:ln", NS):
        sppr.remove(ln)
    ln = etree.Element(q("a:ln"))
    if val is None:
        etree.SubElement(ln, q("a:noFill"))
    else:
        ln.set("w", str(w))
        sf = etree.SubElement(ln, q("a:solidFill"))
        etree.SubElement(sf, q("a:srgbClr")).set("val", val)
    # a:ln goes after fill, before effectLst etc
    idx = 0
    for i, ch in enumerate(sppr):
        if etree.QName(ch).localname in ("xfrm", "prstGeom", "custGeom", "noFill", "solidFill", "gradFill", "blipFill", "pattFill", "grpFill"):
            idx = i + 1
    sppr.insert(idx, ln)


def round_corners(el, radius_in=0.12):
    g = geom(el)
    pg = el.find("./p:spPr/a:prstGeom", NS)
    if pg is None or g is None:
        return
    pg.set("prst", "roundRect")
    av = pg.find("a:avLst", NS)
    if av is None:
        av = etree.SubElement(pg, q("a:avLst"))
    for gd in list(av):
        av.remove(gd)
    adj = int(min(50000, radius_in / max(min(g[2], g[3]), 0.01) * 100000))
    gd = etree.SubElement(av, q("a:gd"))
    gd.set("name", "adj")
    gd.set("fmla", "val %d" % adj)


def set_run_color(rpr, val):
    for tag in ("a:solidFill", "a:noFill", "a:gradFill"):
        for f in rpr.findall(tag, NS):
            rpr.remove(f)
    sf = etree.Element(q("a:solidFill"))
    etree.SubElement(sf, q("a:srgbClr")).set("val", val)
    # solidFill must precede latin/ea/cs etc; after a:ln if present
    idx = 0
    for i, ch in enumerate(rpr):
        if etree.QName(ch).localname == "ln":
            idx = i + 1
    rpr.insert(idx, sf)


def run_color(rpr):
    c = rpr.find("./a:solidFill/a:srgbClr", NS)
    return c.get("val").upper() if c is not None else None


def center_in(inner, outer, tol=0.02):
    cx, cy = inner[0] + inner[2] / 2, inner[1] + inner[3] / 2
    return outer[0] - tol <= cx <= outer[0] + outer[2] + tol and outer[1] - tol <= cy <= outer[1] + outer[3] + tol


_next_id = [5000]


def nid():
    _next_id[0] += 1
    return str(_next_id[0])


def mk_sp(name, g, fill=None, line=None, line_w=9525, prst="rect", radius=None):
    sp = etree.fromstring(
        f'<p:sp xmlns:p="{P}" xmlns:a="{A}"><p:nvSpPr><p:cNvPr id="{nid()}" name="{name}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/></a:xfrm><a:prstGeom prst="{prst}"><a:avLst/></a:prstGeom></p:spPr>'
        f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="pt-BR"/></a:p></p:txBody></p:sp>')
    set_geom(sp, g)
    sppr = sp.find("p:spPr", NS)
    set_solid_fill(sppr, fill)
    set_line(sppr, line, line_w)
    if radius:
        round_corners(sp, radius)
    return sp


def mk_text(name, g, paras, anchor="t", wrap="square", algn="l", inset=0.0):
    """paras: list of list of runs (text, dict(sz, b, i, color, spc))"""
    ins = str(emu(inset))
    sp = etree.fromstring(
        f'<p:sp xmlns:p="{P}" xmlns:a="{A}"><p:nvSpPr><p:cNvPr id="{nid()}" name="{name}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
        f'<p:txBody><a:bodyPr wrap="{wrap}" lIns="{ins}" tIns="{ins}" rIns="{ins}" bIns="{ins}" rtlCol="0" anchor="{anchor}"><a:noAutofit/></a:bodyPr><a:lstStyle/></p:txBody></p:sp>')
    set_geom(sp, g)
    tb = sp.find("p:txBody", NS)
    for para in paras:
        p_ = etree.SubElement(tb, q("a:p"))
        ppr = etree.SubElement(p_, q("a:pPr"))
        ppr.set("algn", algn)
        lsp = para[0][1].get("lnSpc") if para else None
        if lsp:
            ls = etree.SubElement(ppr, q("a:lnSpc"))
            etree.SubElement(ls, q("a:spcPct")).set("val", str(lsp))
        etree.SubElement(ppr, q("a:buNone"))
        for txt, o in para:
            r = etree.SubElement(p_, q("a:r"))
            rpr = etree.SubElement(r, q("a:rPr"))
            rpr.set("lang", "pt-BR")
            rpr.set("sz", str(o.get("sz", 1350)))
            if o.get("b"):
                rpr.set("b", "1")
            if o.get("i"):
                rpr.set("i", "1")
            if o.get("spc"):
                rpr.set("spc", str(o["spc"]))
            rpr.set("dirty", "0")
            sf = etree.SubElement(rpr, q("a:solidFill"))
            c = etree.SubElement(sf, q("a:srgbClr"))
            c.set("val", o.get("color", INK))
            if o.get("alpha"):
                etree.SubElement(c, q("a:alpha")).set("val", str(o["alpha"]))
            for t in ("latin", "ea", "cs"):
                etree.SubElement(rpr, q("a:" + t)).set("typeface", "Arial")
            etree.SubElement(r, q("a:t")).text = txt
    return sp


def mk_pic(name, rid, g):
    pic = etree.fromstring(
        f'<p:pic xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}"><p:nvPicPr><p:cNvPr id="{nid()}" name="{name}" descr="{name}"/>'
        f'<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
        f'<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
        f'<p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')
    set_geom(pic, g)
    return pic


# ---------------------------------------------------------------- rels
class Rels:
    def __init__(self, path):
        self.path = path
        self.tree = etree.parse(path)
        self.root = self.tree.getroot()

    def target(self, rid):
        for r in self.root:
            if r.get("Id") == rid:
                return r.get("Target")

    def add_image(self, fname):
        for r in self.root:
            if r.get("Target") == "../media/" + fname:
                return r.get("Id")
        ids = {r.get("Id") for r in self.root}
        n = 1
        while f"rId{n}" in ids:
            n += 1
        el = etree.SubElement(self.root, "{%s}Relationship" % PR)
        el.set("Id", f"rId{n}")
        el.set("Type", IMG_REL)
        el.set("Target", "../media/" + fname)
        return f"rId{n}"

    def drop_unused(self, slide_root):
        used = set(slide_root.xpath("//@r:embed | //@r:id | //@r:link", namespaces=NS))
        for r in list(self.root):
            if r.get("Type") == IMG_REL and r.get("Id") not in used:
                self.root.remove(r)

    def save(self):
        self.tree.write(self.path, xml_declaration=True, encoding="UTF-8", standalone=True)


# ---------------------------------------------------------------- brand chrome
RIGHT = 19.17  # target content right edge (in)
LEFT = 0.83


def add_logos(tree_el, rels, dark_bg, y0):
    """PremieRpet | DOC lockup, right aligned like the reference."""
    doc_w, doc_h = 1.7056, 0.2708
    pr_w, pr_h = (1.1851, 0.3125) if not dark_bg else (2.2642, 0.4167)
    if dark_bg:
        doc_w, doc_h = 2.2305, 0.3542
    gap = 0.229
    doc_x = RIGHT - doc_w
    div_x = doc_x - gap - 0.0104
    pr_x = div_x - gap - pr_w
    pr = rels.add_image("brand_premier_w.png" if dark_bg else "brand_premier.png")
    dc = rels.add_image("brand_doc_w.png" if dark_bg else "brand_doc.png")
    mid = y0 + max(pr_h, doc_h) / 2
    els = [
        mk_pic("Logo PremieRpet", pr, [pr_x, mid - pr_h / 2, pr_w, pr_h]),
        mk_sp("Divisor logos", [div_x, mid - 0.15, 0.0104, 0.30], fill="FFFFFF" if dark_bg else RULE),
        mk_pic("Logo DOC Consulting", dc, [doc_x, mid - doc_h / 2, doc_w, doc_h]),
    ]
    if dark_bg:
        a = els[1].find(".//a:srgbClr", NS)
        etree.SubElement(a, q("a:alpha")).set("val", "30000")
    for e in els:
        tree_el.append(e)
    return pr_x


def set_bg(root, color):
    csld = root.find("p:cSld", NS)
    for bg in csld.findall("p:bg", NS):
        csld.remove(bg)
    bg = etree.fromstring(f'<p:bg xmlns:p="{P}" xmlns:a="{A}"><p:bgPr><a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>')
    csld.insert(0, bg)


def gradient_rect():
    return etree.fromstring(
        f'<p:sp xmlns:p="{P}" xmlns:a="{A}"><p:nvSpPr><p:cNvPr id="{nid()}" name="Fundo gradiente"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="18288000" cy="10287000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f'<a:gradFill rotWithShape="1"><a:gsLst><a:gs pos="0"><a:srgbClr val="050E2A"/></a:gs><a:gs pos="55000"><a:srgbClr val="0A1D5C"/></a:gs>'
        f'<a:gs pos="100000"><a:srgbClr val="0E2F8A"/></a:gs></a:gsLst><a:lin ang="2700000" scaled="0"/></a:gradFill><a:ln><a:noFill/></a:ln></p:spPr>'
        f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="pt-BR"/></a:p></p:txBody></p:sp>')


def title_width(txt, sz, spc):
    return FONT_B.getlength(txt) / 1000 * sz / 100 / 72 + len(txt) * spc / 100 / 72


# ---------------------------------------------------------------- per slide
def top_children(sptree):
    return [c for c in sptree if etree.QName(c).localname in ("sp", "pic", "graphicFrame", "grpSp", "cxnSp")]


def process_content(i, root, rels):
    sptree = root.find(".//p:spTree", NS)
    set_bg(root, BG)

    # 1. drop old logos
    for pic in sptree.findall("p:pic", NS):
        blip = pic.find(".//a:blip", NS)
        tgt = os.path.basename(rels.target(blip.get(q("r:embed"))) or "")
        if tgt in LOGO_PNGS:
            sptree.remove(pic)

    kids = top_children(sptree)
    on = [k for k in kids if geom(k) and geom(k)[1] >= 0 and geom(k)[0] < 20]

    # 2. title
    cands = [k for k in on if etree.QName(k).localname == "sp" and 0.3 <= geom(k)[1] <= 1.3 and max_sz(k) >= 2600 and text_of(k).strip()]
    title = max(cands, key=lambda k: (max_sz(k), -geom(k)[1])) if cands else None
    title_bottom = 1.5
    if title is not None:
        txt = text_of(title)
        limit = 15.75 - 0.30 - LEFT
        ty = geom(title)[1]
        below = [geom(k)[1] for k in on if k is not title and geom(k)[1] > ty + 0.2
                 and geom(k)[0] < LEFT + limit and geom(k)[0] + geom(k)[2] > LEFT]
        avail = (min(below) if below else ty + 0.8) - ty - 0.03
        sz = min(4200, int(avail * 72 / 1.17 * 100) // 50 * 50)
        sz = max(sz, 2800)
        while sz > 2800 and title_width(txt, sz, -sz * 0.015) > limit:
            sz -= 50
        spc = -int(sz * 0.015)
        for r in runs(title):
            r.set("sz", str(sz))
            r.set("b", "1")
            r.set("spc", str(spc))
            r.set("kern", "0")
            set_run_color(r, INK)
        for r in title.xpath(".//a:endParaRPr", namespaces=NS):
            r.set("sz", str(sz))
        set_geom(title, [LEFT, ty, limit, max(avail, 0.5)])
        bp = title.find(".//a:bodyPr", NS)
        bp.set("wrap", "square")
        for t in ("lIns", "rIns", "tIns", "bIns"):
            bp.set(t, "0")
        bp.set("anchor", "t")
        for af in list(bp):
            bp.remove(af)
        etree.SubElement(bp, q("a:noAutofit"))
        for ppr in title.xpath(".//a:pPr", namespaces=NS):
            for ls in ppr.findall("a:lnSpc", NS):
                ppr.remove(ls)
        title_bottom = ty + avail

    # 3. logos (aligned with the title line)
    add_logos(sptree, rels, False, 0.93)

    # 4. kicker above the title -> grey caps like the reference eyebrows
    for k in on:
        if k is title or etree.QName(k).localname != "sp":
            continue
        g = geom(k)
        if g[1] < 0.8 and text_of(k).strip() and max_sz(k) <= 1600:
            for r in runs(k):
                set_run_color(r, HEAD_TXT)
                r.set("b", "1")

    # 5. subtitles
    subtitle_ids = set()
    for k in on:
        if k is title or etree.QName(k).localname != "sp":
            continue
        g = geom(k)
        if 1.30 <= g[1] <= 2.30 and g[2] >= 8 and text_of(k).strip() and 1400 <= max_sz(k) <= 2200 and fill_of(k) is None:
            subtitle_ids.add(id(k))
            for r in runs(k):
                c = run_color(r)
                r.set("i", "1")
                if c in NAVY or c == "3F6FB5":
                    set_run_color(r, BLUE)
                elif c in ORANGE:
                    pass
                else:
                    set_run_color(r, GREY_TXT)

    # 6. rules: title underline and footer rule
    for k in list(on):
        if etree.QName(k).localname != "sp" or text_of(k).strip():
            continue
        g = geom(k)
        f = fill_of(k)
        if g[3] <= 0.05 and g[2] >= 10 and 1.7 <= g[1] <= 2.6 and f in NAVY:
            sptree.remove(k)
            on.remove(k)
        elif g[3] <= 0.03 and g[2] >= 10 and g[1] >= 10.0:
            sptree.remove(k)
            on.remove(k)

    # 7. footer + page number
    foot = [k for k in on if etree.QName(k).localname == "sp" and geom(k)[1] >= 10.1 and text_of(k).strip()
            and max_sz(k) <= 1250 and geom(k)[2] >= 8]
    fy, fsz = 10.62, 1050
    for k in foot:
        g = geom(k)
        fsz = min(max_sz(k) or 1050, 1200)
        fy = g[1]
        set_geom(k, [g[0], fy, min(g[2], RIGHT - 1.45 - g[0]), max(g[3], 0.25)])
        for r in runs(k):
            if run_color(r) in (None, "8C8C8C", "7F7F7F", "7B8089", "595959", "A6A6A6"):
                set_run_color(r, GREY_TXT)
    if i not in HIDDEN_SLIDES:
        sptree.append(mk_text("Número da página", [RIGHT - 1.30, fy, 1.30, 0.25],
                              [[("Página %02d" % i, {"sz": fsz, "color": GREY_TXT})]], algn="r"))

    # 8. tables built from shapes: header cells (navy/orange fill + white text) -> reference header style
    sps = [k for k in on if etree.QName(k).localname == "sp"]
    texts = [k for k in sps if text_of(k).strip()]

    def white_text_targets(cell):
        g = geom(cell)
        out = []
        if any(run_color(r) in WHITE_TXT for r in runs(cell)):
            out.append(cell)
        for t in texts:
            if t is not cell and center_in(geom(t), g) and any(run_color(r) in WHITE_TXT for r in runs(t)):
                out.append(t)
        return out

    hdr_candidates = [k for k in sps if fill_of(k) in (NAVY | ORANGE) and geom(k)[3] <= 0.80 and geom(k)[1] > 1.2 and white_text_targets(k)]
    rows = {}
    for k in hdr_candidates:
        rows.setdefault(round(geom(k)[1], 1), []).append(k)
    for y, cells in rows.items():
        if len(cells) < 2 and len(white_text_targets(cells[0])) < 3:
            continue
        x0 = min(geom(c)[0] for c in cells)
        x1 = max(geom(c)[0] + geom(c)[2] for c in cells)
        yb = max(geom(c)[1] + geom(c)[3] for c in cells)
        for c in cells:
            orange = fill_of(c) in ORANGE
            set_solid_fill(c.find("p:spPr", NS), None)
            c.set("data-hdr", "1")
            for t in white_text_targets(c):
                for r in runs(t):
                    if run_color(r) in WHITE_TXT:
                        set_run_color(r, "C25300" if orange else "5B6472")
                        r.set("b", "1")
        line = mk_sp("Linha cabeçalho", [x0, yb - 0.01, x1 - x0, 0.0104], fill=RULE)
        cells[-1].addnext(line)

    # 9. white text sitting on mid-blue fills (becomes light blue) -> deep navy text
    for k in sps:
        if fill_of(k) == "3F6FB5":
            g = geom(k)
            for t in [k] + [t for t in texts if t is not k and center_in(geom(t), g)]:
                for r in runs(t):
                    if run_color(r) in WHITE_TXT:
                        set_run_color(r, NAVY_DEEP)

    # 10. cards
    for k in sps:
        f = fill_of(k)
        g = geom(k)
        light = f is not None and f not in ORANGE_CARD_FILLS and f not in ("FFFFFF", "F4F7FD") and min(int(f[i:i + 2], 16) for i in (0, 2, 4)) >= 0xDC
        if (f in LIGHT_CARD_FILLS or light) and g[2] >= 2.5 and g[3] >= 0.9:
            sppr = k.find("p:spPr", NS)
            set_solid_fill(sppr, "FFFFFF")
            set_line(sppr, CARD_LINE, 9525)
            round_corners(k)
        elif f in ORANGE_CARD_FILLS | {"E3E9F2"} and g[2] >= 2.5 and g[3] >= 0.9:
            round_corners(k)
        elif f in (NAVY | {"3F6FB5"}) and g[2] >= 3 and g[3] >= 1.2:
            round_corners(k)
        elif f == "FFFFFF" and k.find("p:spPr/a:ln/a:solidFill", NS) is not None and g[2] >= 2.5 and g[3] >= 0.9:
            set_line(k.find("p:spPr", NS), CARD_LINE, 9525)
            round_corners(k)

    # 11. raster charts -> inside a white card
    for pic in sptree.findall("p:pic", NS):
        blip = pic.find(".//a:blip", NS)
        tgt = os.path.basename(rels.target(blip.get(q("r:embed"))) or "")
        if tgt in CHART_PNGS:
            g = geom(pic)
            pad = 0.18
            s = min((g[2] - 2 * pad) / g[2], (g[3] - 2 * pad) / g[3])
            nw, nh = g[2] * s, g[3] * s
            card = mk_sp("Card gráfico", g, fill="FFFFFF", line=CARD_LINE, radius=0.12)
            pic.addprevious(card)
            set_geom(pic, [g[0] + (g[2] - nw) / 2, g[1] + (g[3] - nh) / 2, nw, nh])

    for gf in sptree.findall("p:graphicFrame", NS):
        if gf.find(".//{http://schemas.openxmlformats.org/drawingml/2006/chart}chart") is not None:
            g = geom(gf)
            card = mk_sp("Card gráfico", g, fill="FFFFFF", line=CARD_LINE, radius=0.12)
            gf.addprevious(card)
            pad = 0.15
            set_geom(gf, [g[0] + pad, g[1] + pad, g[2] - 2 * pad, g[3] - 2 * pad])

    # 12. a:tbl header rows
    for tbl in root.iter(q("a:tbl")):
        trs = tbl.findall("a:tr", NS)
        if not trs:
            continue
        for tc in trs[0].findall("a:tc", NS):
            tcpr = tc.find("a:tcPr", NS)
            c = tcpr.find("a:solidFill/a:srgbClr", NS) if tcpr is not None else None
            if c is not None and c.get("val").upper() in NAVY:
                sf = tcpr.find("a:solidFill", NS)
                idx = list(tcpr).index(sf)
                tcpr.remove(sf)
                tcpr.insert(idx, etree.Element(q("a:noFill")))
                for r in tc.iter(q("a:rPr")):
                    if run_color(r) in WHITE_TXT:
                        set_run_color(r, "5B6472")

    for tc in root.iter(q("a:tc")):
        c = tc.find("a:tcPr/a:solidFill/a:srgbClr", NS)
        if c is not None and c.get("val").upper() == "3F6FB5":
            for r in tc.iter(q("a:rPr")):
                if run_color(r) in WHITE_TXT:
                    set_run_color(r, NAVY_DEEP)

    return subtitle_ids


def generic_colors(root):
    for hl in list(root.iter(q("a:highlight"))):
        hl.getparent().remove(hl)
    for c in root.iter(q("a:srgbClr")):
        v = c.get("val").upper()
        anc = [etree.QName(a).localname for a in c.iterancestors()]
        is_text = any(a in ("rPr", "defRPr", "endParaRPr") for a in anc[:3])
        m = TEXT_MAP if is_text else FILL_MAP
        if v in m:
            c.set("val", m[v])


def process_cover(root, rels):
    sptree = root.find(".//p:spTree", NS)
    for k in top_children(sptree):
        sptree.remove(k)
    sptree.append(gradient_rect())
    add_logos(sptree, rels, True, 0.92)
    sptree.append(mk_text("Título", [LEFT, 3.55, 15.6, 2.4],
                          [[("Tabela, camadas de remuneração e pocket price", {"sz": 7200, "b": 1, "spc": -144, "color": "FFFFFF", "lnSpc": 96000})]],
                          anchor="b"))
    sptree.append(mk_text("Subtítulo", [LEFT, 6.20, 15.0, 0.6],
                          [[("Outubro de 2026", {"sz": 3000, "color": "9BB5EF"})]]))


def process_divider(i, root, rels):
    sptree = root.find(".//p:spTree", NS)
    sub = ""
    for k in top_children(sptree):
        t = text_of(k)
        if "Detalhes" in t:
            sub = t[t.index("Detalhes"):]
        sptree.remove(k)
    csld = root.find("p:cSld", NS)
    for bg in csld.findall("p:bg", NS):
        csld.remove(bg)
    sptree.append(gradient_rect())
    add_logos(sptree, rels, True, 0.73)
    sptree.append(mk_text("Título", [LEFT, 4.40, 15.0, 1.15],
                          [[("Apêndice", {"sz": 7200, "b": 1, "spc": -144, "color": "FFFFFF", "lnSpc": 96000})]]))
    if sub:
        sptree.append(mk_text("Subtítulo", [LEFT, 5.70, 15.0, 0.9],
                              [[(sub, {"sz": 2400, "color": "9BB5EF"})]]))
    sptree.append(mk_text("Número da página", [RIGHT - 1.30, 10.37, 1.30, 0.29],
                          [[("Página %02d" % i, {"sz": 1350, "color": "FFFFFF", "alpha": 60000})]], algn="r"))


def process_slide3(root, rels):
    """The source slide is a pasted spreadsheet screenshot; rebuild it as a native table in the reference style."""
    sptree = root.find(".//p:spTree", NS)
    for pic in sptree.findall("p:pic", NS):
        sptree.remove(pic)
    x0, y0, w = LEFT, 2.05, RIGHT - LEFT
    cols = [("BLOCO", 3.35), ("COMPONENTE", 3.55), ("ATIVIDADE", 5.45), ("ENTREGÁVEL", 0)]
    cols[-1] = ("ENTREGÁVEL", w - 0.5 - sum(c[1] for c in cols[:-1]))
    rows = [
        ("Tabela, camadas de remuneração e pocket price",
         "Montar o racional da mecânica, reconciliar o front margin em número único e rodar o teste econômico do modelo de front margin com as camadas de política",
         "Waterfall front e back com número único de front, e cada real alocado em uma só camada."),
        ("Metas, percentuais e elegibilidade",
         "Montar o racional da mecânica e rodar o teste econômico (modelo macro) para definir a régua de percentuais, metas e elegibilidade",
         "Faixa de parâmetros e regra de atingimento parcial."),
        ("Simulação da economia por atingimento",
         "Simular margem e remuneração por faixa de atingimento (100%, 90%, 70% e 50%), desenhar a mecânica frente ao risco e verificar se há problema comercial (queda de clientes)",
         "Faixa de margem por nível de atingimento, no lugar do cenário único de teto. Mecânica versus risco. Impacto econômico para o cliente e para a Premier por faixa de meta. Hoje existe objetivo de volume, e não meta; a remuneração é por aproveitamento."),
    ]
    row_h = [1.45, 1.25, 1.75]
    card_h = 0.25 + 0.45 + sum(row_h) + 0.25
    els = [mk_sp("Card tabela", [x0, y0, w, card_h], fill="FFFFFF", line=CARD_LINE, radius=0.12)]
    cx = [x0 + 0.25]
    for _, cw in cols[:-1]:
        cx.append(cx[-1] + cw)
    hy = y0 + 0.28
    for (name, cw), x in zip(cols, cx):
        els.append(mk_text("Cab. " + name, [x + 0.12, hy, (cw or cols[-1][1]) - 0.2, 0.25], [[(name, {"sz": 1125, "b": 1, "color": HEAD_TXT, "spc": 100})]]))
    ly = hy + 0.38
    els.append(mk_sp("Linha cabeçalho", [x0 + 0.25, ly, w - 0.5, 0.0104], fill=RULE))
    y = ly + 0.02
    # highlight the row this deck covers
    els.append(mk_sp("Destaque esta apresentação", [cx[1], y, w - 0.25 - (cx[1] - x0), row_h[0]], fill="F4F7FD"))
    els.append(mk_text("Bloco", [cx[0] + 0.12, y + 0.18, cols[0][1] - 0.3, 1.2],
                       [[("1. Política comercial: tabela, camadas e parâmetros", {"sz": 1500, "b": 1, "color": INK, "lnSpc": 115000})]]))
    for k, (comp, ativ, entr) in enumerate(rows):
        hi = k == 0
        els.append(mk_text("Componente", [cx[1] + 0.12, y + 0.18, cols[1][1] - 0.3, row_h[k] - 0.3],
                           [[(comp, {"sz": 1350, "b": 1, "color": BLUE if hi else INK, "lnSpc": 115000})]] +
                           ([[("ESTA APRESENTAÇÃO", {"sz": 1000, "b": 1, "color": BLUE, "spc": 100, "lnSpc": 160000})]] if hi else [])))
        els.append(mk_text("Atividade", [cx[2] + 0.12, y + 0.18, cols[2][1] - 0.3, row_h[k] - 0.3], [[(ativ, {"sz": 1350, "color": INK, "lnSpc": 115000})]]))
        els.append(mk_text("Entregável", [cx[3] + 0.12, y + 0.18, cols[3][1] - 0.3, row_h[k] - 0.3], [[(entr, {"sz": 1350, "color": INK, "lnSpc": 115000})]]))
        y += row_h[k]
        if k < len(rows) - 1:
            els.append(mk_sp("Linha", [cx[1], y, w - 0.25 - (cx[1] - x0), 0.0104], fill=ROW_RULE))
    for e in els:
        sptree.append(e)


def main():
    # brand assets from the reference deck
    rm = os.path.join(REF, "ppt", "media")
    shutil.copy(os.path.join(rm, "image3.png"), os.path.join(MEDIA, "brand_premier.png"))
    shutil.copy(os.path.join(rm, "image4.png"), os.path.join(MEDIA, "brand_doc.png"))
    shutil.copy(os.path.join(rm, "image1.png"), os.path.join(MEDIA, "brand_premier_w.png"))
    shutil.copy(os.path.join(rm, "image2.png"), os.path.join(MEDIA, "brand_doc_w.png"))
    # recolor raster charts
    subprocess.run([sys.executable, "-I", os.path.join(HERE, "recolor_png.py")] +
                   [os.path.join(MEDIA, f) for f in sorted(CHART_PNGS) if os.path.exists(os.path.join(MEDIA, f))], check=True)

    pres = etree.parse(os.path.join(TGT, "ppt", "presentation.xml"))
    prels = Rels(os.path.join(TGT, "ppt", "_rels", "presentation.xml.rels"))
    order = []
    for s in pres.getroot().find("p:sldIdLst", NS):
        order.append(os.path.basename(prels.target(s.get(q("r:id")))))

    for idx, fname in enumerate(order, start=1):
        path = os.path.join(SLIDES, fname)
        tree = etree.parse(path)
        root = tree.getroot()
        if root.get("show") == "0":
            HIDDEN_SLIDES.add(idx)
        rels = Rels(os.path.join(SLIDES, "_rels", fname + ".rels"))
        if idx == 1:
            process_cover(root, rels)
        elif "Apêndice" in "".join(root.xpath("//a:t/text()", namespaces=NS)) and len(top_children(root.find('.//p:spTree', NS))) <= 4:
            process_divider(idx, root, rels)
        else:
            if idx == 3:
                process_slide3(root, rels)
            process_content(idx, root, rels)
            generic_colors(root)
        for el in root.iter():
            if el.get("data-hdr"):
                del el.attrib["data-hdr"]
        rels.drop_unused(root)
        rels.save()
        tree.write(path, xml_declaration=True, encoding="UTF-8", standalone=True)
        print("ok", idx, fname)

    # native charts
    cdir = os.path.join(TGT, "ppt", "charts")
    if os.path.isdir(cdir):
        for f in os.listdir(cdir):
            if f.endswith(".xml"):
                p = os.path.join(cdir, f)
                t = etree.parse(p)
                for c in t.getroot().iter(q("a:srgbClr")):
                    v = c.get("val").upper()
                    anc = [etree.QName(a).localname for a in c.iterancestors()]
                    m = TEXT_MAP if ("txPr" in anc or "rich" in anc) else FILL_MAP
                    if v in m:
                        c.set("val", m[v])
                t.write(p, xml_declaration=True, encoding="UTF-8", standalone=True)

    # drop media no longer referenced
    used = set()
    for dp, _, fs in os.walk(TGT):
        for f in fs:
            if f.endswith(".rels"):
                used |= {os.path.basename(t) for t in re.findall(r'Target="([^"]+)"', open(os.path.join(dp, f)).read())}
    for f in os.listdir(MEDIA):
        if f not in used:
            os.remove(os.path.join(MEDIA, f))
            print("removed orphan", f)


main()
