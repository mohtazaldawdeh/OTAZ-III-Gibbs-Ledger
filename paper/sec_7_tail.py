# -*- coding: utf-8 -*-
"""Sections XI-XIV, appendices and references."""

SEC_XI = '''
<h2>XI. Engineering implications</h2>

<h3>A. What a system should carry</h3>

<p>The theorem of Section IV converts into a design rule that is cheap to state. A
shard that reports a fused value must also report the mass it normalised by, and the
pair must be sufficient statistics of the aggregate: the partition sum <i>Z</i>
together with the mass-weighted sum
<i>S</i> = &sum;<sub><i>i</i></sub><i>e</i><sup>&beta;<i>w<sub>i</sub></i></sup><i>v<sub>i</sub></i>,
or equivalently the pair (ln&nbsp;<i>Z</i>, <i>V</i>), since the two forms are related
by a division and a logarithm. A
shard that reports only a value is not merging; it is approximating, and Section IV
gives the size of the approximation error. The cost of the extra number is one float
per shard, and the benefit is that the merge is exact rather than bounded.</p>

<p>Three implementation details, each of which I have seen go wrong. The merge must be
done in the log domain with a shift by the running maximum, or overflow defeats the
purpose of carrying a log-mass at all [8]; the streaming form of the running partition
sum removes the two-pass requirement [9]. The score must be accumulated in a type wide
enough for the record count &mdash; at 10<sup>9</sup> records and scores of order one,
float32 loses the low bits of the sum, and Theorem 9 gives the exact exchange rate
between that loss and the error in the weights. And the value must be summed in the
same pass as the weights, because the identity that makes the pair a sufficient
statistic assumes both are taken over the same record set; a shard that filters records
between the two passes silently produces a pair that no mass correction can repair.</p>

<h3>B. Choosing between the ledger and the impossibility theorem</h3>

<p>The two results in Section IV point in opposite directions and a practitioner has to
choose. If shards can be changed, carry the mass: error zero, one extra float, no
statistics needed. If shards cannot be changed &mdash; a legacy export, a third-party
model, a logging format nobody will alter &mdash; then the value-only merge is what is
available, and the honest report is an interval of width equal to the range of the shard
values, with the midpoint as the point estimate. Reporting a single number in that
situation with a confidence interval computed as though the merge were exact is the
failure mode Theorem 4 forbids, and it is a common one.</p>

<p>There is a middle option worth naming because it is often available in practice. If
each shard can report one extra scalar in addition to its value &mdash; not the mass
itself but a coarse summary of it, such as a bucket index on a logarithmic scale &mdash;
then Theorem 5 applies with &delta; equal to the bucket width, and the merge error
becomes <i>D</i>&delta;/(1&minus;&delta;) regardless of shard count. The measured worst
case in E15 was a factor of three inside the bound, which suggests that eight to sixteen
logarithmic buckets are enough for four-digit accuracy in the merged value; that is an
engineering statement from one experiment and not a theorem.</p>

<h3>C. Where the certificates belong in a pipeline</h3>

<p>A certificate that is computed after deployment and stored in a log is decoration. The
placement that matters is before the merge, in the sense that the shot count should be
chosen from the target error rather than the error reported from the shot count. That is
the inversion Algorithm 3 performs: given a target &tau; and a truncation bound, solve for
the number of samples and the bucket count that make the composed bound (11) fall below
&tau;. In the worked numbers of Section VII that inversion costs a few hundred samples for
a percent-level target at moderate &beta;, which is small compared to the cost of the
records being summarised. The exception is the regime the limitation section names: at
high &beta; the bound saturates and no sample count rescues it, because the probability
of drawing the dominant record at all is what the bound is measuring.</p>
'''

SEC_XII = '''
<h2>XII. Limitations</h2>

<p>Nine limitations, in the order in which they would trouble a reader who wanted to use
this work.</p>

<ol>
<li><b>The certificate saturates.</b> At high &beta; and few samples, &epsilon;
approaches one and (11) says nothing; the measured certificate at &beta; = 3 with ten
shots was 1.63, larger than any achievable error. A saturating bound is honest and
useless in equal measure, and the remedy is planning rather than reporting: fix the shot
count from the target error before deployment, as Algorithm 3 does.</li>

<li><b>Bootstrap coverage is below nominal.</b> In two of eight cells the interval
covered 0.892 and 0.900 against a nominal 0.95, which is about two standard errors low at
120 replications. The likely cause is that the smoothing is computed from the same
finite sample it is meant to describe, and I have deliberately not repaired it after
seeing the numbers; the table in Section VII reports the under-coverage as found.</li>

<li><b>The quantisation bound is not attained, and I do not know the sharp constant.</b>
The worst ratio of realised error to the bound of Theorem 5 was 0.31 across 600
instances. Either the bound is loose by a factor of about three or the adversarial
rounding pattern that attains it is rare; I cannot distinguish these from the evidence
here.</li>

<li><b>&beta; is treated as known.</b> Every certificate is conditional on the
temperature. Composing them with an estimated &beta; would need a Lipschitz constant for
the aggregate in &beta;, which Theorem 6 supplies locally but which I do not develop into
a uniform certificate.</li>

<li><b>The Helstrom floor is loose.</b> Its mean slack grows with &beta;, reaching 0.235
at &beta; = 8, so it is a prohibition rather than an estimate. Anyone wanting a tight
error probability should compute it directly rather than read it off the figure.</li>

<li><b>Small instances.</b> Dimensions up to forty in the coarse-graining experiments and
up to eight levels in the quantum ones. The theorems are dimension-free, but
floating-point behaviour at scale &mdash; long sums over many shards, catastrophic
cancellation in the value accumulator &mdash; is exercised only modestly here.</li>

<li><b>No hardware, no hardware claim.</b> Every quantum-adjacent result is computed on
simulated states. The word quantum in this paper refers to the mathematics of density
matrices, and to nothing that was measured.</li>

<li><b>The prior-art claim is hedged, on purpose.</b> Theorem 3 is offered as new
because I could not find it in the mergeability and communication-constrained literature,
not because I searched exhaustively. A reader who knows a counterexample to the novelty
claim has a one-line refutation and should apply it.</li>

<li><b>Verification is not replication.</b> The independent verifier re-derives the
reported numbers from the stored outputs with code that does not import the library. That
establishes freedom from algebra slips and determinism on this machine; it does not
establish that an unrelated implementation would agree, which is what replication means
and what this deposit cannot supply by itself.</li>
</ol>
'''

