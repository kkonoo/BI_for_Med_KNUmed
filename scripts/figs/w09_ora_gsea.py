# W9 §5.1 ORA는 기준선으로 자른 목록만, GSEA는 전체 순서를 봄 (BI_for_Biomed W4 ora_vs_gsea를 줄여 다시 그림; 위치는 예시)
from medfig import *

rng = np.random.default_rng(7)
fig, ax = new(8.4, 5.5)
X0, X1 = 1.35, 8.3
L = X1 - X0
cut = 0.13                                         # 기준선 (예시)
inside = np.sort(rng.uniform(0.005, cut - 0.005, 15))
outside = np.sort(np.concatenate([rng.uniform(cut, 0.35, 4), rng.uniform(0.35, 1.0, 6)]))
ticks = np.concatenate([inside, outside])
GREY = "#D5D9DF"
TICK = WINE


def ranked_bar(y, with_cut):
    if with_cut:
        box(ax, X0, y, L * cut, 0.36, fc=CRIMSON, ec="none", r=0.05)
        box(ax, X0 + L * cut + 0.03, y, L * (1 - cut) - 0.03, 0.36, fc=GREY, ec="none", r=0.05)
    else:
        box(ax, X0, y, L, 0.36, fc=GREY, ec="none", r=0.05)
    for t in ticks:
        ax.plot([X0 + L * t] * 2, [y - 0.32, y - 0.06], color=TICK, lw=1.3, zorder=3)
    label(ax, X0 - 0.15, y + 0.18, "전체 유전자", fs=11, c=TEXT2, ha="right")
    label(ax, X0 - 0.15, y - 0.19, "경로 유전자", fs=11, c=TICK, ha="right")
    if with_cut:
        label(ax, X1, y + 0.6, "← 많이 증가 · · · 많이 감소 →", fs=11, c=TEXT2, ha="right")


# ① ORA
label(ax, 0.1, 5.3, "① ORA — 기준선으로 자른 목록만 봄", fs=13, w="bold", ha="left")
y1 = 4.3
ranked_bar(y1, True)
xc = X0 + L * cut
ax.plot([xc, xc], [y1 - 0.4, y1 + 0.45], color=TEXT, lw=1.2, ls=(0, (3, 2)), zorder=4)
label(ax, X0 + L * cut / 2, y1 + 0.18, "유의한 목록", fs=11, w="bold", c="white")
label(ax, xc + 0.1, y1 + 0.6, "기준선", fs=11, w="semibold", c=TEXT, ha="left")
label(ax, X0, y1 - 0.65, f"목록 안 경로 유전자 {len(inside)}개", fs=11.5, w="semibold", c=CRIMSON, ha="left")
label(ax, X1, y1 - 0.65, "→ 우연히 기대되는 수와 비교", fs=11, c=TEXT2, ha="right")
label(ax, X1, y1 - 1.0, "기준선 밖 유전자는 버림", fs=11, c=TEXT2, ha="right")

ax.plot([0.1, X1], [2.95, 2.95], color=LINE, lw=1.0)

# ② GSEA
label(ax, 0.1, 2.62, "② GSEA — 자르지 않고 전체 순서를 봄", fs=13, w="bold", ha="left")
y2 = 0.4
ranked_bar(y2, False)
# running score: 경로 유전자를 만나면 오르고, 아니면 조금씩 내려감
xs = np.linspace(0, 1, 800)
hit = np.searchsorted(np.sort(ticks), xs, side="right")
es = hit / len(ticks) - xs
es = es / es.max()
base, hgt = y2 + 0.7, 0.75
ax.plot(X0 + L * xs, base + hgt * np.clip(es, -0.2, 1), color=CRIMSON, lw=2, zorder=3)
ax.plot([X0, X1], [base, base], color=LINE, lw=0.9, zorder=2)
k = np.argmax(es)
ax.plot([X0 + L * xs[k]] * 2, [base, base + hgt], color=TEXT, lw=1, ls=(0, (3, 2)), zorder=3)
label(ax, X0 + L * xs[k] + 0.15, base + hgt + 0.2, "경로 유전자가 \"많이 증가\" 쪽에 몰림 → 이 경로가 함께 증가",
      fs=11.5, w="semibold", c=CRIMSON, ha="left", va="center")
save(fig, "../../assets/img/w09/ora_gsea.png")
