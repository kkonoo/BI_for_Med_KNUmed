# W13 §6.2 수평 유전자 전달: 플라스미드에 실린 내성 유전자가 다른 종의 세균으로 옮겨 감
from medfig import *

fig, ax = new(10.4, 3.3)
GENE = BLUE                       # the one thing to follow: the resistance gene


def cell(cx, cy, col, w=2.3, h=1.35):
    box(ax, cx - w / 2, cy - h / 2, w, h, fc=mix(col, 0.12), ec=col, lw=2, r=h / 2)


def chromosome(cx, cy, col, s=1.0):
    th = np.linspace(0, 2 * np.pi, 400)
    r = s * (0.33 + 0.035 * np.sin(4 * th) + 0.025 * np.cos(9 * th))
    ax.plot(cx + 1.25 * r * np.cos(th), cy + 0.8 * r * np.sin(th), color=mix(col, 0.7), lw=1.6, zorder=3)


def plasmid(cx, cy, r=0.17):
    ax.add_patch(mp.Circle((cx, cy), r, fc="none", ec="#6B7280", lw=2.6, zorder=4))
    ax.add_patch(mp.Arc((cx, cy), 2 * r, 2 * r, theta1=20, theta2=130, ec=GENE, lw=4.2, zorder=5))


# ① donor with the plasmid
cell(1.4, 1.9, CRIMSON)
chromosome(1.2, 1.9, CRIMSON)
plasmid(2.15, 2.15)
label(ax, 1.4, 0.95, "① 내성 유전자가 실린\n플라스미드를 가진 세균", fs=10, linespacing=1.4, va="top")

# ② two cells touch and a copy crosses over
cell(4.45, 1.9, CRIMSON, w=1.75)
cell(6.35, 1.9, ORANGE, w=1.75)
ax.add_patch(mp.Rectangle((5.3, 1.8), 0.2, 0.2, fc=mix(CRIMSON, 0.25), ec="none", zorder=1))
chromosome(4.25, 1.9, CRIMSON, s=0.75)
chromosome(6.5, 1.9, ORANGE, s=0.75)
plasmid(4.95, 2.2, r=0.15)
plasmid(5.95, 2.2, r=0.15)
arrow(ax, 5.15, 2.48, 5.75, 2.48, color=GENE, lw=1.8, ms=11, rad=-0.4)
label(ax, 5.4, 0.95, "② 두 세균이 붙어\n플라스미드 복사본을 건넴", fs=10, linespacing=1.4, va="top")

# ③ the recipient, another species, is now resistant
cell(9.0, 1.9, ORANGE)
chromosome(8.8, 1.9, ORANGE)
plasmid(9.75, 2.15)
label(ax, 9.0, 0.95, "③ 다른 종의 세균도\n내성을 얻음", fs=10, linespacing=1.4, va="top")
arrow(ax, 7.4, 1.9, 7.75, 1.9, color="#9AA1AB", lw=2)
arrow(ax, 2.65, 1.9, 3.45, 1.9, color="#9AA1AB", lw=2)

# legend
ax.add_patch(mp.Circle((0.55, 3.05), 0.11, fc="none", ec="#6B7280", lw=2.2))
ax.add_patch(mp.Arc((0.55, 3.05), 0.22, 0.22, theta1=20, theta2=130, ec=GENE, lw=3.6))
label(ax, 0.75, 3.05, "플라스미드와 내성 유전자", fs=9.5, c=TEXT2, ha="left")
th = np.linspace(0, 2 * np.pi, 100)
ax.plot(3.25 + 0.14 * np.cos(th), 3.05 + 0.09 * np.sin(th), color="#9AA1AB", lw=1.4)
label(ax, 3.47, 3.05, "염색체", fs=9.5, c=TEXT2, ha="left")
save(fig, "../../assets/img/w13/hgt_plasmid.png")
