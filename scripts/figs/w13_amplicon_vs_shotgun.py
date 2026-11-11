# W13 §2.2 16S 앰플리콘 vs shotgun: ① 16S 유전자의 보존·가변 영역 ② 무엇을 읽나 ③ 어디까지 이름을 붙이나
# BI_for_Biomed W7 amplicon_vs_shotgun(n3_amplicon.py)을 한글로 다시 그림
from medfig import *

C16, CSH = CRIMSON, ORANGE          # 16S, shotgun (parallel methods)
rng = np.random.default_rng(3)
fig, ax = new(8.2, 6.5)

# ① 16S gene: grey conserved stretches, coloured variable regions V1–V9
label(ax, 0.05, 6.4, "① 16S rRNA 유전자", fs=12.5, w="bold", ha="left")
gx, gw, gy = 0.3, 7.7, 5.05
vreg = [(0.04, 0.03), (0.09, 0.07), (0.28, 0.05), (0.38, 0.07), (0.54, 0.04), (0.65, 0.04),
        (0.74, 0.04), (0.82, 0.04), (0.95, 0.02)]
box(ax, gx, gy, gw, 0.32, fc="#D5D9DF", ec="none", r=0.04)
for k, (s, w) in enumerate(vreg):
    ax.add_patch(mp.Rectangle((gx + s * gw, gy), w * gw, 0.32, fc=mix(C16, 0.8), ec="none", zorder=3))
    label(ax, gx + (s + w / 2) * gw, gy - 0.2, f"V{k + 1}", fs=11, c=TEXT2)
# primers sit on the conserved stretches either side of V3–V4 and point at each other
p1a, p1b = gx + 0.19 * gw, gx + 0.265 * gw
p2a, p2b = gx + 0.535 * gw, gx + 0.46 * gw
arrow(ax, p1a, gy + 0.45, p1b, gy + 0.45, color=TEXT, lw=2, ms=11)
arrow(ax, p2a, gy + 0.45, p2b, gy + 0.45, color=TEXT, lw=2, ms=11)
ax.plot([p1a, p1a, p2a, p2a], [gy + 0.55, gy + 0.68, gy + 0.68, gy + 0.55], color=TEXT2, lw=1)
label(ax, (p1a + p2a) / 2, gy + 0.9, "프라이머(→ ←) 사이를 증폭해 읽음 (예: V3–V4)", fs=11, c=TEXT)
label(ax, gx, gy - 0.55, "회색 = 보존 영역 (세균마다 거의 같음)   색 = 가변 영역 (세균마다 다름)",
      fs=11, c=TEXT2, ha="left")

# ② what gets read from one sample
label(ax, 0.05, 4.05, "② 시료 하나에서 무엇을 읽나", fs=12.5, w="bold", ha="left")
gx2, gw2 = 0.15, 1.6
genomes = [("세균 1", 3.42), ("세균 2", 3.14), ("세균 3", 2.86), ("사람", 2.54)]
for nm, y in genomes:
    human = nm == "사람"
    box(ax, gx2, y - 0.07, gw2, 0.14, fc="#9AA1AB" if human else "#D5D9DF", ec="none", r=0.03)
    if not human:
        ax.add_patch(mp.Rectangle((gx2 + 0.35, y - 0.07), 0.16, 0.14, fc=C16, ec="none", zorder=3))
    label(ax, gx2 + gw2 + 0.1, y, nm, fs=11, c=TEXT2, ha="left")
label(ax, gx2 + 0.43, 3.7, "16S 유전자", fs=11, c=C16, w="bold")

cx = 3.15
label(ax, cx, 3.55, "16S 앰플리콘", fs=12, w="bold", c=C16, ha="left")
for k in range(12):
    ax.add_patch(mp.Rectangle((cx + (k % 6) * 0.23, 3.2 - (k // 6) * 0.2), 0.17, 0.1, fc=C16, ec="none"))
label(ax, cx + 1.6, 3.2, "16S 한 조각만 복사해 읽음\n→ 누가 있나", fs=11, c=TEXT, ha="left", linespacing=1.4)
label(ax, cx, 2.6, "Shotgun", fs=12, w="bold", c=CSH, ha="left")
pool = ["#D5D9DF"] * 7 + [C16] * 1 + ["#9AA1AB"] * 4
rng.shuffle(pool)
for k, c in enumerate(pool):
    ax.add_patch(mp.Rectangle((cx + (k % 6) * 0.23, 2.25 - (k // 6) * 0.2), rng.uniform(0.12, 0.2), 0.1,
                              fc=c, ec="none"))
label(ax, cx + 1.6, 2.25, "모든 DNA를 무작위 조각으로 읽음\n→ 누가 있나 + 어떤 유전자가 있나", fs=11, c=TEXT,
      ha="left", linespacing=1.4)
arrow(ax, gx2 + gw2 + 0.65, 3.3, cx - 0.12, 3.15, color="#9AA1AB", lw=1.2, ms=9, rad=-0.1)
arrow(ax, gx2 + gw2 + 0.65, 2.85, cx - 0.12, 2.2, color="#9AA1AB", lw=1.2, ms=9, rad=0.15)

# ③ how far down each can name: levels across, methods down
label(ax, 0.05, 1.88, "③ 어디까지 이름을 붙이나", fs=12.5, w="bold", ha="left")
levels = ["문\n(phylum)", "과\n(family)", "속\n(genus)", "종\n(species)", "균주\n(strain)", "기능\n유전자"]
marks = {"16S": [2, 2, 2, 1, 0, 0], "Shotgun": [2, 2, 2, 2, 1, 2]}
rows = {"16S": (0.98, C16), "Shotgun": (0.58, CSH)}
x0, dx = 1.95, 1.1


def dot(x, y, m, c, r=0.11):
    if m == 2:
        ax.add_patch(mp.Circle((x, y), r, fc=c, ec="none", zorder=3))
    elif m == 1:
        ax.add_patch(mp.Circle((x, y), r, fc="white", ec=c, lw=1.4, zorder=3))
        ax.add_patch(mp.Wedge((x, y), r, 90, 270, fc=c, ec="none", zorder=4))
    else:
        ax.add_patch(mp.Circle((x, y), r, fc="white", ec="#C4C7CC", lw=1.2, zorder=3))


for i, lv in enumerate(levels):
    label(ax, x0 + i * dx, 1.43, lv, fs=11, linespacing=1.25)
ax.plot([x0 + 4.5 * dx] * 2, [0.42, 1.66], color=LINE, lw=0.9)
for nm, (y, c) in rows.items():
    label(ax, 0.15, y, nm, fs=12, w="bold", c=c, ha="left")
    for i in range(len(levels)):
        dot(x0 + i * dx, y, marks[nm][i], c)
for k, (lab, m) in enumerate((("믿을 만함", 2), ("불확실", 1), ("안 됨", 0))):
    x = x0 - 0.1 + k * 1.45
    dot(x, 0.15, m, TEXT2, r=0.08)
    label(ax, x + 0.16, 0.15, lab, fs=11, c=TEXT2, ha="left")
save(fig, "../../assets/img/w13/amplicon_vs_shotgun.png")
