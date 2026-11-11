# W6 §3.4 표적치료 내성: 약을 피하는 변이를 가진 세포가 살아남아 불어남 (세포 수는 예시)
from medfig import *

rng = np.random.default_rng(3)
SENS, RES = mix(CRIMSON, 0.8), ORANGE
fig, ax = new(8.0, 3.9)


def tumour(cx, cy, R, n_res, res_frac=None, r=0.075):
    """Cells packed in a disc of radius R; n_res resistant cells (or a fraction of all)."""
    pts = []
    step = 2 * r + 0.02
    for j, y in enumerate(np.arange(-R, R + 1e-9, step * 0.87)):
        for x in np.arange(-R + (step / 2 if j % 2 else 0), R + 1e-9, step):
            if x * x + y * y <= (R - r * 0.6) ** 2:
                pts.append((cx + x, cy + y))
    n = len(pts)
    k = n_res if res_frac is None else int(round(res_frac * n))
    res = set(rng.choice(n, k, replace=False))
    for i, (x, y) in enumerate(pts):
        ax.add_patch(mp.Circle((x, y), r, fc=RES if i in res else SENS, ec="white", lw=0.7, zorder=3))


cy = 2.1
tumour(0.85, cy, 0.75, 2)
tumour(3.1, cy, 0.3, 3)
tumour(5.35, cy, 0.75, 0, res_frac=0.85)

for x, t, s1, s2 in [(0.85, "치료 전", "내성 세포가 드물게", "있거나 새로 생김"),
                     (3.1, "1·2세대 EGFR 억제제", "듣는 세포가 죽어", "종양이 줄어듦"),
                     (5.35, "시간이 지나 재발", "내성 세포가 불어나", "다시 자람")]:
    label(ax, x, 3.2, t, fs=12.5, w="bold", c=TEXT)
    label(ax, x, 1.05, s1, fs=11, c=TEXT2)
    label(ax, x, 0.76, s2, fs=11, c=TEXT2)
arrow(ax, 1.75, cy, 2.6, cy)
arrow(ax, 3.6, cy, 4.45, cy)

# next step
arrow(ax, 6.17, cy, 6.4, cy)
box(ax, 6.45, 1.5, 1.4, 1.2, fc=mix(ORANGE, 0.12), ec="none", r=0.1)
label(ax, 7.15, 2.36, "3세대 약", fs=12, w="bold", c=ORANGE)
label(ax, 7.15, 2.08, "osimertinib", fs=11, c=TEXT)
label(ax, 7.15, 1.8, "T790M에도 들음", fs=11, c=TEXT2)

# legend
for i, (c, t) in enumerate([(SENS, "약에 듣는 세포"), (RES, "내성 변이(EGFR T790M)를 가진 세포")]):
    x = 0.15 + i * 2.1
    ax.add_patch(mp.Circle((x, 0.25), 0.08, fc=c, ec="none", zorder=3))
    label(ax, x + 0.15, 0.25, t, fs=11, c=TEXT2, ha="left")
save(fig, "../../assets/img/w06/resistance.png")
