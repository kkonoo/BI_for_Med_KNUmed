# W11 §6 공간 전사체: 점(spot) 기반 vs 영상 기반. 같은 가상 조직(종양 · 경계의 T세포 · 기질)
# (BI_for_Biomed W5 spatial을 한글로 다시 그림)
from medfig import *

rng = np.random.default_rng(3)
TUM, TC, STR = CAT[0], CAT[2], CAT[3]
W, H = 4.4, 3.2
OY = 1.15                      # 조직을 그리는 높이 (아래에 범례 자리)
FILL = {TUM: mix(TUM, 0.4), STR: mix(STR, 0.4), TC: mix(TC, 0.85)}

# 가상 조직: 격자 위 세포, 위쪽 = 종양, 아래쪽 = 기질, T세포는 주로 경계에
cells = []
for i in range(int(W / 0.2)):
    for j in range(int(H / 0.2)):
        x = 0.1 + i * 0.2 + (0.1 if j % 2 else 0) + rng.normal(0, 0.02)
        y = 0.1 + j * 0.2 + rng.normal(0, 0.02)
        if x > W - 0.05:
            continue
        b = 1.55 + 0.25 * np.sin(x * 1.6)
        d = y - b
        if abs(d) < 0.32 and rng.random() < 0.55:
            t = TC
        elif d > 0:
            t = TC if rng.random() < 0.06 else TUM
        else:
            t = TC if rng.random() < 0.08 else STR
        cells.append((x, y, t))

def tissue(ax, ox, dots=False):
    for x, y, t in cells:
        ax.add_patch(mp.Circle((ox + x, OY + y), 0.085 if t != TC else 0.075, fc=FILL[t], ec="none", zorder=2))
        if dots:
            for _ in range(rng.integers(1, 4)):
                a, r = rng.uniform(0, 2 * np.pi), rng.uniform(0, 0.05)
                ax.add_patch(mp.Circle((ox + x + r * np.cos(a), OY + y + r * np.sin(a)), 0.017,
                                       fc=t if t != TC else "white", ec="none", zorder=3))

fig, ax = new(10.4, 5.3)
# ① 점 기반
label(ax, 0.1, 5.15, "① 점(spot) 기반", fs=11.5, w="bold", ha="left")
label(ax, 0.1, 4.8, "모든 유전자를 읽음 · 점 하나에 세포 여러 개가 섞임", fs=9.5, c=TEXT2, ha="left")
tissue(ax, 0.1)
hi = None
for i in range(8):
    for j in range(6):
        sx, sy = 0.1 + 0.32 + i * 0.54 + (0.27 if j % 2 else 0), OY + 0.3 + j * 0.5
        if sx > 0.1 + W - 0.2:
            continue
        ax.add_patch(mp.Circle((sx, sy), 0.24, fc="none", ec=mix(TEXT, 0.45), lw=0.9, zorder=4))
        if (i, j) == (3, 3):
            hi = (sx, sy)
ax.add_patch(mp.Circle(hi, 0.24, fc="none", ec=BLUE, lw=2.4, zorder=5))
inside = [t for x, y, t in cells if (0.1 + x - hi[0]) ** 2 + (OY + y - hi[1]) ** 2 < 0.24 ** 2]
frac = [inside.count(t) / len(inside) for t in (TUM, TC, STR)]
label(ax, 0.1, 0.78, "파랑 점 하나가 읽은 신호:", fs=9.5, c=TEXT, ha="left")
bx = 1.85
for f, t in zip(frac, (TUM, TC, STR)):
    box(ax, bx, 0.68, 2.2 * f, 0.2, fc=FILL[t], ec="none", r=0.0)
    bx += 2.2 * f
label(ax, 4.15, 0.78, "세포 섞임", fs=9.5, c=TEXT, ha="left")

# ② 영상 기반
ox = 5.6
label(ax, ox, 5.15, "② 영상 기반", fs=11.5, w="bold", ha="left")
label(ax, ox, 4.8, "RNA 분자 하나하나의 위치 · 미리 고른 유전자만", fs=9.5, c=TEXT2, ha="left")
tissue(ax, ox, dots=True)
label(ax, ox, 0.78, "점 하나 = RNA 분자 하나 → 세포 하나 수준", fs=9.5, c=TEXT, ha="left")

# 범례
for k, (nm, t) in enumerate([("종양세포", TUM), ("T세포", TC), ("기질세포", STR)]):
    x = 0.1 + k * 1.35
    ax.add_patch(mp.Circle((x + 0.08, 0.22), 0.08, fc=FILL[t], ec="none"))
    label(ax, x + 0.24, 0.22, nm, fs=9.5, c=TEXT, ha="left")
save(fig, "../../assets/img/w11/spatial.png")
