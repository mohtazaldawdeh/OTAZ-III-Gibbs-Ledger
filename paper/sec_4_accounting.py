# -*- coding: utf-8 -*-
"""Sections V-VII: temperature, coarse-graining accounting, certified budgets."""

SEC_V = '''
<h2>V. Temperature as a control</h2>

<p>Every practitioner who has fitted a softmax has met &beta; under a different name:
inverse temperature, sharpening parameter, scale, gain, logit multiplier. It is
usually tuned by hand or by a grid search and then left alone. In the ledger the
parameter cannot be left alone, because it appears in both slots: the value it
produces is not a diagnostic but the input to the next merge, and the score it
produces is what a downstream consumer thresholds. This section gives the calculus
that makes &beta; a design variable with predictable consequences.</p>

<div class="thm">
<p><span class="t">Theorem 6 (temperature calculus).</span></p>
<div class="body">
<p>Fix values <i>v</i> and scores <i>w</i>. For finite non-zero &beta;, with
<i>p</i>, <i>V</i> and <i>Z</i> as in (1) and (3):</p>
<p>(i) d<i>V</i>/d&beta; = Cov<sub><i>p</i></sub>(<i>v</i>, <i>w</i>),
coordinate-wise;</p>
<p>(ii) d<i>W</i>/d&beta; = (&sum;<sub><i>i</i></sub><i>p<sub>i</sub>w<sub>i</sub></i>
&minus; <i>W</i>)/&beta;;</p>
<p>(iii) d<sup>2</sup>ln&thinsp;<i>Z</i>/d&beta;<sup>2</sup> =
Var<sub><i>p</i></sub>(<i>w</i>) &ge; 0, so ln&thinsp;<i>Z</i> and <i>W</i> are
convex in &beta;;</p>
<p>(iv) if the values are the scores themselves, d<i>V</i>/d&beta; =
Var<sub><i>p</i></sub>(<i>w</i>) &ge; 0, with equality only when <i>p</i> is
supported on one score value;</p>
<p>(v) d<sup>3</sup>ln&thinsp;<i>Z</i>/d&beta;<sup>3</sup> = &kappa;<sub>3</sub>(<i>w</i>),
the third cumulant, which governs whether the sensitivity is monotone or has an
interior maximum;</p>
<p>(vi) as &beta; &rarr; +&infin;, <i>p</i> concentrates on the arg&nbsp;max of
<i>w</i>; as &beta; &rarr; 0, <i>p</i> tends to the uniform vector and <i>V</i> to the
unweighted mean.</p>
</div>
</div>

<p>The proofs are differentiation and are collected in Appendix A.4. The readings are
what matter. Part (iii) says ln&thinsp;<i>Z</i> is convex in &beta;, so the map
&beta; &mapsto; <i>W</i> has at most one minimum in any interval where its derivative
changes sign once, and a one-dimensional search for a &beta; meeting a score target is
well posed whenever the target lies in the range of the derivative. Part (iv) says that
when records are scored by the quantity being averaged, raising &beta; raises the
fused value: the aggregate rewards the records it already trusts. That sounds like a
tautology and is not, because the statement concerns a derivative rather than a level,
and the derivative is a variance that can be large or small independently of the level.</p>

<p>Part (v) is the part that surprises people, and it is the reason the calibration
procedure below opens with a grid rather than a bisection. The sensitivity
Var<sub><i>p</i></sub>(<i>w</i>) is a function of &beta; whose derivative at a point is
the third cumulant of the scores; when that cumulant is negative across an interval,
the sensitivity decreases monotonically, and when it changes sign the curve has an
interior maximum. Figure 3 shows both behaviours on two five-record instances. For
symmetric scores (&minus;2, &minus;1, 0, 1, 2) the sensitivity falls from 2.0000 to
3.7&times;10<sup>&minus;44</sup> with no interior maximum over a 240-point grid. For
skewed scores (0, 1, 2, 3, 10) it rises to 17.8629 at &beta; = 0.1543 and then
collapses. A calibration routine that assumes monotonicity is correct on the first
instance and wrong on the second, and no amount of validation monitoring will reveal
which case it is in.</p>

<figure>
<img src="figures/fig3_temperature.svg" alt="sensitivity of the fused value to inverse temperature"/>
<figcaption><b>Figure 3.</b> Self-scored sensitivity d<i>V</i>/d&beta; =
Var<sub><i>p</i></sub>(<i>w</i>) against &beta; on a logarithmic axis for two
five-record instances. Solid line and circles: symmetric scores, monotone decreasing.
Dashed line and squares: skewed scores, with an interior maximum of 17.8629 at
&beta; = 0.1543, marked. Only the skewed instance has a temperature at which the
aggregate is maximally sensitive. Source:
<i>results/e2_temperature_calculus.json</i>.</figcaption>
</figure>

<table>
<caption><b>Table 2.</b> Verification of Theorem 6 by central differences at step
10<sup>&minus;6</sup>, 600 random cases per row. Errors are absolute against the
analytic expression. Source: <i>results/e2_temperature_calculus.json</i>.</caption>
<thead><tr><th>Identity</th><th class="num">Max abs. error</th><th class="num">Tolerance</th><th>Verdict</th></tr></thead>
<tbody>
<tr><td>d<i>V</i>/d&beta; = Cov<sub><i>p</i></sub>(<i>v</i>,<i>w</i>)</td><td class="num">2.98&times;10<sup>&minus;9</sup></td><td class="num">10<sup>&minus;4</sup></td><td>holds</td></tr>
<tr><td>d<i>W</i>/d&beta; = (&Sigma;<i>p<sub>i</sub>w<sub>i</sub></i> &minus; <i>W</i>)/&beta;</td><td class="num">2.77&times;10<sup>&minus;9</sup></td><td class="num">10<sup>&minus;4</sup></td><td>holds</td></tr>
<tr><td>d<sup>2</sup>ln&thinsp;<i>Z</i>/d&beta;<sup>2</sup> = Var<sub><i>p</i></sub>(<i>w</i>)</td><td class="num">8.47&times;10<sup>&minus;7</sup></td><td class="num">10<sup>&minus;4</sup></td><td>holds</td></tr>
</tbody>
</table>

<h3>A. A worked example</h3>

<p>The abstract statements are easier to trust with an instance small enough to check
by hand. Five records: three model forecasts of the same quantity with validation
scores, and two cheap heuristics, arranged so that the heuristics sit at opposite ends
of the value range &mdash; the case that separates a weighted mean from a median and is
therefore the case worth tabulating.</p>

<table>
<caption><b>Table 3.</b> Worked example. Weights, fused value, score, sensitivity and
effective number of records exp&thinsp;<i>H</i>(<i>p</i>) for values 10.4, 9.8, 11.7,
8.9, 12.6 and scores 0.92, 0.86, 0.61, 0.35, 0.18. Source:
<i>results/e14_worked_example.json</i>.</caption>
<thead><tr><th class="num">&beta;</th><th>weights</th><th class="num">V</th><th class="num">W</th><th class="num">dV/d&beta;</th><th class="num">eff. records</th></tr></thead>
<tbody>
<tr><td class="num">0.25</td><td>0.217 0.214 0.201 0.188 0.180</td><td class="num">10.6473</td><td class="num">7.0319</td><td class="num">&minus;0.1278</td><td class="num">4.987</td></tr>
<tr><td class="num">0.50</td><td>0.234 0.227 0.201 0.176 0.162</td><td class="num">10.6161</td><td class="num">3.8230</td><td class="num">&minus;0.1215</td><td class="num">4.950</td></tr>
<tr><td class="num">1.00</td><td>0.269 0.253 0.197 0.152 0.128</td><td class="num">10.5586</td><td class="num">2.2331</td><td class="num">&minus;0.1083</td><td class="num">4.812</td></tr>
<tr><td class="num">2.00</td><td>0.336 0.298 0.181 0.108 0.077</td><td class="num">10.4633</td><td class="num">1.4647</td><td class="num">&minus;0.0827</td><td class="num">4.364</td></tr>
<tr><td class="num">4.00</td><td>0.448 0.353 0.130 0.046 0.023</td><td class="num">10.3394</td><td class="num">1.1205</td><td class="num">&minus;0.0446</td><td class="num">3.390</td></tr>
<tr><td class="num">8.00</td><td>0.583 0.361 0.049 0.006 0.002</td><td class="num">10.2414</td><td class="num">0.9875</td><td class="num">&minus;0.0106</td><td class="num">2.389</td></tr>
</tbody>
</table>

<p>Four readings, each a consequence of a different part of Theorem 6 rather than of
these numbers.</p>

<p><i>The sensitivity is negative.</i> The highest scores belong to the lowest
forecasts, so raising &beta; moves the value down; the derivative reports the direction
and its sign is the sign of the covariance (part i). A practitioner who assumes that
raising the temperature trusts the best records and therefore raises the value has
assumed a positive correlation that this instance does not have.</p>

<p><i>Effective records fall faster than the top weight rises.</i> Between &beta; = 1
and &beta; = 8 the leading weight rises from 0.269 to 0.583, but the effective number
of records falls from 4.81 to 2.39. Even at &beta; = 8 the aggregate is not "mostly one
record"; it is about two and a half. The exponential of the entropy is the honest
measure of concentration and the top weight is not.</p>

<p><i>Scores are not comparable across temperatures.</i> <i>W</i> falls from 7.03 to
0.99 as &beta; rises, which looks like degradation and is not: <i>W</i> depends on
&beta; through the partition sum, so comparing scores computed at different
temperatures is a category error. Pipeline scores may be compared only at a fixed
&beta;.</p>

<p><i>The derivative is checkable.</i> At &beta; = 1 the analytic sensitivity is
&minus;0.108319 and a central difference with step 10<sup>&minus;3</sup> gives
&minus;0.1083194, a gap of 3.6&times;10<sup>&minus;7</sup>. That is the level at which
all the finite-difference checks in this paper operate.</p>

<h3>B. Calibrating &beta; against a requirement</h3>

<p>The calculus becomes a procedure when a requirement is written as a derivative
rather than a value. Two forms are common: a <i>sensitivity budget</i>, in which the
fused value may move by at most <i>s</i> when &beta; moves within a tolerance band
(which matters when &beta; is itself estimated), and a <i>sharpness target</i>, in
which the effective number of records must stay below a cap (which matters when a
small set of records must not dominate).</p>

<p>In both forms the standard one-dimensional tools apply, with one caveat: because
Var<sub><i>p</i></sub>(<i>w</i>) need not be monotone in &beta; (part v), bisection is
valid only on a bracket where the sign of the derivative is fixed. The safe procedure
evaluates the criterion on a coarse grid first.</p>

<pre>Algorithm 1  Calibrate beta against a sensitivity budget
input : scores w, values v, target |dV/dbeta| &lt;= s, bracket [b_lo, b_hi]
output: beta meeting the budget, or a certificate that none exists in the bracket
1  evaluate g(beta) = max_coordinate |Cov_p(v, w)| on a grid of 32 points
2  if g(b_lo) &lt;= s return b_lo
3  find the first adjacent pair (b_j, b_j+1) with g(b_j) &gt; s and g(b_j+1) &lt;= s
4  if no such pair return "target not reachable inside the bracket"
5  bisect 40 times on [b_j, b_j+1] using the exact covariance, not a difference
6  return the right end of the final bracket</pre>

<p>The procedure is deliberately dull and it is in the paper because the alternative
&mdash; tuning &beta; until a validation metric stops improving &mdash; confounds two
effects that Theorem 6 separates: the change in sensitivity, governed by a variance,
and the change in the ranking, governed by the sign pattern of the score differences.
When &beta; crosses the reciprocal of a score gap the ranking flips, and no amount of
monitoring tells the operator that a flip happened rather than a gradual reweighting.</p>
'''

