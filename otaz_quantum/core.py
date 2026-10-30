"""OTAZ-III research core.

Contents
--------
* Gibbs / log-partition primitives (weights, log Z, fusion pair, free energy)
* temperature calculus (fluctuation-dissipation, heat capacity)
* exact representability and error non-amplification
* coarse-graining accounting (gap = entropy / beta) and its chain rule
* commuting vs coherent states, trace-distance interface, Helstrom floor
* finite-shot estimation with an explicit certificate

Conventions: beta is a finite non-zero real; w is a real vector of scores;
values v may be vectors; "TV" is the total-variation distance.

SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Required Notice: Copyright 2026 Al-Mu'taz Billah Salah Al-Dawoodiya
Prior work: https://doi.org/10.5281/zenodo.23648070
"""
import math

import numpy as np
from scipy.special import logsumexp, softmax
from scipy.stats import unitary_group


# --------------------------------------------------------------- primitives
def _beta(beta):
    if not math.isfinite(beta):
        raise ValueError("beta must be finite")
    if beta == 0:
        raise ValueError("beta must be non-zero")
    return float(beta)


def _scores(w, beta):
    beta = _beta(beta)
    w = np.asarray(w, dtype=float)
    if w.ndim != 1 or w.size == 0:
        raise ValueError("w must be a non-empty vector")
    if not np.isfinite(w).all():
        raise ValueError("w must be finite")
    x = beta * w
    if not np.isfinite(x).all():
        raise ValueError("scaled scores must be representable")
    return w, x


def weights(w, beta=1.0):
    """p = softmax(beta * w).  The fusion weights are a Gibbs distribution."""
    return softmax(_scores(w, beta)[1])


def log_partition(w, beta=1.0):
    """ln Z with Z = sum_i exp(beta w_i), evaluated by max-shifted logsumexp."""
    return float(logsumexp(_scores(w, beta)[1]))


def fuse(values, w, beta=1.0):
    """Return (p^T v, beta^-1 ln Z), the fused value and the score."""
    _, x = _scores(w, beta)
    v = np.asarray(values, dtype=float)
    if v.ndim == 1:
        v = v[:, None]
    if v.ndim != 2 or v.shape[0] != x.size:
        raise ValueError("values must be (n,) or (n,k) aligned with w")
    if not np.isfinite(v).all():
        raise ValueError("values must be finite")
    p = softmax(x)
    return p @ v, float(logsumexp(x)) / float(beta)


def free_energy(w, beta=1.0):
    """F = -beta^-1 ln Z for the Hamiltonian H = -w, i.e. F = -W."""
    return -log_partition(w, beta) / float(beta)


def masses(w, beta=1.0):
    """Unnormalised Boltzmann masses exp(beta w_i), shifted for stability."""
    beta = _beta(beta)
    w = np.asarray(w, dtype=float)
    if w.ndim != 1 or w.size == 0 or not np.isfinite(w).all():
        raise ValueError("finite non-empty vector required")
    return np.exp(beta * (w - w.max()))


# ------------------------------------------------------- temperature calculus
def temperature_derivative(values, w, beta=1.0):
    """dV/dbeta = Cov_p(v, w) and d2 lnZ/dbeta^2 = Var_p(w) (fluctuation-dissipation)."""
    beta = _beta(beta)
    _, x = _scores(w, beta)
    v = np.asarray(values, dtype=float)
    if v.ndim == 1:
        v = v[:, None]
    if v.ndim != 2 or v.shape[0] != x.size or not np.isfinite(v).all():
        raise ValueError("values must be (n,) or (n,k) aligned with w")
    p = softmax(x)
    w = np.asarray(w, dtype=float)
    centered = w - float(p @ w)
    cov = (p[:, None] * centered[:, None] * (v - p @ v)).sum(axis=0)
    return cov, float((p * centered**2).sum())


