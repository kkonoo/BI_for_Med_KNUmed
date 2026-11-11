# W13 §3 다양성: ① alpha = 한 시료 안 (장 본문 표의 공동체 A·B) ② beta = 시료끼리 (PCoA, 가상의 예)
# BI_for_Biomed W7 diversity(n4_diversity.py)를 장 본문에 맞춰 단순하게 다시 그림
from medfig import *

rng = np.random.default_rng(4)
genus_cols = [CRIMSON, ORANGE, WINE, AMBER]          # 네 속 (나란한 항목)

W, H = 8.0, 7.2
fig = plt.figure(figsize=(W, H))
top = 0.46
ax = fig.add_axes([0, top, 1, 1 - top])
ax.set_xlim(0, W); ax.set_ylim(0, H * (1 - top)); ax.axis("off")
label(ax, 0.05, 3.78, "① Alpha 다양성 — 한 시료 안", fs=12.5, w="bold", ha="left")


def community(cx, cy, counts, name, shannon):
    """20 cells in a 5 × 4 grid inside a rounded frame, coloured by genus."""
    box(ax, cx - 1.2, cy - 1.02, 2.4, 2.04, fc=FAINT, ec="none", r=0.18)
    cells = [k for k, n in enumerate(counts) for _ in range(n)]
    order = rng.permutation(len(cells))
    for i, j in enumerate(order):
        x = cx - 0.88 + (i % 5) * 0.44
        y = cy + 0.66 - (i // 5) * 0.44
        ax.add_patch(mp.Circle((x, y), 0.16, fc=genus_cols[cells[j]], ec="none", zorder=3))
    label(ax, cx, cy + 1.27, name, fs=12, w="bold")
    label(ax, cx, cy - 1.3, "종류 4", fs=11, c=TEXT)
    label(ax, cx, cy - 1.64, f"Shannon {shannon}", fs=12, w="bold", c=TEXT)


community(2.2, 2.12, [5, 5, 5, 5], "공동체 A — 고르게", "1.39")
community(5.8, 2.12, [14, 2, 2, 2], "공동체 B — 한 속이 독차지", "0.94")
label(ax, W / 2, 0.06, "종류 수는 같아도 한 종류가 독차지하면 Shannon 지수가 작아짐", fs=11, c=TEXT2)

# ② beta: PCoA of two groups of samples (illustrative)
fig.text(0.006, 0.415, "② Beta 다양성 — 시료끼리", fontsize=12.5, fontweight="bold", va="center")
b = fig.add_axes([0.07, 0.06, 0.44, 0.30])
g1 = rng.normal([-1.0, 0.35], 0.26, (12, 2))
g2 = rng.normal([1.0, -0.35], 0.3, (12, 2))
b.scatter(*g1.T, s=55, color=CRIMSON, lw=0, label="건강인")
b.scatter(*g2.T, s=55, color=ORANGE, lw=0, label="항생제 치료 뒤")
b.set_xlabel("PCoA 1", fontsize=11, color=TEXT2)
b.set_ylabel("PCoA 2", fontsize=11, color=TEXT2)
b.set_xticks([]); b.set_yticks([])
b.spines["left"].set_color(LINE); b.spines["bottom"].set_color(LINE)
b.set_ylim(-1.6, 1.7)
fig.legend(*b.get_legend_handles_labels(), frameon=False, fontsize=11.5, loc="upper left",
           bbox_to_anchor=(0.58, 0.33), handletextpad=0.3, labelspacing=0.8)
fig.text(0.58, 0.14, "점 하나 = 시료 하나\n가까울수록 비슷한 공동체", fontsize=11, color=TEXT2, va="center",
         linespacing=1.5)
save(fig, "../../assets/img/w13/alpha_beta.png")
