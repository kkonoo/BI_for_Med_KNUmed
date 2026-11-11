# W4 §2.4 집단 구조라는 교란: "젓가락 유전자" 사고실험 (Hamer & Sirota 2000)
# 조상이 변이 빈도와 젓가락 사용을 함께 정함 → 변이와 젓가락이 연관처럼 보임 (사람 수는 설명용)
from medfig import *

fig, ax = new(8.8, 4.8)


def person(x, y, c, s=1.0):
    ax.add_patch(mp.Circle((x, y + 0.34 * s), 0.1 * s, fc=c, ec="none", zorder=3))
    box(ax, x - 0.14 * s, y - 0.05 * s, 0.28 * s, 0.28 * s, fc=c, ec="none", r=0.09 * s, z=3)


# ── 왼쪽: 교란 삼각형 ──
box(ax, 1.4, 3.55, 1.9, 0.85, fc=WINE, ec="none", r=0.1)
label(ax, 2.35, 4.12, "조상", fs=14, w="bold", c="white")
label(ax, 2.35, 3.8, "(ancestry)", fs=11, c="white")
for (x, name, sub, c) in [(0.05, "변이 X", "빈도", CAT[0]), (2.75, "젓가락 사용", "문화", CAT[1])]:
    box(ax, x, 1.25, 1.9, 0.85, fc=mix(c, 0.12), ec=c, lw=1.4, r=0.1)
    label(ax, x + 0.95, 1.83, name, fs=13, w="bold", c=c)
    label(ax, x + 0.95, 1.5, sub, fs=11, c=TEXT2)
arrow(ax, 1.95, 3.5, 1.15, 2.15, color=mix(WINE, 0.7), lw=1.8)
arrow(ax, 2.75, 3.5, 3.55, 2.15, color=mix(WINE, 0.7), lw=1.8)
label(ax, 1.3, 2.95, "조상마다\n빈도가 다름", fs=10.5, ha="right", linespacing=1.4)
label(ax, 3.4, 2.95, "조상마다\n문화가 다름", fs=10.5, ha="left", linespacing=1.4)
arrow(ax, 2.0, 1.67, 2.7, 1.67, color=BLUE, lw=1.8, ls=(0, (3, 2)))
label(ax, 2.35, 0.82, "GWAS에서는 '젓가락 유전자'처럼 보임", fs=11.5, w="bold", c=BLUE)
label(ax, 2.35, 0.47, "변이가 젓가락질을 만든 것이 아님", fs=10.5, c=TEXT2)

# ── 오른쪽: 두 군의 조상 구성 ──
x0, sp = 5.2, 0.36
for g, (name, n_ea) in enumerate([("젓가락을 쓰는 사람 (환자군 역할)", 8), ("쓰지 않는 사람 (대조군 역할)", 2)]):
    y = 4.3 - g * 1.3
    label(ax, x0 - 0.12, y, name, fs=11, w="semibold", ha="left")
    for k in range(10):
        person(x0 + 0.05 + k * sp, y - 0.75, WINE if k < n_ea else "#C4C7CC")
person(x0 + 0.05, 1.5, WINE, s=0.8)
label(ax, x0 + 0.27, 1.62, "동아시아계", fs=10.5, ha="left")
person(x0 + 1.6, 1.5, "#C4C7CC", s=0.8)
label(ax, x0 + 1.82, 1.62, "다른 조상", fs=10.5, ha="left")
label(ax, x0 - 0.12, 0.97, "두 군의 조상 구성이 다르면 →", fs=11, ha="left")
label(ax, x0 - 0.12, 0.66, "조상마다 빈도가 다른 변이가 모두 '유의'", fs=11, ha="left")
label(ax, x0 - 0.12, 0.28, "해결: 조상 성분 보정 · 같은 집단끼리 비교", fs=10.5, c=TEXT2, ha="left")
save(fig, "../../assets/img/w04/population_structure.png")
