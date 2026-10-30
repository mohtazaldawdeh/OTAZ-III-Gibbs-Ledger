"""Cover card for OTAZ III, monochrome, generated deterministically.

The card states the object of the study, the two slots of the ledger, the four
results the paper is built around, and the sizes of the evidence base. It is
deliberately plain: black on white, no colour, no gradients.

Output: publication/OTAZ_III_Cover.png and .svg

SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "publication"
OUT.mkdir(exist_ok=True)

RESULTS = [
    ("Thm 1", "the ledger is a commutative monoid; duplicates add \u03b2\u207b\u00b9 ln 2"),
    ("Thm 3", "value-only summaries leave the merged value on the convex hull"),
    ("Thm 4", "the minimax rule is the midpoint; its error is half the range"),
    ("Thm 5", "quantised masses merge to within D\u03b4/(1\u2212\u03b4), any shard count"),
    ("Thm 6", "temperature calculus: dV/d\u03b2 = Cov(v,w), d\u00b2lnZ/d\u03b2\u00b2 = Var(w)"),
    ("Thm 7", "coarse-graining gap = \u03b2\u207b\u00b9 H(\u03c0) \u2264 \u03b2\u207b\u00b9 ln k"),
    ("Thm 10", "sampling and truncation compose into one certified interval"),
    ("Thm 11", "dephasing contracts trace distance: the diagonal is a lower bound"),
]


def main():
    plt.rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif"]})
    fig = plt.figure(figsize=(8.27, 11.69))          # A4
    fig.patch.set_facecolor("white")

    # outer frame
    fig.add_artist(plt.Rectangle((0.04, 0.03), 0.92, 0.94, fill=False,
                                 lw=1.6, color="black", transform=fig.transFigure))
    fig.add_artist(plt.Rectangle((0.055, 0.045), 0.89, 0.91, fill=False,
                                 lw=0.6, color="black", transform=fig.transFigure))

    fig.text(0.5, 0.928, "OTAZ III", ha="center", va="center", fontsize=32,
             fontweight="bold")
    fig.text(0.5, 0.897, "The Gibbs Ledger", ha="center", va="center", fontsize=16,
             style="italic")
    fig.text(0.5, 0.870,
             "Exact aggregation, a sharp impossibility theorem, and certified error\n"
             "budgets for scored-record fusion",
             ha="center", va="center", fontsize=10.5, linespacing=1.5)

    fig.add_artist(plt.Line2D([0.10, 0.90], [0.842, 0.842], lw=0.9, color="black",
                              transform=fig.transFigure))

    fig.text(0.5, 0.812, "The object: one scored record per shard, one ledger per pair",
             ha="center", va="center", fontsize=11, fontweight="bold")

    fig.text(0.5, 0.765,
             r"$V=\sum_i p_i v_i,\qquad p_i=\frac{e^{\beta w_i}}{Z},\qquad "
             r"W=\frac{1}{\beta}\ln Z$",
             ha="center", va="center", fontsize=17)
    fig.text(0.5, 0.727,
             r"ledger $=(\ln Z,\ \sum_i e^{\beta w_i}v_i)$   $\longrightarrow$   exact merge in any tree",
             ha="center", va="center", fontsize=11)

    fig.add_artist(plt.Line2D([0.10, 0.90], [0.700, 0.700], lw=0.6, color="black",
                              transform=fig.transFigure))

    fig.text(0.145, 0.672, "Result", ha="left", va="center", fontsize=9.5,
             fontweight="bold")
    fig.text(0.300, 0.672, "What is proved in this paper", ha="left", va="center",
             fontsize=9.5, fontweight="bold")

    y = 0.634
    for label, text in RESULTS:
        fig.text(0.150, y, label, ha="left", va="center", fontsize=10,
                 fontweight="bold")
        fig.text(0.300, y, text, ha="left", va="center", fontsize=10)
        fig.add_artist(plt.Line2D([0.10, 0.90], [y - 0.021, y - 0.021], lw=0.3,
                                  color="black", transform=fig.transFigure))
        y -= 0.042

    fig.text(0.5, y - 0.012,
             "plus Theorems 2, 8, 9 and 12, Corollary 1, and two lemmas: twelve theorems, "
             "two lemmas, one corollary",
             ha="center", va="center", fontsize=9)

    fig.add_artist(plt.Line2D([0.10, 0.90], [0.235, 0.235], lw=0.9, color="black",
                              transform=fig.transFigure))
    fig.text(0.5, 0.205,
             "Sixteen seeded experiments, 52 unit tests, a 56-check independent verifier.",
             ha="center", va="center", fontsize=9.5)
    fig.text(0.5, 0.182,
             "Eight monochrome figures, nineteen stored result files, master seed 2026110101.",
             ha="center", va="center", fontsize=9.5)
    fig.text(0.5, 0.152,
             "Negative results are in the text: a bootstrap that under-covers, a certificate\n"
             "that saturates, and a quantisation bound that is proved but not attained.",
             ha="center", va="center", fontsize=9, linespacing=1.5)
    fig.text(0.5, 0.108, "Al-Mu'taz Billah Salah Al-Dawoodiya",
             ha="center", va="center", fontsize=11.5, fontweight="bold")
    fig.text(0.5, 0.085,
             "Preprint, 2026  \u00b7  text and results CC BY-NC 4.0  \u00b7  code PolyForm Noncommercial 1.0.0",
             ha="center", va="center", fontsize=8.5)
    fig.text(0.5, 0.062, "Companion report: doi.org/10.5281/zenodo.23648070",
             ha="center", va="center", fontsize=8.5)

    for ext in ("png", "svg"):
        fig.savefig(OUT / f"OTAZ_III_Cover.{ext}", facecolor="white",
                    dpi=300 if ext == "png" else None)
    plt.close(fig)
    print("cover written")


if __name__ == "__main__":
    main()
