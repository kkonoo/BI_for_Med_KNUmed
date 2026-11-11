# W11 §7 케이스: 반응한 환자의 종양에는 TCF7을 켠 CD8 T세포가 더 많음 (Sade-Feldman 2018 요약)
# 왼쪽 세포 수는 설명용(실제 비율 아님, 그림에 숫자를 쓰지 않음). 오른쪽 숫자(세포 16,291개, 시료 48개)는 장 본문과 같음.
from medfig import *

fig, ax = new(10.6, 4.9)
ACT, EXH = ORANGE, "#A3A9B2"
rng = np.random.default_rng(7)

def tumour(x0, title, sub, n_act, n_exh):
    box(ax, x0, 1.35, 2.75, 2.65, fc=mix(CRIMSON, 0.08), ec=mix(CRIMSON, 0.3), lw=1.1, r=0.25)
    label(ax, x0 + 1.375, 4.6, title, fs=11.5, w="bold")
    label(ax, x0 + 1.375, 4.28, sub, fs=9.5, c=TEXT2)
    kinds = [ACT] * n_act + [EXH] * n_exh
    rng.shuffle(kinds)
    for k, c in enumerate(kinds):
        cx = x0 + 0.4 + (k % 4) * 0.6 + (0.2 if (k // 4) % 2 else 0)
        cy = 3.6 - (k // 4) * 0.6
        ax.add_patch(mp.Circle((cx, cy), 0.21, fc=c, ec="none", zorder=3))
        ax.add_patch(mp.Circle((cx - 0.04, cy + 0.03), 0.08, fc="white", ec="none", alpha=0.55, zorder=4))

tumour(0.1, "종양이 줄어든 환자", "면역관문억제제에 반응", 11, 5)
tumour(3.15, "종양이 진행한 환자", "반응 없음", 4, 12)

# 범례
ax.add_patch(mp.Circle((0.3, 0.85), 0.12, fc=ACT, ec="none"))
label(ax, 0.5, 0.85, "TCF7을 켠 CD8 T세포 — 덜 지침, 다시 늘어나 싸울 수 있음", fs=9.5, ha="left")
ax.add_patch(mp.Circle((0.3, 0.45), 0.12, fc=EXH, ec="none"))
label(ax, 0.5, 0.45, "TCF7이 꺼진 CD8 T세포 — 오래 싸워 지친 탈진 상태", fs=9.5, ha="left")

# 오른쪽: 근거의 크기
x0 = 6.45
label(ax, x0, 4.6, "근거의 크기를 정하는 것", fs=11.5, w="bold", ha="left")
rows = [("면역세포 16,291개", "세포 수 ≠ 근거의 크기", "#A3A9B2", TEXT2),
        ("종양 시료 48개", "근거는 시료(환자) 수", CRIMSON, TEXT),
        ("독립된 환자 집단에서 다시 확인", "TCF7 염색으로 치료 결과 예측", BLUE, TEXT)]
for i, (main, sub, c, tc) in enumerate(rows):
    y = 3.65 - i * 0.95
    box(ax, x0, y - 0.36, 0.1, 0.72, fc=c, ec="none", r=0.03)
    t = label(ax, x0 + 0.28, y + 0.14, main, fs=11, w="bold", c=tc if i else TEXT2, ha="left")
    label(ax, x0 + 0.28, y - 0.18, sub, fs=9.5, c=TEXT2, ha="left")
    if i == 0:
        fig.canvas.draw()                              # 취소선 = 글자 폭만큼
        bb = t.get_window_extent().transformed(ax.transData.inverted())
        ax.plot([bb.x0 - 0.03, bb.x1 + 0.03], [y + 0.14, y + 0.14], color="#A3A9B2", lw=1.3, zorder=6)
    if i < 2:
        arrow(ax, x0 + 0.05, y - 0.45, x0 + 0.05, y - 0.55, color="#C4C9D0", lw=1.2, ms=8)
save(fig, "../../assets/img/w11/tcf7_case.png")
