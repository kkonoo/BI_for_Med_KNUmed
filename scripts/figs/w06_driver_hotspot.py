# W6 §2.2 driver를 알아보는 법: 변이가 단백질 어디에 모이나 (막대 높이 = 그 자리에 변이가 있는 종양 수, 예시)
from medfig import *

rng = np.random.default_rng(6)
MIS, TRUNC = CRIMSON, ORANGE                   # missense vs truncating
TRACK = "#E4E6EA"
fig, ax = new(7.8, 6.7)
X0 = 0.2                                         # where every protein starts


def track(y, L, broken=False):
    box(ax, X0, y - 0.07, L, 0.14, fc=TRACK, ec="none", r=0.07, z=2)
    if broken:                                   # "very long" break mark
        xb = X0 + L * 0.5
        ax.add_patch(mp.Rectangle((xb - 0.09, y - 0.12), 0.18, 0.24, fc="white", ec="none", zorder=3))
        for dx in (-0.09, 0.09):
            ax.plot([xb + dx - 0.04, xb + dx + 0.04], [y - 0.13, y + 0.13], color="#9AA1AB", lw=1.3, zorder=4)


def pop(x, y, h, kind):
    ax.plot([x, x], [y + 0.07, y + 0.07 + h], color="#B9BEC6", lw=1.1, zorder=3)
    if kind == "mis":
        ax.add_patch(mp.Circle((x, y + 0.07 + h), 0.07, fc=MIS, ec="white", lw=0.8, zorder=5))
    else:
        ax.add_patch(mp.Rectangle((x - 0.065, y + 0.07 + h - 0.065), 0.13, 0.13, fc=TRUNC, ec="white", lw=0.8, zorder=5))


def spaced(n, lo, hi, gap, avoid=()):
    """n x positions in [lo, hi] at least `gap` apart (and away from `avoid`)."""
    out = []
    while len(out) < n:
        x = rng.uniform(lo, hi)
        if all(abs(x - o) >= gap for o in list(out) + list(avoid)):
            out.append(x)
    return sorted(out)


def head(y, tag, gene, note, col):
    """Row heading above the track: tag, example gene, what to notice."""
    t = label(ax, X0, y, tag, fs=13, w="bold", c=col, ha="left")
    ax.figure.canvas.draw()
    x = X0 + t.get_window_extent().width / ax.figure.dpi + 0.12
    label(ax, x, y, gene, fs=11.5, c=TEXT2, ha="left")
    label(ax, X0, y - 0.32, note, fs=11.5, c=TEXT, ha="left")


# ① oncogene: one hotspot (KRAS G12)
y = 4.65; L = 3.4
head(6.45, "① 종양유전자", "예: KRAS", "같은 자리가 반복해서 바뀜 = hotspot (켜진 채로 고정)", WINE)
track(y, L)
pop(X0 + L * 12 / 189, y, 1.05, "mis")
label(ax, X0 + L * 12 / 189 + 0.14, y + 1.12, "G12", fs=12, w="bold", c=MIS, ha="left")
for p in [40, 75, 117, 146, 160]:
    pop(X0 + L * p / 189, y, 0.12 + 0.06 * rng.random(), "mis")

# ② tumour suppressor: loss-of-function scattered
y = 2.75; L = 6.0
head(3.9, "② 종양억제유전자", "예: STK11", "일찍 끝나는 변이가 곳곳에 흩어짐 = 기능 상실 (브레이크 고장)", CRIMSON)
track(y, L)
for x in spaced(15, X0 + 0.1, X0 + L - 0.1, 0.24):
    pop(x, y, 0.14 + 0.32 * rng.random(), "trunc" if rng.random() < 0.65 else "mis")

# ③ long gene: many passengers
y = 0.75; L = 7.4
head(1.85, "③ 아주 긴 유전자", "예: TTN", "길이 때문에 변이가 쌓임 → 대부분 passenger", ORANGE)
track(y, L, broken=True)
for x in spaced(24, X0 + 0.1, X0 + L - 0.1, 0.2, avoid=[X0 + L * 0.5]):
    pop(x, y, 0.1 + 0.16 * rng.random(), "mis" if rng.random() < 0.85 else "trunc")

# legend (bottom)
for i, (kind, name) in enumerate([("mis", "아미노산 하나가 바뀜 (missense)"), ("trunc", "일찍 끝남 (종결 코돈 · frameshift)")]):
    xx = X0 + 0.07 + i * 3.75
    pop(xx, 0.08 - 0.07, 0.0, kind)
    label(ax, xx + 0.17, 0.08, name, fs=11, c=TEXT2, ha="left")
label(ax, X0, -0.25, "막대 높이 = 그 자리에 변이가 있는 종양 수 (예시)", fs=11, c=TEXT2, ha="left")
save(fig, "../../assets/img/w06/driver_hotspot.png")
