# W2 §5.2 트리오 분석 — 부모는 0/0, 아이만 0/1인 de novo 변이 (§3.3 VCF 줄과 같은 위치·깊이, 새로 그림)
import matplotlib.patches as mp
from medfig import *

fig, ax = new(9.6, 5.0)
S = 0.42                                    # pedigree symbol size
F, M, C = (3.55, 4.35), (6.05, 4.35), (4.8, 3.15)   # father, mother, child centres

# pedigree: unaffected parents (open), affected child (filled)
ax.add_patch(mp.Rectangle((F[0] - S / 2, F[1] - S / 2), S, S, fc="white", ec=TEXT, lw=1.6, zorder=3))
ax.add_patch(mp.Circle(M, S / 2, fc="white", ec=TEXT, lw=1.6, zorder=3))
ax.add_patch(mp.Rectangle((C[0] - S / 2, C[1] - S / 2), S, S, fc=TEXT, ec=TEXT, lw=1.6, zorder=3))
ax.plot([F[0] + S / 2, M[0] - S / 2], [F[1], F[1]], color=TEXT, lw=1.4)
ax.plot([C[0], C[0]], [F[1], C[1] + S / 2], color=TEXT, lw=1.4)
label(ax, F[0], F[1] + 0.38, "아버지 (건강)", fs=11.5, w="semibold")
label(ax, M[0], M[1] + 0.38, "어머니 (건강)", fs=11.5, w="semibold")
label(ax, C[0] + 0.35, C[1], "아이 (발달지연·경련)", fs=11.5, w="semibold", ha="left")

def pileup(x0, yc, bases, gt, depth):
    """A few reads over the variant position (centre column); x0 = left edge."""
    RW, CW = 1.9, 0.26
    xc = x0 + RW / 2
    shifts = [-0.35, 0.2, -0.1, 0.4, -0.25, 0.05]
    for i, b in enumerate(bases):
        y = yc + 0.42 - i * 0.17
        s = shifts[i]
        box(ax, x0 + s * 0.6 + 0.1, y - 0.045, RW - 0.4, 0.09, fc="#D5D8DD", ec="none", r=0.045, z=2)
        hot = b == "A"
        box(ax, xc - CW / 2, y - 0.085, CW, 0.17, fc=CRIMSON if hot else "white", ec="none" if hot else LINE,
            lw=0.8, r=0.03, z=3)
        label(ax, xc, y, b, fs=10.5, w="bold", c="white" if hot else "#4B5563", z=4)
    ax.plot([xc, xc], [yc + 0.56, yc - 0.56], color="#9AA1AB", lw=0.9, ls=(0, (2, 2)), zorder=1)
    label(ax, xc, yc - 0.77, f"{gt}  ·  깊이 {depth}", fs=12, w="bold", c=CRIMSON if gt == "0/1" else TEXT)

pileup(F[0] - 2.55, F[1] - 0.3, "GGGGGG", "0/0", 48)
pileup(M[0] + 0.45, M[1] - 0.3, "GGGGGG", "0/0", 51)
pileup(C[0] - 0.95, C[1] - 1.12, "GAGAAG", "0/1", 54)
label(ax, 4.8, 5.2, "chr2:166002537  G>A", fs=11.5, w="semibold", c=TEXT2)

label(ax, 5.95, 2.2, "부모는 G만, 아이에게만 A", fs=12, w="bold", c=BLUE, ha="left")
label(ax, 5.95, 1.92, "→ 새로 생긴 변이 (de novo)", fs=12, w="bold", c=BLUE, ha="left")
label(ax, 5.95, 1.5, "확인할 것: 친부모가 맞는지,", fs=11, c=TEXT2, ha="left")
label(ax, 5.95, 1.25, "부모 쪽 깊이가 충분한지", fs=11, c=TEXT2, ha="left")
save(fig, "../../assets/img/w02/trio_denovo.png")
