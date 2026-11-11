# W4 §2.3 Hit ≠ 원인: GWAS 탑 하나 = 함께 물려 내려오는(LD) 변이 수십 개 + 가장 가까운 유전자 ≠ 원인 유전자
# (BI_for_Biomed W2 locus_ld를 단순하게 다시 그림, 설명용 가상 자료)
from medfig import *

plt.rcParams.update({"xtick.labelsize": 11, "ytick.labelsize": 11})
rng = np.random.default_rng(21)
lo, hi, lead, n = 0, 900, 330, 900
pos = np.sort(rng.uniform(lo, hi, n))
r2 = np.clip(np.exp(-((np.abs(pos - lead) / 55) ** 1.7)) * rng.uniform(0.75, 1.0, n), 0, 1)
logp = np.clip(r2 * 13.5 + rng.gamma(1.0, 0.85, n), 0.02, None)
i = np.argmin(np.abs(pos - lead)); logp[i] = logp.max() + 0.7; r2[i] = 1.0

fig, (ax, gx) = plt.subplots(2, 1, figsize=(8.4, 5.6), sharex=True,
                             gridspec_kw={"height_ratios": [3.0, 1.2], "hspace": 0.06})
bins = [(0.8, 1.01, CRIMSON, "0.8–1.0"), (0.6, 0.8, ORANGE, "0.6–0.8"), (0.4, 0.6, AMBER, "0.4–0.6"),
        (0.2, 0.4, mix(AMBER, 0.45), "0.2–0.4"), (-0.01, 0.2, "#C4C7CC", "0.2 미만")]
for a, b, c, _ in bins[::-1]:
    m = (r2 > a) & (r2 <= b) & (np.arange(n) != i)
    ax.scatter(pos[m], logp[m], s=26, color=c, lw=0.3, edgecolor="white", zorder=3)
ax.scatter([pos[i]], [logp[i]], s=160, marker="D", color=WINE, ec="white", lw=1.4, zorder=6)
ax.text(pos[i] + 22, logp[i] + 0.1, "가장 유의한 변이", fontsize=11.5, fontweight="bold", color=WINE, ha="left")
thr = -np.log10(5e-8)
ax.axhline(thr, color=TEXT2, lw=1.1, ls="--")
ax.text(hi - 5, thr + 0.3, "5×10⁻⁸", ha="right", fontsize=10.5, color=TEXT2)
ax.set_ylabel("−log₁₀(p)", fontsize=12); ax.set_ylim(0, 17.8); ax.set_xlim(lo, hi)
ax.spines["bottom"].set_visible(False); ax.tick_params(bottom=False)
# LD legend (top-left, clear of the peak)
ax.text(12, 16.7, "가장 유의한 변이와의 LD (r²)", fontsize=10.5, color=TEXT, fontweight="semibold")
for k, (_, _, c, lab) in enumerate(bins):
    ax.scatter([24], [15.3 - k * 1.25], s=46, color=c, ec="white", lw=0.3)
    ax.text(44, 15.3 - k * 1.25, lab, fontsize=10.5, va="center", color=TEXT)
ax.text(hi - 10, 17.0, "함께 물려 내려온 변이들이\n모두 유의하게 나옴\n→ 이 그림만으로는\n어느 것이 원인인지 모름",
        ha="right", va="top", fontsize=11.5, color=BLUE, fontweight="bold", linespacing=1.5)

# gene track
genes = [("유전자 A", 40, 170, 1), ("유전자 B", 280, 420, 1), ("유전자 C", 560, 650, -1)]
for nm, s, e, strand in genes:
    gx.add_patch(mp.FancyArrow(s if strand > 0 else e, 0.62, (e - s) * strand, 0, width=0.17,
                               head_width=0.38, head_length=18, length_includes_head=True,
                               fc=WINE if nm == "유전자 B" else mix(TEXT, 0.75), ec="none"))
    gx.text((s + e) / 2, 0.02, nm, ha="center", fontsize=11, color=TEXT,
            fontweight="bold" if nm == "유전자 B" else "regular")
gx.text(hi - 10, 0.95, "가장 가까운 유전자(B)가\n원인이라는 보장은 없음\n(예: 1p13 → SORT1)",
        ha="right", va="center", fontsize=10.5, color=TEXT2, linespacing=1.4)
gx.set_ylim(-0.3, 1.6); gx.set_yticks([])
for sp in ("left", "top", "right"):
    gx.spines[sp].set_visible(False)
gx.set_xlabel("염색체 위치 (kb, 설명용)", fontsize=12)
save(fig, "../../assets/img/w04/ld_hit.png")
