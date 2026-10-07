"""Recolor raster charts from the 3 Camadas palette (navy/mid-blue/orange)
to the Piloto palette (royal blue ramp + ink).

Blue-family pixels are mapped along a luminance ramp
  white -> 8FB4DC -> 3F6FB5 -> 1F3864 -> (darker)
onto
  white -> C3D3F5 -> 7BA0EA -> 1A56DB -> 0A1D5C.
Orange (PremieRpet accent), neutrals, reds and greens are left alone.
"""
import sys
import numpy as np
from PIL import Image


def hx(s):
    return np.array([int(s[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float64)


def lum(c):
    return (0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]) / 255.0


W = hx("FFFFFF")
BLUE_SRC = [W, hx("8FB4DC"), hx("3F6FB5"), hx("1F3864"), hx("0B1530")]
BLUE_DST = [W, hx("C3D3F5"), hx("7BA0EA"), hx("1A56DB"), hx("0A1D5C")]
ORANGE_SRC_Y = float(lum(hx("FF6E08")))
INK = hx("14171F")


def ramp(y, src, dst):
    ys = np.array([float(lum(c)) for c in src])  # decreasing
    out = np.zeros(y.shape + (3,))
    yy = np.clip(y, ys[-1], ys[0])
    for k in range(len(ys) - 1):
        hi, lo = ys[k], ys[k + 1]
        m = (yy <= hi) & (yy >= lo)
        t = ((hi - yy[m]) / (hi - lo))[:, None]
        out[m] = dst[k] * (1 - t) + dst[k + 1] * t
    return out


def recolor(path_in, path_out):
    im = Image.open(path_in).convert("RGBA")
    a = np.asarray(im).astype(np.float64)
    rgb, alpha = a[..., :3], a[..., 3:]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx = rgb.max(-1)
    mn = rgb.min(-1)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    # hue in degrees
    d = np.maximum(mx - mn, 1e-9)
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    chroma = mx - mn
    y = lum(rgb)

    blue = (h >= 195) & (h <= 240) & (chroma >= 6) & (sat >= 0.04)
    orange = (h >= 8) & (h <= 40) & (chroma >= 20) & (sat >= 0.12) & (r > 150)
    # keep dark oranges/browns that are not part of the orange ramp (e.g. B8860B goldenrod)
    gold = (h > 40)
    orange &= ~gold

    out = rgb.copy()
    out[blue] = ramp(y[blue], BLUE_SRC, BLUE_DST)
    res = np.concatenate([np.clip(out, 0, 255), alpha], -1).astype(np.uint8)
    Image.fromarray(res, "RGBA").save(path_out, optimize=True)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        recolor(p, p)
        print("recolored", p)
