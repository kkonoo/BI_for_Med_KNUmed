# W9 §2.2 배치가 비교 조건과 완전히 겹친 설계 vs 골고루 섞은 설계 (BI_for_Biomed W4 replicates/batch를 바탕으로 새로 그림)
from medfig import *

fig, ax = new(10.6, 3.4)
TUM, NOR = CAT[0], CAT[3]          # 암 조직, 정상 조직


def sample(x, y, col, r=0.2):
    ax.add_patch(mp.Circle((x, y), r, fc=col, ec="white", lw=1.5, zorder=4))


def batch(x, y, name, cols):
    box(ax, x, y, 2.1, 1.2, fc=FAINT, ec=LINE, r=0.1, z=2)
    label(ax, x + 1.05, y + 0.93, name, fs=10.5, w="semibold", c=TEXT)
    for k, c in enumerate(cols):
        sample(x + 0.4 + k * 0.43, y + 0.42, c)


def panel(x0, tag, mon, fri, verdict, sub, ok):
    label(ax, x0, 3.05, tag, fs=12, w="bold", ha="left")
    batch(x0, 1.45, "월요일 처리", mon)
    batch(x0 + 2.45, 1.45, "금요일 처리", fri)
    label(ax, x0, 1.0, ("✓ " if ok else "✗ ") + verdict, fs=11, w="bold", c=TEXT if ok else WINE, ha="left")
    label(ax, x0, 0.62, sub, fs=9.5, c=TEXT2, ha="left")


panel(0.2, "① 배치 = 비교 조건", [TUM] * 4, [NOR] * 4,
      "암 vs 정상 = 월요일 vs 금요일", "두 차이를 영원히 구분할 수 없음", False)
panel(5.75, "② 배치마다 골고루", [TUM, NOR, TUM, NOR], [NOR, TUM, NOR, TUM],
      "배치 안에서 암과 정상을 비교", "배치를 변수로 넣어 보정할 수 있음", True)
ax.plot([5.3, 5.3], [0.5, 3.2], color=LINE, lw=1.0)

# 범례
for k, (c, t) in enumerate([(TUM, "암 조직"), (NOR, "정상 조직")]):
    xx = 8.35 + k * 1.15
    sample(xx, 3.05, c, r=0.11)
    label(ax, xx + 0.2, 3.05, t, fs=10, c=TEXT, ha="left")
save(fig, "../../assets/img/w09/batch_design.png")
