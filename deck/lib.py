"""Helpers: DOC design tokens, pt-BR number format, slide shell and SVG chart primitives."""
import math
from html import escape

BLUE = "#1A56DB"; INK = "#14171F"; G1 = "#888D97"; G2 = "#9CA3AF"; G3 = "#C7CBD1"; G4 = "#E5E7EB"
WHITE = "#FFFFFF"; PANEL = "#F4F7FD"; LB1 = "#EAF0FB"; LB2 = "#9AB4E8"; GRID = "#F0F1F3"
NAVY = "#0A1D5C"
FONT = "Arial, Helvetica, sans-serif"
MINUS = "−"


def num(x, d=1, sign=False):
    s = f"{abs(x):,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if x < 0 and float(s.replace(".", "").replace(",", ".")) != 0:
        return MINUS + s
    return ("+" + s) if (sign and x > 0) else s


def e(t):
    return escape(str(t), quote=False)


# ---------------------------------------------------------------- HTML pieces
def P(text, left, top, width, size, color=INK, bold=False, italic=False, align="left", lh=1.3,
      extra="", raw=False):
    st = (f"position:absolute;left:{left}px;top:{top}px;width:{width}px;font-size:{size}px;"
          f"line-height:{lh};color:{color};text-align:{align};")
    if bold:
        st += "font-weight:700;"
    if italic:
        st += "font-style:italic;"
    return f'<p style="{st}{extra}">{text if raw else e(text)}</p>'


def p(text, size=18, color=INK, bold=False, italic=False, lh=1.35, extra="", raw=False):
    st = f"font-size:{size}px;line-height:{lh};color:{color};"
    if bold:
        st += "font-weight:700;"
    if italic:
        st += "font-style:italic;"
    return f'<p style="{st}{extra}">{text if raw else e(text)}</p>'


def h3(text, size=15, color=BLUE):
    return (f'<h3 style="font-size:{size}px;font-weight:700;line-height:1.2;color:{color};'
            f'text-transform:uppercase;letter-spacing:1px">{e(text)}</h3>')


SEAL_COLORS = {"COMPROVADA": BLUE, "RECOMENDAÇÃO": BLUE, "PARCIAL": G1, "HIPÓTESE": G1,
               "NÃO MENSURÁVEL": G2, "EXEMPLO ILUSTRATIVO": G1}


def seal_p(label):
    c = SEAL_COLORS[label]
    return (f'<p style="font-size:13px;font-weight:700;line-height:1.2;color:{c};letter-spacing:1px;'
            f'text-transform:uppercase;border:1px solid {c};border-radius:6px;padding:5px 10px">{e(label)}</p>')


def seals(labels, right_x, top):
    """Pinned row of evidence seals whose right edge sits at right_x."""
    w = 560
    inner = "".join(seal_p(l) for l in labels)
    return (f'<div style="position:absolute;left:{right_x - w}px;top:{top}px;width:{w}px;display:flex;'
            f'flex-direction:row;justify-content:end;gap:8px">{inner}</div>')


def logo(dark=False):
    c = WHITE if dark else BLUE
    return P("DOC", 1620, 64, 200, 40, c, bold=True, align="right", lh=1.0, extra="letter-spacing:3px;")


def rail(blocks, left=1330, top=222, width=490, gap=14):
    """blocks: list of (label, inner_html, kind) where kind in {'info','decide'}"""
    out = []
    for label, inner, kind in blocks:
        bg = LB1 if kind == "decide" else PANEL
        col = INK if kind == "decide" else BLUE
        out.append(f'<div style="background:{bg};border-radius:16px;padding:18px 22px;display:flex;'
                   f'flex-direction:column;gap:8px">{h3(label, color=col)}{inner}</div>')
    return (f'<div style="position:absolute;left:{left}px;top:{top}px;width:{width}px;display:flex;'
            f'flex-direction:column;gap:{gap}px">{"".join(out)}</div>')


