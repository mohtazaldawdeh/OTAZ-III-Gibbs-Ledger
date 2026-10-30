"""OTAZ-III deterministic experiments. Scientific outputs contain no timings.
SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""
import json, sys, math, platform, hashlib, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from scipy.special import softmax, logsumexp
from scipy.stats import unitary_group

from otaz_quantum.core import (
    weights, log_partition, fuse, free_energy, temperature_derivative,
    score_derivative, heat_capacity, scores_for_distribution,
    renormalised_logit_weights, nonamplification_bound, coarse_grain,
    hierarchical_chain, density_from_weights, trace_distance,
    von_neumann_entropy, helstrom_error, helstrom_floor,
    random_state_with_diagonal, sample_counts, sampling_experiment, masses, dephase,
    pair_fuse, nary_fuse, chained_pair_fuse, is_linear_in_first_argument,
    achievable_values, minimax_value, ledger_blind_merge, quantised_merge, tree_merge_error,
)

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
RES.mkdir(exist_ok=True)
SEED = 2026110101


def dump(name, obj):
    (RES / name).write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def tv(p, q):
    return 0.5 * float(np.abs(np.asarray(p) - np.asarray(q)).sum())


# ------------------------------------------------------------------ E1
def representability():
    rng = np.random.default_rng(SEED)
    worst = 0.0
    n_trials = 400
    for _ in range(n_trials):
        n = int(rng.integers(2, 30))
        q = rng.dirichlet(np.ones(n))
        beta = float(rng.choice([-4.0, -0.5, 0.3, 1.0, 2.5]))
        w = scores_for_distribution(q, beta)
        worst = max(worst, float(np.max(np.abs(softmax(beta * w) - q))))
    # A single extreme case: nearly degenerate and nearly uniform.
    extreme = []
    for q in [np.array([0.999999, 1e-6]), np.array([0.5, 0.5]), np.array([1 / 3, 1 / 3, 1 / 3])]:
        w = scores_for_distribution(q, 2.0)
        extreme.append({"q": q.tolist(), "max_abs_error": float(np.max(np.abs(softmax(2.0 * w) - q)))})
    dump("e1_representability.json", [{
        "property": "softmax_exactly_represents_any_positive_simplex_point",
        "trials": n_trials,
        "max_abs_error": worst,
        "extreme_cases": extreme,
        "acceptance_le_1e-12": worst <= 1e-12,
    }])


# ------------------------------------------------------------------ E2
def temperature_calculus():
    rng = np.random.default_rng(SEED + 1)
    rows = []
    worst_v = worst_w = worst_h = 0.0
    h = 1e-6
    for beta in [0.2, 0.7, 1.5, 3.0, 6.0]:
        for _ in range(60):
            n = int(rng.integers(2, 12))
            d = int(rng.integers(1, 4))
            w = rng.normal(0, 1.5, n)
            v = rng.normal(0, 2, (n, d))
            Vp, _ = fuse(v, w, beta + h)
            Vm, _ = fuse(v, w, beta - h)
            numeric = (Vp - Vm) / (2 * h)
            analytic, var = temperature_derivative(v, w, beta)
            worst_v = max(worst_v, float(np.max(np.abs(numeric - analytic))))
            Wp = log_partition(w, beta + h) / (beta + h)
            Wm = log_partition(w, beta - h) / (beta - h)
            numeric_w = (Wp - Wm) / (2 * h)
            worst_w = max(worst_w, abs(numeric_w - score_derivative(w, beta)))
            lp = lambda b: log_partition(w, b)
            second = (lp(beta + 1e-4) - 2 * lp(beta) + lp(beta - 1e-4)) / 1e-8
            worst_h = max(worst_h, abs(second - heat_capacity(w, beta)))
    # self-scored monotonicity: v proportional to w gives dV/dbeta >= 0
    mono = []
    for beta in [0.1, 0.5, 2.0, 8.0]:
        w = np.array([-2.0, -0.5, 0.0, 1.0, 2.5])
        deriv, var = temperature_derivative(w, w, beta)
        mono.append({"beta": beta, "dV_dbeta_self_scored": float(deriv[0]),
                     "variance": var, "nonnegative": bool(deriv[0] >= -1e-12)})
    # shape of the self-scored sensitivity: monotone or with an interior maximum
    shape = []
    for label, w in [("symmetric", np.array([-2.0, -1.0, 0.0, 1.0, 2.0])),
                     ("skewed", np.array([0.0, 1.0, 2.0, 3.0, 10.0]))]:
        betas = np.logspace(-2, 2, 240)
        curve = [heat_capacity(w, b) for b in betas]
        diffs = np.diff(curve)
        changes = int(np.sum(np.diff(np.sign(diffs)) != 0))
        # third cumulant of w under p at beta = 1: the derivative of the variance
        b = 1.0
        x = b * w
        p = np.exp(x - x.max()); p /= p.sum()
        mu = float(p @ w)
        k3 = float((p * (w - mu) ** 3).sum())
        shape.append({"label": label, "scores": w.tolist(),
                      "curve_start": float(curve[0]), "curve_end": float(curve[-1]),
                      "curve_max": float(max(curve)),
                      "argmax_beta": float(betas[int(np.argmax(curve))]),
                      "sign_changes_of_derivative": changes,
                      "monotone_decreasing": bool(changes == 0),
                      "third_cumulant_at_beta_1": k3})
    dump("e2_temperature_calculus.json", [{
        "property": "fluctuation_dissipation_and_heat_capacity_identities",
        "finite_difference_step": h,
        "max_abs_error_dV_dbeta": worst_v,
        "max_abs_error_dW_dbeta": worst_w,
        "max_abs_error_heat_capacity": worst_h,
        "self_scored_monotonicity": mono,
        "all_identities_within_1e-4": bool(max(worst_v, worst_w, worst_h) <= 1e-4),
        "sensitivity_shape": shape,
    }])


# ------------------------------------------------------------------ E3
def coarse_graining():
    rng = np.random.default_rng(SEED + 2)
    worst_id = 0.0
    gaps, ratios = [], []
    bound_ok = True
    trials = 0
    for beta in [0.4, 1.0, 2.5, 5.0]:
        for _ in range(80):
            n = int(rng.integers(4, 40))
            w = rng.normal(0, 1.2, n)
            k = int(rng.integers(2, min(n, 9)))
            blocks = np.array_split(rng.permutation(n), k)
            cert = coarse_grain(w, blocks, beta)
            worst_id = max(worst_id, abs(cert["identity_residual"]))
            gaps.append(cert["gap"])
            ratios.append(cert["gap"] / cert["predicted_gap"])
            if cert["gap"] > cert["upper_bound_ln_blocks_over_beta"] + 1e-12:
                bound_ok = False
            trials += 1
    cert_eq = coarse_grain(np.zeros(12), np.array_split(np.arange(12), 3), 1.0)
    # reconstruction: the global score is recoverable from block masses alone
    w = np.array([0.7, -1.1, 2.0, 0.3, 1.4, -0.2])
    blocks = [np.array([0, 1, 2]), np.array([3, 4]), np.array([5])]
    c = coarse_grain(w, blocks, 2.0)
    recovered = math.log(sum(c["masses"])) / 2.0
    # sharpness: n equal blocks reproduce the bound ln(k)/beta with equality
    sharp = coarse_grain(np.zeros(8), np.array_split(np.arange(8), 8), 1.5)
    dump("e3_coarse_graining.json", [{
        "property": "gap_equals_block_entropy_over_beta_and_is_bounded_by_ln_k_over_beta",
        "trials": trials,
        "max_abs_identity_residual": worst_id,
        "mean_gap": float(np.mean(gaps)),
        "max_gap": float(np.max(gaps)),
        "min_ratio_gap_over_prediction": float(np.min(ratios)),
        "max_ratio_gap_over_prediction": float(np.max(ratios)),
        "bound_always_respected": bool(bound_ok),
        "equal_block_scores_gap": cert_eq["gap"],
        "equal_block_entropy": cert_eq["block_entropy"],
        "reconstruction_error": float(abs(recovered - c["W_global"])),
        "sharp_case_gap": sharp["gap"],
        "sharp_case_bound": sharp["upper_bound_ln_blocks_over_beta"],
        "sharp_case_attains_bound": bool(abs(sharp["gap"] - sharp["upper_bound_ln_blocks_over_beta"]) <= 1e-12),
        "identity_verified_le_1e-12": bool(worst_id <= 1e-12),
    }])


# ------------------------------------------------------------------ E4
def hierarchy_additivity():
    rng = np.random.default_rng(SEED + 3)
    worst = 0.0
    rows = []
    identity_err = 0.0
    for _ in range(60):
        n = 32
        beta = float(rng.choice([0.5, 1.5, 4.0]))
        w = rng.normal(0, 1.0, n)
        idx = rng.permutation(n)
        coarse = np.array_split(idx, 4)
        fine = np.array_split(idx, 8)
        chain = hierarchical_chain(w, coarse, fine, beta)
        worst = max(worst, abs(chain["chain_residual"]))
        singles = [np.array([i]) for i in range(n)]
        chain2 = hierarchical_chain(w, fine, singles, beta)
        identity_err = max(identity_err, abs(chain2["chain_residual"]))
        # the full gap down to singletons equals the Shannon entropy over beta
        full = coarse_grain(w, singles, beta)
        p = weights(w, beta)
        H = float(-(p * np.log(p)).sum())
        identity_err = max(identity_err, abs(full["gap"] - H / beta))
        rows.append({"beta": beta, "gap_coarse": chain["gap_coarse"],
                     "gap_fine": chain["gap_fine"],
                     "within": chain["weighted_within_gaps"],
                     "entropy_fine": full["block_entropy"]})
    dump("e4_hierarchy.json", [{
        "property": "shannon_chain_rule_governs_multi_level_coarse_graining",
        "trials": len(rows),
        "max_abs_chain_residual": worst,
        "max_abs_entropy_identity_residual": identity_err,
        "sample_rows": rows[:5],
        "chain_verified_le_1e-12": bool(worst <= 1e-12),
        "entropy_identity_verified_le_1e-12": bool(identity_err <= 1e-12),
    }])


# ------------------------------------------------------------------ E5
def quantum_boundary():
    rng = np.random.default_rng(SEED + 4)
    worst_diag = 0.0
    for _ in range(300):
        n = int(rng.integers(2, 8))
        beta = float(rng.choice([0.5, 1.0, 2.0, 4.0]))
        w = rng.normal(0, 1.0, n)
        delta = rng.normal(0, 0.4, n)
        p = softmax(beta * w)
        q = softmax(beta * (w + delta))
        d = trace_distance(density_from_weights(p), density_from_weights(q))
        bound = math.tanh(abs(beta) * float(np.ptp(delta)) / 4.0)
        worst_diag = max(worst_diag, d - bound)
    dists, lower_gap = [], []
    for _ in range(200):
        n = int(rng.integers(2, 7))
        p = rng.dirichlet(np.ones(n))
        rho = random_state_with_diagonal(p, rng)
        sigma = random_state_with_diagonal(p, rng)
        d = trace_distance(rho, sigma)
        dists.append(d)
        aff = float(np.sum(np.sqrt(np.diag(rho).real * np.diag(sigma).real)))
        lower_gap.append(float(d * d - (1.0 - aff ** 2)))
    phi = np.ones(4) / 2.0
    psi = np.array([1.0, 1.0, -1.0, -1.0]) / 2.0
    r_phi, r_psi = np.outer(phi, phi.conj()), np.outer(psi, psi.conj())
    dump("e5_quantum_boundary.json", [{
        "property": "diagonal_certificate_is_sharp_only_for_commuting_scores",
        "commuting_trials": 300,
        "max_bound_violation_commuting": float(worst_diag),
        "commuting_bound_respected": bool(worst_diag <= 1e-12),
        "coherent_trials": 200,
        "coherent_states_with_nonzero_distance": int(sum(1 for d in dists if d > 1e-9)),
        "coherent_mean_trace_distance": float(np.mean(dists)),
        "coherent_max_trace_distance": float(np.max(dists)),
        "min_TV_squared_minus_one_minus_affinity_squared": float(np.min(lower_gap)),
        "affinity_lower_bound_respected": bool(np.min(lower_gap) >= -1e-12),
        "bell_example": {
            "diagonal": [0.25, 0.25, 0.25, 0.25],
            "diagonals_identical": bool(np.allclose(np.diag(r_phi).real, np.diag(r_psi).real)),
            "trace_distance": trace_distance(r_phi, r_psi),
            "diagonal_only_prediction": 0.0,
        },
    }])


# ------------------------------------------------------------------ E6
def helstrom():
    rng = np.random.default_rng(SEED + 9)
    viol = 0
    rows = []
    for _ in range(400):
        n = int(rng.integers(2, 6))
        beta = float(rng.choice([0.5, 1.0, 3.0, 8.0]))
        w = rng.normal(0, 1.0, n)
        delta = rng.normal(0, 1.0, n)
        delta = delta - delta.mean()
        r = float(np.ptp(delta))
        if r < 1e-9:
            continue
        p = softmax(beta * w)
        q = softmax(beta * (w + delta))
        pe = 0.5 * (1.0 - trace_distance(density_from_weights(p), density_from_weights(q)))
        fl = helstrom_floor(r, beta)
        if pe < fl - 1e-12:
            viol += 1
        rows.append({"beta": beta, "range": r, "pe": pe, "floor": fl, "slack": pe - fl})
    by_beta = {}
    for r in rows:
        by_beta.setdefault(str(r["beta"]), []).append(r["slack"])
    dump("e6_helstrom.json", [{
        "property": "helstrom_error_of_score_perturbations_respects_tanh_floor",
        "cases": len(rows),
        "violations": viol,
        "min_slack": float(min(r["slack"] for r in rows)),
        "mean_slack_by_beta": {k: float(np.mean(v)) for k, v in by_beta.items()},
        "floor_is_attained_scale": "TV <= tanh(beta*range/4) => P_e >= (1 - tanh(beta*range/4))/2",
    }])


# ------------------------------------------------------------------ E7
def sampling():
    rng = np.random.default_rng(SEED + 5)
    rows, coverage = [], []
    viol = 0
    for beta in [1.0, 3.0]:
        n = 8
        p_true = rng.dirichlet(np.ones(n))
        values = rng.normal(0, 1, n)
        diameter = float(np.ptp(values))
        V_true, _ = fuse(values, np.log(p_true) / beta, beta)
        for shots in [10, 100, 1000, 10000]:
            errs, certs, l1s, hits = [], [], [], 0
            for _ in range(120):
                out = sampling_experiment(p_true, values, beta, shots, rng)
                errs.append(out["value_error"])
                cert = diameter * min(1.0, out["certificate_nonamplification"])
                certs.append(cert)
                l1s.append(out["l1_error"])
                if out["value_error"] > cert + 1e-12:
                    viol += 1
                counts = np.asarray(out["counts"], dtype=float)
                p_hat = (counts + 1.0) / (counts.sum() + n)
                boots = []
                for _b in range(200):
                    cb = rng.multinomial(int(counts.sum()), p_hat)
                    pb = (cb + 1.0) / (cb.sum() + n)
                    Vb, _ = fuse(values, np.log(pb) / beta, beta)
                    boots.append(float(Vb[0]))
                lo, hi = np.percentile(boots, [2.5, 97.5])
                if lo - 1e-12 <= float(V_true[0]) <= hi + 1e-12:
                    hits += 1
            coverage.append({"beta": beta, "shots": shots, "coverage_95_bootstrap": hits / 120.0})
            rows.append({"beta": beta, "shots": shots,
                         "mean_value_error": float(np.mean(errs)),
                         "p95_value_error": float(np.percentile(errs, 95)),
                         "mean_l1_error": float(np.mean(l1s)),
                         "mean_certificate": float(np.mean(certs)),
                         "median_certificate": float(np.median(certs)),
                         "replications": 120})
    dump("e7_sampling.json", [{
        "property": "finite_shot_budget_analytic_certificate_and_bootstrap_coverage",
        "rows": rows,
        "coverage": coverage,
        "certificate_violations": viol,
        "note": "at beta=3 with ten shots the L1 certificate saturates at 1 and carries no information",
    }])


# ------------------------------------------------------------------ E8
def entropies():
    rng = np.random.default_rng(SEED + 6)
    worst = 0.0
    rows = []
    for _ in range(200):
        n = int(rng.integers(2, 10))
        p = rng.dirichlet(np.ones(n) * 1.5)
        shannon = float(-(p * np.log(p)).sum())
        vn = von_neumann_entropy(density_from_weights(p))
        worst = max(worst, abs(shannon - vn))
        rows.append(shannon)
    # entropy bounds
    check_bounds = []
    for beta in [0.25, 1.0, 4.0]:
        w = np.array([1.0, 0.2, -0.7, -1.5])
        p = softmax(beta * w)
        check_bounds.append({"beta": beta, "n_eff": float(math.exp(-(p * np.log(p)).sum())),
                             "between_1_and_n": bool(1 - 1e-12 <= math.exp(-(p * np.log(p)).sum()) <= 4 + 1e-12)})
    dump("e8_entropies.json", [{
        "property": "von_neumann_equals_shannon_for_diagonal_states",
        "trials": 200,
        "max_abs_difference": worst,
        "effective_number_checks": check_bounds,
        "verified_le_1e-12": bool(worst <= 1e-12),
    }])


# ------------------------------------------------------------------ E9
def nonamplification():
    rng = np.random.default_rng(SEED + 7)
    worst = -1.0
    viol = 0
    for eps in [0.05, 0.2, 0.5, 0.8]:
        for _ in range(150):
            n = int(rng.integers(2, 9))
            p = rng.dirichlet(np.ones(n))
            d = rng.normal(0, 1, n)
            d = d - d.mean()
            d = d / np.abs(d).sum() * eps
            p_hat = np.clip(p + d, 0, None)
            if p_hat.sum() <= 0:
                continue
            achieved = tv(renormalised_logit_weights(p_hat), p)
            bound = nonamplification_bound(float(np.abs(p_hat - p).sum()))
            worst = max(worst, achieved - bound)
            if achieved > bound + 1e-12:
                viol += 1
    dump("e9_nonamplification.json", [{
        "property": "logit_parametrisation_does_not_amplify_estimation_error",
        "trials": 600,
        "max_excess_over_bound": float(worst),
        "violations": viol,
        "bound_formula": "TV <= eps/(1-eps) with eps = ||p_hat - p||_1",
    }])


# ------------------------------------------------------------------ E10
def pipeline_budget():
    rng = np.random.default_rng(SEED + 8)
    rows, viol = [], 0
    for _ in range(300):
        n = 16
        beta = float(rng.choice([1.0, 2.0, 4.0]))
        p_true = rng.dirichlet(np.ones(n))
        values = rng.normal(0, 1, n)
        diameter = float(np.ptp(values))
        shots = int(rng.choice([50, 200, 2000]))
        counts = rng.multinomial(shots, p_true)
        p_hat = (counts + 1.0) / (shots + n)
        eps = float(np.abs(p_hat - p_true).sum())
        order = np.argsort(-p_hat)
        k = max(1, n // 2)
        keep = order[:k]
        tau_hat = float(p_hat[order[k:]].sum())
        bound = diameter * min(1.0, tau_hat + eps / max(1e-15, 1.0 - eps))
        V_ref, _ = fuse(values, np.log(p_true) / beta, beta)
        V_pipe, _ = fuse(values[keep], np.log(p_hat[keep]) / beta, beta)
        err = float(np.linalg.norm(V_pipe - V_ref))
        rows.append({"error": err, "bound": bound, "shots": shots, "beta": beta})
        if err > bound + 1e-12:
            viol += 1
    errs = [r["error"] for r in rows]
    bounds = [r["bound"] for r in rows]
    ratio = [e / b for e, b in zip(errs, bounds) if b > 1e-12]
    dump("e10_pipeline.json", [{
        "property": "composed_certificate_for_sampling_plus_truncation",
        "trials": len(rows),
        "violations": viol,
        "mean_error": float(np.mean(errs)),
        "mean_bound": float(np.mean(bounds)),
        "p95_error": float(np.percentile(errs, 95)),
        "median_ratio_error_over_bound": float(np.median(ratio)),
        "max_ratio_error_over_bound": float(np.max(ratio)) if ratio else 0.0,
        "all_inside_certificate": bool(viol == 0),
        "bound_formula": "D * min(1, tau_hat + eps/(1-eps)) with eps = ||p_hat - p||_1",
    }])


def dephasing_contractivity():
    rng = np.random.default_rng(SEED + 10)
    viol = 0
    coh, diag_d = [], []
    for _ in range(300):
        n = int(rng.integers(2, 7))
        a = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        b = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        rho = a @ a.conj().T
        sigma = b @ b.conj().T
        rho = rho / np.trace(rho)
        sigma = sigma / np.trace(sigma)
        full = trace_distance(rho, sigma)
        diag = trace_distance(dephase(rho), dephase(sigma))
        coh.append(full - diag)
        diag_d.append(diag)
        if diag > full + 1e-12:
            viol += 1
    dump("e11_dephasing.json", [{
        "property": "dephasing_contracts_trace_distance_so_the_diagonal_gives_a_lower_bound",
        "trials": 300,
        "violations": viol,
        "mean_full_trace_distance": float(np.mean(coh) + np.mean(diag_d)),
        "mean_diagonal_component": float(np.mean(diag_d)),
        "mean_coherence_excess": float(np.mean(coh)),
        "min_slack": float(np.min(coh)),
        "contractivity_holds": bool(viol == 0),
    }])


def binary_algebra():
    """Algebra of the fusion rule: commutativity, associativity, idempotence, homogeneity."""
    rng = np.random.default_rng(SEED + 11)
    # 1) commutativity
    comm = 0.0
    for _ in range(200):
        va, vb = rng.normal(size=2)
        wa, wb = rng.normal(size=2)
        beta = float(rng.choice([0.5, 1.0, 2.5]))
        left = pair_fuse(va, wa, vb, wb, beta)
        right = pair_fuse(vb, wb, va, wa, beta)
        comm = max(comm, float(np.max(np.abs(left["value"] - right["value"]))),
                   abs(left["score"] - right["score"]))
    # 2) idempotence defect: A bowtie A adds ln(2)/beta to the score
    idem = []
    for beta in [0.5, 1.0, 3.0]:
        out = pair_fuse(2.0, -0.4, 2.0, -0.4, beta)
        idem.append({"beta": beta,
                     "value_change": float(out["value"][0] - 2.0),
                     "score_change": float(out["score"] - (-0.4)),
                     "predicted_score_change": math.log(2.0) / beta,
                     "defect": float(out["score"] - (-0.4) - math.log(2.0) / beta)})
    # 3) associativity of the score slot and failure of the value slot
    score_gap, value_gap = 0.0, 0.0
    worst_example = None
    for _ in range(300):
        triples = [(float(rng.normal()), float(rng.normal())) for _ in range(3)]
        beta = float(rng.choice([0.7, 1.0, 2.0]))
        left = chained_pair_fuse(triples, beta)
        right_out = nary_fuse(triples, beta)
        score_gap = max(score_gap, abs(left["score"] - right_out["score"]))
        vgap = float(np.max(np.abs(left["value"] - right_out["value"])))
        if vgap > value_gap:
            value_gap = vgap
            worst_example = {"records": triples, "beta": beta,
                             "left_fold_value": float(left["value"][0]),
                             "nary_value": float(right_out["value"][0]),
                             "difference": vgap}
    # 4) the score slot is genuinely associative for three items in both orders
    assoc_score = 0.0
    for _ in range(200):
        triples = [(float(rng.normal()), float(rng.normal())) for _ in range(3)]
        beta = 1.3
        ab = pair_fuse(triples[0][0], triples[0][1], triples[1][0], triples[1][1], beta)
        left = pair_fuse(ab["value"][0], ab["score"], triples[2][0], triples[2][1], beta)
        bc = pair_fuse(triples[1][0], triples[1][1], triples[2][0], triples[2][1], beta)
        right = pair_fuse(triples[0][0], triples[0][1], bc["value"][0], bc["score"], beta)
        assoc_score = max(assoc_score, abs(left["score"] - right["score"]))
    # 5) homogeneity failure: the bracket is not the first slot of a bilinear form
    scaled, expected = is_linear_in_first_argument(1.0, 0.5, 3.0, 1.5, 1.0, 2.0)
    hom_defect = float(abs(scaled[0] - expected[0]))
    # 6) equal-weight case: binary chaining coincides with the n-ary value
    equal = []
    for n in [2, 4, 8]:
        vals = [(float(v), 0.0) for v in rng.normal(size=n)]
        left = chained_pair_fuse(vals, 1.0)
        full = nary_fuse(vals, 1.0)
        equal.append({"n": n, "difference": float(np.max(np.abs(left["value"] - full["value"])))})
    dump("e13_binary_algebra.json", [{
        "property": "algebra_of_the_single_source_formula",
        "commutativity_max_defect": comm,
        "commutative": bool(comm <= 1e-12),
        "idempotence": idem,
        "score_slot_associative_max_gap_to_nary": score_gap,
        "score_slot_associative": bool(score_gap <= 1e-12),
        "value_slot_max_gap_to_nary": value_gap,
        "value_slot_associative": bool(value_gap <= 1e-12),
        "worst_associativity_example": worst_example,
        "score_slot_associative_under_both_orders": bool(assoc_score <= 1e-12),
        "homogeneity_defect": hom_defect,
        "homogeneous": bool(hom_defect <= 1e-12),
        "equal_weight_chaining": equal,
    }])


def worked_example():
    """The worked example that the source pages announce but do not contain.

    Five records: three model forecasts of the same quantity with validation
    scores, two cheap heuristics.  The table reports, for a grid of beta, the
    weights, the fused value, the score, the sensitivity and the effective
    number of records.
    """
    names = ["model_A", "model_B", "model_C", "heuristic_1", "heuristic_2"]
    values = np.array([10.4, 9.8, 11.7, 8.9, 12.6])
    scores = np.array([0.92, 0.86, 0.61, 0.35, 0.18])
    rows = []
    for beta in [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]:
        p = weights(scores, beta)
        V, W = fuse(values, scores, beta)
        dV, var = temperature_derivative(values, scores, beta)
        n_eff = float(math.exp(-(p * np.log(p)).sum()))
        rows.append({
            "beta": beta,
            "weights": [round(float(x), 6) for x in p],
            "fused_value": round(float(V[0]), 6),
            "score": round(float(W), 6),
            "sensitivity": round(float(dV[0]), 6),
            "effective_records": round(n_eff, 6),
        })
    base = rows[2]
    d_up = fuse(values, scores, 1.0 + 1e-3)
    d_dn = fuse(values, scores, 1.0 - 1e-3)
    numeric = float((d_up[0][0] - d_dn[0][0]) / 2e-3)
    dumped = {
        "property": "worked_example_and_finite_difference_check",
        "names": names,
        "values": values.tolist(),
        "scores": scores.tolist(),
        "rows": rows,
        "finite_difference_at_beta_1": numeric,
        "analytic_sensitivity_at_beta_1": base["sensitivity"],
        "finite_difference_gap": abs(numeric - base["sensitivity"]),
    }
    dump("e14_worked_example.json", [dumped])
    print(json.dumps(rows, indent=1))
    return dumped


def ledger_impossibility():
    """Section IV: value-only summaries cannot determine the merged value."""
    rng = np.random.default_rng(SEED + 12)
    # (a) the reachable set is the convex hull of the block values
    hull_rows = []
    for _ in range(200):
        k = int(rng.integers(2, 6))
        V = rng.normal(0, 2, k)
        lo, hi = float(V.min()), float(V.max())
        # sample admissible datasets: one record per block, arbitrary score
        reach = []
        for _ in range(200):
            w = rng.normal(0, 3, k)
            p = softmax(w)
            reach.append(float(p @ V))
        reach = np.array(reach)
        hull_rows.append({"k": k, "lo": lo, "hi": hi,
                          "sampled_min": float(reach.min()),
                          "sampled_max": float(reach.max()),
                          "inside_hull": bool(reach.min() >= lo - 1e-12 and reach.max() <= hi + 1e-12)})
    cover = float(np.mean([r["inside_hull"] for r in hull_rows]))
    max_gap = max(max(r["lo"] - r["sampled_min"], r["sampled_max"] - r["hi"]) for r in hull_rows)
    # (b) two datasets with the same ((V_B, n_B)) but different global value
    block_A = [(0.0, 0.0), (10.0, 0.0)]
    block_A2 = [(0.0, 3.0), (10.0, 3.0)]
    V_A = ledger_blind_merge([0.0, 10.0])
    pair = {
        "block_summary_A": {"value": 5.0, "count": 2, "mass": 2.0},
        "block_summary_A2": {"value": 5.0, "count": 2,
                             "mass": float(sum(math.exp(3.0) for _ in range(2)))},
        "same_value_and_count": True,
    }
    partner = [(0.0, 0.0)]
    glob1 = (pair["block_summary_A"]["mass"] * 5.0 + 1.0 * 0.0) / (pair["block_summary_A"]["mass"] + 1.0)
    glob2 = (pair["block_summary_A2"]["mass"] * 5.0 + 1.0 * 0.0) / (pair["block_summary_A2"]["mass"] + 1.0)
    # (c) minimax rule and its exact worst case, versus a mass-blind merge
    minimax_rows = []
    for _ in range(300):
        k = int(rng.integers(2, 7))
        V = rng.normal(0, 3, k)
        mm = minimax_value(V)
        blind = ledger_blind_merge(V)
        # adversarial masses place all weight on the block that hurts the rule most
        p_far = np.zeros(k); p_far[int(np.argmax(V)) if blind < mm["estimate"] else int(np.argmin(V))] = 1.0
        worst_blind = max(abs(blind - lo) for lo in (V.min(), V.max()))
        worst_mm = max(abs(mm["estimate"] - lo) for lo in (V.min(), V.max()))
        minimax_rows.append({"k": k, "range": float(V.max() - V.min()),
                             "minimax_worst_case": float(mm["worst_case_error"]),
                             "achieved_worst_case": float(worst_mm),
                             "blind_equal_weight_worst_case": float(worst_blind)})
    max_dev = max(abs(r["minimax_worst_case"] - r["achieved_worst_case"]) for r in minimax_rows)
    ratio = [r["blind_equal_weight_worst_case"] / r["minimax_worst_case"]
             for r in minimax_rows if r["minimax_worst_case"] > 1e-12]
    dump("e12_impossibility.json", [{
        "property": "value_only_summaries_leave_the_merged_value_undetermined",
        "hull_trials": len(hull_rows),
        "fraction_inside_hull": cover,
        "max_hull_violation": float(max_gap),
        "reachable_set_is_interval": bool(cover == 1.0 and max_gap <= 1e-12),
        "same_summary_different_dataset": {
            "example": pair,
            "global_value_with_A": float(glob1),
            "global_value_with_A2": float(glob2),
            "difference": float(abs(glob1 - glob2)),
        },
        "minimax_trials": len(minimax_rows),
        "max_deviation_from_half_range": float(max_dev),
        "minimax_bound_attained": bool(max_dev <= 1e-12),
        "mean_ratio_blind_over_minimax": float(np.mean(ratio)),
        "min_ratio_blind_over_minimax": float(np.min(ratio)),
        "max_ratio_blind_over_minimax": float(np.max(ratio)),
    }])


def quantisation():
    """Section IV: masses known only to relative precision delta."""
    rng = np.random.default_rng(SEED + 13)
    rows = []
    viol = 0
    for delta in [0.01, 0.05, 0.1, 0.25]:
        errs, bounds, ratios = [], [], []
        for _ in range(150):
            k = int(rng.integers(2, 9))
            v = rng.normal(0, 1, k)
            m = np.exp(rng.normal(0, 2, k))
            out = quantised_merge(v, m, delta)
            errs.append(out["error"])
            bounds.append(out["bound"])
            ratios.append(out["error"] / out["bound"])
            if out["error"] > out["bound"] + 1e-12:
                viol += 1
        rows.append({"delta": delta, "trials": 150,
                     "mean_error": float(np.mean(errs)),
                     "mean_bound": float(np.mean(bounds)),
                     "max_ratio_error_over_bound": float(np.max(ratios)),
                     "median_ratio": float(np.median(ratios))})
    # relative error of the total mass is preserved under summation in a tree
    chain = []
    m = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
    for delta in (0.01, 0.1):
        signs = np.array([1, -1, 1, -1, 1, -1, 1, -1], dtype=float)
        cur = m * (1.0 + delta * signs)
        while len(cur) > 1:
            cur = np.array([cur[i] + cur[i + 1] for i in range(0, len(cur), 2)])
        total = float(cur[0])
        chain.append({"delta": delta, "rounded_total": total,
                      "true_total": float(m.sum()),
                      "relative_error": abs(total - float(m.sum())) / float(m.sum()),
                      "within_delta": bool(abs(total - float(m.sum())) / float(m.sum()) <= delta + 1e-15)})
    dump("e15_quantisation.json", [{
        "property": "relative_precision_delta_bounds_the_merge_error_by_D_delta_over_one_minus_delta",
        "rows": rows,
        "violations": viol,
        "bound_holds": bool(viol == 0),
        "summation_chain": chain,
        "note": "the bound is a worst case over admissible roundings and is not attained by the adversarial construction used here",
    }])


def tree_merge():
    """Section III/IX: exactness and cost of merging in arbitrary trees."""
    rng = np.random.default_rng(SEED + 14)
    rows = []
    for n in [100, 1000, 10000]:
        for block_size in [1, 10, 100]:
            vals = rng.normal(10, 3, n)
            scores = rng.normal(0, 1.5, n)
            recs = list(zip(vals.tolist(), scores.tolist()))
            out = tree_merge_error(recs, block_size, 1.3, rng)
            V_ref, W_ref = fuse(vals, scores, 1.3)
            rows.append({
                "records": n, "block_size": block_size,
                "blocks": out["blocks"],
                "value_gap": abs(out["tree_value"] - float(V_ref[0])),
                "score_gap": abs(out["tree_score"] - float(W_ref)),
                "value_gap_relative": abs(out["tree_value"] - float(V_ref[0])) / max(1e-12, abs(float(V_ref[0]))),
            })
    worst = max(r["value_gap_relative"] for r in rows)
    dump("e16_tree_merge.json", [{
        "property": "tree_merged_aggregates_equal_the_n_ary_aggregate",
        "configurations": len(rows),
        "max_relative_value_gap": float(worst),
        "max_absolute_value_gap": float(max(r["value_gap"] for r in rows)),
        "max_score_gap": float(max(r["score_gap"] for r in rows)),
        "exact_to_double_precision": bool(worst <= 1e-12),
        "rows": rows,
    }])


def run_all():
    t0 = time.process_time()
    representability(); temperature_calculus(); coarse_graining(); hierarchy_additivity()
    quantum_boundary(); helstrom(); sampling(); entropies(); nonamplification()
    pipeline_budget(); dephasing_contractivity(); binary_algebra()
    worked_example(); ledger_impossibility(); quantisation(); tree_merge()
    (RES / "environment.json").write_text(json.dumps({
        "python": platform.python_version(), "numpy": np.__version__,
        "platform": platform.platform(), "seed": SEED,
        "process_cpu_seconds_not_scientific": round(time.process_time() - t0, 3),
    }, indent=2) + "\n")
    files = sorted(p for p in ROOT.rglob("*") if p.is_file()
                   and "results" not in p.parts and "__pycache__" not in p.parts
                   and p.suffix in {".py", ".txt", ".md"})
    (RES / "source_hashes.json").write_text(json.dumps(
        {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        indent=2, sort_keys=True) + "\n")
    print("wrote", len(list(RES.glob("*.json"))), "JSON files")


if __name__ == "__main__":
    run_all()
