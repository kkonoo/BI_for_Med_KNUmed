# W1 §3.2 데이터의 여정: 시료 → FASTQ → BAM → VCF → 결과지, 단계마다 크기가 줄어듦
from medfig import *

fig, ax = new(10.6, 3.3)
stages = [  # name, sub, size text, log10 bytes (for the bar)
    ("혈액", "DNA를 뽑을 시료", "몇 mL", None),
    ("FASTQ", "읽은 조각", "수십–100 GB", 11.0),
    ("BAM", "위치를 찾은 조각", "수십–100 GB", 11.0),
    ("VCF", "레퍼런스와 다른 곳", "수백 MB", 8.5),
    ("결과지", "해석한 한 줄", "한 장", 4.3),
]
steps = ["시퀀싱", "정렬", "변이 호출", "해석"]
fills = [mix(CRIMSON, 0.12)] + ramp(4)
W, H, gap, x0, y0 = 1.62, 1.05, 0.52, 0.15, 1.95
for i, (name, sub, size, lb) in enumerate(stages):
    x = x0 + i * (W + gap)
    box(ax, x, y0, W, H, fc=fills[i], ec="none", r=0.1)
    tc = TEXT if i == 0 else "white"
    label(ax, x + W / 2, y0 + 0.66, name, fs=16, w="bold", c=CRIMSON if i == 0 else tc)
    label(ax, x + W / 2, y0 + 0.32, sub, fs=10, c=TEXT2 if i == 0 else tc)
    if i < len(steps):
        xa = x + W + 0.06
        arrow(ax, xa, y0 + H / 2, xa + gap - 0.12, y0 + H / 2, color=mix(CRIMSON, 0.45), lw=2)
        label(ax, xa + (gap - 0.12) / 2, y0 + H + 0.2, steps[i], fs=9.5, w="semibold", c=CRIMSON)
    # size: a bar whose length follows log10(bytes)
    if lb:
        bw = W * lb / 11.0
        box(ax, x, 1.12, bw, 0.18, fc=mix(fills[i], 0.6), ec="none", r=0.09)
    label(ax, x, 1.58, size, fs=11.5, w="bold", c=TEXT, ha="left")

label(ax, x0, 1.21, "막대 길이 = 파일 크기 (자릿수)", fs=9, c=TEXT2, ha="left")
x1, x2 = x0 + 1 * (W + gap), x0 + 4 * (W + gap) + W
arrow(ax, x1, 0.72, x2, 0.72, color="#9AA1AB", lw=1.4, ms=10)
label(ax, (x1 + x2) / 2, 0.48, "단계마다 필요한 것만 남기고 요약 — 100 GB가 결과지 한 장이 됨",
      fs=10, w="semibold", c=TEXT)
save(fig, "../../assets/img/w01/data_journey.png")
