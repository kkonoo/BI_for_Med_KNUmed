# W1 §2.3 같은 유전체, 다른 세포: DNA는 같고, 어떤 유전자를 켜느냐(RNA)가 다름 — 예시 그림
from medfig import *

fig, ax = new(8.4, 4.75)
genes = [("공통 유전자", "#9AA1AB"), ("신경 유전자", CAT[0]), ("간 유전자", CAT[1])]
cells = [("신경세포", 0.0, [0.55, 0.95, 0.0]), ("간세포", 4.55, [0.55, 0.0, 0.95])]
CW = 3.85                                    # column width
GX = [0.62, 1.72, 2.82]                      # gene x offsets inside a column
GW = 0.86                                    # gene box width

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
    draw(x0 + 0.45, 4.3, c)
    label(ax, x0 + (1.3 if name == "신경세포" else 0.95), 4.3, name, fs=14, w="bold", c=c, ha="left")
    # DNA: the same three genes in both cells
    label(ax, x0, 3.55, "DNA", fs=11, w="bold", c=TEXT2, ha="left")
    ax.plot([x0 + 0.5, x0 + CW], [3.55, 3.55], color="#C4C8CF", lw=2, zorder=1)
    for (g, gc), gx in zip(genes, GX):
        box(ax, x0 + gx, 3.43, GW, 0.24, fc=gc, ec="none", r=0.04)
    # RNA: how much of each gene is switched on
    label(ax, x0, 2.55, "RNA", fs=11, w="bold", c=TEXT2, ha="left")
    ax.plot([x0 + 0.5, x0 + CW], [1.85, 1.85], color="#C4C8CF", lw=1)
    for (g, gc), gx, e in zip(genes, GX, expr):
        xc = x0 + gx + GW / 2
        if e > 0:
            box(ax, xc - 0.25, 1.85, 0.5, 1.15 * e, fc=mix(gc, 0.75), ec="none", r=0.03)
        else:
            label(ax, xc, 2.0, "꺼짐", fs=11, c=TEXT2)
        label(ax, xc, 1.6, g, fs=11, c=TEXT)

# what is the same and what differs, between the two columns
xm = (CW + 4.55) / 2
ax.plot([xm, xm], [1.4, 3.95], color=LINE, lw=1, zorder=0)
for t_, y in [("같음", 3.55), ("다름", 2.5)]:
    box(ax, xm - 0.32, y - 0.18, 0.64, 0.36, fc="white", ec=LINE, r=0.18, z=6)
    label(ax, xm, y, t_, fs=11, w="bold", c=TEXT, z=7)
label(ax, 4.55 + GX[2] + GW / 2, 1.3, "(예: 알부민)", fs=11, c=TEXT2)

# what this means for testing
box(ax, 0.0, 0.0, 8.4, 0.95, fc=FAINT, ec="none", r=0.08)
label(ax, 0.2, 0.475, "진료에서", fs=12, w="bold", c=TEXT, ha="left")
label(ax, 1.35, 0.66, "유전 질환 검사 → 혈액이나 침의 DNA로 가능", fs=11, c=TEXT, ha="left")
label(ax, 1.35, 0.29, "발현 검사 → 병이 있는 조직을, 적절한 시점에", fs=11, c=TEXT, ha="left")
save(fig, "../../assets/img/w01/same_genome.png")
