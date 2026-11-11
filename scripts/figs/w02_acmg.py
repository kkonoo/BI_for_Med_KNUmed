# W2 §4.4 ACMG/AMP — 근거를 세기별로 모아 다섯 단계로 분류, 가운데가 VUS (새로 그림)
from medfig import *

fig, ax = new(8.2, 5.0)
X0, BW, GAP = 0.3, 1.42, 0.07
classes = [  # Korean (2 lines max), English, fill, text colour
    ("양성", "Benign", "#9AA1AB", "white"),
    ("양성 가능성\n높음", "Likely benign", "#D5D8DD", TEXT),
    ("의미 불명", "VUS", "white", BLUE),
    ("병적 가능성\n높음", "Likely pathogenic", mix(CRIMSON, 0.35), WINE),
    ("병적", "Pathogenic", CRIMSON, "white"),
]
YC = 3.95
for i, (ko, en, fc, tc) in enumerate(classes):
    x = X0 + i * (BW + GAP)
    if i == 2:
        box(ax, x, YC, BW, 0.92, fc=mix(BLUE, 0.08), ec=BLUE, lw=1.8, r=0.08)
    else:
        box(ax, x, YC, BW, 0.92, fc=fc, ec="none", r=0.08)
    label(ax, x + BW / 2, YC + 0.56, ko, fs=12.5, w="bold", c=tc, linespacing=1.15)
    label(ax, x + BW / 2, YC + 0.17, en, fs=11, w="bold" if i == 2 else "regular",
          c=tc if i in (0, 2, 4) else TEXT2)
xv = X0 + 2 * (BW + GAP) + BW / 2
label(ax, xv, YC - 0.27, "근거가 부족하거나 엇갈림 → 판단 보류", fs=11, w="semibold", c=BLUE)
label(ax, xv, YC - 0.55, "VUS로 진단하지 않음", fs=11, w="semibold", c=BLUE)

def chip(x, y, code, strength, fc, tc, w=0.92):
    box(ax, x, y - 0.29, w, 0.58, fc=fc, ec="none", r=0.08)
    label(ax, x + w / 2, y + 0.1, code, fs=12.5, w="bold", c=tc)
    label(ax, x + w / 2, y - 0.15, strength, fs=11, c=tc)

YE = 2.65
for k, (code, s, fc, tc) in enumerate([("BA1", "단독", "#6B7280", "white"), ("BS", "강함", "#9AA1AB", "white"),
                                         ("BP", "보조", "#D5D8DD", TEXT)]):
    chip(X0 + k * 1.0, YE, code, s, fc, tc)
arrow(ax, X0 + 2.92, YE - 0.48, X0, YE - 0.48, color="#9AA1AB", lw=1.5)
label(ax, X0, YE - 0.72, "양성 쪽 근거", fs=11, w="semibold", c=TEXT2, ha="left")

xe = X0 + 5 * (BW + GAP) - GAP
xs = xe - 3.92
for k, (code, s, fc, tc) in enumerate([("PP", "보조", mix(CRIMSON, 0.25), WINE), ("PM", "중간", mix(CRIMSON, 0.5), "white"),
                                         ("PS", "강함", CRIMSON, "white"), ("PVS1", "매우 강함", WINE, "white")]):
    chip(xs + k * 1.0, YE, code, s, fc, tc)
arrow(ax, xs, YE - 0.48, xe, YE - 0.48, color=mix(CRIMSON, 0.6), lw=1.5)
label(ax, xe, YE - 0.72, "병적 쪽 근거", fs=11, w="semibold", c=CRIMSON, ha="right")

# one combining rule, as in the chapter
YR = 1.2
xr = X0 + 1.65
label(ax, xr - 0.15, YR, "합치는 규칙의 예", fs=11, w="semibold", c=TEXT2, ha="right")
chip(xr, YR, "PVS1", "매우 강함 1개", WINE, "white", w=1.45)
label(ax, xr + 1.65, YR, "+", fs=17, w="bold", c=TEXT2)
chip(xr + 1.85, YR, "PS", "강함 1개 이상", CRIMSON, "white", w=1.45)
arrow(ax, xr + 3.45, YR, xr + 4.15, YR, color=TEXT2, lw=1.6)
box(ax, xr + 4.3, YR - 0.29, 1.4, 0.58, fc=CRIMSON, ec="none", r=0.08)
label(ax, xr + 5.0, YR + 0.1, "병적", fs=12.5, w="bold", c="white")
label(ax, xr + 5.0, YR - 0.15, "Pathogenic", fs=11, c="white")
save(fig, "../../assets/img/w02/acmg.png")
