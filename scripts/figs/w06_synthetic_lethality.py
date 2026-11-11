# W6 §7 합성치사: BRCA가 망가진 종양 세포 + PARP 억제제 → 두 복구 경로를 다 잃고 죽음
from medfig import *

HR, PARP = CRIMSON, ORANGE                      # the two repair pathways
OFF = "#ECEDF0"
fig, ax = new(7.9, 4.9)

X0, Y0, CW, CH = 1.75, 0.1, 3.05, 1.95          # grid origin and cell size
cols = ["PARP 억제제 없음", "PARP 억제제"]
rows = [("BRCA가", "망가진", "종양 세포"), ("정상 세포", "", "")]


def path(x, y, name, sub, col, on):
    box(ax, x, y, 1.95, 0.48, fc=col if on else OFF, ec="none", r=0.24, z=3)
    c = "white" if on else "#9AA1AB"
    label(ax, x + 0.15, y + 0.24, name, fs=11, w="bold", c=c, ha="left", z=5)
    label(ax, x + 1.82, y + 0.24, sub, fs=10, c=c, ha="right", z=5)
    if not on:
        ax.plot([x + 0.1, x + 1.85], [y + 0.24, y + 0.24], color="#9AA1AB", lw=1.4, zorder=6)


for j, c in enumerate(cols):
    label(ax, X0 + CW * (j + 0.5), Y0 + 2 * CH + 0.3, c, fs=12.5, w="bold", c=TEXT)
for i, lines in enumerate(rows):
    yc = Y0 + CH * (i + 0.5)
    lines = [t for t in lines if t]
    for k, t in enumerate(lines):
        label(ax, X0 - 0.15, yc + (len(lines) - 1) * 0.16 - k * 0.32, t, fs=12, w="bold", c=TEXT, ha="right")

for i in range(2):              # i = 0: BRCA-deficient tumour (bottom), 1: normal (top)
    for j in range(2):          # j = 0: no drug, 1: PARP inhibitor
        x, y = X0 + j * CW, Y0 + i * CH
        dies = (i == 0 and j == 1)
        box(ax, x + 0.05, y + 0.05, CW - 0.1, CH - 0.1, fc=mix(BLUE, 0.08) if dies else FAINT,
            ec=BLUE if dies else "none", lw=1.6, r=0.12, z=2)
        hr_on, parp_on = (i == 1), (j == 0)
        path(x + 0.18, y + 1.05, "상동 재조합", "BRCA", HR, hr_on)
        path(x + 0.18, y + 0.42, "한 가닥 복구", "PARP", PARP, parp_on)
        if dies:
            label(ax, x + 2.0 + 0.53, y + 1.15, "죽음", fs=13, w="bold", c=BLUE)
            label(ax, x + 2.0 + 0.53, y + 0.8, "합성치사", fs=11, w="bold", c=BLUE)
        else:
            label(ax, x + 2.0 + 0.53, y + 1.15, "생존", fs=13, w="bold", c=TEXT)
            sub = "둘 다 작동" if hr_on and parp_on else "남은 길로"
            label(ax, x + 2.0 + 0.53, y + 0.8, sub, fs=11, c=TEXT2)
save(fig, "../../assets/img/w06/synthetic_lethality.png")
