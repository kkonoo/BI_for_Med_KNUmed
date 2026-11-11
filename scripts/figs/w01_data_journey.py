# W1 §3.2 데이터의 여정: 시료 → FASTQ → BAM → VCF → 결과지, 단계마다 크기가 줄어듦
from medfig import *

fig, ax = new(8.45, 3.4)
stages = [  # name, sub (one or two lines), size text, log10 bytes (for the bar)
    ("혈액", ["DNA를 뽑을", "시료"], "몇 mL", None),
    ("FASTQ", ["읽은 조각"], "수십–100 GB", 11.0),
    ("BAM", ["위치를 찾은", "조각"], "수십–100 GB", 11.0),
    ("VCF", ["레퍼런스와", "다른 곳"], "수백 MB", 8.5),
    ("결과지", ["해석한 한 줄"], "한 장", 4.3),
]
steps = ["시퀀싱", "정렬", "변이 호출", "해석"]
fills = [mix(CRIMSON, 0.12)] + ramp(4)
W, H, gap, x0, y0 = 1.4, 1.2, 0.34, 0.05, 1.75
for i, (name, sub, size, lb) in enumerate(stages):
    x = x0 + i * (W + gap)
    box(ax, x, y0, W, H, fc=fills[i], ec="none", r=0.1)
    tc = TEXT if i == 0 else "white"
    label(ax, x + W / 2, y0 + 0.86, name, fs=15, w="bold", c=CRIMSON if i == 0 else tc)
    for k, s in enumerate(sub):
        yy = y0 + 0.44 - k * 0.25 + (0.12 if len(sub) == 1 else 0)
        label(ax, x + W / 2, yy, s, fs=11, c=TEXT2 if i == 0 else tc)
    if i < len(steps):
        xa = x + W + 0.04
        arrow(ax, xa, y0 + H / 2, xa + gap - 0.08, y0 + H / 2, color=mix(CRIMSON, 0.45), lw=2)
        label(ax, xa + (gap - 0.08) / 2, y0 + H + 0.2, steps[i], fs=11, w="semibold", c=CRIMSON)
    # size: a bar whose length follows log10(bytes)
    label(ax, x, 1.4, size, fs=12, w="bold", c=TEXT, ha="left")
    if lb:
        bw = W * lb / 11.0
        box(ax, x, 0.98, bw, 0.18, fc=mix(fills[i], 0.6), ec="none", r=0.09)

label(ax, x0, 1.07, "막대 = 파일 크기", fs=11, c=TEXT2, ha="left")
label(ax, x0, 0.83, "(자릿수)", fs=11, c=TEXT2, ha="left")
x1, x2 = x0 + 1 * (W + gap), x0 + 4 * (W + gap) + W
arrow(ax, x1, 0.55, x2, 0.55, color="#9AA1AB", lw=1.4, ms=10)
label(ax, (x1 + x2) / 2, 0.28, "단계마다 필요한 것만 남김 → 100 GB가 결과지 한 장이 됨",
      fs=12, w="semibold", c=TEXT)
save(fig, "../../assets/img/w01/data_journey.png")
