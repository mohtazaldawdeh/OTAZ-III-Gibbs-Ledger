# -*- coding: utf-8 -*-
"""Section III: the algebra of scored-record fusion."""

SEC_III = '''
<h2>III. The algebra of scored-record fusion</h2>

<h3>A. The two slots and what they are called</h3>

<p>Write a record as (<i>v</i>, <i>w</i>) and define the fusion of two records by</p>

<div class="eq">
(v<sub>A</sub>, w<sub>A</sub>) &#8904;<sub>&beta;</sub> (v<sub>B</sub>, w<sub>B</sub>)
= <span style="white-space:nowrap">(</span>
(m<sub>A</sub>v<sub>A</sub> + m<sub>B</sub>v<sub>B</sub>)/(m<sub>A</sub> + m<sub>B</sub>)
&nbsp;|&nbsp; &beta;<sup>&minus;1</sup>ln(m<sub>A</sub> + m<sub>B</sub>)
<span style="white-space:nowrap">)</span>,
<span class="num">(2)</span>
</div>

<p>with <i>m<sub>A</sub></i> = e<sup>&beta;<i>w<sub>A</sub></i></sup> and similarly
for <i>B</i>. The left slot is a mass-weighted mean of values; the right slot is a
scaled log-sum-exp of masses. Everything in this paper follows from two facts about
these slots: the left slot is unchanged when the same constant is added to every
score, and the right slot is additive in masses. It is worth naming the notation
that (2) inherits. The vertical bar and the angle brackets come from the Dirac
bracket, where &lang;&phi;|&psi;&rang; is a sesquilinear form and, when the arguments
are drawn from the same space, an inner product. That reading is tempting and
wrong, and the failure is elementary enough to state as a lemma rather than a
remark.</p>

<h3>B. The bracket is not an inner product</h3>

<p><span class="t">Lemma 1 (no bilinearity).</span> Let
<i>F</i>(<i>v<sub>A</sub></i>, <i>w<sub>A</sub></i>; <i>v<sub>B</sub></i>,
<i>w<sub>B</sub></i>) be the left slot of (2). For &lambda; &ne; 0 and
<i>w<sub>A</sub></i> &ne; <i>w<sub>B</sub></i>,
<i>F</i>(&lambda;<i>v<sub>A</sub></i>, <i>w<sub>A</sub></i>;
<i>v<sub>B</sub></i>, <i>w<sub>B</sub></i>) = &lambda;<i>F</i>(<i>v<sub>A</sub></i>,
<i>w<sub>A</sub></i>; <i>v<sub>B</sub></i>, <i>w<sub>B</sub></i>) fails unless
&lambda; = 1 or <i>v<sub>B</sub></i> = 0. With (<i>v<sub>A</sub></i>, <i>w<sub>A</sub></i>)
= (1, 0.5), (<i>v<sub>B</sub></i>, <i>w<sub>B</sub></i>) = (3, 1.5), &beta; = 1 and
&lambda; = 2, the two sides differ by 2.1932.</p>

<p><i>Proof.</i> Put &alpha; = <i>m<sub>A</sub></i>/(<i>m<sub>A</sub></i>&nbsp;+&nbsp;<i>m<sub>B</sub></i>);
then <i>F</i> = &alpha;<i>v<sub>A</sub></i> + (1&minus;&alpha;)<i>v<sub>B</sub></i>.
Scaling <i>v<sub>A</sub></i> by &lambda; gives &lambda;&alpha;<i>v<sub>A</sub></i> +
(1&minus;&alpha;)<i>v<sub>B</sub></i>, while &lambda;<i>F</i> gives
&lambda;&alpha;<i>v<sub>A</sub></i> + &lambda;(1&minus;&alpha;)<i>v<sub>B</sub></i>.
These agree for every &lambda; only if (1&minus;&alpha;)<i>v<sub>B</sub></i> = 0. The
numerical discrepancy is stored in <i>results/e13_binary_algebra.json</i>. &#9633;</p>

<p>The consequence is not merely notational. A reader who treats the bracket as an
inner product will expect to be able to superpose, to normalise, and to project, and
none of those operations is available. In the remainder of the paper I therefore
write the two slots explicitly as (<i>V</i>, <i>W</i>) and never use the bracket
again. What the operation does have is a clean algebraic description, and it is
worth more than the geometric one it lacks.</p>

<h3>C. The ledger monoid</h3>

<div class="thm">
<p><span class="t">Theorem 1 (the ledger).</span></p>
<div class="body">
<p>Fix &beta; and consider records (<i>v</i>, <i>w</i>) with
<i>v</i> &isin; R<sup><i>d</i></sup>. Then:</p>
<p>(i) &#8904;<sub>&beta;</sub> is commutative;</p>
<p>(ii) &#8904;<sub>&beta;</sub> is associative, and the aggregate of a family
depends only on the multiset of records, not on the order or the bracketing of the
merges;</p>
<p>(iii) &#8904;<sub>&beta;</sub> is not idempotent:
(<i>v</i>, <i>w</i>) &#8904;<sub>&beta;</sub> (<i>v</i>, <i>w</i>) =
(<i>v</i>, <i>w</i> + &beta;<sup>&minus;1</sup>ln&nbsp;2), so a
<i>k</i>-fold duplicate shifts the score by &beta;<sup>&minus;1</sup>ln&nbsp;<i>k</i>
and never changes the value;</p>
<p>(iv) there is no identity element among finite records and the operation is not
invertible;</p>
<p>(v) the map &sigma;(<i>v</i>, <i>w</i>) = (<i>m</i>, <i>mv</i>) is a sufficient
statistic: <i>Z</i> and <i>S</i> = &sum;<sub><i>i</i></sub><i>m<sub>i</sub>v<sub>i</sub></i>
add over merges, and (<i>V</i>, <i>W</i>) is recovered from
(<i>Z</i>, <i>S</i>) by division and logarithm;</p>
<p>(vi) the pair is invariant to a common score shift,
<i>w<sub>i</sub></i> &rarr; <i>w<sub>i</sub></i> + <i>c</i>, which leaves <i>V</i>
and every weight unchanged and shifts <i>W</i> by <i>c</i>.</p>
</div>
</div>

<p><i>Proof.</i> Commutativity is self-evident in (2). For associativity, observe
that the right slot of <i>A</i>&#8904;<i>B</i> is
&beta;<sup>&minus;1</sup>ln(<i>m<sub>A</sub></i>+<i>m<sub>B</sub></i>), so the mass
of an aggregate is the sum of the masses, and the left slot is the mass-weighted mean;
merging the aggregate with <i>C</i> therefore yields mass
<i>m<sub>A</sub></i>+<i>m<sub>B</sub></i>+<i>m<sub>C</sub></i> and the
three-record weighted mean, which is symmetric. Formally, in the coordinates of (v)
the fusion is vector addition and the pair is a function of the sum, so
associativity and commutativity of the operation follow from those of addition.
For (iii), set <i>v<sub>A</sub></i> = <i>v<sub>B</sub></i> = <i>v</i>: the left slot
is <i>v</i> and the right slot is &beta;<sup>&minus;1</sup>ln(2e<sup>&beta;w</sup>) =
<i>w</i> + &beta;<sup>&minus;1</sup>ln&nbsp;2; induction gives the <i>k</i>-fold
claim. For (iv), an identity would need mass zero, which no finite record has, and
&sigma; is many-to-one, so no inverse exists. Part (vi) is immediate from
<i>m<sub>i</sub></i> &rarr; e<sup>&beta;<i>c</i></sup><i>m<sub>i</sub></i>. The full
argument for (ii) and (v) is in Appendix A.1. &#9633;</p>

<p>Four consequences are worth spelling out, because each corresponds to a failure
mode seen in practice.</p>

<p><i>Duplication.</i> Part (iii) says that two identical records are not one record.
If a pipeline de-duplicates before fusing, it changes the score by
&beta;<sup>&minus;1</sup>ln&nbsp;2 per doubling, and through the score it changes
every downstream weight and every decision threshold that consumes the score. The
error is large when &beta; is small: 0.69 nats at &beta; = 1, 6.93 at &beta; = 0.1.
Because the size is known, the defect is fixable; the experiment confirms the
prediction to 2.8&times;10<sup>&minus;17</sup> across three temperatures.</p>

<p><i>Order.</i> Part (ii) is why a distributed merge can be arranged in any tree.
A reviewer might ask why associativity needs proof for an operation that is a
weighted average. The answer is that the two slots interact: the right slot of one
fusion is the score of the next, so associativity of the <i>pair</i> is not the
associativity of a mean, and it fails for the natural alternative in which the score
is carried along unchanged. Experiment E16 merges up to 10,000 records in blocks of
1, 10 and 100 with random tree structures and finds the tree result equal to the
<i>n</i>-ary result to a relative 3.7&times;10<sup>&minus;16</sup>.</p>

<p><i>Distribution.</i> Part (v) says an aggregate is summarised by two numbers per
coordinate, total mass and mass-weighted sum, both additive. A pipeline therefore
merges partial aggregates exactly, in any tree, without revisiting the leaves. This
is the property the mergeable-summaries literature calls mergeability [16, 17], and
the ledger is a linear sketch in exactly their sense. Nothing here is new; what
Section IV adds is the converse direction, namely the price of a summary that is
<i>not</i> of this shape.</p>

<p><i>Gauge.</i> Part (vi) says the score has a free additive constant. That is why
scores from two sources cannot be compared until a common offset is fixed, and why a
system that merges scores produced under different calibrations is silently wrong:
the weights are invariant to the offset but the merged score is not, and the merged
score is what the next merge consumes.</p>

<h3>D. The <i>n</i>-ary form and order independence</h3>

<div class="thm">
<p><span class="t">Theorem 2 (the binary law generates the <i>n</i>-ary form).</span></p>
<div class="body">
<p>For records (<i>v</i><sub>1</sub>, <i>w</i><sub>1</sub>), &hellip;,
(<i>v<sub>n</sub></i>, <i>w<sub>n</sub></i>) with <i>n</i> &ge; 2, every binary
bracketing of &#8904;<sub>&beta;</sub> over the <i>n</i> records yields the pair</p>
<div class="eq">
V = &sum;<sub>i</sub> p<sub>i</sub>v<sub>i</sub>, &nbsp;&nbsp;
W = &beta;<sup>&minus;1</sup> ln &sum;<sub>i</sub> e<sup>&beta;w<sub>i</sub></sup>,
&nbsp;&nbsp; p<sub>i</sub> = e<sup>&beta;w<sub>i</sub></sup>/&sum;<sub>j</sub> e<sup>&beta;w<sub>j</sub></sup>.
<span class="num">(3)</span>
</div>
<p>Consequently a binary implementation, an <i>n</i>-ary implementation and a
tree-structured merge produce the same pair up to floating-point rounding.</p>
</div>
</div>

<p><i>Proof.</i> Induction on <i>n</i>; the case <i>n</i> = 2 is (2). Suppose the
claim holds for a subset <i>S</i> of size <i>n</i>&minus;1, with summary mass
&sum;<sub><i>i</i>&isin;<i>S</i></sub><i>m<sub>i</sub></i> and numerator
&sum;<sub><i>i</i>&isin;<i>S</i></sub><i>m<sub>i</sub>v<sub>i</sub></i>. Fusing with
the remaining record multiplies the mass by e<sup>&beta;<i>w<sub>n</sub></i></sup>
and adds the corresponding numerator, which is the <i>n</i>-ary expression.
Associativity (Theorem 1(ii)) removes the dependence on bracketing. &#9633;</p>

<p>Numerically, (3) is not evaluated as printed, for the reason given in Section II.B;
the library shifts by the maximum score. The identity also settles a design question
that is otherwise arbitrary: an aggregate that carries <i>Z</i> can be merged with
another aggregate without knowing how many records either contains, because
<i>Z</i> is the sufficient statistic and e<sup>&beta;W</sup> recovers it. An aggregate
that carries only <i>V</i> cannot be merged at all without an assumption. That
asymmetry is Theorem 1(v) read as an interface, and Section IV quantifies the
assumption.</p>

<table>
<caption><b>Table 1.</b> Algebraic checklist for the operation of (2), with the
measurement that produced each verdict. Source:
<i>results/e13_binary_algebra.json</i>, <i>results/e16_tree_merge.json</i>.</caption>
<thead><tr><th>Property</th><th>Holds</th><th>Evidence</th></tr></thead>
<tbody>
<tr><td>Commutative</td><td>yes</td><td>max defect 5.6&times;10<sup>&minus;16</sup>, 200 random pairs</td></tr>
<tr><td>Associative, both slots</td><td>yes</td><td>max gap to the <i>n</i>-ary form 8.9&times;10<sup>&minus;16</sup>, 300 triples</td></tr>
<tr><td>Tree merging equals <i>n</i>-ary merging</td><td>yes</td><td>relative gap 3.7&times;10<sup>&minus;16</sup> up to 10<sup>4</sup> records</td></tr>
<tr><td>Idempotent</td><td><b>no</b></td><td>offset &beta;<sup>&minus;1</sup>ln 2, residual &le; 2.8&times;10<sup>&minus;17</sup></td></tr>
<tr><td>Homogeneous in the value</td><td><b>no</b></td><td>discrepancy 2.19 at &lambda; = 2</td></tr>
<tr><td>Has an identity element</td><td><b>no</b></td><td>would require zero mass</td></tr>
<tr><td>Invertible</td><td><b>no</b></td><td>the sufficient statistic is many-to-one</td></tr>
<tr><td>Invariant to a common score shift</td><td>yes (value), shift (score)</td><td>Theorem 1(vi)</td></tr>
</tbody>
</table>
'''
