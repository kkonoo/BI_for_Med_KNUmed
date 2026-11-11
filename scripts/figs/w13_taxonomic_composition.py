# W13 §1.2 몸 부위마다 다른 공동체, 건강한 사람끼리도 다른 장내 공동체 (가상의 예)
# BI_for_Biomed W7 taxonomic_composition(n1_sites.py)을 한글로 다시 그림
from medfig import *

rng = np.random.default_rng(9)
phyla = [("Bacteroidetes", WINE), ("Firmicutes", CRIMSON), ("Proteobacteria", ORANGE),
         ("Actinobacteria", AMBER), ("Fusobacteria", mix(CRIMSON, 0.35)), ("기타", "#D5D9DF")]
sites = {"장": [0.42, 0.45, 0.04, 0.04, 0.005, 0.045],
         "입": [0.18, 0.36, 0.20, 0.12, 0.08, 0.06],
         "피부": [0.05, 0.25, 0.15, 0.50, 0.005, 0.045],
         "질": [0.02, 0.90, 0.02, 0.04, 0.0, 0.02]}

fig, (a, b) = plt.subplots(1, 2, figsize=(10.4, 4.3), gridspec_kw={"wspace": 0.12, "width_ratios": [0.8, 1.2]})


def stack(ax, X, V, w, show_pct):
    bottom = np.zeros(len(X))
    for k, (_, c) in enumerate(phyla):
        ax.bar(X, V[:, k], bottom=bottom, color=c, width=w, edgecolor="white", lw=0.8)
        if show_pct:
            for x, v, y0 in zip(X, V[:, k], bottom):
                if v >= 0.12:
                    ax.text(x, y0 + v / 2, f"{v:.0%}", ha="center", va="center", fontsize=9,
                            color="white" if k < 4 else TEXT)
        bottom += V[:, k]


def style(ax, tag):
    for sp in ("left", "top", "right"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(LINE)
    ax.tick_params(length=0, labelsize=10)
    ax.set_ylim(0, 1.0)
    ax.text(0, 1.06, tag, transform=ax.transAxes, fontsize=11.5, fontweight="bold", color=TEXT, va="bottom")


V = np.array(list(sites.values()))
stack(a, np.arange(4), V, 0.64, True)
a.set_xticks(range(4))
a.set_xticklabels(sites.keys(), fontsize=11.5, fontweight="bold", color=TEXT)
a.set_yticks([0, 0.5, 1])
a.set_yticklabels(["0", "50%", "100%"], color=TEXT2)
style(a, "① 부위마다 다른 생태계")

n = 14
base = np.log(np.array(sites["장"]) + 0.005)
G = np.exp(base + rng.normal(0, 0.6, (n, 6)))
G /= G.sum(1, keepdims=True)
G = G[np.argsort(-G[:, 0])]
stack(b, np.arange(n), G, 0.8, False)
b.set_xticks([])
b.set_yticks([])
b.set_xlabel("건강한 성인 14명의 대변", fontsize=10.5, color=TEXT2, labelpad=8)
style(b, "② 같은 장, 사람마다 다른 공동체")

handles = [mp.Patch(fc=c, ec="none", label=nm) for nm, c in phyla]
fig.legend(handles=handles, loc="lower center", ncol=6, frameon=False, fontsize=10, bbox_to_anchor=(0.5, -0.07),
           handlelength=1.0, columnspacing=1.4)
save(fig, "../../assets/img/w13/taxonomic_composition.png")
