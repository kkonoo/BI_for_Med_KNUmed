# W1 §1.1 생물정보학 = 생물학 + 컴퓨터 + 통계, 시료 → 데이터 생성 → 분석 → 해석
# (BI_for_Biomed W1 bioinformatics.png를 한글로 다시 그림)
from medfig import *

fig, ax = new(8.4, 3.85)

# ── top: three fields overlap, and the goal next to them ───────────────────
R, cx0, cy0 = 0.66, 1.55, 2.68
fields = [("생물학", CAT[0], (cx0, cy0 + 0.36), (cx0, cy0 + 0.78)),
          ("컴퓨터", CAT[1], (cx0 - 0.36, cy0 - 0.27), (cx0 - 0.62, cy0 - 0.5)),
          ("통계", CAT[2], (cx0 + 0.36, cy0 - 0.27), (cx0 + 0.62, cy0 - 0.5))]
for name, c, (cx, cy), (lx, ly) in fields:
    ax.add_patch(mp.Circle((cx, cy), R, fc=mix(c, 0.22), ec="none", alpha=0.75, zorder=2))
    ax.add_patch(mp.Circle((cx, cy), R, fc="none", ec=c, lw=1.6, zorder=3))
    label(ax, lx, ly, name, fs=13, w="bold", c=c)
box(ax, cx0 - 0.56, cy0 - 0.03 - 0.19, 1.12, 0.38, fc="white", ec=LINE, r=0.19, z=6)
label(ax, cx0, cy0 - 0.03, "생물정보학", fs=12, w="bold", c=TEXT, z=7)

label(ax, 3.55, 2.9, "목표는 프로그램을 돌리는 것이 아니라", fs=13, w="bold", c=BLUE, ha="left")
label(ax, 3.55, 2.52, "결과를 믿어도 되는지 판단하는 것", fs=13, w="bold", c=BLUE, ha="left")

# ── bottom: from a tube of blood to a sentence about the patient ───────────
steps = [("시료", ["혈액·조직·세포", "+ 임상 정보"]),
         ("데이터 생성", ["시퀀서로 측정", "→ 아주 큰 표"]),
         ("분석", ["컴퓨터로 정리", "통계로 우연 걸러냄"]),
         ("해석", ["이 환자에게", "무슨 뜻인가?"])]
cols = ramp(4)
W, H, gap, x0, y0 = 1.86, 1.42, 0.3, 0.05, 0.05
for i, (name, lines) in enumerate(steps):
    x = x0 + i * (W + gap)
    box(ax, x, y0, W, H, fc=mix(cols[i], 0.1), ec="none", r=0.1)
    num(ax, x + 0.27, y0 + H - 0.29, i + 1, fc=cols[i], fs=11)
    label(ax, x + 0.5, y0 + H - 0.29, name, fs=13, w="bold", c=cols[i], ha="left")
    for k, t in enumerate(lines):
        label(ax, x + 0.18, y0 + 0.69 - k * 0.34, t, fs=11, c=TEXT, ha="left")
    if i < 3:
        arrow(ax, x + W + 0.04, y0 + H / 2, x + W + gap - 0.04, y0 + H / 2,
              color=mix(CRIMSON, 0.45), lw=2, ms=10)
save(fig, "../../assets/img/w01/bioinformatics.png")