def score_derivative(w, beta=1.0):
    """dW/dbeta = (E_p[w] - W)/beta, with W = beta^-1 ln Z."""
    beta = _beta(beta)
    _, x = _scores(w, beta)
    p = softmax(x)
    W = float(logsumexp(x)) / beta
    return (float(p @ np.asarray(w, dtype=float)) - W) / beta


def heat_capacity(w, beta=1.0):
    """Var_p(w) = d2 ln Z / dbeta^2 >= 0."""
    _, x = _scores(w, beta)
    w = np.asarray(w, dtype=float)
    p = softmax(x)
    return float((p * (w - float(p @ w)) ** 2).sum())


# --------------------------------------------------------- representability
def scores_for_distribution(q, beta=1.0):
    """Exact inverse of softmax: w_i = ln(q_i)/beta reproduces q exactly."""
    beta = _beta(beta)
    q = np.asarray(q, dtype=float)
    if q.ndim != 1 or q.size < 2:
        raise ValueError("q must be a vector with at least two entries")
    if not np.isfinite(q).all() or np.any(q <= 0):
        raise ValueError("q must be strictly positive and finite")
    if abs(q.sum() - 1.0) > 1e-12:
        raise ValueError("q must sum to one")
    return np.log(q) / beta


def renormalised_logit_weights(estimate):
    """softmax(ln a / beta * beta) = a / sum(a): no exponential amplification."""
    a = np.asarray(estimate, dtype=float)
    if a.ndim != 1 or a.size == 0 or not np.isfinite(a).all():
        raise ValueError("finite vector required")
    if np.any(a < 0) or a.sum() <= 0:
        raise ValueError("nonnegative entries with positive sum required")
    return a / a.sum()


def nonamplification_bound(l1_error):
    """If eps = ||p_hat - p||_1 < 1 then TV(p_hat/Z, p) <= eps/(1-eps)."""
    eps = float(l1_error)
    if not (0.0 <= eps < 1.0):
        raise ValueError("L1 error must lie in [0,1)")
    return eps / (1.0 - eps)


# ----------------------------------------------------------- coarse graining
def _check_blocks(w_size, blocks):
    seen = []
    for g in blocks:
        idx = [int(i) for i in g]
        if not idx:
            raise ValueError("empty block")
        if len(set(idx)) != len(idx):
            raise ValueError("repeated index inside a block")
        if min(idx) < 0 or max(idx) >= w_size:
            raise ValueError("index out of range")
        seen.extend(idx)
    if sorted(seen) != list(range(w_size)):
        raise ValueError("blocks must partition all indices exactly once")
    return [[int(i) for i in g] for g in blocks]


def _block_masses(w, blocks, beta):
    w = np.asarray(w, dtype=float)
    shift = w.max()
    return np.array([float(np.exp(beta * (w[idx] - shift)).sum()) for idx in blocks])


def block_entropy(mass_vector):
    """Shannon entropy of a mass vector, normalised internally."""
    m = np.asarray(mass_vector, dtype=float)
    if m.ndim != 1 or m.size == 0 or np.any(m <= 0):
        raise ValueError("strictly positive masses required")
    pi = m / m.sum()
    return float(-(pi * np.log(pi)).sum()), pi