SEC_XIII = '''
<h2>XIII. Reproducibility</h2>

<h3>A. The claim being made</h3>

<p>The claim is narrower than the word reproducibility usually carries, so it is worth
stating exactly. Everything in this paper is regenerated from source by three commands,
on any machine with NumPy [15] and Matplotlib, with no network access, no data download
and no random seed taken from the clock. That establishes bit-level determinism of the
result set. It does not establish that an independent implementation of the same
mathematics would produce the same numbers to the last digit, and it does not establish
the correctness of the theorems; the proofs do that, and the verifier supports them by
testing the identities numerically with independent code.</p>

<h3>B. Procedure</h3>

<p>From the repository root: <span class="code">python experiments/otaz_run_quantum.py</span>
regenerates all nineteen JSON files in <i>results/</i> from the master seed 2026110101;
<span class="code">python -m pytest tests</span> runs the fifty-two tests; and
<span class="code">python scripts/otaz_verify_quantum.py</span> performs the fifty-six
independent checks and writes a verdict. A fourth command,
<span class="code">python scripts/otaz_checksums.py</span>, writes and verifies the SHA-256
manifest of every shipped file, which catches the failure mode that matters in practice:
a file edited after the results were produced.</p>

<p>Two failure modes have been observed in this repository and are worth warning about.
The experiment script records the SHA-256 of each library module it imports, so editing
<i>core.py</i> without re-running the experiments leaves the recorded hashes stale; the
verifier fails loudly in that case, which is the intended behaviour. And the manuscript
and the figures are built from the stored results rather than recomputed at build time,
so a rebuild is only meaningful after the experiments have run.</p>

<h3>C. What is stored</h3>

<p>Each of the nineteen JSON files records the property under test, the instance counts,
the residuals, the worst-case values and a boolean verdict, in the units the theorem uses.
Nothing is stored as an image of a plot alone; every figure in this paper is drawn from
the same JSON that the tables cite, so a reader who distrusts a figure can recover the
numbers behind it. Appendix B lists the scalars quoted in the text and the file each came
from.</p>
'''

SEC_XIV = '''
<h2>XIV. Conclusion</h2>

<p>This paper took one formula &mdash; a temperature-scaled softmax over scores,
normalising a weighted average of values &mdash; and asked what it does algebraically,
what it costs numerically, what it cannot do, and what can be certified about it. The
answer to the first is that it is a Gibbs average with an additive sufficient statistic,
which means it is a monoid and can be merged in any tree, and that it is neither
idempotent nor homogeneous nor bilinear, with the last defect quantified at 2.1932. The
answer to the second is a set of exact identities with matching error terms: the
derivative in temperature is a covariance, the second derivative a variance, the third a
third cumulant, the coarse-graining gap is an entropy divided by &beta;, and finite
sampling costs a total-variation distance that cannot be amplified by the logit
parameterisation.</p>

<p>The answer to the third question is the result I would keep if I could keep only one.
A fusion operator that carries a score alongside a value needs the normalising mass as
well, not for numerical convenience but for information: with a value-only summary the
merged value is undetermined on the convex hull of the shard values, and no amount of
cleverness recovers it, because the construction is a convex combination and the
combination's weights are exactly the information that was discarded. The minimax rule
over that uncertainty is the midpoint, whose error is half the range and is attained, and
which is never beaten by equal weighting in the instances tested. This is not a theorem
about a software bug; it is a theorem about the operator, and it converts a silent,
systematic error into a stated interval.</p>

<p>The answer to the fourth is a short list of certified statements, each with a
condition of validity that is written down rather than assumed: an error budget for
sampling and truncation composed into one number, a temperature calculus that tells an
analyst what changes and by how much when &beta; moves, and a quantum reading in which
the classical theory is the commuting case and coherence is provably not a rounding
error. Two of those statements are negative &mdash; the certificate saturates, the
coverage falls short &mdash; and they are in the paper because a budget that is only
trusted when it looks good is not a budget.</p>

<p>What remains open is worth naming so the paper does not pretend to completeness. The
sharp constant in the quantised ledger is not known. The composition of a certificate
with an estimated temperature is missing. The empirical question of how often real
aggregation weights fall outside the &delta; for which quantised merging is safe has not
been measured on production data, only argued from a single published tolerance study.
And the minimax statement is one-dimensional in its sharp form; the vector-valued version
is bounded by the diameter but is not sharp, and a practitioner with a vector aggregate
will want the sharp version. Each of these is a question this paper makes precise rather
than one it answers.</p>

<p>If there is a single sentence to carry away it is that the mass is not bookkeeping. It
is the part of the record that makes the fusion invertible, and a system that drops it is
not summarising the data it processed, only the values it happened to touch. The
impossibility theorem in Section IV is the formal content of that sentence, and the
ledger in Section III is the smallest object that satisfies it.</p>
'''
