# -*- coding: utf-8 -*-
"""Appendices and references."""

APPENDIX_A = '''
<h2>Appendix A. Proofs</h2>

<p>Proofs are given for the results whose arguments are not a one-line citation. Notation
is that of Section II: records <i>i</i> = 1,&hellip;,<i>n</i> with scores
<i>w<sub>i</sub></i>, values <i>v<sub>i</sub></i>, weights
<i>p<sub>i</sub></i> = <i>e</i><sup>&beta;<i>w<sub>i</sub></i></sup>/<i>Z</i>,
<i>Z</i> = &sum;<sub><i>i</i></sub><i>e</i><sup>&beta;<i>w<sub>i</sub></i></sup>,
aggregate value <i>V</i> = &sum;<sub><i>i</i></sub><i>p<sub>i</sub>v<sub>i</sub></i> and
aggregate score <i>W</i> = &beta;<sup>&minus;1</sup>ln&nbsp;<i>Z</i>.</p>

<h3>A.1 Theorem 1 (ii) and (v): the merge laws</h3>

<p><i>(ii).</i> Write <i>S</i> = &sum;<sub><i>i</i></sub><i>e</i><sup>&beta;<i>w<sub>i</sub></i></sup><i>v<sub>i</sub></i>.
For two disjoint record sets <i>A</i>, <i>B</i> the partition functions and values sums
add, <i>Z</i><sub><i>A</i>&cup;<i>B</i></sub> = <i>Z<sub>A</sub></i>+<i>Z<sub>B</sub></i>
and <i>S</i><sub><i>A</i>&cup;<i>B</i></sub> = <i>S<sub>A</sub></i>+<i>S<sub>B</sub></i>,
because the defining sums are over disjoint index sets. Hence
<i>V</i><sub><i>A</i>&cup;<i>B</i></sub> = (<i>S<sub>A</sub></i>+<i>S<sub>B</sub></i>)/(<i>Z<sub>A</sub></i>+<i>Z<sub>B</sub></i>),
which is the weighted mean of <i>V<sub>A</sub></i> and <i>V<sub>B</sub></i> with weights
<i>Z<sub>A</sub></i>, <i>Z<sub>B</sub></i>. Commutativity and associativity follow because
addition in the two components is commutative and associative. A formal neutral
element would be (<i>Z</i>, <i>S</i>) = (0, 0), that is <i>W</i> = &minus;&infin; with
an empty record set; no non-empty record set attains it, because <i>Z</i> &gt; 0
whenever a record exists. The structure is therefore a commutative monoid whose identity
is not an element of the carrier set, and it is not a group. &#9633;</p>

<p><i>(v).</i> Fix a record set and consider the map &beta; &rarr;
(<i>W</i>, <i>V</i>). By the previous part the pair is additive over disjoint unions and
determined by <i>n</i> + 2 scalars, so it is a sufficient statistic of fixed dimension in
the sense of exponential families [18]. The sufficiency is with respect to the family
obtained by reweighting records by <i>e</i><sup>&beta;<i>w</i></sup>, which is exactly the
family in which the data enter. &#9633;</p>

<h3>A.2 Theorem 3: the reachable set is the convex hull</h3>

<p>Let there be <i>k</i> blocks with reported pairs (<i>V<sub>j</sub></i>,
<i>n<sub>j</sub></i>), <i>j</i> = 1,&hellip;,<i>k</i>, and let <i>V</i> be the true global
aggregate. Because <i>V</i> = &sum;<sub><i>j</i></sub>(<i>Z<sub>j</sub></i>/<i>Z</i>)<i>V<sub>j</sub></i>
with <i>Z</i> = &sum;<sub><i>j</i></sub><i>Z<sub>j</sub></i> and <i>Z<sub>j</sub></i> &gt; 0,
every attainable <i>V</i> is a convex combination of the reported values, so the reachable
set is contained in conv{<i>V<sub>1</sub></i>,&hellip;,<i>V<sub>k</sub></i>}.</p>

<p>For the reverse inclusion let <i>m</i> lie in the relative interior of the simplex and
put <i>Z<sub>j</sub></i> = <i>m<sub>j</sub>Z</i> for an arbitrary <i>Z</i> &gt; 0. It
remains to see that masses <i>Z<sub>j</sub></i> with the given <i>V<sub>j</sub></i> are
realisable by actual records. Take a single record per block with value
<i>v<sub>j</sub></i> = <i>V<sub>j</sub></i>; its partition function is
<i>e</i><sup>&beta;<i>w<sub>j</sub></i></sup>, which equals any prescribed positive number
for the score <i>w<sub>j</sub></i> = &beta;<sup>&minus;1</sup>ln&nbsp;<i>Z<sub>j</sub></i>.
Hence every interior point, and by closure every boundary point, is attainable, and the
reachable set is the hull. Note that the construction uses one record per block, so the
undetermination is not a consequence of small blocks; it persists for blocks of any
size. &#9633;</p>

<p><i>Remark.</i> The argument shows exactly which extra scalar removes the ambiguity: the
mass <i>Z<sub>j</sub></i>, or any strictly monotone transform of it. Two values plus two
masses determine the merge; two values alone determine nothing beyond the hull.</p>

<h3>A.3 Theorem 4: the minimax rule is the midpoint, and the constant is sharp</h3>

<p>Write <i>a</i> = min<sub><i>j</i></sub><i>V<sub>j</sub></i> and
<i>b</i> = max<sub><i>j</i></sub><i>V<sub>j</sub></i>, so the reachable set is
<i>C</i> = [<i>a</i>, <i>b</i>] by Theorem 3. For an estimate <i>c</i> the worst-case
absolute error over <i>C</i> is max(<i>b</i>&minus;<i>c</i>, <i>c</i>&minus;<i>a</i>),
which is minimised when the two terms are equal, that is at <i>c</i> = (<i>a</i>+<i>b</i>)/2,
where the value is (<i>b</i>&minus;<i>a</i>)/2. This is the Chebyshev centre of an interval
and the argument is elementary. For sharpness, take the admissible masses
<i>m</i> = <i>e<sub>j</sub></i> concentrated on the block attaining <i>a</i>, and then on
the block attaining <i>b</i>: both are attainable by A.2, and at them the error of the
midpoint equals exactly half the range. Hence no rule does better in the worst case, and
the midpoint does no worse. &#9633;</p>

<p><i>Remark.</i> In more than one dimension the same argument gives the radius of the
smallest Euclidean ball containing the hull, which is the Chebyshev radius and is not in
general attained by a simple formula; the diameter bounds it and is not sharp. This is why
the theorem is stated for scalar aggregates.</p>

<h3>A.4 Theorem 6: the temperature calculus</h3>

<p>Differentiating ln&nbsp;<i>Z</i> with respect to &beta; gives
&sum;<sub><i>i</i></sub><i>p<sub>i</sub>w<sub>i</sub></i>, and differentiating again gives
&sum;<sub><i>i</i></sub><i>p<sub>i</sub>w<sub>i</sub></i><sup>2</sup> &minus;
(&sum;<sub><i>i</i></sub><i>p<sub>i</sub>w<sub>i</sub></i>)<sup>2</sup>, which is
Var<sub><i>p</i></sub>(<i>w</i>). The third derivative is the third cumulant of <i>w</i>
under <i>p</i> by the same computation, since the cumulant generating function of <i>w</i>
under <i>p</i> is ln&nbsp;&sum;<sub><i>i</i></sub><i>p<sub>i</sub>e</i><sup><i>tw<sub>i</sub></i></sup>
and its derivatives at zero are the cumulants. For the value, differentiate
<i>V</i> = &sum;<sub><i>i</i></sub><i>p<sub>i</sub>v<sub>i</sub></i> using
&part;<i>p<sub>i</sub></i>/&part;&beta; = <i>p<sub>i</sub></i>(<i>w<sub>i</sub></i> &minus;
&sum;<sub><i>l</i></sub><i>p<sub>l</sub>w<sub>l</sub></i>), which is the score's deviation
from its mean. Collecting terms gives
d<i>V</i>/d&beta; = &sum;<sub><i>i</i></sub><i>p<sub>i</sub>v<sub>i</sub>w<sub>i</sub></i>
&minus; (&sum;<sub><i>i</i></sub><i>p<sub>i</sub>v<sub>i</sub></i>)(&sum;<sub><i>i</i></sub><i>p<sub>i</sub>w<sub>i</sub></i>)
= Cov<sub><i>p</i></sub>(<i>v</i>, <i>w</i>). Convexity of &beta; &rarr; ln&nbsp;<i>Z</i>
is Var<sub><i>p</i></sub>(<i>w</i>) &ge; 0, and monotonicity of &beta; &rarr; <i>V</i> is
the sign of that covariance. &#9633;</p>

<h3>A.5 Theorem 7: the coarse-graining gap is an entropy</h3>

<p>Let the record set be partitioned into blocks <i>B</i> with masses
&pi;<sub><i>B</i></sub> = <i>Z<sub>B</sub></i>/<i>Z</i> and block scores
<i>W<sub>B</sub></i> = &beta;<sup>&minus;1</sup>ln&nbsp;<i>Z<sub>B</sub></i>. The exact
score of the union satisfies ln&nbsp;<i>Z</i> = ln&nbsp;&sum;<sub><i>B</i></sub><i>Z<sub>B</sub></i>,
so</p>

<div class="eq">
<i>W</i> &minus; &sum;<sub><i>B</i></sub>&pi;<sub><i>B</i></sub><i>W<sub>B</sub></i>
= &beta;<sup>&minus;1</sup>[ln&nbsp;<i>Z</i> &minus; &sum;<sub><i>B</i></sub>&pi;<sub><i>B</i></sub>ln&nbsp;<i>Z<sub>B</sub></i>]
= &beta;<sup>&minus;1</sup><i>H</i>(&pi;),
<span class="num">(A.1)</span>
</div>

<p>because &sum;<sub><i>B</i></sub>&pi;<sub><i>B</i></sub>ln&nbsp;&pi;<sub><i>B</i></sub>
= &sum;<sub><i>B</i></sub>(<i>Z<sub>B</sub></i>/<i>Z</i>)ln(<i>Z<sub>B</sub></i>/<i>Z</i>),
and the rearrangement of the two logarithms gives the stated entropy. Non-negativity is
Gibbs' inequality, and <i>H</i>(&pi;) &le; ln&nbsp;<i>k</i> for <i>k</i> blocks with
equality at uniform masses. Dividing by &beta; gives the stated bound
&beta;<sup>&minus;1</sup>ln&nbsp;<i>k</i>. &#9633;</p>

<p><i>Remark.</i> The gap is an entropy and not a divergence, and the distinction is not
cosmetic: a divergence would vanish when the block structure is trivial for every
temperature, whereas <i>H</i>(&pi;) is a genuine information loss at every &beta; and is
independent of the values.</p>

<h3>A.6 Theorem 8: the chain rule, and the singleton case</h3>

<p>For a two-level partition with blocks <i>A</i> and then sub-blocks inside each, the
Shannon chain rule gives
<i>H</i>(&pi;) = <i>H</i>(&pi;<sup>top</sup>) + &sum;<sub><i>a</i></sub>&pi;<sub><i>a</i></sub><i>H</i>(&pi;<sup>sub</sup><sub><i>a</i></sub>)
[2, ch. 2]. Applying (A.1) at each level and adding shows that the coarse-graining gap is
additive along the hierarchy, so a tree-shaped summary loses exactly the sum of the
level entropies. If the finest level consists of singletons, then
<i>H</i>(&pi;<sup>sub</sup><sub><i>a</i></sub>) is the conditional entropy of the record
given its block, and the total gap is the entropy of the normalised weights,
&beta;<sup>&minus;1</sup><i>H</i>(<i>p</i>), which is the maximum information a summary
that keeps only block aggregates can lose. &#9633;</p>

<h3>A.7 Theorem 9: the logit parametrisation does not amplify error</h3>

<p>Let <i>p</i> and <i>q</i> be weight vectors with <i>q<sub>i</sub></i> proportional to
<i>p<sub>i</sub></i>(1+&delta;<sub><i>i</i></sub>) and |&delta;<sub><i>i</i></sub>| &le;
&epsilon; &lt; 1, which is what a relative error &epsilon; in the exponentiated scores
produces. Write <i>N</i> = &sum;<sub><i>i</i></sub><i>p<sub>i</sub></i>(1+&delta;<sub><i>i</i></sub>),
so that |<i>N</i>&minus;1| &le; &epsilon; and hence 1/<i>N</i> &le; 1/(1&minus;&epsilon;).
Then</p>

<div class="eq">
&frac12;&Vert;<i>q</i>&minus;<i>p</i>&Vert;<sub>1</sub>
= &frac12;&sum;<sub><i>i</i></sub><i>p<sub>i</sub></i>|(1+&delta;<sub><i>i</i></sub>)/<i>N</i> &minus; 1|
&le; &frac12;[(&sum;<sub><i>i</i></sub><i>p<sub>i</sub></i>|&delta;<sub><i>i</i></sub>|)/<i>N</i> + |1/<i>N</i> &minus; 1|]
&le; &epsilon;/(1&minus;&epsilon;),
<span class="num">(A.2)</span>
</div>

<p>where the last step uses 1/<i>N</i> &le; 1/(1&minus;&epsilon;) and
|1/<i>N</i>&minus;1| &le; &epsilon;/(1&minus;&epsilon;). The amplification factor is
therefore one over one minus epsilon, which is close to one for small errors and diverges
only as &epsilon; &rarr; 1. &#9633;</p>

<h3>A.8 Theorem 10: sampling and truncation compose</h3>

<p>Let <i>p</i> and <i>q</i> be the true and the estimated weights, with
TV(<i>p</i>,<i>q</i>) &le; &eta;. Since <i>V</i>(<i>p</i>) &minus; <i>V</i>(<i>q</i>) =
&sum;<sub><i>i</i></sub>(<i>p<sub>i</sub></i>&minus;<i>q<sub>i</sub></i>)<i>v<sub>i</sub></i>,
which is a bounded linear functional of the difference, its modulus is at most
(max<sub><i>i</i></sub><i>v<sub>i</sub></i> &minus; min<sub><i>i</i></sub><i>v<sub>i</sub></i>)
&middot; TV(<i>p</i>,<i>q</i>), after recentring the values, since the difference sums to
zero. That gives the multiplier <i>D</i> equal to the range of the values, and the
composition of two error sources by the triangle inequality, truncated at one because a
probability is being bounded. Combining with (A.2) for the truncation of the score tail
gives</p>

<div class="eq">
|<i>V</i>&#770; &minus; <i>V</i>| &le; <i>D</i> &middot; min(1, &tau;&#770; + &epsilon;/(1&minus;&epsilon;)),
<span class="num">(A.3)</span>
</div>

<p>with &tau;&#770; the estimated sampling error and &epsilon; the truncation level. The
minimum is taken because the right-hand side is a bound on a total-variation distance,
which cannot exceed one. &#9633;</p>

<h3>A.9 Lemma 2: diagonal states</h3>

<p>For &rho; = diag(<i>p</i>) and &sigma; = diag(<i>q</i>), the difference is diagonal with
entries <i>p<sub>i</sub></i>&minus;<i>q<sub>i</sub></i>, so the trace norm is
&sum;<sub><i>i</i></sub>|<i>p<sub>i</sub></i>&minus;<i>q<sub>i</sub></i>| and the first
identity follows after halving. The spectral decomposition of a diagonal matrix is its
entrywise decomposition, so the von Neumann entropy &minus;tr(&rho;&nbsp;ln&nbsp;&rho;)
equals &minus;&sum;<sub><i>i</i></sub><i>p<sub>i</sub></i>ln&nbsp;<i>p<sub>i</sub></i>.
For the error probability, the Helstrom expression for two states with equal priors is
(1&minus;&frac12;&Vert;&rho;&minus;&sigma;&Vert;<sub>1</sub>)/2 [5], which with the first
identity becomes (1&minus;TV)/2. &#9633;</p>

<h3>A.10 Theorem 12, verified numerically</h3>

<p>The counterexample of Section VIII is the pair of four-dimensional vectors
<i>u</i> = &frac12;(1,1,1,1) and <i>s</i> = &frac12;(1,1,&minus;1,&minus;1), both of unit
norm and mutually orthogonal. Their outer products have diagonal entries &frac14; in every
position, so the dephased states coincide exactly. Evaluating the trace distance of the
dephased pair gives 0.0 to machine precision and of the pure pair gives 1.0 to machine
precision, a difference of exactly one. The code that performs this check constructs the
states from the vectors rather than from stored matrices, so the agreement is not a
consequence of the stored artefact. &#9633;</p>
'''

