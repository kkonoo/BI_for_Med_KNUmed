"""Shared look for the course's concept figures (scripts/figs/*.py → assets/img/wNN/*.png).

Slide-gallery crimson in its gradient + rich mode (kkonoo.github.io/slide-gallery):
wine → crimson → burnt-orange gradient for the main element, tints of those colours for
the rest, and the gallery's blue accent for the one thing the reader should look at.
Korean labels in Pretendard (install the OTFs in ~/.fonts). No titles — the caption in
the chapter says what the figure shows.

Coordinates are inches: new(w, h) gives an axis that runs 0..w and 0..h, so a box drawn
1.0 wide is one inch wide on the page at 100% and text sizes stay predictable.
"""
import glob, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp
from matplotlib import font_manager as fm
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

for f in glob.glob(os.path.expanduser("~/.fonts/Pretendard-*.otf")):
    fm.fontManager.addfont(f)
plt.rcParams.update({
    "font.family": ["Pretendard", "DejaVu Sans"], "font.size": 11,
    "text.color": "#262B33", "axes.labelcolor": "#262B33",
    "axes.edgecolor": "#9AA1AB", "xtick.color": "#4B5563", "ytick.color": "#4B5563",
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white", "savefig.facecolor": "white",
    "axes.unicode_minus": False,
})

# ── colours ────────────────────────────────────────────────────────────────
WINE, CRIMSON, ORANGE = "#7A1F3D", "#B0283C", "#C2531F"   # gradient stops
BLUE = "#2E9CCA"                                          # accent: one look-here per figure
TEXT, TEXT2, LINE, FAINT = "#262B33", "#6B7280", "#E2E5EA", "#F5F6F8"

def mix(c, a):
    """Colour c at strength a (0–1) over white, as a solid colour."""
    c = np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)])
    return "#%02X%02X%02X" % tuple((255 + (c - 255) * a).round().astype(int))

GRAD = LinearSegmentedColormap.from_list("medgrad", [WINE, CRIMSON, ORANGE])

def ramp(n):
    """n colours along the wine → crimson → orange gradient (for steps 1..n)."""
    return [matplotlib.colors.to_hex(GRAD(i / max(n - 1, 1))) for i in range(n)]

# ── canvas ─────────────────────────────────────────────────────────────────
def new(w, h):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis("off")
    return fig, ax

def save(fig, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=200, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print("saved", path)

# ── shapes ─────────────────────────────────────────────────────────────────
def box(ax, x, y, w, h, fc="white", ec=LINE, lw=1.0, r=0.08, z=2, ls="-"):
    """Rounded box with its lower-left corner at (x, y)."""
    p = mp.FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                          fc=fc, ec=ec, lw=lw, zorder=z, ls=ls)
    ax.add_patch(p)
    return p

def gradbox(ax, x, y, w, h, colors=(WINE, CRIMSON, ORANGE), r=0.08, z=2, vertical=False):
    """Rounded box filled with a left→right (or bottom→top) gradient."""
    p = box(ax, x, y, w, h, fc="none", ec="none", r=r, z=z)
    cmap = LinearSegmentedColormap.from_list("g", list(colors))
    g = np.linspace(0, 1, 256)
    g = g[:, None] if vertical else g[None, :]
    im = ax.imshow(g, cmap=cmap, extent=(x, x + w, y, y + h), origin="lower",
                   aspect="auto", zorder=z, interpolation="bicubic")
    im.set_clip_path(p)
    return p

def chevron(ax, x, y, w, h, fc, tip=0.18, first=False, z=2):
    """Arrow-shaped step box (flat left edge if first)."""
    pts = [(x, y), (x + w - tip, y), (x + w, y + h / 2), (x + w - tip, y + h), (x, y + h)]
    if not first:
        pts.append((x + tip, y + h / 2))
    ax.add_patch(mp.Polygon(pts, closed=True, fc=fc, ec="none", zorder=z))

def num(ax, x, y, n, fc=CRIMSON, tc="white", r=0.14, fs=10, z=4):
    """Numbered circle centred at (x, y)."""
    ax.add_patch(mp.Circle((x, y), r, fc=fc, ec="none", zorder=z))
    ax.text(x, y, str(n), ha="center", va="center", color=tc, fontsize=fs,
            fontweight="bold", zorder=z + 1)

def pill(ax, x, y, text, fc=BLUE, tc="white", fs=9.5, padx=0.12, h=0.28, z=4, ha="center"):
    """Text in a rounded label; (x, y) is the centre (or left edge if ha='left')."""
    t = ax.text(0, 0, text, fontsize=fs, fontweight="bold")
    ax.figure.canvas.draw()
    w = t.get_window_extent().width / ax.figure.dpi + 2 * padx
    t.remove()
    x0 = x - w / 2 if ha == "center" else x
    box(ax, x0, y - h / 2, w, h, fc=fc, ec="none", r=h / 2, z=z)
    ax.text(x0 + w / 2, y, text, ha="center", va="center", fontsize=fs, fontweight="bold",
            color=tc, zorder=z + 1)
    return w

def arrow(ax, x1, y1, x2, y2, color="#9AA1AB", lw=1.6, ms=12, z=3, ls="-", rad=0):
    ax.add_patch(mp.FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=ms,
                                    color=color, lw=lw, zorder=z, ls=ls,
                                    connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0))

def label(ax, x, y, text, fs=11, w="regular", c=TEXT, ha="center", va="center", z=5, **kw):
    return ax.text(x, y, text, fontsize=fs, fontweight=w, color=c, ha=ha, va=va, zorder=z, **kw)
