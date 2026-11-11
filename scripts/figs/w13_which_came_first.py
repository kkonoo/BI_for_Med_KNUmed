# W13 §5.1 원인인가 결과인가: 진단 때 한 번 채취하면 두 이야기가 같은 결과를 냄. 발병 전 채취만이 둘을 가름 (가상의 예)
# BI_for_Biomed W7 longitudinal(n17)을 단순하게 다시 그림
from medfig import *

t = np.linspace(-24, 12, 300)
sig = lambda x, c: 1 / (1 + np.exp(-(x - c) / 1.8))
before = 1 - 0.75 * sig(t, -9)       # 세균이 발병 전에 줄어듦 → 원인일 수 있음
after = 1 - 0.75 * sig(t, 2)         # 발병 뒤에 줄어듦 → 결과 (역인과)
t_snap, t_pre = 8, -5                # 진단 때 채취, 발병 전 채취

fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.9), gridspec_kw={"wspace": 0.12})
for ax, y, col, tag, sub in ((axes[0], before, CRIMSON, "① 세균이 먼저 줄어듦", "→ 원인일 수 있음"),
                             (axes[1], after, ORANGE, "② 병이 먼저 생김", "→ 병의 결과 (역인과)")):
    ax.axvspan(0, 12, color=FAINT, lw=0, zorder=0)
    ax.text(6, 1.13, "발병 뒤", ha="center", fontsize=9.5, color=TEXT2)
    ax.axvline(0, color=TEXT, lw=1)
    ax.plot(t, y, color=col, lw=3, solid_capstyle="round")
    # snapshot at diagnosis: same low value in both stories
    ys = np.interp(t_snap, t, y)
    ax.plot([t_snap, t_snap], [0, 1.08], color=TEXT2, lw=1, ls=(0, (3, 2)))
    ax.scatter([t_snap], [ys], s=70, color=col, zorder=4, ec="white", lw=1.5)
    ax.text(t_snap - 0.5, 0.05, "진단 때\n한 번 채취", ha="right", va="bottom", fontsize=9.5, color=TEXT2, linespacing=1.3)
    # sample before onset: tells the stories apart
    yp = np.interp(t_pre, t, y)
    ax.scatter([t_pre], [yp], s=90, color=BLUE, zorder=5, ec="white", lw=1.5)
    if yp < 0.6:      # low point (①): label down-left, below the curve
        ax.text(t_pre - 0.8, yp - 0.06, "발병 전 채취", ha="right", va="top", fontsize=9.8, color=BLUE, fontweight="bold")
    else:             # high point (②): label underneath
        ax.text(t_pre, yp - 0.1, "발병 전 채취", ha="center", va="top", fontsize=9.8, color=BLUE, fontweight="bold")
    ax.set_xlim(-24, 12); ax.set_ylim(0, 1.25)
    ax.set_xticks([-24, -12, 0, 12]); ax.set_xticklabels(["-24", "-12", "발병", "+12"])
    ax.set_xlabel("개월", fontsize=10, color=TEXT2)
    ax.set_yticks([])
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(LINE)
    ax.text(0, 1.1, tag, transform=ax.transAxes, fontsize=11.5, fontweight="bold", color=col, va="bottom")
    ax.text(0, 1.02, sub, transform=ax.transAxes, fontsize=10, color=TEXT, va="bottom")
axes[0].set_ylabel("어떤 세균의 양", fontsize=10, color=TEXT2)
save(fig, "../../assets/img/w13/which_came_first.png")