SEC_VI = '''
<h2>VI. Coarse-graining accounting</h2>

<h3>A. The situation</h3>

<p>A pipeline that fuses a million records is never evaluated in one place. Records
arrive in shards, each shard is summarised, and the summaries are merged. Section III
showed that the summary (<i>Z</i>, <i>S</i>) merges exactly and Section IV showed that
a summary without <i>Z</i> cannot. This section answers the remaining accounting
question: when a shard is summarised <i>coarsely</i>, so that its records are grouped
into blocks and only block-level quantities are combined, what is lost, and can the
loss be corrected from the summary?</p>

<div class="thm">
<p><span class="t">Theorem 7 (coarse-graining gap).</span></p>
<div class="body">
<p>Let &beta; &gt; 0 and let the records be partitioned into blocks
<i>B</i> = 1, &hellip;, <i>k</i>, with masses
<i>m<sub>B</sub></i> = &sum;<sub><i>i</i>&isin;<i>B</i></sub>e<sup>&beta;<i>w<sub>i</sub></i></sup>,
shares &pi;<sub><i>B</i></sub> = <i>m<sub>B</sub></i>/<i>Z</i> and block scores
<i>W<sub>B</sub></i> = &beta;<sup>&minus;1</sup>ln&nbsp;<i>m<sub>B</sub></i>. Then</p>
<div class="eq">
W = &sum;<sub>B</sub> &pi;<sub>B</sub> W<sub>B</sub> + &beta;<sup>&minus;1</sup> H(&pi;),
<span class="num">(7)</span>
</div>
<p>with H(&pi;) the Shannon entropy of the block shares, so</p>
<div class="eq">
0 &le; gap &le; &beta;<sup>&minus;1</sup> ln k,
<span class="num">(8)</span>
</div>
<p>with equality in the upper bound exactly when the block masses are equal. For
&beta; &lt; 0 the identity holds and both inequalities reverse, since
&beta;<sup>&minus;1</sup> is then negative; the implementation returns a signed gap.</p>
</div>
</div>

<p><i>Proof.</i> Since <i>Z</i> = &sum;<sub><i>B</i></sub><i>m<sub>B</sub></i>,
&beta;<sup>&minus;1</sup>ln&nbsp;<i>Z</i> &minus;
&sum;<sub><i>B</i></sub>&pi;<sub><i>B</i></sub>&beta;<sup>&minus;1</sup>ln&nbsp;<i>m<sub>B</sub></i>
= &beta;<sup>&minus;1</sup>[&minus;&sum;<sub><i>B</i></sub>&pi;<sub><i>B</i></sub>ln(<i>m<sub>B</sub></i>/<i>Z</i>)]
= &beta;<sup>&minus;1</sup>H(&pi;). The gap is non-negative because an entropy is; the
upper bound is the maximum of the entropy on <i>k</i> points, attained exactly at the
uniform distribution, which corresponds to equal masses. Appendix A.5 gives the
argument in full. &#9633;</p>

<p>Three consequences matter to a builder. First, the loss is signed: a block-wise
evaluation of the score under-estimates it for &beta; &gt; 0, and the shortfall is
exactly an entropy. Second, the shortfall is computable from the block masses alone,
so a merge service can correct it without ever seeing the records. Third, the
shortfall grows only logarithmically in the number of blocks &mdash; splitting a
pipeline into a thousand shards instead of ten costs at most an extra
&beta;<sup>&minus;1</sup>ln&nbsp;100 &asymp; 4.6/&beta; nats &mdash; which is why
sharding is cheap and why the honest worry is Section IV's mass, not this gap.</p>

<p>I am careful about the status of this result. The ingredients are classical: (7) is
the Gibbs variational principle read in one line and (8) is the elementary
maximum-entropy bound [2]. What I have not found in the fusion-operator literature is
the triple of properties that makes it an operating rule rather than an inequality:
exactness, computability from the summary alone, and a closed-form worst case. Section
IX records that as a repackaging, not as a new result.</p>

<figure>
<img src="figures/fig4_gap_bound.svg" alt="realised gap against its bound"/>
<figcaption><b>Figure 4.</b> Realised gaps against their bounds for
<i>k</i> &isin; {2, 4, 8} blocks and &beta; &isin; {0.5, 1, 2}, with block shares drawn
from Dirichlet distributions of concentration 0.2, 1 and 20 so that the spread from
near-degenerate to near-uniform is covered. No point lies above the line
gap = &beta;<sup>&minus;1</sup>ln&nbsp;<i>k</i>. An implementation can therefore quote
a worst-case correction before seeing the data. Source:
<i>results/e3_coarse_graining.json</i>.</figcaption>
</figure>

<h3>B. Levels, and the chain rule</h3>

<p>A real pipeline has more than one level: records into shards, shards into regions,
regions into a final aggregate. Theorem 7 applies at each level and the corrections
compose in the way entropy does.</p>

<div class="thm">
<p><span class="t">Theorem 8 (chain rule for coarse graining).</span></p>
<div class="body">
<p>Let the fine partition refine the coarse partition. Then</p>
<div class="eq">
gap(fine) = gap(coarse) + &sum;<sub>B</sub> &pi;<sub>B</sub> gap<sub>B</sub>(within).
<span class="num">(9)</span>
</div>
<p>Taking the fine partition to be the singletons,</p>
<div class="eq">
gap(singletons) = &beta;<sup>&minus;1</sup> H(p),
<span class="num">(10)</span>
</div>
<p>with H(p) the Shannon entropy of the weight vector.</p>
</div>
</div>

<p><i>Proof sketch.</i> Equation (9) is the Shannon chain rule
H(&pi;<sup>fine</sup>) = H(&pi;<sup>coarse</sup>) +
&sum;<sub><i>B</i></sub>&pi;<sub><i>B</i></sub>H(&pi;<sub>&middot;|<i>B</i></sub>)
combined with (7) at each level; (10) sets the fine partition to singletons, for which
the within-block entropies vanish. Appendix A.6 gives both derivations. &#9633;</p>

<p>Equation (10) is a good way to remember the construction: the total distance between
the global score and the score obtained by treating every record as its own block is
the entropy of the weight vector divided by &beta;, which is also the logarithm of the
effective number of records. The pipeline's accounting error and its effective sample
size are the same number seen from two sides. Experiment E4 confirms both to machine
precision: over 60 random instances with 32 records and three temperatures the chain
residual never exceeded 8.9&times;10<sup>&minus;16</sup> and the entropy identity held to
1.8&times;10<sup>&minus;15</sup>.</p>

<table>
<caption><b>Table 4.</b> Coarse-graining checks. Sources:
<i>results/e3_coarse_graining.json</i>, <i>results/e4_hierarchy.json</i>.</caption>
<thead><tr><th>Check</th><th class="num">Instances</th><th class="num">Residual</th><th class="num">Ratio range</th><th>Verdict</th></tr></thead>
<tbody>
<tr><td>Identity (7)</td><td class="num">320</td><td class="num">2.2&times;10<sup>&minus;15</sup></td><td class="num">0.99999999999999&ndash;1.00000000000002</td><td>holds</td></tr>
<tr><td>Bound (8)</td><td class="num">320</td><td class="num">&mdash;</td><td class="num">&le; 1</td><td>holds</td></tr>
<tr><td>Sharp case: 8 equal masses, &beta; = 1.5</td><td class="num">1</td><td class="num">&mdash;</td><td class="num">1.000000</td><td>attains ln&nbsp;8/1.5 = 1.3862943611</td></tr>
<tr><td>Reconstruction of <i>W</i> from masses only</td><td class="num">1</td><td class="num">0.0</td><td class="num">&mdash;</td><td>exact in floating point</td></tr>
<tr><td>Chain rule (9)</td><td class="num">60</td><td class="num">8.9&times;10<sup>&minus;16</sup></td><td class="num">&mdash;</td><td>holds</td></tr>
<tr><td>Entropy identity (10)</td><td class="num">60</td><td class="num">1.8&times;10<sup>&minus;15</sup></td><td class="num">&mdash;</td><td>holds</td></tr>
</tbody>
</table>

<h3>C. The merge procedure</h3>

<p>Theorems 1, 7 and 8 turn into an interface with three numbers: the mass <i>Z</i>,
the numerator <i>S</i>, and the record count <i>n</i> (the count is not needed for
merging, but it is needed to interpret and to audit). Merging is addition on the first
two; the pair is recovered from them. An implementation that stores block scores
instead can restore exactness with the correction of (7). An implementation that
stores only values cannot, by Theorem 3.</p>

<pre>Algorithm 2  Exact merge of two pipeline aggregates
input : (Z1, S1) and (Z2, S2)          # Z = total mass, S = sum of m_i * v_i
output: (Z, S) with Z = Z1 + Z2 and S = S1 + S2
1  Z &lt;- Z1 + Z2
2  S &lt;- S1 + S2
3  V &lt;- S / Z                          # fused value, exact
4  W &lt;- log(Z) / beta                  # score, exact
5  if only (W1, V1) and (W2, V2) are available then
6      Z1 &lt;- exp(beta * W1); Z2 &lt;- exp(beta * W2)     # exact, masses were carried
7      V &lt;- (Z1 * V1 + Z2 * V2) / (Z1 + Z2)
8      W &lt;- log(Z1 + Z2) / beta
9      assert |V - exact| &lt;= tolerance    # otherwise see Theorems 3-5
10 return (Z, S)</pre>

<p>Line 5 is the interesting one: a summary that carries its own mass can be merged
exactly, and a summary that carries only a value cannot be merged at all without an
assumption. That asymmetry is the interface form of Theorem 1(v) and the quantitative
content of Section IV.</p>
'''

