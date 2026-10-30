# -*- coding: utf-8 -*-
"""Sections IX-XIV, appendices and references."""

SEC_IX = '''
<h2>IX. Prior art and a conservative novelty assessment</h2>

<h3>A. Method of assessment</h3>

<p>For each statement I ask two questions: is the mathematical content already in the
literature, and if so where; and is the specific form used here already published. A
statement is called <i>classical</i> if content and form are both in the literature,
<i>repackaged</i> if the content is classical but the operational form is not one I can
find, and <i>new</i> only if I can point to a proof and say what would falsify the claim
of novelty. Under that discipline one claim is offered as new &mdash; Theorem 3 together with
the sharp constant of Theorem 4 &mdash; four statements are called repackaged, and the
rest are classical. The one-page novelty assessment accompanying the deposit repeats this
table with the falsification conditions written out.</p>

<table>
<caption><b>Table 6.</b> Prior-art assessment. The third column names the nearest source
I know; the fourth gives the verdict under the discipline described in the text.</caption>
<thead><tr><th>Statement</th><th>Content</th><th>Nearest prior art</th><th>Verdict</th></tr></thead>
<tbody>
<tr><td>Theorem 1 (ledger)</td><td>additive sufficient statistic; weighted-mean barycentre; log-sum-exp</td><td>exponential families [18]; LSE evaluation [8]</td><td>classical</td></tr>
<tr><td>Theorem 1(iii) (duplication)</td><td>ln <i>k</i>/&beta; for a <i>k</i>-fold duplicate</td><td>companion report [1, Thm 1], there as a numerical correction</td><td>repackaged: here derived as an algebraic law</td></tr>
<tr><td>Lemma 1 (no bilinearity)</td><td>elementary counterexample</td><td>none needed</td><td>classical observation</td></tr>
<tr><td>Theorem 2 (<i>n</i>-ary form)</td><td>log-sum-exp associativity</td><td>[8], [18], mergeable summaries [16, 17]</td><td>classical</td></tr>
<tr><td><b>Theorem 3 (reachable set)</b></td><td>value-only summaries leave the convex hull</td><td>mergeability [16, 17]; communication lower bounds [19]</td><td><b>offered as new</b></td></tr>
<tr><td><b>Theorem 4 (sharp constant)</b></td><td>minimax radius = Chebyshev radius; midpoint in one dimension</td><td>standard minimax reasoning; no source found for this operator</td><td><b>offered as new</b> (constant sharp)</td></tr>
<tr><td><b>Theorem 5 (quantised ledger)</b></td><td><i>D</i>&delta;/(1&minus;&delta;) independent of the number of blocks</td><td>quantised averaging bounds, which are not directly applicable here</td><td>repackaged with a new constant</td></tr>
<tr><td>Theorem 6 (temperature)</td><td>fluctuation&ndash;dissipation; convexity; cumulants</td><td>statistical mechanics; convex analysis [3, 7]</td><td>classical</td></tr>
<tr><td>Theorem 7 (gap identity)</td><td>Gibbs variational principle; entropy bound</td><td>[2, ch. 2, 12]</td><td>content classical; <b>form repackaged</b></td></tr>
<tr><td>Theorem 8 (chain rule)</td><td>Shannon chain rule</td><td>[2, ch. 2]</td><td>classical</td></tr>
<tr><td>Theorem 9 (no amplification)</td><td><i>L</i><sub>1</sub> to total variation via renormalisation</td><td>folklore; Hilbert-metric sharp bound [10, 11]</td><td>classical</td></tr>
<tr><td>Theorem 10 (composition)</td><td>convexity plus triangle inequality</td><td>truncation analyses [12, 14]</td><td>classical</td></tr>
<tr><td>Theorem 11 (dephasing)</td><td>pinching inequality</td><td>[6, 4]</td><td>classical</td></tr>
<tr><td>Theorem 12 (no converse)</td><td>orthogonal pure states with equal diagonals</td><td>elementary; known in state discrimination</td><td>classical</td></tr>
<tr><td>Corollary 1 (Helstrom floor)</td><td>composition of a TV bound with Helstrom</td><td>[1, 5, 10]</td><td>repackaged composition</td></tr>
</tbody>
</table>

<h3>B. The claim I will defend, and the ones I will not</h3>

<p>The claim is Theorem 3 with Theorem 4 and Theorem 5 attached: <i>for a fusion operator
that carries a score alongside a value, a summary without the normalising mass leaves the
merged value undetermined on the convex hull of the shard values; the minimax rule is the
Chebyshev centre, whose worst-case error is half the range in one dimension and is
attained; and a ledger quantised to relative precision &delta; merges to within
<i>D</i>&delta;/(1&minus;&delta;) independently of the number of shards.</i> The style of
argument is standard minimax theory and the question is a mergeability question in the
sense of [16]; what I could not find is the statement for this operator with an exact
constant and an explicit attaining construction. That is a small claim and I make only
that one.</p>

<p>Three claims I explicitly do <i>not</i> make. I do not claim that the ledger is
&quot;necessary for distributed fusion&quot; in any general sense: it is necessary for
exactness given a value-only summary, and a system may legitimately accept the error bar
of Theorem 4 instead. I do not claim the constants in Theorem 5 are optimal; the measured
worst case was a factor of three below the bound. And I do not claim priority: the
argument is old enough that it has probably been written down somewhere in the sketches
literature, and a reader who knows such a reference should treat this paragraph as an
invitation to send it.</p>

<h3>C. What would falsify each claim</h3>

<p>For Theorem 3: a dataset whose global value lies outside the hull of the reported
block values, which would contradict the convexity of the weights. For Theorem 4: a merge
rule with worst-case error below half the range on a family of instances, or an instance
where the midpoint's worst case exceeds half the range. For Theorem 5: a rounding pattern
whose induced error exceeds <i>D</i>&delta;/(1&minus;&delta;). For Theorem 7: a negative
gap at &beta; &gt; 0, or a gap above &beta;<sup>&minus;1</sup>ln&nbsp;<i>k</i>. For
Theorem 9: an estimate with &epsilon; &lt; 1 whose renormalised total variation exceeds
&epsilon;/(1&minus;&epsilon;). For Theorem 11: a pair of states whose dephasing increases
the trace distance, which would contradict a standard theorem and would more likely
indicate a bug in my code. The experiments search for exactly these failures and report
none; the negative results that did appear are in Section XII.</p>
'''