APPENDIX_B = '''
<h2>Appendix B. Stored scalars</h2>

<p>Every number quoted in the text is recoverable from the files below. The residuals are
absolute deviations from the predicted identity in the units of the quantity concerned;
the worst-case columns are maxima over the stated instance count.</p>

<table>
<caption><b>Table B.1.</b> Scalars quoted in the text and the file that stores them.</caption>
<thead><tr><th>Quantity</th><th>Value</th><th>File</th></tr></thead>
<tbody>
<tr><td>Master seed</td><td>2026110101</td><td>all</td></tr>
<tr><td>softmax reconstruction error, max over 400</td><td>2.2&times;10<sup>&minus;16</sup></td><td>e1_representability.json</td></tr>
<tr><td>temperature identity residuals (three derivatives)</td><td>2.98&times;10<sup>&minus;9</sup>, 2.77&times;10<sup>&minus;9</sup>, 8.47&times;10<sup>&minus;7</sup></td><td>e2_temperature_calculus.json</td></tr>
<tr><td>coarse-graining residual, max over 320</td><td>2.2&times;10<sup>&minus;15</sup></td><td>e3_coarse_graining.json</td></tr>
<tr><td>sharp gap at &beta; = 1.5 with eight blocks</td><td>ln&nbsp;8/1.5 = 1.3862943611</td><td>e3_coarse_graining.json</td></tr>
<tr><td>mean realised gap over 320 instances</td><td>1.3063</td><td>e3_coarse_graining.json</td></tr>
<tr><td>chain-rule residual; entropy identity residual</td><td>8.9&times;10<sup>&minus;16</sup>; 1.8&times;10<sup>&minus;15</sup></td><td>e4_hierarchy.json</td></tr>
<tr><td>minimum excess in the pure-state inequality</td><td>8.6&times;10<sup>&minus;5</sup></td><td>e5_quantum_boundary.json</td></tr>
<tr><td>coherence contribution to trace distance, mean</td><td>0.314</td><td>e11_dephasing.json</td></tr>
<tr><td>Helstrom floor: smallest slack over 400</td><td>1.2&times;10<sup>&minus;5</sup></td><td>e6_helstrom.json</td></tr>
<tr><td>Helstrom floor: mean slack at &beta; = 8</td><td>0.235</td><td>e6_helstrom.json</td></tr>
<tr><td>bootstrap coverage, eight cells</td><td>0.892&ndash;0.983</td><td>e7_sampling.json</td></tr>
<tr><td>saturated certificate at &beta; = 3, m = 10</td><td>1.6267 against error 0.1017</td><td>e7_sampling.json</td></tr>
<tr><td>von Neumann&ndash;Shannon residual, max over 200</td><td>4.4&times;10<sup>&minus;16</sup></td><td>e8_entropies.json</td></tr>
<tr><td>logit non-amplification: minimum slack</td><td>0.0197</td><td>e9_nonamplification.json</td></tr>
<tr><td>composed certificate: median ratio, max ratio</td><td>0.056, 0.308</td><td>e10_pipeline.json</td></tr>
<tr><td>dephasing: mean full, diagonal, coherence parts</td><td>0.562 = 0.248 + 0.314</td><td>e11_dephasing.json</td></tr>
<tr><td>hull fraction; max violation</td><td>1.000; &minus;6.4&times;10<sup>&minus;8</sup></td><td>e12_impossibility.json</td></tr>
<tr><td>worked example: two values and the gap</td><td>3.3333 vs 4.8786; gap 1.5452</td><td>e12_impossibility.json</td></tr>
<tr><td>minimax: max deviation from half the range</td><td>8.9&times;10<sup>&minus;16</sup></td><td>e12_impossibility.json</td></tr>
<tr><td>equal weighting vs minimax: mean, max ratio</td><td>1.1277, 1.4634</td><td>e12_impossibility.json</td></tr>
<tr><td>idempotence defect; homogeneity defect at &lambda; = 2</td><td>&beta;<sup>&minus;1</sup>ln&nbsp;2; 2.1932</td><td>e13_binary_algebra.json</td></tr>
<tr><td>worked example at &beta; = 1</td><td><i>V</i> = 10.5586, <i>W</i> = 2.2331</td><td>e14_worked_example.json</td></tr>
<tr><td>d<i>V</i>/d&beta; at &beta; = 1; effective record count</td><td>&minus;0.108319; 4.812</td><td>e14_worked_example.json</td></tr>
<tr><td>skewness peak</td><td>17.8629 at &beta; = 0.1543</td><td>e14_worked_example.json</td></tr>
<tr><td>quantisation: violations; max error/bound</td><td>0 of 600; 0.31</td><td>e15_quantisation.json</td></tr>
<tr><td>quantisation: mass chain at &delta; = 0.01, 0.1</td><td>0.00111, 0.01111</td><td>e15_quantisation.json</td></tr>
<tr><td>tree merging: max relative value gap; score gap</td><td>3.7&times;10<sup>&minus;16</sup>; 0</td><td>e16_tree_merge.json</td></tr>
</tbody>
</table>
'''