def coarse_grain(w, blocks, beta=1.0):
    """Exact coarse-graining accounting for a partition of all indices.

    W_global - sum_B pi_B W_B = beta^-1 H(pi),  pi_B = m_B / sum_C m_C,

    with m_B = sum_{i in B} exp(beta w_i) and W_B = beta^-1 ln m_B.  The gap is
    non-negative, bounded by beta^-1 ln(k) for k blocks, and is the correction
    that any block-wise (coarse) evaluation of the fused pair must add back.
    """
    beta = _beta(beta)
    w = np.asarray(w, dtype=float)
    if w.ndim != 1 or not np.isfinite(w).all():
        raise ValueError("finite vector required")
    blocks = _check_blocks(w.size, blocks)
    m = _block_masses(w, blocks, beta)
    total = float(m.sum())
    entropy, pi = block_entropy(m)
    W_block = np.log(m) / beta
    W_global = math.log(total) / beta
    gap = W_global - float(pi @ W_block)
    return {
        "W_global": float(W_global),
        "weighted_block_score": float(pi @ W_block),
        "gap": float(gap),
        "block_entropy": entropy,
        "predicted_gap": entropy / beta,
        "identity_residual": float(gap - entropy / beta),
        "upper_bound_ln_blocks_over_beta": math.log(len(blocks)) / beta,
        "masses": m.tolist(),
        "pi": pi.tolist(),
        "block_scores": W_block.tolist(),
        "n_blocks": len(blocks),
    }


def hierarchy_gap(w, levels, beta=1.0):
    """Certify every level of a nested partition tree and report the gaps."""
    beta = _beta(beta)
    out = [coarse_grain(w, blocks, beta) for blocks in levels]
    return {
        "levels": out,
        "total_gap": float(sum(c["gap"] for c in out)),
        "n_levels": len(out),
    }


def hierarchical_chain(w, coarse_blocks, fine_blocks, beta=1.0):
    """Shannon chain rule for coarse graining.

    Requires fine_blocks to refine coarse_blocks.  Then

        Gap(fine) = Gap(coarse) + sum_B pi_B Gap_within(B).
    """
    beta = _beta(beta)
    w = np.asarray(w, dtype=float)
    if w.ndim != 1 or not np.isfinite(w).all():
        raise ValueError("finite vector required")
    coarse_blocks = _check_blocks(w.size, coarse_blocks)
    fine_blocks = _check_blocks(w.size, fine_blocks)
    owner_coarse = {}
    for gi, g in enumerate(coarse_blocks):
        for i in g:
            owner_coarse[i] = gi
    groups = {}
    for f in fine_blocks:
        owners = {owner_coarse[i] for i in f}
        if len(owners) != 1:
            raise ValueError("fine blocks must refine coarse blocks")
        groups.setdefault(owners.pop(), []).append(f)
    if len(groups) != len(coarse_blocks):
        raise ValueError("every coarse block must contain at least one fine block")
    coarse = coarse_grain(w, coarse_blocks, beta)
    fine = coarse_grain(w, fine_blocks, beta)
    weighted_within = 0.0
    within = []
    for gi, g in enumerate(coarse_blocks):
        local = {int(global_i): k for k, global_i in enumerate(g)}
        local_blocks = [[local[int(i)] for i in f] for f in groups[gi]]
        sub = coarse_grain(w[np.asarray(g, dtype=int)], local_blocks, beta)
        within.append(sub["gap"])
        weighted_within += coarse["pi"][gi] * sub["gap"]
    return {
        "gap_coarse": coarse["gap"],
        "gap_fine": fine["gap"],
        "within_gaps": within,
        "weighted_within_gaps": float(weighted_within),
        "chain_residual": float(fine["gap"] - (coarse["gap"] + weighted_within)),
        "entropy_coarse": coarse["block_entropy"],
        "entropy_fine": fine["block_entropy"],
        "n_coarse": len(coarse_blocks),
        "n_fine": len(fine_blocks),
    }


# ----------------------------------------------------- commuting / coherent
def density_from_weights(p):
    """Diagonal (commuting) state rho = diag(p)."""
    p = np.asarray(p, dtype=float)
    if p.ndim != 1 or np.any(p < 0) or abs(p.sum() - 1.0) > 1e-12:
        raise ValueError("probability vector required")
    return np.diag(p)


def trace_norm(a):
    a = np.asarray(a)
    if a.ndim != 2 or a.shape[0] != a.shape[1]:
        raise ValueError("square matrix required")
    return float(np.linalg.svd(a, compute_uv=False).sum())


