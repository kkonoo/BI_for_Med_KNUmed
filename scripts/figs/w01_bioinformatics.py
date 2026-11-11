# W1 §1.1 생물정보학 = 생물학 + 컴퓨터 + 통계, 시료 → 데이터 생성 → 분석 → 해석
# (BI_for_Biomed W1 bioinformatics.png를 한글로 다시 그림)
from medfig import *

fig, ax = new(10.9, 3.2)

# ── left: three fields overlap ─────────────────────────────────────────────
fields = [("생물학", CAT[0], (1.55, 2.02), (1.55, 2.5)),
          ("컴퓨터", CAT[1], (1.14, 1.32), (0.9, 1.08)),
          ("통계", CAT[2], (1.96, 1.32), (2.2, 1.08))]
for name, c, (cx, cy), (lx, ly) in fields:
    ax.add_patch(mp.Circle((cx, cy), 0.78, fc=mix(c, 0.22), ec="none", alpha=0.75, zorder=2))
    ax.add_patch(mp.Circle((cx, cy), 0.78, fc="none", ec=c, lw=1.6, zorder=3))
    label(ax, lx, ly, name, fs=12.5, w="bold", c=c)
box(ax, 1.55 - 0.52, 1.56 - 0.17, 1.04, 0.34, fc="white", ec=LINE, r=0.17, z=6)
label(ax, 1.55, 1.56, "생물정보학", fs=10.5, w="bold", c=TEXT, z=7)

# ── right: from a tube of blood to a sentence about the patient ────────────
steps = [("시료", ["혈액 · 조직 · 세포", "+ 임상 정보"]),
         ("데이터 생성", ["시퀀서 같은 장비로 측정", "→ 아주 큰 표"]),
         ("분석", ["컴퓨터로 정리", "통계로 우연과 진짜 구분"]),
         ("해석", ["이 환자에게", "무슨 뜻인가?"])]
cols = ramp(4)
W, H, gap, x0, y0 = 1.62, 1.36, 0.3, 3.45, 1.12
for i, (name, lines) in enumerate(steps):
    x = x0 + i * (W + gap)
    box(ax, x, y0, W, H, fc=mix(cols[i], 0.1), ec="none", r=0.1)
    num(ax, x + 0.26, y0 + H - 0.27, i + 1, fc=cols[i])
    label(ax, x + 0.47, y0 + H - 0.27, name, fs=12.5, w="bold", c=cols[i], ha="left")
    for k, t in enumerate(lines):
        label(ax, x + 0.18, y0 + 0.66 - k * 0.32, t, fs=9.8, c=TEXT, ha="left")
    if i < 3:
        arrow(ax, x + W + 0.05, y0 + H / 2, x + W + gap - 0.05, y0 + H / 2, color=mix(CRIMSON, 0.45), lw=2)

xa, xb = x0, x0 + 4 * W + 3 * gap
label(ax, (xa + xb) / 2, 0.66, "목표 = 프로그램을 돌리는 것이 아니라, 결과를 믿어도 되는지 판단하는 것",
      fs=10.5, w="bold", c=BLUE)
save(fig, "../../assets/img/w01/bioinformatics.png")
