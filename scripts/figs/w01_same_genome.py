# W1 §2.3 같은 유전체, 다른 세포: DNA는 같고, 어떤 유전자를 켜느냐(RNA)가 다름 — 예시 그림
from medfig import *

fig, ax = new(9.8, 4.1)
genes = [("공통 유전자", "#9AA1AB"), ("신경 유전자", CAT[0]), ("간 유전자\n(예: 알부민)", CAT[1])]
cells = [("신경세포", 0.35, [0.55, 0.95, 0.0]), ("간세포", 5.5, [0.55, 0.0, 0.95])]
CW = 4.2                                     # column width

def neuron(cx, cy, c):
    for ang in (100, 140, 200, 240, 60):
        a = np.radians(ang)
        ax.plot([cx, cx + 0.42 * np.cos(a)], [cy, cy + 0.42 * np.sin(a)], color=c, lw=2.2,
                solid_capstyle="round", zorder=2)
    ax.plot([cx, cx + 0.62], [cy, cy - 0.08], color=c, lw=2.2, solid_capstyle="round", zorder=2)
    ax.add_patch(mp.Circle((cx, cy), 0.19, fc=c, ec="none", zorder=3))
    ax.add_patch(mp.Circle((cx, cy), 0.07, fc="white", ec="none", zorder=4))

def hepatocyte(cx, cy, c):
    ax.add_patch(mp.RegularPolygon((cx, cy), 6, radius=0.34, fc=mix(c, 0.35), ec=c, lw=1.6, zorder=3))
    ax.add_patch(mp.Circle((cx, cy), 0.1, fc=c, ec="none", zorder=4))

for (name, x0, expr), draw in zip(cells, (neuron, hepatocyte)):
    c = CAT[0] if name == "신경세포" else CAT[1]
    draw(x0 + 0.45, 3.65, c)
    label(ax, x0 + 1.3 if name == "신경세포" else x0 + 0.95, 3.65, name, fs=13.5, w="bold", c=c, ha="left")
    # DNA: the same three genes in both cells
    label(ax, x0, 2.92, "DNA", fs=10, w="bold", c=TEXT2, ha="left")
    gx = [x0 + 0.75 + k * 1.15 for k in range(3)]
    ax.plot([x0 + 0.55, x0 + CW], [2.92, 2.92], color="#C4C8CF", lw=2, zorder=1)
    for (g, gc), xg in zip(genes, gx):
        box(ax, xg, 2.8, 0.85, 0.24, fc=gc, ec="none", r=0.04)
    # RNA: how much of each gene is switched on
    label(ax, x0, 1.95, "RNA", fs=10, w="bold", c=TEXT2, ha="left")
    ax.plot([x0 + 0.55, x0 + CW], [1.25, 1.25], color="#C4C8CF", lw=1)
    for (g, gc), xg, e in zip(genes, gx, expr):
        if e > 0:
            box(ax, xg + 0.17, 1.25, 0.5, 1.15 * e, fc=mix(gc, 0.75), ec="none", r=0.03)
        else:
            label(ax, xg + 0.42, 1.38, "꺼짐", fs=9, c=TEXT2)
        label(ax, xg + 0.42, 0.95 if "\n" not in g else 0.86, g, fs=9, c=TEXT, linespacing=1.2)

# what is the same and what differs, between the two columns
ax.plot([4.95, 4.95], [0.75, 3.3], color=LINE, lw=1, zorder=0)
for t_, y in [("같음", 2.92), ("다름", 1.85)]:
    box(ax, 4.95 - 0.3, y - 0.17, 0.6, 0.34, fc="white", ec=LINE, r=0.17, z=6)
    label(ax, 4.95, y, t_, fs=10.5, w="bold", c=TEXT, z=7)
box(ax, 0.35, 0.05, 9.35, 0.44, fc=FAINT, ec="none", r=0.08)
label(ax, 0.55, 0.27, "진료에서", fs=10, w="bold", c=TEXT, ha="left")
label(ax, 1.5, 0.27, "유전 질환 검사 → 혈액이나 침의 DNA로 가능", fs=9.8, c=TEXT, ha="left")
label(ax, 5.5, 0.27, "발현 검사 → 병이 있는 조직을, 적절한 시점에", fs=9.8, c=TEXT, ha="left")
save(fig, "../../assets/img/w01/same_genome.png")
