# W9 §7.1 mRNA 양으로 단백질 양을 대략만 알 수 있음 (BI_for_Biomed W4 rna_protein을 다시 그림; 점은 가상)
from medfig import *

rng = np.random.default_rng(9)
fig = plt.figure(figsize=(10.2, 4.3))
ax = fig.add_axes([0.06, 0.12, 0.5, 0.78])
n = 900
x = rng.normal(0, 1, n)
y = 0.45 * x + np.sqrt(1 - 0.45 ** 2) * rng.normal(0, 1, n)
mx, my = 1 + 0.7 * x, 3 + 0.9 * y
ax.scatter(mx, my, s=10, color="#C4C9D1", lw=0, alpha=0.85)
b = np.polyfit(mx, my, 1)
xs = np.linspace(mx.min(), mx.max(), 10)
ax.plot(xs, np.polyval(b, xs), color=TEXT2, lw=1.2, ls=(0, (4, 2)))
g1, g2 = (1.6, 4.85), (1.6, 3.35)                       # 같은 mRNA, 단백질은 크게 다름
for (gx, gy), lab in ((g1, "유전자 P"), (g2, "유전자 Q")):
    ax.scatter([gx], [gy], s=60, color=CRIMSON, lw=1.2, edgecolor="white", zorder=3)
    ax.text(gx + 0.12, gy, lab, ha="left", va="center", fontsize=10.5, fontweight="bold", color=CRIMSON)
ax.annotate("", (1.48, g2[1] + 0.07), (1.48, g1[1] - 0.07), arrowprops=dict(arrowstyle="<->", color=CRIMSON, lw=1.2))
ax.text(1.38, (g1[1] + g2[1]) / 2, "mRNA는 같은데\n단백질은 크게 다름", ha="right", va="center", fontsize=10,
        color=CRIMSON, linespacing=1.35, bbox=dict(fc="white", ec="none", alpha=0.9, pad=2))
ax.text(0.02, 0.97, "점 하나 = 유전자 하나", transform=ax.transAxes, ha="left", va="top", fontsize=10.5,
        fontweight="semibold", color=TEXT)
ax.set_xlabel("mRNA 양 (로그)", color=TEXT2, fontsize=10.5)
ax.set_ylabel("단백질 양 (로그)", color=TEXT2, fontsize=10.5)
ax.set_xticks([]); ax.set_yticks([])
for sp in ("left", "bottom"):
    ax.spines[sp].set_color(LINE)

# mRNA와 단백질 사이의 단계
t = fig.add_axes([0.62, 0.12, 0.37, 0.78]); t.axis("off"); t.set_xlim(0, 1); t.set_ylim(0, 1)
t.text(0, 0.97, "단백질 양을 정하는 다른 단계", ha="left", va="top", fontsize=11.5, fontweight="bold", color=TEXT)
rows = [("번역 효율", "같은 mRNA에서 단백질을 얼마나 자주 만드나"),
        ("단백질 수명", "몇 분 만에 분해되는 것부터 며칠 버티는 것까지"),
        ("번역 후 변형", "인산화 등 — 양은 같아도 활성이 달라짐")]
for k, (h, d) in enumerate(rows):
    yy = 0.74 - k * 0.24
    t.add_patch(mp.FancyBboxPatch((0, yy - 0.075), 0.035, 0.15, boxstyle="round,pad=0,rounding_size=0.01",
                                  fc=CAT[k], ec="none"))
    t.text(0.07, yy + 0.035, h, ha="left", va="center", fontsize=11, fontweight="bold", color=CAT[k])
    t.text(0.07, yy - 0.045, d, ha="left", va="center", fontsize=9.5, color=TEXT2)
t.text(0, 0.06, "→ 단백질이 늘었다고 말하려면 단백질을 따로 확인", ha="left", va="center", fontsize=10,
       fontweight="semibold", color=TEXT)
save(fig, "../../assets/img/w09/rna_protein.png")
