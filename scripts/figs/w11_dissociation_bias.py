# W11 §2.1 해리 편향: 조직 안의 실제 구성과 해리 후 시퀀서에 도착한 구성
# (BI_for_Biomed W5 dissociation_bias를 한글로 다시 그림)
from medfig import *

fig, ax = new(10.4, 3.9)
GREY = "#8A919C"
big = [("신경세포", CAT[0]), ("지방세포", CAT[1]), ("심근세포", CAT[3])]

# 왼쪽: 조직 안
box(ax, 0.1, 0.55, 3.7, 3.05, fc="white", ec=LINE, lw=1.2, r=0.12)
label(ax, 0.3, 3.3, "조직 안", fs=12, w="bold", ha="left")
for i, (nm, c) in enumerate(big):
    cx = 0.75 + i * 1.18
    ax.add_patch(mp.Circle((cx, 2.4), 0.48, fc=mix(c, 0.35), ec="none", zorder=3))
    label(ax, cx, 2.4, nm, fs=10, w="semibold", c=TEXT)
for i in range(6):
    ax.add_patch(mp.Circle((0.55 + i * 0.56, 1.35 + (0.1 if i % 2 else -0.05)), 0.17, fc=GREY, ec="none", zorder=3))
label(ax, 0.3, 0.8, "크고 약한 세포 3 · 작고 튼튼한 세포 6", fs=9.5, c=TEXT2, ha="left")

# 가운데: 해리
arrow(ax, 4.0, 2.05, 5.0, 2.05, color="#9AA1AB", lw=1.8)
label(ax, 4.5, 2.6, "효소로 해리", fs=10.5, w="semibold", c=TEXT)
label(ax, 4.5, 1.6, "37 °C\n30–60분", fs=9.5, c=TEXT2, linespacing=1.4)

# 오른쪽: 시퀀서에 도착한 세포
box(ax, 5.2, 0.55, 5.1, 3.05, fc="white", ec=CRIMSON, lw=1.4, r=0.12)
label(ax, 5.4, 3.3, "시퀀서에 도착한 세포", fs=12, w="bold", ha="left")
for i in range(3):
    cx = 5.75 + i * 1.18
    ax.add_patch(mp.Circle((cx, 2.4), 0.48, fc="none", ec="#B8BDC5", lw=1.2, ls=(0, (3, 3)), zorder=3))
label(ax, 6.93, 1.78, "해리 중 부서져 사라짐", fs=9.5, c=TEXT2)
for i in range(6):
    cx, cy = 5.55 + i * 0.56, 1.25 + (0.1 if i % 2 else -0.05)
    ax.add_patch(mp.Circle((cx, cy), 0.17, fc=GREY, ec="none", zorder=3))
    ax.add_patch(mp.Circle((cx + 0.12, cy + 0.12), 0.065, fc=CRIMSON, ec="white", lw=0.8, zorder=4))
label(ax, 5.4, 0.8, "크고 약한 세포 0 · 작고 튼튼한 세포 6", fs=9.5, c=TEXT2, ha="left")

num(ax, 8.85, 2.85, 1, fc=WINE, r=0.12, fs=9)
label(ax, 9.05, 2.85, "구성이 바뀜", fs=10.5, w="bold", c=WINE, ha="left")
label(ax, 8.73, 2.5, "약한 세포는 적게 셈", fs=9.5, c=TEXT, ha="left")
num(ax, 8.85, 1.85, 2, fc=CRIMSON, r=0.12, fs=9)
label(ax, 9.05, 1.85, "살아남은 세포도", fs=10.5, w="bold", c=CRIMSON, ha="left")
label(ax, 8.73, 1.5, "스트레스 유전자를 켬", fs=9.5, c=TEXT, ha="left")
label(ax, 8.73, 1.18, "(FOS, JUN 등)", fs=9.5, c=TEXT2, ha="left")

label(ax, 0.1, 0.18, "측정한 구성 = 원래 구성이 아니라 살아남은 세포의 구성", fs=10.5, w="semibold", ha="left")
save(fig, "../../assets/img/w11/dissociation_bias.png")
