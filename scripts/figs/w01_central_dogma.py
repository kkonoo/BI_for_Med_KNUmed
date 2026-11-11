# W1 §2.1–2.2 중심 원리와 오믹스 층: DNA → RNA → 단백질, 층마다 재는 것과 이 수업의 주차
# (BI_for_Biomed W1 central_dogma.png를 한글로 다시 그림)
from medfig import *

fig, ax = new(8.4, 5.0)
CW = 2.6                        # column width
xs = [1.3, 4.2, 7.1]            # column centres
cols = CAT[:3]                  # DNA crimson · RNA orange · protein wine
gy = 4.55                       # glyph row

# ── glyphs ─────────────────────────────────────────────────────────────────
t = np.linspace(0, 1, 300)
w = 1.6
# DNA: two strands with base-pair rungs
x0 = xs[0] - w / 2
for k in range(11):
    tt = (k + 0.5) / 11
    ya = gy + 0.22 * np.sin(2 * np.pi * 2 * tt)
    yb = gy + 0.22 * np.sin(2 * np.pi * 2 * tt + np.pi)
    ax.plot([x0 + w * tt] * 2, [ya, yb], color=mix(cols[0], 0.45), lw=2.2, zorder=2,
            solid_capstyle="round")
for ph in (0, np.pi):
    ax.plot(x0 + w * t, gy + 0.22 * np.sin(2 * np.pi * 2 * t + ph), color=cols[0], lw=2.6, zorder=3)
# RNA: one strand with bases sticking out on one side
x0 = xs[1] - w / 2
ax.plot(x0 + w * t, gy + 0.15 * np.sin(2 * np.pi * 2 * t), color=cols[1], lw=2.6, zorder=3)
for k in range(11):
    tt = (k + 0.5) / 11
    y = gy + 0.15 * np.sin(2 * np.pi * 2 * tt)
    ax.plot([x0 + w * tt] * 2, [y, y - 0.19], color=mix(cols[1], 0.45), lw=2.2, zorder=2,
            solid_capstyle="round")
# protein: a folded chain of amino-acid beads
s = np.linspace(0.35, 2 * np.pi - 0.35, 15)
px = xs[2] + 0.55 * np.sin(s)
py = gy + 0.27 * np.sin(2 * s)
ax.plot(px, py, color=mix(cols[2], 0.4), lw=1.8, zorder=2)
shades = [cols[2], mix(cols[2], 0.7), mix(cols[2], 0.45)]
for i, (a, b) in enumerate(zip(px, py)):
    ax.add_patch(mp.Circle((a, b), 0.07, fc=shades[i % 3], ec="white", lw=0.8, zorder=3))

# ── arrows between molecules ──────────────────────────────────────────────
for i, verb in enumerate(["전사", "번역"]):
    a, b = xs[i] + 0.92, xs[i + 1] - 0.92
    arrow(ax, a, gy, b, gy, color=mix(CRIMSON, 0.45), lw=2, ms=10)
    label(ax, (a + b) / 2, gy + 0.28, verb, fs=11, w="semibold", c=TEXT2)

# ── names, metaphors and the omics layer of each ──────────────────────────
mols = [("DNA", "설계도"), ("RNA", "설계도를 옮겨 적은 전달자"), ("단백질", "실제로 일하는 기계")]
layers = [("유전체", "genome", ["DNA 염기서열과", "그 차이(변이)"], "W2–W7"),
          ("전사체", "transcriptome", ["어떤 유전자의 RNA가", "얼마나 있나"], "W9–W10"),
          ("단백체", "proteome", ["어떤 단백질이", "얼마나 있나"], "W9")]
for x, c, (m, meta), (ko, en, what, wk) in zip(xs, cols, mols, layers):
    label(ax, x, 3.85, m, fs=17, w="bold", c=c)
    label(ax, x, 3.48, meta, fs=11, c=TEXT2)
    bx = x - CW / 2
    box(ax, bx, 1.4, CW, 1.72, fc=mix(c, 0.1), ec="none", r=0.1)
    t1 = label(ax, bx + 0.18, 2.84, ko, fs=13, w="bold", c=c, ha="left")
    fig.canvas.draw()
    kw = t1.get_window_extent().width / fig.dpi
    label(ax, bx + 0.18 + kw + 0.1, 2.83, en, fs=11, c=TEXT2, ha="left")
    for k, line in enumerate(what):
        label(ax, bx + 0.18, 2.4 - k * 0.3, line, fs=11, c=TEXT, ha="left")
    label(ax, bx + CW - 0.16, 1.6, "이 수업 " + wk, fs=11, w="semibold", c=c, ha="right")

# ── the other layers in the chapter's table, as small tags (2 × 2) ────────
others = ["+ 후성유전체: 유전자를 켜고 끄는 표지 (W6)",
          "+ 단일세포 전사체: 세포 하나하나의 RNA (W11–W12)",
          "+ 대사체: 당·지질 같은 작은 분자 (다루지 않음)",
          "+ 마이크로바이옴: 몸에 사는 미생물의 유전체 (W13–W14)"]
for k, t_ in enumerate(others):
    label(ax, 0.0 + (k % 2) * 4.25, 0.95 - (k // 2) * 0.36, t_, fs=11, c=TEXT2, ha="left")
save(fig, "../../assets/img/w01/central_dogma.png")
