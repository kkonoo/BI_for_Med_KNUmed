# W11 §5.1 세포 수 ≠ 표본 수: 세포 단위 검정 vs 환자별로 합친 pseudobulk
# 오른쪽은 이 스크립트가 직접 돌리는 모의실험: 환자 3명 vs 대조군 3명, 두 군에 실제 차이는 없음.
# 사람마다 발현 수준이 조금씩 다르고(사람 효과), 세포는 그 사람 수준 주변에 흩어짐.
#   세포 단위 = 모든 세포를 독립 표본으로 Wilcoxon 순위합 검정
#   pseudobulk = 사람마다 평균 하나 → t-검정 (n = 6)
# (BI_for_Biomed W5 pseudobulk를 한글로 다시 그림)
from medfig import *
from scipy.stats import mannwhitneyu, ttest_ind

rng = np.random.default_rng(5)
PAT, CTL = ORANGE, "#6B7280"

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

fig = plt.figure(figsize=(10.8, 4.4))
ax = fig.add_axes([0.0, 0.0, 0.52, 1.0]); ax.set_xlim(0, 5.6); ax.set_ylim(0, 4.4); ax.axis("off")
a2 = fig.add_axes([0.63, 0.15, 0.35, 0.72])

# 왼쪽: 누가 표본인가
label(ax, 0.1, 4.25, "① 누가 표본인가", fs=11.5, w="bold", ha="left")
label(ax, 0.1, 3.88, "세포 단위 검정: 점 하나하나를 표본으로 셈 → n = 세포 수", fs=9.5, c=TEXT, ha="left")
names = ["P1", "P2", "P3", "C1", "C2", "C3"]
for i, nm in enumerate(names):
    x = 1.25 + i * 0.72
    col = PAT if i < 3 else CTL
    pts = rng.normal([x, 3.08], [0.11, 0.17], size=(30, 2))
    pts[:, 1] = pts[:, 1].clip(2.72, 3.5)
    ax.scatter(pts[:, 0], pts[:, 1], s=7, color=mix(col, 0.65), lw=0)
    arrow(ax, x, 2.6, x, 2.22, color="#B8BDC5", lw=1.1, ms=8)
    box(ax, x - 0.25, 1.82, 0.5, 0.33, fc=col, ec="none", r=0.06)
    label(ax, x, 1.985, nm, fs=10, w="bold", c="white")
label(ax, 0.1, 2.41, "사람마다\n합침", fs=9, c=TEXT2, ha="left", linespacing=1.3)
label(ax, 1.25 + 0.72, 1.55, "환자", fs=9.5, c=PAT, w="bold")
label(ax, 1.25 + 4 * 0.72, 1.55, "대조군", fs=9.5, c=CTL, w="bold")
label(ax, 0.1, 1.08, "Pseudobulk: 사람 하나 = 표본 하나 → n = 6", fs=9.5, c=TEXT, ha="left")
label(ax, 0.1, 0.6, "한 사람의 세포들은 유전형·약·시료 처리를 함께 나눔", fs=9.5, c=TEXT2, ha="left")
label(ax, 0.1, 0.27, "→ 서로 독립된 표본이 아님", fs=9.5, c=TEXT2, ha="left")

# 오른쪽: 모의실험
a2.plot(sizes, fp[:, 0] * 100, "-o", color=CRIMSON, lw=2, ms=6)
a2.plot(sizes, fp[:, 1] * 100, "-o", color="#4B5563", lw=2, ms=6)
a2.axhline(5, color="#9AA1AB", lw=1, ls="--")
a2.set_xscale("log"); a2.set_xticks(sizes); a2.set_xticklabels([str(s) for s in sizes])
a2.set_ylim(0, 100); a2.set_yticks([0, 25, 50, 75, 100]); a2.set_yticklabels(["0", "25%", "50%", "75%", "100%"])
a2.set_xlabel("사람 한 명당 세포 수", fontsize=10.5)
a2.set_ylabel("거짓 양성 비율 (p < 0.05)", fontsize=10.5)
a2.text(sizes[-1], fp[-1, 0] * 100 + 6, f"세포 단위 {fp[-1, 0] * 100:.0f}%", ha="right", fontsize=10,
        fontweight="bold", color=CRIMSON)
a2.text(sizes[-1], fp[-1, 1] * 100 + 6, f"pseudobulk {fp[-1, 1] * 100:.0f}%", ha="right", fontsize=10,
        fontweight="bold", color="#4B5563")
a2.text(0.0, 1.12, "② 모의실험: 두 군에 실제 차이가 없을 때", transform=a2.transAxes, fontsize=11.5,
        fontweight="bold", color=TEXT, va="bottom")
save(fig, "../../assets/img/w11/pseudobulk.png")
