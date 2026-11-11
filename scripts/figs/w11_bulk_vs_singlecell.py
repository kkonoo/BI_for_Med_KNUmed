# W11 §1.1 평균의 함정: bulk 결과 하나(유전자 X 2배) 뒤에 숨을 수 있는 세 가지 생물학
# (BI_for_Biomed W5 bulk_vs_singlecell을 한글로 다시 그림)
# 숫자는 세 경우 모두 평균이 1.0 → 2.0이 되도록 맞춤:
#   ① 모든 세포 1 → 2   ② 10개 중 2개만 1 → 6   ③ 발현이 높은 H형(3)과 낮은 세포(0.5), H형 20% → 60%
from medfig import *

fig, ax = new(10.6, 4.3)
shade = lambda v: mix(CRIMSON, min(0.12 + 0.15 * v, 1.0))   # 발현량 → 색 진하기

# 맨 위: 세 경우 모두 같은 bulk 결과
box(ax, 0.1, 3.72, 10.4, 0.48, fc=FAINT, ec="none", r=0.1)
label(ax, 0.35, 3.96, "Bulk 결과", fs=11, w="bold", ha="left")
label(ax, 1.4, 3.96, "질환에서 유전자 X가 2배 증가", fs=11, ha="left")
label(ax, 10.3, 3.96, "아래 세 경우 모두 이 결과가 나옴", fs=9.5, c=TEXT2, ha="right")

cases = [
    ("모든 세포가 조금씩 변함", [1] * 10, [2] * 10, None, "모든 세포 1 → 2"),
    ("드문 세포만 크게 변함", [1] * 10, [1] * 8 + [6, 6], None, "10개 중 2개만 1 → 6"),
    ("세포 구성만 바뀜", [3, 3] + [0.5] * 8, [3] * 6 + [0.5] * 4, (2, 6), "변한 세포 없음, H형 20% → 60%"),
]
cw = 3.47
for k, (name, ctl, dis, hcount, note) in enumerate(cases):
    x0 = 0.15 + k * cw
    num(ax, x0 + 0.15, 3.3, k + 1, fc=CAT[k], r=0.13, fs=10)
    label(ax, x0 + 0.38, 3.3, name, fs=11.5, w="bold", c=CAT[k], ha="left")
    for r, (grp, vals) in enumerate([("대조군", ctl), ("질환", dis)]):
        y = 2.72 - r * 0.62
        label(ax, x0, y + 0.25, grp, fs=9, c=TEXT2, ha="left")
        for i, v in enumerate(vals):
            cx = x0 + 0.13 + i * 0.255
            if hcount and i < hcount[r]:      # H형 세포 = 네모
                box(ax, cx - 0.1, y - 0.1, 0.2, 0.2, fc=shade(v), ec="none", r=0.03)
            else:
                ax.add_patch(mp.Circle((cx, y), 0.1, fc=shade(v), ec="none", zorder=3))
        label(ax, x0 + 2.75, y, "평균 " + ("1.0" if r == 0 else "2.0"), fs=9.5,
              w="regular" if r == 0 else "bold", ha="left")
    ax.plot([x0, x0 + 3.25], [1.62, 1.62], color=LINE, lw=1)
    label(ax, x0, 1.36, note, fs=10.5, w="semibold", ha="left")

# 범례
label(ax, 0.15, 0.82, "색 = 그 세포의 유전자 X 발현량", fs=9.5, c=TEXT2, ha="left")
for i, v in enumerate([0.5, 1, 2, 3, 4, 6]):
    ax.add_patch(mp.Circle((2.75 + i * 0.27, 0.82), 0.09, fc=shade(v), ec="none", zorder=3))
label(ax, 2.52, 0.82, "낮음", fs=9, c=TEXT2, ha="right")
label(ax, 4.27, 0.82, "높음", fs=9, c=TEXT2, ha="left")
box(ax, 5.3, 0.73, 0.18, 0.18, fc=shade(3), ec="none", r=0.03)
label(ax, 5.58, 0.82, "= 유전자 X를 많이 켜는 H형 세포", fs=9.5, c=TEXT2, ha="left")
save(fig, "../../assets/img/w11/bulk_vs_singlecell.png")
