# W11 §4.3 클러스터 ≠ 세포 유형: 같은 세포, 같은 알고리즘, 해상도만 바꿈 (4개 vs 7개)
# 점은 설명용으로 만든 가상 세포. 해상도를 높이면 한 무리가 같은 색 계열의 작은 무리로 쪼개짐.
# (BI_for_Biomed W5 umap_resolution을 한글로 다시 그림)
from medfig import *

rng = np.random.default_rng(11)
# 무리 4개: (중심, 퍼짐, 세포 수, 높은 해상도에서 쪼개지는 수, 쪼개는 축)
groups = [((2.2, 2.3), (0.6, 0.42), 600, 3, 0),
          ((-1.6, 2.6), (0.28, 0.8), 330, 2, 1),
          ((-2.0, -1.4), (0.5, 0.35), 260, 1, 0),
          ((1.7, -1.7), (0.35, 0.3), 150, 1, 0)]
pts, low, high, shades = [], [], [], []
k = 0
for g, (c, s, n, split, axis) in enumerate(groups):
    p = rng.normal(c, s, size=(n, 2))
    order = np.argsort(np.argsort(p[:, axis]))
    sub = (order * split // n)
    pts.append(p); low += [g] * n
    high += list(k + sub)
    for j in range(split):
        shades.append(mix(CAT[g], [1.0, 0.6, 0.35][j] if split > 1 else 1.0))
    k += split
pts = np.vstack(pts); low = np.array(low); high = np.array(high)

fig, axes = plt.subplots(1, 2, figsize=(8.2, 4.4), gridspec_kw={"wspace": 0.06})
for a, lab, cols, tag in [(axes[0], low, CAT, "① 해상도 낮게 → 클러스터 4개"),
                          (axes[1], high, shades, "② 해상도 높게 → 클러스터 7개")]:
    a.scatter(pts[:, 0], pts[:, 1], s=5, c=[cols[i] for i in lab], lw=0)
    for i in np.unique(lab):
        cx, cy = pts[lab == i].mean(axis=0)
        a.text(cx, cy, str(i + 1), ha="center", va="center", fontsize=11.5, fontweight="bold", color=TEXT,
               bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none"))
    a.set_xticks([]); a.set_yticks([])
    for sp in a.spines.values():
        sp.set_visible(False)
    a.set_xlim(-3.6, 4.4); a.set_ylim(-2.9, 6.0)
    a.text(-3.5, 5.95, tag, fontsize=12.5, fontweight="bold", color=TEXT, va="top")
fig.text(0.5, 0.0, "어느 쪽이 맞는지 알려 주는 통계는 없음\n→ marker 유전자와 생물학으로 판단",
         ha="center", va="top", fontsize=12, fontweight="bold", color=BLUE, linespacing=1.4)
save(fig, "../../assets/img/w11/umap_resolution.png")
