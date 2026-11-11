# W4 §3.3 좋은 PRS도 환자와 대조군이 거의 겹침 + 같은 자료를 10분위로 보면 (BI_for_Biomed W2 prs_distribution을 다시 그림)
from medfig import *
from statistics import NormalDist

plt.rcParams.update({"xtick.labelsize": 11.5, "ytick.labelsize": 11.5})
nd = NormalDist()
d = 0.62                                   # mean difference in SD
x = np.linspace(-4.2, 4.6, 600)
pdf = lambda m: np.exp(-(x - m) ** 2 / 2) / np.sqrt(2 * np.pi)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 4.4), gridspec_kw={"wspace": 0.32, "width_ratios": [1.1, 1]})
a1.fill_between(x, pdf(0), color=mix("#6B7280", 0.25), lw=0)
a1.plot(x, pdf(0), color="#6B7280", lw=1.5)
a1.fill_between(x, pdf(d), color=mix(CRIMSON, 0.45), lw=0, alpha=0.85)
a1.plot(x, pdf(d), color=CRIMSON, lw=1.5)
a1.set_yticks([]); a1.set_xlabel("PRS (표준화 점수)", fontsize=12)
a1.text(-2.7, 0.30, "대조군", color="#4B5563", fontsize=13, fontweight="bold", ha="center")
a1.text(2.6, 0.33, "환자군", color=CRIMSON, fontsize=13, fontweight="bold", ha="center")
a1.text(0.02, 0.97, "① 점수 분포", transform=a1.transAxes, fontsize=12, fontweight="bold", color=TEXT, va="top")
a1.annotate("대부분의 환자와\n대조군은 점수만으로\n구별되지 않음", xy=(0.9, 0.2), xytext=(2.15, 0.2),
            fontsize=11, fontweight="bold", color=BLUE, ha="left", va="center", linespacing=1.4,
            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.4, connectionstyle="arc3,rad=0.25"))
a1.text(0.98, 0.97, "설명용 가상 자료", transform=a1.transAxes, ha="right", va="top",
        fontsize=10.5, color=TEXT2, bbox=dict(boxstyle="round,pad=0.4", fc=FAINT, ec=LINE))
a1.set_ylim(0, 0.47)

dec = np.arange(1, 11)
z = np.array([nd.inv_cdf((k - 0.5) / 10) for k in dec])
orr = np.exp(d * z); orr = orr / orr[4]
cols = [mix(CRIMSON, 0.25 + 0.06 * i) for i in range(9)] + [ORANGE]
a2.bar(dec, orr, color=cols, width=0.72)
a2.axhline(1, color="#9AA1AB", lw=1.1, ls="--")
a2.set_xticks(dec); a2.set_xlabel("PRS 10분위 (1 = 가장 낮음)", fontsize=12)
a2.set_ylabel("오즈비 (가운데 5분위 대비)", fontsize=12)
a2.text(10, orr[-1] + 0.07, f"{orr[-1]:.1f}배", ha="center", fontsize=12, fontweight="bold", color=ORANGE)
a2.text(1, orr[0] + 0.07, f"{orr[0]:.1f}배", ha="center", fontsize=12, fontweight="bold", color=CRIMSON)
a2.annotate("", xy=(1, orr[0] + 0.28), xytext=(10, orr[-1] + 0.35),
            arrowprops=dict(arrowstyle="<|-|>", color="#6B7280", lw=1.2, connectionstyle="arc3,rad=0.18"))
a2.text(5.3, orr[-1] * 1.2, f"최상위 vs 최하위 {orr[-1] / orr[0]:.1f}배", ha="center", fontsize=11.5, color=TEXT)
a2.text(0.02, 0.97, "② 같은 자료를 10분위로", transform=a2.transAxes, fontsize=12, fontweight="bold", color=TEXT, va="top")
a2.text(0.5, 0.86, "⚠ 같은 자료인데 훨씬 인상적으로 보임", transform=a2.transAxes, ha="center", va="top",
        fontsize=11, color=WINE, bbox=dict(boxstyle="round,pad=0.4", fc=mix(CRIMSON, 0.08), ec=mix(CRIMSON, 0.35)))
a2.set_ylim(0, orr[-1] * 1.75)
save(fig, "../../assets/img/w04/prs_overlap.png")
