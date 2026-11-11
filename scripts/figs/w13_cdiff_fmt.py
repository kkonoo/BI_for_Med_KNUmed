# W13 §7 케이스: 항생제 → 공동체 붕괴 → C. difficile → 또 항생제의 재발 고리, FMT가 고리를 끊음
# 숫자는 장 본문 §5.3의 van Nood et al., NEJM 2013
from medfig import *

fig, ax = new(8.2, 5.7)
BH = 0.84
GREY = "#9AA1AB"


def node(cx, cy, text, fc, w, h=BH, fs=11):
    box(ax, cx - w / 2, cy - h / 2, w, h, fc=fc, ec="none", r=0.1)
    label(ax, cx, cy, text, fs=fs, w="bold", c="white", linespacing=1.35)


# the relapse loop (top left)
node(0.6, 5.05, "광범위\n항생제", WINE, w=1.1)
node(2.85, 5.05, "장내 공동체 붕괴\n집락 저항성 상실", CRIMSON, w=2.25)
node(3.85, 2.85, "C. difficile 증식·독소\n→ 장염 (설사)", ORANGE, w=2.45)
node(1.05, 2.85, "장염 치료에\n또 항생제", WINE, w=1.75)
arrow(ax, 1.2, 5.05, 1.68, 5.05, color=GREY, lw=2)
arrow(ax, 3.55, 4.6, 4.0, 3.3, color=GREY, lw=2, rad=-0.2)           # 붕괴 → C. difficile
arrow(ax, 2.58, 2.85, 1.98, 2.85, color=GREY, lw=2)                   # C. difficile → 또 항생제
arrow(ax, 0.95, 3.3, 2.15, 4.6, color=GREY, lw=2, rad=-0.2)           # 또 항생제 → 붕괴
label(ax, 2.55, 3.88, "재발이\n반복되는 고리", fs=11, c=TEXT2, linespacing=1.35)

# FMT breaks the loop: the one accent
arrow(ax, 4.05, 5.05, 5.75, 5.05, color=BLUE, lw=2.6, ms=15)
label(ax, 4.9, 5.2, "FMT", fs=12.5, w="bold", c=BLUE, va="bottom")
label(ax, 4.9, 4.55, "공여자의 공동체를\n통째로 넣음", fs=11, c=TEXT, linespacing=1.35)
box(ax, 5.85, 4.4, 2.3, 1.3, fc=BLUE, ec="none", r=0.1)
label(ax, 7.0, 5.05, "다양성이 공여자\n수준으로 회복\n→ 집락 저항성 복구", fs=11, w="bold", c="white",
      linespacing=1.4)

# van Nood 2013 result (bottom)
label(ax, 0.05, 1.82, "첫 치료 뒤 설사가 멈추고 재발 없음 (van Nood 2013)", fs=11, c=TEXT2, ha="left")
rows = [("공여자 대변 이식", 13, 16, BLUE), ("반코마이신", 4, 13, "#C4C7CC"), ("반코마이신 + 장 세척", 3, 13, "#C4C7CC")]
bx, full = 2.55, 3.6
for i, (name, k, n, c) in enumerate(rows):
    y = 1.3 - i * 0.5
    label(ax, 0.05, y, name, fs=11.5, ha="left", w="bold" if i == 0 else "regular")
    box(ax, bx, y - 0.14, full, 0.28, fc=FAINT, ec="none", r=0.05)
    box(ax, bx, y - 0.14, full * k / n, 0.28, fc=c, ec="none", r=0.05, z=3)
    label(ax, bx + full + 0.12, y, f"{round(100 * k / n)}%  ({k}/{n})", fs=11.5, ha="left",
          w="bold" if i == 0 else "regular", c=BLUE if i == 0 else TEXT)
save(fig, "../../assets/img/w13/cdiff_fmt.png")
