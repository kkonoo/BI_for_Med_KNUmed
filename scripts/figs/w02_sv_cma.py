# W2 §2.1 큰 변이의 모양과 마이크로어레이(CMA)가 보는 것 — 복제수가 바뀌어야 보임 (BI_for_Biomed W2 sv_types를 다시 그림)
import matplotlib.patches as mp
from medfig import *

SW, SG, SH = 0.5, 0.05, 0.38       # segment width, gap, height
X0 = 1.2
fig, ax = new(9.8, 4.3)

def seg(x, y, name, fc=FAINT, tc="#4B5563", rev=False, empty=None, other=False):
    t = 0.12                         # arrow tip: shows the direction of the segment
    if rev:
        pts = [(x + SW, y), (x + t, y), (x, y + SH / 2), (x + t, y + SH), (x + SW, y + SH)]
    else:
        pts = [(x, y), (x + SW - t, y), (x + SW, y + SH / 2), (x + SW - t, y + SH), (x, y + SH)]
    if empty:
        ax.add_patch(mp.Polygon(pts, closed=True, fc="white", ec=empty, lw=1.3, ls=(0, (3, 2)), zorder=2))
    else:
        ax.add_patch(mp.Polygon(pts, closed=True, fc=fc, ec=LINE if other else "none", lw=1, zorder=2))
        label(ax, x + SW / 2 + (0.04 if rev else -0.04), y + SH / 2, name, fs=12, w="bold", c=tc)
    return x + SW + SG

oth = dict(fc="white", other=True)
rows = [  # label, colour, segments, note, CMA sees it?
    ("레퍼런스", TEXT, [("A", {}), ("B", {}), ("C", {}), ("D", {}), "|", ("W", oth), ("X", oth)],
     "흰 칸 = 다른 염색체", None),
    ("결실", CAT[0], [("A", {}), ("B", "empty"), ("C", {}), ("D", {})], "B가 없어짐 → 복제수 ↓", True),
    ("중복", CAT[1], [("A", {}), ("B", "hot"), ("B", "hot"), ("C", {}), ("D", {})], "B가 한 번 더 → 복제수 ↑", True),
    ("역위", CAT[2], [("A", {}), ("B", "rev"), ("C", {}), ("D", {})], "B가 뒤집힘 → 복제수 그대로", False),
    ("전좌", CAT[3], [("A", {}), ("B", {}), ("X", "hotother"), "|", ("W", oth), ("C", "hot"), ("D", "hot")],
     "끝을 맞바꿈 → 복제수 그대로", False),
]
XN = X0 + 6 * (SW + SG) + 0.35 + 0.4
label(ax, XN + 2.75, 4.05, "CMA로", fs=11, w="semibold", c=TEXT2)
for r, (name, col, segs, note, seen) in enumerate(rows):
    y = 3.55 - r * 0.78
    label(ax, X0 - 0.2, y + SH / 2, name, fs=13, w="bold", c=col, ha="right")
    x = X0
    for s in segs:
        if s == "|":
            x += 0.4
            continue
        nm, kind = s
        if kind == "empty":
            x = seg(x, y, nm, empty=col)
        elif kind == "hot":
            x = seg(x, y, nm, fc=col, tc="white")
        elif kind == "rev":
            x = seg(x, y, nm, fc=col, tc="white", rev=True)
        elif kind == "hotother":
            x = seg(x, y, nm, fc=col, tc="white", other=True)
        else:
            x = seg(x, y, nm, **kind)
    label(ax, XN, y + SH / 2, note, fs=11.5, c=TEXT2 if r == 0 else TEXT, ha="left")
    if seen is not None:
        fc, tc, t = (mix(WINE, 0.16), WINE, "보임") if seen else (FAINT, TEXT2, "못 봄")
        box(ax, XN + 2.3, y + SH / 2 - 0.16, 0.9, 0.32, fc=fc, ec="none", r=0.16)
        label(ax, XN + 2.75, y + SH / 2, t, fs=11, w="bold", c=tc)
    if r == 0:
        ax.plot([0.3, XN + 3.2], [y - 0.2, y - 0.2], color=LINE, lw=1)
save(fig, "../../assets/img/w02/sv_cma.png")
