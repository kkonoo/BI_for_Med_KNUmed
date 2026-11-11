# W2 §1.2 같은 서열에 생긴 변이라도 단백질에 미치는 결과가 다름 — 코돈 줄과 "THE CAT ATE THE RAT" 비유 (새로 그림)
from medfig import *

ref = ["GAG", "CTG", "CGA", "GAC"]
aa_ref = ["Glu", "Leu", "Arg", "Asp"]
rows = [  # name, colour, codons, changed (codon, base), amino acids, changed aa idx, stop at, analogy, coloured letters, impact, note
    ("레퍼런스", TEXT, ref, [], aa_ref, [], None, "THE CAT ATE THE RAT", [], None, ""),
    ("동의 변이", CAT[0], ["GAG", "CTA", "CGA", "GAC"], [(1, 2)], aa_ref, [], None,
     "THE CAT ATE THE RAT", [], "LOW", "염기는 바뀌어도 아미노산은 그대로"),
    ("Missense", CAT[1], ["GTG", "CTG", "CGA", "GAC"], [(0, 1)], ["Val"] + aa_ref[1:], [0], None,
     "THE BAT ATE THE RAT", [4], "MODERATE", "아미노산 하나가 바뀜"),
    ("Nonsense", CAT[2], ["GAG", "CTG", "TGA", "GAC"], [(2, 0)], ["Glu", "Leu", "종결", ""], [2], 2,
     "THE CAT.", [7], "HIGH", "종결 코돈 → 단백질이 일찍 끝남"),
    ("Frameshift", CAT[3], ["GAG", "ACT", "GCG", "AGA"], [(1, 0)], ["Glu", "Thr", "Ala", "Arg"], [1, 2, 3], None,
     "THE CAA TAT ETH ERA T", [6], "HIGH", "1염기 삽입 → 그 뒤가 모두 어긋남"),
]
impact_style = {"LOW": (FAINT, TEXT2), "MODERATE": (mix(CRIMSON, 0.3), WINE), "HIGH": (CRIMSON, "white")}

CW, GAP, X0 = 0.28, 0.13, 1.75           # base cell width, gap between codons, codon start
XA = X0 + 4 * (3 * CW + GAP) + 0.4      # analogy column
fig, ax = new(XA + 3.0, 6.3)
label(ax, X0, 6.05, "DNA (코돈) → 아미노산", fs=11, w="semibold", c=TEXT2, ha="left")
label(ax, XA, 6.05, "문장 비유", fs=11, w="semibold", c=TEXT2, ha="left")
ax.plot([0.3, XA + 2.35], [5.85, 5.85], color=LINE, lw=1)

for r, (name, col, cods, changed, aas, aa_ch, stop, analogy, an_ch, impact, note) in enumerate(rows):
    y = 5.4 - r * 1.12
    label(ax, X0 - 0.2, y + (0.08 if impact else 0), name, fs=13, w="bold", c=col, ha="right")
    if impact:   # W3 표의 impact 등급
        fc, tc = impact_style[impact]
        box(ax, X0 - 1.32, y - 0.42, 1.12, 0.3, fc=fc, ec="none", r=0.15)
        label(ax, X0 - 0.76, y - 0.27, impact, fs=11, w="bold", c=tc)
    for c, cod in enumerate(cods):
        xc = X0 + c * (3 * CW + GAP)
        faded = stop is not None and c > stop
        for b, base in enumerate(cod):
            x = xc + b * CW
            hot = (c, b) in changed
            fc = col if hot else (mix(FAINT, 0.5) if faded else FAINT)
            box(ax, x + 0.015, y - 0.17, CW - 0.03, 0.34, fc=fc, ec="none", r=0.04)
            label(ax, x + CW / 2, y, base, fs=13, w="bold" if hot else "regular",
                  c="white" if hot else ("#C4C7CC" if faded else "#4B5563"))
        if aas[c]:
            ch = c in aa_ch
            label(ax, xc + 1.5 * CW, y - 0.4, aas[c], fs=11.5, w="bold" if ch else "regular",
                  c=col if ch else TEXT2)
    if r == 4:   # the rest of the sequence is shifted too
        label(ax, X0 + 4 * (3 * CW + GAP) - 0.07, y, "…", fs=13, c="#4B5563", ha="left")
    for i, ch in enumerate(analogy):   # letter by letter so changed letters take the row colour
        label(ax, XA + i * 0.118, y + 0.02, ch, fs=12.5, w="bold" if i in an_ch else "regular",
              c=col if i in an_ch else TEXT, ha="left")
    if note:
        label(ax, XA, y - 0.4, note, fs=12, c=TEXT2, ha="left")
label(ax, X0 - 0.76, 6.05, "W3 impact", fs=11, w="semibold", c=TEXT2)
save(fig, "../../assets/img/w02/consequences.png")
