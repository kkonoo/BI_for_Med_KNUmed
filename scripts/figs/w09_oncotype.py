# W9 §6.1 Oncotype DX: 유전자 묶음 → 재발 점수 → 치료 결정, 케이스의 두 환자 (새로 그림)
from medfig import *

fig, ax = new(8.3, 6.5)

# ── 위 왼쪽: 유전자 묶음 ──────────────────────────────────────
groups = [("증식", "MKI67 · AURKA · BIRC5 · CCNB1 · MYBL2", "높을수록 점수 ↑", CAT[0]),
          ("에스트로겐", "ESR1 · PGR · BCL2 · SCUBE2", "높을수록 점수 ↓", CAT[1]),
          ("HER2 · 침습 등", "ERBB2 · GRB7 · MMP11 · CTSV …", "", CAT[2])]
cx, cw, chh = 0.1, 4.6, 0.86
for i, (name, genes, eff, col) in enumerate(groups):
    y = 5.55 - i * (chh + 0.14)
    box(ax, cx, y, cw, chh, fc=FAINT, ec="none", r=0.08)
    box(ax, cx, y, 0.1, chh, fc=col, ec="none", r=0.03, z=3)
    label(ax, cx + 0.28, y + chh - 0.26, name, fs=12.5, w="bold", c=col, ha="left")
    if eff:
        label(ax, cx + cw - 0.15, y + chh - 0.26, eff, fs=11, w="semibold", c=TEXT, ha="right")
    label(ax, cx + 0.28, y + 0.25, genes, fs=11, c="#4B5563", ha="left")

# ── 위 오른쪽: 점수 ───────────────────────────────────────────
arrow(ax, 4.85, 4.99, 5.35, 4.99, color="#9AA1AB", lw=1.8)
box(ax, 5.45, 4.35, 2.6, 1.3, fc=CRIMSON, ec="none", r=0.1)
label(ax, 6.75, 5.25, "재발 점수", fs=13, w="bold", c="white")
label(ax, 6.75, 4.75, "묶음별로 계산해 합침", fs=11, c="white")
label(ax, 5.45, 3.95, "유전자 21개 = 암 관련 16 + 기준용 5", fs=11, c=TEXT2, ha="left")
label(ax, 5.45, 3.6, "FFPE 조직 · RT-PCR", fs=11, c=TEXT2, ha="left")

ax.plot([0.1, 8.2], [3.15, 3.15], color=LINE, lw=1.0)

# ── 아래: 점수 구간과 결정 ────────────────────────────────────
s0, s1, vmax = 0.7, 8.1, 45
sx = lambda v: s0 + (s1 - s0) * v / vmax
ybar = 1.55
regions = [(0, 10.5, mix(AMBER, 0.35)), (10.5, 25.5, mix(ORANGE, 0.45)), (25.5, vmax, mix(CRIMSON, 0.55))]
for a, b, c in regions:
    ax.add_patch(mp.Rectangle((sx(a), ybar), sx(b) - sx(a), 0.34, fc=c, ec="white", lw=2, zorder=2))
for v, t in [(10.5, "10 | 11"), (25.5, "25 | 26")]:
    label(ax, sx(v), ybar - 0.22, t, fs=11, c=TEXT2)
dec = [(5.25, "호르몬\n치료만"), (18, "호르몬 치료만 해도\n항암 추가와 성적 비슷\n(TAILORx)"), (35.25, "항암화학요법\n추가")]
for v, t in dec:
    label(ax, sx(v), ybar - 0.78, t, fs=11, c=TEXT, linespacing=1.35, va="center")
label(ax, sx(18), ybar - 1.42, "50세 이하·16–25점은 항암 이득 일부", fs=11, c=TEXT2)

# 케이스의 두 환자
for v, t, col in [(12, "환자 A · 12점", CAT[1]), (31, "환자 B · 31점", CAT[0])]:
    ax.add_patch(mp.Polygon([(sx(v) - 0.12, ybar + 0.64), (sx(v) + 0.12, ybar + 0.64), (sx(v), ybar + 0.42)],
                            closed=True, fc=col, ec="none", zorder=4))
    label(ax, sx(v), ybar + 0.88, t, fs=12, w="bold", c=col)
label(ax, 0.1, 2.85, "같은 병기, 같은 수용체 상태 — 점수가 치료를 가름", fs=12, w="semibold", c=TEXT, ha="left")
save(fig, "../../assets/img/w09/oncotype.png")