SEC_VII = '''
<h2>VII. Certified error budgets for estimated weights</h2>

<h3>A. Why a certificate</h3>

<p>In production the scores are not given; they are estimated. The estimate may come
from a validation set, from a calibrated model, or from finitely many measurements on
a device. Whoever runs the pipeline then has two numbers: an aggregate computed from
estimated weights, and a claim about how far that aggregate may be from the true one.
The claim is the certificate, and without one the aggregate is a point estimate with no
error bar, which in a regulated setting is worse than useless because it looks like
knowledge.</p>

<p>There are two ways to produce a certificate. The honest way is to bound the error
in the weights and propagate it through the two slots. The dishonest way is to divide
the exponent by &beta; and hope, on the theory that a low temperature cools errors.
Theorem 9 says the second way is not merely dishonest but unnecessary: reading a weight
vector as a softmax of logits &mdash; which is what the formula invites, since
<i>w</i> = &beta;<sup>&minus;1</sup>ln&nbsp;<i>p</i> &mdash; cannot amplify an
<i>L</i><sub>1</sub> error at all.</p>

<div class="thm">
<p><span class="t">Theorem 9 (no amplification by the logit parametrisation).</span></p>
<div class="body">
<p>Let <i>p</i> be a probability vector with strictly positive entries, let
<i>w</i> = &beta;<sup>&minus;1</sup>ln&nbsp;<i>p</i>, and let <i>p&#770;</i> be a
non-negative estimate with <i>L</i><sub>1</sub> error
&epsilon; = &Vert;<i>p&#770;</i>&minus;<i>p</i>&Vert;<sub>1</sub> &lt; 1. Set
<i>w&#770;</i> = &beta;<sup>&minus;1</sup>ln&nbsp;<i>p&#770;</i>, after the
non-negative smoothing needed to keep the logarithm finite, and let <i>q</i> =
softmax(&beta;<i>w&#770;</i>). Then <i>q</i> = <i>p&#770;</i>/&Vert;<i>p&#770;</i>&Vert;<sub>1</sub>
and</p>
<div class="eq">
TV(q, p) &le; &epsilon;/(1 &minus; &epsilon;).
<span class="num">(11)</span>
</div>
<p>In particular the logit step is a renormalisation and carries no exponential
amplification.</p>
</div>
</div>

<p><i>Proof.</i> softmax(&beta;&middot;&beta;<sup>&minus;1</sup>ln&nbsp;<i>p&#770;</i>)
= softmax(ln&nbsp;<i>p&#770;</i>) = <i>p&#770;</i>/&sum;<sub><i>i</i></sub><i>p&#770;<sub>i</sub></i>,
the first claim. Write <i>S</i> = &sum;<sub><i>i</i></sub><i>p&#770;<sub>i</sub></i> = 1
+ &delta; with |&delta;| &le; &epsilon;. For each coordinate,
<i>q<sub>i</sub></i>&minus;<i>p<sub>i</sub></i> =
(<i>p&#770;<sub>i</sub></i>&minus;<i>p<sub>i</sub></i>&minus;&delta;<i>p<sub>i</sub></i>)/<i>S</i>,
so &sum;<sub><i>i</i></sub>|<i>q<sub>i</sub></i>&minus;<i>p<sub>i</sub></i>| &le;
(&epsilon;+|&delta;|)/<i>S</i> &le; 2&epsilon;/(1&minus;&epsilon;), and total variation is
half of that. &#9633;</p>

<p>The bound is useful and honest about its limits: at &epsilon; = 0.1 it gives 0.111,
at &epsilon; = 0.5 it gives 1, and beyond it exceeds 1 and becomes vacuous. Experiment
E9 confirms that it is valid and slack: over 600 random cases at four error levels the
realised total variation never came within 0.0197 of the bound, which is what one
expects, since the bound pays for the worst-case alignment of the perturbation with the
coordinate signs.</p>

<h3>B. Composing the stages</h3>

<p>A realistic pipeline has at least three error sources: the weights are estimated
from finitely many samples, some records are discarded for cost, and the score is
evaluated block-wise. Theorem 10 composes the first two with the diameter of the value
vector; Section VI already handles the third.</p>

<div class="thm">
<p><span class="t">Theorem 10 (composition of sampling and truncation).</span></p>
<div class="body">
<p>Let <i>D</i> = max<sub><i>i</i>,<i>j</i></sub>&Vert;<i>v<sub>i</sub></i>&minus;<i>v<sub>j</sub></i>&Vert;
let <i>p&#770;</i> be an estimate with
&epsilon; = &Vert;<i>p&#770;</i>&minus;<i>p</i>&Vert;<sub>1</sub> &lt; 1; and let
<i>K</i> be the retained set with estimated retained mass 1&minus;&tau;&#770;. Then the
pipeline value <i>V&#770;</i> computed from <i>p&#770;</i> restricted to <i>K</i>
satisfies</p>
<div class="eq">
&Vert;V&#770; &minus; V&Vert; &le; D &middot; min( 1, &tau;&#770; +
&epsilon;/(1&minus;&epsilon;) ).
<span class="num">(12)</span>
</div>
</div>
</div>

<p><i>Proof.</i> Split the error into truncation of the true weights and perturbation
of the retained ones. Dropping mass &tau; from a convex combination moves the result by
at most <i>D</i>&tau;; a perturbation of the retained weights of total variation <i>t</i>
moves it by at most <i>Dt</i>; Theorem 9 bounds <i>t</i> by
&epsilon;/(1&minus;&epsilon;); and the sum is capped at 1 because the value lies in a set
of diameter <i>D</i>. Appendix A.8 gives the details, including the case in which the
retained set is chosen from the estimate rather than from the truth. &#9633;</p>

<p>Theorem 10 is the statement I would defend hardest in an engineering review, because
it lets a pipeline publish a number instead of a hope. It also has an honest failure
mode which the experiment found and which I report rather than hide: when the sample
size is small and &beta; is large, the estimate &epsilon; approaches 1, the bound
saturates, and the certificate says nothing. At &beta; = 3 with ten shots the mean
certificate was 1.63 &mdash; larger than the largest possible value error &mdash; while
the measured error was 0.10. A saturated certificate is not a false statement; it is a
statement that the experiment was not informative enough to support one. The practical
rule is to compute the certificate before the experiment (Algorithm 3) and to raise the
shot count until it is worth reporting.</p>

<figure>
<img src="figures/fig5_sampling.svg" alt="error and certificate against shot count"/>
<figcaption><b>Figure 5.</b> Measured absolute error in the fused value (filled
markers, solid lines) and the certified bound of Theorem 10 (open markers, other line
styles) against the number of shots, for eight records and two temperatures. Both axes
are logarithmic; 120 replications per point. The error falls as the inverse square root
of the shot count, as sampling theory predicts, and the certificate never crosses below
it. At ten shots and &beta; = 3 the certificate is clamped and carries no information.
Source: <i>results/e7_sampling.json</i>.</figcaption>
</figure>

<table>
<caption><b>Table 5.</b> Sampling experiment. Each row aggregates 120 replications of a
fixed eight-record instance. The last column is the realised coverage of a 95%
non-parametric bootstrap interval for the fused value, 200 resamples per replication.
Source: <i>results/e7_sampling.json</i>.</caption>
<thead><tr><th class="num">&beta;</th><th class="num">Shots</th><th class="num">Mean error</th><th class="num">95th pct.</th><th class="num">Mean cert.</th><th class="num">Coverage</th></tr></thead>
<tbody>
<tr><td class="num">1.0</td><td class="num">10</td><td class="num">0.0865</td><td class="num">0.2111</td><td class="num">1.3689</td><td class="num">0.958</td></tr>
<tr><td class="num">1.0</td><td class="num">100</td><td class="num">0.0391</td><td class="num">0.0967</td><td class="num">0.3763</td><td class="num">0.892</td></tr>
<tr><td class="num">1.0</td><td class="num">1 000</td><td class="num">0.0122</td><td class="num">0.0263</td><td class="num">0.0933</td><td class="num">0.967</td></tr>
<tr><td class="num">1.0</td><td class="num">10 000</td><td class="num">0.0038</td><td class="num">0.0094</td><td class="num">0.0277</td><td class="num">0.967</td></tr>
<tr><td class="num">3.0</td><td class="num">10</td><td class="num">0.1017</td><td class="num">0.2626</td><td class="num">1.6267</td><td class="num">0.983</td></tr>
<tr><td class="num">3.0</td><td class="num">100</td><td class="num">0.0485</td><td class="num">0.1088</td><td class="num">0.4030</td><td class="num">0.975</td></tr>
<tr><td class="num">3.0</td><td class="num">1 000</td><td class="num">0.0166</td><td class="num">0.0378</td><td class="num">0.1138</td><td class="num">0.950</td></tr>
<tr><td class="num">3.0</td><td class="num">10 000</td><td class="num">0.0060</td><td class="num">0.0153</td><td class="num">0.0362</td><td class="num">0.900</td></tr>
</tbody>
</table>

<p>The coverage column is the part of Table 5 I would flag first if I were reviewing
this paper. A nominal 95% interval should cover in about 95% of replications; the
observed values range from 0.892 to 0.983, and two of eight cells sit at or below 0.90.
With 120 replications the standard error of a coverage estimate near 0.95 is about
0.02, so one cell at 0.89 is two standard errors low &mdash; uncomfortable but not
damning &mdash; while two cells in the same experiment suggest a systematic effect
rather than noise. The likely cause is that the bootstrap resamples the estimated
weights but treats the smoothing as if it were data, which biases the interval slightly
narrow. I have not corrected it, because correcting after seeing the coverage would be
fitting the protocol to the result; it is recorded as a limitation in Section XII.</p>

<figure>
<img src="figures/fig6_coverage.svg" alt="bootstrap coverage by cell"/>
<figcaption><b>Figure 6.</b> Realised bootstrap coverage per cell of Table 5 against
the nominal 0.95 line (dashed). Unhatched bars are &beta; = 1, hatched bars are
&beta; = 3. The shortfall at intermediate shot counts is the limitation discussed in
the text.</figcaption>
</figure>

<h3>C. The composed certificate</h3>

<p>Combining Theorems 7 and 10 gives the procedure a pipeline should run before
committing to a configuration: it answers "how many shots and how many retained
records do I need in order to publish an error bar of size <i>e</i>?" without running
the experiment.</p>

<pre>Algorithm 3  Plan a certified pipeline
input : value diameter D, target error e, candidate (shots m, retain top-k)
output: a certificate, or the instruction to raise m or k
1  eps_hat &lt;- min(1, E|| p_hat - p ||_1) computed from m and the current p_hat
2  tau_hat &lt;- estimated discarded mass for the chosen k
3  bound &lt;- D * min(1, tau_hat + eps_hat / (1 - eps_hat))
4  if bound &gt; e then
5      report which of the two terms dominates; raise m or raise k
6  else
7      run the pipeline and publish bound alongside the value</pre>

<p>On 300 random instances the composed bound held in every case, with a median ratio
of measured error to bound of 0.056 and a maximum of 0.308
(<i>results/e10_pipeline.json</i>). A median slack of a factor of eighteen is the price
of a worst-case argument, and I state it plainly: the certificate is a guarantee, not an
estimate, and a practitioner who wants a tight number should pair it with the bootstrap
of Table 5 and publish both.</p>
'''
