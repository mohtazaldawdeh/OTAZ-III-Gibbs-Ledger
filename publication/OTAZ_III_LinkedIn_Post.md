# LinkedIn post — OTAZ III (English)

One post, one image. Attach **`OTAZ_III_Social_Card.png`** (square, 1200 × 1200,
black and white). The wide card `OTAZ_III_Social_Card_wide.png` is the fallback for
link previews and for slides.

**Before posting**, replace `ZENODO-LINK` in the text with the deposit URL. Do not
invent a DOI: post the reserved Zenodo record URL, or wait until the record exists.
Nothing in the text claims peer review.

---

## The post (copy from here)

A merge rule that sees only the *number* and not the *mass* behind it is not
slightly under-specified. It is undetermined by half the range of the numbers
themselves — and I can prove it, and measure it.

The object is one of the most re-derived operations in engineering: a
Gibbs-weighted mean of values,

  V = Σ pᵢvᵢ,  pᵢ = e^(βwᵢ)/Z,  W = β⁻¹ ln Z

a softmax over scores normalising an average of values, carried with its scaled
log-partition sum. Recommenders, ensemble forecasters, mixture-of-experts gates,
particle filters, sharded dashboards — all of them merge this pair.

Here is the new theorem. Suppose each shard reports only its fused value, however
many records it holds. Then the set of global values still compatible with those
reports is the *whole convex hull* of the shard values:

  V ∈ conv{V₁, …, V_k}

and therefore no merge rule can promise, in the worst case, better than

  err ≥ ½ ( maxⱼ Vⱼ − minⱼ Vⱼ ).

The bound is attained, the minimax rule is the midpoint, and equal weighting never
beats it — on 300 random instances it was worse by up to 1.46×. Two datasets with
identical per-shard values and identical record counts can disagree by 1.545 on a
range of 10. The information that decides the merge is exactly the information a
value-only summary threw away, and no post-hoc calibration can put it back.

The positive side is just as sharp. Carry the mass and the error is zero, in any
tree, at any shard count. Carry it quantised to relative precision δ and the error
is

  |Ṽ − V| ≤ D δ/(1 − δ),

independent of how many shards you have — proved, and measured on 600 random
instances (worst observed ratio to the bound: 0.31, so I do not claim the constant
is sharp).

Around that result the paper does the accounting properly: the algebra (a
commutative monoid; a duplicate record adds exactly β⁻¹ln2; not homogeneous, so not
a bilinear form), the temperature calculus (dV/dβ = Cov(v,w), d²lnZ/dβ² = Var(w)),
a block-wise loss equal to β⁻¹ × an entropy with its Shannon chain rule, a
certified sampling budget, and the exact boundary of the "quantum" reading —
dephasing contracts trace distance, so the classical computation is only a lower
bound, and two orthogonal states with identical diagonals kill any converse.

Evidence, because a theorem you cannot run is a rumour: 12 theorems, 2 lemmas, 1
corollary; 16 seeded experiments writing 19 result files from a single seed
(2026110101); 52 unit tests; 56 independent checks that do not import the code they
check. The negative results are in the main text, not in a footnote — a bootstrap
that under-covers, a certificate that saturates at low sample counts, a bound that
is proved but not attained.

A one-page Arabic assessment (تقييم الجدة) accompanies the deposit and classifies
every statement against the literature: one claim offered as new, two repackagings,
the rest classical and cited. No priority is claimed for the classical parts.

No peer review. No invented DOI. No quantum speed-up.

Full text, code, figures, results and the assessment in one deposit:
ZENODO-LINK

#Research #Reproducibility #DistributedSystems #InformationTheory
#MachineLearning #OTAZ

---

## Shorter alternative (if you prefer a two-paragraph post)

If a shard reports only its value and not the normalising mass, the answers still
compatible with that report are the entire convex hull of the shard values — so no
merge rule can beat half the range in the worst case, and the midpoint attains it.
Carry the mass and the error is zero; quantise it to precision δ and the error is
Dδ/(1−δ) for any number of shards. That is the centre of my new preprint *OTAZ III:
The Gibbs Ledger*, with the algebra, the temperature calculus and the certified
error budgets around it: 16 seeded experiments, 52 tests, 56 independent checks,
negative results in the text.

Full text and data: ZENODO-LINK

#Research #Reproducibility #DistributedSystems #OTAZ

---

## Posting checklist

1. Reserve the Zenodo record, then copy its URL into both `ZENODO-LINK` slots.
2. Attach `OTAZ_III_Social_Card.png`; alt text: *"OTAZ III social card: value-only
   merging leaves the answer anywhere in the convex hull; the worst case is half
   the range."*
3. Do not add a DOI in the comment before it exists, and do not describe the work
   as reviewed or accepted.
4. If someone asks for the code, point them to the deposit ZIP `OTAZ_III.zip`,
   which is attached to the Zenodo record — not to a repository URL that does not
   exist yet.
