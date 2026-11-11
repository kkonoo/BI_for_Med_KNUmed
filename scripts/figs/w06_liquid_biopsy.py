# W6 §5 액체생검: 혈액 속 cfDNA, ctDNA가 적을 때, 클론성 조혈 (조각 수는 예시)
from medfig import *

rng = np.random.default_rng(11)
NORM, CT, CHIP = "#C3C8D0", ORANGE, WINE
fig, ax = new(7.8, 5.7)


def tube(x, y, w, h, n_norm, n_ct=0, n_chip=0):
    box(ax, x, y, w, h, fc=FAINT, ec=LINE, lw=1.2, r=0.15)
    kinds = [NORM] * n_norm + [CT] * n_ct + [CHIP] * n_chip
    rng.shuffle(kinds)
    # fragments on a jittered grid (never touching), a random subset of the slots
    cols = np.arange(x + 0.24, x + w - 0.2, 0.36)
    rows = np.arange(y + 0.2, y + h - 0.12, 0.18)
    slots = [(cx + rng.uniform(-0.03, 0.03), cy) for cy in rows for cx in cols]
    pick = rng.choice(len(slots), len(kinds), replace=False)
    for i, c in zip(pick, kinds):
        px, py = slots[i]
        box(ax, px - 0.12, py - 0.035, 0.24, 0.07, fc=c, ec="none", r=0.035, z=3)


TY, TH = 2.75, 2.25
# ① cfDNA
label(ax, 0.1, 5.45, "① 혈액 속 DNA 조각", fs=12.5, w="bold", c=TEXT, ha="left")
tube(0.15, TY, 1.8, TH, 32, n_ct=4)
label(ax, 1.05, 2.48, "대부분 혈액세포에서", fs=11, c=TEXT)
label(ax, 1.05, 2.2, "일부만 종양에서 (ctDNA)", fs=11, c=CT, w="semibold")

# ② little ctDNA
label(ax, 2.5, 5.45, "② ctDNA가 적으면", fs=12.5, w="bold", c=TEXT, ha="left")
for x, n_ct, t, s in [(2.55, 5, "진행암", "찾음"), (3.75, 0, "초기암 등", "못 찾을 수 있음")]:
    tube(x, TY, 1.0, TH, 13, n_ct=n_ct)
    label(ax, x + 0.5, 2.48, t, fs=11, w="semibold", c=TEXT)
    label(ax, x + 0.5, 2.2, s, fs=11, c=TEXT2)
label(ax, 3.65, 1.82, "음성 ≠ 없음", fs=12, w="bold", c=BLUE)
label(ax, 3.65, 1.55, "→ 조직 검사로 확인", fs=11.5, w="bold", c=BLUE)

# ③ CHIP
label(ax, 5.3, 5.45, "③ 클론성 조혈", fs=12.5, w="bold", c=TEXT, ha="left")
tube(5.4, TY, 1.8, TH, 26, n_ct=2, n_chip=6)
label(ax, 6.3, 2.48, "혈액세포 자신의 변이", fs=11, c=CHIP, w="semibold")
label(ax, 6.3, 2.2, "→ 혈액세포도 읽어서 뺌", fs=11, c=TEXT)

# legend (left: two items, right: one)
for (x, y, c, t) in [(0.15, 0.85, NORM, "정상 혈액세포에서 온 조각"), (0.15, 0.55, CT, "종양에서 온 조각 (ctDNA)"),
                     (0.15, 0.25, CHIP, "변이를 가진 혈액세포에서 온 조각")]:
    box(ax, x, y - 0.035, 0.24, 0.07, fc=c, ec="none", r=0.035, z=3)
    label(ax, x + 0.33, y, t, fs=11, c=TEXT2, ha="left")
save(fig, "../../assets/img/w06/liquid_biopsy.png")
