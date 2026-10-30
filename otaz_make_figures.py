"""Monochrome figures for OTAZ-III.  No colour is used anywhere: every curve is
distinguished by line style and marker shape only.

Outputs: figures/fig1 ... fig6 as .svg (vector) and .png (300 dpi fallback).

SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[0]
RES = ROOT / "results"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "font.size": 9,
    "axes.edgecolor": "black",
    "axes.linewidth": 0.8,
    "axes.prop_cycle": matplotlib.cycler(color=["black"]),
    "lines.linewidth": 1.0,
    "legend.frameon": False,
    "figure.dpi": 120,
    "savefig.facecolor": "white",
    "text.color": "black",
    "xtick.color": "black",
    "ytick.color": "black",
})

STYLES = ["-", "--", ":", "-."]
MARKERS = ["o", "s", "^", "D"]


def load(name):
    return json.loads((RES / name).read_text())


def save(fig, stem):
    for ext in ("svg", "png"):
        fig.savefig(FIG / f"{stem}.{ext}", bbox_inches="tight",
                    facecolor="white", dpi=300 if ext == "png" else None)
    plt.close(fig)


def fig_gap_bound():
    """Realised gaps spread from zero up to the bounded value beta^-1 ln k."""
    rng = np.random.default_rng(4242)
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    top = 0.0
    for i, k in enumerate([2, 4, 8]):
        xs, ys = [], []
        for alpha in (0.2, 1.0, 20.0):
            for _ in range(60):
                beta = float(rng.choice([0.5, 1.0, 2.0]))
                pi = rng.dirichlet(np.full(k, alpha))
                gap = -float((pi * np.log(pi)).sum()) / beta
                bound = math.log(k) / beta
                xs.append(bound)
                ys.append(gap)
                top = max(top, bound)
        ax.plot(xs, ys, MARKERS[i], ls="none", ms=2.4, mfc="none",
                label=f"$k={k}$")
    lim = np.linspace(0, top * 1.05, 10)
    ax.plot(lim, lim, "k-", lw=0.8, label="bound $\\beta^{-1}\\ln k$")
    ax.set_xlabel("bound for the chosen $k$ and $\\beta$ [nats]")
    ax.set_ylabel("realised gap [nats]")
    ax.legend(fontsize=6, loc="upper left", ncol=2)
    ax.set_title("Every gap lies on or below its bound", fontsize=8)
    save(fig, "fig4_gap_bound")


def fig_sampling_error():
    data = load("e7_sampling.json")[0]
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    for i, beta in enumerate([1.0, 3.0]):
        rows = [r for r in data["rows"] if r["beta"] == beta]
        shots = [r["shots"] for r in rows]
        ax.plot(shots, [r["mean_value_error"] for r in rows], STYLES[i],
                marker=MARKERS[i], ms=3.5, label=rf"error, $\beta={beta}$")
        ax.plot(shots, [r["mean_certificate"] for r in rows], STYLES[(i + 2) % 4],
                marker=MARKERS[(i + 1) % 4], ms=3.0, mfc="none",
                label=rf"certificate, $\beta={beta}$")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("shots per replication")
    ax.set_ylabel("absolute value error")
    ax.legend(fontsize=6, loc="lower left")
    ax.set_title("Measured error and its certificate", fontsize=8)
    save(fig, "fig5_sampling")


def fig_coverage():
    data = load("e7_sampling.json")[0]
    cov = data["coverage"]
    fig, ax = plt.subplots(figsize=(3.4, 2.4))
    labels, vals, hatches = [], [], []
    for i, c in enumerate(cov):
        labels.append(f"{c['shots']}\n$\\beta$={c['beta']:.0f}" if i < 4 else f"{c['shots']}\n$\\beta$={c['beta']:.0f}")
        vals.append(c["coverage_95_bootstrap"])
        hatches.append("" if c["beta"] == 1.0 else "///")
    x = np.arange(len(vals))
    ax.bar(x, vals, color="white", edgecolor="black", linewidth=0.7)
    for bar, h in zip(ax.patches, hatches):
        bar.set_hatch(h)
    ax.axhline(0.95, color="black", ls="--", lw=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=6)
    ax.set_ylim(0.80, 1.02)
    ax.set_ylabel("bootstrap 95% coverage")
    ax.set_title("Nominal against realised coverage", fontsize=8)
    save(fig, "fig6_coverage")


def fig_trace_distance():
    data = load("e11_dephasing.json")[0]
    rng = np.random.default_rng(99)
    full, diag = [], []
    for _ in range(250):
        n = int(rng.integers(2, 6))
        a = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        b = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        ra = a @ a.conj().T
        rb = b @ b.conj().T
        ra /= np.trace(ra)
        rb /= np.trace(rb)
        full.append(0.5 * np.linalg.svd(ra - rb, compute_uv=False).sum())
        da, db = np.diag(ra).real, np.diag(rb).real
        diag.append(0.5 * np.abs(da - db).sum())
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    ax.plot(diag, full, "o", ms=2.4, mfc="none")
    ax.plot([0, 1], [0, 1], "k--", lw=0.8, label="diagonal = full")
    ax.set_xlabel("trace distance of dephased states")
    ax.set_ylabel("trace distance of full states")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.legend(fontsize=7, loc="upper left")
    ax.set_title("Coherence only ever adds distance", fontsize=8)
    save(fig, "fig7_trace_distance")


def fig_temperature():
    """Self-scored sensitivity: monotone for symmetric scores, peaked for skewed ones."""
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    cases = [
        (np.array([-2.0, -1.0, 0.0, 1.0, 2.0]), "-", "o", "symmetric scores"),
        (np.array([0.0, 1.0, 2.0, 3.0, 10.0]), "--", "s", "skewed scores"),
    ]
    betas = np.logspace(-2, 1.5, 240)
    for w, ls, mk, label in cases:
        var = []
        for b in betas:
            x = b * w
            p = np.exp(x - x.max())
            p = p / p.sum()
            var.append(float((p * (w - p @ w) ** 2).sum()))
        ax.plot(betas, var, ls, color="black", lw=1.0, label=label)
        k = int(np.argmax(var))
        ax.plot([betas[k]], [var[k]], mk, ms=4, mfc="none", color="black")
    ax.set_xscale("log")
    ax.set_xlabel(r"inverse temperature $\beta$")
    ax.set_ylabel(r"$\mathrm{Var}_p(w)$ [nats$^2$]")
    ax.set_ylim(-0.5, 19.5)
    ax.set_title("Sensitivity against temperature", fontsize=8)
    ax.legend(fontsize=6.5, loc="upper right")
    save(fig, "fig3_temperature")


def fig_helstrom():
    data = load("e6_helstrom.json")[0]
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    r = np.linspace(0, 4, 200)
    for i, beta in enumerate([0.5, 1.0, 2.0, 4.0]):
        ax.plot(r, 0.5 * (1 - np.tanh(beta * r / 4)), STYLES[i], label=rf"$\beta={beta}$")
    ax.set_xlabel("score range of the perturbation")
    ax.set_ylabel("lower bound on error probability")
    ax.set_title("Distinguishability floor", fontsize=8)
    ax.legend(fontsize=7)
    save(fig, "fig8_helstrom")



def fig_reachable():
    """Value-only summaries leave an interval; the ledger collapses it to a point."""
    rng = np.random.default_rng(777)
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    minimax, blind = [], []
    for _ in range(300):
        k = int(rng.integers(2, 7))
        v = rng.normal(0, 3, k)
        mm = 0.5 * (v.max() - v.min())
        eqw = max(v.max() - v.mean(), v.mean() - v.min())
        minimax.append(mm)
        blind.append(eqw)
    lim = max(max(minimax), max(blind)) * 1.05
    ax.plot(minimax, blind, "o", ms=2.4, mfc="none", color="black")
    ax.plot([0, lim], [0, lim], "k--", lw=0.8, label="equal-risk edge")
    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    ax.set_xlabel("minimax worst-case error  (range/2)")
    ax.set_ylabel("worst-case error of equal weighting")
    ax.legend(fontsize=7, loc="upper left")
    ax.set_title("Mass-blind merging is never minimax", fontsize=8)
    save(fig, "fig1_reachable")


def fig_quantisation():
    data = load("e15_quantisation.json")[0]
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    deltas = [r["delta"] for r in data["rows"]]
    err = [r["mean_error"] for r in data["rows"]]
    bnd = [r["mean_bound"] for r in data["rows"]]
    ax.plot(deltas, err, "o-", color="black", ms=3.5, label="measured error")
    ax.plot(deltas, bnd, "s--", color="black", ms=3.0, mfc="none",
            label=r"bound $D\delta/(1-\delta)$")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"relative precision $\delta$ of the masses")
    ax.set_ylabel("merge error")
    ax.legend(fontsize=7)
    ax.set_title("Price of a lossy ledger", fontsize=8)
    save(fig, "fig2_quantisation")


def main():
    fig_gap_bound()
    fig_sampling_error()
    fig_coverage()
    fig_trace_distance()
    fig_temperature()
    fig_helstrom()
    fig_reachable()
    fig_quantisation()
    print("figures written:", sorted(p.name for p in FIG.glob("*.svg")))


if __name__ == "__main__":
    main()