def trace_distance(rho, sigma):
    rho = np.asarray(rho, dtype=complex)
    sigma = np.asarray(sigma, dtype=complex)
    if rho.shape != sigma.shape or rho.ndim != 2 or rho.shape[0] != rho.shape[1]:
        raise ValueError("two square matrices of equal shape required")
    return 0.5 * trace_norm(rho - sigma)


def von_neumann_entropy(rho):
    rho = np.asarray(rho, dtype=complex)
    ev = np.linalg.eigvalsh((rho + rho.conj().T) / 2)
    ev = ev[ev > 1e-15]
    return float(-(ev * np.log(ev)).sum())


def purity(rho):
    rho = np.asarray(rho, dtype=complex)
    return float(np.real(np.trace(rho @ rho)))


def dephase(rho):
    """Remove coherences (complete dephasing in the computational basis)."""
    rho = np.asarray(rho, dtype=complex)
    return np.diag(np.diag(rho).real).astype(complex)


def helstrom_error(rho, sigma):
    """Minimum error probability under equal priors: (1 - TV)/2."""
    return 0.5 * (1.0 - trace_distance(rho, sigma))


def helstrom_floor(score_range, beta):
    """Commuting-state floor P_e >= (1 - tanh(|beta| * range / 4)) / 2."""
    beta = _beta(beta)
    r = float(score_range)
    if r < 0:
        raise ValueError("range must be non-negative")
    return 0.5 * (1.0 - math.tanh(abs(beta) * r / 4.0))


def random_state_with_diagonal(diagonal, rng):
    """Random pure state whose computational-basis diagonal is the given vector."""
    d = np.asarray(diagonal, dtype=float)
    if d.ndim != 1 or np.any(d < 0) or abs(d.sum() - 1.0) > 1e-12:
        raise ValueError("probability vector required")
    phases = np.exp(2j * np.pi * rng.random(d.size))
    psi = np.sqrt(d) * phases
    psi = psi / np.linalg.norm(psi)
    return np.outer(psi, psi.conj())


def conjugate_by_hadamard(rho):
    """Apply H^tensor(rho) H^tensor for n-level power-of-two systems."""
    n = rho.shape[0]
    bits = int(math.log2(n))
    if 2**bits != n:
        raise ValueError("dimension must be a power of two")
    H1 = np.array([[1, 1], [1, -1]]) / math.sqrt(2)
    Hn = np.array([[1.0]])
    for _ in range(bits):
        Hn = np.kron(Hn, H1)
    return Hn @ rho @ Hn


# ----------------------------------------------------------- sampling budgets
def sample_counts(p, shots, rng):
    p = np.asarray(p, dtype=float)
    if not (isinstance(shots, (int, np.integer)) and shots > 0):
        raise ValueError("positive integer shot count required")
    if abs(p.sum() - 1.0) > 1e-9:
        raise ValueError("probability vector required")
    return rng.multinomial(int(shots), p)


def sampling_experiment(p_true, values, beta, shots, rng):
    """Estimate the weights from finite shots, refit the scores, and certify."""
    beta = _beta(beta)
    p_true = np.asarray(p_true, dtype=float)
    counts = sample_counts(p_true, shots, rng)
    p_hat = counts / float(counts.sum())
    # Add-one smoothing keeps log(p_hat) finite; the smoothing is disclosed.
    p_sm = (counts + 1.0) / (counts.sum() + p_true.size)
    w_true = np.log(p_true) / beta
    w_hat = np.log(p_sm) / beta
    V_true, _ = fuse(values, w_true, beta)
    V_hat, _ = fuse(values, w_hat, beta)
    l1 = float(np.abs(p_hat - p_true).sum())
    v = np.asarray(values, dtype=float)
    v = v[:, None] if v.ndim == 1 else v
    diameter = float(np.linalg.norm(v[:, None, :] - v[None, :, :], axis=2).max())
    return {
        "shots": int(shots),
        "counts": counts.tolist(),
        "l1_error": l1,
        "tv_of_empirical": 0.5 * l1,
        "value_error": float(np.linalg.norm(V_hat - V_true)),
        "certificate_nonamplification": nonamplification_bound(min(l1, 0.999999)),
        "diameter": diameter,
        "certificate_value": diameter * nonamplification_bound(min(l1, 0.999999)),
        "max_per_outcome_sd": float(np.sqrt(p_true * (1 - p_true) / shots).max()),
        "smoothing": "add-one",
    }

