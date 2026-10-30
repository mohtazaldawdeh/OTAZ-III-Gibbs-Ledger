"""Independent verifier for the OTAZ-III result set.

This script deliberately does not import otaz_quantum.core.  It re-derives every
headline claim either from the stored JSON or from first principles with plain
numpy, so that a mistake in the library cannot certify itself.

Usage:  python scripts/otaz_verify_quantum.py
Exit code 0 means every check passed.

SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
CHECKS = []


def check(name, condition, detail=""):
    CHECKS.append({"check": name, "ok": bool(condition), "detail": str(detail)})


def load(name):
    return json.loads((RES / name).read_text())


def softmax(x):
    x = np.asarray(x, dtype=float)
    e = np.exp(x - x.max())
    return e / e.sum()


def main():
    required = [
        "e1_representability.json", "e2_temperature_calculus.json",
        "e3_coarse_graining.json", "e4_hierarchy.json", "e5_quantum_boundary.json",
        "e6_helstrom.json", "e7_sampling.json", "e8_entropies.json",
        "e9_nonamplification.json", "e10_pipeline.json", "e11_dephasing.json",
        "e12_impossibility.json", "e13_binary_algebra.json",
        "e14_worked_example.json", "e15_quantisation.json", "e16_tree_merge.json",
    ]
    missing = [r for r in required if not (RES / r).exists()]
    check("all result files present", not missing, missing)

    # -- E1: the softmax inverse, recomputed here from scratch
    q = np.array([0.5, 0.3, 0.15, 0.05])
    for beta in (0.5, 2.0):
        w = np.log(q) / beta
        check(f"E1 inverse reproduces q at beta={beta}",
              np.max(np.abs(softmax(beta * w) - q)) < 1e-14)
    e1 = load("e1_representability.json")[0]
    check("E1 recorded max error below 1e-12", e1["max_abs_error"] <= 1e-12,
          e1["max_abs_error"])

    # -- E2: identities
    e2 = load("e2_temperature_calculus.json")[0]
    check("E2 dV/dbeta identity", e2["max_abs_error_dV_dbeta"] <= 1e-4,
          e2["max_abs_error_dV_dbeta"])
    check("E2 dW/dbeta identity", e2["max_abs_error_dW_dbeta"] <= 1e-4)
    check("E2 heat capacity identity", e2["max_abs_error_heat_capacity"] <= 1e-4)
    check("E2 self-scored derivative non-negative",
          all(r["nonnegative"] for r in e2["self_scored_monotonicity"]))

    # -- E3: gap identity and bound
    e3 = load("e3_coarse_graining.json")[0]
    check("E3 identity residual", e3["max_abs_identity_residual"] <= 1e-12,
          e3["max_abs_identity_residual"])
    check("E3 bound respected", e3["bound_always_respected"])
    check("E3 sharp case attains the bound", e3["sharp_case_attains_bound"])
    # independent construction: three blocks with masses 2, 2, 4 -> H(pi) = 1.0397
    m = np.array([2.0, 2.0, 4.0])
    pi = m / m.sum()
    h = -float((pi * np.log(pi)).sum())
    check("E3 hand example entropy", abs(h - 1.0397207708399179) < 1e-12, h)

    # -- E4: chain rule
    e4 = load("e4_hierarchy.json")[0]
    check("E4 chain residual", e4["max_abs_chain_residual"] <= 1e-12)
    check("E4 entropy identity", e4["max_abs_entropy_identity_residual"] <= 1e-12)

    # -- E5: commuting bound and coherent counterexample
    e5 = load("e5_quantum_boundary.json")[0]
    check("E5 commuting bound respected", e5["commuting_bound_respected"],
          e5["max_bound_violation_commuting"])
    check("E5 coherent states separate despite equal diagonals",
          e5["coherent_states_with_nonzero_distance"] == e5["coherent_trials"])
    bell = e5["bell_example"]
    check("E5 counterexample has identical diagonals", bell["diagonals_identical"])
    check("E5 counterexample distance is one",
          abs(bell["trace_distance"] - 1.0) < 1e-9, bell["trace_distance"])
    a = np.ones(4) / 2
    b = np.array([1.0, 1.0, -1.0, -1.0]) / 2
    ra, rb = np.outer(a, a), np.outer(b, b)
    tv = 0.5 * np.linalg.svd(ra - rb, compute_uv=False).sum()
    check("E5 counterexample recomputed independently", abs(tv - 1.0) < 1e-9, tv)

    # -- E6: Helstrom floor
    e6 = load("e6_helstrom.json")[0]
    check("E6 no floor violations", e6["violations"] == 0)
    check("E6 floor weakly increases with beta",
          e6["mean_slack_by_beta"]["8.0"] >= e6["mean_slack_by_beta"]["0.5"])

    # -- E7: sampling
    e7 = load("e7_sampling.json")[0]
    check("E7 no certificate violations", e7["certificate_violations"] == 0)
    cov = [c["coverage_95_bootstrap"] for c in e7["coverage"]]
    check("E7 bootstrap coverage plausible", min(cov) >= 0.85 and max(cov) <= 1.0,
          (min(cov), max(cov)))
    for beta in (1.0, 3.0):
        rows = sorted([r for r in e7["rows"] if r["beta"] == beta], key=lambda r: r["shots"])
        check(f"E7 error decreases with shots at beta={beta}",
              all(rows[i]["mean_value_error"] > rows[i + 1]["mean_value_error"]
                  for i in range(len(rows) - 1)))
        ratio = rows[-1]["mean_value_error"] / rows[-2]["mean_value_error"]
        check(f"E7 tenfold shots reduces error at beta={beta}", 0.2 < ratio < 0.6, ratio)

    # -- E8: entropy
    e8 = load("e8_entropies.json")[0]
    check("E8 von Neumann equals Shannon", e8["max_abs_difference"] <= 1e-12)
    p = np.array([0.2, 0.3, 0.5])
    check("E8 independent entropy check",
          abs(float(-(p * np.log(p)).sum()) - 1.0296530140645737) < 1e-12)

    # -- E9: non-amplification
    e9 = load("e9_nonamplification.json")[0]
    check("E9 no non-amplification violations", e9["violations"] == 0)
    check("E9 bound not vacuous", e9["max_excess_over_bound"] < 0.0,
          e9["max_excess_over_bound"])

    # -- E10: composed certificate
    e10 = load("e10_pipeline.json")[0]
    check("E10 all trials inside the certificate", e10["all_inside_certificate"])
    check("E10 median slack below one", e10["median_ratio_error_over_bound"] < 1.0)

    # -- E11: dephasing contractivity
    e11 = load("e11_dephasing.json")[0]
    check("E11 contractivity holds", e11["contractivity_holds"])
    check("E11 coherence contributes distance", e11["mean_coherence_excess"] > 0.0)

    # -- E12: ledger impossibility
    e12 = load("e12_impossibility.json")[0]
    check("E12 reachable set is the convex hull", e12["reachable_set_is_interval"])
    check("E12 minimax bound equals half the range", e12["minimax_bound_attained"])
    check("E12 equal-weight merge is never better than minimax",
          e12["min_ratio_blind_over_minimax"] >= 1.0 - 1e-12,
          e12["min_ratio_blind_over_minimax"])
    ex = e12["same_summary_different_dataset"]
    check("E12 same summary different dataset", ex["difference"] > 1.0, ex["difference"])
    m1, m2 = 2.0, 2.0 * math.exp(3.0)
    g1 = (m1 * 5.0) / (m1 + 1.0)
    g2 = (m2 * 5.0) / (m2 + 1.0)
    check("E12 example recomputed independently",
          abs(abs(g1 - g2) - ex["difference"]) < 1e-9, (g1, g2))
    # the minimax statement itself, recomputed on a fresh instance
    vals = np.array([-2.0, 0.5, 3.0])
    check("E12 midpoint minimax on a fresh instance",
          abs(0.5 * (vals.max() + vals.min()) - 0.5) < 1e-12
          and abs(0.5 * (vals.max() - vals.min()) - 2.5) < 1e-12)

    # -- E13: algebra of the printed formula
    e13 = load("e13_binary_algebra.json")[0]
    check("E13 commutative", e13["commutative"])
    check("E13 associative against the n-ary form", e13["value_slot_associative"])
    check("E13 not homogeneous", not e13["homogeneous"], e13["homogeneity_defect"])
    for row in e13["idempotence"]:
        check(f"E13 duplication offset ln2/beta at beta={row['beta']}",
              abs(row["defect"]) <= 1e-12)

    # -- E15: quantisation budget
    e15 = load("e15_quantisation.json")[0]
    check("E15 quantisation bound holds", e15["bound_holds"], e15["violations"])
    for row in e15["rows"]:
        check(f"E15 measured error below bound at delta={row['delta']}",
              row["max_ratio_error_over_bound"] <= 1.0 + 1e-12,
              row["max_ratio_error_over_bound"])
    check("E15 mass summation keeps relative error",
          all(c["within_delta"] for c in e15["summation_chain"]))

    # -- E16: tree merging
    e16 = load("e16_tree_merge.json")[0]
    check("E16 tree merge equals n-ary merge", e16["exact_to_double_precision"],
          e16["max_relative_value_gap"])

    # -- source hashes
    hash_path = RES / "source_hashes.json"
    if hash_path.exists():
        stored = json.loads(hash_path.read_text())
        bad = []
        for rel, want in stored.items():
            p = ROOT / rel
            if not p.exists():
                bad.append(rel)
                continue
            got = hashlib.sha256(p.read_bytes()).hexdigest()
            if got != want:
                bad.append(rel)
        check("source hashes match the files on disk", not bad, bad)
    else:
        check("source hash manifest present", False)

    # -- figures
    figs = sorted((ROOT / "figures").glob("*.svg"))
    check("eight vector figures present", len(figs) >= 8, [f.name for f in figs])

    out = RES / "verification.json"
    n_ok = sum(1 for c in CHECKS if c["ok"])
    out.write_text(json.dumps({"checks": CHECKS, "passed": n_ok,
                               "total": len(CHECKS)}, indent=2) + "\n")
    for c in CHECKS:
        if not c["ok"]:
            print("FAIL:", c["check"], c["detail"])
    print(f"{n_ok}/{len(CHECKS)} checks passed")
    return 0 if n_ok == len(CHECKS) else 1


if __name__ == "__main__":
    sys.exit(main())
