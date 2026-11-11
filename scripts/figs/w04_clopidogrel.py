# W4 §4.2 클로피도그렐 = 전구약물. CYP2C19가 활성형으로 바꿔야 혈소판을 억제
# 정상 대사형(*1/*1) vs 대사 저하형(*2/*2), 권고는 장의 CPIC 표(Lee 2022)와 같게
from medfig import *

fig, ax = new(8.4, 5.1)
W, H, gap, x0 = 1.78, 1.05, 0.38, 0.1
steps = [("클로피도그렐", "전구약물"), ("CYP2C19", ""), ("활성형", ""), ("혈소판 억제", "")]
cols = [WINE, CRIMSON, ORANGE, AMBER]
rows = [
    ("정상 대사형", "*1/*1", [None, "간에서 활성화", 7, "충분 → 혈전 예방"]),
    ("대사 저하형", "*2/*2", [None, "기능 없음 ✕", 1, "부족 → 혈전 위험"]),
]
for r, (name, gt, subs) in enumerate(rows):
    y = 3.35 - r * 1.75
    label(ax, x0, y + H + 0.3, name, fs=13, w="bold", ha="left")
    label(ax, x0 + 1.2, y + H + 0.3, gt, fs=12, c=TEXT2, ha="left")
    for k, ((title, sub0), c) in enumerate(zip(steps, cols)):
        x = x0 + k * (W + gap)
        broken = (r == 1 and k == 1)
        weak = (r == 1 and k == 3)
        cc = BLUE if broken else c
        box(ax, x, y, W, H, fc=mix(cc, 0.12), ec=cc, lw=1.5, r=0.1, ls=(0, (4, 3)) if weak else "-")
        label(ax, x + W / 2, y + 0.72, title, fs=13, w="bold", c=cc)
        if k == 2:  # active drug molecules
            n = subs[k]
            for j in range(n):
                ax.add_patch(mp.Circle((x + W / 2 - (n - 1) * 0.1 + j * 0.2, y + 0.32), 0.065,
                                       fc=c, ec="none", zorder=4))
        else:
            sub = subs[k] if subs[k] is not None else sub0
            label(ax, x + W / 2, y + 0.32, sub, fs=11, c=BLUE if broken else TEXT2,
                  w="bold" if broken else "regular")
        if k < 3:
            arrow(ax, x + W + 0.05, y + H / 2, x + W + gap - 0.05, y + H / 2,
                  color="#C4C7CC" if (r == 1 and k >= 1) else "#9AA1AB", lw=1.8, ms=10)
label(ax, x0, 0.85, "*2 = splicing 이상으로 기능 있는 효소를 만들지 못하는 대립유전자 (한국인 약 28%)",
      fs=10.5, c=TEXT2, ha="left")
label(ax, x0, 0.42, "CPIC: 대사 저하형 → 클로피도그렐을 피하고, 금기가 없으면 prasugrel 또는 ticagrelor",
      fs=11, ha="left", w="semibold")
save(fig, "../../assets/img/w04/clopidogrel.png")
