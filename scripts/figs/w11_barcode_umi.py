# W11 §2.2 Droplet, barcode, UMI: 물방울 하나 = 구슬 하나(+세포), read마다 세포 바코드와 UMI → 유전자 × 세포 표
# (BI_for_Biomed W5 droplet_loading, barcode_umi를 합쳐 한글로 다시 그림)
# 색 = 어느 세포(바코드), 회색 단계 = 어느 분자(UMI)
from medfig import *

fig, ax = new(8.2, 7.1)
GREY = "#8A919C"
UMI = [("#4B5563", "GATTC"), ("#8A919C", "TTAGC"), ("#C4C9D0", "CCGAA")]   # 분자 셋
beads = ramp(9)
BC = beads[1]                       # ②에서 따라가는 세포의 바코드 색

# ① 물방울 ─────────────────────────────────────────────────────────────
num(ax, 0.15, 6.85, 1, fc=TEXT, r=0.14, fs=10.5)
label(ax, 0.4, 6.85, "물방울 하나 = 바코드 구슬 하나 (+ 세포)", fs=12.5, w="bold", ha="left")
box(ax, 0, 5.6, 8.2, 0.84, fc=FAINT, ec="none", r=0.42)
cells = [0, 1, 0, 0, 1, 0, 2, 0, 1]
for i, n in enumerate(cells):
    cx, cy = 0.5 + i * 0.9, 6.02
    ax.add_patch(mp.Circle((cx, cy), 0.33, fc="white", ec="#B8BDC5", lw=1.1, zorder=3))
    ax.add_patch(mp.Circle((cx + 0.12, cy - 0.1), 0.1, fc=beads[i], ec="none", zorder=4))
    for k in range(n):
        ax.add_patch(mp.Circle((cx - 0.1 + k * 0.13, cy + 0.08 - k * 0.04), 0.11, fc=GREY, ec="white", lw=0.8, zorder=5))
label(ax, 0.5, 5.45, "빈 방울\n(구슬만)", fs=11, c=TEXT2, va="top", linespacing=1.3)
label(ax, 0.5 + 0.9, 5.45, "세포 1개", fs=11, c=TEXT, va="top")
label(ax, 0.5 + 6 * 0.9, 5.45, "세포 2개\n= 이중세포", fs=11, c=CRIMSON, va="top", linespacing=1.3)
label(ax, 8.2, 4.75, "구슬마다 바코드가 다름 → 바코드 = 세포의 주소", fs=11.5, w="semibold", ha="right")

ax.plot([0, 8.2], [4.48, 4.48], color=LINE, lw=1)

# ② read 7개 → 분자 3개 ───────────────────────────────────────────────
num(ax, 0.15, 4.2, 2, fc=TEXT, r=0.14, fs=10.5)
label(ax, 0.4, 4.2, "한 세포, 유전자 X의 read 7개", fs=12.5, w="bold", ha="left")
seg = [(0.05, 0.9, "세포 바코드"), (1.02, 0.75, "UMI"), (1.84, 1.2, "RNA → 유전자 X")]
for x, w, t in seg:
    label(ax, x + w / 2, 3.78, t, fs=11, c=TEXT2)
umis = [UMI[0]] * 3 + [UMI[1]] * 2 + [UMI[2]] * 2
for j, (uc, useq) in enumerate(umis):
    y = 3.32 - j * 0.31 - (0.1 if j >= 3 else 0) - (0.1 if j >= 5 else 0)
    box(ax, 0.05, y, 0.9, 0.24, fc=BC, ec="none", r=0.04)
    box(ax, 1.02, y, 0.75, 0.24, fc=uc, ec="none", r=0.04)
    label(ax, 1.395, y + 0.12, useq, fs=10.5, c="white" if uc != UMI[2][0] else TEXT, family="DejaVu Sans Mono")
    box(ax, 1.84, y, 1.2, 0.24, fc=mix(CRIMSON, 0.15), ec="none", r=0.04)
arrow(ax, 3.2, 2.35, 3.65, 2.35, color="#9AA1AB", lw=1.6)
for k, (c, _) in enumerate(UMI):
    ax.add_patch(mp.Circle((3.95 + k * 0.36, 2.35), 0.14, fc=c, ec="none", zorder=3))
label(ax, 4.31, 1.88, "= 분자 3개", fs=13, w="bold")
label(ax, 0.05, 0.85, "같은 UMI = 한 분자를 PCR로 불린 복사본", fs=11, c=TEXT, ha="left")
label(ax, 0.05, 0.5, "→ 하나로 셈", fs=11, c=TEXT, ha="left")

# ③ 유전자 × 세포 표 ────────────────────────────────────────────────────
x3 = 5.2
num(ax, x3 + 0.15, 4.2, 3, fc=TEXT, r=0.14, fs=10.5)
label(ax, x3 + 0.4, 4.2, "유전자 × 세포 표", fs=12.5, w="bold", ha="left")
cols = [beads[1], beads[4], beads[8]]
vals = [[3, 0, 1], [0, 2, 0], [1, 0, 0], [0, 0, 0]]
genes = ["유전자 X", "유전자 Y", "유전자 Z", "…"]
for c, col in enumerate(cols):
    cx = x3 + 1.25 + c * 0.66
    ax.add_patch(mp.Circle((cx, 3.72), 0.1, fc=col, ec="none", zorder=3))
    label(ax, cx, 3.45, f"세포 {c + 1}", fs=11, c=TEXT2)
for r, (g, row) in enumerate(zip(genes, vals)):
    y = 2.98 - r * 0.47
    label(ax, x3 + 0.85, y, g, fs=11, c=TEXT, ha="right")
    for c, v in enumerate(row):
        cx = x3 + 1.25 + c * 0.66
        hl = (r == 0 and c == 0)
        box(ax, cx - 0.28, y - 0.19, 0.56, 0.38, fc=mix(CRIMSON, 0.15) if hl else FAINT,
            ec=CRIMSON if hl else "none", lw=1.3, r=0.05)
        if g != "…":
            label(ax, cx, y, str(v), fs=12, w="bold" if v else "regular", c=TEXT if v else "#A3A9B2")
label(ax, x3 + 0.05, 0.85, "칸 = 분자 수", fs=11, c=TEXT, ha="left")
label(ax, x3 + 0.05, 0.5, "대부분의 칸이 0", fs=11, c=TEXT, ha="left")
save(fig, "../../assets/img/w11/barcode_umi.png")
