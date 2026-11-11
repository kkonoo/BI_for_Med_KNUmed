# W4 §3.3 상대위험 vs 절대위험: 10년 위험 4% → "평균의 1.5배" = 6% (장의 설명용 숫자)
from medfig import *

fig, ax = new(7.6, 5.7)
G = "#D5D8DD"
SP = 0.31


def person(x, y, c, s=0.27):
    ax.add_patch(mp.Circle((x, y + 0.42 * s), 0.17 * s, fc=c, ec="none", zorder=3))
    box(ax, x - 0.24 * s, y - 0.2 * s, 0.48 * s, 0.42 * s, fc=c, ec="none", r=0.14 * s, z=3)


def grid(x0, y0, n_base, n_extra):
    """100 people, filled row by row from the bottom-left."""
    for k in range(100):
        r, c = divmod(k, 10)
        col = CRIMSON if k < n_base else (BLUE if k < n_base + n_extra else G)
        person(x0 + c * SP, y0 + r * SP, col)


L, R, Y0 = 0.25, 4.6, 1.5
grid(L, Y0, 4, 0)
grid(R, Y0, 4, 2)
cx = lambda x0: x0 + 4.5 * SP
label(ax, cx(L), 5.25, "같은 나이·성별 평균", fs=13, w="bold")
label(ax, cx(L), 4.92, "10년 안에 100명 중 4명 (4%)", fs=11.5, c=TEXT2)
label(ax, cx(R), 5.25, "PRS 결과 \"평균의 1.5배\"", fs=13, w="bold")
label(ax, cx(R), 4.92, "10년 안에 100명 중 6명 (6%)", fs=11.5, c=TEXT2)
arrow(ax, L + 9 * SP + 0.35, 2.85, R - 0.35, 2.85, color="#9AA1AB", lw=1.6)

mid = (cx(L) + cx(R)) / 2
label(ax, mid, 1.0, "상대위험: 1.5배 → \"50% 증가\"", fs=12.5, w="semibold", c=CRIMSON)
label(ax, mid, 0.62, "절대위험 차이: 100명 중 2명 (2%p)", fs=12.5, w="bold", c=BLUE)
label(ax, mid, 0.22, "같은 결과도 어떻게 말하느냐에 따라 크게도, 작게도 들림", fs=11, c=TEXT2)
save(fig, "../../assets/img/w04/absolute_risk.png")
