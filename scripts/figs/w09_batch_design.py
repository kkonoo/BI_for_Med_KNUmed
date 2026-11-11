# W9 §2.2 배치가 비교 조건과 완전히 겹친 설계 vs 골고루 섞은 설계 (BI_for_Biomed W4 replicates/batch를 바탕으로 새로 그림)
from medfig import *

fig, ax = new(8.2, 5.6)
TUM, NOR = CAT[0], CAT[3]          # 암 조직, 정상 조직


def sample(x, y, col, r=0.2):
    ax.add_patch(mp.Circle((x, y), r, fc=col, ec="white", lw=1.5, zorder=4))


def batch(x, y, name, cols):
    box(ax, x, y, 2.1, 1.2, fc=FAINT, ec=LINE, r=0.1, z=2)
    label(ax, x + 1.05, y + 0.93, name, fs=11.5, w="semibold", c=TEXT)
    for k, c in enumerate(cols):
        sample(x + 0.4 + k * 0.43, y + 0.42, c)


def panel(y0, tag, mon, fri, verdict, sub, ok):
    label(ax, 0.1, y0 + 1.6, tag, fs=13, w="bold", ha="left")
    batch(0.1, y0, "월요일 처리", mon)
    batch(2.45, y0, "금요일 처리", fri)
    label(ax, 4.95, y0 + 0.8, ("✓ " if ok else "✗ ") + verdict, fs=12, w="bold", c=TEXT if ok else WINE, ha="left")
    label(ax, 4.95, y0 + 0.38, sub, fs=11, c=TEXT2, ha="left")


panel(3.3, "① 배치 = 비교 조건", [TUM] * 4, [NOR] * 4,
      "암 vs 정상 = 월요일 vs 금요일", "두 차이를 영원히 구분할 수 없음", False)
ax.plot([0.1, 8.1], [2.75, 2.75], color=LINE, lw=1.0)
panel(0.55, "② 배치마다 골고루", [TUM, NOR, TUM, NOR], [NOR, TUM, NOR, TUM],
      "배치 안에서 암과 정상을 비교", "배치를 변수로 넣어 보정할 수 있음", True)

# 범례
for k, (c, t) in enumerate([(TUM, "암 조직"), (NOR, "정상 조직")]):
    xx = 5.6 + k * 1.3
    sample(xx, 4.9, c, r=0.12)
    label(ax, xx + 0.22, 4.9, t, fs=11, c=TEXT, ha="left")
save(fig, "../../assets/img/w09/batch_design.png")
