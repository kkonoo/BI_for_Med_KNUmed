# W9 §3 조직에서 count matrix까지 (BI_for_Biomed W4 rnaseq_workflow · read_to_count를 줄여 다시 그림)
from medfig import *

fig, ax = new(8.3, 6.3)

# ── 위: 다섯 단계 ─────────────────────────────────────────────
steps = [("조직", "수술·생검"), ("RNA 추출", "RNA만 뽑음"), ("시퀀싱", "cDNA로 읽음"),
         ("정렬", "read 위치 찾기"), ("세기", "유전자별 read 수")]
cols = ramp(5)
xs = [0.75 + i * 1.7 for i in range(5)]
y = 5.95
ax.plot([xs[0], xs[-1]], [y, y], color=LINE, lw=1.6, ls=(0, (4, 3)), zorder=1)
for i, ((name, sub), x) in enumerate(zip(steps, xs)):
    num(ax, x, y, i + 1, fc=cols[i], r=0.2, fs=11.5)
    label(ax, x, y - 0.46, name, fs=12.5, w="bold", c=cols[i])
    label(ax, x, y - 0.8, sub, fs=11, c=TEXT2)

ax.plot([0.1, 8.2], [4.7, 4.7], color=LINE, lw=1.0)

# ── 가운데: read를 유전자에 맞추고 세기 ───────────────────────
base = 2.5
ax.plot([0.3, 6.6], [base, base], color="#9AA1AB", lw=1.4, zorder=1)
exA = [(0.7, 1.9), (2.75, 3.75)]
exB = [(4.8, 6.2)]
for a, b in exA:
    box(ax, a, base - 0.15, b - a, 0.3, fc=CAT[0], ec="none", r=0.05, z=2)
for a, b in exB:
    box(ax, a, base - 0.15, b - a, 0.3, fc=CAT[1], ec="none", r=0.05, z=2)
label(ax, 2.22, base - 0.48, "유전자 A", fs=12, w="semibold", c=CAT[0])
label(ax, 5.5, base - 0.48, "유전자 B", fs=12, w="semibold", c=CAT[1])


def read(x0, x1, yy, col, split=None):
    h = 0.13
    if split:  # 엑손 경계를 건너뛰는 read: 두 조각을 점선으로 이음
        (a0, a1), (b0, b1) = split
        box(ax, a0, yy, a1 - a0, h, fc=col, ec="none", r=0.05, z=3)
        box(ax, b0, yy, b1 - b0, h, fc=col, ec="none", r=0.05, z=3)
        ax.plot([a1, b0], [yy + h / 2, yy + h / 2], color=col, lw=1.0, ls=(0, (2, 2)), zorder=3)
    else:
        box(ax, x0, yy, x1 - x0, h, fc=col, ec="none", r=0.05, z=3)


rA = mix(CAT[0], 0.7)
for (a, b, row) in [(0.75, 1.55, 0), (2.8, 3.6, 0), (1.05, 1.85, 1), (2.95, 3.72, 1), (0.78, 1.58, 2)]:
    read(a, b, base + 0.3 + row * 0.24, rA)
read(0, 0, base + 1.02, rA, split=((1.4, 1.9), (2.75, 3.05)))
read(0, 0, base + 1.26, rA, split=((1.55, 1.9), (2.75, 3.2)))
rB = mix(CAT[1], 0.7)
for k, (a, b) in enumerate([(4.9, 5.7), (5.3, 6.1), (5.0, 5.8)]):
    read(a, b, base + 0.3 + k * 0.24, rB)
label(ax, 2.22, base + 1.75, "read 7개", fs=12, w="bold", c=CAT[0])
label(ax, 5.5, base + 1.75, "read 3개", fs=12, w="bold", c=CAT[1])
label(ax, 3.35, base + 1.2, "← 엑손 경계를 건너뛴 read", fs=11, c=TEXT2, ha="left")

# ── 아래: count matrix ───────────────────────────────────────
x0, ytop, cw, rh = 3.6, 1.15, 1.0, 0.36
hdr = ["시료 1", "시료 2", "시료 3"]
rows = [("유전자 A", CAT[0], [7, 15, 4]), ("유전자 B", CAT[1], [3, 1, 11]), ("유전자 C", TEXT2, [0, 2, 1])]
box(ax, x0 + 0.05, ytop - 3 * rh - 0.06, cw - 0.1, 3 * rh + 0.46, fc=mix(CRIMSON, 0.1), ec="none", r=0.06, z=1)
for j, h in enumerate(hdr):
    label(ax, x0 + (j + 0.5) * cw, ytop + 0.19, h, fs=11, w="semibold", c=TEXT)
for i, (g, c, vals) in enumerate(rows):
    yy = ytop - (i + 0.5) * rh
    label(ax, x0 - 0.15, yy, g, fs=11.5, w="semibold", c=c, ha="right")
    for j, v in enumerate(vals):
        label(ax, x0 + (j + 0.5) * cw, yy, str(v), fs=12, w="bold" if j == 0 else "regular",
              c=TEXT if j == 0 else "#4B5563")
    ax.plot([x0, x0 + 3 * cw], [ytop - (i + 1) * rh, ytop - (i + 1) * rh], color=LINE, lw=0.9, zorder=2)
ax.plot([x0, x0 + 3 * cw], [ytop, ytop], color="#9AA1AB", lw=1.0, zorder=2)
label(ax, 0.2, ytop - 0.15, "count matrix", fs=12.5, w="bold", c=TEXT, ha="left")
label(ax, 0.2, ytop - 0.55, "행 = 유전자\n열 = 시료\n칸 = read 수", fs=11, c=TEXT2, ha="left", va="top",
      linespacing=1.4)
save(fig, "../../assets/img/w09/read_to_count.png")
