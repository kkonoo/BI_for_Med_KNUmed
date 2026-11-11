# W11 §1.1 평균의 함정: bulk 결과 하나(유전자 X 2배) 뒤에 숨을 수 있는 세 가지 생물학
# (BI_for_Biomed W5 bulk_vs_singlecell을 한글로 다시 그림)
# 숫자는 세 경우 모두 평균이 1.0 → 2.0이 되도록 맞춤:
#   ① 모든 세포 1 → 2   ② 10개 중 2개만 1 → 6   ③ 발현이 높은 H형(3)과 낮은 세포(0.5), H형 20% → 60%
from medfig import *

fig, ax = new(8.2, 5.7)
shade = lambda v: mix(CRIMSON, min(0.12 + 0.15 * v, 1.0))   # 발현량 → 색 진하기

# 맨 위: 세 경우 모두 같은 bulk 결과
box(ax, 0, 5.1, 8.2, 0.56, fc=FAINT, ec="none", r=0.1)
label(ax, 0.2, 5.38, "Bulk 결과", fs=12, w="bold", ha="left")
label(ax, 1.35, 5.38, "질환에서 유전자 X가 2배 증가", fs=12, ha="left")
label(ax, 8.0, 5.38, "세 경우 모두 이 결과", fs=11, c=TEXT2, ha="right")

cases = [
    ("모든 세포가 조금씩 변함", [1] * 10, [2] * 10, None, "모든 세포 1 → 2"),
    ("드문 세포만 크게 변함", [1] * 10, [1] * 8 + [6, 6], None, "10개 중 2개만 1 → 6"),
    ("세포 구성만 바뀜", [3, 3] + [0.5] * 8, [3] * 6 + [0.5] * 4, (2, 6), "변한 세포 없음\nH형 20% → 60%"),
]
for k, (name, ctl, dis, hcount, note) in enumerate(cases):
    T = 4.5 - k * 1.38
    num(ax, 0.17, T, k + 1, fc=CAT[k], r=0.15, fs=11)
    label(ax, 0.42, T, name, fs=12.5, w="bold", c=CAT[k], ha="left")
    if "\n" in note:
        label(ax, 0.42, T - 0.32, note, fs=11, w="semibold", ha="left", va="top", linespacing=1.35)
    else:
        label(ax, 0.42, T - 0.5, note, fs=11, w="semibold", ha="left")
    for r, (grp, vals) in enumerate([("대조군", ctl), ("질환", dis)]):
        y = T - r * 0.5
        label(ax, 3.35, y, grp, fs=11, c=TEXT2, ha="left")
        for i, v in enumerate(vals):
            cx = 4.15 + i * 0.29
            if hcount and i < hcount[r]:      # H형 세포 = 네모
                box(ax, cx - 0.11, y - 0.11, 0.22, 0.22, fc=shade(v), ec="none", r=0.03)
            else:
                ax.add_patch(mp.Circle((cx, y), 0.11, fc=shade(v), ec="none", zorder=3))
        label(ax, 7.2, y, "평균 " + ("1.0" if r == 0 else "2.0"), fs=11,
              w="regular" if r == 0 else "bold", ha="left")
    if k < 2:
        ax.plot([0, 8.2], [T - 0.92, T - 0.92], color=LINE, lw=1)

# 범례
y = 0.5
label(ax, 0, y, "색 = 유전자 X 발현량", fs=11, c=TEXT2, ha="left")
label(ax, 1.95, y, "낮음", fs=11, c=TEXT2, ha="left")
for i, v in enumerate([0.5, 1, 2, 3, 4, 6]):
    ax.add_patch(mp.Circle((2.55 + i * 0.27, y), 0.1, fc=shade(v), ec="none", zorder=3))
label(ax, 4.1, y, "높음", fs=11, c=TEXT2, ha="left")
box(ax, 5.0, y - 0.1, 0.2, 0.2, fc=shade(3), ec="none", r=0.03)
label(ax, 5.3, y, "= X를 많이 켜는 H형 세포", fs=11, c=TEXT2, ha="left")
save(fig, "../../assets/img/w11/bulk_vs_singlecell.png")
