# W13 §6.1 전파 추적: 환자 A의 분리주와 비교한 SNV 거리 (가상의 예). 기준은 장 본문의 Eyre et al., NEJM 2013
from medfig import *

rng = np.random.default_rng(13)
fig, ax = new(8.0, 4.5)
gx, gw = 1.05, 4.55                         # genome bar
iso = [("환자 A", None, CRIMSON), ("환자 B", 0, CRIMSON), ("환자 C", 2, CRIMSON), ("환자 D", 15, ORANGE)]
for i, (name, n, col) in enumerate(iso):
    y = 3.8 - i * 0.6
    label(ax, gx - 0.2, y, name, fs=12, w="bold", ha="right")
    box(ax, gx, y - 0.13, gw, 0.26, fc=mix(col, 0.22), ec="none", r=0.06)
    if n is None:
        label(ax, gx + gw + 0.2, y, "기준 분리주", fs=11, c=TEXT2, ha="left")
        continue
    xs = [0.3, 0.72] if n == 2 else np.linspace(0.05, 0.95, n) + rng.uniform(-0.02, 0.02, n)
    for x in xs:
        ax.plot([gx + x * gw] * 2, [y - 0.19, y + 0.19], color=TEXT, lw=2, solid_capstyle="butt")
    label(ax, gx + gw + 0.2, y, f"A와 {n}곳 다름", fs=11.5, w="bold", ha="left",
          c=BLUE if n <= 2 else TEXT)
label(ax, 0.1, 4.38, "막대 = 분리주의 유전체 (수백만 염기) · 세로선 = A와 다른 염기 하나", fs=11, c=TEXT2,
      ha="left")

# reading the distance
box(ax, 0.1, 0.15, 3.75, 1.35, fc=mix(BLUE, 0.1), ec=mix(BLUE, 0.45), r=0.1)
label(ax, 1.975, 1.15, "0–2개", fs=13, w="bold", c=BLUE)
label(ax, 1.975, 0.57, "최근 전파 가능성\n→ 입원 기록과 대조", fs=11, linespacing=1.45)
box(ax, 4.15, 0.15, 3.75, 1.35, fc=FAINT, ec="none", r=0.1)
label(ax, 6.025, 1.15, "10개 넘게", fs=13, w="bold", c=ORANGE)
label(ax, 6.025, 0.6, "다른 감염원", fs=11)
save(fig, "../../assets/img/w13/snv_transmission.png")
