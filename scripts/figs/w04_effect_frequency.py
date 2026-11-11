# W4 §1.1 효과 크기 × 빈도: 희귀질환 변이와 복합질환 변이가 놓이는 자리
# (BI_for_Biomed W2 allelic_architecture를 장의 2×2 표에 맞춰 다시 그림)
from medfig import *

fig, ax = new(8.2, 5.4)
ox, oy, X1, Y1 = 1.0, 0.8, 8.05, 5.3
G = "#9AA1AB"
arrow(ax, ox, oy, X1, oy, color=G, lw=1.4, ms=11)
arrow(ax, ox, oy, ox, Y1, color=G, lw=1.4, ms=11)
label(ax, (ox + X1) / 2, 0.3, "대립유전자 빈도", fs=13, w="bold")
label(ax, ox + 0.3, 0.52, "드묾", fs=11, c=TEXT2)
label(ax, X1 - 0.3, 0.52, "흔함", fs=11, c=TEXT2)
label(ax, 0.3, (oy + Y1) / 2, "효과 크기", fs=13, w="bold", rotation=90)
label(ax, 0.78, oy + 0.3, "작음", fs=11, c=TEXT2, ha="right")
label(ax, 0.78, Y1 - 0.3, "큼", fs=11, c=TEXT2, ha="right")


def dot(x, y, c, r=0.09):
    ax.add_patch(mp.Circle((x, y), r, fc=c, ec="white", lw=1, zorder=4))


BW, BH = 3.15, 1.95
# 왼쪽 위: 드물고 효과 큼 = 단일유전자 질환
c = CAT[0]
box(ax, 1.25, 3.15, BW, BH, fc=mix(c, 0.10), ec=c, lw=1.4, r=0.12)
label(ax, 1.45, 4.8, "단일유전자 질환의 원인 변이", fs=13, w="bold", c=c, ha="left")
label(ax, 1.45, 4.45, "드물고 효과가 큼 → W2·W3", fs=11, c=TEXT2, ha="left")
for (y, t) in [(3.95, "SCN1A (W2·W3의 아이)"), (3.5, "LDLR (가족성 고콜레스테롤혈증)")]:
    dot(1.62, y, c)
    label(ax, 1.82, y, t, fs=10.5, ha="left")

# 오른쪽 아래: 흔하고 효과 작음 = 복합질환 GWAS
c = CAT[1]
box(ax, 4.75, 1.0, BW, BH, fc=mix(c, 0.10), ec=c, lw=1.4, r=0.12)
label(ax, 4.95, 2.65, "복합질환 GWAS 변이", fs=13, w="bold", c=c, ha="left")
label(ax, 4.95, 2.3, "흔하고 효과가 작음 → 이 장", fs=11, c=TEXT2, ha="left")
dot(5.12, 1.88, c)
label(ax, 5.32, 1.88, "9p21 (관상동맥질환)", fs=10.5, ha="left", w="semibold")
rng = np.random.default_rng(4)
for x, y in zip(rng.uniform(5.05, 7.65, 30), rng.uniform(1.4, 1.66, 30)):
    dot(x, y, mix(c, 0.55), r=0.05)  # patches, not scatter: medfig.save crops by patch extents
label(ax, 7.75, 1.08, "수백–수천 개", fs=10, c=TEXT2, ha="right", va="bottom")

# 오른쪽 위: 흔하면서 효과 큼 = 드묾
c = CAT[2]
label(ax, 4.85, 4.85, "흔하면서 효과가 큼 → 드묾", fs=12, w="bold", c=c, ha="left")
dot(5.05, 4.3, c)
label(ax, 5.25, 4.3, "APOE ε4 (알츠하이머병)", fs=11, ha="left", w="semibold", c=c)
label(ax, 4.85, 3.7, "자연선택이 이런 변이를 줄여 왔다고 봄", fs=10.5, c=TEXT2, ha="left")

# 왼쪽 아래: 드물고 효과 작음
box(ax, 1.25, 1.0, BW, BH, fc=FAINT, ec="#C4C7CC", lw=1.2, r=0.12, ls=(0, (4, 3)))
label(ax, 1.25 + BW / 2, 2.15, "드물고 효과도 작음", fs=12, w="bold", c=TEXT2)
label(ax, 1.25 + BW / 2, 1.75, "→ 찾기 어려움", fs=11, c=TEXT2)
save(fig, "../../assets/img/w04/effect_frequency.png")
