# Abstract — OTAZ III: The Gibbs Ledger

A scored record is a pair: a value and a score. Fusing a collection of such records
into one pair — a Gibbs-weighted mean of the values together with a scaled
log-sum-exp of the scores — is one of the oldest operations in statistics and one of
the most frequently re-derived in engineering. This paper treats the pair as an
accounting object and asks three questions that the usual treatments leave
implicit: what algebra the operation has, what a distributed implementation must
carry between shards, and what guarantees survive when the inputs are estimated
rather than known.

The algebra is settled first. The records form a commutative monoid whose operation
is associative but not idempotent — duplicating a record adds exactly β⁻¹ ln 2 to the
score — and which is not homogeneous in the values, so the operation is not the
first slot of a bilinear form. The binary rule generates the n-ary one, so
aggregation is order-independent, and the pair (mass, mass-weighted sum) is a
sufficient statistic, which makes tree-structured merging exact.

The distributed question is then answered negatively, and this is the central
contribution. If each shard reports only its value — however many records it
contains — the set of global values compatible with the reports is the whole convex
hull of the shard values, and no merge rule can do better, in the worst case, than
half the range of those values. The bound is sharp, the minimax rule is the
midpoint, and equal weighting is never better. Two datasets with identical per-shard
values and identical record counts can differ in their global value by an amount
proportional to the mass ratio the summary discarded; a worked example gives a gap
of 1.545 on a range of 10. If the masses are carried but rounded to relative
precision δ, the merged value is accurate to Dδ/(1−δ) whatever the number of shards;
both bounds are proved and measured, and the quantisation constant is not claimed
sharp.

On the positive side I prove that block-wise evaluation of a pipeline loses exactly
β⁻¹ times the entropy of the block-mass distribution, bounded by β⁻¹ ln k and
attained by equal masses; that the loss obeys a Shannon chain rule across levels;
that the logit parametrisation cannot amplify an L1 error of the weights; and that
sampling and truncation budgets compose into one certified interval which held in
all 300 random pipelines tried. A closing technical section fixes the boundary of
the quantum reading: the weight vector is the diagonal of a density matrix,
dephasing contracts the trace distance so the classical computation is a lower
bound, a Helstrom floor follows, and two orthogonal states with identical diagonals
show that no converse exists.

Sixteen seeded experiments, 52 unit tests and a 56-check independent verifier
support the text; the negative results, including a bootstrap that under-covers and
a certificate that saturates at small sample sizes, are reported in the main text
rather than in a footnote. The novelty assessment is deliberately conservative: the
ingredients are classical and their sources are named, and the one result offered as
new is the sharp impossibility statement for value-only summaries together with its
quantisation refinement.