SEC_X = '''
<h2>X. Experiments and results</h2>

<h3>A. What counts as evidence here</h3>

<p>The experiments are of one kind: a stated mathematical property is evaluated on
randomly generated instances and the deviation of the computed quantity from the predicted
one is recorded. That is a check of an identity or a bound against floating-point reality,
not an empirical study of a phenomenon, and the difference matters for how the results
should be read. A deviation of 10<sup>&minus;16</sup> does not corroborate Theorem 7 the
way a measurement corroborates a physical theory; it shows that the theorem has been
implemented without algebra errors and that no step of it depends on a cancellation double
precision cannot survive. Where a claim is genuinely empirical &mdash; the bootstrap
coverage of Table 5, for instance &mdash; the experiment uses replication, reports
dispersion, and is described in different language.</p>

<p>Three protocol decisions apply throughout. The pseudo-random generator is seeded per
experiment with a fixed offset from a master seed (2026110101), so the whole result set is
reproduced by one command. No wall-clock timing appears in the scientific outputs: a timing
measurement on a shared machine is not reproducible in the sense this paper needs, and
quoting one would invite a reading of &quot;faster&quot; that the work does not support.
Each experiment writes its own JSON file with the property it checks, the instance counts,
the residuals and a boolean verdict, so the verifier can read verdicts rather than
re-derive them from prose.</p>

<h3>B. The experiment set</h3>

<table>
<caption><b>Table 7.</b> The sixteen experiments, with the property each tests, its
instance count and its verdict. File names are those of the JSON outputs in
<i>results/</i>; the verifier re-derives every verdict independently where possible.</caption>
<thead><tr><th>Id</th><th>Property</th><th class="num">Instances</th><th>Verdict</th></tr></thead>
<tbody>
<tr><td>E1</td><td>softmax is exactly invertible on the positive simplex</td><td class="num">400</td><td>holds, max error 2.2&times;10<sup>&minus;16</sup></td></tr>
<tr><td>E2</td><td>temperature identities of Theorem 6 and the shape of the sensitivity</td><td class="num">600 &times; 3</td><td>holds, max error 8.5&times;10<sup>&minus;7</sup>; monotone and peaked cases both reproduced</td></tr>
<tr><td>E3</td><td>coarse-graining identity, bound and sharpness</td><td class="num">320</td><td>holds, residual 2.2&times;10<sup>&minus;15</sup></td></tr>
<tr><td>E4</td><td>chain rule and the singleton-entropy identity</td><td class="num">60</td><td>holds, residual 1.8&times;10<sup>&minus;15</sup></td></tr>
<tr><td>E5</td><td>commuting bound and the coherent counterexample</td><td class="num">300 + 200</td><td>holds; counterexample confirmed</td></tr>
<tr><td>E6</td><td>Helstrom floor for score perturbations</td><td class="num">400</td><td>holds, 0 violations</td></tr>
<tr><td>E7</td><td>finite-shot error, certificate and bootstrap coverage</td><td class="num">8 &times; 120</td><td>certificate holds; coverage 0.892&ndash;0.983</td></tr>
<tr><td>E8</td><td>von Neumann entropy equals Shannon entropy on diagonals</td><td class="num">200</td><td>holds, 4.4&times;10<sup>&minus;16</sup></td></tr>
<tr><td>E9</td><td>logit parametrisation does not amplify <i>L</i><sub>1</sub> error</td><td class="num">600</td><td>holds, 0 violations</td></tr>
<tr><td>E10</td><td>composed certificate for sampling plus truncation</td><td class="num">300</td><td>holds, 0 violations</td></tr>
<tr><td>E11</td><td>dephasing contracts the trace distance</td><td class="num">300</td><td>holds, 0 violations</td></tr>
<tr><td>E12</td><td>reachable set, minimax constant and the same-summary counterexample</td><td class="num">500</td><td>holds; worst case equals half the range to 8.9&times;10<sup>&minus;16</sup></td></tr>
<tr><td>E13</td><td>algebra of the operation (Theorems 1&ndash;2)</td><td class="num">700+</td><td>commutative and associative; not idempotent; not homogeneous</td></tr>
<tr><td>E14</td><td>worked example and a finite-difference check</td><td class="num">1</td><td>derivative matches to 3.6&times;10<sup>&minus;7</sup></td></tr>
<tr><td>E15</td><td>quantised ledger: error against the bound of Theorem 5</td><td class="num">600 + 1</td><td>holds; max ratio of error to bound 0.31</td></tr>
<tr><td>E16</td><td>tree merging equals <i>n</i>-ary merging up to 10<sup>4</sup> records</td><td class="num">9</td><td>holds, relative gap 3.7&times;10<sup>&minus;16</sup></td></tr>
</tbody>
</table>

<h3>C. Results that deserve a paragraph</h3>

<p><i>Representability (E1).</i> Any strictly positive distribution on <i>n</i> outcomes is
the softmax of some score vector, with a maximum reconstruction error of
2.2&times;10<sup>&minus;16</sup> over 400 instances, including a distribution with a
10<sup>&minus;6</sup> entry and a uniform one. The value is practical: no pipeline need be
restricted to the family of distributions a given score model can express, because if a
target distribution is available the scores reproducing it exist in closed form,
<i>w</i> = &beta;<sup>&minus;1</sup>ln&nbsp;<i>p</i>.</p>

<p><i>Algebra (E13).</i> Commutativity holds to 5.6&times;10<sup>&minus;16</sup> and
associativity to 8.9&times;10<sup>&minus;16</sup>; idempotence fails by exactly
&beta;<sup>&minus;1</sup>ln&nbsp;2 with a residual of at most 2.8&times;10<sup>&minus;17</sup>
across three temperatures; homogeneity fails by 2.1932 at &lambda; = 2, which is the fact
that removes the inner-product reading.</p>

<p><i>Impossibility (E12).</i> Over 200 random datasets every value reached by random
admissible masses lay inside the hull (fraction 1.000, maximum violation
&minus;6.4&times;10<sup>&minus;8</sup> in the direction that is inside), and over 300
instances the minimax rule's realised worst case equalled half the range to
8.9&times;10<sup>&minus;16</sup>. Equal weighting was never better than the minimax rule,
with a ratio of worst cases between 1.000 and 1.463 and a mean of 1.128.</p>

<p><i>Dephasing (E11).</i> Over 300 random pairs the mean full trace distance was 0.562,
of which 0.248 was visible in the diagonals and 0.314 came from coherence; the minimum
slack was 0.009, so there were cases in which coherence added almost nothing, and none in
which it subtracted. This is the profile of a contraction that is sometimes an isometry,
which is what Theorem 11 claims and no more.</p>

<p><i>Sampling (E7).</i> Coverage of the bootstrap interval, computed by resampling
[13] and reported per cell rather than pooled, ranged from 0.892 to 0.983 against a
nominal 0.95: six of eight cells were at or above nominal and two were about two standard
errors low. The certificate, by contrast, held in every cell, with the mean bound 1.6267
against a mean realised error of 0.1017 at &beta; = 3 and ten shots, which is the
saturation reported in Section XII. The concentration background that makes the
certificate work in the non-saturated regime is the <i>L</i><sub>1</sub> deviation
literature [14].</p>

<p><i>Tree merging (E16).</i> Nine configurations spanning 10<sup>2</sup> to
10<sup>4</sup> records and block sizes of 1, 10 and 100 produce tree-merged aggregates
equal to the <i>n</i>-ary aggregate with a maximum relative value gap of
3.7&times;10<sup>&minus;16</sup> and a maximum score gap of exactly zero. The engineering
reading is that sharding is free: any tree, any block size, no loss.</p>
'''
