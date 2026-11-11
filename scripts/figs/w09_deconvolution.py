# W9 §1.3 세포 비율이 바뀌면 bulk에서는 발현이 바뀐 것처럼 보임 (BI_for_Biomed W4 deconvolution을 다시 그림)
from medfig import *

ct = ["신경세포", "성상세포", "미세아교세포", "희소돌기아교세포"]
prof = np.array([[9.2, 1.1, 0.4, 1.9], [1.0, 8.6, 0.6, 2.2], [0.3, 0.8, 9.0, 0.5], [1.5, 2.0, 0.7, 8.8]])
p_ctrl = np.array([0.42, 0.26, 0.07, 0.25])
p_case = np.array([0.31, 0.28, 0.16, 0.25])
GREY, DARK = "#C9CED6", "#5E6670"

fig = plt.figure(figsize=(8.4, 8.3))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 0.95], width_ratios=[1.0, 0.95], hspace=0.45, wspace=0.55,
                      left=0.2, right=0.86, top=0.93, bottom=0.12)
a1, a2 = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])
a3 = fig.add_axes([0.07, 0.12, 0.79, 0.31])


def tag(ax, t, x=0.0):
    ax.text(x, 1.05, t, transform=ax.transAxes, ha="left", va="bottom", fontsize=12.5, fontweight="bold", color=TEXT)


def clean(ax):
    for s in ("left", "top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(LINE)
    ax.tick_params(length=0)


# ① 세포 유형마다 고유한 발현
ax = a1
cm = LinearSegmentedColormap.from_list("cr", ["#FFFFFF", mix(CRIMSON, 0.35), CRIMSON])
ax.imshow(prof, cmap=cm, aspect="auto", vmin=0, vmax=10)
ax.set_xticks(range(4)); ax.set_xticklabels(["1", "2", "3", "4"], fontsize=11, color=TEXT2)
ax.set_xlabel("유전자", fontsize=11, color=TEXT2)
ax.set_yticks(range(4)); ax.set_yticklabels(ct, fontsize=11.5, fontweight="semibold")
for t, col in zip(ax.get_yticklabels(), CAT):
    t.set_color(col)
ax.tick_params(length=0)
for s in ax.spines.values():
    s.set_visible(False)
for i in range(4):
    for j in range(4):
        ax.text(j, i, f"{prof[i, j]:.1f}", ha="center", va="center", fontsize=11,
                color="white" if prof[i, j] > 5 else TEXT)
tag(ax, "① 세포마다 켜는 유전자가 다름", x=-0.62)

# ② 병이 세포 구성을 바꿈
ax = a2
bl = np.zeros(2)
for i, (c, col) in enumerate(zip(ct, CAT)):
    v = np.array([p_ctrl[i], p_case[i]])
    ax.bar([0, 1], v, bottom=bl, color=col, width=0.62, edgecolor="white", lw=1.5)
    for x in (0, 1):
        ax.text(x, bl[x] + v[x] / 2, f"{v[x] * 100:.0f}%", ha="center", va="center", fontsize=11,
                color="white", fontweight="semibold")
    bl += v
ax.set_xticks([0, 1]); ax.set_xticklabels(["대조군", "환자군"], fontsize=11.5, color=TEXT)
ax.set_ylim(0, 1); ax.set_yticks([]); ax.set_xlim(-0.45, 1.45)
clean(ax)
tag(ax, "② 병이 세포 비율을 바꿈")
ax.text(0.5, -0.2, "색 = ①의 세포 유형", transform=ax.transAxes, ha="center", va="top", fontsize=11, color=TEXT2)

# ③ bulk 결과
ax = a3
b_ctrl = p_ctrl @ prof
b_case = p_case @ prof
X = np.arange(4); w = 0.36
GCOL = [CAT[0], TEXT2, CAT[2], TEXT2]   # 유전자 1 = 신경세포 표지, 유전자 3 = 미세아교세포 표지
ax.bar(X - w / 2, b_ctrl, w, color=GREY, edgecolor="white", label="대조군")
ax.bar(X + w / 2, b_case, w, color=DARK, edgecolor="white", label="환자군")
for i, (a, b) in enumerate(zip(b_ctrl, b_case)):
    fc = b / a
    big = abs(np.log2(fc)) > 0.25
    ax.text(i, max(a, b) + 0.2, f"{fc:.2f}배", ha="center", va="bottom", fontsize=12,
            fontweight="bold" if big else "normal", color=GCOL[i] if big else TEXT2)
ax.set_xticks(X)
ax.set_xticklabels(["유전자 1\n(신경세포)", "유전자 2", "유전자 3\n(미세아교세포)", "유전자 4"], fontsize=11)
for t, col in zip(ax.get_xticklabels(), GCOL):
    t.set_color(col)
top = max(b_ctrl.max(), b_case.max()) * 1.3
ax.set_ylim(0, top); ax.set_yticks([])
clean(ax)
ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.16), frameon=False, fontsize=11, handlelength=1.2, ncol=2)
tag(ax, "③ bulk RNA-seq 결과 (환자군 ÷ 대조군)", x=0.0)

fig.text(0.5, 0.03, "어느 세포도 발현을 바꾸지 않았음 — 바뀐 것은 세포 비율뿐", ha="center", va="center",
         fontsize=12.5, fontweight="bold", color=BLUE)
save(fig, "../../assets/img/w09/deconvolution.png")
