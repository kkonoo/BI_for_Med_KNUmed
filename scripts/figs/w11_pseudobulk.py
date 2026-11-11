# W11 §5.1 세포 수 ≠ 표본 수: 세포 단위 검정 vs 환자별로 합친 pseudobulk
# ②는 이 스크립트가 직접 돌리는 모의실험: 환자 3명 vs 대조군 3명, 두 군에 실제 차이는 없음.
# 사람마다 발현 수준이 조금씩 다르고(사람 효과), 세포는 그 사람 수준 주변에 흩어짐.
#   세포 단위 = 모든 세포를 독립 표본으로 Wilcoxon 순위합 검정
#   pseudobulk = 사람마다 평균 하나 → t-검정 (n = 6)
# (BI_for_Biomed W5 pseudobulk를 한글로 다시 그림)
from medfig import *
from scipy.stats import mannwhitneyu, ttest_ind

rng = np.random.default_rng(5)
PAT, CTL, PB = ORANGE, "#6B7280", "#4B5563"

def one_run(n_cells):
    donors = rng.normal(0, 0.5, 6)                       # 사람 효과, 군 차이 없음
    cells = [rng.normal(m, 1.0, n_cells) for m in donors]
    a, b = np.concatenate(cells[:3]), np.concatenate(cells[3:])
    p_cell = mannwhitneyu(a, b).pvalue
    p_pb = ttest_ind([c.mean() for c in cells[:3]], [c.mean() for c in cells[3:]]).pvalue
    return p_cell < 0.05, p_pb < 0.05

sizes = [10, 30, 100, 300, 1000]
runs = 400
fp = np.array([np.mean([one_run(n) for _ in range(runs)], axis=0) for n in sizes])
print("false-positive rates (cell, pseudobulk):", fp.round(3).tolist())

W, H = 8.2, 7.0
fig = plt.figure(figsize=(W, H))
TOP = 3.25                                           # ① 그림 높이 (인치)
ax = fig.add_axes([0, 1 - TOP / H, 1, TOP / H]); ax.set_xlim(0, W); ax.set_ylim(0, TOP); ax.axis("off")
a2 = fig.add_axes([0.11, 0.08, 0.86, 0.36])

# ① 누가 표본인가
label(ax, 0, 3.05, "① 누가 표본인가", fs=12.5, w="bold", ha="left")
names = ["P1", "P2", "P3", "C1", "C2", "C3"]
for i, nm in enumerate(names):
    x = 1.05 + i * 0.7
    col = PAT if i < 3 else CTL
    pts = rng.normal([x, 2.2], [0.1, 0.15], size=(30, 2))
    pts[:, 1] = pts[:, 1].clip(1.9, 2.55)
    for px, py in pts:
        ax.add_patch(mp.Circle((px, py), 0.022, fc=mix(col, 0.65), ec="none", zorder=3))
    arrow(ax, x, 1.78, x, 1.45, color="#B8BDC5", lw=1.1, ms=8)
    box(ax, x - 0.27, 1.0, 0.54, 0.36, fc=col, ec="none", r=0.06)
    label(ax, x, 1.18, nm, fs=11, w="bold", c="white")
label(ax, 0, 1.6, "사람마다\n합침", fs=11, c=TEXT2, ha="left", linespacing=1.3)
label(ax, 1.05 + 0.7, 0.68, "환자", fs=11.5, c=PAT, w="bold")
label(ax, 1.05 + 4 * 0.7, 0.68, "대조군", fs=11.5, c=CTL, w="bold")

x0 = 5.1
label(ax, x0, 2.5, "세포 단위 검정", fs=12, w="bold", c=CRIMSON, ha="left")
label(ax, x0, 2.15, "점 하나 = 표본 하나 → n = 세포 수", fs=11, ha="left")
label(ax, x0, 1.6, "Pseudobulk", fs=12, w="bold", c=PB, ha="left")
label(ax, x0, 1.25, "사람 하나 = 표본 하나 → n = 6", fs=11, ha="left")
label(ax, x0, 0.68, "한 사람의 세포끼리는 독립이 아님", fs=11, c=TEXT2, ha="left")
label(ax, x0, 0.35, "(유전형·약·시료 처리를 함께 나눔)", fs=11, c=TEXT2, ha="left")

# ② 모의실험
a2.plot(sizes, fp[:, 0] * 100, "-o", color=CRIMSON, lw=2, ms=6)
a2.plot(sizes, fp[:, 1] * 100, "-o", color=PB, lw=2, ms=6)
a2.axhline(5, color="#9AA1AB", lw=1, ls="--")
a2.set_xscale("log"); a2.set_xticks(sizes); a2.set_xticklabels([str(s) for s in sizes])
a2.minorticks_off()
a2.set_ylim(0, 100); a2.set_yticks([0, 25, 50, 75, 100]); a2.set_yticklabels(["0", "25%", "50%", "75%", "100%"])
a2.tick_params(labelsize=11)
a2.set_xlabel("사람 한 명당 세포 수", fontsize=11.5)
a2.set_ylabel("거짓 양성 비율\n(p < 0.05)", fontsize=11.5)
a2.text(sizes[-1], fp[-1, 0] * 100 + 7, f"세포 단위 {fp[-1, 0] * 100:.0f}%", ha="right", fontsize=11.5,
        fontweight="bold", color=CRIMSON)
a2.text(sizes[-1], fp[-1, 1] * 100 + 7, f"pseudobulk {fp[-1, 1] * 100:.0f}%", ha="right", fontsize=11.5,
        fontweight="bold", color=PB)
a2.text(-0.12, 1.1, "② 모의실험: 두 군에 실제 차이가 없을 때", transform=a2.transAxes, fontsize=12.5,
        fontweight="bold", color=TEXT, va="bottom")
save(fig, "../../assets/img/w11/pseudobulk.png")
