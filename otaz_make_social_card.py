"""Black-and-white social card for the OTAZ III deposit (LinkedIn / Zenodo teaser).

Two formats are produced, both monochrome, both drawn from the same numbers that
the manuscript proves and the experiments store:

  publication/OTAZ_III_Social_Card.png / .svg    square, 1200 x 1200
  publication/OTAZ_III_Social_Card_wide.png/.svg wide,   1200 x  627

SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "publication"
OUT.mkdir(exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "mathtext.fontset": "dejavuserif",
    "text.color": "black",
    "axes.edgecolor": "black",
})

INK = "black"


def rule(fig, y, x0=0.06, x1=0.94, lw=0.9):
    fig.add_artist(plt.Line2D([x0, x1], [y, y], lw=lw, color=INK,
                              transform=fig.transFigure))


def frame(fig, x0, y0, w, h, lw=1.2):
    fig.add_artist(plt.Rectangle((x0, y0), w, h, fill=False, lw=lw, color=INK,
                                 transform=fig.transFigure))


def card(path_stem, w_in, h_in, compact=False):
    """Draw one card. The square format is the primary asset."""
    fig = plt.figure(figsize=(w_in, h_in), dpi=150)
    fig.patch.set_facecolor("white")
    frame(fig, 0.022, 0.022, 0.956, 0.956, lw=2.0)
    frame(fig, 0.034, 0.034, 0.932, 0.932, lw=0.7)

    # ---- masthead
    fig.text(0.5, 0.937, "OTAZ III", ha="center", va="center",
             fontsize=38 if not compact else 33, fontweight="bold")
    fig.text(0.5, 0.892, "The Gibbs Ledger", ha="center", va="center",
             fontsize=17, style="italic")
    fig.text(0.5, 0.864,
             "Exact aggregation \u00b7 a sharp impossibility theorem \u00b7 "
             "certified error budgets",
             ha="center", va="center", fontsize=10)
    rule(fig, 0.846)

    # ---- the object
    fig.text(0.5, 0.823, "THE OBJECT", ha="center", va="center", fontsize=9,
             fontweight="bold")
    fig.text(0.5, 0.776,
             r"$V=\sum_i p_i v_i,\qquad p_i=e^{\beta w_i}/Z,\qquad "
             r"W=\beta^{-1}\ln Z$",
             ha="center", va="center", fontsize=19 if not compact else 17)
    fig.text(0.5, 0.733,
             "one score and one value per record \u2014 the pair a shard must carry",
             ha="center", va="center", fontsize=10.5)

    # ---- the claim box
    frame(fig, 0.070, 0.252, 0.860, 0.452, lw=1.1)
    fig.text(0.5, 0.678, "THE NEW RESULT", ha="center", va="center",
             fontsize=8.5, fontweight="bold")
    fig.text(0.5, 0.647, "Let every shard report its value and nothing else.",
             ha="center", va="center", fontsize=12)
    fig.text(0.5, 0.613, "Then the answers still compatible with the reports are",
             ha="center", va="center", fontsize=11.5)
    fig.text(0.5, 0.573, r"$V\ \in\ \mathrm{conv}\,\{V_1,\dots,V_k\}$",
             ha="center", va="center", fontsize=16)
    fig.text(0.5, 0.532, "so no rule can promise better, in the worst case, than",
             ha="center", va="center", fontsize=11.5)
    fig.text(0.5, 0.490,
             r"$\mathrm{err}\ \geq\ \frac{1}{2}"
             r"\left(\max_j V_j-\min_j V_j\right)$",
             ha="center", va="center", fontsize=16)
    fig.text(0.5, 0.448, "The bound is attained. The minimax rule is the midpoint.",
             ha="center", va="center", fontsize=11)
    fig.text(0.5, 0.417,
             "Equal weighting never beats it \u2014 worse by up to 1.46\u00d7 "
             "on 300 instances.",
             ha="center", va="center", fontsize=11)
    fig.add_artist(plt.Line2D([0.16, 0.84], [0.394, 0.394], lw=0.5, color=INK,
                              transform=fig.transFigure))
    fig.text(0.5, 0.371,
             "Carry the mass and the error is zero. Quantise it to relative "
             "precision",
             ha="center", va="center", fontsize=11)
    fig.text(0.5, 0.339, r"$\delta$  and the error stays bounded by",
             ha="center", va="center", fontsize=11)
    fig.text(0.5, 0.302,
             r"$|\tilde V-V|\ \leq\ D\,\delta/(1-\delta)$"
             "\u2003 for any number of shards",
             ha="center", va="center", fontsize=13.5)
    fig.text(0.5, 0.272, "proved, and measured on 600 random instances",
             ha="center", va="center", fontsize=9.5, style="italic")

    # ---- evidence strip
    fig.text(0.5, 0.213,
             "12 theorems \u00b7 2 lemmas \u00b7 1 corollary     |     "
             "16 seeded experiments     |     19 result files",
             ha="center", va="center", fontsize=10)
    fig.text(0.5, 0.185,
             "52 unit tests \u00b7 56 independent checks that do not import the code "
             "they check",
             ha="center", va="center", fontsize=10)
    fig.text(0.5, 0.152,
             "one seed (2026110101) \u00b7 every number recoverable from its JSON\n"
             "negative results in the text, not in a footnote",
             ha="center", va="center", fontsize=9.5, linespacing=1.5)
    rule(fig, 0.113)

    # ---- footer
    fig.text(0.5, 0.089, "Al-Mu'taz Billah Salah Al-Dawoodiya",
             ha="center", va="center", fontsize=12, fontweight="bold")
    fig.text(0.5, 0.066,
             "preprint  \u00b7  Zenodo  \u00b7  full text, code and results in one deposit",
             ha="center", va="center", fontsize=9)
    fig.text(0.5, 0.046,
             "CC BY-NC 4.0 text and results  \u00b7  PolyForm Noncommercial 1.0.0 code  "
             "\u00b7  not peer reviewed",
             ha="center", va="center", fontsize=7.8)

    fig.savefig(OUT / f"{path_stem}.png", facecolor="white", dpi=150)
    fig.savefig(OUT / f"{path_stem}.svg", facecolor="white")
    plt.close(fig)
    print("wrote", path_stem)


def card_wide(path_stem):
    """12:6.27 wide card, its own two-column layout (no scaling of the square)."""
    fig = plt.figure(figsize=(12.0, 6.27), dpi=150)
    fig.patch.set_facecolor("white")
    frame(fig, 0.016, 0.030, 0.968, 0.940, lw=2.0)
    frame(fig, 0.026, 0.046, 0.948, 0.908, lw=0.7)

    # left column: masthead and the object
    fig.text(0.245, 0.895, "OTAZ III", ha="center", va="center",
             fontsize=32, fontweight="bold")
    fig.text(0.245, 0.823, "The Gibbs Ledger", ha="center", va="center",
             fontsize=16, style="italic")
    fig.text(0.245, 0.758,
             "Exact aggregation \u00b7 a sharp impossibility\ntheorem \u00b7 certified error budgets",
             ha="center", va="center", fontsize=10.5, linespacing=1.5)
    rule(fig, 0.700, x0=0.06, x1=0.44)

    fig.text(0.245, 0.648, "THE OBJECT", ha="center", va="center", fontsize=9,
             fontweight="bold")
    fig.text(0.245, 0.548,
             r"$V=\sum_i p_i v_i$" "\n"
             r"$p_i=e^{\beta w_i}/Z$" "\n"
             r"$W=\beta^{-1}\ln Z$",
             ha="center", va="center", fontsize=13.5, linespacing=1.8)
    fig.text(0.245, 0.372,
             "one score and one value per record \u2014\nthe pair a shard must carry",
             ha="center", va="center", fontsize=10.5, linespacing=1.5)
    rule(fig, 0.312, x0=0.06, x1=0.44)
    fig.text(0.245, 0.236,
             "12 theorems \u00b7 2 lemmas \u00b7 1 corollary\n"
             "16 seeded experiments \u00b7 19 result files\n"
             "52 unit tests \u00b7 56 independent checks\n"
             "one seed (2026110101) \u00b7 every number\n"
             "recoverable from its JSON",
             ha="center", va="center", fontsize=10, linespacing=1.75)

    # right column: the result
    frame(fig, 0.485, 0.170, 0.470, 0.690, lw=1.1)
    fig.text(0.720, 0.818, "THE NEW RESULT", ha="center", va="center",
             fontsize=9, fontweight="bold")
    fig.text(0.720, 0.755, "Let every shard report its value and nothing else.",
             ha="center", va="center", fontsize=11.5)
    fig.text(0.720, 0.696, "Then every answer in the hull is compatible:",
             ha="center", va="center", fontsize=11)
    fig.text(0.720, 0.628, r"$V\ \in\ \mathrm{conv}\,\{V_1,\dots,V_k\}$",
             ha="center", va="center", fontsize=16)
    fig.text(0.720, 0.552, "so the worst case cannot beat", ha="center",
             va="center", fontsize=11)
    fig.text(0.720, 0.472,
             r"$\mathrm{err}\ \geq\ \frac{1}{2}"
             r"\left(\max_j V_j-\min_j V_j\right)$",
             ha="center", va="center", fontsize=16)
    fig.text(0.720, 0.395, "attained, by the midpoint. Equal weighting\nnever "
                           "beats it (worse by 1.46\u00d7 on 300 cases).",
             ha="center", va="center", fontsize=10.5, linespacing=1.5)
    fig.add_artist(plt.Line2D([0.55, 0.89], [0.330, 0.330], lw=0.5, color=INK,
                              transform=fig.transFigure))
    fig.text(0.720, 0.283, "Carry the mass: error zero. Quantise it to\n"
                           r"precision $\delta$: bounded, always",
             ha="center", va="center", fontsize=10.5, linespacing=1.5)
    fig.text(0.720, 0.212,
             r"$|\tilde V-V|\ \leq\ D\,\delta/(1-\delta)$",
             ha="center", va="center", fontsize=14.5)

    # footer strip
    rule(fig, 0.135, x0=0.05, x1=0.95)
    fig.text(0.5, 0.100, "Al-Mu'taz Billah Salah Al-Dawoodiya", ha="center",
             va="center", fontsize=11.5, fontweight="bold")
    fig.text(0.5, 0.072,
             "preprint  \u00b7  Zenodo  \u00b7  full text, code and results in one deposit",
             ha="center", va="center", fontsize=9)
    fig.text(0.5, 0.052,
             "CC BY-NC 4.0 text and results  \u00b7  PolyForm Noncommercial 1.0.0 code  "
             "\u00b7  not peer reviewed",
             ha="center", va="center", fontsize=8)

    fig.savefig(OUT / f"{path_stem}.png", facecolor="white", dpi=150)
    fig.savefig(OUT / f"{path_stem}.svg", facecolor="white")
    plt.close(fig)
    print("wrote", path_stem)


def main():
    card("OTAZ_III_Social_Card", 8.0, 8.0)
    card_wide("OTAZ_III_Social_Card_wide")


if __name__ == "__main__":
    main()
