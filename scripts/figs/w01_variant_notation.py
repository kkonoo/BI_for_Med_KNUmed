# W1 §4.3 변이 하나를 네 가지로 부름: 유전체 좌표 · c. · p. · rs 번호 (W3 실습의 SCN1A 변이)
from medfig import *

MONO = "DejaVu Sans Mono"
fig, ax = new(10.4, 4.6)
VX = 6.9                                   # the one variant, same x in every row
rows = [  # y, colour, name, what it describes
    (4.0, CAT[0], "유전체 좌표", "염색체 위의 번지"),
    (2.9, CAT[1], "코딩 서열 (c.)", "유전자 안 몇 번째 염기"),
    (1.8, CAT[2], "단백질 (p.)", "몇 번째 아미노산"),
    (0.7, CAT[3], "rs 번호", "데이터베이스의 이름표"),
]
for y, c, name, what in rows:
    label(ax, 0.1, y + 0.14, name, fs=12.5, w="bold", c=c, ha="left")
    label(ax, 0.1, y - 0.17, what, fs=9.5, c=TEXT2, ha="left")

# the variant: one blue line through all four rows
ax.plot([VX, VX], [0.45, 4.35], color=BLUE, lw=1.6, ls=(0, (4, 3)), zorder=1)

# ① chromosome 2 (variant at 166.0 of ~242 Mb → same relative place)
y, c = rows[0][:2]
cx0, cx1 = 2.3, 9.0
box(ax, cx0, y - 0.13, cx1 - cx0, 0.26, fc=mix(c, 0.22), ec=mix(c, 0.5), r=0.13)
label(ax, cx0, y + 0.33, "2번 염색체 (GRCh38 기준)", fs=9.5, c=TEXT2, ha="left")
ax.add_patch(mp.Circle((VX, y), 0.09, fc=BLUE, ec="white", lw=1.2, zorder=6))
label(ax, VX + 0.18, y + 0.33, "chr2:166002537 G>A", fs=11, w="bold", c=c, ha="left", fontfamily=MONO)

# ② SCN1A gene, read on the opposite strand (←)
y, c = rows[1][:2]
gx0, gx1 = 4.6, 9.0
ax.plot([gx0, gx1], [y, y], color=mix(c, 0.6), lw=1.4, zorder=2)
exons = [(4.75, 0.14), (5.3, 0.12), (5.85, 0.16), (6.35, 0.12), (6.82, 0.18), (7.4, 0.12),
         (7.95, 0.14), (8.45, 0.12), (8.82, 0.1)]
for xe, we in exons:
    box(ax, xe, y - 0.15, we, 0.3, fc=c, ec="none", r=0.02, z=4)
mids = [(a + wa + b) / 2 for (a, wa), (b, _) in zip(exons, exons[1:])]
ax.plot(mids, [y] * len(mids), ls="none", marker="<", ms=5, color=mix(c, 0.7), zorder=3)
ax.add_patch(mp.Circle((VX, y), 0.09, fc=BLUE, ec="white", lw=1.2, zorder=6))
label(ax, VX + 0.18, y + 0.36, "SCN1A c.4219C>T", fs=11, w="bold", c=c, ha="left", fontfamily=MONO)
label(ax, 2.3, y + 0.1, "SCN1A 유전자 (확대)", fs=9.5, c=TEXT2, ha="left")
label(ax, 2.3, y - 0.36, "반대쪽 가닥에서 읽는 유전자(←) → 유전체의 G>A가 C>T로 보임", fs=9.3, c=TEXT2,
      ha="left")

# ③ protein: stop codon at 1,407 → the rest is never made
y, c = rows[2][:2]
px0, px1 = 2.3, 9.0
box(ax, px0, y - 0.13, VX - px0, 0.26, fc=mix(c, 0.35), ec="none", r=0.06)
box(ax, VX, y - 0.13, px1 - VX, 0.26, fc="white", ec=mix(c, 0.45), r=0.06, ls=(0, (3, 2)))
label(ax, (VX + px1) / 2, y, "만들어지지 않음", fs=9.3, c=TEXT2)
ax.add_patch(mp.Circle((VX, y), 0.09, fc=BLUE, ec="white", lw=1.2, zorder=6))
label(ax, VX - 0.18, y + 0.33, "p.Arg1407Ter", fs=11, w="bold", c=c, ha="right", fontfamily=MONO)
label(ax, VX + 0.18, y + 0.33, "CGA (Arg) → TGA (종결 코돈)", fs=9.5, c=TEXT, ha="left")

# ④ dbSNP name tag
y, c = rows[3][:2]
ax.add_patch(mp.Circle((VX, y), 0.09, fc=BLUE, ec="white", lw=1.2, zorder=6))
box(ax, VX + 0.25, y - 0.2, 1.9, 0.4, fc=mix(c, 0.15), ec=c, lw=1.2, r=0.08)
label(ax, VX + 0.25 + 0.95, y, "rs398123593", fs=11, w="bold", c=TEXT, fontfamily=MONO)
ax.plot([VX + 0.09, VX + 0.25], [y, y], color=c, lw=1.2)
label(ax, VX - 0.2, y, "dbSNP가 붙인 이름", fs=9.5, c=TEXT2, ha="right")
save(fig, "../../assets/img/w01/variant_notation.png")
