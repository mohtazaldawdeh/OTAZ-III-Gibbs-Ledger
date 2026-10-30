# -*- coding: utf-8 -*-
"""Section IV: the ledger is necessary (impossibility, sharp constant, quantisation)."""

SEC_IV = '''
<h2>IV. The ledger is necessary: an impossibility theorem and its sharp constant</h2>

<h3>A. The interface question</h3>

<p>Suppose a pipeline is partitioned across <i>k</i> shards. Each shard holds a
collection of scored records whose union is the full collection. Two designs are
possible for the interface between a shard and the merge service. In the first, the
shard reports the pair (<i>V<sub>B</sub></i>, <i>W<sub>B</sub></i>) computed from its
own records, and the merge service combines the reported pairs using (2). In the
second, the shard reports only its value <i>V<sub>B</sub></i> &mdash; possibly with the
number of records <i>n<sub>B</sub></i> &mdash; and the merge service does what it can.</p>

<p>The first design is exact by Theorem 1: the pair determines the mass
<i>Z<sub>B</sub></i> = e<sup>&beta;<i>W<sub>B</sub></i></sup> and the numerator
<i>S<sub>B</sub></i> = <i>Z<sub>B</sub>V<sub>B</sub></i>, both additive, so the merge
is a two-line computation with no error at all. The second design is what a
cost-conscious implementation drifts toward, because a value is one number and a pair
is two, and because a downstream consumer often wants only the value. It is also
what happens by accident whenever a shard computes its own average, reports it, and
the merge service averages the reports.</p>

<p>This section settles what the second design costs. The answer has three parts:
the set of global values that remain possible is exactly the convex hull of the
reported values; every merge rule has worst-case error at least the radius of that
hull, which in one dimension is half the range, and the midpoint attains it; and if
the mass is carried but rounded, the error is bounded by
<i>D</i>&delta;/(1&minus;&delta;). None of these statements is deep. Together they
convert a stylistic choice into a quantitative one, which is what an architect needs
in order to decide how much of the ledger to keep.</p>

<h3>B. What a value-only summary can and cannot determine</h3>

<div class="thm">
<p><span class="t">Theorem 3 (the reachable set is the hull).</span></p>
<div class="body">
<p>Fix &beta; and let a partition into <i>k</i> blocks have reported values
<i>V</i><sub>1</sub>, &hellip;, <i>V<sub>k</sub></i> &isin; R<sup><i>d</i></sup>.
Consider any merge rule &Gamma; whose input is the collection of pairs
(<i>V<sub>B</sub></i>, <i>w<sub>B</sub></i><sup>(inside)</sup>) in the sense that it
may use anything computable from within block <i>B</i> except the block's normalising
mass. Then the set of global values compatible with what &Gamma; sees is exactly</p>
<div class="eq">
S = conv{ V<sub>1</sub>, &hellip;, V<sub>k</sub> },
<span class="num">(4)</span>
</div>
<p>the convex hull of the reported values. In particular the number of records per
block, and any function of the within-block weights, adds nothing.</p>
</div>
</div>

<p><i>Proof.</i> That <i>S</i> &sube; conv{<i>V<sub>B</sub></i>} is immediate: the
global value is a convex combination of the block values with weights
&pi;<sub><i>B</i></sub> = <i>Z<sub>B</sub></i>/<i>Z</i> &ge; 0 summing to one.</p>

<p>For the reverse inclusion, take any &pi; in the simplex. It is enough to exhibit,
for each block <i>B</i>, a block of records whose reported value is
<i>V<sub>B</sub></i> and whose mass is any prescribed positive number
<i>M<sub>B</sub></i>. Take a single record (<i>V<sub>B</sub></i>,
<i>w<sub>B</sub></i>) with <i>w<sub>B</sub></i> =
&beta;<sup>&minus;1</sup>ln&nbsp;<i>M<sub>B</sub></i>: its value is
<i>V<sub>B</sub></i> and its mass is <i>M<sub>B</sub></i>. Then the global value is
&sum;<sub><i>B</i></sub>&pi;<sub><i>B</i></sub><i>V<sub>B</sub></i> for
&pi;<sub><i>B</i></sub> = <i>M<sub>B</sub></i>/&sum;<sub><i>C</i></sub><i>M<sub>C</sub></i>,
and since the <i>M<sub>B</sub></i> are free the weights range over the whole
simplex. The same construction works when blocks must contain at least
<i>n<sub>B</sub></i> records, because adding records with the block value
<i>V<sub>B</sub></i> changes neither the value nor the sensitivity to the free mass.
Appendix A.2 gives the construction in the multi-record case. &#9633;</p>

<p>The mechanism deserves a name, because it recurs. Shifting every score inside a
block by the same constant <i>c</i> multiplies that block's mass by
e<sup>&beta;<i>c</i></sup> and leaves every within-block weight, hence the block's
value, unchanged (Theorem 1(vi)). A value-only summary is therefore blind to a
quantity that the merge needs, and blind in a way that cannot be repaired by any
local computation: the information was never collected.</p>

<div class="note">
<p><b>A concrete pair.</b> Let block <i>A</i> contain two records with values 0 and
10 and scores 0 and 0, and let block <i>A&#8242;</i> contain two records with the same
two values and scores 3 and 3. Both blocks report <i>V<sub>A</sub></i> = 5.0 and
<i>n<sub>A</sub></i> = 2; their masses are 2.0 and 40.17. Merge each with a third
block holding a single record of value 0 and score 0. The two global values are
<b>3.3333</b> and <b>4.8786</b> &mdash; a difference of <b>1.5452</b> on a value range
of 10, produced by two datasets that are indistinguishable to any merge rule that
looks at values and counts. The numbers are regenerated by experiment E12 and stored
in <i>results/e12_impossibility.json</i>.</p>
</div>

<p>The pair also shows why a pipeline cannot repair the omission downstream. Once the
mass is gone, two different datasets are consistent with the same report, so no
post-hoc adjustment, calibration or reweighting can separate them: a rule that
handles one of the two correctly must mishandle the other. That is the sense in which
the ledger is necessary rather than merely advisable.</p>

<figure>
<img src="figures/fig1_reachable.svg" alt="mass-blind merging against the minimax bound"/>
<figcaption><b>Figure 1.</b> Worst-case error of equal weighting against the minimax
worst-case error, over 300 instances with two to six blocks and values drawn from a
normal distribution. Every point lies on or above the diagonal: the equal-weight
merge is never better than the minimax rule, and it coincides with it only when the
mean happens to be the midpoint of the extremes. The horizontal axis is the sharp
constant of Theorem 4, namely half the range. Source:
<i>results/e12_impossibility.json</i>.</figcaption>
</figure>

<h3>C. The sharp constant, and why the midpoint is forced</h3>

<div class="thm">
<p><span class="t">Theorem 4 (minimax constant for a lossy ledger).</span></p>
<div class="body">
<p>Under the hypotheses of Theorem 3, for every merge rule &Gamma; that sees the block
values,</p>
<div class="eq">
sup<sub>consistent datasets</sub> &Vert;&Gamma; &minus; V&Vert;
&ge; rad(S) := min<sub>c &isin; R<sup>d</sup></sub> max<sub>B</sub>
&Vert;V<sub>B</sub> &minus; c&Vert;,
<span class="num">(5)</span>
</div>
<p>and the bound is attained: the rule
&Gamma;* = arg&nbsp;min<sub>c</sub> max<sub>B</sub>
&Vert;<i>V<sub>B</sub></i>&minus;<i>c</i>&Vert; has worst-case error exactly
rad(<i>S</i>). In one dimension rad(<i>S</i>) = &frac12;(max<sub><i>B</i></sub><i>V<sub>B</sub></i>
&minus; min<sub><i>B</i></sub><i>V<sub>B</sub></i>) and &Gamma;* is the midpoint.
Moreover every averaging rule with fixed weights &pi; has worst-case error
max<sub><i>B</i></sub>|&sum;<sub><i>C</i></sub>&pi;<sub><i>C</i></sub><i>V<sub>C</sub></i>
&minus; <i>V<sub>B</sub></i>| &ge; rad(<i>S</i>), with equality only when the weighted
mean is itself the Chebyshev centre.</p>
</div>
</div>

<p><i>Proof.</i> By Theorem 3 the compatible values form <i>S</i>. Two points of
<i>S</i> at distance 2&nbsp;rad(<i>S</i>) apart exist by the definition of the
Chebyshev radius applied to the finite set {<i>V<sub>B</sub></i>}: choose
<i>V<sub>B</sub></i>* and <i>V<sub>C</sub></i>** attaining the diameter, both of
which lie in <i>S</i>. Any &Gamma; &isin; R<sup><i>d</i></sup> has
max(&Vert;&Gamma;&minus;<i>V<sub>B</sub></i>*&Vert;,
&Vert;&Gamma;&minus;<i>V<sub>C</sub></i>**&Vert;) &ge; &frac12;&Vert;<i>V<sub>B</sub></i>*
&minus; <i>V<sub>C</sub></i>**&Vert; &ge; rad(<i>S</i>). Attainment is the definition
of the Chebyshev centre, which exists because the function
max<sub><i>B</i></sub>&Vert;<i>V<sub>B</sub></i>&minus;<i>c</i>&Vert; is convex and
coercive. The statement about fixed-weight averages follows by taking the two extreme
blocks. In one dimension the Chebyshev centre of a finite set is its midpoint and the
radius is half the range. Appendix A.3 gives the details. &#9633;</p>

<p>Three readings matter.</p>

<p><i>The bound is not loose.</i> Experiment E12 evaluates the minimax rule on 300
random instances and finds its realised worst-case error equal to half the range to
within 8.9&times;10<sup>&minus;16</sup>, and every compatible value inside the hull to
within the same tolerance. A practitioner can therefore use half the range of the
shard values as the error bar of a value-only pipeline with no further analysis:
if the shards report 10 and 30, the honest statement about the merged quantity is
"20 &plusmn; 10", not "20".</p>

<p><i>Equal weighting is never the answer.</i> The mean of the reported values is
admissible only when it coincides with the midpoint of the extremes, which happens
for symmetric configurations and fails otherwise; over the 300 instances the ratio of
its worst-case error to the optimum ranged from 1.000 to 1.463 with mean 1.128. This
is the precise form of the folk observation that averaging shard means is unsafe: the
danger is not bias but the absence of a guarantee.</p>

<p><i>The bound is per merge.</i> If the reported values are themselves results of
earlier merges, the hull argument applies level by level, and the radii add along the
longest path in the merge tree rather than staying bounded. A pipeline that drops
masses at every level therefore degrades with depth, which no amount of care at any
single level can prevent.</p>

<h3>D. A lossy ledger: what quantisation costs</h3>

<p>The opposite extreme is to carry the mass but to store it cheaply. Suppose each
block reports a mass <i>M&#770;<sub>B</sub></i> correct to relative precision
&delta;, that is |<i>M&#770;<sub>B</sub></i> &minus; <i>M<sub>B</sub></i>| &le;
&delta;<i>M<sub>B</sub></i>, and that the service merges the reported pairs naively.
The question is how much of the guarantee survives.</p>

<div class="thm">
<p><span class="t">Theorem 5 (quantised ledger budget).</span></p>
<div class="body">
<p>Let the values have diameter <i>D</i> and let the masses be known to relative
precision &delta; &isin; (0,1). Then for the merged value <i>V&#770;</i> computed from
the rounded masses,</p>
<div class="eq">
|V&#770; &minus; V| &le; D &middot; &delta;/(1 &minus; &delta;),
&nbsp;&nbsp;and&nbsp;&nbsp;
TV(&pi;&#770;, &pi;) &le; &delta;/(1 &minus; &delta;).
<span class="num">(6)</span>
</div>
<p>Both statements are independent of the number of blocks, and neither requires the
rounding errors to be independent or unbiased.</p>
</div>
</div>

<p><i>Proof.</i> Write <i>Z</i> = &sum;<sub><i>B</i></sub><i>M<sub>B</sub></i> and
<i>Z&#770;</i> = &sum;<sub><i>B</i></sub><i>M&#770;<sub>B</sub></i>, so
|<i>Z&#770;</i>&minus;<i>Z</i>| &le; &delta;<i>Z</i> and
<i>Z&#770;</i> &ge; (1&minus;&delta;)<i>Z</i>. For each block,</p>

<div class="eq">
|&pi;&#770;<sub>B</sub> &minus; &pi;<sub>B</sub>| &le;
|M&#770;<sub>B</sub>&minus;M<sub>B</sub>|/Z&#770; +
M<sub>B</sub>|Z&#770;&minus;Z|/(Z Z&#770;) &le;
2&delta;&pi;<sub>B</sub>/(1&minus;&delta;),
</div>

<p>and summing over blocks gives &sum;<sub><i>B</i></sub>|&pi;&#770;<sub><i>B</i></sub>
&minus; &pi;<sub><i>B</i></sub>| &le; 2&delta;/(1&minus;&delta;), half of which is the
total variation. Since <i>V</i> is the expectation of a bounded value under &pi;,
|&sum;<sub><i>B</i></sub>&pi;&#770;<sub><i>B</i></sub><i>V<sub>B</sub></i> &minus;
&sum;<sub><i>B</i></sub>&pi;<sub><i>B</i></sub><i>V<sub>B</sub></i>| &le;
<i>D</i>&nbsp;TV(&pi;&#770;,&pi;) &le; <i>D</i>&delta;/(1&minus;&delta;).
&#9633;</p>

<p>The bound is a worst case over admissible roundings and it is not tight: in
experiment E15 (150 instances per &delta;, four values of &delta; from 0.01 to 0.25)
the maximum observed ratio of measured error to bound was 0.31. I state the
deficiency rather than hide it, and I do not claim the constant is optimal; what the
theorem provides is a usable error bar that does not grow with the number of blocks,
which is the property a builder needs. Figure 2 shows the measured error and the bound
against &delta;.</p>

<figure>
<img src="figures/fig2_quantisation.svg" alt="quantisation error against the certified bound"/>
<figcaption><b>Figure 2.</b> Merge error when the masses are known only to relative
precision &delta;, against the certified bound <i>D</i>&delta;/(1&minus;&delta;) of
Theorem 5. Both axes are logarithmic; each point aggregates 150 random instances.
The measured error tracks the bound's slope in &delta; and stays a factor of three to
four below it, which is the slack of the worst-case analysis and not an error in it.
Source: <i>results/e15_quantisation.json</i>.</figcaption>
</figure>

<p>One corollary is useful in its own right, and it is the reason quantised ledgers
are practical at all. Masses are positive and additive, so their relative rounding
error does not compound when they are summed: if each of <i>k</i> masses carries
relative error at most &delta;, the sum carries relative error at most &delta;, no
matter how the additions are bracketed. Experiment E15 verifies this on a tree
summation with alternating rounding and finds a final relative error of 0.0011 at
&delta; = 0.01 and 0.0111 at &delta; = 0.1, both within the promised envelope.</p>

<h3>E. What this section settles, and what it leaves open</h3>

<p>The section converts a design habit into three statements a system can be held to.
A pipeline that reports values only has an error bar of at least half the range of its
shard values, and the midpoint is the best it can do. A pipeline that reports
(<i>V</i>, <i>W</i>) has no error at all. A pipeline that reports (<i>V</i>,
<i>W</i>) with a quantised mass has the error bar (6). The choice of how much ledger
to keep is therefore a choice of a constant, not a leap of faith.</p>

<p>Three questions are left open, and I state them because they are the ones I would
ask a reviewer to press on. First, the constants are for the worst case over
admissible datasets, and the worst case is attained by adversarial masses; a
distributional or average-case statement, of the kind the mergeable-summaries
literature provides for specific sketches [16], would be more useful in practice and
is not attempted here. Second, the constraint in Theorem 3 is exclusion of the mass
specifically; a broader treatment would ask which <i>other</i> scalar summaries of a
block are lossy, and I can see how to repeat the argument for any summary that is
invariant to the score shift of Theorem 1(vi), but not for arbitrary summaries.
Third, if shards are allowed to communicate adaptively the problem changes into a
communication-constrained estimation problem with its own lower-bound machinery [19],
and the interaction between those bounds and the hull argument here is not worked
out.</p>
'''
