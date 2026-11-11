# W9 §4.1 깊이와 조성 때문에 raw count가 달라짐 (BI_for_MD_PhD W4 normalization을 다시 그림; 자료는 가상)
from medfig import *

rng = np.random.default_rng(4)
GREY, TREAT = "#C9CED6", mix(CRIMSON, 0.6)
n = 3000
mu = rng.lognormal(mean=2.0, sigma=1.6, size=n)            # 유전자마다 실제 발현량 (두 군이 같음)
depth = np.array([1.0, 0.95, 1.05, 3.0, 3.1, 2.9])          # 처리군을 약 3배 깊게 읽음
counts = np.array([rng.poisson(mu * d) for d in depth])
ref = np.exp(np.mean(np.log(counts + 1), axis=0))
sf = np.array([np.median((c + 1) / ref) for c in counts])
norm = counts / sf[:, None]
labels = ["C1", "C2", "C3", "T1", "T2", "T3"]
colors = [GREY] * 3 + [TREAT] * 3

fig, axes = plt.subplots(1, 3, figsize=(11, 4.4), gridspec_kw={"wspace": 0.38})


def tag(ax, t):
    ax.text(0, 1.05, t, transform=ax.transAxes, ha="left", va="bottom", fontsize=11.5, fontweight="bold", color=TEXT)


def boxes(ax, data):
    bp = ax.boxplot([np.log2(d + 1) for d in data], widths=0.6, patch_artist=True, showfliers=False,
                    medianprops=dict(color=TEXT, lw=1.4), whiskerprops=dict(color="#9AA1AB"),
                    capprops=dict(color="#9AA1AB"))
    for b, c in zip(bp["boxes"], colors):
        b.set(facecolor=c, edgecolor="none")
    ax.set_xticks(range(1, 7)); ax.set_xticklabels(labels, fontsize=10)
    for t, c in zip(ax.get_xticklabels(), ["#6B7280"] * 3 + [CRIMSON] * 3):
        t.set_color(c)
    ax.set_ylim(-0.3, 13.2)
    ax.spines["left"].set_color(LINE); ax.spines["bottom"].set_color(LINE)
    ax.tick_params(length=0, labelsize=9.5)


# ① raw count
ax = axes[0]
boxes(ax, counts)
ax.set_ylabel("log₂(count + 1)", fontsize=10, color=TEXT2)
ax.text(3.5, 12.3, "처리군(T)을 약 3배 더 깊게 읽음\n→ 모든 유전자가 \"증가\"해 보임", ha="center", va="center",
        fontsize=9.5, color=WINE, linespacing=1.45)
tag(ax, "① raw count")

# ② 정규화 후
ax = axes[1]
boxes(ax, norm)
ax.set_ylabel("log₂(정규화 count + 1)", fontsize=10, color=TEXT2)
ax.text(3.5, 12.3, "깊이 차이를 보정\n→ 시료끼리 비교할 수 있음", ha="center", va="center",
        fontsize=9.5, color=TEXT, linespacing=1.45)
tag(ax, "② 정규화 후")

# ③ 조성 효과: 깊이는 같고 유전자 X 하나가 폭증
ax = axes[2]
genes = ["A", "B", "C", "D", "X"]
ctrl = np.array([24, 24, 24, 24, 4]) * 10           # 라이브러리 비율 (‰)
trt = np.array([7.5, 7.5, 7.5, 7.5, 70]) * 10
X = np.arange(5); w = 0.38
ax.bar(X - w / 2, ctrl, w, color=GREY, edgecolor="white")
ax.bar(X + w / 2, trt, w, color=[TREAT] * 4 + [CRIMSON], edgecolor="white")
ax.set_xticks(X); ax.set_xticklabels(genes, fontsize=10, color=TEXT2)
ax.set_xlabel("유전자", fontsize=10, color=TEXT2)
ax.set_ylabel("라이브러리 안의 비율 (%)", fontsize=10, color=TEXT2, labelpad=8)
ax.set_yticks([0, 200, 400, 600]); ax.set_yticklabels(["0", "20", "40", "60"])
ax.set_ylim(0, 860)
ax.spines["left"].set_color(LINE); ax.spines["bottom"].set_color(LINE)
ax.tick_params(length=0, labelsize=9.5)
ax.text(4.0, 760, "X 하나가 폭증", ha="right", va="center", fontsize=9.5, color=CRIMSON, fontweight="semibold")
ax.text(1.5, 360, "나머지는 변하지 않았는데\n비율로는 줄어 보임", ha="center", va="center", fontsize=9.5,
        color=WINE, linespacing=1.45)
ax.add_patch(mp.Rectangle((-0.45, 815), 0.3, 32, fc=GREY, ec="none"))
ax.text(-0.05, 831, "대조군", fontsize=9.5, color=TEXT2, va="center")
ax.add_patch(mp.Rectangle((1.25, 815), 0.3, 32, fc=TREAT, ec="none"))
ax.text(1.65, 831, "처리군", fontsize=9.5, color=CRIMSON, va="center")
tag(ax, "③ 조성 효과")
save(fig, "../../assets/img/w09/normalization.png")