APPENDIX_C = '''
<h2>Appendix C. Repository manifest</h2>

<table>
<caption><b>Table C.1.</b> Contents of the deposit. The SHA-256 manifest is
authoritative for what is present; this table says what each path is for.</caption>
<thead><tr><th>Path</th><th>Contents</th></tr></thead>
<tbody>
<tr><td>otaz_quantum/core.py</td><td>the reference implementation: primitives, the binary and <i>n</i>-ary algebra, the temperature calculus, coarse-graining and hierarchy, the ledger (impossibility, minimax, quantisation, tree merging), the quantum interface, sampling</td></tr>
<tr><td>experiments/otaz_run_quantum.py</td><td>the sixteen experiments, seeded, writing nineteen JSON files</td></tr>
<tr><td>tests/test_core.py</td><td>fifty-two unit tests, including seven for the ledger statements</td></tr>
<tr><td>scripts/otaz_verify_quantum.py</td><td>fifty-six independent checks; does not import the library</td></tr>
<tr><td>scripts/otaz_checksums.py</td><td>writes and verifies the SHA-256 manifest</td></tr>
<tr><td>otaz_make_figures.py</td><td>the eight figures, in SVG and PNG, black line art only</td></tr>
<tr><td>otaz_make_cover.py</td><td>the deposit cover sheet</td></tr>
<tr><td>paper/</td><td>this manuscript as HTML plus the builder, the two style sheets and the section modules sec_1_front to sec_8_appendix</td></tr>
<tr><td>results/</td><td>nineteen JSON files, each with the property, the instance count, the residuals and a verdict</td></tr>
<tr><td>figures/</td><td>fig1&ndash;fig8 in SVG and PNG</td></tr>
<tr><td>publication/</td><td>the built PDFs, the cover sheet, the one-page Arabic novelty assessment (<i>OTAZ_III_Novelty_Assessment_AR</i>, with its HTML source and build script), metadata and the deposit archives</td></tr>
<tr><td>docs/</td><td>reading guide, release steps and the colour policy</td></tr>
<tr><td>README.md, CHANGELOG.md, CITATION.cff</td><td>orientation, version history and citation record</td></tr>
</tbody>
</table>

<p>Licensing: the text and the results are released under CC BY-NC 4.0; the code is
released under the PolyForm Noncommercial License 1.0.0. Neither permits commercial use,
which is deliberate. The repository contains no third-party data.</p>
'''