# --------------------------------------------------- binary fusion algebra
def pair_fuse(v_a, w_a, v_b, w_b, beta=1.0):
    """The source formula: A bowtie_beta B = (weighted value | log-sum-exp score).

    The value slot is the Gibbs-weighted mean of the two values and the second
    slot is beta^-1 ln(e^{beta w_A} + e^{beta w_B}).  Both slots are returned.
    """
    beta = _beta(beta)
    va = np.atleast_1d(np.asarray(v_a, dtype=float))
    vb = np.atleast_1d(np.asarray(v_b, dtype=float))
    if va.shape != vb.shape:
        raise ValueError("values must have equal shape")
    if not (np.isfinite(va).all() and np.isfinite(vb).all()):
        raise ValueError("values must be finite")
    alpha = float(softmax(beta * np.array([float(w_a), float(w_b)]))[0])
    value = alpha * va + (1.0 - alpha) * vb
    score = float(logsumexp(beta * np.array([float(w_a), float(w_b)]))) / beta
    return {"value": value, "score": score, "alpha_A": alpha}


def nary_fuse(records, beta=1.0):
    """n-ary fusion of records [(value, score), ...]; the n-item ground truth."""
    beta = _beta(beta)
    if len(records) < 1:
        raise ValueError("at least one record required")
    w = np.array([float(r[1]) for r in records])
    v = np.array([np.atleast_1d(np.asarray(r[0], dtype=float)) for r in records])
    V, W = fuse(v, w, beta)
    return {"value": V, "score": W}


def chained_pair_fuse(records, beta=1.0):
    """Left fold of pair_fuse; used to test associativity of the binary law."""
    beta = _beta(beta)
    if len(records) < 2:
        raise ValueError("at least two records required")
    value = np.atleast_1d(np.asarray(records[0][0], dtype=float))
    score = float(records[0][1])
    for v, w in records[1:]:
        out = pair_fuse(value, score, v, w, beta)
        value, score = out["value"], out["score"]
    return {"value": value, "score": score}


def is_linear_in_first_argument(v_a, w_a, v_b, w_b, beta=1.0, lam=2.0):
    """Check homogeneity of the value slot: F(lam*A, B) =? lam*F(A, B).

    Returns (left, right); equality would be required for the bracket to behave
    like the first slot of a bilinear form.
    """
    if lam == 0:
        raise ValueError("lam must be non-zero")
    base = pair_fuse(v_a, w_a, v_b, w_b, beta)["value"]
    scaled = pair_fuse(lam * np.atleast_1d(np.asarray(v_a, dtype=float)), w_a,
                       np.atleast_1d(np.asarray(v_b, dtype=float)), w_b, beta)["value"]
    return scaled, lam * base

# ------------------------------------------------- ledger necessity (Sec. IV)
def achievable_values(block_values, beta=1.0):
    """Set of global values reachable from value-only block summaries.

    Each block may carry any positive mass, so the reachable set is the convex
    hull of the block values, i.e. the closed interval [min, max].  Returned as
    a pair so callers can reason about the diameter without importing numpy
    conventions.
    """
    beta = _beta(beta)
    v = np.asarray(block_values, dtype=float)
    if v.ndim != 1 or v.size == 0 or not np.isfinite(v).all():
        raise ValueError("finite non-empty vector of block values required")
    return {"low": float(v.min()), "high": float(v.max()),
            "diameter": float(v.max() - v.min()), "k": int(v.size)}


