"""Unit tests for the OTAZ-III core (stdlib unittest, no fixtures required).

Run with:  python -m unittest discover -s tests -v
SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""
import math
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from otaz_quantum import core as C


class TestPrimitives(unittest.TestCase):
    def test_weights_match_softmax(self):
        w = np.array([0.3, -0.7, 1.1])
        x = np.exp(w)
        np.testing.assert_allclose(C.weights(w, 1.0), x / x.sum())

    def test_beta_scaling_is_not_invariance(self):
        w = np.array([1.0, 0.0])
        p1 = C.weights(w, 1.0)
        p2 = C.weights(w, 2.0)
        self.assertFalse(np.allclose(p1, p2))
        self.assertGreater(p2[0], p1[0])

    def test_beta_must_be_finite_nonzero(self):
        for bad in [0.0, float("nan"), float("inf")]:
            with self.assertRaises(ValueError):
                C.weights(np.array([1.0, 2.0]), bad)

    def test_shift_invariance(self):
        w = np.array([0.1, 0.9, -2.0])
        np.testing.assert_allclose(C.weights(w, 1.3), C.weights(w + 7.5, 1.3))

    def test_log_partition_matches_direct_sum(self):
        w = np.array([0.5, -0.5, 2.0])
        self.assertAlmostEqual(C.log_partition(w, 1.0), math.log(np.exp(w).sum()))

    def test_log_partition_is_shift_equivariant(self):
        w = np.array([0.5, -0.5, 2.0])
        self.assertAlmostEqual(C.log_partition(w + 3.0, 1.0),
                               C.log_partition(w, 1.0) + 3.0)

    def test_fuse_returns_pair(self):
        V, W = C.fuse(np.array([10.0, 20.0]), np.array([0.0, 0.0]), 1.0)
        self.assertAlmostEqual(float(V[0]), 15.0)
        self.assertAlmostEqual(W, math.log(2.0))

    def test_free_energy_is_minus_score(self):
        w = np.array([0.2, 1.4])
        self.assertAlmostEqual(C.free_energy(w, 2.0), -C.log_partition(w, 2.0) / 2.0)

    def test_masses_are_shift_stable(self):
        w = np.array([800.0, 801.0, 799.5])
        m = C.masses(w, 3.0)
        self.assertTrue(np.isfinite(m).all())
        np.testing.assert_allclose(m / m.sum(), C.weights(w, 3.0))


class TestTemperature(unittest.TestCase):
    def test_fluctuation_dissipation(self):
        rng = np.random.default_rng(0)
        w = rng.normal(size=5)
        v = rng.normal(size=(5, 2))
        cov, var = C.temperature_derivative(v, w, 1.4)
        p = C.weights(w, 1.4)
        manual = ((v - p @ v) * (w - p @ w)[:, None] * p[:, None]).sum(axis=0)
        np.testing.assert_allclose(cov, manual)
        self.assertGreaterEqual(var, 0.0)

    def test_heat_capacity_nonnegative(self):
        w = np.array([-1.0, 0.0, 2.0])
        self.assertGreaterEqual(C.heat_capacity(w, 0.7), 0.0)

    def test_log_partition_convex_in_beta(self):
        w = np.array([0.0, 1.0, 3.0])
        betas = np.linspace(0.2, 3.0, 40)
        vals = [C.log_partition(w, b) for b in betas]
        second = np.diff(vals, 2)
        self.assertTrue((second >= -1e-12).all())

    def test_self_scored_derivative_equals_variance(self):
        w = np.array([0.4, -1.2, 2.2])
        dV, var = C.temperature_derivative(w, w, 0.9)
        self.assertAlmostEqual(float(dV[0]), var, places=12)

    def test_cold_limit_selects_maximum(self):
        w = np.array([0.0, 1.0, 5.0])
        p = C.weights(w, 1e4)
        self.assertGreater(p[2], 1 - 1e-9)

    def test_hot_limit_selects_mean(self):
        w = np.array([0.0, 1.0, 5.0])
        p = C.weights(w, 1e-6)
        np.testing.assert_allclose(p, np.ones(3) / 3, atol=1e-6)


class TestRepresentability(unittest.TestCase):
    def test_exact_inverse(self):
        rng = np.random.default_rng(1)
        q = rng.dirichlet(np.ones(6))
        w = C.scores_for_distribution(q, 2.5)
        np.testing.assert_allclose(C.weights(w, 2.5), q, atol=1e-14)

    def test_rejects_zero_entries(self):
        with self.assertRaises(ValueError):
            C.scores_for_distribution(np.array([0.5, 0.0, 0.5]), 1.0)

    def test_rejects_unnormalised(self):
        with self.assertRaises(ValueError):
            C.scores_for_distribution(np.array([0.4, 0.4]), 1.0)

    def test_renormalised_logits_equal_softmax_of_log(self):
        a = np.array([0.2, 0.5, 0.3])
        beta = 3.0
        np.testing.assert_allclose(C.renormalised_logit_weights(a),
                                   C.weights(np.log(a) / beta, beta), atol=1e-14)

    def test_nonamplification_bound_monotone(self):
        vals = [C.nonamplification_bound(e) for e in (0.01, 0.1, 0.5)]
        self.assertTrue(all(x < y for x, y in zip(vals, vals[1:])))

    def test_nonamplification_bound_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            C.nonamplification_bound(1.0)
        with self.assertRaises(ValueError):
            C.nonamplification_bound(-0.1)


class TestCoarseGraining(unittest.TestCase):
    def test_gap_identity(self):
        rng = np.random.default_rng(2)
        w = rng.normal(size=9)
        blocks = np.array_split(np.arange(9), 3)
        cert = C.coarse_grain(w, blocks, 1.3)
        self.assertAlmostEqual(cert["gap"], cert["block_entropy"] / 1.3, places=12)
        self.assertLess(abs(cert["identity_residual"]), 1e-12)

    def test_gap_nonnegative_and_bounded(self):
        rng = np.random.default_rng(3)
        for _ in range(30):
            w = rng.normal(size=12)
            blocks = np.array_split(np.arange(12), 4)
            cert = C.coarse_grain(w, blocks, 0.8)
            self.assertGreaterEqual(cert["gap"], -1e-12)
            self.assertLessEqual(cert["gap"], math.log(4) / 0.8 + 1e-12)

    def test_single_block_gap_zero(self):
        w = np.array([1.0, -2.0, 0.5])
        cert = C.coarse_grain(w, [np.arange(3)], 1.0)
        self.assertAlmostEqual(cert["gap"], 0.0, places=12)

    def test_every_singleton_gap_is_entropy(self):
        rng = np.random.default_rng(4)
        w = rng.normal(size=7)
        beta = 1.7
        singles = [np.array([i]) for i in range(7)]
        cert = C.coarse_grain(w, singles, beta)
        p = C.weights(w, beta)
        self.assertAlmostEqual(cert["gap"], float(-(p * np.log(p)).sum()) / beta, places=12)

    def test_partition_validation(self):
        w = np.zeros(4)
        with self.assertRaises(ValueError):
            C.coarse_grain(w, [np.array([0, 1]), np.array([1, 2, 3])], 1.0)
        with self.assertRaises(ValueError):
            C.coarse_grain(w, [np.array([0, 1, 2])], 1.0)

    def test_chain_rule(self):
        rng = np.random.default_rng(5)
        w = rng.normal(size=16)
        idx = rng.permutation(16)
        coarse = np.array_split(idx, 4)
        fine = np.array_split(idx, 8)
        out = C.hierarchical_chain(w, coarse, fine, 1.1)
        self.assertLess(abs(out["chain_residual"]), 1e-12)

    def test_chain_requires_refinement(self):
        w = np.zeros(4)
        with self.assertRaises(ValueError):
            C.hierarchical_chain(w, [np.array([0, 1]), np.array([2, 3])],
                                 [np.array([0, 2]), np.array([1, 3])], 1.0)


class TestQuantum(unittest.TestCase):
    def test_diagonal_state_trace_distance_equals_tv(self):
        p = np.array([0.7, 0.2, 0.1])
        q = np.array([0.4, 0.5, 0.1])
        self.assertAlmostEqual(C.trace_distance(C.density_from_weights(p),
                                                C.density_from_weights(q)),
                               0.5 * np.abs(p - q).sum())

    def test_entropy_matches_shannon(self):
        p = np.array([0.2, 0.3, 0.5])
        self.assertAlmostEqual(C.von_neumann_entropy(C.density_from_weights(p)),
                               float(-(p * np.log(p)).sum()))

    def test_pure_orthogonal_states_distance_one(self):
        a = np.array([1.0, 0.0])
        b = np.array([0.0, 1.0])
        ra, rb = np.outer(a, a), np.outer(b, b)
        self.assertAlmostEqual(C.trace_distance(ra, rb), 1.0)

    def test_identical_diagonal_different_state(self):
        a = np.ones(4) / 2
        b = np.array([1.0, 1.0, -1.0, -1.0]) / 2
        ra, rb = np.outer(a, a), np.outer(b, b)
        np.testing.assert_allclose(np.diag(ra), np.diag(rb))
        self.assertAlmostEqual(C.trace_distance(ra, rb), 1.0)

    def test_dephasing_contracts(self):
        rng = np.random.default_rng(6)
        a = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
        b = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
        ra = a @ a.conj().T
        rb = b @ b.conj().T
        ra /= np.trace(ra)
        rb /= np.trace(rb)
        self.assertLessEqual(C.trace_distance(C.dephase(ra), C.dephase(rb)) + 1e-12,
                             C.trace_distance(ra, rb))

    def test_helstrom_identity(self):
        p = np.array([0.9, 0.1])
        q = np.array([0.2, 0.8])
        pe = C.helstrom_error(C.density_from_weights(p), C.density_from_weights(q))
        self.assertAlmostEqual(pe, 0.5 * (1 - 0.5 * np.abs(p - q).sum()))

    def test_helstrom_floor_nonnegative(self):
        for r in (0.0, 0.5, 3.0):
            self.assertGreaterEqual(C.helstrom_floor(r, 2.0), 0.0)

    def test_random_state_diagonal(self):
        rng = np.random.default_rng(7)
        d = np.array([0.4, 0.35, 0.25])
        rho = C.random_state_with_diagonal(d, rng)
        np.testing.assert_allclose(np.diag(rho).real, d, atol=1e-12)
        self.assertAlmostEqual(C.purity(rho), 1.0, places=10)


class TestSampling(unittest.TestCase):
    def test_counts_sum(self):
        rng = np.random.default_rng(8)
        p = np.array([0.2, 0.5, 0.3])
        c = C.sample_counts(p, 1000, rng)
        self.assertEqual(int(c.sum()), 1000)

    def test_sampling_experiment_certificate_holds(self):
        rng = np.random.default_rng(9)
        p = np.array([0.25, 0.25, 0.25, 0.25])
        v = np.array([0.0, 1.0, 2.0, 3.0])
        for shots in (50, 500):
            out = C.sampling_experiment(p, v, 1.0, shots, rng)
            self.assertLessEqual(out["value_error"], out["certificate_value"] + 1e-12)

    def test_rejects_zero_shots(self):
        with self.assertRaises(ValueError):
            C.sample_counts(np.array([0.5, 0.5]), 0, np.random.default_rng(0))


class TestBinaryAlgebra(unittest.TestCase):
    def test_pair_fuse_matches_nary_for_two(self):
        a = C.pair_fuse(1.0, 0.5, 3.0, 1.5, 1.0)
        b = C.nary_fuse([(1.0, 0.5), (3.0, 1.5)], 1.0)
        self.assertAlmostEqual(float(a["value"][0]), float(b["value"][0]), places=12)
        self.assertAlmostEqual(a["score"], b["score"], places=12)

    def test_commutative(self):
        left = C.pair_fuse(0.3, -1.2, 2.1, 0.4, 0.8)
        right = C.pair_fuse(2.1, 0.4, 0.3, -1.2, 0.8)
        self.assertAlmostEqual(float(left["value"][0]), float(right["value"][0]), places=12)
        self.assertAlmostEqual(left["score"], right["score"], places=12)

    def test_not_idempotent_offset_is_ln_two_over_beta(self):
        for beta in (0.5, 1.0, 4.0):
            out = C.pair_fuse(2.0, -0.4, 2.0, -0.4, beta)
            self.assertAlmostEqual(out["score"] - (-0.4), math.log(2) / beta, places=12)
            self.assertAlmostEqual(float(out["value"][0]), 2.0, places=12)

    def test_associativity_against_nary(self):
        rng = np.random.default_rng(11)
        for _ in range(20):
            recs = [(float(rng.normal()), float(rng.normal())) for _ in range(4)]
            left = C.chained_pair_fuse(recs, 1.7)
            full = C.nary_fuse(recs, 1.7)
            self.assertAlmostEqual(float(left["value"][0]), float(full["value"][0]), places=12)
            self.assertAlmostEqual(left["score"], full["score"], places=12)

    def test_not_homogeneous(self):
        scaled, expected = C.is_linear_in_first_argument(1.0, 0.5, 3.0, 1.5, 1.0, 2.0)
        self.assertGreater(abs(float(scaled[0] - expected[0])), 1e-3)

    def test_mass_monoid_representation(self):
        beta = 1.3
        recs = [(0.4, -0.2), (1.1, 0.9)]
        masses = np.array([math.exp(beta * w) for _, w in recs])
        expected_value = float((masses * np.array([v for v, _ in recs])).sum() / masses.sum())
        out = C.chained_pair_fuse(recs, beta)
        self.assertAlmostEqual(float(out["value"][0]), expected_value, places=12)
        self.assertAlmostEqual(out["score"], math.log(masses.sum()) / beta, places=12)



class TestLedger(unittest.TestCase):
    def test_reachable_set_is_the_hull(self):
        out = C.achievable_values([1.0, 4.0, 2.0])
        self.assertAlmostEqual(out["low"], 1.0)
        self.assertAlmostEqual(out["high"], 4.0)
        self.assertAlmostEqual(out["diameter"], 3.0)

    def test_minimax_is_the_midpoint(self):
        out = C.minimax_value([0.0, 10.0])
        self.assertAlmostEqual(out["estimate"], 5.0)
        self.assertAlmostEqual(out["worst_case_error"], 5.0)

    def test_blind_merge_uses_counts_only(self):
        self.assertAlmostEqual(C.ledger_blind_merge([0.0, 10.0]), 5.0)
        self.assertAlmostEqual(C.ledger_blind_merge([0.0, 10.0], counts=[3, 1]), 2.5)

    def test_same_summary_different_mass(self):
        m1 = sum(math.exp(0.0) for _ in range(2))
        m2 = sum(math.exp(3.0) for _ in range(2))
        g1 = (m1 * 5.0 + 1.0 * 0.0) / (m1 + 1.0)
        g2 = (m2 * 5.0 + 1.0 * 0.0) / (m2 + 1.0)
        self.assertGreater(abs(g1 - g2), 1.0)

    def test_quantised_merge_within_bound(self):
        rng = np.random.default_rng(21)
        for _ in range(50):
            k = int(rng.integers(2, 8))
            v = rng.normal(size=k)
            m = np.exp(rng.normal(size=k))
            out = C.quantised_merge(v, m, 0.1)
            self.assertLessEqual(out["error"], out["bound"] + 1e-12)

    def test_quantised_merge_rejects_bad_precision(self):
        with self.assertRaises(ValueError):
            C.quantised_merge(np.array([1.0, 2.0]), np.array([1.0, 1.0]), 0.0)
        with self.assertRaises(ValueError):
            C.quantised_merge(np.array([1.0, 2.0]), np.array([1.0, 1.0]), 1.0)

    def test_tree_merge_exact(self):
        rng = np.random.default_rng(22)
        recs = [(float(rng.normal()), float(rng.normal())) for _ in range(64)]
        out = C.tree_merge_error(recs, 5, 1.1, rng)
        vals = np.array([r[0] for r in recs])
        scores = np.array([r[1] for r in recs])
        V, W = C.fuse(vals, scores, 1.1)
        self.assertAlmostEqual(out["tree_value"], float(V[0]), places=9)
        self.assertAlmostEqual(out["tree_score"], float(W), places=9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
