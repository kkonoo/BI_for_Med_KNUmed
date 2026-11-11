# W13 §6.1 전파 추적: 환자 A의 분리주와 비교한 SNV 거리 (가상의 예). 기준은 장 본문의 Eyre et al., NEJM 2013
from medfig import *

rng = np.random.default_rng(13)
fig, ax = new(10.4, 3.6)
gx, gw = 1.45, 5.2                          # genome bar
iso = [("환자 A", None, CRIMSON), ("환자 B", 0, CRIMSON), ("환자 C", 2, CRIMSON), ("환자 D", 15, ORANGE)]
for i, (name, n, col) in enumerate(iso):
    y = 3.05 - i * 0.72
    label(ax, gx - 0.2, y, name, fs=11, w="bold", ha="right")
    box(ax, gx, y - 0.13, gw, 0.26, fc=mix(col, 0.22), ec="none", r=0.06)
    if n is None:
        label(ax, gx + gw + 0.2, y, "기준 분리주", fs=10, c=TEXT2, ha="left")
        continue
    xs = [0.3, 0.72] if n == 2 else np.linspace(0.05, 0.95, n) + rng.uniform(-0.02, 0.02, n)
    for x in xs:
        ax.plot([gx + x * gw] * 2, [y - 0.19, y + 0.19], color=TEXT, lw=2, solid_capstyle="butt")
    label(ax, gx + gw + 0.2, y, f"A와 {n}곳 다름", fs=10.5, w="bold", ha="left",
          c=BLUE if n <= 2 else TEXT)
label(ax, gx, 3.6, "막대 = 분리주의 유전체 전체 (수백만 염기) · 검은 세로선 = A와 다른 염기 하나", fs=9.5, c=TEXT2,
      ha="left")

# reading the distance
bx = 8.35
box(ax, bx, 1.75, 2.0, 1.55, fc=mix(BLUE, 0.1), ec=mix(BLUE, 0.45), r=0.1)
label(ax, bx + 1.0, 2.95, "0–2개", fs=12, w="bold", c=BLUE)
label(ax, bx + 1.0, 2.35, "최근 전파 가능성\n→ 입원 기록과 대조", fs=10, linespacing=1.4)
box(ax, bx, 0.25, 2.0, 1.25, fc=FAINT, ec="none", r=0.1)
label(ax, bx + 1.0, 1.15, "10개 넘게", fs=12, w="bold", c=ORANGE)
label(ax, bx + 1.0, 0.65, "다른 감염원", fs=10)
ax.plot([gx + gw + 1.45] * 2, [0.3, 3.3], color=LINE, lw=1)
save(fig, "../../assets/img/w13/snv_transmission.png")
