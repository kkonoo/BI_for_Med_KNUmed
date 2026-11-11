# W11 §2.2 Droplet, barcode, UMI: 물방울 하나 = 구슬 하나(+세포), read마다 세포 바코드와 UMI → 유전자 × 세포 표
# (BI_for_Biomed W5 droplet_loading, barcode_umi를 합쳐 한글로 다시 그림)
# 색 = 어느 세포(바코드), 회색 단계 = 어느 분자(UMI)
from medfig import *

fig, ax = new(10.6, 5.6)
GREY = "#8A919C"
UMI = [("#4B5563", "GATTC"), ("#8A919C", "TTAGC"), ("#C4C9D0", "CCGAA")]   # 분자 셋
beads = ramp(9)
BC = beads[1]                       # 오른쪽 아래에서 따라가는 세포의 바코드 색

# ① 물방울 ─────────────────────────────────────────────────────────────
num(ax, 0.22, 5.35, 1, fc=TEXT, r=0.12, fs=9)
label(ax, 0.42, 5.35, "물방울 하나 = 바코드 구슬 하나 (+ 세포)", fs=11.5, w="bold", ha="left")
box(ax, 0.1, 4.05, 7.4, 0.9, fc=FAINT, ec="none", r=0.45)
cells = [0, 1, 0, 0, 1, 0, 2, 0, 1]
for i, n in enumerate(cells):
    cx, cy = 0.62 + i * 0.79, 4.5
    ax.add_patch(mp.Circle((cx, cy), 0.33, fc="white", ec="#B8BDC5", lw=1.1, zorder=3))
    ax.add_patch(mp.Circle((cx + 0.12, cy - 0.1), 0.1, fc=beads[i], ec="none", zorder=4))
    for k in range(n):
        ax.add_patch(mp.Circle((cx - 0.1 + k * 0.13, cy + 0.08 - k * 0.04), 0.11, fc=GREY, ec="white", lw=0.8, zorder=5))
label(ax, 0.62, 3.95, "빈 방울\n(구슬만)", fs=9.5, c=TEXT2, va="top", linespacing=1.3)
label(ax, 0.62 + 0.79, 3.95, "세포 1개", fs=9.5, c=TEXT, va="top")
label(ax, 0.62 + 6 * 0.79, 3.95, "세포 2개\n= 이중세포", fs=9.5, c=CRIMSON, va="top", linespacing=1.3)
label(ax, 7.8, 4.72, "구슬마다 바코드가 다름", fs=10.5, w="semibold", ha="left")
label(ax, 7.8, 4.32, "→ 바코드 = 세포의 주소", fs=10.5, ha="left")

ax.plot([0.1, 10.5], [3.05, 3.05], color=LINE, lw=1)

# ② read 7개 → 분자 3개 ───────────────────────────────────────────────
num(ax, 0.22, 2.75, 2, fc=TEXT, r=0.12, fs=9)
label(ax, 0.42, 2.75, "세포 하나에서 읽은 유전자 X의 read 7개", fs=11.5, w="bold", ha="left")
seg = [(0.25, 0.75, "세포 바코드"), (1.03, 0.6, "UMI"), (1.66, 1.45, "RNA 서열 → 유전자 X")]
for x, w, t in seg:
    label(ax, x + w / 2, 2.38, t, fs=9, c=TEXT2)
umis = [UMI[0]] * 3 + [UMI[1]] * 2 + [UMI[2]] * 2
for j, (uc, useq) in enumerate(umis):
    y = 2.05 - j * 0.25 - (0.08 if j >= 3 else 0) - (0.08 if j >= 5 else 0)
    box(ax, 0.25, y, 0.75, 0.17, fc=BC, ec="none", r=0.03)
    box(ax, 1.03, y, 0.6, 0.17, fc=uc, ec="none", r=0.03)
    label(ax, 1.33, y + 0.085, useq, fs=8.5, c="white" if uc != UMI[2][0] else TEXT, family="DejaVu Sans Mono")
    box(ax, 1.66, y, 1.45, 0.17, fc=mix(CRIMSON, 0.15), ec="none", r=0.03)
arrow(ax, 3.3, 1.2, 3.85, 1.2, color="#9AA1AB", lw=1.6)
for k, (c, _) in enumerate(UMI):
    ax.add_patch(mp.Circle((4.15 + k * 0.33, 1.2), 0.13, fc=c, ec="none", zorder=3))
label(ax, 5.05, 1.2, "= 분자 3개", fs=12, w="bold", ha="left")
label(ax, 0.25, 0.12, "같은 UMI = 한 분자를 PCR로 불린 복사본 → 하나로 셈", fs=10, c=TEXT, ha="left")

# ③ 유전자 × 세포 표 ────────────────────────────────────────────────────
num(ax, 6.5, 2.75, 3, fc=TEXT, r=0.12, fs=9)
label(ax, 6.7, 2.75, "유전자 × 세포 표 (분자 수)", fs=11.5, w="bold", ha="left")
cols = [beads[1], beads[4], beads[8]]
vals = [[3, 0, 1], [0, 2, 0], [1, 0, 0], [0, 0, 0]]
genes = ["유전자 X", "유전자 Y", "유전자 Z", "…"]
for c, col in enumerate(cols):
    cx = 8.2 + c * 0.75
    ax.add_patch(mp.Circle((cx, 2.38), 0.09, fc=col, ec="none", zorder=3))
    label(ax, cx, 2.17, f"세포 {c + 1}", fs=9, c=TEXT2)
for r, (g, row) in enumerate(zip(genes, vals)):
    y = 1.78 - r * 0.42
    label(ax, 7.75, y, g, fs=10, c=TEXT, ha="right")
    for c, v in enumerate(row):
        cx = 8.2 + c * 0.75
        hl = (r == 0 and c == 0)
        box(ax, cx - 0.32, y - 0.17, 0.64, 0.34, fc=mix(CRIMSON, 0.15) if hl else FAINT,
            ec=CRIMSON if hl else "none", lw=1.3, r=0.05)
        if g != "…":
            label(ax, cx, y, str(v), fs=11, w="bold" if v else "regular", c=TEXT if v else "#A3A9B2")
label(ax, 6.7, 0.12, "대부분의 칸이 0", fs=10, c=TEXT, ha="left")
save(fig, "../../assets/img/w11/barcode_umi.png")