def mini_table(rows, widths, size=16, head=None, bold_first=True, colors=None):
    """Grid of text made with flex rows (keeps rich control vs <table>)."""
    out = []
    if head:
        cells = "".join(
            f'<p style="width:{w}px;font-size:13px;line-height:1.25;color:{G1};font-weight:700">{e(h)}</p>'
            for h, w in zip(head, widths))
        out.append(f'<div style="display:flex;flex-direction:row;gap:6px;border-bottom:1px solid {G4};'
                   f'padding:0px 0px 4px 0px">{cells}</div>')
    for ri, r in enumerate(rows):
        cells = []
        for ci, (c, w) in enumerate(zip(r, widths)):
            col = (colors[ri] if colors else INK)
            b = "font-weight:700;" if (bold_first and ci == 0) else ""
            cells.append(f'<p style="width:{w}px;font-size:{size}px;line-height:1.3;color:{col};{b}">{e(c)}</p>')
        out.append(f'<div style="display:flex;flex-direction:row;gap:6px">{"".join(cells)}</div>')
    return f'<div style="display:flex;flex-direction:column;gap:5px">{"".join(out)}</div>'


def placeholder(left, top, width, height, title, filename, legend):
    return (f'<div style="position:absolute;left:{left}px;top:{top}px;width:{width}px;height:{height}px;'
            f'background:{PANEL};border:2px dashed {LB2};border-radius:16px;display:flex;flex-direction:column;'
            f'justify-content:center;align-items:center;gap:14px;padding:48px">'
            f'{p("GRÁFICO EM PNG: INSERIR ANTES DE APRESENTAR", 15, BLUE, bold=True, extra="letter-spacing:1px;text-align:center;")}'
            f'{p(title, 22, INK, bold=True, extra="text-align:center;")}'
            f'{p(legend, 17, G1, extra="text-align:center;")}'
            f'{p("Arquivo: " + filename, 15, G1, italic=True, extra="text-align:center;")}'
            f'</div>')


def slide(sid, title, subtitle, body, footer, page, notes, dark=False, transition="fade"):
    if dark:
        bg = "linear-gradient(135deg, #050E2A 0%, #0A1D5C 55%, #0E2F8A 100%)"
        parts = [body]
        parts.append(logo(dark=True))
        parts.append(P(footer, 100, 992, 1500, 15, "#9AB4E8", lh=1.3))
        parts.append(P(f"Página {page}", 1640, 992, 180, 15, "#9AB4E8", align="right", lh=1.3))
        color = WHITE
    else:
        bg = WHITE
        parts = [P(title, 100, 50, 1440, 56, INK, bold=True, lh=1.1, extra="white-space:nowrap;"),
                 P(subtitle, 100, 122, 1480, 24, G1, italic=True, lh=1.3),
                 logo(), body,
                 P(footer, 100, 992, 1500, 15, G1, lh=1.3),
                 P(f"Página {page}", 1640, 992, 180, 15, G1, align="right", lh=1.3)]
        color = INK
    notes = notes.strip()
    assert len(notes) <= 4000, (sid, len(notes))
    return (f'<section id="{sid}" data-transition="{transition}" style="background:{bg};color:{color};'
            f'font-family:{FONT};padding:90px 100px 60px 100px;display:flex;flex-direction:column">\n'
            + "\n".join(parts) + f"\n<aside>{e(notes)}</aside>\n</section>\n")


