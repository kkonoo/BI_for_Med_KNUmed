# W9 §6.1 Oncotype DX: 유전자 묶음 → 재발 점수 → 치료 결정, 케이스의 두 환자 (새로 그림)
from medfig import *

fig, ax = new(10.6, 4.3)

# ── 왼쪽: 유전자 묶음 ──────────────────────────────────────────
groups = [("증식", "MKI67 · AURKA · BIRC5 · CCNB1 · MYBL2", "높을수록 점수 ↑", CAT[0]),
          ("에스트로겐", "ESR1 · PGR · BCL2 · SCUBE2", "높을수록 점수 ↓", CAT[1]),
          ("HER2 · 침습 등", "ERBB2 · GRB7 · MMP11 · CTSV …", "", CAT[2])]
cx, cw, chh = 0.15, 3.85, 0.82
for i, (name, genes, eff, col) in enumerate(groups):
    y = 3.2 - i * (chh + 0.16)
    box(ax, cx, y, cw, chh, fc=FAINT, ec="none", r=0.08)
    box(ax, cx, y, 0.1, chh, fc=col, ec="none", r=0.03, z=3)
    label(ax, cx + 0.28, y + chh - 0.25, name, fs=11.5, w="bold", c=col, ha="left")
    if eff:
        label(ax, cx + cw - 0.15, y + chh - 0.25, eff, fs=10, w="semibold", c=TEXT, ha="right")
    label(ax, cx + 0.28, y + 0.24, genes, fs=9.5, c="#4B5563", ha="left")
label(ax, cx, 0.95, "암 관련 16개 + 측정 기준용 5개 = 유전자 21개 (FFPE 조직, RT-PCR)", fs=9.5, c=TEXT2, ha="left")

# ── 가운데: 점수 ──────────────────────────────────────────────
arrow(ax, 4.15, 2.25, 4.6, 2.25, color="#9AA1AB", lw=1.8)
box(ax, 4.7, 1.7, 1.25, 1.1, fc=CRIMSON, ec="none", r=0.1)
label(ax, 5.325, 2.4, "재발 점수", fs=12, w="bold", c="white")
label(ax, 5.325, 2.02, "묶음별로 계산해\n하나로 합침", fs=9, c="white", linespacing=1.3)
arrow(ax, 6.05, 2.25, 6.4, 2.25, color="#9AA1AB", lw=1.8)

# ── 오른쪽: 점수 구간과 결정 ──────────────────────────────────
s0, s1, vmax = 6.5, 10.45, 45
sx = lambda v: s0 + (s1 - s0) * v / vmax
ybar = 2.05
regions = [(0, 10.5, mix(AMBER, 0.35)), (10.5, 25.5, mix(ORANGE, 0.45)), (25.5, vmax, mix(CRIMSON, 0.55))]
for a, b, c in regions:
    ax.add_patch(mp.Rectangle((sx(a), ybar), sx(b) - sx(a), 0.32, fc=c, ec="white", lw=2, zorder=2))
for v, t in [(10.5, "10 | 11"), (25.5, "25 | 26")]:
    label(ax, sx(v), ybar - 0.2, t, fs=9, c=TEXT2)
dec = [(5.25, "호르몬\n치료"), (18, "호르몬 치료만 해도\n항암 추가와 성적 비슷\n(TAILORx)"), (35.25, "항암화학요법\n추가")]
for v, t in dec:
    label(ax, sx(v), ybar - 0.78, t, fs=9.5, c=TEXT, linespacing=1.35, va="center")
label(ax, sx(18), ybar - 1.3, "50세 이하·16–25점은 항암 이득 일부", fs=9, c=TEXT2)

# 케이스의 두 환자
for v, t, col in [(12, "환자 A · 12점", CAT[1]), (31, "환자 B · 31점", CAT[0])]:
    ax.add_patch(mp.Polygon([(sx(v) - 0.11, ybar + 0.62), (sx(v) + 0.11, ybar + 0.62), (sx(v), ybar + 0.4)],
                            closed=True, fc=col, ec="none", zorder=4))
    label(ax, sx(v), ybar + 0.85, t, fs=10.5, w="bold", c=col)
label(ax, (s0 + s1) / 2, 3.55, "같은 병기, 같은 수용체 상태 — 점수가 치료를 가름", fs=10, w="semibold", c=TEXT)
save(fig, "../../assets/img/w09/oncotype.png")
