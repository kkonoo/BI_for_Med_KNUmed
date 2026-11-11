# W2 §1.1 작은 변이: SNV, 삽입, 결실을 레퍼런스와 나란히 (BI_for_Biomed W2 small_variants를 다시 그림)
from medfig import *

ref = "ACGTGCATGCAGTA"
rows = [  # name, bases (None = deleted), marks {index: (kind, colour)}, note
    ("레퍼런스", list(ref), {}, ""),
    ("SNV", list(ref[:8] + "A" + ref[9:]), {8: ("fill", CAT[0])}, "염기 1개가 바뀜"),
    ("삽입", list(ref[:11] + "TTA" + ref[11:]), {11: ("fill", CAT[1]), 12: ("fill", CAT[1]), 13: ("fill", CAT[1])},
     "염기 3개가 들어감"),
    ("결실", list(ref[:5]) + [None] * 3 + list(ref[8:]), {5: ("gap", CAT[2]), 6: ("gap", CAT[2]), 7: ("gap", CAT[2])},
     "염기 3개가 빠짐"),
]
cw, ch, x0 = 0.36, 0.46, 2.0
fig, ax = new(x0 + 17 * cw + 0.2, 3.6)
for r, (name, seq, marks, note) in enumerate(rows):
    y = 3.1 - r * 0.86
    col = TEXT if r == 0 else CAT[r - 1]
    label(ax, x0 - 0.25, y + (0.1 if note else 0), name, fs=13.5, w="bold", ha="right", c=col)
    if note:
        label(ax, x0 - 0.25, y - 0.17, note, fs=11, c=TEXT2, ha="right")
    for i, b in enumerate(seq):
        x = x0 + i * cw
        kind, mc = marks.get(i, (None, None))
        if kind == "fill":
            box(ax, x + 0.02, y - ch / 2, cw - 0.04, ch, fc=mc, ec="none", r=0.05)
            label(ax, x + cw / 2, y, b, fs=13.5, w="bold", c="white")
        elif kind == "gap":
            box(ax, x + 0.02, y - ch / 2, cw - 0.04, ch, fc=mix(mc, 0.08), ec=mc, lw=1.3, r=0.05, ls=(0, (3, 2)))
        else:
            box(ax, x + 0.02, y - ch / 2, cw - 0.04, ch, fc=FAINT, ec="none", r=0.05)
            label(ax, x + cw / 2, y, b, fs=13.5, c="#4B5563")
save(fig, "../../assets/img/w02/small_variants.png")
