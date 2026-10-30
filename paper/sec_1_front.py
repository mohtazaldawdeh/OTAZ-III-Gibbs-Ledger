# -*- coding: utf-8 -*-
"""Front matter, introduction and setting for the OTAZ-III manuscript.

SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""

TITLE = '''
<h1 class="title">OTAZ III: The Gibbs Ledger &mdash; Exact Aggregation, a Sharp
Impossibility Theorem, and Certified Error Budgets for Scored-Record Fusion</h1>
<p class="authors">Al-Mu'taz Billah Salah Al-Dawoodiya</p>
<p class="affil">Independent researcher &middot; Software developer, artificial intelligence and
computer science &middot; Amman, Jordan</p>
<p class="affil">Contact: mohtazaldawdeh@gmail.com</p>
<p class="affil">Preprint, prepared for deposit on Zenodo. Version 3.0.0, 28 October 2026.</p>
<p class="affil">Companion deposit: OTAZ &mdash; Exponentially Weighted Fusion,
<i>Algebraic Structure, Numerical Stability, and Reproducible Experiments</i>,
DOI 10.5281/zenodo.23648070.</p>
<p class="notice"><b>Status.</b> This document is a preprint. It has not been peer
reviewed, it has not been submitted to a journal, and no claim of acceptance or
review is made anywhere in it. A one-page novelty assessment accompanies the
deposit and states, item by item, what is classical, what is a repackaging, and
what is offered as new and checkable. All code, data and figures needed to
re-derive every number in the text are included in the accompanying repository
under the PolyForm Noncommercial 1.0.0 licence; the text is under CC BY-NC 4.0.</p>
'''

ABSTRACT = '''
<div class="abstract">
<p><span class="lbl">Abstract.</span> A scored record is a pair: a value and a
score. Fusing a collection of such records into one pair &mdash; a Gibbs-weighted
mean of the values together with a scaled log-sum-exp of the scores &mdash; is one
of the oldest operations in statistics and one of the most frequently re-derived
in engineering. This paper treats the pair as an accounting object and asks three
questions that the usual treatments leave implicit: what algebra the operation
has, what a distributed implementation must carry between shards, and what
guarantees survive when the inputs are estimated rather than known.</p>
<p>The algebra is settled first. The records form a commutative monoid whose
operation is associative but <i>not</i> idempotent &mdash; duplicating a record
adds exactly &beta;<sup>&minus;1</sup>ln&nbsp;2 to the score &mdash; and which is
not homogeneous in the values, so the operation is not the first slot of a
bilinear form. The binary rule generates the <i>n</i>-ary one, so aggregation is
order-independent, and the pair (mass, mass-weighted sum) is a sufficient
statistic, which makes tree-structured merging exact.</p>
<p>The distributed question is then answered negatively, and this is the central
contribution. If each shard reports only its value &mdash; however many records it
contains &mdash; the set of global values compatible with the reports is the whole
convex hull of the shard values, and no merge rule can do better, in the worst
case, than half the range of those values. The bound is sharp, the minimax rule is
the midpoint, and equal weighting is never better. Two datasets with identical
per-shard values and identical record counts can differ in their global value by
an amount proportional to the mass ratio the summary discarded; a worked example
gives a gap of 1.545 on a range of 10. If the masses are carried but rounded to
relative precision &delta;, the merged value is accurate to
<i>D</i>&delta;/(1&minus;&delta;) whatever the number of shards; both bounds are proved and
measured.</p>
<p>On the positive side I prove that block-wise evaluation of a pipeline loses
exactly &beta;<sup>&minus;1</sup> times the entropy of the block-mass
distribution, bounded by &beta;<sup>&minus;1</sup>ln&nbsp;<i>k</i> and attained by
equal masses; that the loss obeys a Shannon chain rule across levels; that the
logit parametrisation cannot amplify an <i>L</i><sub>1</sub> error of the weights;
and that sampling and truncation budgets compose into one certified interval which
held in all 300 random pipelines tried. A closing technical section fixes the
boundary of the quantum reading: the weight vector is the diagonal of a density
matrix, dephasing contracts the trace distance so the classical computation is a
lower bound, a Helstrom floor follows, and two orthogonal states with identical
diagonals show that no converse exists.</p>
<p>Sixteen seeded experiments, 52 unit tests and a 56-check independent verifier
support the text; the negative results, including a bootstrap that under-covers and
a certificate that saturates at small sample sizes, are reported in the main text
rather than in a footnote. The novelty assessment is deliberately conservative: the
ingredients are classical and their sources are named, and the one result offered
as new is the sharp impossibility statement for value-only summaries together with
its quantisation refinement.</p>
<p><span class="lbl">Index Terms.</span> Gibbs distribution, log-sum-exp, softmax,
fusion, mergeable summaries, distributed aggregation, minimax lower bound,
quantisation, entropy, certified error bounds, trace distance, dephasing,
reproducible research.</p>
</div>
'''

TOC = '''
<h2>Contents</h2>
<div class="toc">
<p>I. Introduction &nbsp;&middot;&nbsp; II. Setting, notation and related work
&nbsp;&middot;&nbsp; III. The algebra of scored-record fusion
&nbsp;&middot;&nbsp; IV. The ledger is necessary: an impossibility theorem and
its sharp constant &nbsp;&middot;&nbsp; V. Temperature as a control
&nbsp;&middot;&nbsp; VI. Coarse-graining accounting &nbsp;&middot;&nbsp;
VII. Certified error budgets for estimated weights &nbsp;&middot;&nbsp; VIII. The
quantum interface &nbsp;&middot;&nbsp; IX. Prior art and a conservative novelty
assessment &nbsp;&middot;&nbsp; X. Experiments and results &nbsp;&middot;&nbsp;
XI. Engineering implications &nbsp;&middot;&nbsp; XII. Limitations
&nbsp;&middot;&nbsp; XIII. Reproducibility &nbsp;&middot;&nbsp; XIV. Conclusion
&nbsp;&middot;&nbsp; Appendix A: proofs &nbsp;&middot;&nbsp; Appendix B: stored
scalars &nbsp;&middot;&nbsp; Appendix C: repository manifest &nbsp;&middot;&nbsp;
References</p>
</div>
'''

SEC_I = '''
<h2>I. Introduction</h2>

<h3>A. The object</h3>

<p>Most systems that produce a quantity also produce a claim about how much that
quantity should be trusted. A weather model emits a temperature and a verification
score; a learned ranker emits a probability and a calibration measure; a sensor
emits a reading and a signal-to-noise ratio; a Monte-Carlo estimator emits a sample
and a log-weight. When such records must be combined, the combination has to
respect both halves of the pair, and the classical answer is a Gibbs average:
exponentiate the scores, normalise, take the weighted mean of the values, and
report the scaled logarithm of the partition sum as the aggregate's own score.</p>

<div class="eq">
m<sub>i</sub> = e<sup>&beta;w<sub>i</sub></sup>, &nbsp;&nbsp;
p<sub>i</sub> = m<sub>i</sub>/Z, &nbsp;&nbsp; Z = &sum;<sub>i</sub> m<sub>i</sub>,
&nbsp;&nbsp; V = &sum;<sub>i</sub> p<sub>i</sub>v<sub>i</sub>, &nbsp;&nbsp;
W = &beta;<sup>&minus;1</sup>ln&nbsp;Z.
<span class="num">(1)</span>
</div>

<p>I call <i>m<sub>i</sub></i> the mass of record <i>i</i>, <i>Z</i> the partition
sum, <i>V</i> the fused value and <i>W</i> the fused score, and the triple
(<i>Z</i>, <i>V</i>, <i>W</i>) the <i>ledger</i> of an aggregate. The word is
deliberate. A ledger is not a summary of what happened; it is the set of numbers
one must keep in order to answer later questions exactly, and the difference between
those two things is the subject of Section IV.</p>

<p>The operation appears under many names: exponential weighting, logarithmic
pooling, log-mean-exp pooling, soft gating in a mixture of experts, Bayesian model
averaging over a finite model set, likelihood-ratio combination, the recursive
update of a particle filter, and the partition function of a Gibbs distribution with
a fixed sufficient statistic. Each community has re-derived the two-line algebra
above and each has, reasonably, stopped there, because the two lines are easy and
the applications are pressing. The cost of stopping there is that the interesting
questions are never asked. Three of them organise this paper.</p>

<h3>B. Three questions</h3>

<p><b>What algebra does the operation have?</b> Texts state that the fused score is
a log-sum-exp and the fused value a weighted mean, and then move on. But the
properties engineers rely on &mdash; may I merge in any order? may I merge two
partial results without revisiting the inputs? what happens if a record arrives
twice? &mdash; are algebraic properties, and they are not all visible in the
formula. Duplication is not neutral: a record that arrives twice is not the same as
a record that arrives once, because the partition sum counts it twice while the
value does not move, and the size of the effect is exactly
&beta;<sup>&minus;1</sup>ln&nbsp;2. Section III proves the algebra in full,
including the parts that fail.</p>

<p><b>What must a distributed implementation carry between shards?</b> This is the
question with the sharpest answer, and I regard it as the contribution of the
paper. The tempting interface is to send the value: each shard computes its own
fused value and reports it. The correct interface is to send the mass as well.
Section IV shows that the difference is not a matter of taste. With values alone,
the set of global values still compatible with the reports is the entire convex hull
of the reported values, so a merge rule can be wrong by half the range of those
values no matter how clever it is; the midpoint is minimax and attains that bound
exactly. Two datasets whose shards agree in value and in record count but differ in
mass can produce global values differing by 1.5452 on a range of 10 &mdash;
about a sixth of the range, from two datasets no value-only rule can tell apart. If the mass
is carried but quantised, the loss is <i>D</i>&delta;/(1&minus;&delta;), and that is
sharp too.</p>

<p><b>What survives when the inputs are estimated?</b> Production inputs are never
known: weights come from finitely many samples, some records are dropped for cost,
and some aggregates are computed block by block. Each introduces an error, and a
system that reports a number without an interval around it reports an illusion.
Sections VI and VII supply the three statements that make an interval possible: the
exact cost of coarse evaluation, an error non-amplification result for the logit
parametrisation, and a composition theorem that turns sampling and truncation into
one certified bound. Section VIII takes the last step and asks what the same
construction means when the weights come from a quantum device; the answer is
precise and one-directional.</p>

<h3>C. What this paper does not claim</h3>

<p>The mathematics is built from classical parts: the Gibbs variational principle,
the entropy bound, the pinching inequality, the Helstrom formula, elementary minimax
reasoning. Section IX lists the components against their sources in one table and
states, for each, whether it is classical, repackaged or offered as new. Exactly one
item is offered as new: the impossibility statement of Section IV with its sharp
constant and its quantisation refinement, in the setting of a fusion operator that
carries a score alongside a value. Even there, the <i>style</i> of argument is
standard minimax theory and the framing owes an obvious debt to the
mergeable-summaries literature; what I could not find is the statement itself for
this operator. The one-page novelty assessment that accompanies the deposit repeats
this in a form a reader can attack item by item.</p>

<p>Two conventions. A result is not called new unless a proof is given and the
nearest prior art is named. And no number appears in the text that is not produced
by the accompanying code from a stated seed and stored in a named file; when the
code and the prose disagree, the code wins and the prose is a bug.</p>

<h3>D. Contributions</h3>
<ol>
<li><b>Algebra.</b> The records form a commutative monoid, associative and exactly
mergeable, with an explicit two-number sufficient statistic; the operation is not
idempotent (duplication adds &beta;<sup>&minus;1</sup>ln&nbsp;2 exactly) and not
homogeneous, so it is not the first slot of a bilinear form (Theorems 1&ndash;2).</li>
<li><b>Impossibility.</b> Value-only summaries leave the merged value undetermined
on the full convex hull of the shard values (Theorem 3); every merge rule has
worst-case error at least half the range, and the midpoint attains it (Theorem 4); a
ledger rounded to relative precision &delta; merges to within
<i>D</i>&delta;/(1&minus;&delta;), independently of the number of shards, with the
constant not claimed sharp (Theorem 5).</li>
<li><b>Accounting.</b> Block-wise evaluation loses exactly
&beta;<sup>&minus;1</sup>&times;the entropy of the block masses, bounded by
&beta;<sup>&minus;1</sup>ln&nbsp;<i>k</i>, attained by equal masses, and obeying a
Shannon chain rule across levels (Theorems 7&ndash;8).</li>
<li><b>Certificates.</b> The logit parametrisation cannot amplify an
<i>L</i><sub>1</sub> error (Theorem 9), and sampling plus truncation compose into a
single certified interval (Theorem 10).</li>
<li><b>Quantum boundary.</b> The theory is the commuting special case; dephasing
contracts the trace distance so the classical computation is a lower bound
(Theorem 11), a Helstrom floor follows (Corollary 1), and two orthogonal states with
identical diagonals rule out a converse (Theorem 12).</li>
<li><b>Reproducibility.</b> Sixteen seeded experiments, 52 unit tests, a 56-check
verifier that does not import the library it checks, a checksum manifest and stored
results (Section XIII).</li>
</ol>
'''

SEC_II = '''
<h2>II. Setting, notation and related work</h2>

<h3>A. Notation</h3>

<p>A record is a pair (<i>v</i>, <i>w</i>) with value
<i>v</i> &isin; R<sup><i>d</i></sup> and score <i>w</i> &isin; R. The parameter
&beta; is a finite non-zero real; by convention &beta; &gt; 0 sharpens the weights
toward high scores and &beta; &lt; 0 toward low ones, and several statements below
fix a sign because an inequality reverses when &beta;<sup>&minus;1</sup> changes
sign. <i>D</i> is the diameter of the values under the norm in use. Total variation
is TV(<i>p</i>, <i>q</i>) = &frac12;&Vert;<i>p</i>&minus;<i>q</i>&Vert;<sub>1</sub>.
Trace distance is &frac12;&Vert;&rho;&minus;&sigma;&Vert;<sub>1</sub>; the two agree
for diagonal states.</p>

<h3>B. Numerical realisation</h3>

<p>Equation (1) must not be evaluated as printed. The exponentials overflow in
double precision for &beta;<i>w</i> beyond roughly 709 and underflow below roughly
&minus;745, and both failures are silent: the sum becomes zero or infinite and the
subsequent division produces a not-a-number that propagates without a warning in
most array libraries. The remedy is the max-shifted form
&beta;<sup>&minus;1</sup>(<i>c</i> + ln&sum;<sub><i>i</i></sub>e<sup>&beta;<i>w<sub>i</sub></i>&minus;<i>c</i></sup>)
with <i>c</i> = max<sub><i>i</i></sub>&beta;<i>w<sub>i</sub></i>, which leaves the
weights unchanged and shifts the score by the known amount
&beta;<sup>&minus;1</sup><i>c</i>. The shifted form is what the accompanying library
implements, and the test suite includes scores of order 800 so that a regression to
the naive form fails loudly. The error analysis of this primitive, including bounds
on the relative error of the result, is due to Blanchard, Higham and Higham [8]; the
one-pass streaming version to Milakov and Gimelshein [9].</p>

<p>The natural object for a distributed implementation is not the pair but the
triple (<i>Z</i>, <i>S</i>, <i>n</i>) with
<i>S</i> = &sum;<sub><i>i</i></sub><i>m<sub>i</sub>v<sub>i</sub></i>, because
<i>Z</i> and <i>S</i> are additive and the pair is recovered by division and
logarithm. Section III shows that this is forced rather than convenient; Section IV
shows what happens when an implementation drops <i>Z</i>.</p>

<h3>C. Where the object appears</h3>

<p><i>Forecast combination.</i> Combining predictive distributions under a
logarithmic score reduces to a score-weighted average whose weights are softmax in
the accumulated scores; the fifty-year review of Wang, Hyndman, Li and Kang [12]
documents both the practice and the strength of the equal-weight baseline, which is
why Section IV states its comparison against equal weighting specifically.</p>

<p><i>Mixtures and products of experts.</i> Soft gating computes
<i>g<sub>i</sub></i> = softmax(<i>s<sub>i</sub></i>) and returns
&sum;<sub><i>i</i></sub><i>g<sub>i</sub>e<sub>i</sub></i>(<i>x</i>) [20], which is
(1) with the gate logit in the role of the score. Product-of-experts models use the
same log-sum-exp arithmetic in the log domain [21], which is the same function read as
a smooth maximum [3].</p>

<p><i>Sequential Monte Carlo.</i> Particle filters carry log-weights and combine
them by exactly this recursion; the fused score is the estimated log-evidence [22].</p>

<p><i>Distributed estimation.</i> When devices cannot share raw data they share
summaries, and which summaries compose is the subject of the mergeable-summaries
literature [16, 17]; linear sketches are trivially mergeable. Section III shows that
the ledger is a linear sketch of the required kind, and Section IV shows that
anything smaller is not.</p>

<p><i>Quantum state estimation.</i> A weight vector is a diagonal density matrix,
and what a classical summary of a quantum state can certify is the
classical-versus-quantum question of Section VIII [4, 5, 6].</p>

<h3>D. Related theory</h3>

<p>Three bodies of work bound what this paper can claim. The
<i>exponential-family</i> literature establishes that the natural sufficient
statistic of a Gibbs family is additive and of fixed dimension [18], which is the
content of Theorem 1(v) and of the merge procedure. The <i>mergeability</i>
framework of Agarwal et al. [16], with the sketching literature [17] alongside,
formalises when a summary can be merged while
preserving an error and size guarantee, and proves both positive and negative
results for concrete summaries. <i>Communication-constrained minimax theory</i>
[19] gives lower bounds on estimation error as a function of a bit budget, via
metric entropy. The result of Section IV sits between the last two: the constraint
is not the number of bits but the <i>shape</i> of the summary, and because that shape
is so restrictive the bound is exact rather than order-optimal, with an explicit
attaining construction.</p>
'''
