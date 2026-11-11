# W13 §7 케이스: 항생제 → 공동체 붕괴 → C. difficile → 또 항생제의 재발 고리, FMT가 고리를 끊음
# 숫자는 장 본문 §5.3의 van Nood et al., NEJM 2013
from medfig import *

fig, ax = new(10.8, 4.7)
BW, BH = 2.2, 0.82
GREY = "#9AA1AB"


def node(cx, cy, text, fc, w=BW, h=BH, fs=10.5):
    box(ax, cx - w / 2, cy - h / 2, w, h, fc=fc, ec="none", r=0.1)
    label(ax, cx, cy, text, fs=fs, w="bold", c="white", linespacing=1.35)


# entry and the relapse loop (left)
node(0.75, 3.75, "광범위\n항생제", WINE, w=1.2)
node(3.25, 3.75, "장내 공동체 붕괴\n집락 저항성 상실", CRIMSON)
node(4.6, 1.3, "C. difficile 증식·독소\n→ 장염 (설사)", ORANGE)
node(1.55, 1.3, "장염 치료에\n또 항생제", WINE)
arrow(ax, 1.4, 3.75, 2.05, 3.75, color=GREY, lw=2)
arrow(ax, 4.0, 3.3, 4.6, 1.76, color=GREY, lw=2, rad=-0.2)          # 붕괴 → C. difficile
arrow(ax, 3.45, 1.3, 2.7, 1.3, color=GREY, lw=2)                     # C. difficile → 또 항생제
arrow(ax, 1.45, 1.76, 2.45, 3.3, color=GREY, lw=2, rad=-0.2)         # 또 항생제 → 붕괴
label(ax, 3.05, 2.5, "재발이\n반복되는 고리", fs=10, c=TEXT2, linespacing=1.35)

# FMT breaks the loop (right): the one accent
arrow(ax, 4.45, 3.75, 6.75, 3.75, color=BLUE, lw=2.6, ms=15)
label(ax, 5.6, 3.9, "FMT", fs=11.5, w="bold", c=BLUE, va="bottom")
label(ax, 5.6, 3.3, "건강한 공여자의\n공동체를 통째로 넣음", fs=9.5, c=TEXT, linespacing=1.35)
box(ax, 6.85, 3.3, 3.85, 0.9, fc=BLUE, ec="none", r=0.1)
label(ax, 8.775, 3.75, "다양성이 공여자 수준으로 회복\n→ 집락 저항성(방어막) 복구", fs=10.5, w="bold", c="white",
      linespacing=1.4)

# van Nood 2013 result
label(ax, 6.85, 2.55, "첫 치료 뒤 설사가 멈추고 재발 없음 (van Nood 2013)", fs=9.5, c=TEXT2, ha="left")
rows = [("공여자 대변 이식", 13, 16, BLUE), ("반코마이신", 4, 13, "#C4C7CC"), ("반코마이신 + 장 세척", 3, 13, "#C4C7CC")]
bx, full = 8.45, 1.5
for i, (name, k, n, c) in enumerate(rows):
    y = 2.05 - i * 0.48
    label(ax, 6.85, y, name, fs=10, ha="left", w="bold" if i == 0 else "regular")
    box(ax, bx, y - 0.13, full, 0.26, fc=FAINT, ec="none", r=0.05)
    box(ax, bx, y - 0.13, full * k / n, 0.26, fc=c, ec="none", r=0.05, z=3)
    label(ax, bx + full + 0.1, y, f"{round(100 * k / n)}%  ({k}/{n})", fs=10, ha="left",
          w="bold" if i == 0 else "regular", c=BLUE if i == 0 else TEXT)
save(fig, "../../assets/img/w13/cdiff_fmt.png")