REFERENCES = '''
<h2>References</h2>
<div class="refs">
<p>[1] A.-M. B. S. Al-Dawoodiya, &ldquo;OTAZ: Exponentially Weighted Fusion &mdash;
Algebraic Structure, Numerical Stability, and Reproducible Experiments,&rdquo; preprint,
Zenodo, 2026, DOI 10.5281/zenodo.23648070. [Companion report: the duplication defect and
the total-variation bound composed in Corollary 1 originate there.]</p>
<p>[2] T. M. Cover and J. A. Thomas, <i>Elements of Information Theory</i>, 2nd ed.
Hoboken, NJ: Wiley, 2006. [Entropy bounds, the chain rule, the maximum-entropy
principle.]</p>
<p>[3] S. Boyd and L. Vandenberghe, <i>Convex Optimization</i>. Cambridge, U.K.: Cambridge
University Press, 2004. [Convexity of the log-partition function; log-sum-exp as a smooth
maximum.]</p>
<p>[4] M. A. Nielsen and I. L. Chuang, <i>Quantum Computation and Quantum Information</i>.
Cambridge, U.K.: Cambridge University Press, 2000. [Trace distance, fidelity,
pinching.]</p>
<p>[5] C. W. Helstrom, <i>Quantum Detection and Estimation Theory</i>. New York: Academic
Press, 1976. [Minimum error probability for two states with equal priors.]</p>
<p>[6] R. Bhatia, <i>Matrix Analysis</i>. New York: Springer, 1997. [Pinching inequality
and trace-norm inequalities.]</p>
<p>[7] R. T. Rockafellar and R. J.-B. Wets, <i>Variational Analysis</i>. Berlin: Springer,
1998. [Conjugacy and smoothness of the log-sum-exp function; the convex-analytic reading
of Theorem 6.]</p>
<p>[8] P. Blanchard, N. J. Higham, and T. Higham, &ldquo;Accurately computing the
log-sum-exp and softmax functions,&rdquo; <i>IMA Journal of Numerical Analysis</i>,
vol. 41, no. 4, pp. 2311&ndash;2330, 2021, doi:10.1093/imanum/draa038.</p>
<p>[9] M. Milakov and N. Gimelshein, &ldquo;Online normalizer calculation for
softmax,&rdquo; arXiv:1805.02867, 2018. [One-pass streaming evaluation of the partition
sum.]</p>
<p>[10] S. Cohen and V. Fausti, &ldquo;Hilbert metric and total variation in probability
measures,&rdquo; arXiv:2309.02413, 2023. [Sharp total-variation bounds via the Hilbert
metric.]</p>
<p>[11] S. Somasundaram, C. Guille-Escuret, J. M. Moreno, E. Liu, and E. Xing,
&ldquo;Softmax geometry and the Hilbert metric,&rdquo; arXiv:2610.17588, 2026.
[Contemporary treatment of the same bound; cited to avoid a priority claim.]</p>
<p>[12] X. Wang, R. J. Hyndman, B. Li, and Y. Kang, &ldquo;Forecast combinations: an over
50-year review,&rdquo; arXiv:2205.04216, 2022. [Why equal weighting is a hard baseline;
what truncation does to a combined forecast.]</p>
<p>[13] B. Efron and R. J. Tibshirani, <i>An Introduction to the Bootstrap</i>. New York:
Chapman &amp; Hall, 1993. [The resampling procedure of the coverage study.]</p>
<p>[14] T. Weissman, E. Ordentlich, G. Seroussi, S. Verd&uacute;, and M. J. Weinberger,
&ldquo;Inequalities for the <i>L</i><sub>1</sub> deviation of the empirical
distribution,&rdquo; Hewlett-Packard Laboratories Technical Report HPL-2003-97R1, 2003.
[The statistical background to the sampling certificate.]</p>
<p>[15] C. R. Harris <i>et al.</i>, &ldquo;Array programming with NumPy,&rdquo;
<i>Nature</i>, vol. 585, pp. 357&ndash;362, 2020. [Software.]</p>
<p>[16] P. K. Agarwal, G. Cormode, Z. Huang, J. M. Phillips, Z. Wei, and K. Yi,
&ldquo;Mergeable summaries,&rdquo; <i>ACM Transactions on Database Systems</i>, vol. 38,
no. 4, art. 26, 2013. [Formal mergeability; positive and negative results for concrete
summaries; the frame for Theorem 3.]</p>
<p>[17] G. Cormode, &ldquo;Data sketching,&rdquo; <i>Communications of the ACM</i>,
vol. 60, no. 9, pp. 48&ndash;55, 2017. [Linear sketches and their mergeability; why the
ledger is one.]</p>
<p>[18] M. J. Wainwright and M. I. Jordan, &ldquo;Graphical models, exponential families,
and variational inference,&rdquo; <i>Foundations and Trends in Machine Learning</i>,
vol. 1, no. 1&ndash;2, pp. 1&ndash;305, 2008. [Additive sufficient statistics; the
Gibbs variational principle; the content of Theorems 1 and 7.]</p>
<p>[19] Y. Zhang, J. C. Duchi, M. I. Jordan, and M. J. Wainwright,
&ldquo;Information-theoretic lower bounds for distributed statistical estimation with
communication constraints,&rdquo; in <i>Advances in Neural Information Processing
Systems</i>, 2013. [Minimax rates as a function of a bit budget; the template for the
lower-bound side of Theorem 3.]</p>
<p>[20] R. A. Jacobs, M. I. Jordan, S. J. Nowlan, and G. E. Hinton, &ldquo;Adaptive
mixtures of local experts,&rdquo; <i>Neural Computation</i>, vol. 3, no. 1, pp. 79&ndash;87,
1991. [Soft gating; the gate logit in the role of the score.]</p>
<p>[21] G. E. Hinton, &ldquo;Training products of experts by minimizing contrastive
divergence,&rdquo; <i>Neural Computation</i>, vol. 14, no. 8, pp. 1771&ndash;1800, 2002.
[Products of experts; the same log-domain arithmetic.]</p>
<p>[22] S. Thrun, W. Burgard, and D. Fox, <i>Probabilistic Robotics</i>. Cambridge, MA:
MIT Press, 2005. [Particle filters carry log-weights and compose them by this recursion;
the fused score is the estimated log-evidence.]</p>
</div>
'''
