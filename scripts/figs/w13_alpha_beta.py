# W13 §3 다양성: ① alpha = 한 시료 안 (장 본문 표의 공동체 A·B) ② beta = 시료끼리 (PCoA, 가상의 예)
# BI_for_Biomed W7 diversity(n4_diversity.py)를 장 본문에 맞춰 단순하게 다시 그림
from medfig import *

rng = np.random.default_rng(4)
genus_cols = [CRIMSON, ORANGE, WINE, AMBER]          # 네 속 (나란한 항목)

fig = plt.figure(figsize=(10.4, 4.4))
ax = fig.add_axes([0, 0, 0.56, 1])
ax.set_xlim(0, 5.82); ax.set_ylim(0, 4.4); ax.axis("off")
label(ax, 0.1, 4.2, "① Alpha 다양성 — 한 시료 안", fs=11.5, w="bold", ha="left")


def community(cx, cy, counts, name, shannon):
    """20 cells in a 5 × 4 grid inside a rounded frame, coloured by genus."""
    box(ax, cx - 1.15, cy - 1.0, 2.3, 2.0, fc=FAINT, ec="none", r=0.18)
    cells = [k for k, n in enumerate(counts) for _ in range(n)]
    order = rng.permutation(len(cells))
    for i, j in enumerate(order):
        x = cx - 0.84 + (i % 5) * 0.42
        y = cy + 0.63 - (i // 5) * 0.42
        ax.add_patch(mp.Circle((x, y), 0.15, fc=genus_cols[cells[j]], ec="none", zorder=3))
    label(ax, cx, cy + 1.22, name, fs=11, w="bold")
    label(ax, cx, cy - 1.3, "종류 4", fs=10, c=TEXT)
    label(ax, cx, cy - 1.62, f"Shannon {shannon}", fs=10.5, w="bold", c=TEXT)


community(1.45, 2.45, [5, 5, 5, 5], "공동체 A — 고르게", "1.39")
community(4.25, 2.45, [14, 2, 2, 2], "공동체 B — 한 속이 독차지", "0.94")
label(ax, 2.85, 0.3, "종류 수는 같아도, 한 종류가 독차지할수록 Shannon 지수가 작아짐", fs=9.8, c=TEXT2)

# ② beta: PCoA of two groups of samples (illustrative)
b = fig.add_axes([0.66, 0.16, 0.32, 0.66])
g1 = rng.normal([-1.0, 0.35], 0.26, (12, 2))
g2 = rng.normal([1.0, -0.35], 0.3, (12, 2))
b.scatter(*g1.T, s=46, color=CRIMSON, lw=0, label="건강인")
b.scatter(*g2.T, s=46, color=ORANGE, lw=0, label="항생제 치료 뒤")
b.set_xlabel("PCoA 1", fontsize=10, color=TEXT2)
b.set_ylabel("PCoA 2", fontsize=10, color=TEXT2)
b.set_xticks([]); b.set_yticks([])
b.spines["left"].set_color(LINE); b.spines["bottom"].set_color(LINE)
b.legend(frameon=False, fontsize=9.5, loc="upper left", bbox_to_anchor=(-0.02, 1.02), handletextpad=0.2)
b.set_ylim(-1.6, 1.7)
fig.text(0.66, 0.955, "② Beta 다양성 — 시료끼리", fontsize=11.5, fontweight="bold", va="center")
fig.text(0.66, 0.05, "점 하나 = 시료 하나. 가까울수록 비슷한 공동체", fontsize=9.8, color=TEXT2, va="center")
save(fig, "../../assets/img/w13/alpha_beta.png")
