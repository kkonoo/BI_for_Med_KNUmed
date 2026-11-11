# W2 §2.2 검사마다 읽는 범위가 다름 — 패널, 엑솜, 전장 유전체, 마이크로어레이와 세 가지 변이 (새로 그림)
import matplotlib.patches as mp
from medfig import *

T0, T1 = 2.3, 6.7                       # genome stretch drawn from T0 to T1 (inches)
S = lambda u: T0 + u * (T1 - T0)        # position along the stretch, 0..1 → inches
fig, ax = new(8.8, 5.4)
YT = 4.25                               # genome track
genes = [  # name, exons as (start, end) fractions of the stretch
    ("유전자 A (패널 목록)", [(0.04, 0.075), (0.115, 0.15), (0.195, 0.23)]),
    ("유전자 B", [(0.34, 0.37), (0.405, 0.435), (0.585, 0.615), (0.65, 0.68)]),
    ("유전자 C", [(0.795, 0.83), (0.885, 0.915)]),
]
exons = [e for _, ex in genes for e in ex]
DEL = (0.75, 0.96)                      # ③ large deletion covering gene C

ax.plot([T0, T1], [YT, YT], color="#C4C7CC", lw=1.2, zorder=1)
for name, ex in genes:
    ax.plot([S(ex[0][0]), S(ex[-1][1])], [YT, YT], color="#6B7280", lw=1.6, zorder=2)
    for a, b in ex:
        box(ax, S(a), YT - 0.14, S(b) - S(a), 0.28, fc="#6B7280", ec="none", r=0.02, z=3)
    label(ax, (S(ex[0][0]) + S(ex[-1][1])) / 2, YT - 0.37, name, fs=11, c=TEXT2)
box(ax, S(DEL[0]), YT - 0.23, S(DEL[1]) - S(DEL[0]), 0.46, fc="none", ec=CAT[2], lw=1.3, r=0.05, z=4,
    ls=(0, (3, 2)))

variants = [  # position, colour, text
    (0.13, CAT[0], "엑손의 SNV"),
    (0.51, CAT[1], "인트론 변이"),
    ((DEL[0] + DEL[1]) / 2, CAT[2], "유전자 C를 덮는 큰 결실"),
]
for k, (u, col, txt) in enumerate(variants):
    x = S(u)
    ax.plot([x, x], [YT + 0.15, YT + 0.38], color=col, lw=1.4, zorder=3)
    num(ax, x, YT + 0.53, k + 1, fc=col, r=0.15, fs=11)
    label(ax, x + 0.22, YT + 0.53, txt, fs=11, w="semibold", c=col, ha="left")

tests = [
    ("유전자 패널", "목록 유전자만, 깊게"),
    ("엑솜", "모든 엑손 = 유전체의 1–2%"),
    ("전장 유전체", "유전체 거의 전부"),
    ("마이크로어레이", "복제수(결실·중복)만"),
]
seen = [(2, 0, 0), (2, 0, 1), (2, 2, 2), (0, 0, 2)]   # ① ② ③ : 2 보임, 1 약함, 0 못 봄
col_x = [7.25, 7.8, 8.35]
for k, x in enumerate(col_x):
    num(ax, x, YT - 0.05, k + 1, fc=variants[k][1], r=0.15, fs=11)
rowc = mix(WINE, 0.55)

def mark(x, y, s, r=0.12):
    if s == 2:
        ax.add_patch(mp.Circle((x, y), r, fc=WINE, ec="none", zorder=3))
    elif s == 1:
        ax.add_patch(mp.Circle((x, y), r, fc="white", ec=WINE, lw=1.4, zorder=3))
        ax.add_patch(mp.Wedge((x, y), r, 90, 270, fc=WINE, ec="none", zorder=4))
    else:
        ax.add_patch(mp.Circle((x, y), r, fc="white", ec="#C4C7CC", lw=1.4, zorder=3))

for r, (name, sub) in enumerate(tests):
    y = 3.25 - r * 0.78
    label(ax, T0 - 0.2, y + 0.1, name, fs=12.5, w="bold", c=TEXT, ha="right")
    label(ax, T0 - 0.2, y - 0.2, sub, fs=11, c=TEXT2, ha="right")
    ax.plot([T0, T1], [y, y], color=LINE, lw=1, zorder=1)
    if r == 0:      # panel: only gene A's exons, read deeply (tall bars)
        for a, b in genes[0][1]:
            box(ax, S(a), y - 0.18, S(b) - S(a), 0.36, fc=rowc, ec="none", r=0.02, z=3)
    elif r == 1:    # exome: every exon
        for a, b in exons:
            box(ax, S(a), y - 0.1, S(b) - S(a), 0.2, fc=rowc, ec="none", r=0.02, z=3)
    elif r == 2:    # genome: everything, evenly
        box(ax, T0, y - 0.07, T1 - T0, 0.14, fc=rowc, ec="none", r=0.03, z=3)
    else:           # array: probes spread out; copy number drops inside the deletion
        for u in np.arange(0.01, 1.0, 0.035):
            inside = DEL[0] < u < DEL[1]
            ax.add_patch(mp.Circle((S(u), y - (0.14 if inside else 0)), 0.035,
                                   fc=CAT[2] if inside else rowc, ec="none", zorder=3))
    for k, s in enumerate(seen[r]):
        mark(col_x[k], y, s)

for k, (s, t) in enumerate([(2, "보임"), (1, "약함"), (0, "못 봄")]):
    x = 6.75 + k * 0.72
    mark(x, 0.35, s, r=0.09)
    label(ax, x + 0.15, 0.35, t, fs=11, c=TEXT2, ha="left")
save(fig, "../../assets/img/w02/test_coverage.png")
