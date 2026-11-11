# W11 §7 케이스: 반응한 환자의 종양에는 TCF7을 켠 CD8 T세포가 더 많음 (Sade-Feldman 2018 요약)
# 위의 세포 수는 설명용(실제 비율 아님, 그림에 숫자를 쓰지 않음). 아래 숫자(세포 16,291개, 시료 48개)는 장 본문과 같음.
from medfig import *

fig, ax = new(8.2, 6.6)
ACT, EXH = ORANGE, "#A3A9B2"
rng = np.random.default_rng(7)

def tumour(x0, title, sub, n_act, n_exh):
    label(ax, x0 + 1.95, 6.4, title, fs=13, w="bold")
    label(ax, x0 + 1.95, 6.05, sub, fs=11, c=TEXT2)
    box(ax, x0, 3.55, 3.9, 2.2, fc=mix(CRIMSON, 0.08), ec=mix(CRIMSON, 0.3), lw=1.1, r=0.25)
    kinds = [ACT] * n_act + [EXH] * n_exh
    rng.shuffle(kinds)
    pos = []
    for r, n in enumerate([5, 4, 5, 2]):           # 줄마다 가운데 맞춤, 16개
        for j in range(n):
            pos.append((x0 + 1.95 + (j - (n - 1) / 2) * 0.72, 5.38 - r * 0.5))
    for (cx, cy), c in zip(pos, kinds):
        ax.add_patch(mp.Circle((cx, cy), 0.2, fc=c, ec="none", zorder=3))
        ax.add_patch(mp.Circle((cx - 0.04, cy + 0.03), 0.075, fc="white", ec="none", alpha=0.55, zorder=4))

tumour(0, "종양이 줄어든 환자", "면역관문억제제에 반응", 11, 5)
tumour(4.3, "종양이 진행한 환자", "반응 없음", 4, 12)

# 범례
ax.add_patch(mp.Circle((0.15, 3.1), 0.13, fc=ACT, ec="none"))
label(ax, 0.4, 3.1, "TCF7을 켠 CD8 T세포 — 덜 지침, 다시 늘어나 싸울 수 있음", fs=11, ha="left")
ax.add_patch(mp.Circle((0.15, 2.7), 0.13, fc=EXH, ec="none"))
label(ax, 0.4, 2.7, "TCF7이 꺼진 CD8 T세포 — 오래 싸워 지친 탈진 상태", fs=11, ha="left")

ax.plot([0, 8.2], [2.3, 2.3], color=LINE, lw=1)

# 아래: 근거의 크기
label(ax, 0, 1.95, "근거의 크기를 정하는 것", fs=13, w="bold", ha="left")
rows = [("면역세포 16,291개", "세포 수 ≠ 근거의 크기", "#A3A9B2"),
        ("종양 시료 48개", "근거는 시료(환자) 수", CRIMSON),
        ("독립 집단에서 재확인", "TCF7 염색으로 결과 예측", BLUE)]
cw, gap = 2.5, 0.35
for i, (main, sub, c) in enumerate(rows):
    x = i * (cw + gap)
    box(ax, x, 0.25, cw, 1.15, fc=FAINT, ec="none", r=0.1)
    box(ax, x, 0.25, 0.1, 1.15, fc=c, ec="none", r=0.03)
    label(ax, x + 0.28, 1.0, main, fs=12, w="bold", ha="left")
    label(ax, x + 0.28, 0.6, sub, fs=11, c=TEXT2, ha="left")
    if i < 2:
        arrow(ax, x + cw + 0.06, 0.825, x + cw + gap - 0.06, 0.825, color="#9AA1AB", lw=1.4, ms=10)
save(fig, "../../assets/img/w11/tcf7_case.png")
