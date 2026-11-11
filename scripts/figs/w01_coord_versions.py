# W1 §4.3 레퍼런스 버전이 다르면 같은 변이도 좌표가 다름: CYP2C19*2 (rs4244285)
from medfig import *

MONO = "DejaVu Sans Mono"
fig, ax = new(8.4, 3.2)
lo, hi = 93.6, 97.4                       # chr10, Mb shown on both rulers
X0, X1 = 1.75, 8.3
xm = lambda mb: X0 + (mb - lo) / (hi - lo) * (X1 - X0)
rows = [(2.45, CAT[0], "GRCh37", "옛 버전", 96.541616, "chr10:96541616"),
        (0.8, CAT[1], "GRCh38", "현재 표준", 94.781859, "chr10:94781859")]
for y, c, ver, note, pos, txt in rows:
    label(ax, 0.0, y + 0.12, ver, fs=13, w="bold", c=c, ha="left")
    label(ax, 0.0, y - 0.22, note, fs=11, c=TEXT2, ha="left")
    box(ax, X0, y - 0.09, X1 - X0, 0.18, fc=mix(c, 0.18), ec="none", r=0.09)
    for mb in (94, 95, 96, 97):
        ax.plot([xm(mb)] * 2, [y - 0.09, y - 0.17], color="#9AA1AB", lw=1)
        label(ax, xm(mb), y - 0.33, f"{mb} Mb", fs=11, c=TEXT2)
    ax.add_patch(mp.Circle((xm(pos), y), 0.1, fc=c, ec="white", lw=1.2, zorder=6))
    if ver == "GRCh37":
        label(ax, xm(pos), y + 0.34, txt, fs=11.5, w="bold", c=c, fontfamily=MONO)
    else:
        label(ax, xm(pos) - 0.18, y + 0.3, txt, fs=11.5, w="bold", c=c, fontfamily=MONO, ha="right")

# same variant, two addresses
x37, x38 = xm(rows[0][4]), xm(rows[1][4])
arrow(ax, x37, rows[0][0] - 0.12, x38, rows[1][0] + 0.14, color="#9AA1AB", lw=1.4, ls=(0, (4, 3)))
label(ax, X0, 1.74, "같은 변이 rs4244285 (CYP2C19 *2)", fs=12, w="semibold", c=TEXT, ha="left")
label(ax, X0, 1.44, "→ 어느 버전 기준인지 확인", fs=11, c=TEXT2, ha="left")
save(fig, "../../assets/img/w01/coord_versions.png")
