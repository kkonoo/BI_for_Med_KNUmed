# W2 §1.1 크기별 변이의 종류와 그 크기를 보는 검사 (BI_for_Biomed W2 variant_tree를 크기 눈금으로 다시 그림)
from medfig import *

X0, K, SMAX = 2.3, 0.66, 8.5           # left edge, inches per 10×, largest size (log10 bp)
X = lambda s: X0 + s * K
fig, ax = new(X(SMAX) + 0.3, 5.0)

# variant classes (parallel items → CAT colours); note inside the bar when it fits
classes = [  # name, from, to (log10 bp), colour, note
    ("SNV", 0, 0.38, CAT[0], "염기 1개"),
    ("작은 삽입·결실", 0, 1.7, CAT[1], "보통 50염기 미만"),
    ("복제수 변이 (CNV)", 3.3, 6.6, CAT[2], "수천–수백만 염기"),
    ("구조 변이 (SV)", 3.6, SMAX, CAT[3], "역위·전좌 같은 큰 재배열"),
]
for k, (name, a, b, col, note) in enumerate(classes):
    y = 4.6 - k * 0.46
    label(ax, X0 - 0.2, y, name, fs=12.5, w="bold", c=col, ha="right")
    box(ax, X(a), y - 0.15, X(b) - X(a), 0.3, fc=col, ec="none", r=0.06)
    if X(b) - X(a) > 2:
        label(ax, (X(a) + X(b)) / 2, y, note, fs=11, w="semibold", c="white")
    else:
        label(ax, X(b) + 0.1, y, note, fs=11, c=TEXT2, ha="left")

# size axis
ya = 2.8
ax.plot([X(0), X(SMAX)], [ya, ya], color="#9AA1AB", lw=1.1, zorder=1)
ticks = ["1", "10", "100", "1천", "1만", "10만", "100만", "1000만", "1억"]
for i, t in enumerate(ticks):
    ax.plot([X(i), X(i)], [ya - 0.05, ya + 0.05], color="#9AA1AB", lw=1.1)
    label(ax, X(i), ya - 0.23, t, fs=11, c=TEXT2)
label(ax, X0 - 0.2, ya, "크기 (염기 수)", fs=11, w="semibold", c=TEXT2, ha="right")

# tests: what size each one can see
tests = [
    ("핵형 검사", 6.5, SMAX, "수백만 염기 이상"),
    ("마이크로어레이", 4.0, SMAX, "결실·중복 (균형 재배열은 못 봄)"),
    ("패널 · 엑솜", 0, 1.7, "SNV · 작은 삽입·결실 (엑손 안)"),
    ("전장 유전체", 0, SMAX, "SNV부터 구조 변이까지 한 번에"),
]
for k, (name, a, b, note) in enumerate(tests):
    y = 2.05 - k * 0.46
    label(ax, X0 - 0.2, y, name, fs=12, w="semibold", c=TEXT, ha="right")
    box(ax, X(a), y - 0.14, X(b) - X(a), 0.28, fc=mix(WINE, 0.14), ec="none", r=0.06)
    if X(b) - X(a) > 2.5:
        label(ax, (X(a) + X(b)) / 2, y, note, fs=11, c=WINE)
    elif X(a) > 5:
        label(ax, X(a) - 0.1, y, note, fs=11, c=WINE, ha="right")
    else:
        label(ax, X(b) + 0.1, y, note, fs=11, c=WINE, ha="left")
save(fig, "../../assets/img/w02/size_classes.png")
