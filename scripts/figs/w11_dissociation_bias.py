# W11 §2.1 해리 편향: 조직 안의 실제 구성(왼쪽)과 해리 후 시퀀서에 도착한 구성(오른쪽)
# (BI_for_Biomed W5 dissociation_bias를 한글로 다시 그림)
from medfig import *

fig, ax = new(8.1, 5.0)
GREY = "#8A919C"
big = [("신경세포", CAT[0]), ("지방세포", CAT[1]), ("심근세포", CAT[3])]
PW, Y0, Y1 = 3.5, 1.6, 4.85          # 패널 폭, 아래·위

def panel(x0, title, ec, lw):
    box(ax, x0, Y0, PW, Y1 - Y0, fc="white", ec=ec, lw=lw, r=0.12)
    label(ax, x0 + 0.2, Y1 - 0.32, title, fs=13, w="bold", ha="left")

# 왼쪽: 조직 안
panel(0, "조직 안", LINE, 1.2)
for i, (nm, c) in enumerate(big):
    cx = 0.65 + i * 1.1
    ax.add_patch(mp.Circle((cx, 3.6), 0.47, fc=mix(c, 0.35), ec="none", zorder=3))
    label(ax, cx, 3.6, nm, fs=11, w="semibold", c=TEXT)
for i in range(6):
    ax.add_patch(mp.Circle((0.45 + i * 0.52, 2.5 + (0.08 if i % 2 else -0.04)), 0.17, fc=GREY, ec="none", zorder=3))
label(ax, 0.2, 1.9, "큰 세포 3 · 작은 세포 6", fs=11, c=TEXT2, ha="left")

# 가운데: 해리
arrow(ax, 3.6, 3.2, 4.4, 3.2, color="#9AA1AB", lw=1.8)
label(ax, 4.0, 3.62, "해리", fs=11.5, w="semibold", c=TEXT)
label(ax, 4.0, 2.6, "효소\n37 °C\n30–60분", fs=11, c=TEXT2, linespacing=1.35)

# 오른쪽: 시퀀서에 도착한 세포
x0 = 4.55
panel(x0, "시퀀서에 도착한 세포", CRIMSON, 1.4)
for i in range(3):
    cx = x0 + 0.65 + i * 1.1
    ax.add_patch(mp.Circle((cx, 3.6), 0.47, fc="none", ec="#B8BDC5", lw=1.2, ls=(0, (3, 3)), zorder=3))
label(ax, x0 + PW / 2, 2.95, "해리 중 부서져 사라짐", fs=11, c=TEXT2)
for i in range(6):
    cx, cy = x0 + 0.45 + i * 0.52, 2.4 + (0.08 if i % 2 else -0.04)
    ax.add_patch(mp.Circle((cx, cy), 0.17, fc=GREY, ec="none", zorder=3))
    ax.add_patch(mp.Circle((cx + 0.12, cy + 0.12), 0.07, fc=CRIMSON, ec="white", lw=0.8, zorder=4))
label(ax, x0 + 0.2, 1.9, "큰 세포 0 · 작은 세포 6", fs=11, c=TEXT2, ha="left")

# 아래: 두 가지 변화와 결론
num(ax, 0.15, 1.1, 1, fc=WINE, r=0.14, fs=10.5)
label(ax, 0.4, 1.1, "구성이 바뀜", fs=12, w="bold", c=WINE, ha="left")
label(ax, 0.4, 0.68, "크고 약한 세포는 적게 셈", fs=11, ha="left")
num(ax, 4.7, 1.1, 2, fc=CRIMSON, r=0.14, fs=10.5)
label(ax, 4.95, 1.1, "살아남은 세포도", fs=12, w="bold", c=CRIMSON, ha="left")
ax.add_patch(mp.Circle((5.02, 0.68), 0.07, fc=CRIMSON, ec="white", lw=0.8, zorder=4))
label(ax, 5.17, 0.68, "스트레스 유전자를 켬 (FOS, JUN 등)", fs=11, ha="left")
label(ax, 0, 0.12, "측정한 구성 = 원래 구성이 아니라 살아남은 세포의 구성", fs=12, w="semibold", ha="left")
save(fig, "../../assets/img/w11/dissociation_bias.png")
