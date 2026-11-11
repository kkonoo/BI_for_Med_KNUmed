# W9 §3 조직에서 count matrix까지 (BI_for_Biomed W4 rnaseq_workflow · read_to_count를 줄여 다시 그림)
from medfig import *

fig, ax = new(10.6, 4.3)

# ── 위: 다섯 단계 ─────────────────────────────────────────────
steps = [("조직", "수술·생검으로 얻은 조각"), ("RNA 추출", "RNA만 뽑아냄"), ("시퀀싱", "cDNA로 바꿔 읽음"),
         ("정렬", "read가 온 유전자 찾기"), ("세기", "유전자마다 read 수")]
cols = ramp(5)
xs = [0.75 + i * 2.25 for i in range(5)]
y = 3.95
ax.plot([xs[0], xs[-1]], [y, y], color=LINE, lw=1.6, ls=(0, (4, 3)), zorder=1)
for i, ((name, sub), x) in enumerate(zip(steps, xs)):
    num(ax, x, y, i + 1, fc=cols[i], r=0.19, fs=11)
    label(ax, x, y - 0.42, name, fs=12, w="bold", c=cols[i])
    label(ax, x, y - 0.74, sub, fs=9.5, c=TEXT2)

# ── 아래 왼쪽: read를 유전자에 맞추고 세기 ─────────────────────
base = 0.75
ax.plot([0.2, 5.6], [base, base], color="#9AA1AB", lw=1.4, zorder=1)
exA = [(0.55, 1.55), (2.25, 3.1)]
exB = [(4.0, 5.2)]
for a, b in exA:
    box(ax, a, base - 0.13, b - a, 0.26, fc=CAT[0], ec="none", r=0.04, z=2)
for a, b in exB:
    box(ax, a, base - 0.13, b - a, 0.26, fc=CAT[1], ec="none", r=0.04, z=2)
label(ax, 1.83, base - 0.42, "유전자 A", fs=10.5, w="semibold", c=CAT[0])
label(ax, 4.6, base - 0.42, "유전자 B", fs=10.5, w="semibold", c=CAT[1])

def read(x0, x1, yy, col, split=None):
    if split:  # 엑손 경계를 건너뛰는 read: 두 조각을 점선으로 이음
        (a0, a1), (b0, b1) = split
        box(ax, a0, yy, a1 - a0, 0.11, fc=col, ec="none", r=0.04, z=3)
        box(ax, b0, yy, b1 - b0, 0.11, fc=col, ec="none", r=0.04, z=3)
        ax.plot([a1, b0], [yy + 0.055, yy + 0.055], color=col, lw=0.9, ls=(0, (2, 2)), zorder=3)
    else:
        box(ax, x0, yy, x1 - x0, 0.11, fc=col, ec="none", r=0.04, z=3)

rA = mix(CAT[0], 0.7)
for (a, b, row) in [(0.6, 1.25, 0), (2.3, 2.95, 0), (0.85, 1.5, 1), (2.45, 3.08, 1), (0.62, 1.27, 2)]:
    read(a, b, base + 0.28 + row * 0.2, rA)
read(0, 0, base + 0.88, rA, split=((1.15, 1.55), (2.25, 2.5)))
read(0, 0, base + 1.08, rA, split=((1.3, 1.55), (2.25, 2.65)))
rB = mix(CAT[1], 0.7)
for k, (a, b) in enumerate([(4.1, 4.75), (4.45, 5.1), (4.2, 4.85)]):
    read(a, b, base + 0.28 + k * 0.2, rB)
label(ax, 1.83, base + 1.5, "read 7개", fs=10.5, w="bold", c=CAT[0])
label(ax, 4.6, base + 1.5, "read 3개", fs=10.5, w="bold", c=CAT[1])
label(ax, 2.75, base + 0.98, "← 엑손 경계를 건너뛴 read", fs=9, c=TEXT2, ha="left")

arrow(ax, 5.85, 1.45, 6.45, 1.45, color="#9AA1AB", lw=1.8)

# ── 아래 오른쪽: count matrix ────────────────────────────────
x0, ytop, cw, rh = 7.85, 2.35, 0.82, 0.42
hdr = ["시료 1", "시료 2", "시료 3"]
rows = [("유전자 A", CAT[0], [7, 15, 4]), ("유전자 B", CAT[1], [3, 1, 11]), ("유전자 C", TEXT2, [0, 2, 1])]
box(ax, x0 + 0.02, ytop - 3 * rh - 0.08, cw - 0.04, 3 * rh + 0.5, fc=mix(CRIMSON, 0.1), ec="none", r=0.06, z=1)
for j, h in enumerate(hdr):
    label(ax, x0 + (j + 0.5) * cw, ytop + 0.2, h, fs=10, w="semibold", c=TEXT)
for i, (g, c, vals) in enumerate(rows):
    yy = ytop - (i + 0.5) * rh
    label(ax, x0 - 0.12, yy, g, fs=10.5, w="semibold", c=c, ha="right")
    for j, v in enumerate(vals):
        label(ax, x0 + (j + 0.5) * cw, yy, str(v), fs=11, w="bold" if j == 0 else "regular",
              c=TEXT if j == 0 else "#4B5563")
    ax.plot([x0, x0 + 3 * cw], [ytop - (i + 1) * rh, ytop - (i + 1) * rh], color=LINE, lw=0.9, zorder=2)
ax.plot([x0, x0 + 3 * cw], [ytop, ytop], color="#9AA1AB", lw=1.0, zorder=2)
label(ax, x0 + 1.5 * cw - 0.35, ytop - 3 * rh - 0.38, "행 = 유전자, 열 = 시료, 칸 = read 수", fs=9.5, c=TEXT2)
save(fig, "../../assets/img/w09/read_to_count.png")
