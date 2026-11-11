# W13 §4.1 상대 풍부도의 함정: 실제로는 D만 늘었는데, 비율로 보면 A·B·C가 줄어든 것처럼 보임
# BI_for_Biomed W7 compositional(n5_comp.py)의 숫자를 쓰고, ③은 장 본문의 해결책(총량 × 비율)으로 바꿈
from medfig import *

groups = ["대조군", "환자군"]
absol = np.array([[100, 100, 100, 20],      # 대조군: A, B, C, D (세포 수, 상대 단위)
                  [100, 100, 100, 300]])    # 환자군: D만 늘어남
taxa = ["A", "B", "C", "D"]
cols = [mix(CRIMSON, 0.85), mix(ORANGE, 0.85), mix(AMBER, 0.85), BLUE]   # D = 유일하게 바뀐 것
rel = absol / absol.sum(1, keepdims=True)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.6, 5.0), gridspec_kw={"wspace": 0.8})


def stacked(ax, M, fmt):
    for g in range(2):
        bottom = 0
        for k in range(4):
            v = M[g, k]
            ax.bar(g, v, bottom=bottom, color=cols[k], width=0.66, edgecolor="white", lw=1.2)
            ax.text(g, bottom + v / 2, f"{taxa[k]}  {fmt(v)}", ha="center", va="center", fontsize=11,
                    color="white", fontweight="bold") if v >= M.sum(1).max() * 0.045 else None
            bottom += v
    ax.set_xticks([0, 1])
    ax.set_xticklabels(groups, fontsize=12, fontweight="bold")
    ax.set_xlim(-0.6, 1.6)
    ax.tick_params(length=0, labelsize=11)
    ax.spines["left"].set_color(LINE)
    ax.spines["bottom"].set_color(LINE)


stacked(a1, absol, lambda v: f"{v:.0f}")
a1.set_ylabel("실제 세균 수 (상대 단위)", fontsize=11, color=TEXT2)
a1.set_ylim(0, 680)
a1.text(-0.05, 1.05, "① 장 속의 실제 양", transform=a1.transAxes, fontsize=12.5, fontweight="bold", va="bottom")
a1.text(1, 612, "D만 늘었음", ha="center", va="bottom", fontsize=12, fontweight="bold", color=BLUE)

stacked(a2, rel * 100, lambda v: f"{v:.0f}%")
a2.set_yticks([0, 50, 100])
a2.set_yticklabels(["0%", "50%", "100%"])
a2.set_ylim(0, 107)
a2.text(-0.05, 1.05, "② 시퀀싱 결과 = 비율", transform=a2.transAxes, fontsize=12.5, fontweight="bold", va="bottom")
a2.text(1.42, 33, "A·B·C가\n줄어든 것처럼\n보임", ha="left", va="center", fontsize=11, color=TEXT, linespacing=1.4)

# ② → ①: multiply back by the total
fig.text(0.5, 0.57, "← × 세균 총량\n(예: 16S qPCR)", ha="center", va="center", fontsize=11, color=TEXT,
         fontweight="bold", linespacing=1.4)
fig.text(0.5, 0.43, "총량을 곱하면\n①로 돌아감", ha="center", va="center", fontsize=11, color=TEXT2,
         linespacing=1.4)
save(fig, "../../assets/img/w13/compositional.png")