def minimax_value(block_values, beta=1.0):
    """Minimax estimate of the global value from value-only summaries.

    With the reachable set equal to [min V_B, max V_B], the minimax rule is the
    midpoint and its worst-case error is exactly half the range (Theorem 4).
    """
    a = achievable_values(block_values, beta)
    mid = 0.5 * (a["low"] + a["high"])
    return {"estimate": mid, "worst_case_error": 0.5 * a["diameter"],
            "reachable": a}


def ledger_blind_merge(block_values, counts=None):
    """A merge that ignores masses: equal weights, or counted equal weights."""
    v = np.asarray(block_values, dtype=float)
    if v.ndim != 1 or v.size == 0 or not np.isfinite(v).all():
        raise ValueError("finite non-empty vector required")
    if counts is None:
        return float(v.mean())
    n = np.asarray(counts, dtype=float)
    if n.shape != v.shape or np.any(n <= 0):
        raise ValueError("counts must be positive and aligned")
    return float((n * v).sum() / n.sum())


def quantised_merge(block_values, block_masses, relative_precision):
    """Merge using masses known only to relative precision delta.

    Returns the merged value, the exact value and the certified error bound
    D * delta / (1 - delta) of Theorem 5, where D is the value diameter.
    """
    v = np.asarray(block_values, dtype=float)
    m = np.asarray(block_masses, dtype=float)
    d = float(relative_precision)
    if v.shape != m.shape or v.ndim != 1 or v.size == 0:
        raise ValueError("aligned non-empty vectors required")
    if np.any(m <= 0) or not np.all(np.isfinite(m)):
        raise ValueError("positive finite masses required")
    if not (0.0 < d < 1.0):
        raise ValueError("relative precision must lie in (0,1)")
    exact = float((m * v).sum() / m.sum())
    # adversarial rounding: round the masses whose values lie above the mean up,
    # and those below the mean down, which pushes the merged value upward.
    signs = np.sign(v - exact)
    signs[signs == 0] = 1.0
    m_hat = m * (1.0 + d * signs)
    approx = float((m_hat * v).sum() / m_hat.sum())
    diameter = float(np.ptp(v))
    return {"exact": exact, "approx": approx,
            "error": abs(approx - exact),
            "bound": diameter * d / (1.0 - d),
            "diameter": diameter, "delta": d,
            "relative_mass_error": float(np.max(np.abs(m_hat - m) / m))}


def tree_merge_error(records, block_size, beta=1.0, rng=None):
    """Merge records exactly in random trees and report the deviation.

    records is a list of (value, score) pairs.  Returns the exact n-ary pair and
    the tree-merged pair, so the caller can measure the deviation.
    """
    beta = _beta(beta)
    if len(records) < 2:
        raise ValueError("at least two records required")
    if block_size < 1:
        raise ValueError("block size must be positive")
    if rng is None:
        rng = np.random.default_rng(0)
    n = len(records)
    order = rng.permutation(n)
    blocks = [order[i:i + block_size] for i in range(0, n, block_size)]
    summaries = []
    for b in blocks:
        M = float(sum(math.exp(beta * records[i][1]) for i in b))
        S = float(sum(math.exp(beta * records[i][1]) * records[i][0] for i in b))
        summaries.append([M, S])
    while len(summaries) > 1:
        nxt = []
        for i in range(0, len(summaries), 2):
            if i + 1 < len(summaries):
                nxt.append([summaries[i][0] + summaries[i + 1][0],
                            summaries[i][1] + summaries[i + 1][1]])
            else:
                nxt.append(summaries[i])
        summaries = nxt
    M, S = summaries[0]
    return {"tree_value": S / M, "tree_score": math.log(M) / beta,
            "blocks": len(blocks), "records": n}