# ---------------------------------------------------------------- SVG
class Svg:
    def __init__(self, left, top, w, h, alt):
        self.left, self.top, self.w, self.h, self.alt = left, top, w, h, alt
        self.items = []

    def add(self, s):
        self.items.append(s)

    def text(self, x, y, t, size=16, color=INK, anchor="start", bold=False, italic=False, rotate=None):
        attrs = f'x="{x:.1f}" y="{y:.1f}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" fill="{color}" text-anchor="{anchor}"'
        if bold:
            attrs += ' font-weight="700"'
        if italic:
            attrs += ' font-style="italic"'
        if rotate is not None:
            attrs += f' transform="rotate({rotate} {x:.1f} {y:.1f})"'
        self.add(f"<text {attrs}>{e(t)}</text>")

    def line(self, x1, y1, x2, y2, color=INK, w=1, dash=None, cap="butt"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{w}"{d} stroke-linecap="{cap}"/>')

    def rect(self, x, y, w, h, fill, stroke=None, sw=1, rx=0, dash=None, opacity=None):
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        if dash:
            s += f' stroke-dasharray="{dash}"'
        if opacity is not None:
            s += f' fill-opacity="{opacity}"'
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w,0):.1f}" height="{max(h,0):.1f}" rx="{rx}" fill="{fill}"{s}/>')

    def circle(self, x, y, r, fill, stroke=None, sw=1.5):
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}"{s}/>')

    def diamond(self, x, y, r, fill):
        self.add(f'<path d="M{x:.1f} {y-r:.1f} L{x+r:.1f} {y:.1f} L{x:.1f} {y+r:.1f} L{x-r:.1f} {y:.1f} Z" fill="{fill}" stroke="{WHITE}" stroke-width="1.5"/>')

    def path(self, d, stroke=INK, w=1.5, fill="none", dash=None):
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<path d="{d}" stroke="{stroke}" stroke-width="{w}" fill="{fill}"{ds}/>')

    def arrow(self, pts, color=G2, w=2, label=None, lx=None, ly=None, lsize=15, lcolor=INK, anchor="middle"):
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        self.path(d, color, w)
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        ang = math.atan2(y2 - y1, x2 - x1)
        L = 11
        a1 = (x2 - L * math.cos(ang - 0.4), y2 - L * math.sin(ang - 0.4))
        a2 = (x2 - L * math.cos(ang + 0.4), y2 - L * math.sin(ang + 0.4))
        self.add(f'<path d="M{x2:.1f} {y2:.1f} L{a1[0]:.1f} {a1[1]:.1f} L{a2[0]:.1f} {a2[1]:.1f} Z" fill="{color}"/>')
        if label:
            self.text(lx, ly, label, lsize, lcolor, anchor)

    def hatch_def(self, pid, color=G3):
        self.add(f'<defs><pattern id="{pid}" width="10" height="10" patternUnits="userSpaceOnUse" '
                 f'patternTransform="rotate(45)"><rect width="10" height="10" fill="#FAFAFB"/>'
                 f'<line x1="0" y1="0" x2="0" y2="10" stroke="{color}" stroke-width="3"/></pattern></defs>')

    def render(self):
        body = "".join(self.items)
        s = (f'<svg aria-label="{e(self.alt)}" xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
             f'viewBox="0 0 {self.w} {self.h}" style="position:absolute;left:{self.left}px;top:{self.top}px;'
             f'width:{self.w}px;height:{self.h}px">{body}</svg>')
        assert len(s.encode()) < 52000, (self.alt, len(s.encode()))
        return s


class Scale:
    def __init__(self, d0, d1, r0, r1, log=False):
        self.d0, self.d1, self.r0, self.r1, self.log = d0, d1, r0, r1, log

    def __call__(self, v):
        if self.log:
            t = (math.log(v) - math.log(self.d0)) / (math.log(self.d1) - math.log(self.d0))
        else:
            t = (v - self.d0) / (self.d1 - self.d0)
        return self.r0 + t * (self.r1 - self.r0)


def axes(svg, sx, sy, xticks, yticks, xfmt, yfmt, xtitle=None, ytitle=None, tick_size=16, grid=True,
         xtitle_dy=44, ytitle_dx=62):
    x0, x1 = sx.r0, sx.r1
    y0, y1 = sy.r0, sy.r1  # y0 bottom, y1 top
    for t in yticks:
        y = sy(t)
        if grid:
            svg.line(x0, y, x1, y, GRID, 1)
        svg.text(x0 - 8, y + 5, yfmt(t), tick_size, G1, "end")
    for t in xticks:
        x = sx(t)
        svg.line(x, y0, x, y0 + 5, G2, 1)
        svg.text(x, y0 + 22, xfmt(t), tick_size, G1, "middle")
    svg.line(x0, y0, x1, y0, G2, 1)
    svg.line(x0, y0, x0, y1, G2, 1)
    if xtitle:
        svg.text((x0 + x1) / 2, y0 + xtitle_dy, xtitle, 15, G1, "middle")
    if ytitle:
        xm = x0 - ytitle_dx
        ym = (y0 + y1) / 2
        svg.text(xm, ym, ytitle, 15, G1, "middle", rotate=-90)
