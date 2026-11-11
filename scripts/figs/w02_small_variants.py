# W2 §1.1 작은 변이: SNV, 삽입, 결실을 레퍼런스와 나란히 (BI_for_Biomed W2 small_variants를 다시 그림)
from medfig import *

ref = "ACGTTGCATGCAGTTACG"
rows = [
    ("레퍼런스", list(ref), {}, ""),
    ("SNV", list(ref[:11] + "T" + ref[12:]), {11: ("fill", CAT[0])}, "염기 1개가 바뀜"),
    ("삽입", list(ref[:13] + "TTA" + ref[13:]), {13: ("fill", CAT[1]), 14: ("fill", CAT[1]), 15: ("fill", CAT[1])},
     "염기 3개가 들어감"),
    ("결실", list(ref[:9]) + [None] * 3 + list(ref[12:]), {9: ("gap", CAT[2]), 10: ("gap", CAT[2]), 11: ("gap", CAT[2])},
     "염기 3개가 빠짐"),
]
cw, ch, x0 = 0.34, 0.42, 1.55
fig, ax = new(x0 + 21 * cw + 2.1, 3.1)
for r, (name, seq, marks, note) in enumerate(rows):
    y = 2.55 - r * 0.78
    label(ax, x0 - 0.25, y, name, fs=12.5, w="bold", ha="right",
          c=TEXT if r == 0 else CAT[r - 1])
    for i, b in enumerate(seq):
        x = x0 + i * cw
        kind, col = marks.get(i, (None, None))
        if kind == "fill":
            box(ax, x + 0.02, y - ch / 2, cw - 0.04, ch, fc=col, ec="none", r=0.05)
            label(ax, x + cw / 2, y, b, fs=12, w="bold", c="white")
        elif kind == "gap":
            box(ax, x + 0.02, y - ch / 2, cw - 0.04, ch, fc=mix(CAT[2], 0.08), ec=CAT[2], lw=1.3, r=0.05, ls=(0, (3, 2)))
        else:
            box(ax, x + 0.02, y - ch / 2, cw - 0.04, ch, fc=FAINT, ec="none", r=0.05)
            label(ax, x + cw / 2, y, b, fs=12, c="#4B5563")
    if note:
        label(ax, x0 + len(seq) * cw + 0.2, y, note, fs=11, c=TEXT2, ha="left")
save(fig, "../../assets/img/w02/small_variants.png")
