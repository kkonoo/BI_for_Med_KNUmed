# W6 §1.2 상황별로 기대되는 VAF (두 벌 염색체 중 한쪽에만 변이가 있을 때)
#   생식세포 이형접합 변이: VAF ≈ 50% (종양 세포든 정상 세포든 모두 가짐)
#   체세포 변이: VAF ≈ 종양 순도 × 그 변이를 가진 종양 세포 비율 ÷ 2
from medfig import *

GERM, SOMA = WINE, ORANGE           # same colours as germline_somatic.png
rows = [  # label line 1, line 2, VAF %, germline?
    ("생식세포 이형접합 변이", "종양 순도와 상관없이", 50, True),
    ("체세포 변이 · 모든 종양 세포", "종양 순도 100%", 50, False),
    ("체세포 변이 · 모든 종양 세포", "종양 순도 60%", 30, False),
    ("체세포 변이 · 종양 세포의 20%", "종양 순도 60%", 6, False),
]

fig, ax = plt.subplots(figsize=(6.9, 4.1))
ys = np.arange(len(rows))[::-1]
for y, (l1, l2, v, g) in zip(ys, rows):
    ax.barh(y, v, height=0.56, color=GERM if g else SOMA)
    ax.text(v - 1.2 if v > 10 else v + 1.0, y, f"{v}%", ha="right" if v > 10 else "left", va="center",
            fontsize=12.5, fontweight="bold", color="white" if v > 10 else SOMA)
    ax.text(-2.5, y + 0.13, l1, ha="right", va="center", fontsize=12, fontweight="semibold",
            color=GERM if g else SOMA)
    ax.text(-2.5, y - 0.2, l2, ha="right", va="center", fontsize=11, color=TEXT2)

ax.axvline(32, color=BLUE, lw=1.6, ls=(0, (4, 3)), zorder=3)
ax.text(32.8, 3.47, "케이스 EGFR VAF 32%", color=BLUE, fontsize=12, fontweight="bold", va="center")
ax.set_xlim(0, 60); ax.set_ylim(-0.5, 3.75)
ax.set_xticks(range(0, 61, 10)); ax.set_xticklabels([f"{t}%" for t in range(0, 61, 10)])
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.set_xlabel("기대되는 변이 대립유전자 빈도 (VAF)", fontsize=11, color=TEXT)
ax.tick_params(axis="x", labelsize=11)
save(fig, "../../assets/img/w06/vaf_expected.png")
