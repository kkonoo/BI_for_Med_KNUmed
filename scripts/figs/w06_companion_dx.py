# W6 §3.2 동반진단: 검사 결과가 약을 고르는 흐름 (케이스: 폐선암, EGFR exon 19 결실)
from medfig import *

fig, ax = new(7.8, 3.5)


def card(x, y, w, h, title, sub, fc, tc="white", sc=None):
    box(ax, x, y, w, h, fc=fc, ec="none", r=0.1)
    label(ax, x + w / 2, y + h * 0.64, title, fs=12.5, w="bold", c=tc)
    label(ax, x + w / 2, y + h * 0.3, sub, fs=11, c=sc or tc)


W, H, Y = 1.55, 1.0, 1.1
card(0.05, Y, W, H, "폐선암 4기", "종양 조직·혈액", mix(CRIMSON, 0.12), tc=CRIMSON, sc=TEXT2)
arrow(ax, 1.66, Y + H / 2, 1.9, Y + H / 2)
card(1.95, Y, W, H, "NGS 패널", "= 동반진단 검사", WINE)
arrow(ax, 3.56, Y + H / 2, 3.8, Y + H / 2)
card(3.85, Y, W, H, "EGFR 활성화", "변이가 있나?", CRIMSON)

# yes / no
arrow(ax, 5.47, Y + 0.78, 5.83, 2.45, color=BLUE, lw=2.2, ms=14)
label(ax, 5.5, 2.3, "예", fs=12, w="bold", c=BLUE)
card(5.9, 2.15, 1.85, 0.95, "EGFR 억제제", "osimertinib 등", ORANGE)
arrow(ax, 5.47, Y + 0.22, 5.83, 0.75)
label(ax, 5.42, 0.8, "아니오", fs=11, w="bold", c=TEXT2)
card(5.9, 0.1, 1.85, 0.95, "다른 driver 확인", "ALK 융합 등", AMBER)

label(ax, 5.9 + 1.85 / 2, 3.3, "케이스: exon 19 결실", fs=12, w="bold", c=BLUE)
save(fig, "../../assets/img/w06/companion_dx.png")
