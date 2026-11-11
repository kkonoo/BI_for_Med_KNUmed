# W6 §1.1 생식세포 변이 vs 체세포 변이: 어느 세포에 있나, 시료마다 무엇이 보이나
from medfig import *

GERM, SOMA = WINE, ORANGE                       # the two kinds of variant
NORMAL_FC, NORMAL_EC = "#F1F2F4", "#D5D8DD"
TUMOUR_FC, TUMOUR_EC = mix(CRIMSON, 0.2), mix(CRIMSON, 0.55)

fig, ax = new(7.7, 6.6)


def tissue(x0, y0, somatic):
    """A patch of tissue: grid of cells, a tumour cluster on the right."""
    nx, ny, r, step = 10, 5, 0.1, 0.25
    cx, cy = x0 + 6.9 * step, y0 + 2.0 * step         # tumour centre
    for i in range(nx):
        for j in range(ny):
            x, y = x0 + i * step + (0.12 if j % 2 else 0), y0 + j * step
            tum = ((x - cx) / 0.72) ** 2 + ((y - cy) / 0.48) ** 2 <= 1
            ax.add_patch(mp.Circle((x, y), r, fc=TUMOUR_FC if tum else NORMAL_FC,
                                   ec=TUMOUR_EC if tum else NORMAL_EC, lw=0.9, zorder=2))
            if (not somatic) or tum:
                ax.add_patch(mp.Circle((x, y), 0.036, fc=SOMA if somatic else GERM, ec="none", zorder=3))
    return cx, cy


# ① ② where the variant is
for x0, somatic, tag, line1, line2 in [
        (0.25, False, "① 생식세포 변이", "몸의 거의 모든 세포에 있음", "→ 자녀에게 전달될 수 있음"),
        (4.15, True, "② 체세포 변이", "종양 세포에만 있음", "→ 자녀에게 전달되지 않음")]:
    col = SOMA if somatic else GERM
    label(ax, x0 - 0.1, 6.2, tag, fs=13, w="bold", c=col, ha="left")
    cx, cy = tissue(x0, 4.55, somatic)
    label(ax, cx, cy + 0.72, "종양", fs=11, w="semibold", c=CRIMSON)
    label(ax, x0 - 0.1, 4.12, line1, fs=11, c=TEXT, ha="left")
    label(ax, x0 - 0.1, 3.82, line2, fs=11, c=TEXT2, ha="left")

ax.plot([0.1, 7.6], [3.45, 3.45], color=LINE, lw=1)

# ③ what each sample shows
label(ax, 0.15, 3.12, "③ 시료마다 보이는 변이", fs=13, w="bold", c=TEXT, ha="left")
cols = [(3.7, "생식세포 변이", GERM), (5.6, "체세포 변이", SOMA)]
for x, name, c in cols:
    label(ax, x, 2.7, name, fs=11, w="semibold", c=c)
for y, name, has in [(2.2, "종양 조직", (True, True)), (1.55, "혈액 (정상 세포)", (True, False))]:
    box(ax, 0.15, y - 0.26, 6.6, 0.52, fc=FAINT, ec="none", r=0.08)
    label(ax, 0.35, y, name, fs=11, w="semibold", ha="left")
    for (x, _, c), h in zip(cols, has):
        if h:
            ax.add_patch(mp.Circle((x, y), 0.11, fc=c, ec="none", zorder=4))
        else:
            label(ax, x, y, "없음", fs=11, c=TEXT2)

# conclusions
label(ax, 0.15, 0.92, "종양만 읽으면 두 변이가 똑같이 '종양에서 찾은 변이'로 보고됨 → 구별 못 함",
      fs=11, w="bold", c=BLUE, ha="left")
label(ax, 0.15, 0.55, "혈액도 함께 읽어 겹치는 것을 빼면 체세포 변이만 남음 (종양-정상 쌍)",
      fs=11, c=TEXT, ha="left")
save(fig, "../../assets/img/w06/germline_somatic.png")
